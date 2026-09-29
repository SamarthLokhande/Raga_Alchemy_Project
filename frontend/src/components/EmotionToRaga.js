import React, { useState } from 'react';
import { detectEmotion } from '../services/api';

const EmotionToRaga = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState(null);

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setResults(null);
    }
  };

  const handleDetectEmotion = async () => {
    if (!selectedFile) return;

    setIsLoading(true);
    try {
      const result = await detectEmotion(selectedFile);
      setResults(result);
    } catch (error) {
      console.error('Error detecting emotion:', error);
      alert('Error detecting emotion. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const getEmotionColor = (emotion) => {
    const colors = {
      happy: '#16A34A',    // Green
      sad: '#3B82F6',      // Blue  
      angry: '#DC2626',    // Red
      peaceful: '#7C3AED', // Purple
      romantic: '#DB2777', // Pink
      neutral: '#6B7280',  // Gray
      surprise: '#F59E0B', // Amber
      fear: '#8B5CF6'      // Violet
    };
    return colors[emotion] || '#D4AF37';
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Emotion to Raga Mapper</h1>
        <p>Upload your image to detect emotion and get personalized raga recommendations</p>
      </div>

      <div className="raga-card">
        {/* File Upload Section */}
        <div className="file-upload" onClick={() => document.getElementById('file-input').click()}>
          <div className="upload-icon">📷</div>
          <h3>Choose File</h3>
          <p>{selectedFile ? selectedFile.name : 'No file chosen'}</p>
          <input
            id="file-input"
            type="file"
            accept="image/*"
            onChange={handleFileSelect}
          />
          <p className="upload-hint">Click to upload an image for emotion analysis</p>
        </div>

        {/* Action Button */}
        <div className="action-section">
          <button 
            className="btn-primary" 
            onClick={handleDetectEmotion}
            disabled={!selectedFile || isLoading}
          >
            {isLoading ? (
              <>
                <div className="loading-spinner" style={{marginRight: '10px'}}></div>
                Analyzing Emotion...
              </>
            ) : (
              'DETECT EMOTION & GET RAGAS'
            )}
          </button>
        </div>

        {/* How it Works */}
        <div className="info-section">
          <h3>How it Works</h3>
          <p>Our AI system uses advanced computer vision to:</p>
          <ul>
            <li>🎭 Detect facial expressions using DeepFace AI</li>
            <li>🎵 Map emotions to appropriate ragas based on classical music theory</li>
            <li>⏰ Consider time of day and mood characteristics</li>
            <li>💫 Provide personalized music recommendations</li>
          </ul>
        </div>
      </div>

      {/* Results Display */}
      {results && results.success && (
        <div className="results-container">
          <h2>Emotion Analysis Results</h2>
          
          {/* Emotion Analysis */}
          <div className="result-section">
            <h3>Emotion Detection</h3>
            <div className="result-grid">
              <div className="result-item highlight" style={{borderLeftColor: getEmotionColor(results.emotion_analysis.emotion)}}>
                <strong>Detected Emotion:</strong> 
                <span 
                  className="emotion-badge"
                  style={{backgroundColor: getEmotionColor(results.emotion_analysis.emotion)}}
                >
                  {results.emotion_analysis.emotion.toUpperCase()}
                </span>
              </div>
              <div className="result-item">
                <strong>Confidence:</strong> 
                {(results.emotion_analysis.confidence * 100).toFixed(1)}%
              </div>
              <div className="result-item">
                <strong>Face Detected:</strong> 
                {results.emotion_analysis.face_detected ? 'Yes ✅' : 'No (Using enhanced analysis) 🔍'}
              </div>
              <div className="result-item">
                <strong>Analysis Method:</strong> 
                {results.emotion_analysis.method || 'AI Emotion Recognition'}
              </div>
            </div>
          </div>

          {/* Recommended Ragas */}
          <div className="result-section">
            <h3>Recommended Ragas</h3>
            <div className="raga-grid">
              {results.recommended_ragas.map((raga, index) => (
                <div key={index} className="raga-recommendation">
                  <div className="raga-icon">🎵</div>
                  <div className="raga-info">
                    <h4>{raga.toUpperCase()}</h4>
                    <p>Perfect match for {results.emotion_analysis.emotion} mood</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Suggestions */}
          {results.suggestions && (
            <div className="suggestion-section">
              <h3>Musical Suggestion</h3>
              <p className="suggestion-text">{results.suggestions}</p>
            </div>
          )}
        </div>
      )}

      {/* Error Display */}
      {results && !results.success && (
        <div className="results-container error">
          <h2>❌ Analysis Failed</h2>
          <p>{results.error || "Unknown error occurred"}</p>
          <button 
            className="btn-primary"
            onClick={handleDetectEmotion}
          >
            Try Again
          </button>
        </div>
      )}
    </div>
  );
};

export default EmotionToRaga;