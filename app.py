from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from datetime import datetime, timedelta
from functools import wraps
import base64
import io
from PIL import Image
import os
import sys
import json
import secrets
import traceback
from dotenv import load_dotenv

load_dotenv()

# Add model directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'model'))

app = Flask(__name__)
CORS(app)

# Session configuration
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)

# Import inference service (will be loaded lazily)
inference_service = None

def get_inference_service():
    global inference_service
    if inference_service is None:
        try:
            from model.inference_pretrained import get_inference_service as get_service
            inference_service = get_service()
            print("✓ Symptom analyzer loaded (using pre-trained BioMedCLIP)")
        except Exception as e:
            print(f"⚠️ FATAL: Could not load symptom analyzer:")
            print(traceback.format_exc())  # 👈 Prints exact line & error
            inference_service = False
    return inference_service if inference_service is not False else None


# =========================
# GLOBAL ASYNC PROFILE STORE
# =========================
GLOBAL_DOCTOR_PROFILE = {
    "doctor_id": "",
    "name": "",
    "specialty": "",
    "experience": "",
    "bio": ""
}


def load_json_data(filename):
    try:
        filepath = os.path.join('data', filename)
        with open(filepath, 'r') as f:
            return json.load(f)
    except:
        return {}

patients_data = load_json_data('patients.json')
doctors_data = load_json_data('doctors.json')
appointments_data = load_json_data('appointments.json')
credentials_data = load_json_data('credentials.json')

CURRENT_PATIENT_ID = 'P001'

# =========================
# AUTHENTICATION HELPERS
# =========================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_session_user():
    return {
        'user_id': session.get('user_id'),
        'role': session.get('role'),
        'name': session.get('name')
    }

available_slots = {
    '2026-05-17': ['09:00 AM', '11:00 AM', '02:00 PM', '03:00 PM', '04:00 PM'],
    '2026-05-18': ['09:00 AM', '10:00 AM', '11:00 AM', '02:00 PM', '03:00 PM'],
    '2026-05-19': ['09:00 AM', '11:00 AM', '03:00 PM', '04:00 PM'],
    '2026-05-20': ['10:00 AM', '11:00 AM', '02:00 PM', '03:00 PM', '04:00 PM'],
    '2026-05-21': ['09:00 AM', '10:00 AM', '02:00 PM', '03:00 PM'],
}

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


def get_current_patient():
    return patients_data.get(CURRENT_PATIENT_ID, {})


def get_patient_appointments(patient_id):
    patient_appointments = []
    for apt_id, apt in appointments_data.items():
        if apt['patient_id'] == patient_id and apt['status'] == 'scheduled':
            doctor = doctors_data.get(apt['doctor_id'], {})
            doctor_name     = apt.get('doctor_name') or doctor.get('name', 'Unknown Doctor')
            doctor_specialty = apt.get('doctor_specialty') or doctor.get('specialty', 'General')
            patient_appointments.append({
                'appointment_id': apt_id,
                'date': apt['date'],
                'time': apt['time'],
                'doctor': doctor_name,
                'specialty': doctor_specialty,
                'booked_at': apt['booked_at'],
                'notes': apt.get('notes', '')
            })
    return patient_appointments


def get_medication_reminders(patient_id):
    patient = patients_data.get(patient_id, {})
    prescriptions = patient.get('prescription', [])
    reminders = []
    for med in prescriptions:
        reminders.append({
            'medication': med['medication'],
            'time': '08:00 AM',
            'frequency': med['dosage'],
            'notes': med.get('notes', '')
        })
    return reminders


# =========================
# PAGES
# =========================

@app.route('/')
def index():
    return render_template('landing.html')


@app.route('/healthz')
def healthz():
    return jsonify({'status': 'ok'}), 200


@app.route('/schedule')
@login_required
def schedule():
    user_id = session.get('user_id')
    return render_template('schedule.html',
                         available_slots=available_slots,
                         upcoming_tasks=upcoming_tasks,
                         medication_reminders=get_medication_reminders(user_id),
                         booked_appointments=get_patient_appointments(user_id))


@app.route('/appointments')
@login_required
def appointments():
    user_id = session.get('user_id')
    patient_appointments = get_patient_appointments(user_id)
    return render_template('appointments.html',
                         booked_appointments=patient_appointments)


@app.route('/profile')
@login_required
def profile():
    user_id = session.get('user_id')
    patient = patients_data.get(user_id, {})
    patient_profile = {
        'name': patient.get('patient_name', 'Unknown'),
        'age': patient.get('patient_age', 0),
        'blood_group': patient.get('blood_group', 'Unknown'),
        'contact_number': patient.get('contact_number', ''),
        'email': patient.get('email', ''),
        'allergies': patient.get('allergies', []),
        'current_medications': [
            f"{med['medication']} - {med['dosage']}"
            for med in patient.get('prescription', [])
        ],
        'emergency_contact': patient.get('emergency_contact', {})
    }
    return render_template('profile.html', patient_profile=patient_profile)


@app.route('/symptom-analyzer')
@login_required
def symptom_analyzer():
    return render_template('symptom_analyzer.html')


# =========================
# DOCTOR PROFILE PAGE
# =========================

@app.route('/docprofile')
@login_required
def docprofile():
    return render_template('docprofile.html')


# =========================
# GLOBAL ASYNC API
# =========================

@app.route('/api/doc-profile', methods=['GET'])
def get_doc_profile():
    return jsonify({"success": True, "profile": GLOBAL_DOCTOR_PROFILE})


@app.route('/api/doc-profile', methods=['POST'])
def update_doc_profile():
    global GLOBAL_DOCTOR_PROFILE
    data = request.get_json()
    GLOBAL_DOCTOR_PROFILE = {
        "doctor_id": data.get("doctor_id", ""),
        "name": data.get("name", ""),
        "specialty": data.get("specialty", ""),
        "experience": data.get("experience", ""),
        "bio": data.get("bio", "")
    }
    return jsonify({"success": True, "message": "Doctor profile updated successfully", "profile": GLOBAL_DOCTOR_PROFILE})


@app.route('/login')
def login():
    if 'user_id' in session:
        if session.get('role') == 'doctor':
            return redirect(url_for('docprofile'))
        else:
            return redirect(url_for('schedule'))
    return render_template('login.html')


@app.route('/api/authenticate', methods=['POST'])
def authenticate():
    data = request.get_json()
    user_id = data.get('user_id', '').strip()
    password = data.get('password', '').strip()

    if not user_id or not password:
        return jsonify({'success': False, 'message': 'Please enter both User ID and Password'}), 400

    role = None
    if user_id.startswith('P'):
        role = 'patient'
        credentials = credentials_data.get('patients', {})
    elif user_id.startswith('D'):
        role = 'doctor'
        credentials = credentials_data.get('doctors', {})
    else:
        return jsonify({'success': False, 'message': 'Invalid User ID format. Use P### for patients or D### for doctors'}), 401

    user_creds = credentials.get(user_id)
    if not user_creds or user_creds.get('password') != password:
        return jsonify({'success': False, 'message': 'Invalid User ID or Password'}), 401

    if role == 'patient':
        user_profile = patients_data.get(user_id, {})
        user_name = user_profile.get('patient_name', 'Unknown Patient')
    else:
        user_profile = doctors_data.get(user_id, {})
        user_name = user_profile.get('name', 'Unknown Doctor')

    session.permanent = True
    session['user_id'] = user_id
    session['role'] = role
    session['name'] = user_name
    session['profile'] = user_profile

    redirect_url = '/docprofile' if role == 'doctor' else '/schedule'

    return jsonify({
        'success': True,
        'message': 'Login successful',
        'role': role,
        'user_id': user_id,
        'name': user_name,
        'redirect_url': redirect_url
    })


@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'})


@app.route('/api/session', methods=['GET'])
def get_session():
    if 'user_id' not in session:
        return jsonify({'authenticated': False})
    return jsonify({
        'authenticated': True,
        'user_id': session.get('user_id'),
        'role': session.get('role'),
        'name': session.get('name'),
        'profile': session.get('profile', {})
    })


# =========================
# EXISTING APIs
# =========================

@app.route('/api/book', methods=['POST'])
@login_required
def book_appointment():
    data = request.get_json()
    date = data.get('date')
    time = data.get('time')
    doctor_id = data.get('doctor_id', 'LOCAL')
    doctor_name = data.get('doctor_name', '')
    doctor_specialty = data.get('doctor_specialty', '')

    if not date or not time:
        return jsonify({'success': False, 'message': 'Date and time required'}), 400

    if date in available_slots and time in available_slots[date]:
        available_slots[date].remove(time)

        new_apt_id = f"A{str(len(appointments_data) + 1).zfill(3)}"

        if not doctor_name:
            doctor = doctors_data.get(doctor_id, {})
            doctor_name = doctor.get('name', 'Unknown Doctor')
            doctor_specialty = doctor.get('specialty', 'General')

        patient_id = session.get('user_id')

        new_appointment = {
            'appointment_id': new_apt_id,
            'patient_id': patient_id,
            'doctor_id': doctor_id,
            'doctor_name': doctor_name,
            'doctor_specialty': doctor_specialty,
            'date': date,
            'time': time,
            'status': 'scheduled',
            'type': 'consultation',
            'notes': 'Scheduled via web portal',
            'booked_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        appointments_data[new_apt_id] = new_appointment
        return jsonify({'success': True, 'message': 'Appointment booked successfully'})

    return jsonify({'success': False, 'message': 'Slot not available'}), 400


@app.route('/api/slots/<date>')
def get_slots(date):
    return jsonify({'date': date, 'slots': available_slots.get(date, [])})


@app.route('/api/doctors')
def get_doctors():
    return jsonify({
        'success': True,
        'doctors': [
            {'doctor_id': doc_id, 'name': doc['name'], 'specialty': doc['specialty']}
            for doc_id, doc in doctors_data.items()
        ]
    })


@app.route('/api/patient')
@login_required
def get_patient():
    user_id = session.get('user_id')
    patient = patients_data.get(user_id, {})
    return jsonify({'success': True, 'patient': patient})


@app.route('/api/all-patients', methods=['GET'])
@login_required
def get_all_patients():
    return jsonify({'success': True, 'patients': patients_data})


@app.route('/patientinfo')
@login_required
def patientinfo():
    return render_template('patientinfo.html')


@app.route('/api/next-patient-id')
def next_patient_id():
    existing = list(patients_data.keys())
    nums = []
    for pid in existing:
        try:
            nums.append(int(pid.replace('P', '')))
        except:
            pass
    next_num = max(nums) + 1 if nums else 1
    return jsonify({'patient_id': f'P{str(next_num).zfill(3)}'})


@app.route('/api/patients', methods=['POST'])
def save_patient():
    data = request.get_json()
    patient_id = data.get('patient_id')
    if not patient_id or not data.get('patient_name'):
        return jsonify({'success': False, 'message': 'Patient ID and name are required'}), 400

    # 1. Update memory
    patients_data[patient_id] = {
        'patient_id':           patient_id,
        'patient_name':         data.get('patient_name', ''),
        'patient_age':          data.get('patient_age', 0),
        'blood_group':          data.get('blood_group', ''),
        'allergies':            data.get('allergies', []),
        'symptom':              data.get('symptom', ''),
        'diagnosis':            data.get('diagnosis', ''),
        'appointment_details':  data.get('appointment_details', ''),
        'dietary_restrictions': data.get('dietary_restrictions', ''),
        'prescription':         data.get('prescription', [])
    }

    # 2. Save patients.json
    try:
        with open(os.path.join('data', 'patients.json'), 'w') as f:
            json.dump(patients_data, f, indent=2)
    except Exception as e:
        return jsonify({'success': False, 'message': f'Failed to save patient data: {str(e)}'}), 500

    # 3. Auto-generate credentials if new patient
    try:
        creds_path = os.path.join('data', 'credentials.json')
        creds_store = {}
        try:
            with open(creds_path, 'r') as f:
                creds_store = json.load(f)
        except:
            creds_store = {"patients": {}, "doctors": {}}
            
        if 'patients' not in creds_store:
            creds_store['patients'] = {}

        if patient_id not in creds_store['patients']:
            numeric_part = ''.join(filter(str.isdigit, patient_id)) or "000"
            creds_store['patients'][patient_id] = {
                'patient_id': patient_id,
                'password': f"patient{numeric_part}"
            }
            with open(creds_path, 'w') as f:
                json.dump(creds_store, f, indent=2)
            global credentials_data
            credentials_data = creds_store
    except Exception as e:
        print(f"⚠️ Credential sync failed (non-fatal): {e}")

    return jsonify({'success': True, 'patient_id': patient_id})

# =========================
# SYMPTOM ANALYZER
# =========================

@app.route('/api/analyze-symptom', methods=['POST'])
def analyze_symptom():
    try:
        service = get_inference_service()
        if service is None:
            return jsonify({'success': False, 'error': 'Model not available'}), 503

        data = request.get_json()
        image_data = data['image'].split(',')[-1]
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        result = service.analyze_symptom(image)
        return jsonify(result)

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# =========================
# PROFILE & CONTACTS API
# =========================

def load_contacts_data():
    try:
        filepath = os.path.join('data', 'patient_contacts.json')
        with open(filepath, 'r') as f:
            return json.load(f)
    except:
        return {}


@app.route('/api/patient-contact/<patient_id>', methods=['GET'])
def get_patient_contact(patient_id):
    contacts = load_contacts_data()
    return jsonify({'success': True, 'contact': contacts.get(patient_id, {})})


@app.route('/api/patient-contact', methods=['POST'])
def save_patient_contact():
    data = request.get_json()
    pid = data.get('patient_id')

    if not pid:
        return jsonify({'success': False, 'message': 'No patient ID provided'}), 400

    contacts = load_contacts_data()
    contacts[pid] = {
        'patient_id': pid,
        'email': data.get('email', ''),
        'contact_number': data.get('contact_number', ''),
        'emergency_contact': data.get('emergency_contact', '')
    }

    try:
        os.makedirs('data', exist_ok=True)
        filepath = os.path.join('data', 'patient_contacts.json')
        with open(filepath, 'w') as f:
            json.dump(contacts, f, indent=2)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# =========================
# CHATBOT API ENDPOINTS
# FIXED: use session user_id instead of hardcoded CURRENT_PATIENT_ID
# =========================

import secrets

def _get_chatbot_service():
    """Lazy-load chatbot service to prevent app startup crashes"""
    try:
        from chatbot.service import get_chatbot_service as _get_service
        return _get_service()
    except Exception as e:
        print(f"⚠️ Chatbot service failed to load: {e}")
        return None


@app.route('/api/chatbot/query', methods=['POST'])
@login_required  # Protect patient data access
def chatbot_query():
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        session_id = data.get('session_id')

        if not query:
            return jsonify({'success': False, 'message': 'Query is required'}), 400

        # ✅ Use logged-in user instead of hardcoded P001
        patient_id = session.get('user_id', 'P001')

        # ✅ Generate session_id if frontend didn't provide one
        if not session_id:
            session_id = f"session_{patient_id}_{secrets.token_hex(8)}"

        service = _get_chatbot_service()
        if service is None:
            return jsonify({
                'success': False, 
                'message': 'Chatbot service is currently initializing or unavailable. Please try again in a moment.'
            }), 503

        result = service.process_query(
            patient_id=patient_id,
            query=query,
            session_id=session_id
        )

        return jsonify(result)

    except Exception as e:
        print(f"🔴 Chatbot query error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False, 
            'message': 'An error occurred processing your query',
            'error': str(e)
        }), 500


@app.route('/api/chatbot/status', methods=['GET'])
def chatbot_status():
    try:
        service = _get_chatbot_service()
        if service is None:
            return jsonify({
                'available': False,
                'message': 'Chatbot service failed to initialize'
            }), 503
            
        return jsonify({
            'available': True,
            'message': 'Chatbot service is ready',
            'huggingface_available': getattr(service, 'use_huggingface', False),
            'mode': 'LLM' if getattr(service, 'use_huggingface', False) else 'Template'
        })
    except Exception as e:
        return jsonify({'available': False, 'message': f'Chatbot service unavailable: {str(e)}'}), 503


@app.route('/api/chatbot/history', methods=['GET'])
@login_required
def chatbot_history():
    try:
        session_id = request.args.get('session_id')
        if not session_id:
            # Fallback to user-based session if not provided
            patient_id = session.get('user_id', 'P001')
            session_id = f"session_{patient_id}_default"
            
        service = _get_chatbot_service()
        if service is None:
            return jsonify({'success': False, 'message': 'Service unavailable'}), 503
            
        history = service.get_conversation_history(session_id)
        return jsonify({'success': True, 'history': history, 'session_id': session_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/chatbot/clear', methods=['POST'])
@login_required
def chatbot_clear():
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        if not session_id:
            patient_id = session.get('user_id', 'P001')
            session_id = f"session_{patient_id}_default"
            
        service = _get_chatbot_service()
        if service is None:
            return jsonify({'success': False, 'message': 'Service unavailable'}), 503
            
        service.clear_conversation_history(session_id)
        return jsonify({'success': True, 'message': 'Conversation history cleared'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(
        debug=os.environ.get('FLASK_DEBUG') == '1',
        host='0.0.0.0',
        port=int(os.environ.get('PORT', '5000')),
    )
