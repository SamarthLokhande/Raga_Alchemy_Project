import React, { useState, useRef, useEffect } from 'react';
import useAudioRecorder from '../hooks/useAudioRecorder';
import './RealTimePitchMonitor.css';

const RealTimePitchMonitor = () => {
  const { isRecording, startRecording, stopRecording, error } = useAudioRecorder();
  const [currentPitch, setCurrentPitch] = useState(null);
  const [pitchHistory, setPitchHistory] = useState([]);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const analyzerRef = useRef(null);
  const audioContextRef = useRef(null);
  const sourceRef = useRef(null);

  useEffect(() => {
    return () => {
      // Cleanup
      if (sourceRef.current) {
        sourceRef.current.disconnect();
      }
      if (audioContextRef.current) {
        audioContextRef.current.close();
      }
    };
  }, []);

  const startPitchMonitoring = async () => {
    try {
      setIsAnalyzing(true);
      setPitchHistory([]);
      
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          sampleRate: 22050,
          channelCount: 1,
          echoCancellation: true
        } 
      });

      audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)();
      sourceRef.current = audioContextRef.current.createMediaStreamSource(stream);
      
      // Create analyzer for pitch detection
      analyzerRef.current = audioContextRef.current.createAnalyser();
      analyzerRef.current.fftSize = 2048;
      sourceRef.current.connect(analyzerRef.current);

      startAnalyzing();
      startRecording();

    } catch (err) {
      console.error('Error starting pitch monitoring:', err);
      setIsAnalyzing(false);
    }
  };

  const startAnalyzing = () => {
    const analyzePitch = () => {
      if (!analyzerRef.current || !isAnalyzing) return;

      const bufferLength = analyzerRef.current.frequencyBinCount;
      const dataArray = new Uint8Array(bufferLength);
      analyzerRef.current.getByteTimeDomainData(dataArray);

      const pitch = detectPitch(dataArray, audioContextRef.current.sampleRate);
      
      if (pitch > 0) {
        setCurrentPitch(pitch);
        setPitchHistory(prev => [...prev.slice(-49), pitch]); // Keep last 50 values
      }

      requestAnimationFrame(analyzePitch);
    };

    analyzePitch();
  };

  const detectPitch = (dataArray, sampleRate) => {
    // Simple autocorrelation pitch detection
    const correlation = autoCorrelate(dataArray, sampleRate);
    return correlation;
  };

  const autoCorrelate = (buf, sampleRate) => {
    const SIZE = buf.length;
    const MAX_SAMPLES = Math.floor(SIZE / 2);
    let best_offset = -1;
    let best_correlation = 0;
    let rms = 0;

    for (let i = 0; i < SIZE; i++) {
      const val = (buf[i] - 128) / 128;
      rms += val * val;
    }
    rms = Math.sqrt(rms / SIZE);

    if (rms < 0.01) return -1;

    let lastCorrelation = 1;
    for (let offset = 0; offset < MAX_SAMPLES; offset++) {
      let correlation = 0;

      for (let i = 0; i < MAX_SAMPLES; i++) {
        const val1 = (buf[i] - 128) / 128;
        const val2 = (buf[i + offset] - 128) / 128;
        correlation += Math.abs(val1 - val2);
      }

      correlation = 1 - (correlation / MAX_SAMPLES);
      if (correlation > 0.9 && correlation > lastCorrelation) {
        if (correlation > best_correlation) {
          best_correlation = correlation;
          best_offset = offset;
        }
      }
      lastCorrelation = correlation;
    }

    if (best_correlation > 0.01) {
      return sampleRate / best_offset;
    }
    return -1;
  };

  const stopPitchMonitoring = () => {
    setIsAnalyzing(false);
    stopRecording();
    
    if (sourceRef.current) {
      sourceRef.current.disconnect();
    }
    if (audioContextRef.current) {
      audioContextRef.current.close();
    }
  };

  const frequencyToNote = (frequency) => {
    if (!frequency || frequency === -1) return null;
    
    const noteNames = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
    const A4 = 440;
    const note = 12 * (Math.log(frequency / A4) / Math.log(2));
    const noteNumber = Math.round(note) + 69;
    const noteName = noteNames[noteNumber % 12];
    const octave = Math.floor(noteNumber / 12) - 1;
    
    return `${noteName}${octave}`;
  };

  const frequencyToSwara = (frequency) => {
    // Simplified mapping - in practice, this would be more complex
    const swaraMap = {
      261.63: 'S', 277.18: 'r', 293.66: 'R', 311.13: 'g',
      329.63: 'G', 349.23: 'M', 392.00: 'P', 440.00: 'D'
    };
    
    if (!frequency) return 'S';
    
    // Find closest swara
    let closestSwara = 'S';
    let minDiff = Infinity;
    
    Object.entries(swaraMap).forEach(([freq, swara]) => {
      const diff = Math.abs(frequency - parseFloat(freq));
      if (diff < minDiff) {
        minDiff = diff;
        closestSwara = swara;
      }
    });
    
    return closestSwara;
  };

  return (
    <div className="pitch-monitor-container">
      <h3>Real-Time Pitch Monitor</h3>
      
      <div className="monitor-controls">
        <button
          className={`monitor-btn ${isAnalyzing ? 'stop' : 'start'}`}
          onClick={isAnalyzing ? stopPitchMonitoring : startPitchMonitoring}
          disabled={false}
        >
          {isAnalyzing ? '⏹️ Stop Monitoring' : '🎤 Start Monitoring'}
        </button>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      <div className="pitch-display">
        <div className="current-pitch">
          <h4>Current Pitch</h4>
          {currentPitch ? (
            <div className="pitch-info">
              <div className="frequency">
                {currentPitch.toFixed(2)} Hz
              </div>
              <div className="note">
                Note: {frequencyToNote(currentPitch)}
              </div>
              <div className="swara">
                Swara: {frequencyToSwara(currentPitch)}
              </div>
            </div>
          ) : (
            <div className="no-pitch">
              No pitch detected
            </div>
          )}
        </div>

        <div className="pitch-history">
          <h4>Pitch Stability</h4>
          <div className="history-graph">
            {pitchHistory.map((pitch, index) => (
              <div
                key={index}
                className="pitch-bar"
                style={{
                  height: `${Math.min(100, (pitch / 1000) * 100)}%`,
                  backgroundColor: pitch > 400 ? '#ff6b6b' : '#51cf66'
                }}
                title={`${pitch.toFixed(2)} Hz`}
              />
            ))}
          </div>
        </div>
      </div>

      <div className="monitor-info">
        <p>🎵 Sing into your microphone to see real-time pitch analysis</p>
        <p>🎯 Green bars indicate stable pitch, red shows high pitch</p>
      </div>
    </div>
  );
};

export default RealTimePitchMonitor;