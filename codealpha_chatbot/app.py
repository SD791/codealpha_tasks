from flask import Flask, render_template, request, jsonify
import nltk
from nltk.chat.util import Chat, reflections

# Download necessary NLTK packages (this only needs to be run once)
nltk.download('punkt')

# Create a simple chatbot using nltk's Chat class
pairs = [
    (r'hi|hello', ['Hello, how can I assist you today?']),
    (r'how are you?', ['I am doing great, thank you for asking!']),
    (r'(.*) your name?', ['I am a chatbot created to assist you.']),
    (r'bye', ['Goodbye! Have a great day!']),
    (r'(.*)', ['Sorry, I didn\'t understand that. Can you try again?'])
]

chatbot = Chat(pairs, reflections)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get', methods=['GET', 'POST'])
def get_bot_response():
    user_message = request.args.get('msg')  # Get the user input
    bot_response = chatbot.respond(user_message)  # Get the chatbot response
    return jsonify({'response': bot_response})  # Return the response as JSON

if __name__ == '__main__':
    app.run(debug=True)
