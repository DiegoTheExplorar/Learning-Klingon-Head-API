from flask import Flask, jsonify
import pandas as pd
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def load_data():
    df = pd.read_csv('English_To_Klingon.csv')
    df['difficulty'] = df['english'].apply(calculate_difficulty)
    return df

def calculate_difficulty(phrase):
    length = len(phrase)
    if length <= 20:
        return 'Easy'
    elif length <= 30:
        return 'Medium'
    else:
        return 'Hard'

@app.route('/flashcard', methods=['GET'])
def get_random_flashcard():
    df = load_data()
    flashcards = df.to_dict(orient='records')
    random_flashcard = random.choice(flashcards)
    return jsonify(random_flashcard)

@app.route('/quiz', methods=['GET'])
def get_quiz_data():
    df = pd.read_csv('English_To_Klingon.csv')
    # Ensure your CSV has columns for `english`, `klingon`, and other decoy options if applicable

    # Randomly select 4 unique questions
    questions = df.sample(4).to_dict(orient='records')

    # Prepare data structure for the quiz
    quiz_data = []
    for question in questions:
        # Assuming 'klingon' is the correct answer, and there are decoys in the data
        correct_answer = question['klingon']
        possible_decoys = df[df['klingon'] != correct_answer].sample(2)['klingon'].tolist()  # Adjust number of decoys if needed

        # Combine correct answer with decoys and shuffle
        all_options = [correct_answer] + possible_decoys
        random.shuffle(all_options)

        # Find the index of the correct answer in the shuffled list
        correct_index = all_options.index(correct_answer)

        quiz_data.append({
            'question': question['english'],
            'options': all_options,
            'correct_index': correct_index
        })

    return jsonify(quiz_data)

if __name__ == '__main__':
    app.run(debug=True)
