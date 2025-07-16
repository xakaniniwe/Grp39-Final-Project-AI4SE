from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

# Load the trained model
model = joblib.load('student_grade_model.pkl')

# Define mentors for subjects
mentors = {
    "Maths": {"name": "Sipho Nkosi", "email": "sipho.nkosi@example.com"},
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

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # General study info
        studytime = float(request.form['studytime'])
        failures = float(request.form['failures'])
        absences = float(request.form['absences'])
        schoolsup = 1 if request.form.get('schoolsup') == 'yes' else 0
        famsup = 1 if request.form.get('famsup') == 'yes' else 0
        goout = float(request.form['goout'])

        # Predict using ML model
        features = np.array([[studytime, failures, absences, schoolsup, famsup, goout]])
        predicted_grade = model.predict(features)[0]
        percentage_grade = round((predicted_grade / 20) * 100, 1)

        # Determine CAPS Level for predicted grade
        if percentage_grade >= 80:
            level = 7
            level_description = "Outstanding Achievement"
        elif percentage_grade >= 70:
            level = 6
            level_description = "Meritorious Achievement"
        elif percentage_grade >= 60:
            level = 5
            level_description = "Substantial Achievement"
        elif percentage_grade >= 50:
            level = 4
            level_description = "Moderate Achievement"
        elif percentage_grade >= 40:
            level = 3
            level_description = "Adequate Achievement"
        elif percentage_grade >= 30:
            level = 2
            level_description = "Elementary Achievement"
        else:
            level = 1
            level_description = "Not Achieved"

        # Build general study advice
        advice_list = []
        if studytime <= 2:
            advice_list.append("Try to increase your study time to at least 3 or 4.")
        if absences > 5:
            advice_list.append("Reducing your absences can help improve your score.")
        if failures > 0:
            advice_list.append("Consider reviewing past material to avoid failures.")
        if goout >= 4:
            advice_list.append("Balancing social activities with studies might help.")
        if schoolsup == 0:
            advice_list.append("Consider asking for extra school support if available.")

        # Handle subject inputs - LEVELS
        subject_names = [
            request.form['subject1'],
            request.form['subject2'],
            request.form['subject3']
        ]
        subject_levels = [
            int(request.form['grade1']),
            int(request.form['grade2']),
            int(request.form['grade3'])
        ]

        # Subject-specific advice based on level
        for name, level_input in zip(subject_names, subject_levels):
            if level_input <= 3:
                message = f"Your level in {name} is Level {level_input}. Consider improving in this subject."
                mentor = mentors.get(name)
                if mentor:
                    message += f" Contact Mentor: {mentor['name']} (Email: {mentor['email']})."
                advice_list.append(message)
            else:
                advice_list.append(f"Good job in {name} with Level {level_input}!")

        # Overall pass/fail message
        if level >= 4:
            overall_message = "Good job! You're on track to pass."
        else:
            overall_message = "Consider more study time or extra help to improve."

        return render_template('result.html',
                               percentage=percentage_grade,
                               level=level,
                               level_description=level_description,
                               overall=overall_message,
                               advice_list=advice_list)
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
