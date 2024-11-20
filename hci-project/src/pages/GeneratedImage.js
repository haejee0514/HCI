import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom'; // useLocation, useNavigate import
import Header from './Header';
import '../styles/GeneratedImage.css';

const GeneratedImage = () => {
  const location = useLocation(); // 이전 페이지에서 전달된 데이터 가져오기
  const navigate = useNavigate(); // 페이지 이동을 위한 useNavigate
  const [explanation, setExplanation] = useState(''); // 설명 데이터 상태
  const [generatedImage, setGeneratedImage] = useState(null); // 생성된 이미지 상태
  const [error, setError] = useState(null); // 에러 상태

  // Kakao SDK 초기화 확인
  useEffect(() => {
    if (!window.Kakao.isInitialized()) {
      window.Kakao.init(process.env.REACT_APP_KAKAO_API_KEY); // 환경변수에서 Kakao API Key 가져오기
      console.log('Kakao SDK initialized:', window.Kakao.isInitialized());
    }
  }, []);

  // 설명 및 생성된 이미지 데이터를 가져오는 함수
  useEffect(() => {
    const fetchData = async () => {
      try {
        // 1. 설명 데이터 가져오기
        const descriptionResponse = await fetch('${process.env.REACT_APP_BACKEND_URL}/api/get-description');
        if (!descriptionResponse.ok) {
          throw new Error(`Error ${descriptionResponse.status}: 설명 데이터를 가져올 수 없습니다.`);
        }
        const descriptionData = await descriptionResponse.json();
        if (descriptionData.status === 'success') {
          setExplanation(descriptionData.explanation);
        } else {
          throw new Error(descriptionData.message || '설명 데이터를 가져오는 중 문제가 발생했습니다.');
        }

        // 2. 이미지 데이터 가져오기
        const imageResponse = await fetch('${process.env.REACT_APP_BACKEND_URL}/api/images/generate', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            image_prompt: location.state?.prompt || '기본 프롬프트',
          }),
        });

        if (imageResponse.status === 503) {
          const imageData = await imageResponse.json();
          throw new Error(
            `현재 서버가 바쁩니다. 예상 대기 시간: ${imageData.estimated_time}초`
          );
        }

        if (!imageResponse.ok) {
          throw new Error(
            `Error ${imageResponse.status}: 이미지를 가져오는 중 문제가 발생했습니다.`
          );
        }

        const imageData = await imageResponse.json();
        if (imageData.status === 'success') {
          setGeneratedImage(`data:image/png;base64,${imageData.generated_image}`);
        } else {
          throw new Error(imageData.error || '이미지 데이터를 가져오는 중 문제가 발생했습니다.');
        }
      } catch (err) {
        setError(err.message);
      }
    };

    fetchData();
  }, [location.state?.prompt]);

  // 이미지 수정 페이지로 이동하는 함수
  const handleModificationClick = () => {
    navigate('/ImageModification');
  };

  // 카카오톡 공유하기 함수
  const shareToKakao = () => {
    if (window.Kakao) {
      window.Kakao.Share.sendDefault({
        objectType: 'feed',
        content: {
          title: 'AI 이미지 생성 결과',
          description: explanation, // 설명 데이터
          imageUrl: generatedImage, // 생성된 이미지
          link: {
            webUrl: 'http://localhost:3000', // 공유 시 클릭하면 이동할 URL
            mobileWebUrl: 'http://localhost:3000',
          },
        },
        buttons: [
          {
            title: '결과 보기',
            link: {
              webUrl: 'http://localhost:3000',
              mobileWebUrl: 'http://localhost:3000',
            },
          },
        ],
      });
    } else {
      alert('Kakao SDK가 초기화되지 않았습니다.');
    }
  };

  if (error) {
    return (
      <div>
        <Header />
        <p className="error-message">오류 발생: {error}</p>
      </div>
    );
  }

  if (!generatedImage) {
    return (
      <div>
        <Header />
        <p>이미지 및 설명 데이터를 불러오는 중입니다...</p>
      </div>
    );
  }

  return (
    <div>
      <Header />
      <div className="outer-container">
        <div className="generated-image-container">
          <div className="left-section">
            <div className="image-box">
              <img src={generatedImage} alt="Generated Result" className="generated-image" />
              <p className="image-title">이미지 생성 결과</p>
            </div>
          </div>
          <div className="right-section">
            <div className="description-box">
              <p className="image-description">{explanation}</p> {/* 설명 출력 */}
            </div>
            <div className="action-box">
              <p
                className="image-modification-text"
                onClick={handleModificationClick} // 클릭 시 수정 페이지로 이동
                style={{ cursor: 'pointer', textDecoration: 'underline' }}
              >
                이미지를 수정하고 싶으신가요?
              </p>
              <button
                className="kakao-share-button"
                onClick={shareToKakao} // Kakao 공유 함수 연결
              >
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
