import os
import logging
import asyncio
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# Import necessary werk24 components
from werk24 import (
    Werk24Client,
    AskMetaData,
    AskFeatures,
    AskInsights,
    TechreadMessageType
)

# --- Basic Setup ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)
CORS(app, origins="*") # Enable CORS for n8n

# --- Core Werk24 Logic ---
async def analyze_drawing(file_bytes: bytes) -> list:
    """Analyzes a drawing file with the Werk24 API and returns the results."""
    logger.info("Starting drawing analysis with Werk24.")

    # Define which data to extract
    asks = [AskMetaData(), AskFeatures(), AskInsights()]

    async with Werk24Client() as client:
        # Use a list comprehension for a more concise way to gather results
        results = [
            message.payload_dict
            async for message in client.read_drawing(drawing=file_bytes, asks=asks)
            if message.message_type == TechreadMessageType.ASK and message.payload_dict
        ]

    logger.info(f"Analysis complete. Found {len(results)} result sets.")
    return results

# --- API Endpoints ---
@app.route('/')
def index():
    """Renders a simple frontend for manual testing."""
    return render_template('index.html')

@app.route('/process-drawing', methods=['POST'])
def process_drawing_endpoint():
    """Receives a file via POST, processes it with Werk24, and returns JSON."""
    logger.info("Received request to /process-drawing.")

    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if not file or not file.filename:
        return jsonify({"error": "No file selected"}), 400

    # Read file into memory
    file_bytes = file.read()
    file_size_mb = len(file_bytes) / (1024 * 1024)
    logger.info(f"Read file '{file.filename}' ({file_size_mb:.2f} MB).")

    # Validate file type and size
    allowed_extensions = {'pdf', 'png', 'jpg', 'jpeg', 'tiff', 'tif', 'bmp'}
    file_ext = os.path.splitext(file.filename)[1].lower().lstrip('.')

    if file_ext not in allowed_extensions:
        return jsonify({"error": f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"}), 415
    if file_size_mb > 50:
        return jsonify({"error": "File exceeds 50MB limit."}), 413

    try:
        # Bridge the async Werk24 function with Flask's sync context
        analysis_results = asyncio.run(analyze_drawing(file_bytes))

        response_data = {
            "success": True,
            "filename": file.filename,
            "results_count": len(analysis_results),
            "results": analysis_results
        }
        return jsonify(response_data), 200

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        return jsonify({"success": False, "error": "An unexpected error occurred", "details": str(e)}), 500

@app.route('/health')
def health_check():
    """A simple health check endpoint."""
    return jsonify({"status": "healthy"}), 200

# --- Server Start ---
if __name__ == '__main__':
    # Check for required Werk24 credentials
    for var in ['W24TECHREAD_AUTH_REGION', 'W24TECHREAD_AUTH_TOKEN']:
        if not os.getenv(var):
            logger.warning(f"Environment variable '{var}' is not set. Werk24 API calls will fail.")

    # Use threaded=True to handle concurrent requests from n8n
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)