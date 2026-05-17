**User:**

<task>
look at the "schedule" page, look where you cam improve the UI design without changing the colour scheme
</task>
<environment_details>
# VSCode Visible Files
..\..\..\..\..\85,.gitignore,test_chatbot_simple.py

# VSCode Open Tabs
templates/schedule.html,templates/appointments.html,templates/profile.html,templates/assistant.html,requirements.txt,medical_chatbot.py,test_chatbot.py,SETUP_GUIDE.md,README.md,app.py,.env,chatbot/service.py,test_chatbot_simple.py,static/style.css

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T11:26:12.209Z
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
.gitignore
app.py
CHATBOT_DOCUMENTATION.md
CHATBOT_SETUP.md
DATA_STRUCTURE.md
README.md
requirements.txt
SETUP_INSTRUCTIONS.md
test_api.py
test_chatbot_simple.py
test_chatbot.py
chatbot/
chatbot/__init__.py
chatbot/config.py
chatbot/context.py
chatbot/safety.py
chatbot/service.py
chatbot/templates.py
data/
data/appointments.json
data/credentials.json
data/doctors.json
data/patient_contacts.json
data/patients.json
frontend/
frontend/src/
frontend/src/App.tsx
frontend/src/components/
frontend/src/components/SymptomAnalyzer.tsx
frontend/src/components/TopNav.tsx
frontend/src/services/
frontend/src/services/symptomAnalyzerService.ts
frontend/src/types/
frontend/src/types/symptom.ts
model/
model/config.py
model/dataset_loader.py
model/inference_pretrained.py
model/inference.py
model/train_biomedclip.py
static/
static/style.css
templates/
templates/appointments.html
templates/docprofile.html
templates/index.html
templates/login.html
templates/patientinfo.html
templates/profile.html
templates/schedule.html
templates/symptom_analyzer.html
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I'll analyze the schedule page to identify UI improvements while maintaining the current color scheme.

<read_file>
<args>
<file>
<path>templates/schedule.html</path>
</file>
<file>
<path>static/style.css</path>
</file>
</args>
</read_file>

---

**User:**

[read_file for 'templates/schedule.html', 'static/style.css'] Result:
<files>
<file><path>templates/schedule.html</path>
<content lines="1-615">
  1 | <!DOCTYPE html>
  2 | <html lang="en">
  3 | <head>
  4 |     <meta charset="UTF-8">
  5 |     <meta name="viewport" content="width=device-width, initial-scale=1.0">
  6 |     <title>MedAssistant - Schedule Appointment</title>
  7 |     <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
  8 | </head>
  9 | <body>
 10 |     <!-- Navigation Header -->
 11 |    <header class="navbar">
 12 |     <div class="container">
 13 |         <div class="nav-brand">
 14 |             <svg class="logo-icon" width="32" height="32" viewBox="0 0 32 32" fill="none">
 15 |                 <rect x="14" y="8" width="4" height="16" fill="#2563eb"/>
 16 |                 <rect x="8" y="14" width="16" height="4" fill="#2563eb"/>
 17 |                 <circle cx="16" cy="16" r="14" stroke="#2563eb" stroke-width="2" fill="none"/>
 18 |             </svg>
 19 |             <h1>MedAssistant</h1>
 20 |         </div>
 21 |         <nav class="nav-links" id="main-nav">
 22 |             <!-- Populated by JS based on role -->
 23 |         </nav>
 24 |         <button class="btn btn-secondary" id="logout-btn"
 25 |             style="font-size:13px;height:34px;padding:0 14px;"
 26 |             onclick="logout()">
 27 |             Log out
 28 |         </button>
 29 |     </div>
 30 | </header>
 31 | 
 32 | <script>
 33 |     (function () {
 34 |         const role = localStorage.getItem('userRole');
 35 | 
 36 |         if (!role) {
 37 |             window.location.href = '/login';
 38 |             return;
 39 |         }
 40 | 
 41 |         const currentPath = window.location.pathname;
 42 | 
 43 |         if (role === 'patient' && currentPath === '/docprofile') {
 44 |             window.location.href = '/';
 45 |             return;
 46 |         }
 47 | 
 48 |         if (role === 'doctor' && currentPath === '/') {
 49 |             window.location.href = '/docprofile';
 50 |             return;
 51 |         }
 52 | 
 53 |         const nav = document.getElementById('main-nav');
 54 | 
 55 |         const patientLinks = `
 56 |             <a href="/" class="nav-link ${currentPath === '/' ? 'active' : ''}">Schedule</a>
 57 |             <a href="/appointments" class="nav-link ${currentPath === '/appointments' ? 'active' : ''}">My Appointments</a>
 58 |             <a href="/profile" class="nav-link ${currentPath === '/profile' ? 'active' : ''}">Profile</a>
 59 |         `;
 60 | 
 61 |         const doctorLinks = `
 62 |             <a href="/docprofile" class="nav-link ${currentPath === '/docprofile' ? 'active' : ''}">Doctor Profile</a>
 63 |             <a href="/patientinfo" class="nav-link ${currentPath === '/patientinfo' ? 'active' : ''}">Patient Info</a>
 64 |         `;
 65 | 
 66 |         nav.innerHTML = role === 'doctor' ? doctorLinks : patientLinks;
 67 |     })();
 68 | 
 69 |     async function logout() {
 70 |         try {
 71 |             await fetch('/api/logout', {
 72 |                 method: 'POST',
 73 |                 headers: { 'Content-Type': 'application/json' }
 74 |             });
 75 |         } catch (error) {
 76 |             console.error('Logout error:', error);
 77 |         }
 78 |         localStorage.removeItem('userRole');
 79 |         localStorage.removeItem('userId');
 80 |         localStorage.removeItem('userName');
 81 |         window.location.href = '/login';
 82 |     }
 83 | </script>
 84 | 
 85 |     <!-- Main Content -->
 86 |     <main class="main-content">
 87 |         <div class="container">
 88 |             <div class="page-header">
 89 |                 <h2>Schedule Follow-Up Appointment</h2>
 90 |                 <p class="subtitle">Select a convenient date and time for your next consultation</p>
 91 |             </div>
 92 | 
 93 |             <div class="content-grid">
 94 |                 <!-- Left Column: Chatbot & Appointment Booking -->
 95 |                 <section class="booking-section">
 96 |                     <!-- AI Medical Chatbot -->
 97 |                     <div class="card chatbot-card">
 98 |                         <div class="chatbot-header-section">
 99 |                             <h3 class="card-title">💬 Medical Assistant</h3>
100 |                             <p class="chatbot-subtitle">Ask about medications, diet, or appointments</p>
101 |                         </div>
102 |                         
103 |                         <div class="chatbot-chat-container">
104 |                             <div class="chatbot-messages" id="chatbot-messages">
105 |                                 <div class="chatbot-message bot-message">
106 |                                     <div class="message-avatar bot-avatar">🤖</div>
107 |                                     <div class="message-content">
108 |                                         <p>Hello! I'm your medical assistant. I can help you with:</p>
109 |                                         <ul>
110 |                                             <li>Medication information</li>
111 |                                             <li>Dietary advice</li>
112 |                                             <li>Appointment scheduling</li>
113 |                                             <li>Allergy information</li>
114 |                                         </ul>
115 |                                         <p>How can I assist you today?</p>
116 |                                     </div>
117 |                                 </div>
118 |                             </div>
119 |                             
120 |                             <div class="chatbot-typing" id="chatbot-typing" style="display: none;">
121 |                                 <div class="typing-indicator">
122 |                                     <span></span>
123 |                                     <span></span>
124 |                                     <span></span>
125 |                                 </div>
126 |                             </div>
127 |                         </div>
128 |                         
129 |                         <div class="chatbot-quick-actions">
130 |                             <button class="quick-action-btn" data-query="What medications am I taking?">
131 |                                 💊 My Medications
132 |                             </button>
133 |                             <button class="quick-action-btn" data-query="What should I eat with my condition?">
134 |                                 🥗 Diet Advice
135 |                             </button>
136 |                             <button class="quick-action-btn" data-query="What are my allergies?">
137 |                                 ⚠️ My Allergies
138 |                             </button>
139 |                         </div>
140 |                         
141 |                         <div class="chatbot-input-container">
142 |                             <input
143 |                                 type="text"
144 |                                 id="chatbot-input"
145 |                                 class="chatbot-input"
146 |                                 placeholder="Type your question..."
147 |                                 autocomplete="off"
148 |                             />
149 |                             <button id="chatbot-send" class="chatbot-send-btn">
150 |                                 <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
151 |                                     <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
152 |                                 </svg>
153 |                             </button>
154 |                         </div>
155 |                     </div>
156 | 
157 |                     <!-- Book Your Appointment -->
158 |                     <div class="card">
159 |                         <h3 class="card-title">Book Your Appointment</h3>
160 | 
161 |                         <div class="form-group">
162 |                             <label for="appointment-date" class="form-label">Select Date</label>
163 |                             <select id="appointment-date" class="form-select">
164 |                                 <option value="">Choose a date...</option>
165 |                                 {% for date in available_slots.keys() %}
166 |                                 <option value="{{ date }}">{{ date }}</option>
167 |                                 {% endfor %}
168 |                             </select>
169 |                         </div>
170 | 
171 |                         <div class="form-group">
172 |                             <label class="form-label">Available Time Slots</label>
173 |                             <div id="time-slots-container" class="time-slots-grid">
174 |                                 <p class="placeholder-text">Please select a date to view available time slots</p>
175 |                             </div>
176 |                         </div>
177 | 
178 |                         <div id="doctor-selector-area" style="display:none;">
179 |                             <div class="doctor-selector-panel">
180 |                                 <div class="doctor-selector-header">
181 |                                     <span class="doctor-selector-label">Consulting Doctor</span>
182 |                                     <span class="doctor-selector-hint">Choose your preferred doctor</span>
183 |                                 </div>
184 |                                 <div id="doctor-selector-body"></div>
185 |                             </div>
186 |                         </div>
187 | 
188 |                         <div id="confirmation-area" class="confirmation-area" style="display: none;">
189 |                             <div class="confirmation-card">
190 |                                 <h4>Selected Appointment</h4>
191 |                                 <div class="confirmation-details">
192 |                                     <div class="detail-row">
193 |                                         <span class="detail-label">Date:</span>
194 |                                         <span id="selected-date" class="detail-value">-</span>
195 |                                     </div>
196 |                                     <div class="detail-row">
197 |                                         <span class="detail-label">Time:</span>
198 |                                         <span id="selected-time" class="detail-value">-</span>
199 |                                     </div>
200 |                                     <div class="detail-row">
201 |                                         <span class="detail-label">Doctor:</span>
202 |                                         <span id="selected-doctor" class="detail-value">-</span>
203 |                                     </div>
204 |                                     <div class="detail-row">
205 |                                         <span class="detail-label">Specialty:</span>
206 |                                         <span id="selected-specialty" class="detail-value">-</span>
207 |                                     </div>
208 |                                 </div>
209 |                                 <button id="confirm-booking" class="btn btn-primary">Confirm Booking</button>
210 |                                 <button id="cancel-selection" class="btn btn-secondary">Cancel</button>
211 |                             </div>
212 |                         </div>
213 |                     </div>
214 | 
215 |                     {% if booked_appointments %}
216 |                     <div class="card">
217 |                         <h3 class="card-title">Your Upcoming Appointments</h3>
218 |                         <div class="appointments-list">
219 |                             {% for appointment in booked_appointments %}
220 |                             <div class="appointment-item">
221 |                                 <div class="appointment-icon">
222 |                                     <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
223 |                                         <path d="M8 7V3M16 7V3M7 11H17M5 21H19C20.1046 21 21 20.1046 21 19V7C21 5.89543 20.1046 5 19 5H5C3.89543 5 3 5.89543 3 7V19C3 20.1046 3.89543 21 5 21Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
224 |                                     </svg>
225 |                                 </div>
226 |                                 <div class="appointment-details">
227 |                                     <div class="appointment-date">{{ appointment.date }} at {{ appointment.time }}</div>
228 |                                     <div class="appointment-doctor">{{ appointment.doctor }} - {{ appointment.specialty }}</div>
229 |                                 </div>
230 |                             </div>
231 |                             {% endfor %}
232 |                         </div>
233 |                     </div>
234 |                     {% endif %}
235 |                 </section>
236 | 
237 |                 <!-- Right Column -->
238 |                 <aside class="reminders-section">
239 |                     <div class="card">
240 |                         <h3 class="card-title">Medication Reminders</h3>
241 |                         <div class="reminders-list">
242 |                             {% for reminder in medication_reminders %}
243 |                             <div class="reminder-item">
244 |                                 <div class="reminder-icon medication-icon">
245 |                                     <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
246 |                                         <path d="M4.5 16.5C3 15 3 12.5 4.5 11L11 4.5C12.5 3 15 3 16.5 4.5C18 6 18 8.5 16.5 10L10 16.5C8.5 18 6 18 4.5 16.5Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
247 |                                         <path d="M13.5 6.5L17.5 10.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
248 |                                     </svg>
249 |                                 </div>
250 |                                 <div class="reminder-content">
251 |                                     <div class="reminder-title">{{ reminder.medication }}</div>
252 |                                     <div class="reminder-time">{{ reminder.time }} - {{ reminder.frequency }}</div>
253 |                                     <div class="reminder-notes">{{ reminder.notes }}</div>
254 |                                 </div>
255 |                             </div>
256 |                             {% endfor %}
257 |                         </div>
258 |                     </div>
259 | 
260 |                     <div class="card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none;">
261 |                         <h3 class="card-title" style="color: white;">🔬 AI Symptom Analyzer</h3>
262 |                         <p style="margin: 15px 0; font-size: 14px; opacity: 0.95;">
263 |                             Upload an image of a skin condition for instant AI-powered analysis and recommendations.
264 |                         </p>
265 |                         <a href="{{ url_for('symptom_analyzer') }}" class="btn btn-primary" style="background: white; color: #667eea; border: none; width: 100%; font-weight: 600;">
266 |                             Check Symptom Now →
267 |                         </a>
268 |                     </div>
269 | 
270 |                     <div class="card">
271 |                         <h3 class="card-title">Upcoming Tasks</h3>
272 |                         <div class="tasks-list">
273 |                             {% for task in upcoming_tasks %}
274 |                             <div class="task-item">
275 |                                 <div class="task-icon">
276 |                                     <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
277 |                                         <path d="M9 11L12 14L22 4M21 12V19C21 20.1046 20.1046 21 19 21H5C3.89543 21 3 20.1046 3 19V5C3 3.89543 3.89543 5 5 5H16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
278 |                                     </svg>
279 |                                 </div>
280 |                                 <div class="task-content">
281 |                                     <div class="task-title">{{ task.task }}</div>
282 |                                     <div class="task-datetime">{{ task.date }} at {{ task.time }}</div>
283 |                                     <div class="task-location">{{ task.location }}</div>
284 |                                 </div>
285 |                             </div>
286 |                             {% endfor %}
287 |                         </div>
288 |                     </div>
289 |                 </aside>
290 |             </div>
291 |         </div>
292 |     </main>
293 | 
294 |     <!-- Success Modal -->
295 |     <div id="success-modal" class="modal" style="display: none;">
296 |         <div class="modal-content">
297 |             <div class="modal-icon success-icon">
298 |                 <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
299 |                     <path d="M22 11.08V12C21.9988 14.1564 21.3005 16.2547 20.0093 17.9818C18.7182 19.7088 16.9033 20.9725 14.8354 21.5839C12.7674 22.1953 10.5573 22.1219 8.53447 21.3746C6.51168 20.6273 4.78465 19.2461 3.61096 17.4371C2.43727 15.628 1.87979 13.4881 2.02168 11.3363C2.16356 9.18455 2.99721 7.13631 4.39828 5.49706C5.79935 3.85781 7.69279 2.71537 9.79619 2.24013C11.8996 1.76489 14.1003 1.98232 16.07 2.86" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
300 |                     <path d="M22 4L12 14.01L9 11.01" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
301 |                 </svg>
302 |             </div>
303 |             <h3>Appointment Confirmed!</h3>
304 |             <p id="success-message">Your appointment has been successfully booked.</p>
305 |             <button id="close-modal" class="btn btn-primary">Close</button>
306 |         </div>
307 |     </div>
308 | 
309 |     <script type="application/json" id="available-slots-data">
310 |         {{ available_slots | tojson | safe }}
311 |     </script>
312 | 
313 |     <script>
314 |         // ===================================
315 |         // Appointment Booking Logic
316 |         // ===================================
317 |         const availableSlots = JSON.parse(document.getElementById('available-slots-data').textContent);
318 |         let selectedDate = null;
319 |         let selectedTime = null;
320 |         let selectedDoctor = null;
321 | 
322 |         function loadDoctorsFromStorage() {
323 |             const saved = JSON.parse(localStorage.getItem('savedDoctorProfiles') || '[]');
324 |             return saved.filter(d => d.name && d.name.trim() !== '');
325 |         }
326 | 
327 |         function buildDoctorSelector() {
328 |             const doctors = loadDoctorsFromStorage();
329 |             const selectorArea = document.getElementById('doctor-selector-area');
330 |             const selectorBody = document.getElementById('doctor-selector-body');
331 | 
332 |             selectorArea.style.display = 'block';
333 |             selectorBody.innerHTML = '';
334 | 
335 |             if (doctors.length === 0) {
336 |                 selectorBody.innerHTML = `
337 |                     <div class="doctor-empty">
338 |                         No doctors saved yet.
339 |                         <a href="/docprofile" class="doctor-empty-link">Add one in Doctor Profile →</a>
340 |                     </div>
341 |                 `;
342 |                 selectedDoctor = null;
343 |                 document.getElementById('selected-doctor').textContent = 'None assigned';
344 |                 document.getElementById('selected-specialty').textContent = '-';
345 |                 return;
346 |             }
347 | 
348 |             const grid = document.createElement('div');
349 |             grid.className = 'doctor-options-grid';
350 | 
351 |             doctors.forEach((doc, idx) => {
352 |                 const card = document.createElement('div');
353 |                 card.className = 'doctor-option-card' + (idx === 0 ? ' selected' : '');
354 |                 card.dataset.index = idx;
355 | 
356 |                 const initials = doc.name
357 |                     .split(' ')
358 |                     .filter(w => w.length > 0)
359 |                     .slice(0, 2)
360 |                     .map(w => w[0].toUpperCase())
361 |                     .join('');
362 | 
363 |                 card.innerHTML = `
364 |                     <div class="doctor-option-avatar">${initials}</div>
365 |                     <div class="doctor-option-info">
366 |                         <div class="doctor-option-name">${doc.name}</div>
367 |                         <div class="doctor-option-specialty">${doc.specialty || 'No specialty'}</div>
368 |                         ${doc.experience ? `<div class="doctor-option-exp">${doc.experience} yrs experience</div>` : ''}
369 |                     </div>
370 |                     <div class="doctor-option-check">
371 |                         <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
372 |                             <path d="M20 6L9 17L4 12" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
373 |                         </svg>
374 |                     </div>
375 |                 `;
376 | 
377 |                 card.addEventListener('click', function () {
378 |                     document.querySelectorAll('.doctor-option-card').forEach(c => c.classList.remove('selected'));
379 |                     this.classList.add('selected');
380 |                     const i = parseInt(this.dataset.index);
381 |                     selectedDoctor = loadDoctorsFromStorage()[i];
382 |                     document.getElementById('selected-doctor').textContent = selectedDoctor.name;
383 |                     document.getElementById('selected-specialty').textContent = selectedDoctor.specialty || '-';
384 |                 });
385 | 
386 |                 grid.appendChild(card);
387 |             });
388 | 
389 |             selectorBody.appendChild(grid);
390 | 
391 |             // Auto-select first
392 |             selectedDoctor = doctors[0];
393 |             document.getElementById('selected-doctor').textContent = doctors[0].name;
394 |             document.getElementById('selected-specialty').textContent = doctors[0].specialty || '-';
395 |         }
396 | 
397 |         // Date change handler
398 |         document.getElementById('appointment-date').addEventListener('change', function (e) {
399 |             selectedDate = e.target.value;
400 |             selectedTime = null;
401 | 
402 |             const slotsContainer = document.getElementById('time-slots-container');
403 |             const confirmationArea = document.getElementById('confirmation-area');
404 |             const selectorArea = document.getElementById('doctor-selector-area');
405 | 
406 |             confirmationArea.style.display = 'none';
407 |             selectorArea.style.display = 'none';
408 | 
409 |             if (selectedDate && availableSlots[selectedDate]) {
410 |                 const slots = availableSlots[selectedDate];
411 | 
412 |                 if (slots.length === 0) {
413 |                     slotsContainer.innerHTML = '<p class="placeholder-text">No available slots for this date</p>';
414 |                 } else {
415 |                     slotsContainer.innerHTML = '';
416 |                     slots.forEach(time => {
417 |                         const slotCard = document.createElement('div');
418 |                         slotCard.className = 'time-slot-card';
419 |                         slotCard.textContent = time;
420 |                         slotCard.dataset.time = time;
421 | 
422 |                         slotCard.addEventListener('click', function () {
423 |                             document.querySelectorAll('.time-slot-card').forEach(c => c.classList.remove('selected'));
424 |                             this.classList.add('selected');
425 |                             selectedTime = this.dataset.time;
426 | 
427 |                             document.getElementById('selected-date').textContent = selectedDate;
428 |                             document.getElementById('selected-time').textContent = selectedTime;
429 | 
430 |                             buildDoctorSelector();
431 |                             confirmationArea.style.display = 'block';
432 |                             confirmationArea.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
433 |                         });
434 | 
435 |                         slotsContainer.appendChild(slotCard);
436 |                     });
437 |                 }
438 |             } else {
439 |                 slotsContainer.innerHTML = '<p class="placeholder-text">Please select a date to view available time slots</p>';
440 |             }
441 |         });
442 | 
443 |         // Cancel selection — FIXED: no longer wrapping chatbot code inside this handler
444 |         document.getElementById('cancel-selection').addEventListener('click', function () {
445 |             document.querySelectorAll('.time-slot-card').forEach(c => c.classList.remove('selected'));
446 |             document.getElementById('confirmation-area').style.display = 'none';
447 |             document.getElementById('doctor-selector-area').style.display = 'none';
448 |             selectedTime = null;
449 |             selectedDoctor = null;
450 |         });
451 | 
452 |         // Confirm booking
453 |         document.getElementById('confirm-booking').addEventListener('click', function () {
454 |             if (!selectedDate || !selectedTime) {
455 |                 alert('Please select a date and time.');
456 |                 return;
457 |             }
458 |             if (!selectedDoctor) {
459 |                 alert('Please select a doctor before confirming.');
460 |                 return;
461 |             }
462 | 
463 |             fetch('/api/book', {
464 |                 method: 'POST',
465 |                 headers: { 'Content-Type': 'application/json' },
466 |                 body: JSON.stringify({
467 |                     date: selectedDate,
468 |                     time: selectedTime,
469 |                     doctor_name: selectedDoctor.name,
470 |                     doctor_specialty: selectedDoctor.specialty,
471 |                     doctor_id: selectedDoctor.doctor_id || 'LOCAL'
472 |                 })
473 |             })
474 |             .then(r => r.json())
475 |             .then(data => {
476 |                 if (data.success) {
477 |                     document.getElementById('success-message').textContent =
478 |                         `Your appointment on ${selectedDate} at ${selectedTime} with ${selectedDoctor.name} has been confirmed.`;
479 |                     document.getElementById('success-modal').style.display = 'flex';
480 | 
481 |                     const idx = availableSlots[selectedDate].indexOf(selectedTime);
482 |                     if (idx > -1) availableSlots[selectedDate].splice(idx, 1);
483 | 
484 |                     document.getElementById('confirmation-area').style.display = 'none';
485 |                     document.getElementById('doctor-selector-area').style.display = 'none';
486 |                     document.getElementById('appointment-date').value = '';
487 |                     document.getElementById('time-slots-container').innerHTML =
488 |                         '<p class="placeholder-text">Please select a date to view available time slots</p>';
489 |                     selectedDate = null;
490 |                     selectedTime = null;
491 |                     selectedDoctor = null;
492 |                 } else {
493 |                     alert(data.message || 'Failed to book appointment');
494 |                 }
495 |             })
496 |             .catch(err => {
497 |                 console.error(err);
498 |                 alert('An error occurred while booking.');
499 |             });
500 |         });
501 | 
502 |         // Close modal
503 |         document.getElementById('close-modal').addEventListener('click', function () {
504 |             document.getElementById('success-modal').style.display = 'none';
505 |             location.reload();
506 |         });
507 | 
508 |         document.getElementById('success-modal').addEventListener('click', function (e) {
509 |             if (e.target === this) {
510 |                 this.style.display = 'none';
511 |                 location.reload();
512 |             }
513 |         });
514 | 
515 | 
516 |         // ===================================
517 |         // Chatbot Logic — FIXED: properly placed at top level, not nested inside cancel handler
518 |         // ===================================
519 |         const chatbotMessages = document.getElementById('chatbot-messages');
520 |         const chatbotInput = document.getElementById('chatbot-input');
521 |         const chatbotSend = document.getElementById('chatbot-send');
522 |         const chatbotTyping = document.getElementById('chatbot-typing');
523 |         const quickActionBtns = document.querySelectorAll('.quick-action-btn');
524 | 
525 |         let sessionId = 'session_' + Date.now();
526 | 
527 |         function addMessage(text, isBot = false) {
528 |             const messageDiv = document.createElement('div');
529 |             messageDiv.className = `chatbot-message ${isBot ? 'bot-message' : 'user-message'}`;
530 | 
531 |             if (isBot) {
532 |                 messageDiv.innerHTML = `
533 |                     <div class="message-avatar bot-avatar">🤖</div>
534 |                     <div class="message-content">${formatMessage(text)}</div>
535 |                 `;
536 |             } else {
537 |                 messageDiv.innerHTML = `
538 |                     <div class="message-content">${escapeHtml(text)}</div>
539 |                     <div class="message-avatar user-avatar">👤</div>
540 |                 `;
541 |             }
542 | 
543 |             chatbotMessages.appendChild(messageDiv);
544 |             chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
545 |         }
546 | 
547 |         function formatMessage(text) {
548 |             text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
549 |             text = text.replace(/^[•\-\*]\s+(.+)$/gm, '<li>$1</li>');
550 |             text = text.replace(/(<li>.*<\/li>\s*)+/g, '<ul>$&</ul>');
551 |             text = text.replace(/\n/g, '<br>');
552 |             return text;
553 |         }
554 | 
555 |         function escapeHtml(text) {
556 |             const div = document.createElement('div');
557 |             div.textContent = text;
558 |             return div.innerHTML;
559 |         }
560 | 
561 |         async function sendMessage(query) {
562 |             if (!query.trim()) return;
563 | 
564 |             addMessage(query, false);
565 |             chatbotInput.value = '';
566 | 
567 |             chatbotTyping.style.display = 'block';
568 |             chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
569 | 
570 |             try {
571 |                 const response = await fetch('/api/chatbot/query', {
572 |                     method: 'POST',
573 |                     headers: { 'Content-Type': 'application/json' },
574 |                     body: JSON.stringify({
575 |                         query: query,
576 |                         session_id: sessionId
577 |                     })
578 |                 });
579 | 
580 |                 const data = await response.json();
581 |                 chatbotTyping.style.display = 'none';
582 | 
583 |                 if (data.success) {
584 |                     addMessage(data.response, true);
585 |                 } else {
586 |                     addMessage('Sorry, I encountered an error. Please try again.', true);
587 |                 }
588 |             } catch (error) {
589 |                 console.error('Chatbot error:', error);
590 |                 chatbotTyping.style.display = 'none';
591 |                 addMessage("Sorry, I'm having trouble connecting. Please try again later.", true);
592 |             }
593 |         }
594 | 
595 |         // Send button
596 |         chatbotSend.addEventListener('click', () => {
597 |             sendMessage(chatbotInput.value);
598 |         });
599 | 
600 |         // Enter key
601 |         chatbotInput.addEventListener('keypress', (e) => {
602 |             if (e.key === 'Enter') {
603 |                 sendMessage(chatbotInput.value);
604 |             }
605 |         });
606 | 
607 |         // Quick action buttons
608 |         quickActionBtns.forEach(btn => {
609 |             btn.addEventListener('click', () => {
610 |                 sendMessage(btn.dataset.query);
611 |             });
612 |         });
613 |     </script>
614 | </body>
615 | </html>
</content>
</file>
<file><path>static/style.css</path>
<content lines="1-959">
  1 | /* ===================================
  2 |    MedAssistant - Claude.com Design System
  3 |    Warm Editorial Medical Dashboard
  4 |    =================================== */
  5 | 
  6 | /* ===================================
  7 |    CSS Variables - Claude.com Palette
  8 |    =================================== */
  9 | :root {
 10 |     --color-primary: #cc785c;
 11 |     --color-primary-active: #a9583e;
 12 |     --color-primary-disabled: #e6dfd8;
 13 |     --color-accent-teal: #5db8a6;
 14 |     --color-accent-amber: #e8a55a;
 15 |     
 16 |     --color-canvas: #faf9f5;
 17 |     --color-surface-soft: #f5f0e8;
 18 |     --color-surface-card: #efe9de;
 19 |     --color-surface-cream-strong: #e8e0d2;
 20 |     --color-surface-dark: #181715;
 21 |     --color-surface-dark-elevated: #252320;
 22 |     --color-surface-dark-soft: #1f1e1b;
 23 |     --color-hairline: #e6dfd8;
 24 |     --color-hairline-soft: #ebe6df;
 25 |     
 26 |     --color-ink: #141413;
 27 |     --color-body-strong: #252523;
 28 |     --color-body: #3d3d3a;
 29 |     --color-muted: #6c6a64;
 30 |     --color-muted-soft: #8e8b82;
 31 |     --color-on-primary: #ffffff;
 32 |     --color-on-dark: #faf9f5;
 33 |     --color-on-dark-soft: #a09d96;
 34 |     
 35 |     --color-success: #5db872;
 36 |     --color-warning: #d4a017;
 37 |     --color-error: #c64545;
 38 |     
 39 |     --spacing-xxs: 4px;
 40 |     --spacing-xs: 8px;
 41 |     --spacing-sm: 12px;
 42 |     --spacing-md: 16px;
 43 |     --spacing-lg: 24px;
 44 |     --spacing-xl: 32px;
 45 |     --spacing-xxl: 48px;
 46 |     --spacing-section: 96px;
 47 |     
 48 |     --rounded-xs: 4px;
 49 |     --rounded-sm: 6px;
 50 |     --rounded-md: 8px;
 51 |     --rounded-lg: 12px;
 52 |     --rounded-xl: 16px;
 53 |     --rounded-pill: 9999px;
 54 |     --rounded-full: 50%;
 55 |     
 56 |     --font-display: 'Tiempos Headline', 'Cormorant Garamond', 'EB Garamond', Garamond, 'Times New Roman', serif;
 57 |     --font-body: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
 58 |     --font-code: 'JetBrains Mono', 'Courier New', monospace;
 59 |     
 60 |     --shadow-subtle: 0 1px 3px rgba(20, 20, 19, 0.08);
 61 | }
 62 | 
 63 | /* ===================================
 64 |    Reset and Base Styles
 65 |    =================================== */
 66 | * {
 67 |     margin: 0;
 68 |     padding: 0;
 69 |     box-sizing: border-box;
 70 | }
 71 | 
 72 | body {
 73 |     font-family: var(--font-body);
 74 |     background-color: var(--color-canvas);
 75 |     color: var(--color-body);
 76 |     line-height: 1.55;
 77 |     font-size: 16px;
 78 |     font-weight: 400;
 79 |     -webkit-font-smoothing: antialiased;
 80 |     -moz-osx-font-smoothing: grayscale;
 81 | }
 82 | 
 83 | h1, h2, h3, h4 {
 84 |     font-family: var(--font-display);
 85 |     font-weight: 400;
 86 |     color: var(--color-ink);
 87 |     line-height: 1.15;
 88 | }
 89 | 
 90 | h1 { font-size: 48px; letter-spacing: -1px; line-height: 1.1; }
 91 | h2 { font-size: 36px; letter-spacing: -0.5px; line-height: 1.15; }
 92 | h3 { font-size: 28px; letter-spacing: -0.3px; line-height: 1.2; }
 93 | h4 { font-size: 22px; letter-spacing: 0; line-height: 1.3; }
 94 | 
 95 | .title-lg { font-family: var(--font-body); font-size: 22px; font-weight: 500; line-height: 1.3; }
 96 | .title-md { font-family: var(--font-body); font-size: 18px; font-weight: 500; line-height: 1.4; }
 97 | .title-sm { font-family: var(--font-body); font-size: 16px; font-weight: 500; line-height: 1.4; }
 98 | .body-md { font-size: 16px; font-weight: 400; line-height: 1.55; }
 99 | .body-sm { font-size: 14px; font-weight: 400; line-height: 1.55; }
100 | .caption { font-size: 13px; font-weight: 500; line-height: 1.4; }
101 | .caption-uppercase { font-size: 12px; font-weight: 500; line-height: 1.4; letter-spacing: 1.5px; text-transform: uppercase; }
102 | 
103 | /* ===================================
104 |    Navigation Bar
105 |    =================================== */
106 | .navbar {
107 |     background-color: var(--color-canvas);
108 |     border-bottom: 1px solid var(--color-hairline);
109 |     position: sticky;
110 |     top: 0;
111 |     z-index: 1000;
112 |     height: 64px;
113 | }
114 | 
115 | .navbar .container {
116 |     max-width: 1200px;
117 |     margin: 0 auto;
118 |     padding: 0 var(--spacing-lg);
119 |     display: flex;
120 |     justify-content: space-between;
121 |     align-items: center;
122 |     height: 100%;
123 | }
124 | 
125 | .nav-brand {
126 |     display: flex;
127 |     align-items: center;
128 |     gap: var(--spacing-md);
129 | }
130 | 
131 | .logo-icon { width: 32px; height: 32px; }
132 | .logo-icon rect, .logo-icon circle { stroke: var(--color-primary); fill: var(--color-primary); }
133 | 
134 | .nav-brand h1 {
135 |     font-size: 24px;
136 |     font-weight: 500;
137 |     color: var(--color-ink);
138 |     letter-spacing: -0.5px;
139 |     font-family: var(--font-body);
140 | }
141 | 
142 | .nav-links { display: flex; gap: var(--spacing-xs); }
143 | 
144 | .nav-link {
145 |     text-decoration: none;
146 |     color: var(--color-muted);
147 |     font-weight: 500;
148 |     font-size: 14px;
149 |     padding: var(--spacing-sm) var(--spacing-md);
150 |     border-radius: var(--rounded-md);
151 |     transition: all 150ms ease-in-out;
152 | }
153 | .nav-link:hover { color: var(--color-ink); background-color: var(--color-surface-soft); }
154 | .nav-link.active { color: var(--color-ink); background-color: var(--color-surface-card); }
155 | 
156 | /* ===================================
157 |    Main Content Layout
158 |    =================================== */
159 | .main-content {
160 |     padding: var(--spacing-section) var(--spacing-lg);
161 |     min-height: calc(100vh - 64px);
162 | }
163 | 
164 | .container { max-width: 1200px; margin: 0 auto; }
165 | 
166 | .page-header { margin-bottom: var(--spacing-xxl); }
167 | .page-header h2 { margin-bottom: var(--spacing-sm); }
168 | .subtitle { font-size: 18px; color: var(--color-muted); font-weight: 400; }
169 | 
170 | /* ===================================
171 |    Grid Layout
172 |    =================================== */
173 | .content-grid {
174 |     display: grid;
175 |     grid-template-columns: 1fr;
176 |     gap: var(--spacing-xl);
177 | }
178 | 
179 | @media (min-width: 1024px) {
180 |     .content-grid { grid-template-columns: 2fr 1fr; }
181 | }
182 | 
183 | /* ===================================
184 |    Card Component
185 |    =================================== */
186 | .card {
187 |     background-color: var(--color-surface-card);
188 |     border-radius: var(--rounded-lg);
189 |     padding: var(--spacing-xl);
190 |     margin-bottom: var(--spacing-xl);
191 |     border: 1px solid var(--color-hairline);
192 | }
193 | 
194 | .card-title {
195 |     font-family: var(--font-display);
196 |     font-size: 22px;
197 |     font-weight: 400;
198 |     color: var(--color-ink);
199 |     margin-bottom: var(--spacing-lg);
200 |     padding-bottom: var(--spacing-md);
201 |     border-bottom: 1px solid var(--color-hairline);
202 |     letter-spacing: -0.3px;
203 | }
204 | 
205 | /* ===================================
206 |    Buttons
207 |    =================================== */
208 | .btn {
209 |     padding: 12px 20px;
210 |     border: none;
211 |     border-radius: var(--rounded-md);
212 |     font-size: 14px;
213 |     font-weight: 500;
214 |     cursor: pointer;
215 |     transition: all 150ms ease-in-out;
216 |     font-family: var(--font-body);
217 |     height: 40px;
218 |     display: inline-flex;
219 |     align-items: center;
220 |     justify-content: center;
221 |     text-decoration: none;
222 | }
223 | 
224 | .btn-primary { background-color: var(--color-primary); color: var(--color-on-primary); }
225 | .btn-primary:hover { background-color: var(--color-primary-active); }
226 | .btn-primary:active { background-color: var(--color-primary-active); }
227 | .btn-secondary { background-color: var(--color-canvas); color: var(--color-ink); border: 1px solid var(--color-hairline); }
228 | .btn-secondary:hover { background-color: var(--color-surface-soft); }
229 | .btn-danger { background-color: var(--color-error); color: var(--color-on-primary); }
230 | .btn-danger:hover { background-color: #a93838; }
231 | 
232 | /* ===================================
233 |    Form Elements
234 |    =================================== */
235 | .form-group { margin-bottom: var(--spacing-lg); }
236 | 
237 | .form-label {
238 |     display: block;
239 |     font-weight: 500;
240 |     color: var(--color-body-strong);
241 |     margin-bottom: var(--spacing-sm);
242 |     font-size: 14px;
243 | }
244 | 
245 | .form-select {
246 |     width: 100%;
247 |     padding: 10px 14px;
248 |     border: 1px solid var(--color-hairline);
249 |     border-radius: var(--rounded-md);
250 |     font-size: 16px;
251 |     color: var(--color-ink);
252 |     background-color: var(--color-canvas);
253 |     transition: all 150ms ease-in-out;
254 |     cursor: pointer;
255 |     font-family: var(--font-body);
256 |     height: 40px;
257 | }
258 | .form-select:hover { border-color: var(--color-primary); }
259 | .form-select:focus { outline: none; border-color: var(--color-primary); box-shadow: 0 0 0 3px rgba(204, 120, 92, 0.15); }
260 | 
261 | /* ===================================
262 |    Time Slots Grid
263 |    =================================== */
264 | .time-slots-grid {
265 |     display: grid;
266 |     grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
267 |     gap: var(--spacing-md);
268 |     margin-top: var(--spacing-md);
269 | }
270 | 
271 | .time-slot-card {
272 |     background-color: var(--color-canvas);
273 |     border: 1px solid var(--color-hairline);
274 |     border-radius: var(--rounded-md);
275 |     padding: var(--spacing-md);
276 |     text-align: center;
277 |     font-weight: 500;
278 |     color: var(--color-body-strong);
279 |     cursor: pointer;
280 |     transition: all 150ms ease-in-out;
281 |     user-select: none;
282 | }
283 | .time-slot-card:hover { border-color: var(--color-primary); background-color: var(--color-surface-soft); }
284 | .time-slot-card.selected { background-color: var(--color-primary); border-color: var(--color-primary); color: var(--color-on-primary); }
285 | .placeholder-text { color: var(--color-muted); font-style: italic; text-align: center; padding: var(--spacing-xl); }
286 | 
287 | /* ===================================
288 |    Confirmation Area
289 |    =================================== */
290 | .confirmation-area {
291 |     margin-top: var(--spacing-xl);
292 |     animation: slideIn 0.3s ease-out;
293 | }
294 | 
295 | @keyframes slideIn {
296 |     from { opacity: 0; transform: translateY(-10px); }
297 |     to { opacity: 1; transform: translateY(0); }
298 | }
299 | 
300 | .confirmation-card {
301 |     background-color: var(--color-surface-dark);
302 |     border-radius: var(--rounded-lg);
303 |     padding: var(--spacing-xl);
304 |     color: var(--color-on-dark);
305 | }
306 | 
307 | .confirmation-card h4 { font-size: 22px; margin-bottom: var(--spacing-lg); font-weight: 400; color: var(--color-on-dark); }
308 | 
309 | .confirmation-details {
310 |     background-color: var(--color-surface-dark-elevated);
311 |     border-radius: var(--rounded-md);
312 |     padding: var(--spacing-lg);
313 |     margin-bottom: var(--spacing-lg);
314 | }
315 | 
316 | .detail-row { display: flex; justify-content: space-between; padding: var(--spacing-sm) 0; border-bottom: 1px solid rgba(255, 255, 255, 0.1); }
317 | .detail-row:last-child { border-bottom: none; }
318 | .detail-label { font-weight: 500; color: var(--color-on-dark-soft); font-size: 14px; }
319 | .detail-value { font-weight: 500; color: var(--color-on-dark); }
320 | 
321 | .confirmation-card .btn-primary { background-color: var(--color-canvas); color: var(--color-primary); margin-right: var(--spacing-sm); }
322 | .confirmation-card .btn-primary:hover { background-color: var(--color-surface-soft); }
323 | .confirmation-card .btn-secondary { background-color: transparent; color: var(--color-on-dark); border: 1px solid var(--color-on-dark-soft); }
324 | .confirmation-card .btn-secondary:hover { background-color: var(--color-surface-dark-elevated); }
325 | 
326 | /* ===================================
327 |    Appointments List
328 |    =================================== */
329 | .appointments-list { display: flex; flex-direction: column; gap: var(--spacing-md); }
330 | 
331 | .appointment-item {
332 |     display: flex;
333 |     align-items: center;
334 |     gap: var(--spacing-md);
335 |     padding: var(--spacing-lg);
336 |     background-color: var(--color-canvas);
337 |     border-radius: var(--rounded-md);
338 |     border-left: 3px solid var(--color-primary);
339 |     transition: all 150ms ease-in-out;
340 | }
341 | .appointment-item:hover { background-color: var(--color-surface-soft); transform: translateX(4px); }
342 | 
343 | .appointment-icon {
344 |     flex-shrink: 0;
345 |     width: 48px; height: 48px;
346 |     background-color: var(--color-primary);
347 |     color: var(--color-on-primary);
348 |     border-radius: var(--rounded-md);
349 |     display: flex; align-items: center; justify-content: center;
350 | }
351 | .appointment-details { flex: 1; }
352 | .appointment-date { font-weight: 600; color: var(--color-ink); margin-bottom: var(--spacing-xxs); }
353 | .appointment-doctor { font-size: 14px; color: var(--color-muted); }
354 | 
355 | /* ===================================
356 |    Reminders Section
357 |    =================================== */
358 | .reminders-list { display: flex; flex-direction: column; gap: var(--spacing-md); }
359 | 
360 | .reminder-item {
361 |     display: flex;
362 |     gap: var(--spacing-md);
363 |     padding: var(--spacing-lg);
364 |     background-color: var(--color-canvas);
365 |     border-radius: var(--rounded-md);
366 |     border-left: 3px solid var(--color-accent-teal);
367 |     transition: all 150ms ease-in-out;
368 | }
369 | .reminder-item:hover { background-color: var(--color-surface-soft); transform: translateX(4px); }
370 | 
371 | .reminder-icon {
372 |     flex-shrink: 0;
373 |     width: 40px; height: 40px;
374 |     background-color: var(--color-accent-teal);
375 |     color: var(--color-on-primary);
376 |     border-radius: var(--rounded-md);
377 |     display: flex; align-items: center; justify-content: center;
378 | }
379 | .medication-icon { background-color: var(--color-primary); }
380 | .reminder-content { flex: 1; }
381 | .reminder-title { font-weight: 600; color: var(--color-ink); margin-bottom: var(--spacing-xxs); }
382 | .reminder-time { font-size: 14px; color: var(--color-muted); margin-bottom: var(--spacing-xxs); }
383 | .reminder-notes { font-size: 14px; color: var(--color-muted-soft); font-style: italic; }
384 | 
385 | /* ===================================
386 |    Tasks Section
387 |    =================================== */
388 | .tasks-list { display: flex; flex-direction: column; gap: var(--spacing-md); }
389 | 
390 | .task-item {
391 |     display: flex;
392 |     gap: var(--spacing-md);
393 |     padding: var(--spacing-lg);
394 |     background-color: var(--color-canvas);
395 |     border-radius: var(--rounded-md);
396 |     border-left: 3px solid var(--color-accent-amber);
397 |     transition: all 150ms ease-in-out;
398 | }
399 | .task-item:hover { background-color: var(--color-surface-soft); transform: translateX(4px); }
400 | 
401 | .task-icon {
402 |     flex-shrink: 0;
403 |     width: 40px; height: 40px;
404 |     background-color: var(--color-accent-amber);
405 |     color: var(--color-on-primary);
406 |     border-radius: var(--rounded-md);
407 |     display: flex; align-items: center; justify-content: center;
408 | }
409 | .task-content { flex: 1; }
410 | .task-title { font-weight: 600; color: var(--color-ink); margin-bottom: var(--spacing-xxs); }
411 | .task-datetime { font-size: 14px; color: var(--color-muted); margin-bottom: var(--spacing-xxs); }
412 | .task-location { font-size: 14px; color: var(--color-muted-soft); }
413 | 
414 | /* ===================================
415 |    Modal
416 |    =================================== */
417 | .modal {
418 |     display: none;
419 |     position: fixed;
420 |     top: 0; left: 0;
421 |     width: 100%; height: 100%;
422 |     background-color: rgba(20, 20, 19, 0.6);
423 |     z-index: 2000;
424 |     align-items: center;
425 |     justify-content: center;
426 |     backdrop-filter: blur(4px);
427 |     animation: fadeIn 0.3s ease-out;
428 | }
429 | 
430 | @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
431 | 
432 | .modal-content {
433 |     background-color: var(--color-canvas);
434 |     border-radius: var(--rounded-xl);
435 |     padding: var(--spacing-xxl);
436 |     max-width: 500px;
437 |     width: 90%;
438 |     box-shadow: 0 20px 25px -5px rgba(20, 20, 19, 0.2);
439 |     text-align: center;
440 |     animation: scaleIn 0.3s ease-out;
441 | }
442 | 
443 | @keyframes scaleIn { from { transform: scale(0.9); opacity: 0; } to { transform: scale(1); opacity: 1; } }
444 | 
445 | .modal-icon {
446 |     width: 80px; height: 80px;
447 |     margin: 0 auto var(--spacing-lg);
448 |     border-radius: var(--rounded-full);
449 |     display: flex; align-items: center; justify-content: center;
450 | }
451 | .success-icon { background-color: rgba(93, 184, 114, 0.15); color: var(--color-success); }
452 | .error-icon { background-color: rgba(198, 69, 69, 0.15); color: var(--color-error); }
453 | .modal-content h3 { font-size: 28px; color: var(--color-ink); margin-bottom: var(--spacing-md); }
454 | .modal-content p { color: var(--color-muted); margin-bottom: var(--spacing-xl); line-height: 1.6; }
455 | .modal-content .btn { width: 100%; }
456 | .modal-actions { display: flex; gap: var(--spacing-md); margin-top: var(--spacing-lg); }
457 | .modal-actions .btn { flex: 1; margin: 0; }
458 | 
459 | /* ===================================
460 |    Appointments Page Styles
461 |    =================================== */
462 | .appointments-section { max-width: 1200px; margin: 0 auto; }
463 | 
464 | .appointments-grid {
465 |     display: grid;
466 |     grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
467 |     gap: var(--spacing-xl);
468 | }
469 | 
470 | .appointment-card { background-color: var(--color-surface-card); border: 1px solid var(--color-hairline); transition: all 150ms ease-in-out; }
471 | .appointment-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-subtle); }
472 | 
473 | .appointment-card-header {
474 |     display: flex;
475 |     align-items: center;
476 |     gap: var(--spacing-lg);
477 |     padding-bottom: var(--spacing-lg);
478 |     border-bottom: 1px solid var(--color-hairline);
479 |     margin-bottom: var(--spacing-lg);
480 | }
481 | .appointment-card-info { flex: 1; }
482 | .appointment-card .appointment-date { font-size: 20px; font-weight: 600; color: var(--color-ink); margin-bottom: var(--spacing-xs); }
483 | .appointment-card .appointment-time { font-size: 16px; font-weight: 500; color: var(--color-primary); }
484 | .appointment-card-body { margin-bottom: var(--spacing-lg); }
485 | .appointment-card-body .detail-row { display: flex; justify-content: space-between; padding: var(--spacing-sm) 0; border-bottom: 1px solid var(--color-hairline-soft); color: var(--color-body); }
486 | .appointment-card-body .detail-row:last-child { border-bottom: none; }
487 | .appointment-card-body .detail-label { font-weight: 500; color: var(--color-muted); font-size: 14px; }
488 | .appointment-card-body .detail-value { font-weight: 500; color: var(--color-ink); text-align: right; }
489 | .appointment-card-footer { padding-top: var(--spacing-lg); border-top: 1px solid var(--color-hairline); }
490 | .appointment-card-footer .btn { width: 100%; }
491 | 
492 | .empty-state {
493 |     text-align: center;
494 |     padding: var(--spacing-xxl) var(--spacing-xl);
495 |     max-width: 600px;
496 |     margin: 0 auto;
497 |     background-color: var(--color-surface-card);
498 | }
499 | .empty-state-icon {
500 |     width: 80px; height: 80px;
501 |     margin: 0 auto var(--spacing-xl);
502 |     background-color: var(--color-surface-soft);
503 |     border-radius: var(--rounded-full);
504 |     display: flex; align-items: center; justify-content: center;
505 |     color: var(--color-muted);
506 | }
507 | .empty-state h3 { font-size: 28px; color: var(--color-ink); margin-bottom: var(--spacing-md); }
508 | .empty-state p { color: var(--color-muted); margin-bottom: var(--spacing-xl); line-height: 1.6; }
509 | .empty-state .btn { display: inline-block; text-decoration: none; }
510 | 
511 | /* ===================================
512 |    Profile Page Styles
513 |    =================================== */
514 | .profile-layout { max-width: 1200px; margin: 0 auto; }
515 | .profile-header-card { margin-bottom: var(--spacing-xl); background-color: var(--color-surface-card); }
516 | 
517 | .profile-header-content { display: flex; align-items: center; gap: var(--spacing-xl); }
518 | .profile-avatar {
519 |     flex-shrink: 0;
520 |     width: 100px; height: 100px;
521 |     background-color: var(--color-primary);
522 |     border-radius: var(--rounded-full);
523 |     display: flex; align-items: center; justify-content: center;
524 |     color: var(--color-on-primary);
525 | }
526 | .profile-header-info { flex: 1; }
527 | .profile-name { font-size: 32px; font-weight: 400; color: var(--color-ink); margin-bottom: var(--spacing-sm); font-family: var(--font-display); letter-spacing: -0.5px; }
528 | .profile-meta { display: flex; gap: var(--spacing-lg); flex-wrap: wrap; }
529 | .profile-meta-item { display: flex; align-items: center; gap: var(--spacing-sm); color: var(--color-muted); font-size: 14px; font-weight: 500; }
530 | .profile-meta-item svg { color: var(--color-primary); }
531 | .profile-left-column, .profile-right-column { display: flex; flex-direction: column; gap: var(--spacing-xl); }
532 | 
533 | .info-list { display: flex; flex-direction: column; gap: var(--spacing-md); }
534 | .info-item {
535 |     display: flex; align-items: flex-start; gap: var(--spacing-md);
536 |     padding: var(--spacing-lg);
537 |     background-color: var(--color-canvas);
538 |     border-radius: var(--rounded-md);
539 |     transition: all 150ms ease-in-out;
540 | }
541 | .info-item:hover { background-color: var(--color-surface-soft); transform: translateX(4px); }
542 | .info-icon {
543 |     flex-shrink: 0;
544 |     width: 40px; height: 40px;
545 |     background-color: var(--color-primary);
546 |     color: var(--color-on-primary);
547 |     border-radius: var(--rounded-md);
548 |     display: flex; align-items: center; justify-content: center;
549 | }
550 | .info-content { flex: 1; }
551 | .info-label { font-size: 12px; font-weight: 500; color: var(--color-muted); text-transform: uppercase; letter-spacing: 1px; margin-bottom: var(--spacing-xs); }
552 | .info-value { font-size: 16px; font-weight: 500; color: var(--color-ink); }
553 | 
554 | .emergency-contact-card { border-left: 3px solid var(--color-error); background-color: var(--color-surface-card); }
555 | .emergency-contact-content { display: flex; align-items: center; gap: var(--spacing-lg); padding: var(--spacing-lg); background-color: var(--color-canvas); border-radius: var(--rounded-md); }
556 | .emergency-icon {
557 |     flex-shrink: 0; width: 60px; height: 60px;
558 |     background-color: var(--color-error); color: var(--color-on-primary);
559 |     border-radius: var(--rounded-full);
560 |     display: flex; align-items: center; justify-content: center;
561 | }
562 | .emergency-info { flex: 1; }
563 | .emergency-name { font-size: 18px; font-weight: 600; color: var(--color-ink); margin-bottom: var(--spacing-xs); }
564 | .emergency-relationship { font-size: 14px; color: var(--color-muted); margin-bottom: var(--spacing-xs); }
565 | .emergency-phone { font-size: 16px; font-weight: 500; color: var(--color-primary); }
566 | 
567 | .medical-section { margin-bottom: var(--spacing-xl); }
568 | .medical-section:last-child { margin-bottom: 0; }
569 | .medical-section-title { font-size: 16px; font-weight: 500; color: var(--color-body-strong); margin-bottom: var(--spacing-md); padding-bottom: var(--spacing-sm); border-bottom: 1px solid var(--color-hairline); }
570 | 
571 | .allergies-container { display: flex; flex-wrap: wrap; gap: var(--spacing-sm); }
572 | .tag-allergy {
573 |     display: inline-flex; align-items: center;
574 |     padding: var(--spacing-sm) var(--spacing-md);
575 |     background-color: rgba(198, 69, 69, 0.1);
576 |     color: var(--color-error);
577 |     border-radius: var(--rounded-pill);
578 |     font-size: 13px; font-weight: 500;
579 |     border: 1px solid var(--color-error);
580 |     transition: all 150ms ease-in-out;
581 | }
582 | .tag-allergy:hover { background-color: var(--color-error); color: var(--color-on-primary); transform: translateY(-2px); }
583 | 
584 | .medications-list { display: flex; flex-direction: column; gap: var(--spacing-sm); }
585 | .medication-item {
586 |     display: flex; align-items: center; gap: var(--spacing-md);
587 |     padding: var(--spacing-md);
588 |     background-color: var(--color-canvas);
589 |     border-radius: var(--rounded-md);
590 |     border-left: 3px solid var(--color-primary);
591 |     transition: all 150ms ease-in-out;
592 | }
593 | .medication-item:hover { background-color: var(--color-surface-soft); transform: translateX(4px); }
594 | .medication-icon {
595 |     flex-shrink: 0; width: 32px; height: 32px;
596 |     background-color: var(--color-primary); color: var(--color-on-primary);
597 |     border-radius: var(--rounded-sm);
598 |     display: flex; align-items: center; justify-content: center;
599 | }
600 | .medication-text { flex: 1; font-size: 14px; font-weight: 500; color: var(--color-body); }
601 | .no-data { color: var(--color-muted); font-style: italic; text-align: center; padding: var(--spacing-lg); }
602 | .edit-profile-btn { width: 100%; display: flex; align-items: center; justify-content: center; gap: var(--spacing-sm); }
603 | .edit-profile-btn svg { width: 20px; height: 20px; }
604 | 
605 | /* ===================================
606 |    Doctor Selector Panel
607 |    =================================== */
608 | .doctor-selector-panel {
609 |     margin-top: var(--spacing-xl);
610 |     margin-bottom: var(--spacing-lg);
611 |     border: 1px solid var(--color-hairline);
612 |     border-radius: var(--rounded-lg);
613 |     overflow: hidden;
614 | }
615 | .doctor-selector-header {
616 |     display: flex; align-items: baseline; justify-content: space-between;
617 |     padding: var(--spacing-md) var(--spacing-lg);
618 |     background-color: var(--color-surface-soft);
619 |     border-bottom: 1px solid var(--color-hairline);
620 | }
621 | .doctor-selector-label { font-family: var(--font-body); font-size: 14px; font-weight: 500; color: var(--color-body-strong); letter-spacing: 0.3px; }
622 | .doctor-selector-hint { font-size: 12px; color: var(--color-muted-soft); }
623 | .doctor-options-grid { display: flex; flex-direction: column; gap: 0; }
624 | .doctor-option-card {
625 |     display: flex; align-items: center; gap: var(--spacing-md);
626 |     padding: var(--spacing-md) var(--spacing-lg);
627 |     background-color: var(--color-canvas);
628 |     border-bottom: 1px solid var(--color-hairline-soft);
629 |     cursor: pointer; transition: all 150ms ease-in-out; position: relative;
630 | }
631 | .doctor-option-card:last-child { border-bottom: none; }
632 | .doctor-option-card:hover { background-color: var(--color-surface-soft); }
633 | .doctor-option-card.selected { background-color: rgba(204, 120, 92, 0.06); border-left: 3px solid var(--color-primary); }
634 | .doctor-option-avatar {
635 |     flex-shrink: 0; width: 42px; height: 42px;
636 |     border-radius: var(--rounded-full);
637 |     background-color: var(--color-primary); color: var(--color-on-primary);
638 |     display: flex; align-items: center; justify-content: center;
639 |     font-size: 13px; font-weight: 600; font-family: var(--font-body); letter-spacing: 0.5px;
640 | }
641 | .doctor-option-card.selected .doctor-option-avatar { background-color: var(--color-primary-active); }
642 | .doctor-option-info { flex: 1; min-width: 0; }
643 | .doctor-option-name { font-size: 14px; font-weight: 500; color: var(--color-ink); margin-bottom: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
644 | .doctor-option-specialty { font-size: 13px; color: var(--color-primary); font-weight: 500; }
645 | .doctor-option-exp { font-size: 12px; color: var(--color-muted-soft); margin-top: 2px; }
646 | .doctor-option-check {
647 |     flex-shrink: 0; width: 24px; height: 24px;
648 |     border-radius: var(--rounded-full);
649 |     background-color: var(--color-primary); color: var(--color-on-primary);
650 |     display: none; align-items: center; justify-content: center;
651 | }
652 | .doctor-option-card.selected .doctor-option-check { display: flex; }
653 | .doctor-empty {
654 |     padding: var(--spacing-lg) var(--spacing-xl);
655 |     font-size: 14px; color: var(--color-muted); font-style: italic;
656 |     background-color: var(--color-canvas);
657 |     display: flex; align-items: center; gap: var(--spacing-sm); flex-wrap: wrap;
658 | }
659 | .doctor-empty-link { color: var(--color-primary); text-decoration: none; font-style: normal; font-weight: 500; white-space: nowrap; }
660 | .doctor-empty-link:hover { color: var(--color-primary-active); text-decoration: underline; }
661 | 
662 | /* ===================================
663 |    Login Page
664 |    =================================== */
665 | .login-body { min-height: 100vh; display: flex; align-items: center; justify-content: center; background-color: var(--color-canvas); padding: var(--spacing-xl); }
666 | .login-wrapper { width: 100%; max-width: 460px; display: flex; flex-direction: column; align-items: center; gap: var(--spacing-lg); }
667 | .login-brand { display: flex; align-items: center; gap: var(--spacing-md); }
668 | .login-brand-name { font-family: var(--font-body); font-size: 26px; font-weight: 500; color: var(--color-ink); letter-spacing: -0.5px; }
669 | .login-tagline { font-size: 15px; color: var(--color-muted); margin-top: calc(-1 * var(--spacing-sm)); text-align: center; }
670 | .login-card { width: 100%; background-color: var(--color-surface-card); border: 1px solid var(--color-hairline); border-radius: var(--rounded-xl); padding: var(--spacing-xxl); }
671 | .login-card-header { text-align: center; margin-bottom: var(--spacing-xl); }
672 | .login-card-title { font-family: var(--font-display); font-size: 28px; font-weight: 400; color: var(--color-ink); margin-bottom: var(--spacing-xs); letter-spacing: -0.3px; }
673 | .login-card-subtitle { font-size: 15px; color: var(--color-muted); }
674 | .login-options { display: flex; flex-direction: column; gap: 0; }
675 | .login-option-btn { display: flex; align-items: center; gap: var(--spacing-md); width: 100%; padding: var(--spacing-lg) var(--spacing-xl); background-color: var(--color-canvas); border: 1px solid var(--color-hairline); border-radius: var(--rounded-lg); cursor: pointer; transition: all 150ms ease-in-out; text-align: left; font-family: var(--font-body); margin-bottom: 0; }
676 | .login-option-btn:hover { border-color: var(--color-primary); background-color: var(--color-surface-soft); transform: translateY(-2px); box-shadow: 0 4px 12px rgba(204, 120, 92, 0.12); }
677 | .login-option-btn:active { transform: translateY(0); }
678 | .login-option-icon { flex-shrink: 0; width: 52px; height: 52px; border-radius: var(--rounded-md); display: flex; align-items: center; justify-content: center; transition: all 150ms ease-in-out; }
679 | .login-option-doctor .login-option-icon { background-color: rgba(204, 120, 92, 0.12); color: var(--color-primary); }
680 | .login-option-doctor:hover .login-option-icon { background-color: var(--color-primary); color: var(--color-on-primary); }
681 | .login-option-patient .login-option-icon { background-color: rgba(93, 184, 166, 0.12); color: var(--color-accent-teal); }
682 | .login-option-patient:hover .login-option-icon { background-color: var(--color-accent-teal); color: var(--color-on-primary); }
683 | .login-option-text { flex: 1; display: flex; flex-direction: column; gap: 3px; }
684 | .login-option-title { font-size: 16px; font-weight: 500; color: var(--color-ink); }
685 | .login-option-desc { font-size: 13px; color: var(--color-muted); }
686 | .login-option-arrow { flex-shrink: 0; color: var(--color-muted-soft); transition: all 150ms ease-in-out; }
687 | .login-option-btn:hover .login-option-arrow { color: var(--color-primary); transform: translateX(3px); }
688 | .login-divider { display: flex; align-items: center; gap: var(--spacing-md); margin: var(--spacing-md) 0; color: var(--color-muted-soft); font-size: 13px; }
689 | .login-divider::before, .login-divider::after { content: ''; flex: 1; height: 1px; background-color: var(--color-hairline); }
690 | .login-disclaimer { margin-top: var(--spacing-xl); font-size: 12px; color: var(--color-muted-soft); text-align: center; font-style: italic; padding-top: var(--spacing-lg); border-top: 1px solid var(--color-hairline-soft); }
691 | .login-footer { font-size: 12px; color: var(--color-muted-soft); text-align: center; }
692 | 
693 | /* ===================================
694 |    Patient Info Page
695 |    =================================== */
696 | .patient-id-banner { display: flex; align-items: center; justify-content: space-between; background-color: var(--color-surface-dark); border-radius: var(--rounded-lg); padding: var(--spacing-md) var(--spacing-xl); margin-bottom: var(--spacing-xl); }
697 | .patient-id-label { font-size: 13px; font-weight: 500; color: var(--color-on-dark-soft); text-transform: uppercase; letter-spacing: 1px; }
698 | .patient-id-value { font-size: 22px; font-weight: 600; color: var(--color-primary); font-family: var(--font-code); letter-spacing: 1px; }
699 | .form-row { display: grid; grid-template-columns: 1fr 1fr; gap: var(--spacing-md); }
700 | .form-hint { font-size: 11px; font-weight: 400; color: var(--color-muted-soft); margin-left: var(--spacing-sm); font-style: italic; text-transform: none; letter-spacing: 0; }
701 | .form-textarea { height: 90px; resize: vertical; }
702 | .prescription-row { background-color: var(--color-canvas); border: 1px solid var(--color-hairline); border-radius: var(--rounded-md); padding: var(--spacing-lg); margin-bottom: var(--spacing-md); }
703 | .prescription-row-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: var(--spacing-md); }
704 | .prescription-row-title { font-size: 13px; font-weight: 500; color: var(--color-muted); text-transform: uppercase; letter-spacing: 1px; }
705 | .prescription-remove-btn { background: none; border: none; font-size: 12px; color: var(--color-error); cursor: pointer; font-weight: 500; padding: 4px 8px; border-radius: var(--rounded-sm); transition: all 150ms ease-in-out; }
706 | .prescription-remove-btn:hover { background-color: rgba(198, 69, 69, 0.1); }
707 | .save-feedback-success, .save-feedback-error { margin-top: var(--spacing-md); padding: var(--spacing-md) var(--spacing-lg); border-radius: var(--rounded-md); font-size: 14px; font-weight: 500; text-align: center; }
708 | .save-feedback-success { background-color: rgba(93, 184, 114, 0.12); color: var(--color-success); border: 1px solid var(--color-success); }
709 | .save-feedback-error { background-color: rgba(198, 69, 69, 0.10); color: var(--color-error); border: 1px solid var(--color-error); }
710 | .preview-header { display: flex; align-items: center; gap: var(--spacing-md); padding-bottom: var(--spacing-lg); border-bottom: 1px solid var(--color-hairline); margin-bottom: var(--spacing-lg); }
711 | .preview-avatar { flex-shrink: 0; width: 52px; height: 52px; border-radius: var(--rounded-full); background-color: var(--color-primary); color: var(--color-on-primary); display: flex; align-items: center; justify-content: center; font-size: 16px; font-weight: 600; font-family: var(--font-body); }
712 | .preview-name { font-size: 17px; font-weight: 500; color: var(--color-ink); margin-bottom: 3px; }
713 | .preview-id-tag { font-size: 12px; font-weight: 500; color: var(--color-primary); font-family: var(--font-code); letter-spacing: 0.5px; }
714 | .preview-stats { display: grid; grid-template-columns: 1fr 1fr; gap: var(--spacing-md); margin-bottom: var(--spacing-lg); }
715 | .preview-stat { background-color: var(--color-surface-soft); border-radius: var(--rounded-md); padding: var(--spacing-sm) var(--spacing-md); display: flex; flex-direction: column; gap: 3px; }
716 | .preview-stat-label { font-size: 11px; font-weight: 500; color: var(--color-muted-soft); text-transform: uppercase; letter-spacing: 1px; }
717 | .preview-stat-value { font-size: 16px; font-weight: 500; color: var(--color-ink); }
718 | .preview-section { padding: var(--spacing-sm) 0; border-bottom: 1px solid var(--color-hairline-soft); margin-bottom: var(--spacing-sm); }
719 | .preview-section:last-child { border-bottom: none; }
720 | .preview-field-label { font-size: 11px; font-weight: 500; color: var(--color-muted-soft); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
721 | .preview-field-value { font-size: 14px; color: var(--color-body); line-height: 1.5; }
722 | .preview-tags { display: flex; flex-wrap: wrap; gap: var(--spacing-xs); margin-top: 4px; }
723 | .preview-prescription-item { background-color: var(--color-surface-soft); border-left: 3px solid var(--color-primary); border-radius: var(--rounded-sm); padding: var(--spacing-sm) var(--spacing-md); margin-bottom: var(--spacing-xs); }
724 | .preview-presc-name { font-size: 13px; font-weight: 500; color: var(--color-ink); margin-bottom: 2px; }
725 | .preview-presc-meta { font-size: 12px; color: var(--color-muted); }
726 | 
727 | /* ===================================
728 |    Chatbot Styles
729 |    FIXED: These are now at the TOP LEVEL, NOT inside a media query block
730 |    =================================== */
731 | .chatbot-card {
732 |     display: flex;
733 |     flex-direction: column;
734 |     overflow: hidden;
735 |     /* Override the default card padding so inner sections control their own spacing */
736 |     padding: 0;
737 | }
738 | 
739 | .chatbot-header-section {
740 |     padding: var(--spacing-lg) var(--spacing-xl);
741 |     background: var(--color-canvas);
742 |     border-bottom: 2px solid var(--color-hairline);
743 | }
744 | 
745 | .chatbot-header-section .card-title {
746 |     margin-bottom: var(--spacing-xs);
747 |     font-size: 20px;
748 |     border-bottom: none;
749 |     padding-bottom: 0;
750 | }
751 | 
752 | .chatbot-subtitle {
753 |     font-size: 14px;
754 |     color: var(--color-muted);
755 |     margin: 0;
756 | }
757 | 
758 | .chatbot-chat-container {
759 |     background: linear-gradient(to bottom, #f9f7f4 0%, #f5f0e8 100%);
760 |     padding: var(--spacing-lg);
761 |     min-height: 350px;
762 |     max-height: 350px;
763 |     display: flex;
764 |     flex-direction: column;
765 |     position: relative;
766 | }
767 | 
768 | .chatbot-messages {
769 |     flex: 1;
770 |     overflow-y: auto;
771 |     display: flex;
772 |     flex-direction: column;
773 |     gap: var(--spacing-md);
774 |     scroll-behavior: smooth;
775 |     padding-right: var(--spacing-xs);
776 | }
777 | 
778 | .chatbot-messages::-webkit-scrollbar { width: 6px; }
779 | .chatbot-messages::-webkit-scrollbar-track { background: rgba(255,255,255,0.3); border-radius: var(--rounded-pill); }
780 | .chatbot-messages::-webkit-scrollbar-thumb { background: var(--color-muted-soft); border-radius: var(--rounded-pill); }
781 | .chatbot-messages::-webkit-scrollbar-thumb:hover { background: var(--color-muted); }
782 | 
783 | .chatbot-message {
784 |     display: flex;
785 |     gap: var(--spacing-sm);
786 |     align-items: flex-start;
787 |     animation: messageSlideIn 0.3s ease;
788 | }
789 | 
790 | @keyframes messageSlideIn {
791 |     from { opacity: 0; transform: translateY(10px); }
792 |     to { opacity: 1; transform: translateY(0); }
793 | }
794 | 
795 | .user-message { flex-direction: row-reverse; }
796 | 
797 | .message-avatar {
798 |     width: 36px; height: 36px;
799 |     border-radius: var(--rounded-full);
800 |     display: flex; align-items: center; justify-content: center;
801 |     font-size: 18px;
802 |     flex-shrink: 0;
803 |     box-shadow: 0 2px 8px rgba(0,0,0,0.1);
804 | }
805 | 
806 | .bot-avatar { background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-accent-amber) 100%); }
807 | .user-avatar { background: linear-gradient(135deg, var(--color-accent-teal) 0%, var(--color-success) 100%); }
808 | 
809 | .message-content {
810 |     background: white;
811 |     padding: var(--spacing-md) var(--spacing-lg);
812 |     border-radius: var(--rounded-lg);
813 |     max-width: 80%;
814 |     font-size: 14px;
815 |     line-height: 1.6;
816 |     color: var(--color-body);
817 |     box-shadow: 0 1px 3px rgba(0,0,0,0.08);
818 | }
819 | 
820 | .user-message .message-content { background: var(--color-primary); color: var(--color-on-primary); }
821 | .message-content p { margin: 0 0 var(--spacing-xs) 0; }
822 | .message-content p:last-child { margin-bottom: 0; }
823 | .message-content ul { margin: var(--spacing-xs) 0; padding-left: var(--spacing-lg); }
824 | .message-content li { margin: var(--spacing-xxs) 0; }
825 | .message-content strong { font-weight: 600; color: var(--color-ink); }
826 | .user-message .message-content strong { color: var(--color-on-primary); }
827 | 
828 | .chatbot-typing { padding: var(--spacing-sm) 0; display: flex; align-items: center; }
829 | 
830 | .typing-indicator {
831 |     display: flex; gap: 4px;
832 |     padding: var(--spacing-sm) var(--spacing-md);
833 |     background: white;
834 |     border-radius: var(--rounded-lg);
835 |     margin-left: 44px;
836 |     box-shadow: 0 1px 3px rgba(0,0,0,0.08);
837 | }
838 | 
839 | .typing-indicator span {
840 |     width: 8px; height: 8px;
841 |     border-radius: var(--rounded-full);
842 |     background: var(--color-muted-soft);
843 |     animation: typingBounce 1.4s infinite;
844 | }
845 | .typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
846 | .typing-indicator span:nth-child(3) { animation-delay: 0.4s; }
847 | 
848 | @keyframes typingBounce {
849 |     0%, 60%, 100% { transform: translateY(0); }
850 |     30% { transform: translateY(-6px); }
851 | }
852 | 
853 | .chatbot-quick-actions {
854 |     display: flex;
855 |     gap: var(--spacing-xs);
856 |     padding: var(--spacing-md) var(--spacing-lg);
857 |     background: var(--color-canvas);
858 |     border-top: 1px solid var(--color-hairline);
859 |     flex-wrap: wrap;
860 | }
861 | 
862 | .quick-action-btn {
863 |     background: white;
864 |     border: 1px solid var(--color-hairline);
865 |     color: var(--color-body);
866 |     padding: var(--spacing-xs) var(--spacing-md);
867 |     border-radius: var(--rounded-pill);
868 |     font-size: 13px; font-weight: 500;
869 |     cursor: pointer; transition: all 0.2s ease;
870 |     white-space: nowrap;
871 |     font-family: var(--font-body);
872 | }
873 | .quick-action-btn:hover {
874 |     background: var(--color-primary); color: var(--color-on-primary);
875 |     border-color: var(--color-primary);
876 |     transform: translateY(-1px);
877 |     box-shadow: 0 2px 8px rgba(204, 120, 92, 0.2);
878 | }
879 | 
880 | .chatbot-input-container {
881 |     display: flex; gap: var(--spacing-sm);
882 |     padding: var(--spacing-lg);
883 |     background: var(--color-canvas);
884 |     border-top: 1px solid var(--color-hairline);
885 | }
886 | 
887 | .chatbot-input {
888 |     flex: 1;
889 |     padding: var(--spacing-sm) var(--spacing-md);
890 |     border: 2px solid var(--color-hairline);
891 |     border-radius: var(--rounded-lg);
892 |     font-size: 14px;
893 |     font-family: var(--font-body);
894 |     background: white;
895 |     color: var(--color-body);
896 |     transition: all 0.2s ease;
897 | }
898 | .chatbot-input:focus { outline: none; border-color: var(--color-primary); box-shadow: 0 0 0 3px rgba(204, 120, 92, 0.1); }
899 | .chatbot-input::placeholder { color: var(--color-muted-soft); }
900 | 
901 | .chatbot-send-btn {
902 |     background: var(--color-primary);
903 |     border: none; color: var(--color-on-primary);
904 |     width: 44px; height: 44px;
905 |     border-radius: var(--rounded-lg);
906 |     cursor: pointer;
907 |     display: flex; align-items: center; justify-content: center;
908 |     transition: all 0.2s ease; flex-shrink: 0;
909 |     box-shadow: 0 2px 8px rgba(204, 120, 92, 0.3);
910 | }
911 | .chatbot-send-btn:hover { background: var(--color-primary-active); transform: translateY(-2px); box-shadow: 0 4px 12px rgba(204, 120, 92, 0.4); }
912 | .chatbot-send-btn:active { transform: translateY(0); }
913 | 
914 | /* ===================================
915 |    Accessibility
916 |    =================================== */
917 | .btn:focus, .form-select:focus, .time-slot-card:focus { outline: 2px solid var(--color-primary); outline-offset: 2px; }
918 | .nav-link:focus { outline: 2px solid var(--color-primary); outline-offset: 2px; }
919 | 
920 | /* ===================================
921 |    Responsive Design
922 |    =================================== */
923 | @media (max-width: 768px) {
924 |     h1 { font-size: 32px; }
925 |     h2 { font-size: 28px; }
926 |     h3 { font-size: 22px; }
927 | 
928 |     .navbar .container { flex-direction: column; gap: var(--spacing-md); height: auto; padding: var(--spacing-md); }
929 |     .nav-links { width: 100%; justify-content: center; }
930 |     .main-content { padding: var(--spacing-xxl) var(--spacing-md); }
931 |     .card { padding: var(--spacing-lg); }
932 |     .time-slots-grid { grid-template-columns: repeat(2, 1fr); }
933 |     .confirmation-card { padding: var(--spacing-lg); }
934 |     .btn { width: 100%; margin-bottom: var(--spacing-sm); }
935 |     .confirmation-card .btn-primary { margin-right: 0; }
936 |     .appointments-grid { grid-template-columns: 1fr; }
937 |     .modal-actions { flex-direction: column; }
938 |     .modal-actions .btn { width: 100%; }
939 |     .profile-header-content { flex-direction: column; text-align: center; }
940 |     .profile-meta { justify-content: center; }
941 |     .emergency-contact-content { flex-direction: column; text-align: center; }
942 |     .info-item { flex-direction: column; text-align: center; }
943 |     .form-row { grid-template-columns: 1fr; }
944 | 
945 |     /* Chatbot mobile overrides */
946 |     .chatbot-chat-container { min-height: 300px; max-height: 300px; }
947 |     .message-content { max-width: 85%; }
948 |     .chatbot-quick-actions { flex-direction: column; }
949 |     .quick-action-btn { width: 100%; }
950 | }
951 | 
952 | /* Reduced motion */
953 | @media (prefers-reduced-motion: reduce) {
954 |     *, *::before, *::after {
955 |         animation-duration: 0.01ms !important;
956 |         animation-iteration-count: 1 !important;
957 |         transition-duration: 0.01ms !important;
958 |     }
959 | }
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
..\..\..\..\..\85,.gitignore,test_chatbot_simple.py

# VSCode Open Tabs
templates/schedule.html,templates/appointments.html,templates/profile.html,templates/assistant.html,requirements.txt,medical_chatbot.py,test_chatbot.py,SETUP_GUIDE.md,README.md,app.py,.env,chatbot/service.py,test_chatbot_simple.py,static/style.css

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T11:26:19.955Z
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

I'll analyze the schedule page and identify UI improvements while maintaining the color scheme. Let me create a todo list for this task.

<update_todo_list>
<todos>
[x] Read and analyze schedule.html and style.css
[-] Identify UI improvement opportunities
[ ] Document recommendations
[ ] Present findings to user
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
<environment_details>
# VSCode Visible Files
..\..\..\..\..\85,.gitignore,test_chatbot_simple.py

# VSCode Open Tabs
templates/schedule.html,templates/appointments.html,templates/profile.html,templates/assistant.html,requirements.txt,medical_chatbot.py,test_chatbot.py,SETUP_GUIDE.md,README.md,app.py,.env,chatbot/service.py,test_chatbot_simple.py,static/style.css

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T11:26:28.345Z
User time zone: Asia/Kuala_Lumpur, UTC+8:00

# Current Cost
$0.09

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Read and analyze schedule.html and style.css | Completed |
| 2 | Identify UI improvement opportunities | In Progress |
| 3 | Document recommendations | Pending |
| 4 | Present findings to user | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<attempt_completion>
<result>
After analyzing the schedule page, here are UI improvements that maintain the current color scheme:

## **Layout & Spacing Improvements**

1. **Page Header Enhancement**
   - Add subtle icon next to "Schedule Follow-Up Appointment" heading
   - Increase spacing between title and subtitle for better hierarchy
   - Add a decorative underline or accent bar using existing primary color

2. **Chatbot Card Improvements**
   - Add subtle shadow on hover for better depth perception
   - Increase border radius slightly for softer appearance
   - Add smooth transitions when expanding/collapsing
   - Improve message bubble spacing for better readability

3. **Time Slots Grid**
   - Add hover scale effect (subtle grow on hover)
   - Improve selected state with subtle pulse animation
   - Add disabled state styling for unavailable slots
   - Better visual feedback with transition effects

4. **Doctor Selector Panel**
   - Add subtle hover elevation effect on doctor cards
   - Improve avatar styling with gradient borders
   - Add smooth slide-in animation when panel appears
   - Better visual hierarchy between selected/unselected states

5. **Confirmation Card**
   - Add subtle glow effect around the card
   - Improve button spacing and alignment
   - Add icon indicators next to detail labels
   - Smooth fade-in animation when appearing

## **Typography Improvements**

6. **Better Text Hierarchy**
   - Increase font weight for section titles
   - Add letter-spacing to labels for better readability
   - Improve line-height in chatbot messages
   - Use consistent font sizes across similar elements

## **Interactive Elements**

7. **Form Elements**
   - Add focus ring animations on inputs
   - Improve dropdown arrow styling
   - Add subtle background color change on hover
   - Better disabled state visibility

8. **Quick Action Buttons**
   - Add ripple effect on click
   - Improve icon alignment
   - Better spacing between buttons
   - Add subtle shadow on hover

## **Visual Feedback**

9. **Loading States**
   - Add skeleton loaders for time slots
   - Improve typing indicator animation
   - Add progress indicators for booking process
   - Better error state messaging

10. **Micro-interactions**
    - Add smooth scroll to confirmation area
    - Improve modal entrance/exit animations
    - Add success checkmark animation
    - Better transition between states

## **Accessibility Enhancements**

11. **Visual Indicators**
    - Improve focus states with better contrast
    - Add aria-labels where missing
    - Better color contrast for muted text
    - Larger touch targets for mobile

12. **Responsive Improvements**
    - Better mobile spacing
    - Improved card stacking on small screens
    - Better chatbot height on mobile
    - Optimized button sizes for touch

All improvements maintain the warm editorial medical aesthetic with the existing color palette (primary: #cc785c, accent-teal: #5db8a6, accent-amber: #e8a55a).
</result>
</attempt_completion>

---

**User:**

[attempt_completion] Result:
The user has provided feedback on the results. Consider their input to continue the task, and then attempt completion again.
<feedback>
make it less white, theres too much making it bland
</feedback>
<environment_details>
# VSCode Visible Files
..\..\..\..\..\85,.gitignore,test_chatbot_simple.py

# VSCode Open Tabs
templates/schedule.html,templates/appointments.html,templates/profile.html,templates/assistant.html,requirements.txt,medical_chatbot.py,test_chatbot.py,SETUP_GUIDE.md,README.md,app.py,.env,chatbot/service.py,test_chatbot_simple.py,static/style.css

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T11:34:35.912Z
User time zone: Asia/Kuala_Lumpur, UTC+8:00

# Current Cost
$0.17

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Read and analyze schedule.html and style.css | Completed |
| 2 | Identify UI improvement opportunities | In Progress |
| 3 | Document recommendations | Pending |
| 4 | Present findings to user | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<update_todo_list>
<todos>
[x] Read and analyze schedule.html and style.css
[x] Identify UI improvement opportunities
[-] Apply CSS changes to reduce white and add warmth
[ ] Present final changes to user
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
<environment_details>
# VSCode Visible Files
..\..\..\..\..\85,.gitignore,test_chatbot_simple.py

# VSCode Open Tabs
templates/schedule.html,templates/appointments.html,templates/profile.html,templates/assistant.html,requirements.txt,medical_chatbot.py,test_chatbot.py,SETUP_GUIDE.md,README.md,app.py,.env,chatbot/service.py,test_chatbot_simple.py,static/style.css

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T11:34:40.804Z
User time zone: Asia/Kuala_Lumpur, UTC+8:00

# Current Cost
$0.25

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Read and analyze schedule.html and style.css | Completed |
| 2 | Identify UI improvement opportunities | Completed |
| 3 | Apply CSS changes to reduce white and add warmth | In Progress |
| 4 | Present final changes to user | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<apply_diff>
<path>static/style.css</path>
<diff>
<<<<<<< SEARCH
:start_line:264
-------
.time-slots-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: var(--spacing-md);
    margin-top: var(--spacing-md);
}

.time-slot-card {
    background-color: var(--color-canvas);
    border: 1px solid var(--color-hairline);
    border-radius: var(--rounded-md);
    padding: var(--spacing-md);
    text-align: center;
    font-weight: 500;
    color: var(--color-body-strong);
    cursor: pointer;
    transition: all 150ms ease-in-out;
    user-select: none;
}
.time-slot-card:hover { border-color: var(--color-primary); background-color: var(--color-surface-soft); }
.time-slot-card.selected { background-color: var(--color-primary); border-color: var(--color-primary); color: var(--color-on-primary); }
.placeholder-text { color: var(--color-muted); font-style: italic; text-align: center; padding: var(--spacing-xl); }
=======
.time-slots-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: var(--spacing-md);
    margin-top: var(--spacing-md);
}

.time-slot-card {
    background: linear-gradient(135deg, var(--color-surface-card) 0%, var(--color-surface-soft) 100%);
    border: 2px solid var(--color-hairline);
    border-radius: var(--rounded-md);
    padding: var(--spacing-md);
    text-align: center;
    font-weight: 500;
    color: var(--color-body-strong);
    cursor: pointer;
    transition: all 200ms ease-in-out;
    user-select: none;
    box-shadow: 0 2px 4px rgba(20, 20, 19, 0.05);
}
.time-slot-card:hover { 
    border-color: var(--color-primary); 
    background: linear-gradient(135deg, var(--color-surface-cream-strong) 0%, var(--color-surface-card) 100%);
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(204, 120, 92, 0.15);
}
.time-slot-card.selected { 
    background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-active) 100%);
    border-color: var(--color-primary-active); 
    color: var(--color-on-primary);
    box-shadow: 0 4px 12px rgba(204, 120, 92, 0.3);
}
.placeholder-text { color: var(--color-muted); font-style: italic; text-align: center; padding: var(--spacing-xl); }
>>>>>>> REPLACE
</diff>
</apply_diff>

---

**User:**

[apply_diff for 'static/style.css'] Result:
<file_write_result>
<path>static/style.css</path>
<operation>modified</operation>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
</notice>
</file_write_result>

<notice>Making multiple related changes in a single apply_diff is more efficient. If other changes are needed in this file, please include them as additional SEARCH/REPLACE blocks.</notice>
<environment_details>
# VSCode Visible Files
..\..\..\..\..\85,.gitignore,static\style.css

# VSCode Open Tabs
templates/schedule.html,templates/appointments.html,templates/profile.html,templates/assistant.html,requirements.txt,medical_chatbot.py,test_chatbot.py,SETUP_GUIDE.md,README.md,app.py,.env,chatbot/service.py,test_chatbot_simple.py,static/style.css

# Recently Modified Files
These files have been modified since you last accessed them (file was just edited so you may need to re-read it before editing):
static/style.css

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T11:34:57.327Z
User time zone: Asia/Kuala_Lumpur, UTC+8:00

# Current Cost
$0.34

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Read and analyze schedule.html and style.css | Completed |
| 2 | Identify UI improvement opportunities | Completed |
| 3 | Apply CSS changes to reduce white and add warmth | In Progress |
| 4 | Present final changes to user | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<apply_diff>
<path>static/style.css</path>
<diff>
<<<<<<< SEARCH
:start_line:328
-------
.appointments-list { display: flex; flex-direction: column; gap: var(--spacing-md); }

.appointment-item {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
    padding: var(--spacing-lg);
    background-color: var(--color-canvas);
    border-radius: var(--rounded-md);
    border-left: 3px solid var(--color-primary);
    transition: all 150ms ease-in-out;
}
.appointment-item:hover { background-color: var(--color-surface-soft); transform: translateX(4px); }
=======
.appointments-list { display: flex; flex-direction: column; gap: var(--spacing-md); }

.appointment-item {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
    padding: var(--spacing-lg);
    background: linear-gradient(135deg, var(--color-surface-card) 0%, var(--color-surface-soft) 100%);
    border-radius: var(--rounded-md);
    border-left: 4px solid var(--color-primary);
    transition: all 200ms ease-in-out;
    box-shadow: 0 2px 4px rgba(20, 20, 19, 0.06);
}
.appointment-item:hover { 
    background: linear-gradient(135deg, var(--color-surface-cream-strong) 0%, var(--color-surface-card) 100%);
    transform: translateX(6px);
    box-shadow: 0 4px 8px rgba(204, 120, 92, 0.12);
}
>>>>>>> REPLACE
<<<<<<< SEARCH
:start_line:358
-------
.reminders-list { display: flex; flex-direction: column; gap: var(--spacing-md); }

.reminder-item {
    display: flex;
    gap: var(--spacing-md);
    padding: var(--spacing-lg);
    background-color: var(--color-canvas);
    border-radius: var(--rounded-md);
    border-left: 3px solid var(--color-accent-teal);
    transition: all 150ms ease-in-out;
}
.reminder-item:hover { background-color: var(--color-surface-soft); transform: translateX(4px); }
=======
.reminders-list { display: flex; flex-direction: column; gap: var(--spacing-md); }

.reminder-item {
    display: flex;
    gap: var(--spacing-md);
    padding: var(--spacing-lg);
    background: linear-gradient(135deg, var(--color-surface-card) 0%, var(--color-surface-soft) 100%);
    border-radius: var(--rounded-md);
    border-left: 4px solid var(--color-accent-teal);
    transition: all 200ms ease-in-out;
    box-shadow: 0 2px 4px rgba(20, 20, 19, 0.06);
}
.reminder-item:hover { 
    background: linear-gradient(135deg, var(--color-surface-cream-strong) 0%, var(--color-surface-card) 100%);
    transform: translateX(6px);
    box-shadow: 0 4px 8px rgba(93, 184, 166, 0.12);
}
>>>>>>> REPLACE
<<<<<<< SEARCH
:start_line:388
-------
.tasks-list { display: flex; flex-direction: column; gap: var(--spacing-md); }

.task-item {
    display: flex;
    gap: var(--spacing-md);
    padding: var(--spacing-lg);
    background-color: var(--color-canvas);
    border-radius: var(--rounded-md);
    border-left: 3px solid var(--color-accent-amber);
    transition: all 150ms ease-in-out;
}
.task-item:hover { background-color: var(--color-surface-soft); transform: translateX(4px); }
=======
.tasks-list { display: flex; flex-direction: column; gap: var(--spacing-md); }

.task-item {
    display: flex;
    gap: var(--spacing-md);
    padding: var(--spacing-lg);
    background: linear-gradient(135deg, var(--color-surface-card) 0%, var(--color-surface-soft) 100%);
    border-radius: var(--rounded-md);
    border-left: 4px solid var(--color-accent-amber);
    transition: all 200ms ease-in-out;
    box-shadow: 0 2px 4px rgba(20, 20, 19, 0.06);
}
.task-item:hover { 
    background: linear-gradient(135deg, var(--color-surface-cream-strong) 0%, var(--color-surface-card) 100%);
    transform: translateX(6px);
    box-shadow: 0 4px 8px rgba(232, 165, 90, 0.12);
}
>>>>>>> REPLACE
<<<<<<< SEARCH
:start_line:758
-------
.chatbot-chat-container {
    background: linear-gradient(to bottom, #f9f7f4 0%, #f5f0e8 100%);
    padding: var(--spacing-lg);
    min-height: 350px;
    max-height: 350px;
    display: flex;
    flex-direction: column;
    position: relative;
}
=======
.chatbot-chat-container {
    background: linear-gradient(135deg, var(--color-surface-card) 0%, var(--color-surface-soft) 50%, var(--color-surface-cream-strong) 100%);
    padding: var(--spacing-lg);
    min-height: 350px;
    max-height: 350px;
    display: flex;
    flex-direction: column;
    position: relative;
}
>>>>>>> REPLACE
<<<<<<< SEARCH
:start_line:808
-------
.message-content {
    background: white;
    padding: var(--spacing-md) var(--spacing-lg);
    border-radius: var(--rounded-lg);
    max-width: 80%;
    font-size: 14px;
    line-height: 1.6;
    color: var(--color-body);
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}

.user-message .message-content { background: var(--color-primary); color: var(--color-on-primary); }
=======
.message-content {
    background: linear-gradient(135deg, #ffffff 0%, var(--color-canvas) 100%);
    padding: var(--spacing-md) var(--spacing-lg);
    border-radius: var(--rounded-lg);
    max-width: 80%;
    font-size: 14px;
    line-height: 1.6;
    color: var(--color-body);
    box-shadow: 0 2px 6px rgba(20, 20, 19, 0.1);
    border: 1px solid var(--color-hairline-soft);
}

.user-message .message-content { 
    background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-active) 100%);
    color: var(--color-on-primary);
    border: 1px solid var(--color-primary-active);
}
>>>>>>> REPLACE
<<<<<<< SEARCH
:start_line:830
-------
.typing-indicator {
    display: flex; gap: 4px;
    padding: var(--spacing-sm) var(--spacing-md);
    background: white;
    border-radius: var(--rounded-lg);
    margin-left: 44px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}
=======
.typing-indicator {
    display: flex; gap: 4px;
    padding: var(--spacing-sm) var(--spacing-md);
    background: linear-gradient(135deg, var(--color-canvas) 0%, var(--color-surface-soft) 100%);
    border-radius: var(--rounded-lg);
    margin-left: 44px;
    box-shadow: 0 2px 6px rgba(20, 20, 19, 0.1);
    border: 1px solid var(--color-hairline-soft);
}
>>>>>>> REPLACE
<<<<<<< SEARCH
:start_line:861
-------
.quick-action-btn {
    background: white;
    border: 1px solid var(--color-hairline);
    color: var(--color-body);
    padding: var(--spacing-xs) var(--spacing-md);
    border-radius: var(--rounded-pill);
    font-size: 13px; font-weight: 500;
    cursor: pointer; transition: all 0.2s ease;
    white-space: nowrap;
    font-family: var(--font-body);
}
.quick-action-btn:hover {
    background: var(--color-primary); color: var(--color-on-primary);
    border-color: var(--color-primary);
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(204, 120, 92, 0.2);
}
=======
.quick-action-btn {
    background: linear-gradient(135deg, var(--color-surface-card) 0%, var(--color-surface-soft) 100%);
    border: 2px solid var(--color-hairline);
    color: var(--color-body);
    padding: var(--spacing-xs) var(--spacing-md);
    border-radius: var(--rounded-pill);
    font-size: 13px; font-weight: 500;
    cursor: pointer; transition: all 0.2s ease;
    white-space: nowrap;
    font-family: var(--font-body);
    box-shadow: 0 2px 4px rgba(20, 20, 19, 0.05);
}
.quick-action-btn:hover {
    background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-active) 100%);
    color: var(--color-on-primary);
    border-color: var(--color-primary-active);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(204, 120, 92, 0.25);
}
>>>>>>> REPLACE
<<<<<<< SEARCH
:start_line:887
-------
.chatbot-input {
    flex: 1;
    padding: var(--spacing-sm) var(--spacing-md);
    border: 2px solid var(--color-hairline);
    border-radius: var(--rounded-lg);
    font-size: 14px;
    font-family: var(--font-body);
    background: white;
    color: var(--color-body);
    transition: all 0.2s ease;
}
.chatbot-input:focus { outline: none; border-color: var(--color-primary); box-shadow: 0 0 0 3px rgba(204, 120, 92, 0.1); }
=======
.chatbot-input {
    flex: 1;
    padding: var(--spacing-sm) var(--spacing-md);
    border: 2px solid var(--color-hairline);
    border-radius: var(--rounded-lg);
    font-size: 14px;
    font-family: var(--font-body);
    background: linear-gradient(135deg, #ffffff 0%, var(--color-canvas) 100%);
    color: var(--color-body);
    transition: all 0.2s ease;
}
.chatbot-input:focus { 
    outline: none; 
    border-color: var(--color-primary); 
    box-shadow: 0 0 0 4px rgba(204, 120, 92, 0.15);
    background: #ffffff;
}
>>>>>>> REPLACE
</diff>
</apply_diff>

---

**User:**

[apply_diff for 'static/style.css'] Result:
<file_write_result>
<path>static/style.css</path>
<operation>modified</operation>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
</notice>
</file_write_result>

<environment_details>
# VSCode Visible Files
..\..\..\..\..\85,.gitignore,static\style.css

# VSCode Open Tabs
templates/schedule.html,templates/appointments.html,templates/profile.html,templates/assistant.html,requirements.txt,medical_chatbot.py,test_chatbot.py,SETUP_GUIDE.md,README.md,app.py,.env,chatbot/service.py,test_chatbot_simple.py,static/style.css

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T11:35:29.443Z
User time zone: Asia/Kuala_Lumpur, UTC+8:00

# Current Cost
$0.43

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Read and analyze schedule.html and style.css | Completed |
| 2 | Identify UI improvement opportunities | Completed |
| 3 | Apply CSS changes to reduce white and add warmth | In Progress |
| 4 | Present final changes to user | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<apply_diff>
<path>static/style.css</path>
<diff>
<<<<<<< SEARCH
:start_line:623
-------
.doctor-option-card {
    display: flex; align-items: center; gap: var(--spacing-md);
    padding: var(--spacing-md) var(--spacing-lg);
    background-color: var(--color-canvas);
    border-bottom: 1px solid var(--color-hairline-soft);
    cursor: pointer; transition: all 150ms ease-in-out; position: relative;
}
.doctor-option-card:last-child { border-bottom: none; }
.doctor-option-card:hover { background-color: var(--color-surface-soft); }
.doctor-option-card.selected { background-color: rgba(204, 120, 92, 0.06); border-left: 3px solid var(--color-primary); }
=======
.doctor-option-card {
    display: flex; align-items: center; gap: var(--spacing-md);
    padding: var(--spacing-md) var(--spacing-lg);
    background: linear-gradient(135deg, var(--color-surface-card) 0%, var(--color-surface-soft) 100%);
    border-bottom: 1px solid var(--color-hairline-soft);
    cursor: pointer; transition: all 200ms ease-in-out; position: relative;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.5);
}
.doctor-option-card:last-child { border-bottom: none; }
.doctor-option-card:hover { 
    background: linear-gradient(135deg, var(--color-surface-cream-strong) 0%, var(--color-surface-card) 100%);
    transform: translateX(4px);
}
.doctor-option-card.selected { 
    background: linear-gradient(135deg, rgba(204, 120, 92, 0.12) 0%, rgba(204, 120, 92, 0.08) 100%);
    border-left: 4px solid var(--color-primary);
    box-shadow: inset 0 1px 0 rgba(204, 120, 92, 0.2);
}
>>>>>>> REPLACE
<<<<<<< SEARCH
:start_line:245
-------
.form-select {
    width: 100%;
    padding: 10px 14px;
    border: 1px solid var(--color-hairline);
    border-radius: var(--rounded-md);
    font-size: 16px;
    color: var(--color-ink);
    background-color: var(--color-canvas);
    transition: all 150ms ease-in-out;
    cursor: pointer;
    font-family: var(--font-body);
    height: 40px;
}
.form-select:hover { border-color: var(--color-primary); }
.form-select:focus { outline: none; border-color: var(--color-primary); box-shadow: 0 0 0 3px rgba(204, 120, 92, 0.15); }
=======
.form-select {
    width: 100%;
    padding: 10px 14px;
    border: 2px solid var(--color-hairline);
    border-radius: var(--rounded-md);
    font-size: 16px;
    color: var(--color-ink);
    background: linear-gradient(135deg, var(--color-surface-card) 0%, var(--color-surface-soft) 100%);
    transition: all 200ms ease-in-out;
    cursor: pointer;
    font-family: var(--font-body);
    height: 40px;
    box-shadow: 0 2px 4px rgba(20, 20, 19, 0.05);
}
.form-select:hover { 
    border-color: var(--color-primary);
    background: linear-gradient(135deg, var(--color-surface-cream-strong) 0%, var(--color-surface-card) 100%);
}
.form-select:focus { 
    outline: none; 
    border-color: var(--color-primary); 
    box-shadow: 0 0 0 4px rgba(204, 120, 92, 0.15);
    background: var(--color-canvas);
}
>>>>>>> REPLACE
<<<<<<< SEARCH
:start_line:186
-------
.card {
    background-color: var(--color-surface-card);
    border-radius: var(--rounded-lg);
    padding: var(--spacing-xl);
    margin-bottom: var(--spacing-xl);
    border: 1px solid var(--color-hairline);
}
=======
.card {
    background: linear-gradient(135deg, var(--color-surface-card) 0%, var(--color-surface-soft) 100%);
    border-radius: var(--rounded-lg);
    padding: var(--spacing-xl);
    margin-bottom: var(--spacing-xl);
    border: 1px solid var(--color-hairline);
    box-shadow: 0 2px 8px rgba(20, 20, 19, 0.06);
}
>>>>>>> REPLACE
<<<<<<< SEARCH
:start_line:343
-------
.appointment-icon {
    flex-shrink: 0;
    width: 48px; height: 48px;
    background-color: var(--color-primary);
    color: var(--color-on-primary);
    border-radius: var(--rounded-md);
    display: flex; align-items: center; justify-content: center;
}
=======
.appointment-icon {
    flex-shrink: 0;
    width: 48px; height: 48px;
    background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-active) 100%);
    color: var(--color-on-primary);
    border-radius: var(--rounded-md);
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 4px 8px rgba(204, 120, 92, 0.25);
}
>>>>>>> REPLACE
<<<<<<< SEARCH
:start_line:371
-------
.reminder-icon {
    flex-shrink: 0;
    width: 40px; height: 40px;
    background-color: var(--color-accent-teal);
    color: var(--color-on-primary);
    border-radius: var(--rounded-md);
    display: flex; align-items: center; justify-content: center;
}
.medication-icon { background-color: var(--color-primary); }
=======
.reminder-icon {
    flex-shrink: 0;
    width: 40px; height: 40px;
    background: linear-gradient(135deg, var(--color-accent-teal) 0%, #4a9d8d 100%);
    color: var(--color-on-primary);
    border-radius: var(--rounded-md);
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 3px 6px rgba(93, 184, 166, 0.25);
}
.medication-icon { 
    background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-active) 100%);
    box-shadow: 0 3px 6px rgba(204, 120, 92, 0.25);
}
>>>>>>> REPLACE
<<<<<<< SEARCH
:start_line:401
-------
.task-icon {
    flex-shrink: 0;
    width: 40px; height: 40px;
    background-color: var(--color-accent-amber);
    color: var(--color-on-primary);
    border-radius: var(--rounded-md);
    display: flex; align-items: center; justify-content: center;
}
=======
.task-icon {
    flex-shrink: 0;
    width: 40px; height: 40px;
    background: linear-gradient(135deg, var(--color-accent-amber) 0%, #d89545 100%);
    color: var(--color-on-primary);
    border-radius: var(--rounded-md);
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 3px 6px rgba(232, 165, 90, 0.25);
}
>>>>>>> REPLACE
</diff>
</apply_diff>

---

**User:**

[apply_diff for 'static/style.css'] Result:
<file_write_result>
<path>static/style.css</path>
<operation>modified</operation>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
</notice>
</file_write_result>

<environment_details>
# VSCode Visible Files
..\..\..\..\..\85,.gitignore,static\style.css

# VSCode Open Tabs
templates/schedule.html,templates/appointments.html,templates/profile.html,templates/assistant.html,requirements.txt,medical_chatbot.py,test_chatbot.py,SETUP_GUIDE.md,README.md,app.py,.env,chatbot/service.py,test_chatbot_simple.py,static/style.css

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T11:35:54.131Z
User time zone: Asia/Kuala_Lumpur, UTC+8:00

# Current Cost
$0.53

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Read and analyze schedule.html and style.css | Completed |
| 2 | Identify UI improvement opportunities | Completed |
| 3 | Apply CSS changes to reduce white and add warmth | In Progress |
| 4 | Present final changes to user | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<update_todo_list>
<todos>
[x] Read and analyze schedule.html and style.css
[x] Identify UI improvement opportunities
[x] Apply CSS changes to reduce white and add warmth
[-] Present final changes to user
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
<environment_details>
# VSCode Visible Files
..\..\..\..\..\85,.gitignore,static\style.css

# VSCode Open Tabs
templates/schedule.html,templates/appointments.html,templates/profile.html,templates/assistant.html,requirements.txt,medical_chatbot.py,test_chatbot.py,SETUP_GUIDE.md,README.md,app.py,.env,chatbot/service.py,test_chatbot_simple.py,static/style.css

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T11:35:57.149Z
User time zone: Asia/Kuala_Lumpur, UTC+8:00

# Current Cost
$0.63

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Read and analyze schedule.html and style.css | Completed |
| 2 | Identify UI improvement opportunities | Completed |
| 3 | Apply CSS changes to reduce white and add warmth | Completed |
| 4 | Present final changes to user | In Progress |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<attempt_completion>
<result>
✅ **UI Improvements Applied - Reduced White, Added Warmth**

I've transformed the schedule page from bland white to a warm, layered design while maintaining your color scheme. Here's what changed:

## **Key Visual Improvements**

### 1. **Gradient Backgrounds** (Replaced Flat White)
- **Cards**: Now use subtle gradients from `surface-card` → `surface-soft` with soft shadows
- **Time Slots**: Gradient backgrounds with enhanced hover effects (lift + shadow)
- **Chatbot Messages**: Warm gradient backgrounds instead of pure white
- **Form Inputs**: Textured gradient backgrounds for depth

### 2. **Enhanced Depth & Layering**
- Added box shadows to all interactive elements (2-8px depth)
- Gradient overlays create visual hierarchy
- Icons now have gradient fills with colored shadows
- Hover states include elevation effects (translateY/translateX)

### 3. **Warmer Interactive Elements**
- **Appointment Items**: Gradient backgrounds with 4px colored left borders
- **Reminder Items**: Teal-accented gradients with enhanced shadows
- **Task Items**: Amber-accented gradients with depth
- **Doctor Cards**: Layered gradients with inset highlights

### 4. **Chatbot Enhancements**
- Chat container: Multi-stop gradient (card → soft → cream-strong)
- Message bubbles: Subtle gradients with borders
- Quick action buttons: Textured backgrounds with shadows
- Input field: Gradient background that becomes solid on focus

### 5. **Improved Visual Feedback**
- Thicker borders (2px → 4px on accents)
- Enhanced hover states with color shifts
- Smooth 200ms transitions (up from 150ms)
- Colored shadows matching element themes

## **Color Palette Usage**
All changes use your existing warm palette:
- Primary: `#cc785c` (terracotta)
- Accent Teal: `#5db8a6`
- Accent Amber: `#e8a55a`
- Surface layers: `#efe9de` → `#f5f0e8` → `#e8e0d2`

**Result**: The page now has rich, warm textures with depth and dimension instead of flat white surfaces. Every element feels tactile and inviting while maintaining the medical professionalism.
</result>
</attempt_completion>

