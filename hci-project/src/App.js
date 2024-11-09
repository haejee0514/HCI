import React, { useState } from 'react';
import NameInput from './pages/NameInput';
import BrainwaveReading from './pages/BrainwaveReading';

function App() {
  const [name, setName] = useState('');
  const [showBrainwaveReading, setShowBrainwaveReading] = useState(false);

  const handleNameSubmit = (enteredName) => {
    setName(enteredName);
    setShowBrainwaveReading(true); // BrainwaveReading 화면으로 전환
  };

  return (
    <div className="App">
      {!showBrainwaveReading ? (
        <NameInput onNameSubmit={handleNameSubmit} />
      ) : (
        <BrainwaveReading name={name} />
      )}
    </div>
  );
}

export default App;
