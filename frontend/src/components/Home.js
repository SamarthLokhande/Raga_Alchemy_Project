import React from 'react';

const Home = () => {
  return (
    <div className="home-container">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <div className="hero-mandala">🎵</div>
          <h1 className="hero-title">Raga Alchemy</h1>
          <p className="hero-subtitle">Advanced AI meets Indian Classical Music</p>
          <div className="hero-decoration">
            <span>🪷</span>
            <span>🎶</span>
            <span>🪕</span>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="features-grid">
        <div className="feature-card">
          <div className="feature-icon">😊</div>
          <h3>Emotion to Raga Mapper</h3>
          <p>AI emotion detection with personalized raga recommendations using advanced computer vision</p>
          <div className="feature-decoration">✨</div>
        </div>

        <div className="feature-card">
          <div className="feature-icon">🎹</div>
          <h3>MIDI Generation</h3>
          <p>Generate authentic Indian classical music in MIDI format with rule-based algorithms</p>
          <div className="feature-decoration">🎼</div>
        </div>

        <div className="feature-card">
          <div className="feature-icon">🔍</div>
          <h3>Raga & Swara Detection</h3>
          <p>Real-time audio analysis for raga identification and swara detection with ML models</p>
          <div className="feature-decoration">📊</div>
        </div>

        <div className="feature-card">
          <div className="feature-icon">🤖</div>
          <h3>Advanced AI Features</h3>
          <p>Cutting-edge machine learning for music composition and analysis</p>
          <div className="feature-decoration">🚀</div>
        </div>
      </section>

      {/* How it Works */}
      <section className="how-it-works">
        <h2>How it Works</h2>
        <div className="process-flow">
          <div className="process-step">
            <div className="step-number">1</div>
            <h4>User Input & Feature Extraction</h4>
            <p>Upload audio or image for analysis</p>
          </div>
          <div className="process-arrow">→</div>
          <div className="process-step">
            <div className="step-number">2</div>
            <h4>Emotion-to-Raga Mapping</h4>
            <p>AI maps emotions to appropriate ragas</p>
          </div>
          <div className="process-arrow">→</div>
          <div className="process-step">
            <div className="step-number">3</div>
            <h4>Generate MIDI Music</h4>
            <p>Create authentic Indian classical music</p>
          </div>
          <div className="process-arrow">→</div>
          <div className="process-step">
            <div className="step-number">4</div>
            <h4>Raga & Swara Detection</h4>
            <p>Real-time analysis and identification</p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;