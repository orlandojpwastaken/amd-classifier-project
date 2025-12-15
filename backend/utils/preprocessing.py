from PIL import Image
import torch
from torchvision import transforms
import numpy as np
import cv2

def apply_clahe(image_array):
    """
    Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) during training
    Takes :
        image_array: numpy array of the image (rgb)
    Output:
        clahe-enhanced image array
    """
    # convert rgb to lab color space
    lab = cv2.cvtColor(image_array, cv2.COLOR_RGB2LAB)
    
    # split into l, a, b channels
    l, a, b = cv2.split(lab)
    
    # apply clahe to l channel
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l_clahe = clahe.apply(l)
    
    # merge channels back
    lab_clahe = cv2.merge([l_clahe, a, b])
    
    # convert back to rgb
    enhanced = cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2RGB)
    
    return enhanced


def preprocess_image(image_path, target_size=(300, 300)):
    """Preprocess fundus image exactly matching training pipeline"""
    
    try:
        # Load image
        image = Image.open(image_path).convert('RGB')
        
        # resize to 300x300
        image = image.resize(target_size, Image.BILINEAR)
        
        # apply CLAHE
        image_array = np.array(image)
        image_array = apply_clahe(image_array)
        image = Image.fromarray(image_array)
        
        # custom mean/std
        mean = [0.3945028483867645, 0.2406897395849228, 0.1255148947238922]
        std = [0.3052328824996948, 0.19580349326133728, 0.10917191952466965]
        
        # define preprocessing transform
        transform = transforms.Compose([
            transforms.ToTensor(),           # converts to tensor [0, 1] and chw format
            transforms.Normalize(mean, std)  # normalize with mean/std
        ])
        
        # apply transformations
        processed_image = transform(image)
        
        # add batch Dimension [1, c, h, w]
        processed_image = processed_image.unsqueeze(0)
        
        return processed_image
        
    except Exception as e:
        raise Exception(f"Image preprocessing failed: {str(e)}")
        
    except Exception as e:
        raise Exception(f"Image preprocessing failed: {str(e)}")


#alternative
def preprocess_from_bytes(image_bytes, target_size=(224, 224)):
    """
    Alternative preprocessing from image bytes (if needed)
    
    Args:
        image_bytes: Raw image bytes
        target_size: Target size for the image
    
    Returns:
        Preprocessed image tensor
    """
    transform = transforms.Compose([
        transforms.Resize(target_size),
        transforms.CenterCrop(target_size),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
    
    from io import BytesIO
    image = Image.open(BytesIO(image_bytes)).convert('RGB')
    processed_image = transform(image)
    processed_image = processed_image.unsqueeze(0)
    
    return processed_image
