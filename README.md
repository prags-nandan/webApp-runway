VNZ+ AI Image to Video Generator
A modern web application that converts images to videos using the Runway ML API. Built with Flask and a beautiful, responsive UI.
Features

🎨 Modern, dark-themed UI with gradient accents
📤 Drag-and-drop image upload
🎬 Real-time video generation status
🔄 Automatic polling for video completion
🎯 Clean, modular code architecture
🛡️ Secure file handling

tvnz-video-generator/
├── app.py                 # Main Flask application
├── templates/
│   └── index.html        # Frontend HTML template
├── uploads/              # Temporary upload directory (auto-created)
├── .env                  # Environment variables (not in repo)
├── requirements.txt      # Python dependencies
└── README.md            # This file

Setup Instructions
1. Clone the repository
bashgit clone <your-repo-url>
cd tvnz-video-generator
2. Create a virtual environment
bashpython -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
3. Install dependencies
bashpip install -r requirements.txt
4. Configure environment variables

Copy the .env.example to .env:
bashcp .env.example .env

Edit .env and add your Runway API token:
RUNWAY_API_TOKEN=your_actual_bearer_token_here


5. Create required directories
bashmkdir templates uploads
6. Run the application
bashpython app.py
The application will start on http://localhost:5000
Usage

Open the application in your web browser
Upload an image by either:

Clicking the upload area
Dragging and dropping an image


Enter a prompt describing what you want to see in the video
Click "Generate Video" to start the process
Wait for generation (usually 30-60 seconds)
Click the link to view your generated video

API Endpoints
GET /

Serves the main web interface

POST /api/upload-and-generate

Handles image upload and initiates video generation
Request: multipart/form-data with image file and prompt text
Response: JSON with task ID

GET /api/check-status/<task_id>

Checks the status of a video generation task
Response: JSON with task status and video URL when complete

Technical Details
Backend Architecture
The application uses a modular Flask structure with:

File handling: Secure file uploads with validation
API integration: Clean separation of Runway API calls
Error handling: Comprehensive error catching and user feedback
Environment configuration: Secure token management via .env

Frontend Features

Responsive design: Works on desktop and mobile
Modern UI: Glass morphism effects, gradients, and animations
Real-time updates: Polling mechanism for status updates
User feedback: Clear status messages and error handling

Security Considerations

File size limits (16MB max)
Allowed file types validation
Secure filename handling
API token stored in environment variables
Temporary file cleanup after processing

Troubleshooting
Common Issues

"No module named 'flask'"

Make sure you've activated your virtual environment
Run pip install -r requirements.txt


"API request failed"

Check your API token in .env
Ensure you have a valid Runway API subscription


"File upload failed"

Check file size (must be under 16MB)
Ensure file is a valid image format



Debug Mode
The application runs in debug mode by default. For production: