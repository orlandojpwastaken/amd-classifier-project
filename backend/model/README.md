# AMD Classification Model

## Required Model File

**Note:** The trained model file is NOT included in this repository due to its size (94MB).

### Setup Instructions

1. Place your trained model file here:
   ```
   backend/model/best_ResNet50.pt
   ```

2. Model specifications:
   - **Architecture:** ResNet50
   - **Classes:** 3 (Early AMD, Intermediate AMD, Late AMD)
   - **Input Size:** 300x300
   - **Preprocessing:** CLAHE + Custom Normalization

### Model Details

- **File Format:** PyTorch state_dict (.pt)
- **Expected Size:** ~94MB
- **Normalization Mean:** [0.3945, 0.2407, 0.1255]
- **Normalization Std:** [0.3052, 0.1958, 0.1092]

### Verification

The application will automatically load the model on startup. Check the logs for:
```
Model loaded!
```

If the model file is missing, the application will fail to start.
