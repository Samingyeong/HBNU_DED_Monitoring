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
    <header className="w-[98%] mx-auto h-16 bg-white shadow-lg rounded-xl">
      <div className="flex items-center justify-between h-full px-8">
        {/* Left Side - Logo and Title */}
        <div className="flex items-center space-x-3">
          {/* Logo Image Placeholder */}
          <div className="w-12 h-4 bg-gray-300 flex items-center justify-center rounded">
            <span className="text-xs text-gray-600 font-medium">LOGO</span>
          </div>
          
          {/* DED Monitoring System Title */}
          <h1 
            className="text-sm lg:text-base xl:text-lg font-normal"
            style={{ 
              fontFamily: 'Expo M, sans-serif',
              color: '#09357F'
            }}
          >
            DED Monitoring System
          </h1>
        </div>
        
        {/* Right Side - Time and Settings */}
        <div className="flex items-center space-x-4">
          {/* Time Display */}
          <div 
            className="text-xs lg:text-sm font-normal"
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
            className="w-8 h-8 flex items-center justify-center hover:bg-gray-100 rounded-lg transition-colors"
          >
            <svg 
              className="w-4 h-4" 
              fill="none" 
              stroke="#1D1B20" 
              viewBox="0 0 24 24"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" 
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
