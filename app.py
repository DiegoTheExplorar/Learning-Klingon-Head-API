from flask import Flask, jsonify
import pandas as pd
import random
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# Function to read CSV data and add difficulty levels
def load_data():
    df = pd.read_csv('English_To_Klingon.csv')
    df['difficulty'] = df['english'].apply(calculate_difficulty)
    return df.to_dict(orient='records')

# Function to calculate difficulty based on length of the English phrase
def calculate_difficulty(phrase):
    length = len(phrase)
    if length <= 20:
        return 'Easy'
    elif length <= 30:
        return 'Medium'
    else:
        return 'Hard'

# Route to get a random flashcard
@app.route('/flashcard', methods=['GET'])
def get_random_flashcard():
    flashcards = load_data()
    random_flashcard = random.choice(flashcards)  # Select a random flashcard
    return jsonify(random_flashcard)
