from flask import Flask, render_template, request, redirect, url_for, flash
import joblib
import numpy as np
import logging
import os

app = Flask(__name__)
app.secret_key = 'f2e4a871d9c6b3f7a0e1d2c3b4f56789'  # Needed for flashing messages

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load the trained model once when app starts
try:
    model = joblib.load('student_grade_model.pkl')
    app.logger.info("Model loaded successfully.")
except Exception as e:
    app.logger.error(f"Error loading model: {e}")
    model = None

# Mentors dictionary
mentors = {
    "Mathematics": {"name": "Sipho Nkosi", "email": "sipho.nkosi@gmail.com"},
    "Physical Science": {"name": "Thandi Mthembu", "email": "thandi.mthembu@example.com"},
    "Life Sciences": {"name": "Lebo Molefe", "email": "lebo.molefe@example.com"},
    "English": {"name": "John Smith", "email": "john.smith@example.com"},
    "Geography": {"name": "Nomsa Dlamini", "email": "nomsa.dlamini@example.com"},
    "History": {"name": "David Zulu", "email": "david.zulu@example.com"},
    "Business Studies": {"name": "Karabo Mokoena", "email": "karabo.mokoena@example.com"},
    "Accounting": {"name": "Zanele Khumalo", "email": "zanele.khumalo@example.com"},
    "Economics": {"name": "Sibusiso Ndlovu", "email": "sibusiso.ndlovu@example.com"},
    "Afrikaans": {"name": "Pieter van der Merwe", "email": "pieter.vdm@example.com"}
}

def map_percentage_to_level(percentage):
    if percentage >= 80:
        return 7, "Outstanding Achievement"
    elif percentage >= 70:
        return 6, "Meritorious Achievement"
    elif percentage >= 60:
        return 5, "Substantial Achievement"
    elif percentage >= 50:
        return 4, "Moderate Achievement"
    elif percentage >= 40:
        return 3, "Adequate Achievement"
    elif percentage >= 30:
        return 2, "Elementary Achievement"
    else:
        return 1, "Not Achieved"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        flash("Model is not loaded, please try again later.", "error")
        return redirect(url_for('home'))

    try:
        # Validate and parse inputs
        studytime = float(request.form['studytime'])
        failures = float(request.form['failures'])
        absences = float(request.form['absences'])
        schoolsup = 1 if request.form.get('schoolsup', 'no') == 'yes' else 0
        famsup = 1 if request.form.get('famsup', 'no') == 'yes' else 0
        goout = float(request.form['goout'])

        features = np.array([[studytime, failures, absences, schoolsup, famsup, goout]])
        predicted_grade = model.predict(features)[0]
        percentage_grade = round((predicted_grade / 20) * 100, 1)

        level, level_description = map_percentage_to_level(percentage_grade)

        advice_list = []
        # General advice rules
        if studytime <= 2:
            advice_list.append("Try to increase your study time to at least 3 or 4 hours per week.")
        if absences > 5:
            advice_list.append("Reducing your absences can help improve your score.")
        if failures > 0:
            advice_list.append("Consider reviewing past material to avoid failures.")
        if goout >= 4:
            advice_list.append("Balancing social activities with studies might help.")
        if schoolsup == 0:
            advice_list.append("Consider asking for extra school support if available.")

        # Handle subject-specific CAPS levels
        subject_names = [
            request.form['subject1'],
            request.form['subject2'],
            request.form['subject3'],
            request.form['subject4']
        ]
        subject_levels = [
            int(request.form['grade1']),
            int(request.form['grade2']),
            int(request.form['grade3']),
            int(request.form['grade4']) 
        ]

        for subject, level_input in zip(subject_names, subject_levels):
            if level_input <= 3:
                msg = f"Your level in {subject} is Level {level_input}. Consider improving in this subject."
                mentor = mentors.get(subject)
                if mentor:
                    msg += f" Contact Mentor: {mentor['name']} (Email: {mentor['email']})."
                advice_list.append(msg)
            else:
                advice_list.append(f"Good job in {subject} with Level {level_input}!")

        overall_message = "Good job! You're on track to pass." if level >= 4 else "Consider more study time or extra help to improve."

        # Log prediction
        app.logger.info(f"Prediction done: Grade={predicted_grade:.2f}, Percentage={percentage_grade}%, Level={level}")

        return render_template(
            'result.html',
            percentage=percentage_grade,
            level=level,
            level_description=level_description,
            overall=overall_message,
            advice_list=advice_list
        )
    except Exception as e:
        app.logger.error(f"Error during prediction: {e}")
        flash("An error occurred while processing your request. Please check your inputs and try again.", "error")
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))