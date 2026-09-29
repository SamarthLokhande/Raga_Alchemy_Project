import React, { useState } from 'react';
import './App.css';
import Home from './components/Home';
import EmotionToRaga from './components/EmotionToRaga';
import MidiGeneration from './components/MidiGeneration';
import RagaDetection from './components/RagaDetection';
import AdvancedFeatures from './components/AdvancedFeatures';

function App() {
  const [currentPage, setCurrentPage] = useState('home');

  const renderPage = () => {
    switch (currentPage) {
      case 'emotion':
        return <EmotionToRaga />;
      case 'midi':
        return <MidiGeneration />;
      case 'detection':
        return <RagaDetection />;
      case 'advanced':
        return <AdvancedFeatures />;
      default:
        return <Home />;
    }
  };

  return (
    <div className="App">
      {/* Navigation Header */}
      <header className="app-header">
        <div className="nav-container">
          <div className="logo-section">
            <div className="logo-mandala">🪷</div>
            <h1 className="logo-text">Raga Alchemy</h1>
            <div className="logo-subtitle">Advanced AI meets Indian Classical Music</div>
          </div>
          
          <nav className="nav-menu">
            <button 
              className={`nav-btn ${currentPage === 'home' ? 'active' : ''}`}
              onClick={() => setCurrentPage('home')}
            >
              HOME
            </button>
            <button 
              className={`nav-btn ${currentPage === 'emotion' ? 'active' : ''}`}
              onClick={() => setCurrentPage('emotion')}
            >
              EMOTION TO RAGA
            </button>
            <button 
              className={`nav-btn ${currentPage === 'midi' ? 'active' : ''}`}
              onClick={() => setCurrentPage('midi')}
            >
              MIDI GENERATION
            </button>
            <button 
              className={`nav-btn ${currentPage === 'detection' ? 'active' : ''}`}
              onClick={() => setCurrentPage('detection')}
            >
              RAGA & SWARA DETECTION
            </button>
            <button 
              className={`nav-btn ${currentPage === 'advanced' ? 'active' : ''}`}
              onClick={() => setCurrentPage('advanced')}
            >
              ADVANCED AI
            </button>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="main-content">
        {renderPage()}
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <div className="footer-content">
          <div className="footer-mandala">🎵</div>
          <p>Experience the magic of Indian Classical Music with AI</p>
          <div className="footer-decoration">
            <span>🪷</span>
            <span>🎶</span>
            <span>🪕</span>
            <span>🥁</span>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;