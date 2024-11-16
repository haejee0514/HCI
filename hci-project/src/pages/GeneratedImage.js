import React from 'react';
import Header from './Header';
import '../styles/GeneratedImage.css';

const GeneratedImage = () => {
  return (
    <div>
      <Header /> {/* Header 컴포넌트를 상단에 추가 */}
      <div className="outer-container">
        <div className="generated-image-container">
          <div className="left-section">
            <div className="image-box">
              <img src="/img/example.png" alt="Generated Example" className="generated-image" />
              <p className="image-title">이미지 생성 결과</p>
            </div>
          </div>
          <div className="right-section">
            <div className="description-box">
              <p className="image-description">
                이 이미지는 당신의 뇌파 상태를 반영하여 평온하고 안정된 상태를 표현합니다. 부드러운 파스텔 색조와 잔잔한 물결은 높은 알파파가 주는 차분함과 내적 고요를 상징합니다. 구름과 태양의 부드러운 빛은 편안한 마음 상태와 평화로운 사고를 나타냅니다. 전체적으로, 이 작품은 평온을 중심에 둔 현재 안정되고 차분한 상태의 모습을 시각적으로 보여줍니다.
              </p>
            </div>
            <div className="action-box">
              <p className="image-modification-text">이미지를 수정하고 싶으신가요?</p>
              <button className="kakao-share-button">
                <img src="/img/kakao.png" alt="Kakao Icon" className="kakao-icon" />
                카카오톡 공유하기
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GeneratedImage;

