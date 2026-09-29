import React, { useState } from 'react';
import { generateMidi } from '../services/api';

const MidiGeneration = () => {
  const [raga, setRaga] = useState('yaman');
  const [sequenceLength, setSequenceLength] = useState(16);
  const [tempo, setTempo] = useState(120);
  const [instrument, setInstrument] = useState('sitar');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedMidi, setGeneratedMidi] = useState(null);

  const ragaOptions = [
    { value: 'yaman', label: 'Yaman - Peaceful Evening Raga' },
    { value: 'bhairav', label: 'Bhairav - Devotional Morning Raga' },
    { value: 'malkauns', label: 'Malkauns - Serious Night Raga' },
    { value: 'kafi', label: 'Kafi - Romantic Night Raga' },
    { value: 'bhairavi', label: 'Bhairavi - Devotional Morning Raga' },
    { value: 'todi', label: 'Todi - Serious Morning Raga' }
  ];

  const instrumentOptions = [
    { value: 'sitar', label: '🎸 Sitar (Traditional Indian)', program: 104 },
    { value: 'flute', label: '🎵 Bansuri (Indian Flute)', program: 73 },
    { value: 'violin', label: '🎻 Violin', program: 40 },
    { value: 'piano', label: '🎹 Piano', program: 0 },
    { value: 'guitar', label: '🎸 Acoustic Guitar', program: 24 },
    { value: 'santoor', label: '🎵 Santoor', program: 15 },
    { value: 'tabla', label: '🥁 Tabla (Percussion)', program: 114 },
    { value: 'veena', label: '🎵 Veena', program: 105 }
  ];

  const handleGenerateMidi = async () => {
    setIsGenerating(true);
    try {
      const result = await generateMidi({
        raga,
        length: sequenceLength,
        tempo: tempo,
        instrument: instrument
      });
      setGeneratedMidi(result);
    } catch (error) {
      console.error('Error generating MIDI:', error);
      alert('Error generating MIDI. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleDownloadMidi = () => {
    if (!generatedMidi || !generatedMidi.midi_data) return;

    const link = document.createElement('a');
    link.href = `data:audio/midi;base64,${generatedMidi.midi_data}`;
    link.download = generatedMidi.filename || `raga_${raga}.mid`;
    link.click();
  };

  // Safe data access functions
  const getRagaName = () => {
    return generatedMidi?.raga ? generatedMidi.raga.toUpperCase() : 'YAMAN';
  };

  const getInstrumentName = () => {
    return generatedMidi?.composition_info?.instrument || instrument;
  };

  const getSequenceLength = () => {
    return generatedMidi?.composition_info?.length || sequenceLength;
  };

  const getTempo = () => {
    return generatedMidi?.composition_info?.tempo || tempo;
  };

  const getSwaraSequence = () => {
    return generatedMidi?.swara_sequence || ['S', 'R', 'G', 'M', 'P', 'D', 'N'];
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>MIDI Generation</h1>
        <p>Generate authentic Indian classical music in MIDI format with different instruments</p>
      </div>

      <div className="raga-card">
        <div className="form-group">
          <label className="form-label">Select Raga:</label>
          <select 
            className="form-select"
            value={raga} 
            onChange={(e) => setRaga(e.target.value)}
          >
            {ragaOptions.map(option => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label className="form-label">Select Instrument:</label>
          <select 
            className="form-select"
            value={instrument} 
            onChange={(e) => setInstrument(e.target.value)}
          >
            {instrumentOptions.map(option => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label className="form-label">Sequence Length: {sequenceLength} swaras</label>
          <input
            type="range"
            className="form-input"
            min="8"
            max="64"
            value={sequenceLength}
            onChange={(e) => setSequenceLength(parseInt(e.target.value))}
          />
          <div className="range-labels">
            <span>Short (8)</span>
            <span>Long (64)</span>
          </div>
        </div>

        <div className="form-group">
          <label className="form-label">Tempo (BPM): {tempo}</label>
          <input
            type="range"
            className="form-input"
            min="40"
            max="200"
            value={tempo}
            onChange={(e) => setTempo(parseInt(e.target.value))}
          />
          <div className="range-labels">
            <span>Slow (40)</span>
            <span>Fast (200)</span>
          </div>
        </div>

        <button 
          className="btn-primary"
          onClick={handleGenerateMidi}
          disabled={isGenerating}
        >
          {isGenerating ? (
            <>
              <div className="loading-spinner" style={{marginRight: '10px'}}></div>
              Generating {instrument} MIDI...
            </>
          ) : (
            `GENERATE ${instrument.toUpperCase()} MIDI`
          )}
        </button>
      </div>

      {/* Generated MIDI Results */}
      {generatedMidi && generatedMidi.success && (
        <div className="results-container">
          <h2>🎵 {getInstrumentName().charAt(0).toUpperCase() + getInstrumentName().slice(1)} Composition Complete!</h2>
          
          <div className="result-grid">
            <div className="result-item highlight">
              <strong>Raga:</strong> {getRagaName()}
            </div>
            <div className="result-item">
              <strong>Instrument:</strong> {getInstrumentName()}
            </div>
            <div className="result-item">
              <strong>Sequence Length:</strong> {getSequenceLength()} swaras
            </div>
            <div className="result-item">
              <strong>Tempo:</strong> {getTempo()} BPM
            </div>
          </div>

          {/* Swara Sequence */}
          <div className="swara-sequence">
            <h3>Swara Sequence</h3>
            <div className="swara-display">
              {getSwaraSequence().map((swara, index) => (
                <span key={index} className="swara-item">
                  {swara}
                </span>
              ))}
            </div>
          </div>

          {/* Download Button */}
          <div className="action-section">
            <button 
              className="btn-secondary"
              onClick={handleDownloadMidi}
            >
              📥 Download {getInstrumentName().toUpperCase()} MIDI File
            </button>
          </div>
        </div>
      )}

      {/* Error Display */}
      {generatedMidi && !generatedMidi.success && (
        <div className="results-container error">
          <h2>❌ Generation Failed</h2>
          <p>{generatedMidi.error || "Unknown error occurred"}</p>
          <button 
            className="btn-primary"
            onClick={handleGenerateMidi}
          >
            Try Again
          </button>
        </div>
      )}
    </div>
  );
};

export default MidiGeneration;