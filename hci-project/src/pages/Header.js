import React from 'react';
import { Link } from 'react-router-dom'; // React Router에서 Link를 가져옵니다.
import '../styles/Header.css';

const Header = () => {
  return (
    <div className="header">
      <Link to="/nameinput"> {/* 로고 클릭 시 NameInput 페이지로 이동 */}
        <img src="/img/logo.png" alt="NeuroCanvas Logo" className="logo" />
      </Link>
    </div>
  );
};

export default Header;
