# GPT-Powered Python Quiz API

This project is a Flask-based API that generates Python multiple-choice quiz questions using OpenAI's GPT-3.5 API. The API generates questions about Python concepts, syntax, or best practices, and returns the question, options, correct answer, and an explanation in JSON format.

## Features

- Flask web framework for serving the API
- OpenAI API integration to generate quiz questions
- Environment variables for configuration
- Logging for debugging and error handling
- Exponential backoff strategy for handling OpenAI's rate limits

## Getting Started

### Prerequisites

Ensure you have the following installed on your machine:

- Python 3.10+
- `pip` for package management
- A valid OpenAI API key

### Installation

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/your-username/gpt-python-quiz-api.git
    cd gpt-python-quiz-api
    ```

2. Create a virtual environment (optional but recommended):

    ```bash
    python -m venv path/to/venv
    source path/to/venv/bin/activate  # On Windows: path\to\venv\Scripts\activate
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables by creating a `.env` file:

    ```bash
    touch .env
    ```

    Inside `.env`, add the following:

    ```bash
    OPENAI_API_KEY=your-openai-api-key
    ```

5. Run the Flask app:

    ```bash
    python app.py
    ```

6. The app will be available at `http://127.0.0.1:5000/`.

### API Endpoints

#### `GET /`

Renders the homepage (if `index.html` is present in the `templates/` directory).

#### `POST /get_question`

Generates a Python multiple-choice quiz question. The response includes a question, answer options (A, B, C, D), the correct answer, and an explanation.

**Example request:**

```bash
curl -X POST http://127.0.0.1:5000/get_question
