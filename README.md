# English to Klingon Learning API

**API Name**: English to Klingon Learning API  
**Description**: This API facilitates learning English to Klingon translations through flashcards and quizzes. It provides multiple endpoints to interact with, including flashcards, quizzes, and mixed questions.

## Features

- **Flashcards**: Retrieve a random English to Klingon flashcard to aid in language learning.
- **Quizzes**: Access quizzes with multiple-choice questions to test your knowledge of English to Klingon translations.
- **Klingon Questions**: Get quizzes where the questions are in Klingon, and the answers are in English.
- **Mixed Questions**: Access mixed quizzes with either English or Klingon questions and corresponding options.

## Endpoints

- `/`: Provides details about the API including available endpoints and descriptions.
- `/flashcard`: Returns a random flashcard containing an English phrase and its Klingon translation.
- `/english-questions`: Returns a set of quiz questions where the prompts are in English with multiple Klingon translation options.
- `/klingon-questions`: Returns a set of quiz questions where the prompts are in Klingon with multiple English translation options.
- `/mixed-questions`: Returns a set of mixed quiz questions where the prompts could be in either English or Klingon.

## Data Source

The data used by this API is loaded from a CSV file named `English_To_Klingon.csv`, which contains English phrases and their corresponding Klingon translations. Each phrase is also categorized by difficulty based on its length.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/english-to-klingon-api.git
    cd english-to-klingon-api
    ```

2. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Add the English to Klingon data**:
   Ensure you have a `English_To_Klingon.csv` file in the root directory of the project.

4. **Run the application**:
    ```bash
    python app.py
    ```

    The API will be available at `http://127.0.0.1:5000/`.

## Usage

### Example Requests

1. **Get API Details**:
    ```bash
    curl http://127.0.0.1:5000/
    ```

2. **Get a Random Flashcard**:
    ```bash
    curl http://127.0.0.1:5000/flashcard
    ```

3. **Get English Quiz Questions**:
    ```bash
    curl http://127.0.0.1:5000/english-questions
    ```

4. **Get Klingon Quiz Questions**:
    ```bash
    curl http://127.0.0.1:5000/klingon-questions
    ```

5. **Get Mixed Quiz Questions**:
    ```bash
    curl http://127.0.0.1:5000/mixed-questions
    ```

## Technologies Used

- **Flask**: Python web framework used to create the API.
- **Pandas**: For data manipulation and loading the CSV file.
- **Flask-CORS**: To handle Cross-Origin Resource Sharing, allowing the API to be accessed from different domains.


## Acknowledgments

- **Klingon Language Community**: For their dedication to preserving and expanding the Klingon language.
- **Pandas and Flask Communities**: For providing excellent documentation and tools that make projects like this possible.

---

This README provides a comprehensive overview of your API, including installation instructions, usage examples, and a description of each endpoint. Let me know if you need any changes!
