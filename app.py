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

@app.route('/klingon-question', methods=['GET'])
def get_klingon_question():
    df = pd.read_csv('English_To_Klingon.csv')

    klingon_question = df.sample(1)
    english_answers = df[df['klingon'] != klingon_question.iloc[0]['klingon']].sample(3)['english'].tolist()

    correct_answer = klingon_question.iloc[0]['english']


    options = [correct_answer] + english_answers
    random.shuffle(options)


    correct_index = options.index(correct_answer)

    question_data = {
        'question': klingon_question.iloc[0]['klingon'],
        'options': options,
        'correct_index': correct_index
    }
    return jsonify(question_data)

@app.route('/mixed-questions', methods=['GET'])
def get_mixed_questions():
    df = pd.read_csv('English_To_Klingon.csv')
    questions = df.sample(4)
    mixed_quiz_data = []

    for index, question in questions.iterrows():
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


if __name__ == '__main__':
    app.run(debug=True)
