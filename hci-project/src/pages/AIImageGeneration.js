import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom'; // useNavigate import
import Header from './Header'; // Header 컴포넌트 임포트
import '../styles/AIImageGeneration.css';

const AIImageGeneration = () => {
  const navigate = useNavigate(); // 페이지 이동을 위한 useNavigate

  useEffect(() => {
    const fetchGeneratedImage = async () => {
      try {
        const response = await fetch(
          `${process.env.REACT_APP_BACKEND_URL}/api/images/generate`, 
          {
            method: 'GET', // GET 방식으로 변경
          }
        );

        if (!response.ok) {
          if (response.status === 503) {
            const data = await response.json();
            alert(`현재 서버가 바쁩니다. 예상 대기 시간: ${data.estimated_time}초`);
            return;
          }
          throw new Error(`Error: ${response.status}, ${response.statusText}`);
        }

        const data = await response.json();

        if (data.status === 'success') {
          const generatedImage = `data:image/png;base64,${data.generated_image}`; // Base64 이미지
          navigate('/GeneratedImage', {
            state: { generatedImage }, // seed 제거 후, generatedImage만 전달
          });
        } else {
          throw new Error(data.error || '이미지 생성에 실패했습니다.');
        }
      } catch (error) {
        console.error('이미지 생성 중 오류:', error.message);
        alert('이미지 생성 중 문제가 발생했습니다. 다시 시도해주세요.');
      }
    };

    fetchGeneratedImage();
  }, [navigate]);

  return (
    <div>
      <Header /> {/* Header 컴포넌트를 상단에 추가 */}
      <div className="ai-image-generation-container">
        <div className="vital-wave-loader">
          <div className="wave-bar"></div>
          <div className="wave-bar"></div>
          <div className="wave-bar"></div>
          <div className="wave-bar"></div>
          <div className="wave-bar"></div>
        </div>
        <p className="loading-text">
          뇌파에 따른 AI 이미지 생성 중..
          <br />
          잠시만 기다려주세요
        </p>
      </div>
    </div>
  );
};

export default AIImageGeneration;
