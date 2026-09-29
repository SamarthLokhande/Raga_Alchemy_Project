import React, { useState } from 'react';
import { detectRaga, detectSwaras } from '../services/api';

const RagaDetection = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisType, setAnalysisType] = useState('raga');
  const [results, setResults] = useState(null);

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setResults(null);
    }
  };

  const handleAnalyze = async () => {
    if (!selectedFile) return;

    setIsAnalyzing(true);
    try {
      let result;
      if (analysisType === 'raga') {
        result = await detectRaga(selectedFile);
      } else {
        result = await detectSwaras(selectedFile);
      }
      setResults(result);
    } catch (error) {
      console.error('Error analyzing audio:', error);
      alert('Error analyzing audio. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Raga & Swara Detection</h1>
        <p>Real-time audio analysis for raga identification and swara detection</p>
      </div>

      <div className="raga-card">
        {/* Analysis Type Selection */}
        <div className="form-group">
          <label className="form-label">Analysis Type:</label>
          <div className="analysis-type-selector">
            <button
              className={`analysis-type-btn ${analysisType === 'raga' ? 'active' : ''}`}
              onClick={() => setAnalysisType('raga')}
            >
              🎵 Raga Detection
            </button>
            <button
              className={`analysis-type-btn ${analysisType === 'swara' ? 'active' : ''}`}
              onClick={() => setAnalysisType('swara')}
            >
              🎼 Swara Detection
            </button>
          </div>
        </div>

        {/* File Upload */}
        <div className="file-upload" onClick={() => document.getElementById('audio-input').click()}>
          <div className="upload-icon">🎵</div>
          <h3>Choose Audio File</h3>
          <p>{selectedFile ? selectedFile.name : 'No file chosen'}</p>
          <input
            id="audio-input"
            type="file"
            accept="audio/*"
            onChange={handleFileSelect}
          />
          <p className="upload-hint">Click to upload an audio file for analysis</p>
        </div>

        {/* Action Button */}
        <button 
          className="btn-primary"
          onClick={handleAnalyze}
          disabled={!selectedFile || isAnalyzing}
        >
          {isAnalyzing ? (
            <>
              <div className="loading-spinner" style={{marginRight: '10px'}}></div>
              Analyzing {analysisType === 'raga' ? 'Raga' : 'Swara'}...
            </>
          ) : (
            `ANALYZE ${analysisType.toUpperCase()}`
          )}
        </button>
      </div>

      {/* Results Display */}
      {results && (
        <div className="results-container">
          <h2>Analysis Results</h2>
          
          {analysisType === 'raga' && results.detection_result && (
            <div className="result-section">
              <h3>Raga Identification</h3>
              <div className="result-grid">
                <div className="result-item highlight">
                  <strong>Detected Raga:</strong> 
                  <span className="raga-name">{results.detection_result.raga.toUpperCase()}</span>
                </div>
                <div className="result-item">
                  <strong>Confidence:</strong> 
                  {(results.detection_result.confidence * 100).toFixed(1)}%
                </div>
                <div className="result-item">
                  <strong>Model Type:</strong> 
                  {results.detection_result.model_type}
                </div>
              </div>
            </div>
          )}

          {analysisType === 'swara' && results.swara_detection && (
            <div className="result-section">
              <h3>Swara Analysis</h3>
              <div className="result-grid">
                <div className="result-item highlight">
                  <strong>Detected Swara:</strong> 
                  <span className="swara-name">{results.swara_detection.swara}</span>
                </div>
                <div className="result-item">
                  <strong>Confidence:</strong> 
                  {(results.swara_detection.confidence * 100).toFixed(1)}%
                </div>
                <div className="result-item">
                  <strong>Frequency:</strong> 
                  {results.swara_detection.exact_frequency.toFixed(2)} Hz
                </div>
              </div>

              {/* Swara Sequence */}
              {results.swara_sequence && (
                <div className="swara-sequence-section">
                  <h4>Swara Sequence</h4>
                  <div className="swara-display">
                    {results.swara_sequence.map((swara, index) => (
                      <span key={index} className="swara-item">
                        {swara}
                        <small>{Math.round((results.confidence_scores[index] || 0) * 100)}%</small>
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Performance Metrics */}
              {results.performance_metrics && (
                <div className="metrics-section">
                  <h4>Performance Metrics</h4>
                  <div className="metrics-grid">
                    <div className="metric-item">
                      <span className="metric-value">{results.performance_metrics.total_swaras_detected}</span>
                      <span className="metric-label">Total Swaras</span>
                    </div>
                    <div className="metric-item">
                      <span className="metric-value">
                        {(results.performance_metrics.average_confidence * 100).toFixed(1)}%
                      </span>
                      <span className="metric-label">Avg Confidence</span>
                    </div>
                    <div className="metric-item">
                      <span className="metric-value">
                        {(results.performance_metrics.pitch_stability * 100).toFixed(1)}%
                      </span>
                      <span className="metric-label">Pitch Stability</span>
                    </div>
                  </div>
                </div>
              )}

              {/* Suggested Ragas */}
              {results.suggested_ragas && results.suggested_ragas.length > 0 && (
                <div className="suggestions-section">
                  <h4>Suggested Ragas</h4>
                  <div className="raga-suggestions">
                    {results.suggested_ragas.map((raga, index) => (
                      <div key={index} className="raga-suggestion">
                        <span className="raga-suggestion-name">{raga.raga.toUpperCase()}</span>
                        <span className="raga-suggestion-score">
                          {(raga.match_score * 100).toFixed(1)}% match
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default RagaDetection;