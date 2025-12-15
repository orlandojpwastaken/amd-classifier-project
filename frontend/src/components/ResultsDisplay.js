import React from 'react';
import './ResultsDisplay.css';

function ResultsDisplay({ result }) {
  const { prediction, confidence, probabilities, amd_stage } = result;

  const getStatusColor = () => {
    if (amd_stage === 'Early AMD') return '#f59e0b';
    if (amd_stage === 'Intermediate AMD') return '#f97316';
    return '#dc2626';
  };

  const getSeverityLevel = () => {
    if (amd_stage === 'Early AMD') return 'Low Risk';
    if (amd_stage === 'Intermediate AMD') return 'Moderate Risk';
    return 'High Risk';
  };

  return (
    <div className="results-display">
      {/* diagnostics report header */}
      <div className="report-header">
        <h2>Diagnostic Report</h2>
        <p className="report-date">{new Date().toLocaleDateString('en-US', { 
          year: 'numeric', 
          month: 'long', 
          day: 'numeric' 
        })}</p>
      </div>

      {/* two column grid for classification and confidence report*/}
      <div className="diagnosis-grid">
        {/* classification*/}
        <div className="diagnosis-card">
          <div className="diagnosis-label">Classification</div>
          <div className="diagnosis-value" style={{ color: getStatusColor() }}>
            {prediction}
          </div>
          <div className="severity-badge" style={{ backgroundColor: getStatusColor() }}>
            {getSeverityLevel()}
          </div>
        </div>

        {/* confidence */}
        <div className="confidence-card">
          <div className="diagnosis-label">Confidence Level</div>
          <div className="confidence-circle">
            <svg viewBox="0 0 120 120">
              <circle cx="60" cy="60" r="50" className="circle-bg"/>
              <circle 
                cx="60" 
                cy="60" 
                r="50" 
                className="circle-progress"
                style={{
                  stroke: getStatusColor(),
                  strokeDasharray: `${2 * Math.PI * 50}`,
                  strokeDashoffset: `${2 * Math.PI * 50 * (1 - confidence)}`
                }}
              />
            </svg>
            <div className="confidence-value">
              <span className="percentage">{(confidence * 100).toFixed(0)}</span>
              <span className="percent-sign">%</span>
            </div>
          </div>
        </div>
      </div>

      {/* Probability FDistribution */}
      <div className="distribution-card">
        <h3>Probability Distribution</h3>
        <div className="distribution-grid">
          {Object.entries(probabilities).map(([label, prob]) => (
            <div 
              key={label} 
              className={`distribution-item ${label === prediction ? 'active' : ''}`}
            >
              <div className="distribution-header">
                <span className="distribution-name">{label}</span>
                <span className="distribution-percent">{(prob * 100).toFixed(1)}%</span>
              </div>
              <div className="distribution-bar">
                <div
                  className="distribution-fill"
                  style={{
                    width: `${prob * 100}%`,
                    backgroundColor: label === prediction ? getStatusColor() : '#cbd5e1',
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* IMPORTNATN MEDICAL NOTICE */}
      <div className="medical-notice">
        <svg className="notice-icon" viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
        </svg>
        <div className="notice-content">
          <strong>Medical Disclaimer</strong>
          <p>This AI-assisted analysis is for screening purposes only. Please consult a qualified optometrist for professional diagnosis and treatment recommendations.</p>
        </div>
      </div>
    </div>
  );
}

export default ResultsDisplay;
