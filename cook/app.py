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

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json['user_input']
    
    system_message = """
    You are a professional chef with extensive knowledge of cuisines, cooking techniques, and ingredients. Provide expert culinary advice and recipes. When giving recipes, always include:
    1. A list of ingredients with measurements
    2. Step-by-step cooking instructions
    3. Cooking time and temperature
    4. Serving suggestions
    5. Any relevant tips or variations

    Your tone should be friendly but authoritative, and you should always prioritize food safety and proper cooking techniques.
    """
    
    max_retries = 5
    base_delay = 1

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_input}
                ]
            )
            return jsonify({"response": response.choices[0].message.content})
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

    return jsonify({"error": "Failed to get a response after multiple attempts. Please try again later."}), 500

if __name__ == '__main__':
    app.run(debug=True)