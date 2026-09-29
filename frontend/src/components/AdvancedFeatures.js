import React, { useState } from 'react';
import { advancedDetectRaga, advancedGenerateMusic } from '../services/api';

const AdvancedFeatures = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [activeTab, setActiveTab] = useState('detection');
  const [results, setResults] = useState(null);

  // Music Generation State
  const [raga, setRaga] = useState('yaman');
  const [length, setLength] = useState(50);
  const [temperature, setTemperature] = useState(1.0);

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setResults(null);
    }
  };

  const handleAdvancedDetection = async () => {
    if (!selectedFile) return;

    setIsProcessing(true);
    try {
      const result = await advancedDetectRaga(selectedFile);
      setResults(result);
    } catch (error) {
      console.error('Error in advanced detection:', error);
      alert('Error in advanced detection. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleGenerateMusic = async () => {
    setIsProcessing(true);
    try {
      const result = await advancedGenerateMusic({
        raga,
        length,
        temperature
      });
      setResults(result);
    } catch (error) {
      console.error('Error generating music:', error);
      alert('Error generating music. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Advanced AI Features</h1>
        <p>Cutting-edge machine learning for music composition and analysis</p>
      </div>

      {/* Tab Navigation */}
      <div className="tab-navigation">
        <button 
          className={`tab-btn ${activeTab === 'detection' ? 'active' : ''}`}
          onClick={() => setActiveTab('detection')}
        >
          🤖 Advanced Raga Detection
        </button>
        <button 
          className={`tab-btn ${activeTab === 'generation' ? 'active' : ''}`}
          onClick={() => setActiveTab('generation')}
        >
          🎼 AI Music Generation
        </button>
      </div>

      {/* Advanced Raga Detection Tab */}
      {activeTab === 'detection' && (
        <div className="raga-card">
          <h2>Advanced Raga Detection</h2>
          <p>Using CNN + LSTM deep learning models for superior accuracy</p>

          <div className="file-upload" onClick={() => document.getElementById('advanced-audio-input').click()}>
            <div className="upload-icon">🔍</div>
            <h3>Choose Audio File</h3>
            <p>{selectedFile ? selectedFile.name : 'No file chosen'}</p>
            <input
              id="advanced-audio-input"
              type="file"
              accept="audio/*"
              onChange={handleFileSelect}
            />
            <p className="upload-hint">Upload audio for advanced AI analysis</p>
          </div>

          <button 
            className="btn-primary"
            onClick={handleAdvancedDetection}
            disabled={!selectedFile || isProcessing}
          >
            {isProcessing ? (
              <>
                <div className="loading-spinner" style={{marginRight: '10px'}}></div>
                Advanced AI Analysis...
              </>
            ) : (
              'RUN ADVANCED DETECTION'
            )}
          </button>

          <div className="ai-info">
            <h4>AI Model Information</h4>
            <ul>
              <li>🎯 CNN + LSTM Architecture</li>
              <li>📊 Multi-layer Feature Extraction</li>
              <li>🎵 Temporal Pattern Recognition</li>
              <li>⚡ Real-time Processing</li>
            </ul>
          </div>
        </div>
      )}

      {/* AI Music Generation Tab */}
      {activeTab === 'generation' && (
        <div className="raga-card">
          <h2>AI Music Generation</h2>
          <p>LSTM-based music composition with creative control</p>

          <div className="form-group">
            <label className="form-label">Select Raga:</label>
            <select 
              className="form-select"
              value={raga} 
              onChange={(e) => setRaga(e.target.value)}
            >
              <option value="yaman">Yaman - Peaceful Evening</option>
              <option value="bhairav">Bhairav - Devotional Morning</option>
              <option value="malkauns">Malkauns - Serious Night</option>
              <option value="kafi">Kafi - Romantic Night</option>
              <option value="bhairavi">Bhairavi - Devotional Morning</option>
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Composition Length: {length}</label>
            <input
              type="range"
              className="form-input"
              min="20"
              max="100"
              value={length}
              onChange={(e) => setLength(parseInt(e.target.value))}
            />
          </div>

          <div className="form-group">
            <label className="form-label">
              Creativity (Temperature): {temperature.toFixed(1)}
            </label>
            <input
              type="range"
              className="form-input"
              min="0.1"
              max="2.0"
              step="0.1"
              value={temperature}
              onChange={(e) => setTemperature(parseFloat(e.target.value))}
            />
            <small>Lower: More Traditional, Higher: More Creative</small>
          </div>

          <button 
            className="btn-primary"
            onClick={handleGenerateMusic}
            disabled={isProcessing}
          >
            {isProcessing ? (
              <>
                <div className="loading-spinner" style={{marginRight: '10px'}}></div>
                AI Composing Music...
              </>
            ) : (
              'GENERATE AI MUSIC'
            )}
          </button>
        </div>
      )}

      {/* Results Display */}
      {results && (
        <div className="results-container">
          <h2>AI Results</h2>
          
          {activeTab === 'detection' && results.detection_result && (
            <div className="result-section">
              <h3>Advanced Raga Analysis</h3>
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
                  <strong>AI Model:</strong> 
                  {results.detection_result.model_type}
                </div>
                <div className="result-item">
                  <strong>Features Used:</strong> 
                  {results.detection_result.features_used}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'generation' && results.generation_result && (
            <div className="result-section">
              <h3>AI Music Composition</h3>
              <div className="result-grid">
                <div className="result-item">
                  <strong>Raga:</strong> {results.generation_result.raga.toUpperCase()}
                </div>
                <div className="result-item">
                  <strong>Length:</strong> {results.generation_result.length} swaras
                </div>
                <div className="result-item">
                  <strong>AI Model:</strong> {results.generation_result.model_type}
                </div>
                <div className="result-item">
                  <strong>Creativity Level:</strong> {results.generation_result.temperature}
                </div>
              </div>

              {/* Generated Composition */}
              <div className="composition-section">
                <h4>Generated Composition</h4>
                <div className="swara-display advanced">
                  {results.generation_result.composition.map((swara, index) => (
                    <span key={index} className="swara-item ai-generated">{swara}</span>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default AdvancedFeatures;