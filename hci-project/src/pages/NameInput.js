import React, { useState } from 'react';
import '../styles/NameInput.css';

const NameInput = ({ onNameSubmit }) => {
  const [name, setName] = useState('');

  const handleInputChange = (e) => {
    setName(e.target.value);
  };

  const handleSubmit = () => {
    if (name.trim() === '') {
      alert("이름을 입력해주세요");
    } else {
      onNameSubmit(name); // 이름을 전달하여 BrainwaveReading 화면으로 이동
    }
  };

  return (
    <div className="name-input-container">
      <h1 className="welcome-message">환영합니다!</h1>
      <input
        type="text"
        placeholder="이름을 입력해주세요"
        value={name}
        onChange={handleInputChange}
        className="name-input-field"
      />
      <button
        onClick={handleSubmit}
        className="submit-button" // 클릭 시 색상 변화 없음
      >
        확인
      </button>
    </div>
  );
};

export default NameInput;
