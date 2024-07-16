from flask import Flask, jsonify, render_template_string
import pandas as pd
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

api_info = {
    'api_name': 'English to Klingon Learning API',
    'description': 'An API for learning English to Klingon translations through flashcards and quizzes.',
    'endpoints': {
        '/': 'Returns details about the API.',
        '/flashcard': 'Returns a random English to Klingon flashcard.',
        '/quiz': 'Returns quiz data with multiple-choice questions.',
        '/klingon-question': 'Returns Klingon questions with English options.',
        '/mixed-questions': 'Returns mixed English or Klingon questions with options.'
    }
}


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
    
@app.route('/', methods=['GET'])
def api_details():
    template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ api_info['api_name'] }} - API Details</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            h1 {
                color: #333;
            }
            h2 {
                color: #555;
            }
            ul {
                list-style-type: none;
                padding: 0;
            }
            li {
                margin-bottom: 10px;
            }
        </style>
    </head>
    <body>
        <h1>{{ api_info['api_name'] }}</h1>
        <p>{{ api_info['description'] }}</p>
        <h2>Endpoints:</h2>
        <ul>
            {% for endpoint, description in api_info['endpoints'].items() %}
            <li><strong>{{ endpoint }}</strong>: {{ description }}</li>
            {% endfor %}
        </ul>
    </body>
    </html>
    """
    return render_template_string(template, api_info=api_info)

@app.route('/flashcard', methods=['GET'])
def get_random_flashcard():
    df = load_data()
    flashcards = df.to_dict(orient='records')
    random_flashcard = random.choice(flashcards)
    return jsonify(random_flashcard)

@app.route('/english-questions', methods=['GET'])
def get_quiz_data():
    df = load_data()
    questions = df.sample(4).to_dict(orient='records')
    quiz_data = []

    for question in questions:
        correct_answer = question['klingon']
        possible_decoys = df[df['klingon'] != correct_answer].sample(2)['klingon'].tolist()
        all_options = [correct_answer] + possible_decoys
        random.shuffle(all_options)
        correct_index = all_options.index(correct_answer)

        quiz_data.append({
            'question': question['english'],
            'options': all_options,
            'correct_index': correct_index
        })

    return jsonify(quiz_data)

@app.route('/klingon-questions', methods=['GET'])
def get_klingon_question():
    df = load_data()
    questions = df.sample(4)
    quiz_data = []

    for _, question in questions.iterrows():
        klingon_question = question['klingon']
        correct_answer = question['english']
        english_answers = df[df['english'] != correct_answer].sample(3)['english'].tolist()
        options = [correct_answer] + english_answers
        random.shuffle(options)
        correct_index = options.index(correct_answer)

        quiz_data.append({
            'question': klingon_question,
            'options': options,
            'correct_index': correct_index
        })

    return jsonify(quiz_data)

@app.route('/mixed-questions', methods=['GET'])
def get_mixed_questions():
    df = load_data()
    questions = df.sample(4)
    mixed_quiz_data = []

    for _, question in questions.iterrows():
        if random.choice([True, False]):
            question_text = question['english']
            correct_answer = question['klingon']
            decoys = df[df['klingon'] != correct_answer].sample(2)['klingon'].tolist()
        else:
            question_text = question['klingon']
            correct_answer = question['english']
            decoys = df[df['english'] != correct_answer].sample(2)['english'].tolist()

        options = [correct_answer] + decoys
        random.shuffle(options)
        correct_index = options.index(correct_answer)

        mixed_quiz_data.append({
            'question': question_text,
            'options': options,
            'correct_index': correct_index
        })

    return jsonify(mixed_quiz_data)
