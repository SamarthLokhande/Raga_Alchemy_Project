export class AudioUtils {
  static async createAudioContext() {
    return new (window.AudioContext || window.webkitAudioContext)();
  }

  static async createAudioBuffer(audioContext, audioBlob) {
    const arrayBuffer = await audioBlob.arrayBuffer();
    return await audioContext.decodeAudioData(arrayBuffer);
  }

  static playAudioBuffer(audioContext, audioBuffer) {
    const source = audioContext.createBufferSource();
    source.buffer = audioBuffer;
    source.connect(audioContext.destination);
    source.start();
    return source;
  }

  static stopAudioSource(source) {
    if (source) {
      source.stop();
    }
  }

  static async convertToWav(audioBlob) {
    // Convert any audio format to WAV for better processing
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const arrayBuffer = await audioBlob.arrayBuffer();
    const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
    
    return this.encodeWav(audioBuffer);
  }

  static encodeWav(audioBuffer) {
    const numChannels = audioBuffer.numberOfChannels;
    const sampleRate = audioBuffer.sampleRate;
    const format = 1; // PCM
    const bitDepth = 16;

    const bytesPerSample = bitDepth / 8;
    const blockAlign = numChannels * bytesPerSample;
    const byteRate = sampleRate * blockAlign;
    const dataSize = audioBuffer.length * blockAlign;

    const buffer = new ArrayBuffer(44 + dataSize);
    const view = new DataView(buffer);

    // Write WAV header
    const writeString = (offset, string) => {
      for (let i = 0; i < string.length; i++) {
        view.setUint8(offset + i, string.charCodeAt(i));
      }
    };

    writeString(0, 'RIFF');
    view.setUint32(4, 36 + dataSize, true);
    writeString(8, 'WAVE');
    writeString(12, 'fmt ');
    view.setUint32(16, 16, true);
    view.setUint16(20, format, true);
    view.setUint16(22, numChannels, true);
    view.setUint32(24, sampleRate, true);
    view.setUint32(28, byteRate, true);
    view.setUint16(32, blockAlign, true);
    view.setUint16(34, bitDepth, true);
    writeString(36, 'data');
    view.setUint32(40, dataSize, true);

    // Write audio data
    let offset = 44;
    for (let i = 0; i < audioBuffer.length; i++) {
      for (let channel = 0; channel < numChannels; channel++) {
        const sample = Math.max(-1, Math.min(1, audioBuffer.getChannelData(channel)[i]));
        view.setInt16(offset, sample < 0 ? sample * 0x8000 : sample * 0x7FFF, true);
        offset += 2;
      }
    }

    return new Blob([buffer], { type: 'audio/wav' });
  }

  static calculateRMS(audioBuffer) {
    // Calculate Root Mean Square for volume monitoring
    const channelData = audioBuffer.getChannelData(0);
    let sum = 0;
    
    for (let i = 0; i < channelData.length; i++) {
      sum += channelData[i] * channelData[i];
    }
    
    return Math.sqrt(sum / channelData.length);
  }

  static async analyzePitch(audioBuffer) {
    // Simple pitch detection using autocorrelation
    const channelData = audioBuffer.getChannelData(0);
    const sampleRate = audioBuffer.sampleRate;
    
    // Basic autocorrelation pitch detection
    const correlation = this.autoCorrelate(channelData, sampleRate);
    return correlation;
  }

  static autoCorrelate(buf, sampleRate) {
    // Implements a simple autocorrelation pitch detection
    const SIZE = buf.length;
    const MAX_SAMPLES = Math.floor(SIZE / 2);
    let best_offset = -1;
    let best_correlation = 0;
    let rms = 0;
    let foundGoodCorrelation = false;

    for (let i = 0; i < SIZE; i++) {
      rms += buf[i] * buf[i];
    }
    rms = Math.sqrt(rms / SIZE);

    if (rms < 0.01) return -1; // Not enough signal

    let lastCorrelation = 1;
    for (let offset = 0; offset < MAX_SAMPLES; offset++) {
      let correlation = 0;

      for (let i = 0; i < MAX_SAMPLES; i++) {
        correlation += Math.abs(buf[i] - buf[i + offset]);
      }

      correlation = 1 - (correlation / MAX_SAMPLES);
      if (correlation > 0.9 && correlation > lastCorrelation) {
        foundGoodCorrelation = true;
        if (correlation > best_correlation) {
          best_correlation = correlation;
          best_offset = offset;
        }
      } else if (foundGoodCorrelation) {
        // Shift doesn't get better
        let shift = (best_correlation * MAX_SAMPLES) / sampleRate;
        return sampleRate / best_offset;
      }
      lastCorrelation = correlation;
    }

    if (best_correlation > 0.01) {
      return sampleRate / best_offset;
    }
    return -1;
  }

  static frequencyToNote(frequency) {
    // Convert frequency to musical note
    const A4 = 440;
    const noteNames = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
    
    if (frequency === -1) return null;
    
    const note = 12 * (Math.log(frequency / A4) / Math.log(2));
    const noteNumber = Math.round(note) + 69; // MIDI note number
    const noteName = noteNames[noteNumber % 12];
    const octave = Math.floor(noteNumber / 12) - 1;
    
    return {
      name: noteName,
      octave: octave,
      frequency: frequency,
      midiNumber: noteNumber
    };
  }

  static createDownloadLink(blob, filename) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  }
}