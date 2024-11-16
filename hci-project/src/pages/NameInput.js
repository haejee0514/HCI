import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // useNavigate import
import Header from './Header'; // Header 컴포넌트 import
import '../styles/NameInput.css';

const NameInput = () => {
  const [name, setName] = useState('');
  const navigate = useNavigate(); // useNavigate 훅 생성

  const handleInputChange = (e) => {
    setName(e.target.value);
  };

  const handleSubmit = () => {
    if (name.trim() === '') {
      alert("이름을 입력해주세요");
    } else {
      // MuseConnectionPrompt 페이지로 이름을 전달하며 이동
      navigate('/MuseConnectionPrompt', { state: { name } });
    }
  };

  return (
    <div>
      <Header /> {/* Header 컴포넌트 추가 */}
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
          className="submit-button"
        >
          확인
        </button>
      </div>
    </div>
  );
};

export default NameInput;
