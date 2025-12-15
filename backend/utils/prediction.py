import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models


def load_model(model_path):
    # Loads the trained RESnNet50 model for the classification
    try:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {device}")
        
        # load architecture
        model = models.resnet50(pretrained=False)
        
        # replace final layer for 3 amd stages
        in_features = model.fc.in_features
        model.fc = nn.Linear(in_features, 3)  # 3 classes - early, intermediate, late
        
        # load the trained weights (state_dict only)
        print(f"Loading model weights from: {model_path}")
        state_dict = torch.load(model_path, map_location=device)
        model.load_state_dict(state_dict)
        
        # move model to device and set to evaluation mode
        model = model.to(device)
        model.eval()
        
        print("Model loaded!")
        return model
        
    except Exception as e:
        print(f"ERROR loading model: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def predict(model, image_tensor):
    # AMD stage labels
    label_mapping = {
        0: "Early",
        1: "Intermediate",
        2: "Late"
    }
    
    try:
        # move tensor to same device as model
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        image_tensor = image_tensor.to(device)
        
        # perform inference
        with torch.no_grad():
            outputs = model(image_tensor)
            probabilities = F.softmax(outputs, dim=1)
            confidence, predicted_class = torch.max(probabilities, 1)
            
            confidence = confidence.item()
            predicted_class = predicted_class.item()
            probabilities = probabilities[0].cpu().numpy().tolist()
        
        result = {
            'prediction': label_mapping[predicted_class],
            'amd_stage': label_mapping[predicted_class],
            'confidence': float(confidence),
            'probabilities': {
                label_mapping[i]: float(prob) 
                for i, prob in enumerate(probabilities)
            }
        }
        
        return result
        
    except Exception as e:
        raise Exception(f"Prediction error: {str(e)}")
