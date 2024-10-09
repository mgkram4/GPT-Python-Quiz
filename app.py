import logging
import os
import random
import time

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from openai import OpenAI

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize the OpenAI client with the API key from environment variable
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_question', methods=['POST'])
def get_question():
    system_message = """
    You are a Python programming expert creating quiz questions. Generate a multiple-choice question about Python concepts, syntax, or best practices. 
    The questions should be text-only, without any code snippets or examples.
    Format your response exactly as follows:
    Question: [question text]
    A) [option A]
    B) [option B]
    C) [option C]
    D) [option D]
    Correct Answer: [A, B, C, or D]
    Explanation: [brief explanation of the correct answer]
    """

    max_retries = 5
    base_delay = 1

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": "Generate a text-only Python quiz question."}
                ]
            )
            question_data = parse_question(response.choices[0].message.content)
            return jsonify(question_data)
        except OpenAI.RateLimitError as e:
            if attempt == max_retries - 1:
                logger.error(f"Rate limit error after {max_retries} attempts: {str(e)}")
                return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429
            delay = (2 ** attempt) * base_delay + random.uniform(0, 0.1 * (2 ** attempt))
            logger.warning(f"Rate limit hit. Retrying in {delay:.2f} seconds...")
            time.sleep(delay)
        except Exception as e:
            logger.error(f"Error in API call: {str(e)}", exc_info=True)
            logger.error(f"Error type: {type(e)}")
            logger.error(f"Error details: {e.__dict__}")
            return jsonify({"error": "An error occurred while processing your request. Please check the server logs for more details."}), 500

    return jsonify({"error": "Failed to get a question after multiple attempts. Please try again later."}), 500

def parse_question(raw_question):
    lines = raw_question.strip().split('\n')
    question = lines[0].replace('Question: ', '')
    options = {
        'A': lines[1].replace('A) ', ''),
        'B': lines[2].replace('B) ', ''),
        'C': lines[3].replace('C) ', ''),
        'D': lines[4].replace('D) ', '')
    }
    correct_answer = lines[5].replace('Correct Answer: ', '')
    explanation = lines[6].replace('Explanation: ', '')
    return {
        'question': question,
        'options': options,
        'correct_answer': correct_answer,
        'explanation': explanation
    }

if __name__ == '__main__':
    app.run(debug=True)