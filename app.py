from flask import Flask, render_template, request, jsonify
import requests
from pymongo import MongoClient
from datetime import datetime

# Assuming you have a utility module for MongoDB interactions
from utils import mongo_module

app = Flask(__name__)

# MongoDB Setup
URI = mongo_module.mongo_creds_from_config()
client = mongo_module.create_mongo_client(URI)

db = client['personalAI']  # Assuming your DB name is 'personalAI'

# Route to render the main page (displaying user IDs and chat input form)
@app.route('/')
def index():
    # Fetch all user IDs from the database
    user_ids = mongo_module.get_user_ids(client, db, "chatHistory")  # Function to fetch user IDs from the DB
    return render_template('index.html', user_ids=user_ids)

# Route to fetch chat history for a selected user
@app.route('/get_chat_history', methods=['POST'])
def get_chat_history():
    user_id = request.form.get('user_id')

    # Fetch the last 10 chat conversations for the user from MongoDB
    chat_history = mongo_module.get_last_10_conversations(client, db, "chatHistory", user_id)

    return jsonify({'chat_history': chat_history})

@app.route('/chat', methods=['POST'])
def chat():
    user_id = request.form.get('user_id')
    
    # Check if it's a new user or an old user
    if user_id == 'new_user':
        user_id = request.form.get('new_user_id')  # Get the user_id entered by the user
    elif user_id == 'select_user':
        # For old users, just get the selected user_id
        user_id = request.form.get('user_id')
    
    prompt = request.form['prompt']
    
    # If user_id is empty, return error
    if not user_id:
        return jsonify({"error": "User ID is required!"})

    # Fetch the last 10 conversations for the selected user
    chat_history = mongo_module.get_last_10_conversations(client, db, "chatHistory", user_id)

    # Prepare the message data (chat history + new prompt)
    user_message = {
        "role": "user",
        "content": prompt,
        "timestamp": datetime.utcnow()
    }

    # Append the new user message to chat history
    chat_history.append(user_message)

    # Prepare the system message (static or dynamic based on your requirement)
    system_message = {"role": "system", "content": "You are a patient and knowledgeable teacher."}
    
    # Construct the full messages list (including system message and chat history)
    messages = [system_message] + chat_history

    # Send request to FastAPI server to generate response (replace with your actual FastAPI URL)
    FASTAPI_URL = "http://127.0.0.1:8000/generate"
    response = requests.post(FASTAPI_URL, json={
        "user_id": user_id,
        "prompt": prompt
    })

    if response.status_code == 200:
        result = response.json()
        model_response = result['response']
        model_timestamp = result['timestamp']

        # Store the new conversation (user's question and assistant's response)
        mongo_module.store_conversation(client, db, "chatHistory", user_id, chat_history, model_response, model_timestamp)

        # Return the updated chat history and model response
        return jsonify({
            'chat_history': chat_history,
            'model_response': model_response,
            'model_timestamp': model_timestamp
        })
    else:
        return jsonify({"error": "Something went wrong!"})


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)