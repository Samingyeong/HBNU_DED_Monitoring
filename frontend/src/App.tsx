import React, { useState } from 'react';
import Header from './components/Header';
import CNCStatus from './components/CNCStatus';
import ConnectionStatus from './components/ConnectionStatus';
import CameraView from './components/CameraView';
import Charts from './components/Charts';

function App() {
  const [emergency, setEmergency] = useState(false);

  const handleEmergencyToggle = (newEmergency: boolean) => {
    setEmergency(newEmergency);
  };

  return (
    <div className="h-screen bg-gray-100 flex flex-col">
      {/* Header */}
      <Header emergency={emergency} onEmergencyToggle={handleEmergencyToggle} />
      
      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Panel - CNC Status & Connection Status */}
        <div className="w-80 bg-white border-r border-gray-200 flex flex-col">
          <div className="flex-1 overflow-hidden">
            <CNCStatus />
          </div>
          <div className="h-80 border-t border-gray-200 overflow-hidden">
            <ConnectionStatus />
          </div>
        </div>
        
        {/* Right Panel - Camera View & Charts */}
        <div className="flex-1 flex flex-col p-4 space-y-4">
          {/* Top Row - Camera View & Melt Pool Area Chart */}
          <div className="flex space-x-4 h-1/2">
            <div className="flex-1">
              <CameraView />
            </div>
            <div className="flex-1">
              <Charts chartType="meltpoolArea" />
            </div>
          </div>
          
          {/* Bottom Row - Temperature & Laser Power Charts */}
          <div className="flex space-x-4 h-1/2">
            <div className="flex-1">
              <Charts chartType="meltpoolTemp" />
            </div>
            <div className="flex-1">
              <Charts chartType="laserPower" />
            </div>
          </div>
        </div>
      </div>
      
      {/* Bottom Bar */}
      <div className="h-12 bg-white border-t border-gray-200 flex items-center justify-between px-6">
        <div className="text-sm text-gray-500">
          Copyright by KITECH V2.0
        </div>
        <div className="flex space-x-3">
          <button className="btn-primary">
            SAVE
          </button>
          <button className="btn-secondary">
            EXIT
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;