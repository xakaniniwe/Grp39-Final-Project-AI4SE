# Grp39-Final-Project-AI4SE
# 🌍 Sakha Sonke: Student Performance Predictor

**"Sakha Sonke"** means *"We Build Together"* — this AI-powered project predicts student academic performance and gives personalized, CAPS-aligned feedback and mentorship advice to help learners succeed in South Africa’s diverse school system. Live link: https://sakhasonkepred.up.railway.app

---

## 🎯 Project Overview

This web app uses machine learning to:
- Predict final grade performance based on study habits, absences, failures, and support.
- Interpret predicted performance into CAPS levels (1–7).
- Recommend improvement strategies.
- Suggest subject-specific mentors if needed.
- Support all South African schools — public and private — including technical and agricultural streams.

---

## 🌱 SDG Alignment

This project directly supports **UN Sustainable Development Goal 4: Quality Education** by:

- Providing early academic insights to learners.
- Connecting underperforming students with helpful mentorship.
- Reducing the digital divide with accessible AI tools.

---

## 🧠 How It Works

### 1. Model Training
- A Random Forest Regressor is trained on anonymized student data (`student-mat.csv`).
- Input features: `studytime`, `failures`, `absences`, `schoolsup`, `famsup`, and `goout`.
- Output: Final grade prediction (0–20 scale), converted to percentage and CAPS level.

### 2. Web Application
- **Flask** backend serves predictions.
- Users enter:
  - General study information.
  - 3 CAPS subjects and their current performance levels (1–7).
- The app returns:
  - CAPS level prediction.
  - Subject-specific feedback.
  - Contact info for mentors (email).
  - Visual progress bar and personalized advice.

---

## 🛠️ Technologies Used

- Python 3.10+
- Flask 3.1.1
- scikit-learn 1.2.2
- HTML/CSS (Dark Mode Theme)
- Jinja2 Templates
- Joblib (model saving/loading)

---

## 🗂️ Folder Structure
Grp39-Final-Project-AI4SE/
│
├── app.py
├── train_model.py
├── student_grade_model.pkl
├── requirements.txt
├── README.md
│
├── static/
│ └── css/
│ └── styles.css
| └── style.css
│ └── img/
│ └── logo.svg
│
└── templates/
├── index.html
└── result.html


---

## 🚀 How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/xakaniniwe/Grp39-Final-Project-AI4SE.git
cd Grp39-Final-Project-AI4SE

### **2. Set Up Environment**
Make sure you have Python 3.10+ installed.

pip install -r requirements.txt

### **3. Run the App**
python app.py
Visit http://127.0.0.1:5000 in your browser.

🧪 Test the Model
To re-train the model:
python train_model.py

This generates a new student_grade_model.pkl.

📦 Deploying Online
You can deploy this app to:

Render

PythonAnywhere

Heroku

Make sure to configure gunicorn or flask run in Procfile.

🙌 Team Credits
Moleboheng Madela
Veronica Moshesha
Niniwe Xaka

🧩 Acknowledgments
Dataset adapted from Kaggle open education datasets.
Inspired by the AI for Software Engineering module and UN SDG 4.
Built with love to serve South African learners.

✨ "Empowering every learner, one prediction at a time." ✨




