import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom'; // useNavigate import
import Header from './Header';
import '../styles/RegeneratedImage.css'; // 새로운 CSS 파일

const RegeneratedImage = () => {
  const [modifiedImage, setModifiedImage] = useState('');
  const [explanation, setExplanation] = useState('설명을 불러오는 중입니다...');
  const [error, setError] = useState(null);
  const navigate = useNavigate(); // 페이지 이동을 위한 useNavigate

  // 수정된 이미지를 API에서 가져오는 함수
  const fetchModifiedImage = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/images/regenerate`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
  
      if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status}, ${response.statusText}`);
      }
  
      const data = await response.json();
  
      // modified_image가 존재하는지 확인
      if (data.modified_image) {
        setModifiedImage(`data:image/png;base64,${data.modified_image}`);
      } else {
        throw new Error('API 응답에 modified_image 속성이 없습니다.');
      }
    } catch (err) {
      setError(`이미지를 가져오는 중 오류 발생: ${err.message}`);
      console.error('Error details:', err);
    }
  };

  // 설명 데이터를 API에서 가져오는 함수
  const fetchExplanation = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/get-description`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        if (response.status === 404) {
          setExplanation('설명 데이터가 존재하지 않습니다.');
        } else {
          throw new Error(`HTTP Error: ${response.status}, ${response.statusText}`);
        }
      } else {
        const data = await response.json();
        if (data.status === 'success') {
          setExplanation(data.explanation);
        } else {
          setExplanation('설명을 불러오는 중 오류가 발생했습니다.');
        }
      }
    } catch (err) {
      setError(`설명을 가져오는 중 오류 발생: ${err.message}`);
    }
  };

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

  // 컴포넌트 로드 시 API 호출
  useEffect(() => {
    fetchModifiedImage();
    fetchExplanation();
  }, []);

  if (error) {
    return (
      <div>
        <Header />
        <div className="error-container">
          <p className="error-message">{error}</p>
          <button onClick={() => navigate('/ImageModification')} className="retry-button">
            수정 화면으로 돌아가기
          </button>
        </div>
      </div>
    );
  }

  if (!modifiedImage) {
    return (
      <div>
        <Header />
        <div className="loading-container">
          <p>이미지를 불러오는 중입니다...</p>
        </div>
      </div>
    );
  }

  // 카카오톡 공유 함수
  const shareToKakao = () => {
    if (window.Kakao) {
      try {
        // Base64 이미지를 Blob URL로 변환
        const blobUrl = convertBase64ToBlobUrl(modifiedImage);

        // 카카오톡 공유 API 호출
        window.Kakao.Share.sendDefault({
          objectType: 'feed',
          content: {
            title: 'AI가 생성한 이미지',
            description: explanation, // 설명 데이터
            imageUrl: blobUrl, // Blob URL 사용
            link: { // 필수 link 키 추가
              mobileWebUrl: 'http://localhost:3000', // 실제 배포 URL로 변경 필요
              webUrl: 'http://localhost:3000', // 실제 배포 URL로 변경 필요
            },
          },
          buttons: [
            {
              title: '이미지 확인하기',
              link: { // 버튼 링크 추가
                mobileWebUrl: 'http://localhost:3000',
                webUrl: 'http://localhost:3000',
              },
            },
          ],
        });
      } catch (error) {
        console.error('카카오톡 공유 중 오류 발생:', error);
        alert('카카오톡 공유 중 오류가 발생했습니다. 다시 시도해주세요.');
      }
    } else {
      alert('Kakao SDK가 초기화되지 않았습니다.');
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
              <p className="image-description">{explanation}</p>
            </div>
            <div className="action-box">
              <p
                className="image-modification-text"
                onClick={() => navigate('/ImageModification')}
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
