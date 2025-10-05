import React from 'react';

function CameraView() {
  return (
    <div className="card h-full flex flex-col">
      <h3 className="text-lg font-medium text-gray-900 mb-2">Camera Feeds</h3>
      <div className="flex-1 grid grid-rows-2 gap-4">
        <div className="bg-gray-200 flex items-center justify-center text-gray-500 rounded-lg">
          Basler Camera Feed
        </div>
        <div className="bg-gray-200 flex items-center justify-center text-gray-500 rounded-lg">
          HikRobot Cameras (Combined)
        </div>
      </div>
    </div>
  );
}

export default CameraView;
