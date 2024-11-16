import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import NameInput from './pages/NameInput';
import MuseConnectionPrompt from './pages/MuseConnectionPrompt';

function App() {
  return (
    <Router>
      <Routes>
        {/* 기본 경로 "/"에서 Home 컴포넌트를 렌더링 */}
        <Route path="/" element={<Home />} />
        {/* NameInput 페이지 */}
        <Route path="/NameInput" element={<NameInput />} />
        {/* MuseConnectionPrompt 페이지 */}
        <Route path="/MuseConnectionPrompt" element={<MuseConnectionPrompt />} />
      </Routes>
    </Router>
  );
}

export default App;
