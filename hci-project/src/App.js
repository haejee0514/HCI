import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import NameInput from './pages/NameInput';
import MuseConnectionPrompt from './pages/MuseConnectionPrompt';
import BrainwaveReading from './pages/BrainwaveReading';
import AIImageGeneration from './pages/AIImageGeneration';
import GeneratedImage from './pages/GeneratedImage';
import ImageModification from './pages/ImageModification';
import RegeneratedImage from './pages/RegeneratedImage';
import ImageRegeneration from './pages/ImageRegeneration'; // ImageRegeneration 추가

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/NameInput" element={<NameInput />} />
        <Route path="/MuseConnectionPrompt" element={<MuseConnectionPrompt />} />
        <Route path="/BrainwaveReading" element={<BrainwaveReading />} />
        <Route path="/AIImageGeneration" element={<AIImageGeneration />} />
        <Route path="/GeneratedImage" element={<GeneratedImage />} />
        <Route path="/ImageModification" element={<ImageModification />} />
        <Route path="/RegeneratedImage" element={<RegeneratedImage />} />
        <Route path="/ImageRegeneration" element={<ImageRegeneration />} /> {/* ImageRegeneration 경로 추가 */}
      </Routes>
    </Router>
  );
}

export default App;
