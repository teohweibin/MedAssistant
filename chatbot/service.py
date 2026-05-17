"""
Chatbot Service
Main service for handling chatbot queries with LLM integration
Updated to use Groq API (fast, reliable, free-tier) with template fallback
"""

import json
import time
import threading
from typing import Dict, List, Optional
from datetime import datetime

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

from .context import PatientContextRetriever, get_context_retriever
from .safety import SafetyValidator, get_safety_validator
from .templates import ResponseTemplates
from .config import (
    GROQ_API_KEY,
    PRIMARY_MODEL,
    FALLBACK_MODEL,
    MODEL_TEMPERATURE,
    MAX_TOKENS,
    REQUEST_TIMEOUT,
    MAX_RETRIES,
    RATE_LIMIT_DELAY,
    SYSTEM_PROMPT_MEDICAL,
    SYSTEM_PROMPT_GENERAL,  # ✅ ADDED: Missing import was causing crashes
    ESCALATION_MESSAGE,
    MAX_CONVERSATION_LENGTH
)


class ChatbotService:
    """Main chatbot service with LLM integration"""
    
    def __init__(self):
        """Initialize chatbot service"""
        self._lock = threading.Lock()
        self.context_retriever = get_context_retriever()
        self.safety_validator = get_safety_validator()
        self.templates = ResponseTemplates()
        self.conversation_history: Dict[str, List[Dict]] = {}
        self.llm_available = False
        self.last_request_time = 0
        self.groq_client = None

        # Initialize Groq client if configured
        if GROQ_AVAILABLE and GROQ_API_KEY and not GROQ_API_KEY.startswith('gsk_xxx'):
            try:
                self.groq_client = Groq(api_key=GROQ_API_KEY)
                print("✓ Groq client initialized successfully")
            except Exception as e:
                print(f"⚠️ Groq client initialization failed: {e}")

        # Check LLM availability in background
        threading.Thread(target=self._init_llm_check, daemon=True).start()
    
    def _init_llm_check(self):
        """Test Groq API connectivity"""
        if not self.groq_client:
            print("⚠️ Groq not configured. Using template-based responses.")
            return
        try:
            # Quick test query
            self.groq_client.chat.completions.create(
                model=PRIMARY_MODEL,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5,
                temperature=0.1
            )
            self.llm_available = True
            print(f"✓ LLM mode enabled ({PRIMARY_MODEL})")
        except Exception as e:
            print(f"⚠️ LLM API test failed: {e}. Using template-based responses.")
    
    def process_query(
        self,
        patient_id: str,
        query: str,
        session_id: Optional[str] = None
    ) -> Dict:
        """Process user query and generate response"""
        try:
            # Refresh context to sync with latest JSON data
            self.context_retriever.refresh()
            
            # Validate patient exists
            if not self.context_retriever.validate_patient_exists(patient_id):
                return {
                    'success': False,
                    'error': 'Patient not found',
                    'message': 'Unable to retrieve patient information.'
                }
            
            # Validate query safety
            is_safe, error_message = self.safety_validator.validate_query(query)
            if not is_safe:
                return {
                    'success': True,
                    'response': error_message,
                    'type': 'safety_block',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Get patient context (DEFENSIVE: use .get() to prevent KeyError)
            patient_context = self.context_retriever.get_patient_context(patient_id) or {}
            if not patient_context:
                return {
                    'success': False,
                    'error': 'Patient context unavailable',
                    'message': 'Unable to retrieve patient medical information.'
                }
            
            # Classify query type
            query_type = self._classify_query(query)
            
            # Handle template-based responses first (fastest path)
            template_response = self._try_template_response(query, query_type, patient_context)
            if template_response:
                return {
                    'success': True,
                    'response': template_response,
                    'type': query_type,
                    'source': 'template',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Generate LLM response if available
            if self.llm_available:
                response = self._generate_llm_response(query, patient_context, query_type, session_id)
            else:
                response = self._generate_fallback_response(query, query_type, patient_context)
            
            # Validate response safety
            is_safe, modified_response = self.safety_validator.validate_response(
                response, patient_context, confidence=0.8
            )
            if modified_response:
                response = modified_response
            
            # Store in conversation history
            if session_id and response:
                self._add_to_history(session_id, query, response)
            
            return {
                'success': True,
                'response': response,
                'type': query_type,
                'source': 'llm' if self.llm_available else 'fallback',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"🔴 Chatbot process_query failed: {e}")
            import traceback
            traceback.print_exc()
            return {
                'success': True,
                'response': "I'm experiencing a temporary issue. Please try again in a moment.",
                'type': 'error',
                'source': 'system',
                'timestamp': datetime.now().isoformat()
            }
    
    def _classify_query(self, query: str) -> str:
        query_lower = query.lower()
        if any(w in query_lower for w in ['medication', 'medicine', 'prescription', 'pill', 'drug', 'dose']):
            return 'medication'
        if any(w in query_lower for w in ['food', 'eat', 'diet', 'nutrition', 'meal']):
            return 'dietary'
        if any(w in query_lower for w in ['appointment', 'schedule', 'book', 'visit', 'consultation']):
            return 'appointment'
        if any(w in query_lower for w in ['allergy', 'allergic', 'allergen']):
            return 'allergy'
        if any(w in query_lower for w in ['hello', 'hi', 'hey', 'greetings']):
            return 'greeting'
        if any(w in query_lower for w in ['bye', 'goodbye', 'thanks', 'thank you']):
            return 'farewell'
        return 'general'
    
    def _try_template_response(self, query: str, query_type: str, patient_context: Dict) -> Optional[str]:
        query_lower = query.lower()
        
        if query_type == 'greeting':
            return self.templates.greeting(patient_context.get('patient_name', 'there'))
        if query_type == 'farewell':
            return self.templates.farewell()
        if 'list' in query_lower and 'medication' in query_lower:
            return self.templates.medication_list(patient_context.get('prescriptions', []))
        if query_type == 'allergy' or 'allerg' in query_lower:
            return self.templates.allergy_information(patient_context.get('allergies', []))
        if query_type == 'dietary' and 'should i eat' in query_lower:
            return self.templates.dietary_advice(
                patient_context.get('diagnosis', 'your condition'),
                patient_context.get('allergies', [])
            )
        if query_type == 'appointment' and any(w in query_lower for w in ['book', 'schedule']):
            return self.templates.appointment_booking_nudge()
        if query_type == 'medication':
            for prescription in patient_context.get('prescriptions', []):
                med_name = prescription.get('medication', '').split()[0].lower()
                if med_name in query_lower:
                    return self.templates.medication_guidance(prescription)
        if 'side effect' in query_lower:
            return self.templates.side_effects_response()
        if any(w in query_lower for w in ['worse', 'worsening', 'getting worse']):
            return self.templates.symptom_worsening_response()
        return None
    
    def _generate_llm_response(self, query: str, patient_context: Dict, query_type: str, session_id: Optional[str]) -> str:
        model = PRIMARY_MODEL if query_type in ['medication', 'allergy'] else FALLBACK_MODEL
        system_prompt = self._get_system_prompt(query_type)
        
        history = self._get_history(session_id) if session_id else []
        patient_info = self.context_retriever.get_formatted_context(patient_context.get('patient_id', 'unknown'))
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "system", "content": f"Patient Context:\n{patient_info}"}
        ]
        for msg in history[-6:]:
            messages.append({"role": "user", "content": msg['query']})
            messages.append({"role": "assistant", "content": msg['response']})
        messages.append({"role": "user", "content": query})
        
        self._apply_rate_limit()
        
        for attempt in range(MAX_RETRIES + 1):
            try:
                if not self.groq_client:
                    raise RuntimeError("Groq client not initialized")
                
                response = self.groq_client.chat.completions.create(
                    model=model,  # gpt-oss-20b
                    messages=messages,
                    temperature=MODEL_TEMPERATURE,
                    max_tokens=MAX_TOKENS,
                    stop=[
                        "\n\nOkay", "\n\nLet me", "\n\nFirst",  "\n\nBased on the",  # Explanation starters
                    ]
                )
                
                if response.choices and response.choices[0].message.content:
                    return response.choices[0].message.content.strip()  # ✅ Direct return
                
                if attempt == 0 and model == PRIMARY_MODEL:
                    model = FALLBACK_MODEL
                    continue
                    
            except Exception as e:
                print(f"⚠️ LLM Attempt {attempt + 1} failed: {e}")
                if attempt < MAX_RETRIES:
                    time.sleep(2 ** attempt)
        
        print("⚠️ All LLM attempts failed. Using template fallback.")
        return self._generate_fallback_response(query, query_type, patient_context)
    
    def _apply_rate_limit(self):
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < RATE_LIMIT_DELAY:
            time.sleep(RATE_LIMIT_DELAY - time_since_last)
        self.last_request_time = time.time()
    
    def _generate_fallback_response(self, query: str, query_type: str, patient_context: Dict) -> str:
        if query_type == 'medication':
            return self.templates.medication_list(patient_context.get('prescriptions', []))
        elif query_type == 'dietary':
            return self.templates.dietary_advice(
                patient_context.get('diagnosis', 'your condition'),
                patient_context.get('allergies', [])
            )
        elif query_type == 'appointment':
            return self.templates.appointment_booking_nudge()
        elif query_type == 'allergy':
            return self.templates.allergy_information(patient_context.get('allergies', []))
        else:
            return (
                "I can help you with:\n"
                "• Medication information\n"
                "• Dietary advice\n"
                "• Appointment scheduling\n"
                "• Allergy information\n\n"
                "Please ask a specific question about any of these topics!"
            )
    
    def _add_to_history(self, session_id: str, query: str, response: str):
        if session_id not in self.conversation_history:
            self.conversation_history[session_id] = []
        self.conversation_history[session_id].append({
            'query': query,
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
        if len(self.conversation_history[session_id]) > MAX_CONVERSATION_LENGTH:
            self.conversation_history[session_id] = \
                self.conversation_history[session_id][-MAX_CONVERSATION_LENGTH:]
    
    def _get_history(self, session_id: str) -> List[Dict]:
        return self.conversation_history.get(session_id, [])
    
    def get_conversation_history(self, session_id: str) -> List[Dict]:
        return self._get_history(session_id)
    
    def clear_conversation_history(self, session_id: str):
        self.conversation_history.pop(session_id, None)

    def _get_system_prompt(self, query_type: str) -> str:
        # Strict medical prompt for high-stakes queries
        if query_type in ['medication', 'allergy']:
            return SYSTEM_PROMPT_MEDICAL.replace("{escalation_message}", ESCALATION_MESSAGE)
        
        # Flexible general prompt for wellness/lifestyle queries
        elif query_type in ['dietary', 'appointment', 'greeting', 'farewell', 'general']:
            return SYSTEM_PROMPT_GENERAL
        
        # Default to medical for safety
        return SYSTEM_PROMPT_MEDICAL.replace("{escalation_message}", ESCALATION_MESSAGE)

# =========================
# THREAD-SAFE SINGLETON
# =========================
_chatbot_service = None
_init_lock = threading.Lock()

def get_chatbot_service() -> ChatbotService:
    global _chatbot_service
    if _chatbot_service is None:
        with _init_lock:
            if _chatbot_service is None:
                _chatbot_service = ChatbotService()
    return _chatbot_service