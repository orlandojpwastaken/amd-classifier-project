import React, { useRef } from 'react';
import './ImageUploader.css';

function ImageUploader({ onImageSelect, imagePreview, onPredict, onReset, loading }) {
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // filetype validation
      if (!file.type.startsWith('image/')) {
        alert('Please select a valid image file');
        return;
      }
      // file size validation (16mb max)
      if (file.size > 16 * 1024 * 1024) {
        alert('File size must be less than 16MB');
        return;
      }
      onImageSelect(file);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      onImageSelect(file);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  return (
    <div className="image-uploader">
      {!imagePreview ? (
        <div
          className="upload-zone"
          onClick={() => fileInputRef.current.click()}
          onDrop={handleDrop}
          onDragOver={handleDragOver}
        >
          <div className="upload-icon">📁</div>
          <h3>Upload Fundus Image</h3>
          <p>Click to browse or drag and drop</p>
          <p className="file-types">Supported: JPG, PNG (Max 16MB)</p>
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            style={{ display: 'none' }}
          />
        </div>
      ) : (
        <div className="preview-section">
          <div className="image-preview">
            <img src={imagePreview} alt="Fundus preview" />
          </div>
          <div className="action-buttons">
            <button
              className="btn btn-primary"
              onClick={onPredict}
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Analyzing...
                </>
              ) : (
                '🔍 Analyze Image'
              )}
            </button>
            <button
              className="btn btn-secondary"
              onClick={onReset}
              disabled={loading}
            >
              🔄 Upload New Image
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default ImageUploader;
