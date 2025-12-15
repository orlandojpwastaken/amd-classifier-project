# AMD Detection System

Age-Related Macular Degeneration (AMD) classification system using deep learning deployed on Azure Kubernetes Service.

## 🎯 Overview

Full-stack web application for automated AMD stage classification from fundus images using ResNet50 deep learning model.

**Features:**
- Automated AMD stage detection (Early, Intermediate, Late)
- ResNet50 CNN architecture
- CLAHE image preprocessing
- Docker containerization
- Kubernetes orchestration
- Azure cloud deployment

## 🏗️ Architecture

```
Frontend (React) → Backend (Flask) → ML Model (PyTorch ResNet50)
       ↓                ↓                      ↓
     Nginx           Gunicorn              GPU/CPU
       ↓                ↓                      ↓
   Docker Container   Docker Container    Model Inference
       ↓________________↓______________________↓
              Azure Kubernetes Service (AKS)
```

## 📁 Project Structure

```
.
├── backend/              # Flask API server
│   ├── app.py           # main application
│   ├── utils/           # preprocessing & prediction
│   ├── model/           # model directory (add best_ResNet50.pt here)
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/            # React web interface
│   ├── src/
│   │   ├── components/  # UI components
│   │   ├── App.css
│   │   ├── App.js
│   │   ├── index.js
│   │   └── index.css
│   ├── package.json
│   └── Dockerfile
├── kubernetes/          # K8s deployment manifests
│   ├── backend-deployment.yaml
│   ├── frontend-deployment.yaml
│   └── configmap.yaml
├── docker-compose.yml   # local development
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.8+
- Node.js 18+
- Trained model file: `backend/model/best_ResNet50.pt` (NOT INCLUDED - refer to [Model Setup](#model-setup))

### Model Setup

**Important:** The trained model file is not included in this repository.

1. Place your trained ResNet50 model file in:
   ```
   backend/model/best_ResNet50.pt
   ```

2. Model specifications:
   - Architecture: ResNet50
   - Classes: 3 (Early, Intermediate, Late)
   - Input: 300x300 RGB images
   - Preprocessing: CLAHE enhancement + normalization

### Local Development

```bash
# start both services
docker-compose up --build

# access application
# frontend: http://localhost:3000
# backend: http://localhost:5000
```

### Manual Setup (Without Docker)

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python app.py
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

## 🧠 Model Details

### Architecture
- **Base Model:** ResNet50 (pretrained on ImageNet)
- **Output Classes:** 3 (Early AMD, Intermediate AMD, Late AMD)
- **Input Size:** 300×300 pixels

### Preprocessing Pipeline
1. Resize to 300×300
2. Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
3. Normalize with dataset-specific mean/std:
   - Mean: [0.3945, 0.2407, 0.1255]
   - Std: [0.3052, 0.1958, 0.1092]

### Performance
- Model Size: ~94MB

## 🛠️ Tech Stack

**Backend:**
- Flask 3.0.0
- PyTorch 2.1.0
- torchvision 0.16.0
- OpenCV (headless)
- Gunicorn

**Frontend:**
- React 18.2.0
- Axios
- Nginx

**Infrastructure:**
- Docker
- Kubernetes
- Azure AKS
- Azure Container Registry

## ☸️ Kubernetes Deployment

See `WORKFLOW.md` for complete Azure deployment instructions.

**Quick Deploy:**
```bash
# build and tag images
docker build -t amd-backend:latest ./backend
docker build -t amd-frontend:latest ./frontend

# deploy to kubernetes
kubectl apply -f kubernetes/

# check status
kubectl get pods
kubectl get services
```

## 📊 API Endpoints

### Health Check
```
GET /health
Response: {"status": "healthy"}
```

### Prediction
```
POST /api/predict
Content-Type: multipart/form-data
Body: image file

Response:
{
  "prediction": "Early",
  "amd_stage": "Early",
  "confidence": 0.87,
  "probabilities": {
    "Early": 0.87,
    "Intermediate": 0.10,
    "Late": 0.03
  }
}
```

### Model Info
```
GET /api/model-info
Response:
{
  "model_loaded": true,
  "classes": ["Early", "Intermediate", "Late"],
  "model": "ResNet50",
  "input_size": "300x300",
  "preprocessing": "CLAHE + Custom Normalization",
  "version": "1.0"
}
```

## 🧪 Testing

```bash
# test backend endpoint
curl -X POST -F "image=@test_fundus.jpg" http://localhost:5000/api/predict

# check health
curl http://localhost:5000/health
```

## 📝 Configuration

### Environment Variables

**Backend:**
- `FLASK_ENV`: development/production
- `MODEL_PATH`: path to model file (default: model/best_ResNet50.pt)

**Frontend:**
- `REACT_APP_API_URL`: backend API URL (default: http://localhost:5000)

## 🔒 Security Notes

- CORS is configured for development (allow all origins)
- For production, restrict CORS to specific domains
- Implement authentication/authorization as needed
- Validate and sanitize all file uploads

## 📚 Documentation

- `QUICKSTART.md` - Quick setup guide
- `WORKFLOW.md` - Azure deployment workflow
- Inline code comments with explanations

## Note:

This project was made for academic purposes. The results provided by this project should not directly be used as a diagnosis. Please consult a qualified optometrist for professional diagnosis and treatment recommendations.
