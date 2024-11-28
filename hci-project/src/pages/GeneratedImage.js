import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom'; // useLocation, useNavigate import
import Header from './Header';
import '../styles/GeneratedImage.css';

const GeneratedImage = () => {
  const location = useLocation(); // 이전 페이지에서 전달된 데이터 가져오기
  const navigate = useNavigate(); // 페이지 이동을 위한 useNavigate
  const { generatedImage } = location.state || {}; // AIImageGeneration에서 전달된 데이터 가져오기
  const [explanation, setExplanation] = useState(''); // 설명 데이터 상태
  const [error, setError] = useState(null); // 에러 상태

  // Kakao SDK 초기화 확인
  useEffect(() => {
    if (!window.Kakao.isInitialized()) {
      window.Kakao.init(process.env.REACT_APP_KAKAO_API_KEY); // 환경변수에서 Kakao API Key 가져오기
      console.log('Kakao SDK initialized:', window.Kakao.isInitialized());
    }
  }, []);

  // 설명 데이터 가져오기
  useEffect(() => {
    const fetchExplanation = async () => {
      try {
        const descriptionResponse = await fetch(
          `${process.env.REACT_APP_BACKEND_URL}/api/get-description`
        );
        if (!descriptionResponse.ok) {
          throw new Error(
            `Error ${descriptionResponse.status}: 설명 데이터를 가져올 수 없습니다.`
          );
        }
        const descriptionData = await descriptionResponse.json();
        if (descriptionData.status === 'success') {
          setExplanation(descriptionData.explanation);
        } else {
          throw new Error(
            descriptionData.message ||
              '설명 데이터를 가져오는 중 문제가 발생했습니다.'
          );
        }
      } catch (err) {
        setError(err.message);
      }
    };

    fetchExplanation();
  }, []);

  // Base64 이미지를 Blob URL로 변환
  const convertBase64ToBlobUrl = (base64Image) => {
    const byteString = atob(base64Image.split(',')[1]);
    const mimeString = base64Image.split(',')[0].split(':')[1].split(';')[0];

    const arrayBuffer = new Uint8Array(byteString.length);
    for (let i = 0; i < byteString.length; i++) {
      arrayBuffer[i] = byteString.charCodeAt(i);
    }

    const blob = new Blob([arrayBuffer], { type: mimeString });
    return URL.createObjectURL(blob); // Blob URL 반환
  };

  // 이미지 수정 페이지로 이동하는 함수
  const handleModificationClick = () => {
    navigate('/ImageModification');
  };

  // 카카오톡 공유하기 함수
  const shareToKakao = () => {
    if (window.Kakao) {
      try {
        if (!generatedImage.startsWith('data:image')) {
          console.error('유효하지 않은 이미지 URL입니다:', generatedImage);
          alert('유효하지 않은 이미지 URL입니다.');
          return;
        }

        // Base64 이미지를 Blob URL로 변환
        const blobUrl = convertBase64ToBlobUrl(generatedImage);

        // 카카오톡 공유 API 호출
        window.Kakao.Share.sendDefault({
          objectType: 'feed',
          content: {
            title: 'AI 이미지 생성 결과',
            description: explanation, // 설명 데이터
            imageUrl: blobUrl, // Blob URL 사용
            link: {
              mobileWebUrl: 'http://localhost:3000',
              webUrl: 'http://localhost:3000',
            },
          },
          buttons: [
            {
              title: '결과 보기',
              link: {
                mobileWebUrl: 'http://localhost:3000',
                webUrl: 'http://localhost:3000',
              },
            },
          ],
        });
      } catch (error) {
        console.error('Kakao 공유하기 중 오류:', error);
        alert('Kakao 공유하기 중 문제가 발생했습니다. 다시 시도해주세요.');
      }
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
              <img
                src={generatedImage}
                alt="Generated Result"
                className="generated-image"
              />
              <p className="image-title">이미지 생성 결과</p>
            </div>
          </div>
          <div className="right-section">
            <div className="description-box">
              <p className="image-description">{explanation}</p>
            </div>
            <div className="action-box">
              <p
                className="image-modification-text"
                onClick={handleModificationClick}
                style={{ cursor: 'pointer', textDecoration: 'underline' }}
              >
                이미지를 수정하고 싶으신가요?
              </p>
              <button
                className="kakao-share-button"
                onClick={shareToKakao}
              >
                <img
                  src="/img/kakao.png"
                  alt="Kakao Icon"
                  className="kakao-icon"
                />
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
