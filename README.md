# AI-powered-intervie-practice
 AI Voice Interview Coach — A full-stack web app built with Django &amp; React. Users record interview answers via microphone, speech is converted to text using Web Speech API, and Google Gemini AI scores the response on Clarity, Content, Confidence &amp; Overall with personalized feedback.
# 🎤 AI Voice Interview Coach — How to Run

## ✅ Requirements
- Python 3.10+
- Node.js 18+
- Google Chrome browser
- Google Gemini API Key (free) → https://aistudio.google.com/app/apikey

---

## 🔧 BACKEND SETUP

### 1. Open terminal inside the `backend` folder

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
pip install setuptools
```

### 3. Create the environment file
```bash
copy .env.example .env
```

Open `.env` and fill in your details:
```
SECRET_KEY=anyrandomstring123456789
DEBUG=True
GEMINI_API_KEY=paste_your_gemini_key_here
```

### 4. Setup the database
```bash
python manage.py makemigrations accounts interviews
python manage.py migrate
python manage.py seed_questions
```

### 5. Start the backend server
```bash
python manage.py runserver
```
✅ Backend running at → http://localhost:8000

---

## 🎨 FRONTEND SETUP

### 6. Open a NEW terminal inside the `frontend` folder

### 7. Install Node dependencies
```bash
npm install
```

### 8. Start the frontend
```bash
npm run dev
```
✅ Frontend running at → http://localhost:5173

---

## 🌐 OPEN THE APP

Open **Google Chrome** and go to:
```
http://localhost:5173
```

---

## 📌 IMPORTANT NOTES

- ⚠️ Use **Google Chrome** only (speech recognition not supported in other browsers)
- ⚠️ Both terminals must be running at the same time
- ⚠️ Never share your Gemini API key publicly
- ⚠️ Never upload the `.env` file to GitHub
