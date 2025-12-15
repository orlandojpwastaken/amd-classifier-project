# Quick Start Guide

## 🚀 Running Locally

### With Docker (Recommended)
```bash
# make sure docker is running
docker-compose up --build

# access the app
# frontend: http://localhost:3000
# backend: http://localhost:5000
```

### Without Docker

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # windows
source venv/bin/activate  # mac/linux
pip install -r requirements.txt
python app.py
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

## 📋 Prerequisites

- Python 3.8+
- Node.js 18+
- Docker & Docker Compose (for containerized deployment)
- Trained model file: `backend/model/best_ResNet50.pt`

## 🔧 Configuration

Model is already configured for:
- ResNet50 architecture
- 3 AMD stages: Early, Intermediate, Late
- 300x300 input size
- CLAHE preprocessing
- Custom normalization values

## 📦 Deployment

See `WORKFLOW.md` for Azure Kubernetes deployment steps

# Build images
docker build -t amd-backend:latest ./backend
docker build -t amd-frontend:latest ./frontend

# Deploy
kubectl apply -f kubernetes/

# Check status
kubectl get all

# Get URL (if using minikube)
minikube service amd-frontend-service --url
```

## 🎓 I Don't Know Flask - Help!

### Flask Basics (5 min crash course)

Flask is super simple! Here's all you need to know:

```python
from flask import Flask
app = Flask(__name__)

# This creates an API endpoint
@app.route('/hello', methods=['GET'])
def say_hello():
    return {'message': 'Hello!'}

# Run the app
app.run()
```

**In your project:**
- `app.py` - Main file, has all API routes
- `@app.route('/api/predict')` - The prediction endpoint
- `request.files['image']` - Gets uploaded image
- `jsonify(result)` - Sends JSON response

That's it! The code has comments explaining everything else.

## 🐳 Docker Commands You'll Need

```bash
# Build images
docker build -t image-name .

# Run container
docker run -p 5000:5000 image-name

# Use docker-compose (much easier!)
docker-compose up          # Start
docker-compose down        # Stop
docker-compose logs        # View logs
```

## ☸️ Kubernetes Commands You'll Need

```bash
# Deploy everything
kubectl apply -f kubernetes/

# Check what's running
kubectl get pods
kubectl get services
kubectl get deployments

# Debug issues
kubectl logs pod-name
kubectl describe pod pod-name

# Delete everything
kubectl delete -f kubernetes/
```

## 🔍 Common Issues & Fixes

### "Model file not found"
→ Put your `.pth` file in `backend/model/`

### "ModuleNotFoundError" 
→ Run `pip install -r requirements.txt`

### "Port already in use"
→ Change port in `app.py` or kill the process

### "CORS error" in browser
→ Already handled! Check `flask-cors` in backend

### Frontend can't reach backend
→ Check `REACT_APP_API_URL` in frontend

## 📋 Workflow Summary

1. **Add model** → `backend/model/fundus_model.pth`
2. **Update code** → `backend/utils/prediction.py`
3. **Test locally** → `docker-compose up`
4. **Build images** → `docker build ...`
5. **Deploy K8s** → `kubectl apply -f kubernetes/`
6. **Access app** → Get service URL

## 💡 Pro Tips

- Start with docker-compose first (easier to debug)
- Check logs if something breaks: `docker-compose logs`
- All files have detailed comments - read them!
- Test with a sample image first
- Frontend at port 3000, backend at 5000

## 🆘 Still Stuck?

1. Read the comments in the code files
2. Check the main README.md
3. Use `docker-compose logs` to see errors
4. Make sure your model file exists and is correct

You got this! 🚀
