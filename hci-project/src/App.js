import React, { useState } from 'react';
import NameInput from './pages/NameInput';
import MuseConnectionPrompt from './pages/MuseConnectionPrompt'; // 파일 이름과 컴포넌트 이름 수정

function App() {
  const [name, setName] = useState('');
  const [showMuseConnectionPrompt, setShowMuseConnectionPrompt] = useState(false);

  const handleNameSubmit = (enteredName) => {
    setName(enteredName);
    setShowMuseConnectionPrompt(true); // MuseConnectionPrompt 화면으로 전환
  };

  return (
    <div className="App">
      {!showMuseConnectionPrompt ? (
        <NameInput onNameSubmit={handleNameSubmit} />
      ) : (
        <MuseConnectionPrompt name={name} />
      )}
    </div>
  );
}

export default App;
