"""
Patient Context Retriever
Extracts and formats patient medical information for chatbot context
"""

import json
import os
import threading
from typing import Dict, List, Optional, Any


class PatientContextRetriever:
    """Retrieves and formats patient medical context from JSON data"""
    
    def __init__(self, patients_data_path: str = None):
        """Initialize context retriever with thread-safe path resolution"""
        # Resolve path relative to this file's directory (works regardless of CWD)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.patients_data_path = patients_data_path or os.path.join(base_dir, '..', 'data', 'patients.json')
        self.patients_data = {}
        self._load_patients_data()
        self._lock = threading.Lock()
    
    def _load_patients_data_raw(self) -> Dict:
        """Internal method to safely load JSON"""
        try:
            with open(self.patients_data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️ Warning: {self.patients_data_path} not found")
            return {}
        except json.JSONDecodeError as e:
            print(f"⚠️ Warning: Error parsing {self.patients_data_path}: {e}")
            return {}
        except Exception as e:
            print(f"⚠️ Warning: Unexpected error loading {self.patients_data_path}: {e}")
            return {}

    def refresh(self):
        """Reload data from JSON file to catch external updates"""
        with self._lock:
            self.patients_data = self._load_patients_data_raw()

    def _load_patients_data(self):
        """Initial load"""
        self.patients_data = self._load_patients_data_raw()
    
    def get_patient_context(self, patient_id: str) -> Optional[Dict[str, Any]]:
        """Get complete patient context (defensive .get() usage)"""
        patient = self.patients_data.get(patient_id)
        if not patient:
            return None
        
        return {
            'patient_id': patient.get('patient_id', patient_id),
            'patient_name': patient.get('patient_name', 'Unknown'),
            'patient_age': patient.get('patient_age', 'N/A'),
            'blood_group': patient.get('blood_group', 'Unknown'),
            'allergies': patient.get('allergies', []),
            'current_symptom': patient.get('symptom', 'None reported'),
            'diagnosis': patient.get('diagnosis', 'Pending'),
            'prescriptions': patient.get('prescription', []),
            'emergency_contact': patient.get('emergency_contact', {})
        }
    
    def get_formatted_context(self, patient_id: str) -> str:
        """Get formatted patient context as a string for LLM"""
        context = self.get_patient_context(patient_id)
        if not context:
            return "No patient data available."
        
        # ✅ FIXED: Safe prescription formatting (prevents KeyError on missing 'duration')
        prescriptions_text = ""
        if context['prescriptions']:
            prescriptions_list = []
            for med in context['prescriptions']:
                med_name = med.get('medication', 'Unknown Medication')
                dosage = med.get('dosage', 'Unspecified')
                duration = med.get('duration', 'Not specified')
                notes = med.get('notes', '')
                
                med_text = f"  - {med_name}: {dosage}, {duration}"
                if notes:
                    med_text += f" ({notes})"
                prescriptions_list.append(med_text)
            prescriptions_text = "\n".join(prescriptions_list)
        else:
            prescriptions_text = "  None"
        
        allergies_text = ", ".join(context['allergies']) if context['allergies'] else "None"
        
        return f"""
PATIENT MEDICAL CONTEXT:

Patient Information:
- Name: {context['patient_name']}
- Age: {context['patient_age']} years
- Blood Group: {context['blood_group']}

Allergies: {allergies_text}

Current Diagnosis: {context['diagnosis']}

Current Symptoms: {context['current_symptom']}

Current Prescriptions:
{prescriptions_text}

IMPORTANT: Only provide information based on this medical context. Do not invent or assume any medical information not explicitly stated above.
""".strip()
    
    def get_prescriptions(self, patient_id: str) -> List[Dict]:
        context = self.get_patient_context(patient_id)
        return context['prescriptions'] if context else []
    
    def get_allergies(self, patient_id: str) -> List[str]:
        context = self.get_patient_context(patient_id)
        return context['allergies'] if context else []
    
    def get_diagnosis(self, patient_id: str) -> Optional[str]:
        context = self.get_patient_context(patient_id)
        return context['diagnosis'] if context else None
    
    def find_medication(self, patient_id: str, medication_name: str) -> Optional[Dict]:
        prescriptions = self.get_prescriptions(patient_id)
        medication_name_lower = medication_name.lower()
        
        for med in prescriptions:
            # ✅ FIXED: Safe key access
            if medication_name_lower in med.get('medication', '').lower():
                return med
        return None
    
    def has_allergy(self, patient_id: str, substance: str) -> bool:
        allergies = self.get_allergies(patient_id)
        substance_lower = substance.lower()
        return any(substance_lower in allergy.lower() for allergy in allergies)
    
    def get_medication_summary(self, patient_id: str) -> str:
        prescriptions = self.get_prescriptions(patient_id)
        if not prescriptions:
            return "You currently have no active prescriptions."
        
        summary = "Your current medications:\n\n"
        for i, med in enumerate(prescriptions, 1):
            summary += f"{i}. **{med.get('medication', 'Unknown')}**\n"
            summary += f"   - Dosage: {med.get('dosage', 'Unspecified')}\n"
            summary += f"   - Duration: {med.get('duration', 'Not specified')}\n"
            if med.get('notes'):
                summary += f"   - Instructions: {med['notes']}\n"
            summary += "\n"
        
        return summary.strip()
    
    def get_allergy_warning(self, patient_id: str) -> str:
        allergies = self.get_allergies(patient_id)
        if not allergies:
            return ""
        return f"⚠️ **Allergy Alert**: You are allergic to: {', '.join(allergies)}"
    
    def validate_patient_exists(self, patient_id: str) -> bool:
        return patient_id in self.patients_data


# =========================
# THREAD-SAFE SINGLETON
# =========================
_context_retriever = None
_init_lock = threading.Lock()

def get_context_retriever() -> PatientContextRetriever:
    """Get or create context retriever instance (thread-safe)"""
    global _context_retriever
    if _context_retriever is None:
        with _init_lock:
            if _context_retriever is None:
                _context_retriever = PatientContextRetriever()
    return _context_retriever