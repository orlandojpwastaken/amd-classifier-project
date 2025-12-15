from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
from werkzeug.utils import secure_filename
from utils.preprocessing import preprocess_image
from utils.prediction import load_model, predict

# initialize flask
app = Flask(__name__)

# cors for frontend
CORS(app, resources={r"/api/*": {"origins": "*"}})

# enable debug logging
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# config
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16mb max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# load pytorch model when the app starts
model = load_model('model/best_ResNet50.pt')

def allowed_file(filename):
    """Filetype check"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for kubernetes"""
    return jsonify({'status': 'healthy'}), 200


@app.route('/api/predict', methods=['POST'])
def predict_image():
    """Main prediction endpoint"""
    logger.info("=== PREDICTION REQUEST RECEIVED ===")
    logger.info(f"Request method: {request.method}")
    logger.info(f"Request headers: {dict(request.headers)}")
    logger.info(f"Request files: {request.files}")
    
    # check if image file is in request
    if 'image' not in request.files:
        logger.error("No image file in request")
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    logger.info(f"File received: {file.filename}")
    
    # check if file is selected
    if file.filename == '':
        logger.error("Empty filename")
        return jsonify({'error': 'No file selected'}), 400
    
    # validates file type
    if not allowed_file(file.filename):
        logger.error(f"Invalid file type: {file.filename}")
        return jsonify({'error': 'Invalid file type. Allowed: png, jpg, jpeg'}), 400
    
    try:
        logger.info("Starting prediction process...")
        # save the uploaded file temporarilly
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        logger.info(f"Saving file to: {filepath}")
        file.save(filepath)
        
        # preprocess and get prediction for the image
        logger.info("Preprocessing image...")
        processed_image = preprocess_image(filepath)
        logger.info("Running model prediction...")
        result = predict(model, processed_image)
        logger.info(f"Prediction result: {result}")
        
        # clean up uploaded file
        os.remove(filepath)
        logger.info("File cleaned up successfully")
        
        # return prediction
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"PREDICTION ERROR: {str(e)}", exc_info=True)
        # clean up file if it exists
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500


@app.route('/api/model-info', methods=['GET'])
def model_info():
    """Get info on loaded model"""
    return jsonify({
        'model_loaded': model is not None,
        'classes': ['Early', 'Intermediate', 'Late'],
        'model': 'ResNet50',
        'input_size': '300x300',
        'preprocessing': 'CLAHE + Custom Normalization',
        'version': '1.0'
    }), 200


if __name__ == '__main__':
    # run flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
