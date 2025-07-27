import os
import json
import base64
import requests
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import time
from datetime import datetime

# Load environment variables
load_dotenv()

#Ensuring the uploads directory exists, need to create Vars in AppRunner
app = Flask(__name__)
CORS(app)
 
 #why its not working in AppRunner

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# API Configuration
API_BASE_URL = "https://api.dev.runwayml.com/v1"
BEARER_TOKEN = os.getenv('RUNWAY_API_TOKEN')

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_image_to_base64_data_url(image_path):
    """Convert local image to base64 data URL"""
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    
    # Determine MIME type
    extension = image_path.split('.')[-1].lower()
    mime_types = {
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'webp': 'image/webp'
    }
    mime_type = mime_types.get(extension, 'image/jpeg')
    
    return f"data:{mime_type};base64,{encoded_string}"

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/upload-and-generate', methods=['POST'])
def upload_and_generate():
    """Handle image upload and initiate video generation"""
    try:
        # Check if file is present
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        prompt_text = request.form.get('promptText', 'Generate a creative video from this image')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            # Save the file
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Convert to base64 data URL
            image_data_url = convert_image_to_base64_data_url(filepath)
            
            # Prepare API request
            headers = {
                'Authorization': f'Bearer {BEARER_TOKEN}',
                'Content-Type': 'application/json',
                'X-Runway-Version': '2024-11-06'
            }
            
            data = {
                "promptImage": image_data_url,
                "promptText": prompt_text,
                "model": "gen4_turbo",
                "ratio": "1280:720",
                "duration": 5
            }
            
            # Make API request
            response = requests.post(
                f"{API_BASE_URL}/image_to_video",
                headers=headers,
                json=data
            )
            
            # Clean up uploaded file
            os.remove(filepath)
            
            if response.status_code == 200:
                return jsonify(response.json())
            else:
                return jsonify({
                    'error': f'API request failed with status {response.status_code}',
                    'details': response.text
                }), response.status_code
                
        else:
            return jsonify({'error': 'Invalid file type'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/check-status/<task_id>')
def check_status(task_id):
    """Check the status of a video generation task"""
    try:
        headers = {
            'Authorization': f'Bearer {BEARER_TOKEN}',
            'X-Runway-Version': '2024-11-06'
        }
        
        response = requests.get(
            f"{API_BASE_URL}/tasks/{task_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({
                'error': f'API request failed with status {response.status_code}',
                'details': response.text
            }), response.status_code
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)