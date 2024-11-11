import React from 'react';
import '../styles/GeneratedImage.css';

const GeneratedImage = () => {
  return (
    <div className="generated-image-container">
      <img src="/img/example.webp" alt="Generated Example" className="generated-image" />
      <p className="image-description">
        "당신의 높은 알파파는 평온한 상태를 나타내어 이 풍경 이미지에 반영되었습니다."
      </p>
      <p className="image-modification-text">이미지를 수정하고 싶으신가요?</p>
      
      <button className="kakao-share-button">
        <img src="/img/kakao.png" alt="Kakao Icon" className="kakao-icon" />
        카카오톡 공유하기
      </button>
    </div>
  );
};

export default GeneratedImage;
