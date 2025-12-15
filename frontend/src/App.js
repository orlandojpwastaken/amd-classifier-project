import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import ImageUploader from './components/ImageUploader';
import ResultsDisplay from './components/ResultsDisplay';

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [predictionResult, setPredictionResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // backend api
  const isLocalhost =
    typeof window !== 'undefined' &&
    (window.location.hostname === 'localhost' ||
      window.location.hostname === '127.0.0.1');

  // Prefer build-time env; fall back to local vs deployed URL
  const API_URL =
    process.env.REACT_APP_API_URL ||
    (isLocalhost ? 'http://localhost:5000' : 'http://4.145.123.52:5000');

  const handleImageSelect = (file) => {
    setSelectedImage(file);
    setError(null);
    setPredictionResult(null);
    
    // create preview
    const reader = new FileReader();
    reader.onloadend = () => {
      setImagePreview(reader.result);
    };
    reader.readAsDataURL(file);
  };

  const handlePredict = async () => {
    if (!selectedImage) {
      setError('Please select an image first');
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('image', selectedImage);

    try {
      const response = await axios.post(`${API_URL}/api/predict`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setPredictionResult(response.data);
    } catch (err) {
      setError(
        err.response?.data?.error || 
        'An error occurred during prediction. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedImage(null);
    setImagePreview(null);
    setPredictionResult(null);
    setError(null);
  };

  return (
    <div className="App">
      <div className="container">
        <header className="header">
          <h1>AMD Detection System</h1>
          <p className="subtitle">
            Age-Related Macular Degeneration Classification
          </p>
        </header>

        <div className="main-content">
          {error && (
            <div className="error-message">
              <span>⚠️</span> {error}
            </div>
          )}

          <ImageUploader
            onImageSelect={handleImageSelect}
            imagePreview={imagePreview}
            onPredict={handlePredict}
            onReset={handleReset}
            loading={loading}
          />

          {predictionResult && (
            <ResultsDisplay result={predictionResult} />
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
