from flask import Flask, request, jsonify
from flask_cors import CORS
from model import AnomalyDetector
import logging

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the AI Model
detector = AnomalyDetector()

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "status": "online",
        "message": "AI Pipeline Server is Running",
        "endpoints": ["/process (POST)", "/health (GET)"]
    })

@app.route('/process', methods=['POST'])
def process_data():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        logger.info(f"Received data: {data}")
        
        # Run the anomaly detection and rectification pipeline
        corrected_data, anomalies = detector.process_point(data)
        
        # Explicitly log anomalies to the terminal
        if any(anomalies.values()):
            print(f"\n[ANOMALY DETECTED] ----------------------------------------")
            print(f"Raw Data:   {data}")
            print(f"Anomalies:  {anomalies}")
            print(f"Corrected:  {corrected_data}")
            print(f"-----------------------------------------------------------\n")
        else:
            # Optional: Print a dot or small log to show it's alive
            # print(".", end="", flush=True)
            pass
        
        return jsonify({
            "original": data,
            "corrected": corrected_data,
            "anomalies": anomalies
        })
        
    except Exception as e:
        logger.error(f"Error processing data: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "model": "AnomalyDetector v1.0"})

if __name__ == '__main__':
    print("Starting AI Pipeline Server on port 8000...")
    app.run(host='0.0.0.0', port=8000, debug=True)
