import React, { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import Header from './Header'; // Header 컴포넌트 import
import '../styles/ImageRegeneration.css';

const ImageRegeneration = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { modifiedImage, seed } = location.state || {};

  useEffect(() => {
    if (!modifiedImage) {
      // 데이터가 없으면 이전 페이지로 이동
      navigate('/ImageModification');
    } else {
      // 로딩 후 RegeneratedImage 페이지로 이동
      const timer = setTimeout(() => {
        navigate('/RegeneratedImage', { state: { modifiedImage, seed } });
      }, 3000); // 3초 로딩 시간

      return () => clearTimeout(timer); // 컴포넌트 언마운트 시 타이머 정리
    }
  }, [modifiedImage, seed, navigate]);

  return (
    <div>
      <Header /> {/* Header 추가 */}
      <div className="ai-image-generation-container">
        <div className="vital-wave-loader">
          <div className="wave-bar"></div>
          <div className="wave-bar"></div>
          <div className="wave-bar"></div>
          <div className="wave-bar"></div>
          <div className="wave-bar"></div>
        </div>
        <p className="loading-text">
          수정사항을 반영한 이미지 생성 중..
          <br />
          잠시만 기다려주세요
        </p>
      </div>
    </div>
  );
};

export default ImageRegeneration;
