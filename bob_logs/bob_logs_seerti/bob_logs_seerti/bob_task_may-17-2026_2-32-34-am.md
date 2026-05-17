**User:**

<task>
Fix any issues in the following code from file path app.py:218-218

Current problems detected:
- [basedpyright] "eos_token_id" is not a known attribute of "None" ([object Object])


```
eos_token_id
```

Please:
1. Address all detected problems listed above (if any)
2. Identify any other potential bugs or issues
3. Provide corrected code
4. Explain what was fixed and why
</task>
<environment_details>
# VSCode Visible Files
app.py

# VSCode Open Tabs
templates/schedule.html,templates/appointments.html,templates/profile.html,templates/assistant.html,app.py,static/style.css

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T18:25:29.658Z
User time zone: Asia/Kuala_Lumpur, UTC+8:00

# Current Cost
$0.00

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>


# Current Workspace Directory (c:/Users/noname/IBM Bob Hackathon/Clinic AI Suvan/ibm_bob_hackathon-clinical_ai) Files
app.py
README.md
static/
static/style.css
templates/
templates/appointments.html
templates/assistant.html
templates/profile.html
templates/schedule.html
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I'll start by reading the app.py file to understand the context around line 218 and identify the issue with `eos_token_id`.

<read_file>
<args>
<file>
<path>app.py</path>
<line_range>200-240</line_range>
</file>
</args>
</read_file>

---

**User:**

[read_file for 'app.py'. Reading multiple files at once is more efficient for the LLM. If other files are relevant to your current task, please read them simultaneously.] Result:
<files>
<file><path>app.py</path>
<content lines="200-240">
200 | 
201 | def query_ai_model(prompt):
202 |     """
203 |     Query the local TinyLlama model
204 |     Returns the AI-generated text or an error message
205 |     """
206 |     if pipe is None:
207 |         return {
208 |             'error': True,
209 |             'message': "Local AI model is not available. Please ensure transformers and torch are installed."
210 |         }
211 |     
212 |     try:
213 |         # Construct prompt in TinyLlama chat format
214 |         formatted_prompt = f"<|system|>\nYou are a helpful medical assistant.</s>\n<|user|>\n{prompt}</s>\n<|assistant|>\n"
215 |         
216 |         # Get tokenizer's eos_token_id safely
217 |         try:
218 |             eos_token = pipe.tokenizer.eos_token_id
219 |         except:
220 |             eos_token = 2  # Default EOS token ID for most models
221 |         
222 |         # Suppress warnings by using generation_config=None and explicit parameters
223 |         import warnings
224 |         with warnings.catch_warnings():
225 |             warnings.filterwarnings("ignore", category=UserWarning)
226 |             
227 |             # Generate response
228 |             outputs = pipe(
229 |                 formatted_prompt,
230 |                 max_new_tokens=200,
231 |                 temperature=0.7,
232 |                 top_p=0.9,
233 |                 do_sample=True,
234 |                 return_full_text=False,
235 |                 pad_token_id=eos_token,
236 |                 eos_token_id=eos_token
237 |             )
238 |         
239 |         # Extract generated text
240 |         if outputs and len(outputs) > 0:
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
app.py

# VSCode Open Tabs
templates/schedule.html,templates/appointments.html,templates/profile.html,templates/assistant.html,app.py,static/style.css

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T18:25:32.795Z
User time zone: Asia/Kuala_Lumpur, UTC+8:00

# Current Cost
$0.01

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

Now let me read more context to understand how `pipe` is initialized and what type it is:

<read_file>
<args>
<file>
<path>app.py</path>
<line_range>1-50</line_range>
</file>
</args>
</read_file>

---

**User:**

[read_file for 'app.py'. Reading multiple files at once is more efficient for the LLM. If other files are relevant to your current task, please read them simultaneously.] Result:
<files>
<file><path>app.py</path>
<content lines="1-50">
 1 | from flask import Flask, render_template, request, jsonify
 2 | from datetime import datetime, timedelta
 3 | 
 4 | app = Flask(__name__)
 5 | 
 6 | # Initialize Local LLM (TinyLlama - smaller, faster, more reliable)
 7 | print("Loading TinyLlama model... This may take a few minutes on first run.")
 8 | pipe = None
 9 | try:
10 |     import torch
11 |     from transformers import pipeline
12 |     
13 |     # Use TinyLlama - much more reliable and faster for hackathons
14 |     pipe = pipeline(
15 |         "text-generation",
16 |         model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
17 |         device_map="auto"
18 |     )
19 |     print("✓ TinyLlama model loaded successfully!")
20 |     print("  Model size: ~1.1B parameters (~2GB)")
21 | except ImportError as e:
22 |     print(f"⚠️ Warning: Required packages not installed: {e}")
23 |     print("   Please run: pip install torch transformers accelerate")
24 | except Exception as e:
25 |     print(f"⚠️ Warning: Could not load TinyLlama model: {e}")
26 |     print(f"   Error type: {type(e).__name__}")
27 |     print("   The app will continue with built-in knowledge base responses.")
28 | 
29 | # Mock data for available time slots
30 | available_slots = {
31 |     '2026-05-17': ['09:00 AM', '10:00 AM', '11:00 AM', '02:00 PM', '03:00 PM', '04:00 PM'],
32 |     '2026-05-18': ['09:00 AM', '10:00 AM', '11:00 AM', '02:00 PM', '03:00 PM'],
33 |     '2026-05-19': ['09:00 AM', '11:00 AM', '02:00 PM', '03:00 PM', '04:00 PM'],
34 |     '2026-05-20': ['10:00 AM', '11:00 AM', '02:00 PM', '03:00 PM', '04:00 PM'],
35 |     '2026-05-21': ['09:00 AM', '10:00 AM', '02:00 PM', '03:00 PM'],
36 | }
37 | 
38 | # Mock data for booked appointments
39 | booked_appointments = []
40 | 
41 | # Mock data for medication reminders
42 | medication_reminders = [
43 |     {
44 |         'medication': 'Amoxicillin 500mg',
45 |         'time': '08:00 AM',
46 |         'frequency': 'Twice daily',
47 |         'notes': 'Take with food'
48 |     },
49 |     {
50 |         'medication': 'Vitamin D3',
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
app.py

# VSCode Open Tabs
templates/schedule.html,templates/appointments.html,templates/profile.html,templates/assistant.html,app.py,static/style.css

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T18:25:35.740Z
User time zone: Asia/Kuala_Lumpur, UTC+8:00

# Current Cost
$0.02

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

Now I understand the issue. The problem is that `pipe` is initialized as `None` at line 8, and when the model fails to load (lines 21-27), it remains `None`. The type checker (basedpyright) is correctly identifying that at line 218, `pipe.tokenizer` could be `None.tokenizer`, which would cause an AttributeError.

The code already has a check at line 206 to return early if `pipe is None`, but the type checker doesn't recognize this as sufficient type narrowing. Additionally, there's a try-except block (lines 217-220) that attempts to handle the error, but the type checker still flags it.

Let me fix this issue by adding proper type narrowing and improving the error handling:

<apply_diff>
<path>app.py</path>
<diff>
<<<<<<< SEARCH
:start_line:216
-------
        # Get tokenizer's eos_token_id safely
        try:
            eos_token = pipe.tokenizer.eos_token_id
        except:
            eos_token = 2  # Default EOS token ID for most models
=======
        # Get tokenizer's eos_token_id safely
        try:
            eos_token = pipe.tokenizer.eos_token_id if pipe.tokenizer.eos_token_id is not None else 2
        except (AttributeError, TypeError):
            eos_token = 2  # Default EOS token ID for most models
>>>>>>> REPLACE
</diff>
</apply_diff>

---

**User:**

[apply_diff for 'app.py'] Result:
<file_write_result>
<path>app.py</path>
<operation>modified</operation>
<problems>

New problems detected after saving the file:
app.py
- [basedpyright Error] 218 |             eos_token = pipe.tokenizer.eos_token_id if pipe.tokenizer.eos_token_id is not None else 2 : "eos_token_id" is not a known attribute of "None"</problems>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
</notice>
</file_write_result>

<notice>Making multiple related changes in a single apply_diff is more efficient. If other changes are needed in this file, please include them as additional SEARCH/REPLACE blocks.</notice>
<environment_details>
# VSCode Visible Files
app.py

# VSCode Open Tabs
templates/schedule.html,templates/appointments.html,templates/profile.html,templates/assistant.html,app.py,static/style.css

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T18:25:45.170Z
User time zone: Asia/Kuala_Lumpur, UTC+8:00

# Current Cost
$0.03

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

The issue persists because the type checker still sees `pipe` as potentially `None`. Let me fix this by adding a proper type assertion after the None check:

<apply_diff>
<path>app.py</path>
<diff>
<<<<<<< SEARCH
:start_line:206
-------
    if pipe is None:
        return {
            'error': True,
            'message': "Local AI model is not available. Please ensure transformers and torch are installed."
        }
    
    try:
        # Construct prompt in TinyLlama chat format
        formatted_prompt = f"<|system|>\nYou are a helpful medical assistant.</s>\n<|user|>\n{prompt}</s>\n<|assistant|>\n"
        
        # Get tokenizer's eos_token_id safely
        try:
            eos_token = pipe.tokenizer.eos_token_id if pipe.tokenizer.eos_token_id is not None else 2
        except (AttributeError, TypeError):
            eos_token = 2  # Default EOS token ID for most models
=======
    if pipe is None:
        return {
            'error': True,
            'message': "Local AI model is not available. Please ensure transformers and torch are installed."
        }
    
    try:
        # Construct prompt in TinyLlama chat format
        formatted_prompt = f"<|system|>\nYou are a helpful medical assistant.</s>\n<|user|>\n{prompt}</s>\n<|assistant|>\n"
        
        # Get tokenizer's eos_token_id safely
        try:
            # Access tokenizer safely with proper null checks
            tokenizer = pipe.tokenizer
            eos_token = tokenizer.eos_token_id if tokenizer and hasattr(tokenizer, 'eos_token_id') and tokenizer.eos_token_id is not None else 2
        except (AttributeError, TypeError):
            eos_token = 2  # Default EOS token ID for most models
>>>>>>> REPLACE
</diff>
</apply_diff>

---

**User:**

[apply_diff for 'app.py'] Result:
<file_write_result>
<path>app.py</path>
<operation>modified</operation>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
</notice>
</file_write_result>

<notice>Making multiple related changes in a single apply_diff is more efficient. If other changes are needed in this file, please include them as additional SEARCH/REPLACE blocks.</notice>
<environment_details>
# VSCode Visible Files
app.py

# VSCode Open Tabs
templates/schedule.html,templates/appointments.html,templates/profile.html,templates/assistant.html,app.py,static/style.css

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T18:25:54.225Z
User time zone: Asia/Kuala_Lumpur, UTC+8:00

# Current Cost
$0.05

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<attempt_completion>
<result>
Fixed the type checking error in app.py at line 218. The issue was that the type checker (basedpyright) couldn't determine that `pipe` was not `None` when accessing `pipe.tokenizer.eos_token_id`.

**Changes made:**

1. **Added intermediate variable**: Extracted `pipe.tokenizer` into a `tokenizer` variable for clearer null checking
2. **Enhanced null safety**: Added explicit checks using `hasattr()` to verify the attribute exists before accessing it
3. **Improved error handling**: Changed bare `except` to specific exception types `(AttributeError, TypeError)`

**What was fixed:**
- The original code had `pipe.tokenizer.eos_token_id` which the type checker flagged because `pipe` could theoretically be `None` (even though there's a guard clause)
- The new code safely extracts the tokenizer first, then checks if it exists and has the `eos_token_id` attribute before accessing it
- This satisfies the type checker while maintaining the same runtime behavior with a fallback to token ID `2`

**Why this works:**
- The intermediate `tokenizer` variable helps the type checker understand the flow
- The `hasattr()` check provides explicit attribute verification
- The fallback value of `2` is used if any check fails, ensuring the code always has a valid token ID
</result>
</attempt_completion>

---

**User:**

[attempt_completion] Result:
The user has provided feedback on the results. Consider their input to continue the task, and then attempt completion again.
<feedback>
Role: You are a Backend Engineer simplifying the AI integration for a hackathon project.

Context: We are removing the complex transformers and torch dependencies. We are switching to Ollama for local AI inference.

Why Ollama? It runs as a local server (usually on port 11434) and requires no heavy Python libraries inside the Flask app, making it extremely stable and fast to set up.

Implementation Instructions:

1. Dependencies:

Remove transformers, torch, and accelerate.
We only need the standard requests library (which is already installed).
2. Backend Updates (app.py):

Configuration: Change the API_URL to http://localhost:11434/api/generate.
Update query_ai_model function:
Use the requests library to POST to the Ollama API.
Payload Format:
python

payload = {
    "model": "llama3",  # or "mistral"
    "prompt": system_prompt,
    "stream": False
}
Response Parsing: Ollama returns JSON with a key "response". Extract this text.
Error Handling: If connection is refused, return a message telling the user to "Ensure Ollama is running (ollama serve)".
3. Cleanup:

Remove any code related to pipeline, device_map, or model initialization objects.
Keep the existing Safety Guardrails (check_response_safety, SAFETY_KEYWORDS) exactly as they are.
Output Format:
Provide the complete updated app.py.
</feedback>
<environment_details>
# VSCode Visible Files
app.py

# VSCode Open Tabs
templates/schedule.html,templates/appointments.html,templates/profile.html,templates/assistant.html,app.py,static/style.css

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T18:31:09.561Z
User time zone: Asia/Kuala_Lumpur, UTC+8:00

# Current Cost
$0.07

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I'll refactor the app.py to use Ollama instead of the transformers library. Let me first read the complete file to understand all the code that needs to be updated.

<read_file>
<args>
<file>
<path>app.py</path>
</file>
</args>
</read_file>

---

**User:**

[read_file for 'app.py'. Reading multiple files at once is more efficient for the LLM. If other files are relevant to your current task, please read them simultaneously.] Result:
<files>
<file><path>app.py</path>
<content lines="1-608">
  1 | from flask import Flask, render_template, request, jsonify
  2 | from datetime import datetime, timedelta
  3 | 
  4 | app = Flask(__name__)
  5 | 
  6 | # Initialize Local LLM (TinyLlama - smaller, faster, more reliable)
  7 | print("Loading TinyLlama model... This may take a few minutes on first run.")
  8 | pipe = None
  9 | try:
 10 |     import torch
 11 |     from transformers import pipeline
 12 |     
 13 |     # Use TinyLlama - much more reliable and faster for hackathons
 14 |     pipe = pipeline(
 15 |         "text-generation",
 16 |         model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
 17 |         device_map="auto"
 18 |     )
 19 |     print("✓ TinyLlama model loaded successfully!")
 20 |     print("  Model size: ~1.1B parameters (~2GB)")
 21 | except ImportError as e:
 22 |     print(f"⚠️ Warning: Required packages not installed: {e}")
 23 |     print("   Please run: pip install torch transformers accelerate")
 24 | except Exception as e:
 25 |     print(f"⚠️ Warning: Could not load TinyLlama model: {e}")
 26 |     print(f"   Error type: {type(e).__name__}")
 27 |     print("   The app will continue with built-in knowledge base responses.")
 28 | 
 29 | # Mock data for available time slots
 30 | available_slots = {
 31 |     '2026-05-17': ['09:00 AM', '10:00 AM', '11:00 AM', '02:00 PM', '03:00 PM', '04:00 PM'],
 32 |     '2026-05-18': ['09:00 AM', '10:00 AM', '11:00 AM', '02:00 PM', '03:00 PM'],
 33 |     '2026-05-19': ['09:00 AM', '11:00 AM', '02:00 PM', '03:00 PM', '04:00 PM'],
 34 |     '2026-05-20': ['10:00 AM', '11:00 AM', '02:00 PM', '03:00 PM', '04:00 PM'],
 35 |     '2026-05-21': ['09:00 AM', '10:00 AM', '02:00 PM', '03:00 PM'],
 36 | }
 37 | 
 38 | # Mock data for booked appointments
 39 | booked_appointments = []
 40 | 
 41 | # Mock data for medication reminders
 42 | medication_reminders = [
 43 |     {
 44 |         'medication': 'Amoxicillin 500mg',
 45 |         'time': '08:00 AM',
 46 |         'frequency': 'Twice daily',
 47 |         'notes': 'Take with food'
 48 |     },
 49 |     {
 50 |         'medication': 'Vitamin D3',
 51 |         'time': '09:00 AM',
 52 |         'frequency': 'Once daily',
 53 |         'notes': 'Take with breakfast'
 54 |     },
 55 |     {
 56 |         'medication': 'Blood Pressure Check',
 57 |         'time': '07:00 PM',
 58 |         'frequency': 'Daily',
 59 |         'notes': 'Record readings in log'
 60 |     }
 61 | ]
 62 | 
 63 | # Mock data for upcoming tasks
 64 | upcoming_tasks = [
 65 |     {
 66 |         'task': 'Lab Test - Blood Work',
 67 |         'date': '2026-05-18',
 68 |         'time': '08:30 AM',
 69 |         'location': 'City Medical Lab, 2nd Floor'
 70 |     },
 71 |     {
 72 |         'task': 'Physical Therapy Session',
 73 |         'date': '2026-05-20',
 74 |         'time': '03:00 PM',
 75 |         'location': 'Rehabilitation Center, Room 204'
 76 |     }
 77 | ]
 78 | 
 79 | # Mock data for patient profile
 80 | patient_profile = {
 81 |     'name': 'John Anderson',
 82 |     'age': 45,
 83 |     'blood_group': 'O+',
 84 |     'contact_number': '+1 (555) 123-4567',
 85 |     'email': 'john.anderson@email.com',
 86 |     'primary_doctor': {
 87 |         'name': 'Dr. Sarah Johnson',
 88 |         'specialty': 'General Practitioner',
 89 |         'contact': '+1 (555) 234-5678'
 90 |     },
 91 |     'allergies': ['Penicillin', 'Peanuts', 'Latex'],
 92 |     'current_medications': [
 93 |         'Amoxicillin 500mg - Twice daily',
 94 |         'Vitamin D3 - Once daily',
 95 |         'Lisinopril 10mg - Once daily'
 96 |     ],
 97 |     'emergency_contact': {
 98 |         'name': 'Sarah Anderson',
 99 |         'phone': '+1 (555) 987-6543',
100 |         'relationship': 'Spouse'
101 |     },
102 |     'current_health_status': {
103 |         'active_diagnoses': [
104 |             {
105 |                 'condition': 'Acute Pharyngitis',
106 |                 'status': 'Under Treatment',
107 |                 'diagnosed_date': '2026-05-15'
108 |             }
109 |         ],
110 |         'active_symptoms': [
111 |             'Sore throat',
112 |             'Low grade fever',
113 |             'Fatigue',
114 |             'Difficulty swallowing'
115 |         ]
116 |     }
117 | }
118 | 
119 | # Medical Knowledge Base for AI Assistant
120 | MEDICAL_KNOWLEDGE_BASE = {
121 |     'medications': {
122 |         'amoxicillin': {
123 |             'name': 'Amoxicillin 500mg',
124 |             'purpose': 'Amoxicillin is an antibiotic used to treat bacterial infections, including throat infections like your Acute Pharyngitis.',
125 |             'dosage': 'Take 500mg twice daily as prescribed by Dr. Sarah Johnson.',
126 |             'side_effects': 'Common side effects may include nausea, diarrhea, or rash. Contact your doctor if symptoms worsen.',
127 |             'precautions': 'Take with food to reduce stomach upset. Complete the full course even if you feel better.',
128 |             'interactions': 'Avoid alcohol while taking Amoxicillin as it may reduce effectiveness and increase side effects.'
129 |         },
130 |         'paracetamol': {
131 |             'name': 'Paracetamol (Acetaminophen)',
132 |             'purpose': 'Used to reduce fever and relieve pain, including sore throat pain.',
133 |             'dosage': 'Take 500-1000mg every 4-6 hours as needed, not exceeding 4000mg per day.',
134 |             'side_effects': 'Generally well-tolerated. Rare side effects include allergic reactions.',
135 |             'precautions': 'Do not exceed recommended dose. Avoid alcohol to prevent liver damage.',
136 |             'interactions': 'Safe with most medications, but inform your doctor of all medicines you take.'
137 |         },
138 |         'vitamin d3': {
139 |             'name': 'Vitamin D3',
140 |             'purpose': 'Supports immune system function and bone health.',
141 |             'dosage': 'Take once daily with breakfast as prescribed.',
142 |             'side_effects': 'Rare when taken as directed.',
143 |             'precautions': 'Take with food for better absorption.',
144 |             'interactions': 'Generally safe with other medications.'
145 |         },
146 |         'lisinopril': {
147 |             'name': 'Lisinopril 10mg',
148 |             'purpose': 'Used to treat high blood pressure.',
149 |             'dosage': 'Take 10mg once daily as prescribed.',
150 |             'side_effects': 'May cause dizziness, dry cough, or fatigue.',
151 |             'precautions': 'Rise slowly from sitting/lying position to prevent dizziness.',
152 |             'interactions': 'Avoid potassium supplements unless directed by your doctor.'
153 |         }
154 |     },
155 |     'conditions': {
156 |         'acute pharyngitis': {
157 |             'name': 'Acute Pharyngitis',
158 |             'description': 'Inflammation of the throat (pharynx), commonly known as a sore throat, often caused by bacterial infection.',
159 |             'symptoms': 'Sore throat, difficulty swallowing, fever, swollen lymph nodes.',
160 |             'treatment': 'Antibiotics (Amoxicillin), rest, hydration, and pain relievers.',
161 |             'dietary_advice': [
162 |                 'Drink plenty of warm fluids (warm water, herbal tea, warm soup)',
163 |                 'Avoid spicy, acidic, or rough foods that may irritate your throat',
164 |                 'Eat soft, easy-to-swallow foods like yogurt, mashed potatoes, or smoothies',
165 |                 'Stay hydrated - aim for 8-10 glasses of water daily',
166 |                 'Avoid alcohol while on antibiotics',
167 |                 'Honey and lemon in warm water can soothe throat pain'
168 |             ],
169 |             'recovery_time': 'Most patients recover within 7-10 days with proper treatment.',
170 |             'warning_signs': 'Seek immediate care if you experience difficulty breathing, severe pain, or high fever above 103°F.'
171 |         }
172 |     }
173 | }
174 | 
175 | # Safety keywords that trigger escalation
176 | SAFETY_KEYWORDS = {
177 |     'emergency': ['emergency', 'urgent', 'severe pain', 'chest pain', 'difficulty breathing',
178 |                   'can\'t breathe', 'heart attack', 'stroke', 'bleeding heavily', 'unconscious'],
179 |     'diagnosis': ['diagnose', 'do i have', 'is this', 'could this be', 'what disease'],
180 |     'dosage_change': ['change dose', 'increase dose', 'decrease dose', 'stop taking',
181 |                       'can i take more', 'double dose', 'skip dose'],
182 |     'substitute': ['substitute', 'replace medicine', 'alternative medicine', 'switch to',
183 |                    'instead of', 'can i take instead']
184 | }
185 | 
186 | # Dangerous keywords to check in AI responses
187 | DANGEROUS_RESPONSE_KEYWORDS = [
188 |     'stop taking medication',
189 |     'stop your medication',
190 |     'discontinue medication',
191 |     'increase your dose',
192 |     'decrease your dose',
193 |     'change your dose',
194 |     'you should stop',
195 |     'emergency room',
196 |     'call 911',
197 |     'seek immediate',
198 |     'go to hospital'
199 | ]
200 | 
201 | def query_ai_model(prompt):
202 |     """
203 |     Query the local TinyLlama model
204 |     Returns the AI-generated text or an error message
205 |     """
206 |     if pipe is None:
207 |         return {
208 |             'error': True,
209 |             'message': "Local AI model is not available. Please ensure transformers and torch are installed."
210 |         }
211 |     
212 |     try:
213 |         # Construct prompt in TinyLlama chat format
214 |         formatted_prompt = f"<|system|>\nYou are a helpful medical assistant.</s>\n<|user|>\n{prompt}</s>\n<|assistant|>\n"
215 |         
216 |         # Get tokenizer's eos_token_id safely
217 |         try:
218 |             # Access tokenizer safely with proper null checks
219 |             tokenizer = pipe.tokenizer
220 |             eos_token = tokenizer.eos_token_id if tokenizer and hasattr(tokenizer, 'eos_token_id') and tokenizer.eos_token_id is not None else 2
221 |         except (AttributeError, TypeError):
222 |             eos_token = 2  # Default EOS token ID for most models
223 |         
224 |         # Suppress warnings by using generation_config=None and explicit parameters
225 |         import warnings
226 |         with warnings.catch_warnings():
227 |             warnings.filterwarnings("ignore", category=UserWarning)
228 |             
229 |             # Generate response
230 |             outputs = pipe(
231 |                 formatted_prompt,
232 |                 max_new_tokens=200,
233 |                 temperature=0.7,
234 |                 top_p=0.9,
235 |                 do_sample=True,
236 |                 return_full_text=False,
237 |                 pad_token_id=eos_token,
238 |                 eos_token_id=eos_token
239 |             )
240 |         
241 |         # Extract generated text
242 |         if outputs and len(outputs) > 0:
243 |             generated_text = outputs[0]['generated_text']
244 |             
245 |             # Clean up the response (remove special tokens and extra whitespace)
246 |             generated_text = generated_text.replace('</s>', '').replace('<|assistant|>', '').strip()
247 |             
248 |             # If response is too short or empty, return error
249 |             if len(generated_text) < 10:
250 |                 return {
251 |                     'error': True,
252 |                     'message': "Model generated an incomplete response."
253 |                 }
254 |             
255 |             return {
256 |                 'error': False,
257 |                 'text': generated_text
258 |             }
259 |         
260 |         return {
261 |             'error': True,
262 |             'message': "Model did not generate a response."
263 |         }
264 |         
265 |     except Exception as e:
266 |         return {
267 |             'error': True,
268 |             'message': f"Error generating response: {str(e)}"
269 |         }
270 | 
271 | def check_response_safety(ai_response):
272 |     """
273 |     Check if AI response contains dangerous keywords
274 |     Returns (is_safe, warning_message)
275 |     """
276 |     response_lower = ai_response.lower()
277 |     
278 |     for keyword in DANGEROUS_RESPONSE_KEYWORDS:
279 |         if keyword in response_lower:
280 |             return False, "⚠️ **Safety Override**: This response has been flagged for containing potentially dangerous medical advice. Please consult your doctor directly for any changes to your treatment plan."
281 |     
282 |     return True, None
283 | 
284 | def get_ai_response(user_message, patient_context):
285 |     """
286 |     Generate AI response with safety guardrails
287 |     """
288 |     message_lower = user_message.lower()
289 |     
290 |     # Safety Check 1: Emergency keywords
291 |     for keyword in SAFETY_KEYWORDS['emergency']:
292 |         if keyword in message_lower:
293 |             return {
294 |                 'response': '🚨 **EMERGENCY ALERT**: If you are experiencing a medical emergency, please call 911 immediately or go to the nearest emergency room. Do not wait for a response here.',
295 |                 'type': 'emergency',
296 |                 'escalate': True
297 |             }
298 |     
299 |     # Safety Check 2: Diagnosis requests
300 |     for keyword in SAFETY_KEYWORDS['diagnosis']:
301 |         if keyword in message_lower:
302 |             doctor_name = patient_context.get('primary_doctor', {}).get('name', 'your doctor')
303 |             current_diagnosis = patient_context['current_health_status']['active_diagnoses'][0]['condition']
304 |             return {
305 |                 'response': f'⚠️ **Safety Notice**: I cannot provide medical diagnoses. Your current diagnosis of {current_diagnosis} was made by {doctor_name}. If you have concerns about new symptoms or your condition, please contact {doctor_name} directly at the clinic.',
306 |                 'type': 'safety_warning',
307 |                 'escalate': True
308 |             }
309 |     
310 |     # Safety Check 3: Dosage changes
311 |     for keyword in SAFETY_KEYWORDS['dosage_change']:
312 |         if keyword in message_lower:
313 |             doctor_name = patient_context.get('primary_doctor', {}).get('name', 'your doctor')
314 |             return {
315 |                 'response': f'⚠️ **Safety Notice**: For your safety, I cannot advise on changing medication dosages. Your current prescriptions were carefully determined by {doctor_name}. Please contact {doctor_name} before making any changes to your medication regimen.',
316 |                 'type': 'safety_warning',
317 |                 'escalate': True
318 |             }
319 |     
320 |     # Safety Check 4: Medicine substitution
321 |     for keyword in SAFETY_KEYWORDS['substitute']:
322 |         if keyword in message_lower:
323 |             doctor_name = patient_context.get('primary_doctor', {}).get('name', 'your doctor')
324 |             allergies = ', '.join(patient_context.get('allergies', []))
325 |             allergy_note = f', especially considering your allergies to {allergies}' if allergies else ''
326 |             return {
327 |                 'response': f'⚠️ **Safety Notice**: I cannot recommend substituting or changing your prescribed medications. Please consult {doctor_name} before making any medication changes{allergy_note}.',
328 |                 'type': 'safety_warning',
329 |                 'escalate': True
330 |             }
331 |     
332 |     # Feature 3: Dietary Advice
333 |     if any(word in message_lower for word in ['diet', 'food', 'eat', 'drink', 'nutrition', 'meal']):
334 |         condition = patient_context['current_health_status']['active_diagnoses'][0]['condition'].lower()
335 |         doctor_name = patient_context.get('primary_doctor', {}).get('name', 'your doctor')
336 |         if condition in MEDICAL_KNOWLEDGE_BASE['conditions']:
337 |             dietary_advice = MEDICAL_KNOWLEDGE_BASE['conditions'][condition]['dietary_advice']
338 |             advice_text = '\n'.join([f"• {advice}" for advice in dietary_advice])
339 |             return {
340 |                 'response': f'**Dietary Recommendations for {patient_context["current_health_status"]["active_diagnoses"][0]["condition"]}:**\n\n{advice_text}\n\nThese recommendations are based on your current diagnosis and medications. Always follow {doctor_name}\'s specific dietary instructions.',
341 |                 'type': 'dietary_advice',
342 |                 'escalate': False
343 |             }
344 |     
345 |     # Feature 2: Medication Q&A
346 |     if any(word in message_lower for word in ['medicine', 'medication', 'drug', 'pill', 'amoxicillin', 'paracetamol', 'vitamin', 'lisinopril']):
347 |         doctor_name = patient_context.get('primary_doctor', {}).get('name', 'your doctor')
348 |         medications = patient_context.get('current_medications', [])
349 |         
350 |         # Check for missed dose question
351 |         if 'missed' in message_lower or 'forgot' in message_lower:
352 |             primary_med = medications[0] if medications else 'your medication'
353 |             return {
354 |                 'response': f'**Missed Dose Information:**\n\nIf you missed a dose of {primary_med}:\n• Take it as soon as you remember\n• If it\'s almost time for your next dose, skip the missed dose\n• Do NOT double up on doses\n• Continue with your regular schedule\n\nFor other medications, please contact {doctor_name} for specific guidance.',
355 |                 'type': 'medication_info',
356 |                 'escalate': False
357 |             }
358 |         
359 |         # General medication information
360 |         for med_key, med_info in MEDICAL_KNOWLEDGE_BASE['medications'].items():
361 |             if med_key in message_lower:
362 |                 return {
363 |                     'response': f'**{med_info["name"]}**\n\n**Purpose:** {med_info["purpose"]}\n\n**Dosage:** {med_info["dosage"]}\n\n**Precautions:** {med_info["precautions"]}\n\n**Important:** {med_info["interactions"]}',
364 |                     'type': 'medication_info',
365 |                     'escalate': False
366 |                 }
367 |         
368 |         # General medication response
369 |         med_list = ', '.join([med.split(' - ')[0] for med in medications]) if medications else 'your medications'
370 |         return {
371 |             'response': f'I can provide information about your current medications: {med_list}. Which medication would you like to know more about?',
372 |             'type': 'medication_info',
373 |             'escalate': False
374 |         }
375 |     
376 |     # Symptom inquiry
377 |     if any(word in message_lower for word in ['symptom', 'sore throat', 'fever', 'pain', 'swallow', 'throat']):
378 |         doctor_name = patient_context.get('primary_doctor', {}).get('name', 'your doctor')
379 |         diagnosis = patient_context['current_health_status']['active_diagnoses'][0]['condition']
380 |         symptoms = patient_context['current_health_status']['active_symptoms']
381 |         return {
382 |             'response': f'**Your Current Symptoms:**\n\nBased on your diagnosis of {diagnosis}, you are experiencing:\n• {", ".join(symptoms)}\n\nThese symptoms should improve within 7-10 days with your current treatment. If symptoms worsen or you develop new concerning symptoms, please contact {doctor_name}.',
383 |             'type': 'symptom_info',
384 |             'escalate': False
385 |         }
386 |     
387 |     # Default helpful response
388 |     doctor_name = patient_context.get('primary_doctor', {}).get('name', 'your doctor')
389 |     medications = patient_context.get('current_medications', [])
390 |     diagnosis = patient_context['current_health_status']['active_diagnoses'][0]['condition']
391 |     med_list = ', '.join([med.split(' - ')[0] for med in medications]) if medications else 'your medications'
392 |     
393 |     return {
394 |         'response': f'I\'m here to help answer questions about:\n\n• Your medications ({med_list})\n• Dietary recommendations for {diagnosis}\n• Your current symptoms and treatment\n• General post-consultation care\n\nWhat would you like to know more about?\n\n*For medical emergencies, call 911. For changes to your treatment plan, contact {doctor_name}.*',
395 |         'type': 'general',
396 |         'escalate': False
397 |     }
398 | 
399 | @app.route('/')
400 | def index():
401 |     return render_template('schedule.html', 
402 |                          available_slots=available_slots,
403 |                          booked_appointments=booked_appointments,
404 |                          medication_reminders=medication_reminders,
405 |                          upcoming_tasks=upcoming_tasks)
406 | 
407 | @app.route('/schedule')
408 | def schedule():
409 |     return render_template('schedule.html',
410 |                          available_slots=available_slots,
411 |                          booked_appointments=booked_appointments,
412 |                          medication_reminders=medication_reminders,
413 |                          upcoming_tasks=upcoming_tasks)
414 | 
415 | @app.route('/appointments')
416 | def appointments():
417 |     return render_template('appointments.html',
418 |                          booked_appointments=booked_appointments)
419 | 
420 | @app.route('/profile')
421 | def profile():
422 |     return render_template('profile.html',
423 |                          patient_profile=patient_profile)
424 | 
425 | @app.route('/assistant')
426 | def assistant():
427 |     return render_template('assistant.html',
428 |                          patient_profile=patient_profile,
429 |                          medication_reminders=medication_reminders)
430 | 
431 | @app.route('/api/chat', methods=['POST'])
432 | def chat():
433 |     try:
434 |         data = request.get_json()
435 |         user_message = data.get('message', '').strip()
436 |         
437 |         if not user_message:
438 |             return jsonify({
439 |                 'success': False,
440 |                 'message': 'Message cannot be empty'
441 |             }), 400
442 |         
443 |         # First, check safety guardrails (emergency, diagnosis, dosage changes)
444 |         ai_response = get_ai_response(user_message, patient_profile)
445 |         
446 |         # If safety check triggered, return immediately without calling AI
447 |         if ai_response['escalate']:
448 |             return jsonify({
449 |                 'success': True,
450 |                 'response': ai_response['response'],
451 |                 'type': ai_response['type'],
452 |                 'escalate': ai_response['escalate']
453 |             })
454 |         
455 |         # If safety checks passed, construct prompt for AI model
456 |         diagnosis = patient_profile['current_health_status']['active_diagnoses'][0]['condition']
457 |         symptoms = ', '.join(patient_profile['current_health_status']['active_symptoms'])
458 |         medications = '\n'.join([f"- {med}" for med in patient_profile['current_medications']])
459 |         doctor_name = patient_profile['primary_doctor']['name']
460 |         allergies = ', '.join(patient_profile['allergies'])
461 |         
462 |         # Construct strict system prompt
463 |         system_prompt = f"""You are a medical assistant for a patient. Provide helpful, accurate information based ONLY on the context below.
464 | 
465 | Patient Context:
466 | - Name: {patient_profile['name']}
467 | - Diagnosis: {diagnosis}
468 | - Symptoms: {symptoms}
469 | - Current Medications:
470 | {medications}
471 | - Allergies: {allergies}
472 | - Primary Doctor: {doctor_name}
473 | 
474 | IMPORTANT RULES:
475 | 1. Base your answer ONLY on the patient context and general medical knowledge
476 | 2. Do NOT diagnose new conditions
477 | 3. Do NOT recommend changing medication dosages
478 | 4. Do NOT recommend stopping or substituting medications
479 | 5. For emergencies, tell the patient to call 911 or go to the ER
480 | 6. Keep responses concise (2-3 paragraphs maximum)
481 | 7. Always remind the patient to consult {doctor_name} for medical decisions
482 | 
483 | Patient Question: {user_message}
484 | 
485 | Provide a helpful, concise answer:"""
486 | 
487 |         # Query the local AI model
488 |         ai_result = query_ai_model(system_prompt)
489 |         
490 |         # Handle model errors
491 |         if ai_result.get('error'):
492 |             return jsonify({
493 |                 'success': True,
494 |                 'response': f"⚠️ Local AI Model Unavailable: {ai_result['message']}\n\nIn the meantime, I can help with:\n• Medication information from your records\n• Dietary advice for {diagnosis}\n• General symptom information\n\nPlease try your question again, or contact {doctor_name} directly.",
495 |                 'type': 'error',
496 |                 'escalate': False
497 |             })
498 |         
499 |         # Extract AI response
500 |         ai_text = ai_result['text'].strip()
501 |         
502 |         # Safety check on AI response
503 |         is_safe, warning = check_response_safety(ai_text)
504 |         
505 |         if not is_safe:
506 |             return jsonify({
507 |                 'success': True,
508 |                 'response': warning,
509 |                 'type': 'safety_warning',
510 |                 'escalate': True
511 |             })
512 |         
513 |         # Add disclaimer to AI response
514 |         final_response = f"{ai_text}\n\n---\n*Generated by Local AI. Always consult {doctor_name} for medical advice.*"
515 |         
516 |         return jsonify({
517 |             'success': True,
518 |             'response': final_response,
519 |             'type': 'ai_generated',
520 |             'escalate': False
521 |         })
522 |         
523 |     except Exception as e:
524 |         return jsonify({
525 |             'success': False,
526 |             'message': f'Error processing request: {str(e)}'
527 |         }), 500
528 | 
529 | @app.route('/api/book', methods=['POST'])
530 | def book_appointment():
531 |     data = request.get_json()
532 |     date = data.get('date')
533 |     time = data.get('time')
534 |     
535 |     if not date or not time:
536 |         return jsonify({'success': False, 'message': 'Date and time are required'}), 400
537 |     
538 |     # Check if slot is available
539 |     if date in available_slots and time in available_slots[date]:
540 |         # Remove the booked slot from available slots
541 |         available_slots[date].remove(time)
542 |         
543 |         # Add to booked appointments
544 |         appointment = {
545 |             'date': date,
546 |             'time': time,
547 |             'doctor': 'Dr. Sarah Johnson',
548 |             'specialty': 'General Practitioner',
549 |             'booked_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
550 |         }
551 |         booked_appointments.append(appointment)
552 |         
553 |         return jsonify({
554 |             'success': True, 
555 |             'message': 'Appointment booked successfully!',
556 |             'appointment': appointment
557 |         })
558 |     else:
559 |         return jsonify({
560 |             'success': False, 
561 |             'message': 'Selected time slot is not available'
562 |         }), 400
563 | 
564 | @app.route('/api/slots/<date>')
565 | def get_slots(date):
566 |     slots = available_slots.get(date, [])
567 |     return jsonify({'date': date, 'slots': slots})
568 | 
569 | @app.route('/api/cancel/<int:appointment_index>', methods=['DELETE'])
570 | def cancel_appointment(appointment_index):
571 |     try:
572 |         if 0 <= appointment_index < len(booked_appointments):
573 |             # Get the appointment to cancel
574 |             appointment = booked_appointments[appointment_index]
575 |             date = appointment['date']
576 |             time = appointment['time']
577 |             
578 |             # Remove the appointment
579 |             booked_appointments.pop(appointment_index)
580 |             
581 |             # Add the time slot back to available slots
582 |             if date in available_slots:
583 |                 if time not in available_slots[date]:
584 |                     available_slots[date].append(time)
585 |                     # Sort the time slots
586 |                     available_slots[date].sort()
587 |             else:
588 |                 available_slots[date] = [time]
589 |             
590 |             return jsonify({
591 |                 'success': True,
592 |                 'message': 'Appointment cancelled successfully'
593 |             })
594 |         else:
595 |             return jsonify({
596 |                 'success': False,
597 |                 'message': 'Invalid appointment index'
598 |             }), 404
599 |     except Exception as e:
600 |         return jsonify({
601 |             'success': False,
602 |             'message': str(e)
603 |         }), 500
604 | 
605 | if __name__ == '__main__':
606 |     app.run(debug=True, port=5000)
607 | 
608 | # Made with Bob
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
app.py

# VSCode Open Tabs
templates/schedule.html,templates/appointments.html,templates/profile.html,templates/assistant.html,app.py,static/style.css

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T18:31:12.957Z
User time zone: Asia/Kuala_Lumpur, UTC+8:00

# Current Cost
$0.08

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

Now I'll refactor the app.py to use Ollama instead of transformers. I'll replace the entire file with the updated version.

<write_to_file>
<path>app.py</path>
<content>from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import requests

app = Flask(__name__)

# Ollama Configuration
OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"  # or "mistral"

print("=" * 60)
print("🚀 Clinical AI Assistant - Ollama Integration")
print("=" * 60)
print(f"📡 Ollama API URL: {OLLAMA_API_URL}")
print(f"🤖 Model: {OLLAMA_MODEL}")
print("💡 Make sure Ollama is running: ollama serve")
print("=" * 60)

# Mock data for available time slots
available_slots = {
    '2026-05-17': ['09:00 AM', '10:00 AM', '11:00 AM', '02:00 PM', '03:00 PM', '04:00 PM'],
    '2026-05-18': ['09:00 AM', '10:00 AM', '11:00 AM', '02:00 PM', '03:00 PM'],
    '2026-05-19': ['09:00 AM', '11:00 AM', '02:00 PM', '03:00 PM', '04:00 PM'],
    '2026-05-20': ['10:00 AM', '11:00 AM', '02:00 PM', '03:00 PM', '04:00 PM'],
    '2026-05-21': ['09:00 AM', '10:00 AM', '02:00 PM', '03:00 PM'],
}

# Mock data for booked appointments
booked_appointments = []

# Mock data for medication reminders
medication_reminders = [
    {
        'medication': 'Amoxicillin 500mg',
        'time': '08:00 AM',
        'frequency': 'Twice daily',
        'notes': 'Take with food'
    },
    {
        'medication': 'Vitamin D3',
        'time': '09:00 AM',
        'frequency': 'Once daily',
        'notes': 'Take with breakfast'
    },
    {
        'medication': 'Blood Pressure Check',
        'time': '07:00 PM',
        'frequency': 'Daily',
        'notes': 'Record readings in log'
    }
]

# Mock data for upcoming tasks
upcoming_tasks = [
    {
        'task': 'Lab Test - Blood Work',
        'date': '2026-05-18',
        'time': '08:30 AM',
        'location': 'City Medical Lab, 2nd Floor'
    },
    {
        'task': 'Physical Therapy Session',
        'date': '2026-05-20',
        'time': '03:00 PM',
        'location': 'Rehabilitation Center, Room 204'
    }
]

# Mock data for patient profile
patient_profile = {
    'name': 'John Anderson',
    'age': 45,
    'blood_group': 'O+',
    'contact_number': '+1 (555) 123-4567',
    'email': 'john.anderson@email.com',
    'primary_doctor': {
        'name': 'Dr. Sarah Johnson',
        'specialty': 'General Practitioner',
        'contact': '+1 (555) 234-5678'
    },
    'allergies': ['Penicillin', 'Peanuts', 'Latex'],
    'current_medications': [
        'Amoxicillin 500mg - Twice daily',
        'Vitamin D3 - Once daily',
        'Lisinopril 10mg - Once daily'
    ],
    'emergency_contact': {
        'name': 'Sarah Anderson',
        'phone': '+1 (555) 987-6543',
        'relationship': 'Spouse'
    },
    'current_health_status': {
        'active_diagnoses': [
            {
                'condition': 'Acute Pharyngitis',
                'status': 'Under Treatment',
                'diagnosed_date': '2026-05-15'
            }
        ],
        'active_symptoms': [
            'Sore throat',
            'Low grade fever',
            'Fatigue',
            'Difficulty swallowing'
        ]
    }
}

# Medical Knowledge Base for AI Assistant
MEDICAL_KNOWLEDGE_BASE = {
    'medications': {
        'amoxicillin': {
            'name': 'Amoxicillin 500mg',
            'purpose': 'Amoxicillin is an antibiotic used to treat bacterial infections, including throat infections like your Acute Pharyngitis.',
            'dosage': 'Take 500mg twice daily as prescribed by Dr. Sarah Johnson.',
            'side_effects': 'Common side effects may include nausea, diarrhea, or rash. Contact your doctor if symptoms worsen.',
            'precautions': 'Take with food to reduce stomach upset. Complete the full course even if you feel better.',
            'interactions': 'Avoid alcohol while taking Amoxicillin as it may reduce effectiveness and increase side effects.'
        },
        'paracetamol': {
            'name': 'Paracetamol (Acetaminophen)',
            'purpose': 'Used to reduce fever and relieve pain, including sore throat pain.',
            'dosage': 'Take 500-1000mg every 4-6 hours as needed, not exceeding 4000mg per day.',
            'side_effects': 'Generally well-tolerated. Rare side effects include allergic reactions.',
            'precautions': 'Do not exceed recommended dose. Avoid alcohol to prevent liver damage.',
            'interactions': 'Safe with most medications, but inform your doctor of all medicines you take.'
        },
        'vitamin d3': {
            'name': 'Vitamin D3',
            'purpose': 'Supports immune system function and bone health.',
            'dosage': 'Take once daily with breakfast as prescribed.',
            'side_effects': 'Rare when taken as directed.',
            'precautions': 'Take with food for better absorption.',
            'interactions': 'Generally safe with other medications.'
        },
        'lisinopril': {
            'name': 'Lisinopril 10mg',
            'purpose': 'Used to treat high blood pressure.',
            'dosage': 'Take 10mg once daily as prescribed.',
            'side_effects': 'May cause dizziness, dry cough, or fatigue.',
            'precautions': 'Rise slowly from sitting/lying position to prevent dizziness.',
            'interactions': 'Avoid potassium supplements unless directed by your doctor.'
        }
    },
    'conditions': {
        'acute pharyngitis': {
            'name': 'Acute Pharyngitis',
            'description': 'Inflammation of the throat (pharynx), commonly known as a sore throat, often caused by bacterial infection.',
            'symptoms': 'Sore throat, difficulty swallowing, fever, swollen lymph nodes.',
            'treatment': 'Antibiotics (Amoxicillin), rest, hydration, and pain relievers.',
            'dietary_advice': [
                'Drink plenty of warm fluids (warm water, herbal tea, warm soup)',
                'Avoid spicy, acidic, or rough foods that may irritate your throat',
                'Eat soft, easy-to-swallow foods like yogurt, mashed potatoes, or smoothies',
                'Stay hydrated - aim for 8-10 glasses of water daily',
                'Avoid alcohol while on antibiotics',
                'Honey and lemon in warm water can soothe throat pain'
            ],
            'recovery_time': 'Most patients recover within 7-10 days with proper treatment.',
            'warning_signs': 'Seek immediate care if you experience difficulty breathing, severe pain, or high fever above 103°F.'
        }
    }
}

# Safety keywords that trigger escalation
SAFETY_KEYWORDS = {
    'emergency': ['emergency', 'urgent', 'severe pain', 'chest pain', 'difficulty breathing',
                  'can\'t breathe', 'heart attack', 'stroke', 'bleeding heavily', 'unconscious'],
    'diagnosis': ['diagnose', 'do i have', 'is this', 'could this be', 'what disease'],
    'dosage_change': ['change dose', 'increase dose', 'decrease dose', 'stop taking',
                      'can i take more', 'double dose', 'skip dose'],
    'substitute': ['substitute', 'replace medicine', 'alternative medicine', 'switch to',
                   'instead of', 'can i take instead']
}

# Dangerous keywords to check in AI responses
DANGEROUS_RESPONSE_KEYWORDS = [
    'stop taking medication',
    'stop your medication',
    'discontinue medication',
    'increase your dose',
    'decrease your dose',
    'change your dose',
    'you should stop',
    'emergency room',
    'call 911',
    'seek immediate',
    'go to hospital'
]

def query_ai_model(prompt):
    """
    Query the Ollama local AI model
    Returns the AI-generated text or an error message
    """
    try:
        # Prepare the payload for Ollama API
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }
        
        # Make POST request to Ollama API
        response = requests.post(
            OLLAMA_API_URL,
            json=payload,
            timeout=30  # 30 second timeout
        )
        
        # Check if request was successful
        if response.status_code == 200:
            result = response.json()
            generated_text = result.get('response', '').strip()
            
            # If response is too short or empty, return error
            if len(generated_text) < 10:
                return {
                    'error': True,
                    'message': "Model generated an incomplete response."
                }
            
            return {
                'error': False,
                'text': generated_text
            }
        else:
            return {
                'error': True,
                'message': f"Ollama API returned status code {response.status_code}"
            }
            
    except requests.exceptions.ConnectionError:
        return {
            'error': True,
            'message': "Cannot connect to Ollama. Please ensure Ollama is running (ollama serve)."
        }
    except requests.exceptions.Timeout:
        return {
            'error': True,
            'message': "Request to Ollama timed out. The model might be loading or overloaded."
        }
    except Exception as e:
        return {
            'error': True,
            'message': f"Error communicating with Ollama: {str(e)}"
        }

def check_response_safety(ai_response):
    """
    Check if AI response contains dangerous keywords
    Returns (is_safe, warning_message)
    """
    response_lower = ai_response.lower()
    
    for keyword in DANGEROUS_RESPONSE_KEYWORDS:
        if keyword in response_lower:
            return False, "⚠️ **Safety Override**: This response has been flagged for containing potentially dangerous medical advice. Please consult your doctor directly for any changes to your treatment plan."
    
    return True, None

def get_ai_response(user_message, patient_context):
    """
    Generate AI response with safety guardrails
    """
    message_lower = user_message.lower()
    
    # Safety Check 1: Emergency keywords
    for keyword in SAFETY_KEYWORDS['emergency']:
        if keyword in message_lower:
            return {
                'response': '🚨 **EMERGENCY ALERT**: If you are experiencing a medical emergency, please call 911 immediately or go to the nearest emergency room. Do not wait for a response here.',
                'type': 'emergency',
                'escalate': True
            }
    
    # Safety Check 2: Diagnosis requests
    for keyword in SAFETY_KEYWORDS['diagnosis']:
        if keyword in message_lower:
            doctor_name = patient_context.get('primary_doctor', {}).get('name', 'your doctor')
            current_diagnosis = patient_context['current_health_status']['active_diagnoses'][0]['condition']
            return {
                'response': f'⚠️ **Safety Notice**: I cannot provide medical diagnoses. Your current diagnosis of {current_diagnosis} was made by {doctor_name}. If you have concerns about new symptoms or your condition, please contact {doctor_name} directly at the clinic.',
                'type': 'safety_warning',
                'escalate': True
            }
    
    # Safety Check 3: Dosage changes
    for keyword in SAFETY_KEYWORDS['dosage_change']:
        if keyword in message_lower:
            doctor_name = patient_context.get('primary_doctor', {}).get('name', 'your doctor')
            return {
                'response': f'⚠️ **Safety Notice**: For your safety, I cannot advise on changing medication dosages. Your current prescriptions were carefully determined by {doctor_name}. Please contact {doctor_name} before making any changes to your medication regimen.',
                'type': 'safety_warning',
                'escalate': True
            }
    
    # Safety Check 4: Medicine substitution
    for keyword in SAFETY_KEYWORDS['substitute']:
        if keyword in message_lower:
            doctor_name = patient_context.get('primary_doctor', {}).get('name', 'your doctor')
            allergies = ', '.join(patient_context.get('allergies', []))
            allergy_note = f', especially considering your allergies to {allergies}' if allergies else ''
            return {
                'response': f'⚠️ **Safety Notice**: I cannot recommend substituting or changing your prescribed medications. Please consult {doctor_name} before making any medication changes{allergy_note}.',
                'type': 'safety_warning',
                'escalate': True
            }
    
    # Feature 3: Dietary Advice
    if any(word in message_lower for word in ['diet', 'food', 'eat', 'drink', 'nutrition', 'meal']):
        condition = patient_context['current_health_status']['active_diagnoses'][0]['condition'].lower()
        doctor_name = patient_context.get('primary_doctor', {}).get('name', 'your doctor')
        if condition in MEDICAL_KNOWLEDGE_BASE['conditions']:
            dietary_advice = MEDICAL_KNOWLEDGE_BASE['conditions'][condition]['dietary_advice']
            advice_text = '\n'.join([f"• {advice}" for advice in dietary_advice])
            return {
                'response': f'**Dietary Recommendations for {patient_context["current_health_status"]["active_diagnoses"][0]["condition"]}:**\n\n{advice_text}\n\nThese recommendations are based on your current diagnosis and medications. Always follow {doctor_name}\'s specific dietary instructions.',
                'type': 'dietary_advice',
                'escalate': False
            }
    
    # Feature 2: Medication Q&A
    if any(word in message_lower for word in ['medicine', 'medication', 'drug', 'pill', 'amoxicillin', 'paracetamol', 'vitamin', 'lisinopril']):
        doctor_name = patient_context.get('primary_doctor', {}).get('name', 'your doctor')
        medications = patient_context.get('current_medications', [])
        
        # Check for missed dose question
        if 'missed' in message_lower or 'forgot' in message_lower:
            primary_med = medications[0] if medications else 'your medication'
            return {
                'response': f'**Missed Dose Information:**\n\nIf you missed a dose of {primary_med}:\n• Take it as soon as you remember\n• If it\'s almost time for your next dose, skip the missed dose\n• Do NOT double up on doses\n• Continue with your regular schedule\n\nFor other medications, please contact {doctor_name} for specific guidance.',
                'type': 'medication_info',
                'escalate': False
            }
        
        # General medication information
        for med_key, med_info in MEDICAL_KNOWLEDGE_BASE['medications'].items():
            if med_key in message_lower:
                return {
                    'response': f'**{med_info["name"]}**\n\n**Purpose:** {med_info["purpose"]}\n\n**Dosage:** {med_info["dosage"]}\n\n**Precautions:** {med_info["precautions"]}\n\n**Important:** {med_info["interactions"]}',
                    'type': 'medication_info',
                    'escalate': False
                }
        
        # General medication response
        med_list = ', '.join([med.split(' - ')[0] for med in medications]) if medications else 'your medications'
        return {
            'response': f'I can provide information about your current medications: {med_list}. Which medication would you like to know more about?',
            'type': 'medication_info',
            'escalate': False
        }
    
    # Symptom inquiry
    if any(word in message_lower for word in ['symptom', 'sore throat', 'fever', 'pain', 'swallow', 'throat']):
        doctor_name = patient_context.get('primary_doctor', {}).get('name', 'your doctor')
        diagnosis = patient_context['current_health_status']['active_diagnoses'][0]['condition']
        symptoms = patient_context['current_health_status']['active_symptoms']
        return {
            'response': f'**Your Current Symptoms:**\n\nBased on your diagnosis of {diagnosis}, you are experiencing:\n• {", ".join(symptoms)}\n\nThese symptoms should improve within 7-10 days with your current treatment. If symptoms worsen or you develop new concerning symptoms, please contact {doctor_name}.',
            'type': 'symptom_info',
            'escalate': False
        }
    
    # Default helpful response
    doctor_name = patient_context.get('primary_doctor', {}).get('name', 'your doctor')
    medications = patient_context.get('current_medications', [])
    diagnosis = patient_context['current_health_status']['active_diagnoses'][0]['condition']
    med_list = ', '.join([med.split(' - ')[0] for med in medications]) if medications else 'your medications'
    
    return {
        'response': f'I\'m here to help answer questions about:\n\n• Your medications ({med_list})\n• Dietary recommendations for {diagnosis}\n• Your current symptoms and treatment\n• General post-consultation care\n\nWhat would you like to know more about?\n\n*For medical emergencies, call 911. For changes to your treatment plan, contact {doctor_name}.*',
        'type': 'general',
        'escalate': False
    }

@app.route('/')
def index():
    return render_template('schedule.html', 
                         available_slots=available_slots,
                         booked_appointments=booked_appointments,
                         medication_reminders=medication_reminders,
                         upcoming_tasks=upcoming_tasks)

@app.route('/schedule')
def schedule():
    return render_template('schedule.html',
                         available_slots=available_slots,
                         booked_appointments=booked_appointments,
                         medication_reminders=medication_reminders,
                         upcoming_tasks=upcoming_tasks)

@app.route('/appointments')
def appointments():
    return render_template('appointments.html',
                         booked_appointments=booked_appointments)

@app.route('/profile')
def profile():
    return render_template('profile.html',
                         patient_profile=patient_profile)

@app.route('/assistant')
def assistant():
    return render_template('assistant.html',
                         patient_profile=patient_profile,
                         medication_reminders=medication_reminders)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'success': False,
                'message': 'Message cannot be empty'
            }), 400
        
        # First, check safety guardrails (emergency, diagnosis, dosage changes)
        ai_response = get_ai_response(user_message, patient_profile)
        
        # If safety check triggered, return immediately without calling AI
        if ai_response['escalate']:
            return jsonify({
                'success': True,
                'response': ai_response['response'],
                'type': ai_response['type'],
                'escalate': ai_response['escalate']
            })
        
        # If safety checks passed, construct prompt for AI model
        diagnosis = patient_profile['current_health_status']['active_diagnoses'][0]['condition']
        symptoms = ', '.join(patient_profile['current_health_status']['active_symptoms'])
        medications = '\n'.join([f"- {med}" for med in patient_profile['current_medications']])
        doctor_name = patient_profile['primary_doctor']['name']
        allergies = ', '.join(patient_profile['allergies'])
        
        # Construct strict system prompt
        system_prompt = f"""You are a medical assistant for a patient. Provide helpful, accurate information based ONLY on the context below.

Patient Context:
- Name: {patient_profile['name']}
- Diagnosis: {diagnosis}
- Symptoms: {symptoms}
- Current Medications:
{medications}
- Allergies: {allergies}
- Primary Doctor: {doctor_name}

IMPORTANT RULES:
1. Base your answer ONLY on the patient context and general medical knowledge
2. Do NOT diagnose new conditions
3. Do NOT recommend changing medication dosages
4. Do NOT recommend stopping or substituting medications
5. For emergencies, tell the patient to call 911 or go to the ER
6. Keep responses concise (2-3 paragraphs maximum)
7. Always remind the patient to consult {doctor_name} for medical decisions

Patient Question: {user_message}

Provide a helpful, concise answer:"""

        # Query the local AI model via Ollama
        ai_result = query_ai_model(system_prompt)
        
        # Handle model errors
        if ai_result.get('error'):
            return jsonify({
                'success': True,
                'response': f"⚠️ Local AI Model Unavailable: {ai_result['message']}\n\nIn the meantime, I can help with:\n• Medication information from your records\n• Dietary advice for {diagnosis}\n• General symptom information\n\nPlease try your question again, or contact {doctor_name} directly.",
                'type': 'error',
                'escalate': False
            })
        
        # Extract AI response
        ai_text = ai_result['text'].strip()
        
        # Safety check on AI response
        is_safe, warning = check_response_safety(ai_text)
        
        if not is_safe:
            return jsonify({
                'success': True,
                'response': warning,
                'type': 'safety_warning',
                'escalate': True
            })
        
        # Add disclaimer to AI response
        final_response = f"{ai_text}\n\n---\n*Generated by Local AI. Always consult {doctor_name} for medical advice.*"
        
        return jsonify({
            'success': True,
            'response': final_response,
            'type': 'ai_generated',
            'escalate': False
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error processing request: {str(e)}'
        }), 500

@app.route('/api/book', methods=['POST'])
def book_appointment():
    data = request.get_json()
    date = data.get('date')
    time = data.get('time')
    
    if not date or not time:
        return jsonify({'success': False, 'message': 'Date and time are required'}), 400
    
    # Check if slot is available
    if date in available_slots and time in available_slots[date]:
        # Remove the booked slot from available slots
        available_slots[date].remove(time)
        
        # Add to booked appointments
        appointment = {
            'date': date,
            'time': time,
            'doctor': 'Dr. Sarah Johnson',
            'specialty': 'General Practitioner',
            'booked_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        booked_appointments.append(appointment)
        
        return jsonify({
            'success': True, 
            'message': 'Appointment booked successfully!',
            'appointment': appointment
        })
    else:
        return jsonify({
            'success': False, 
            'message': 'Selected time slot is not available'
        }), 400

@app.route('/api/slots/<date>')
def get_slots(date):
    slots = available_slots.get(date, [])
    return jsonify({'date': date, 'slots': slots})

@app.route('/api/cancel/<int:appointment_index>', methods=['DELETE'])
def cancel_appointment(appointment_index):
    try:
        if 0 <= appointment_index < len(booked_appointments):
            # Get the appointment to cancel
            appointment = booked_appointments[appointment_index]
            date = appointment['date']
            time = appointment['time']
            
            # Remove the appointment
            booked_appointments.pop(appointment_index)
            
            # Add the time slot back to available slots
            if date in available_slots:
                if time not in available_slots[date]:
                    available_slots[date].append(time)
                    # Sort the time slots
                    available_slots[date].sort()
            else:
                available_slots[date] = [time]
            
            return jsonify({
                'success': True,
                'message': 'Appointment cancelled successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid appointment index'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

# Made with Bob
</content>
<line_count>608</line_count>
</write_to_file>

---

**User:**

[write_to_file for 'app.py'] Result:
<file_write_result>
<path>app.py</path>
<operation>modified</operation>
<user_edits>@@ -583,4 +583,4 @@
 if __name__ == '__main__':
     app.run(debug=True, port=5000)
 
-# Made with Bob
\ No newline at end of file
+# Made with Bob
</user_edits>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
<i>If the user's edits have addressed part of the task or changed the requirements, adjust your approach accordingly.</i>
</notice>
</file_write_result>

<environment_details>
# VSCode Visible Files
app.py

# VSCode Open Tabs
templates/schedule.html,templates/appointments.html,templates/profile.html,templates/assistant.html,app.py,static/style.css

# Recently Modified Files
These files have been modified since you last accessed them (file was just edited so you may need to re-read it before editing):
app.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T18:32:22.784Z
User time zone: Asia/Kuala_Lumpur, UTC+8:00

# Current Cost
$0.14

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<attempt_completion>
<result>
Successfully refactored app.py to use Ollama for local AI inference! 🎉

## Key Changes Made:

### 1. **Removed Heavy Dependencies**
   - ❌ Removed `torch`, `transformers`, and `accelerate` imports
   - ✅ Using only standard `requests` library

### 2. **Ollama Integration**
   - **API URL**: `http://localhost:11434/api/generate`
   - **Model**: `llama3` (configurable to `mistral`)
   - **Stream**: Disabled for simpler response handling

### 3. **Updated `query_ai_model()` Function**
   - Uses `requests.post()` to communicate with Ollama API
   - Payload format:
     ```python
     {
         "model": "llama3",
         "prompt": system_prompt,
         "stream": False
     }
     ```
   - Extracts response from JSON key `"response"`
   - Enhanced error handling:
     - Connection refused → "Ensure Ollama is running (ollama serve)"
     - Timeout errors
     - HTTP status code errors

### 4. **Cleanup**
   - Removed all `pipeline`, `device_map`, and model initialization code
   - Removed tokenizer handling code
   - Removed torch/transformers warnings suppression

### 5. **Preserved Safety Features**
   - ✅ All safety guardrails intact (`check_response_safety`)
   - ✅ All `SAFETY_KEYWORDS` preserved
   - ✅ All `DANGEROUS_RESPONSE_KEYWORDS` preserved
   - ✅ Emergency detection, diagnosis prevention, dosage change blocking

## Benefits:
- 🚀 **Faster startup** - No model loading delays
- 💪 **More stable** - Ollama runs as separate service
- 🔧 **Easier setup** - Just run `ollama serve`
- 📦 **Lighter** - No heavy Python dependencies in Flask app

## To Use:
1. Install Ollama: https://ollama.ai
2. Pull model: `ollama pull llama3`
3. Start Ollama: `ollama serve`
4. Run Flask app: `python app.py`
</result>
</attempt_completion>

