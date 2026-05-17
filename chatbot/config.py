import os

# Groq Configuration
GROQ_API_KEY = os.environ.get('GROQ_API_KEY', 'gsk_xxx')  
GROQ_BASE_URL = "https://api.groq.com/openai/v1"

PRIMARY_MODEL = "qwen/qwen3-32b"        
FALLBACK_MODEL = "qwen/qwen3-32b"     

MODEL_TEMPERATURE = 0.3
MAX_TOKENS = 300
REQUEST_TIMEOUT = 20
MAX_RETRIES = 2
RATE_LIMIT_DELAY = 0.5  # Groq is FAST

# =========================
# SAFETY THRESHOLDS
# =========================
CONFIDENCE_THRESHOLD = 0.70      # Minimum confidence to provide answer
ESCALATION_THRESHOLD = 0.50      # Below this, escalate to doctor
MAX_CONVERSATION_LENGTH = 20     # Maximum messages in history

# =========================
# UNSAFE QUERY PATTERNS (regex)
# =========================
UNSAFE_PATTERNS = [
    r'\b(stop|quit|discontinue|cease)\s+(taking|medication|medicine|drug|prescription)',
    r'\b(diagnose|diagnosis|what\s+do\s+i\s+have|what\'s\s+wrong\s+with\s+me)',
    r'\b(change|modify|adjust|increase|decrease)\s+(dose|dosage|medication|prescription)',
    r'\b(instead\s+of|replace|substitute)\s+(medication|medicine|drug)',
    r'\b(emergency|urgent|severe\s+pain|chest\s+pain|difficulty\s+breathing)',
]

# =========================
# ESCALATION TRIGGERS
# =========================
ESCALATION_KEYWORDS = [
    'emergency', 'urgent', 'severe', 'chest pain', 'difficulty breathing',
    'unconscious', 'bleeding heavily', 'allergic reaction', 'overdose',
    'suicidal', 'heart attack', 'stroke', 'seizure'
]

# =========================
# RESPONSE TEMPLATES
# =========================
ESCALATION_MESSAGE = (
    "I'm unable to confidently answer this based on your medical records. "
    "Please consult your doctor for medical advice."
)

EMERGENCY_MESSAGE = (
    "⚠️ This sounds like a medical emergency. Please call emergency services "
    "immediately or go to the nearest emergency room. If you're experiencing "
    "severe symptoms, do not wait."
)

UNSAFE_REQUEST_MESSAGE = (
    "I cannot provide guidance on this matter as it involves medical decisions "
    "that require professional consultation. Please speak with your doctor about: {topic}"
)

# =========================
# DIETARY GUIDELINES BY DIAGNOSIS
# =========================
DIETARY_GUIDELINES = {
    'upper respiratory tract infection': {
        'recommended': [
            'Warm fluids (herbal tea, warm water with honey)',
            'Chicken soup or broth',
            'Soft, easy-to-swallow foods',
            'Fruits rich in Vitamin C (oranges, kiwi)',
            'Ginger tea for throat relief'
        ],
        'avoid': [
            'Dairy products (may increase mucus)',
            'Cold beverages',
            'Spicy or acidic foods',
            'Alcohol and caffeine'
        ]
    },
    'allergic rhinitis': {
        'recommended': [
            'Anti-inflammatory foods (turmeric, ginger)',
            'Omega-3 rich foods (salmon, walnuts)',
            'Quercetin-rich foods (apples, onions)',
            'Probiotic foods (yogurt, kefir)',
            'Green tea'
        ],
        'avoid': [
            'Histamine-rich foods (aged cheese, wine)',
            'Processed foods',
            'Foods you\'re allergic to',
            'Excessive sugar'
        ]
    },
    'hypertension': {
        'recommended': [
            'DASH diet foods (fruits, vegetables)',
            'Whole grains',
            'Low-fat dairy',
            'Lean proteins (fish, poultry)',
            'Potassium-rich foods (bananas, spinach)',
            'Foods with magnesium (nuts, seeds)'
        ],
        'avoid': [
            'High sodium foods',
            'Processed and canned foods',
            'Excessive alcohol',
            'Saturated fats',
            'Caffeine (limit intake)'
        ]
    },
    'default': {
        'recommended': [
            'Balanced diet with fruits and vegetables',
            'Adequate hydration (8 glasses of water daily)',
            'Whole grains and lean proteins',
            'Regular meal times'
        ],
        'avoid': [
            'Excessive processed foods',
            'High sugar intake',
            'Excessive alcohol',
            'Foods you\'re allergic to'
        ]
    }
}

# =========================
# MEDICATION TIMING GUIDELINES
# =========================
MEDICATION_TIMING = {
    'with food': 'Take this medication with a meal or snack to reduce stomach upset.',
    'before food': 'Take this medication 30-60 minutes before eating for best absorption.',
    'after food': 'Take this medication after eating to minimize side effects.',
    'with breakfast': 'Take this medication with your morning meal.',
    'in the evening': 'Take this medication in the evening, preferably at the same time each day.',
    'at bedtime': 'Take this medication before going to bed.',
    'twice daily': 'Take this medication approximately 12 hours apart (e.g., 8 AM and 8 PM).',
    'once daily': 'Take this medication at the same time each day for consistency.'
}

# =========================
# SYSTEM PROMPTS (Hardened for Medical Safety)
# =========================
SYSTEM_PROMPT_MEDICAL = """[INST] You are a clinical AI assistant in a hospital patient portal. Respond DIRECTLY to the patient's question using ONLY the provided medical context. 
Do not show your reasoning process. Just briefly answer in 2 to 3 sentences max.

### CRITICAL OUTPUT RULES:
• NEVER show reasoning, thinking steps, or internal monologue
• NEVER start with "Okay", "Let me think", "Based on your records", or "They should"
• ALWAYS address the patient directly as "you" and "your"
• Keep responses to 2-3 concise sentences maximum
• If the query is outside the provided context, respond EXACTLY with: "{escalation_message}"

### PATIENT CONTEXT (USE ONLY THIS INFORMATION):
{patient_context}

### PATIENT QUESTION:
{question}

### YOUR RESPONSE (2-3 sentences, direct answer only):
[/INST]"""

SYSTEM_PROMPT_GENERAL = """[INST] You are a helpful health assistant. Respond DIRECTLY to the user's question. Do not show your reasoning process. Just briefly answer in 2 to 3 sentences max

### OUTPUT RULES:
• NEVER show reasoning or thinking steps
• ALWAYS address the user as "you" and "your"
• Keep responses friendly, concise (2-3 sentences), and actionable
• Encourage consulting healthcare professionals for medical concerns

### USER QUESTION:
{question}

### YOUR RESPONSE (2-3 sentences, direct answer only):
[/INST]"""