from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from joblib import load

app = Flask(__name__)

# Load trained models
model_stars_rating = load('models/model_stars_rating.joblib')
model_overall_score = load('models/model_overall_score.joblib')

# Define your preprocessing and prediction logic
all_features = ['theme', 'formateur', 'knowledge', 'professionalism', 'communication',
                'relevence', 'structure', 'duration', 'clarity', 'environment', 'typef']
categorical_features = ['theme', 'formateur']
numerical_features = [feature for feature in all_features if feature not in categorical_features]
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
        ('num', 'passthrough', numerical_features)
    ])

# Function to predict stars_rating and overall_score
def predict_scores(formateur, typef, duration, knowledge, theme):
    # Example new data for prediction
    new_data = pd.DataFrame({
        'formateur': [formateur],
        'duration': [duration],
        'knowledge': [knowledge],
        'theme': [theme],  # Use input theme value
        'typef': [typef],  # Assuming typef is binary (0 or 1)
        'professionalism': [2.2000666888962987],  # Mean values for missing features
        'communication': [2.2147382460820273],
        'relevence': [1.9896632210736913],
        'structure': [1.991997332444148],
        'clarity': [2.0106702234078027],
        'environment': [2.2517505835278424]
    })
    # Ensure new data matches the format of training data
    new_data_all_features = new_data[all_features]
    # Predict on new data for stars_rating
    stars_rating_prediction = model_stars_rating.predict(new_data_all_features)[0]
    # Predict on new data for overall_score
    overall_score_prediction = model_overall_score.predict(new_data_all_features)[0]
    return stars_rating_prediction, overall_score_prediction
# Route for home page with form and result display
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        formateur = request.form['formateur']
        typef = int(request.form['typef'])
        duration = int(request.form['duration'])
        knowledge = int(request.form['knowledge'])
        theme = request.form['theme']  # Get theme value from form
        stars_rating_pred, overall_score_pred = predict_scores(formateur, typef, duration, knowledge, theme)
        return jsonify({
            'stars_rating': stars_rating_pred,
            'overall_score': overall_score_pred
        })
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)
