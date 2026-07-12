import os
import threading
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import webview
from agent import get_agent_response

# Initialize Flask app
app = Flask(__name__, static_folder='ui')
CORS(app)

# Serve the static UI files
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# API Endpoint for chat
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_msg = data.get('message', '')
    
    if not user_msg:
        return jsonify({'error': 'No message provided'}), 400

    try:
        reply = get_agent_response(user_msg)
        return jsonify({'reply': reply})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def start_server():
    # Run flask in a separate thread so webview can run on main thread
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    # Start flask server in background
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Start Desktop Window
    webview.create_window(
        title='Thatwaat Agent AI',
        url='http://127.0.0.1:5000/',
        width=1200,
        height=800,
        resizable=True,
        frameless=False
    )
    webview.start()
