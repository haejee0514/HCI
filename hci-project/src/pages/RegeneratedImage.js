import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom'; // useLocation, useNavigate import
import Header from './Header';
import '../styles/RegeneratedImage.css'; // 새로운 CSS 파일

const RegeneratedImage = () => {
  const location = useLocation(); // 이전 페이지에서 전달된 데이터 가져오기
  const navigate = useNavigate(); // 페이지 이동을 위한 useNavigate

  // 상태 데이터
  const modifiedImage = location.state?.modifiedImage || ''; // 전달된 수정된 이미지
  const explanation = location.state?.explanation || '설명이 제공되지 않았습니다.'; // 설명 데이터

  if (!modifiedImage) {
    return (
      <div>
        <Header />
        <div className="error-container">
          <p className="error-message">
            수정된 이미지를 불러오는 데 실패했습니다. 다시 시도해주세요.
          </p>
          <button onClick={() => navigate('/ImageModification')} className="retry-button">
            수정 화면으로 돌아가기
          </button>
        </div>
      </div>
    );
  }

  // 카카오톡 공유 함수
  const shareToKakao = () => {
    if (window.Kakao) {
      window.Kakao.Share.sendDefault({
        objectType: 'feed',
        content: {
          title: 'AI가 생성한 이미지',
          description: explanation,
          imageUrl: modifiedImage, // 이미지 URL
          link: {
            webUrl: 'https://your-website.com', // 공유할 링크
            mobileWebUrl: 'https://your-website.com',
          },
        },
        buttons: [
          {
            title: '자세히 보기',
            link: {
              webUrl: 'https://your-website.com',
              mobileWebUrl: 'https://your-website.com',
            },
          },
        ],
      });
    } else {
      alert('카카오톡 공유를 사용할 수 없습니다. 관리자에게 문의하세요.');
    }
  };

  return (
    <div>
      <Header />
      <div className="outer-container">
        <div className="generated-image-container">
          <div className="left-section">
            <div className="image-box">
              <img src={modifiedImage} alt="Regenerated Result" className="generated-image" />
              <p className="image-title">이미지 생성 결과</p>
            </div>
          </div>
          <div className="right-section">
            <div className="description-box">
              <p className="image-description">{explanation}</p> {/* 기존 설명 출력 */}
            </div>
            <div className="action-box">
              <p
                className="image-modification-text"
                onClick={() => navigate('/ImageModification')} // 다시 수정 페이지로 이동
                style={{ cursor: 'pointer', textDecoration: 'underline' }}
              >
                이미지를 수정하고 싶으신가요?
              </p>
              <button className="kakao-share-button" onClick={shareToKakao}>
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

export default RegeneratedImage;
