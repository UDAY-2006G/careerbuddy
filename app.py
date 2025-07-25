from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from groq import Groq
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Groq client
# You'll need to set your GROQ_API_KEY environment variable
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Career guidance system prompt
        system_prompt = """You are a helpful career guidance counselor for students. Your role is to:
        - Provide career advice and guidance
        - Help students explore different career paths
        - Suggest educational pathways and skill development
        - Offer insights about job markets and industry trends
        - Help with resume and interview preparation
        - Be encouraging and supportive
        
        Keep your responses concise, practical, and tailored to students. Always ask follow-up questions to better understand their interests and goals."""
        
        # Create chat completion
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            model="llama3-8b-8192",  # Using Llama 3 8B model
            temperature=0.7,
            max_tokens=1000
        )
        
        response = chat_completion.choices[0].message.content
        return jsonify({'response': response})
        
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    if not os.getenv("GROQ_API_KEY"):
        print("Warning: GROQ_API_KEY environment variable not set!")
        print("Please set your Groq API key: set GROQ_API_KEY=your_api_key_here")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
