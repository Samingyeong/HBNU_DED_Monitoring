import React, { useState, useEffect } from 'react';
import EmergencyModal from './EmergencyModal';

interface HeaderProps {
  emergency: boolean;
  onEmergencyToggle: (emergency: boolean) => void;
}

export default function Header({ emergency, onEmergencyToggle }: HeaderProps) {
  const [currentTime, setCurrentTime] = useState(new Date().toLocaleString('ko-KR'));
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date().toLocaleString('ko-KR'));
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const handleSettingsClick = () => {
    setIsModalOpen(true);
  };

  const handleModalClose = () => {
    setIsModalOpen(false);
  };

  return (
    <header className="w-[98%] mx-auto h-20 bg-white shadow-lg rounded-lg relative">
      <div className="flex items-center justify-between h-full px-8">
        {/* Left Side - Logo and Title */}
        <div className="flex items-center space-x-4">
          {/* Logo Image Placeholder */}
          <div className="w-16 h-6 bg-gray-300 flex items-center justify-center rounded">
            <span className="text-xs text-gray-600 font-medium">LOGO</span>
          </div>
          
          {/* DED Monitoring System Title */}
          <h1 
            className="text-lg lg:text-xl xl:text-2xl font-normal"
            style={{ 
              fontFamily: 'Expo M, sans-serif',
              color: '#09357F'
            }}
          >
            DED Monitoring System
          </h1>
        </div>
        
        {/* Right Side - Time and Settings */}
        <div className="flex items-center space-x-6">
          {/* Time Display */}
          <div 
            className="text-base lg:text-lg font-normal"
            style={{ 
              fontFamily: 'Roboto, sans-serif',
              color: '#000000',
              opacity: 0.5
            }}
          >
            {currentTime}
          </div>
          
          {/* Settings Button */}
          <button 
            onClick={handleSettingsClick}
            className="w-10 h-10 flex items-center justify-center hover:bg-gray-100 rounded-lg transition-colors"
          >
            <svg 
              className="w-5 h-5" 
              fill="none" 
              stroke="#1D1B20" 
              viewBox="0 0 24 24"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" 
              />
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" 
              />
            </svg>
          </button>
        </div>
      </div>

      <EmergencyModal
        isOpen={isModalOpen}
        onClose={handleModalClose}
        emergency={emergency}
        onEmergencyToggle={onEmergencyToggle}
      />
    </header>
  );
}
