import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib
import sklearn

# Print scikit-learn version to confirm
print(f"Using scikit-learn version: {sklearn.__version__}")

# Load dataset
df = pd.read_csv('student-mat.csv', sep=';')

# Select relevant features
features = ['studytime', 'failures', 'absences', 'schoolsup', 'famsup', 'goout', 'G3']
df = df[features]

# Encode categorical yes/no to 1/0
df['schoolsup'] = df['schoolsup'].map({'yes': 1, 'no': 0})
df['famsup'] = df['famsup'].map({'yes': 1, 'no': 0})

# Define features and target
X = df.drop('G3', axis=1)
y = df['G3']

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate model
score = model.score(X_test, y_test)
print(f"✅ Model R^2 Score on Test Set: {score:.2f}")

# Save trained model
joblib.dump(model, 'student_grade_model.pkl')
print("✅ Model saved as 'student_grade_model.pkl'")