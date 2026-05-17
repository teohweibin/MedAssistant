"""
BioMedCLIP Inference with Pre-trained Model (No Training Required)
Uses base BioMedCLIP for zero-shot classification
"""

import os
import sys
import torch
import threading
from PIL import Image
import open_clip
import numpy as np
from datetime import datetime
import traceback

# =========================
# SAFE CONFIG IMPORT
# =========================
try:
    from config import (
        IMAGE_SIZE, HAM10000_CLASSES,
        SEVERITY_MAPPING, ACTION_RECOMMENDATIONS, CONDITION_NOTES,
        CONFIDENCE_THRESHOLD
    )
except ImportError:
    print("⚠️ config.py not found in sys.path. Using built-in fallbacks.")
    IMAGE_SIZE = 224
    HAM10000_CLASSES = {
        'MEL': 'Melanoma',
        'NV': 'Melanocytic nevus',
        'BCC': 'Basal cell carcinoma',
        'AK': 'Actinic keratosis',
        'BKL': 'Benign keratosis',
        'DF': 'Dermatofibroma',
        'VASC': 'Vascular lesion'
    }
    SEVERITY_MAPPING = {
        'MEL': {'level': 'severe', 'score': 9},
        'BCC': {'level': 'moderate-high', 'score': 7},
        'AK': {'level': 'moderate-high', 'score': 7},
        'NV': {'level': 'low', 'score': 2},
        'BKL': {'level': 'low', 'score': 2},
        'DF': {'level': 'low', 'score': 2},
        'VASC': {'level': 'low', 'score': 2},
    }
    ACTION_RECOMMENDATIONS = {
        'severe': 'Seek immediate medical attention. Schedule an urgent dermatology appointment.',
        'moderate-high': 'Consult a dermatologist within 1-2 weeks for professional evaluation.',
        'moderate': 'Monitor for changes. Schedule a routine dermatology check-up.',
        'low': 'Routine monitoring. No immediate action required.'
    }
    CONDITION_NOTES = {k: 'Please consult with a healthcare professional for proper diagnosis.' for k in HAM10000_CLASSES}
    CONFIDENCE_THRESHOLD = 0.30

# =========================
# INFERENCE SERVICE
# =========================
class BioMedCLIPPretrainedInference:
    """Inference service using pre-trained BioMedCLIP (no fine-tuning needed)"""
    
    def __init__(self):
        """Initialize inference service with pre-trained model"""
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"🖥️ BioMedCLIP using device: {self.device}")
        
        print("⏳ Loading pre-trained BioMedCLIP model from HuggingFace Hub...")
        try:
            model_name = 'hf-hub:microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224'
            self.model, _, self.preprocess = open_clip.create_model_and_transforms(model_name)
            self.tokenizer = open_clip.get_tokenizer(model_name)
            
            self.model.to(self.device)
            self.model.eval()
            
            # Pre-encode text prompts
            self.condition_texts = [
                f"A dermatoscopic image of {desc.lower()}"
                for desc in HAM10000_CLASSES.values()
            ]
            self.condition_labels = list(HAM10000_CLASSES.keys())
            
            with torch.no_grad():
                text_tokens = self.tokenizer(self.condition_texts).to(self.device)
                self.text_features = self.model.encode_text(text_tokens)
                self.text_features /= self.text_features.norm(dim=-1, keepdim=True)
            
            print("✅ BioMedCLIP loaded successfully (zero-shot ready)")
            
        except Exception as e:
            print(f"❌ FATAL: Failed to load BioMedCLIP model:")
            print(traceback.format_exc())
            raise RuntimeError(f"Model loading failed: {e}")
    
    def preprocess_image(self, image):
        """Preprocess image for inference"""
        if isinstance(image, str):
            image = Image.open(image).convert('RGB')
        elif not isinstance(image, Image.Image):
            raise ValueError("Image must be a PIL Image or file path")
        else:
            image = image.convert('RGB')
            
        return self.preprocess(image).unsqueeze(0).to(self.device)
    
    def predict(self, image):
        """Perform zero-shot classification"""
        image_tensor = self.preprocess_image(image)
        
        with torch.no_grad():
            image_features = self.model.encode_image(image_tensor)
            image_features /= image_features.norm(dim=-1, keepdim=True)
            similarity = (100.0 * image_features @ self.text_features.T).softmax(dim=-1)
        
        probs = similarity.cpu().numpy()[0]
        sorted_indices = np.argsort(probs)[::-1]
        
        return [
            {
                'label': self.condition_labels[idx],
                'condition': HAM10000_CLASSES[self.condition_labels[idx]],
                'confidence': float(probs[idx])
            }
            for idx in sorted_indices[:3]
        ]
    
    def analyze_symptom(self, image):
        """Analyze symptom and provide comprehensive assessment"""
        try:
            predictions = self.predict(image)
            if not predictions:
                return {'success': False, 'error': 'No predictions generated'}
                
            top_prediction = predictions[0]
            label = top_prediction['label']
            confidence = top_prediction['confidence']
            
            if confidence < CONFIDENCE_THRESHOLD:
                return {
                    'success': False,
                    'error': 'Low confidence prediction',
                    'message': f'Confidence too low ({confidence:.2%}). Please provide a clearer image.',
                    'confidence': confidence
                }
            
            severity_info = SEVERITY_MAPPING.get(label, {'level': 'moderate', 'score': 5})
            recommended_action = ACTION_RECOMMENDATIONS.get(severity_info['level'], ACTION_RECOMMENDATIONS['moderate'])
            additional_notes = CONDITION_NOTES.get(label, 'Consult a healthcare professional for proper diagnosis.')
            
            return {
                'success': True,
                'analysis': {
                    'condition': top_prediction['condition'],
                    'condition_code': label,
                    'confidence': confidence,
                    'severity': severity_info['level'],
                    'severity_score': severity_info['score'],
                    'recommended_action': recommended_action,
                    'additional_notes': additional_notes,
                    'timestamp': datetime.now().isoformat(),
                    'alternative_diagnoses': [
                        {'condition': p['condition'], 'confidence': p['confidence']}
                        for p in predictions[1:] if p['confidence'] > 0.05
                    ],
                    'model_info': 'Pre-trained BioMedCLIP (zero-shot classification)'
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            }


# =========================
# THREAD-SAFE SINGLETON
# =========================
_inference_service = None
_init_lock = threading.Lock()

def get_inference_service():
    """Get or create inference service instance (thread-safe)"""
    global _inference_service
    if _inference_service is None:
        with _init_lock:
            if _inference_service is None:  # Double-check
                _inference_service = BioMedCLIPPretrainedInference()
    return _inference_service

def analyze_image(image):
    """Convenience function"""
    return get_inference_service().analyze_symptom(image)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python inference_pretrained.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        sys.exit(1)
        
    print(f"\n🔍 Analyzing: {image_path}\n")
    try:
        result = analyze_image(image_path)
        if result.get('success'):
            a = result['analysis']
            print(f"🏥 Condition: {a['condition']}")
            print(f"📈 Confidence: {a['confidence']:.2%}")
            print(f"⚠️ Severity: {a['severity'].upper()} (Score: {a['severity_score']}/10)")
            print(f"💡 Action: {a['recommended_action']}")
        else:
            print(f"❌ Failed: {result.get('message') or result.get('error')}")
    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()