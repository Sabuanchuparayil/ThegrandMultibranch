/**
 * Real-time Indicator Component
 * Shows when data was last updated
 */
'use client';

import React, { useState, useEffect } from 'react';

interface RealTimeIndicatorProps {
  lastUpdate?: Date;
  pollInterval?: number;
}

export const RealTimeIndicator: React.FC<RealTimeIndicatorProps> = ({
  lastUpdate,
  pollInterval = 60000,
}) => {
  const [timeSinceUpdate, setTimeSinceUpdate] = useState<string>('Just now');

  useEffect(() => {
    const updateTimeSince = () => {
      if (!lastUpdate) {
        setTimeSinceUpdate('Just now');
        return;
      }

      const now = new Date();
      const diff = now.getTime() - lastUpdate.getTime();
      const seconds = Math.floor(diff / 1000);
      const minutes = Math.floor(seconds / 60);

      if (seconds < 10) {
        setTimeSinceUpdate('Just now');
      } else if (seconds < 60) {
        setTimeSinceUpdate(`${seconds}s ago`);
      } else if (minutes < 60) {
        setTimeSinceUpdate(`${minutes}m ago`);
      } else {
        const hours = Math.floor(minutes / 60);
        setTimeSinceUpdate(`${hours}h ago`);
      }
    };

    updateTimeSince();
    const interval = setInterval(updateTimeSince, 1000);

    return () => clearInterval(interval);
  }, [lastUpdate]);

  return (
    <div className="flex items-center space-x-2 text-sm text-gray-500">
      <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
      <span>Live</span>
      <span className="text-gray-400">•</span>
      <span>Updated {timeSinceUpdate}</span>
    </div>
  );
};

