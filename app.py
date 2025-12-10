print("Starting import process...")
try:
    import os
    print("OS import successful")
    from flask import Flask, render_template, request, jsonify, session
    print("Flask imports successful")
    from database import initialize_db, save_booking, get_analytics
    print("Database imports successful")
    from translator import translate_text
    print("Translator import successful")
    from chatbot import process_message
    print("Chatbot import successful")
    print("All imports successful")
except Exception as e:
    print(f"Import error: {e}")

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize database on startup
initialize_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    analytics = get_analytics()
    return render_template('dashboard.html', analytics=analytics)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    
    # Limit user input to 200 characters
    user_message = user_message[:200]
    
    language = request.json.get('language', 'en')
    
    # Store session data if needed
    if 'chat_history' not in session:
        session['chat_history'] = []
    
    # Add user message to history
    session['chat_history'].append({'role': 'user', 'content': user_message})
    
    # Translate to English if not already
    if language != 'en':
        translated_message = translate_text(user_message, language, 'en')
    else:
        translated_message = user_message
    
    # Process message
    response = process_message(translated_message, session)
    
    # Limit response to 350 characters
    response = response[:350]
    
    # Translate response back if needed
    if language != 'en':
        response = translate_text(response, 'en', language)
    
    # Add bot response to history
    session['chat_history'].append({'role': 'bot', 'content': response})
    
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=False)
