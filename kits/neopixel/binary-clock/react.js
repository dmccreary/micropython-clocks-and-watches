import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

const BinaryClock = () => {
  const [time, setTime] = useState(new Date());
  const [showText, setShowText] = useState(false);
  const [showValues, setShowValues] = useState(false);

  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  // Function to get binary digits for a number with specified length
  const getBinaryDigits = (num, length) => {
    return num.toString(2).padStart(length, '0').split('').map(Number);
  };

  // Get individual digits and their binary representations
  const hours = time.getHours();
  const minutes = time.getMinutes();
  const seconds = time.getSeconds();

  const hoursTens = Math.floor(hours / 10);
  const hoursOnes = hours % 10;
  const minutesTens = Math.floor(minutes / 10);
  const minutesOnes = minutes % 10;
  const secondsTens = Math.floor(seconds / 10);
  const secondsOnes = seconds % 10;

  // Get binary arrays for each digit
  const hoursTensBinary = getBinaryDigits(hoursTens, 2);
  const hoursOnesBinary = getBinaryDigits(hoursOnes, 4);
  const minutesTensBinary = getBinaryDigits(minutesTens, 3);
  const minutesOnesBinary = getBinaryDigits(minutesOnes, 4);
  const secondsTensBinary = getBinaryDigits(secondsTens, 3);
  const secondsOnesBinary = getBinaryDigits(secondsOnes, 4);

  const renderBinaryColumn = (bits, powerValues, label) => (
    <div className="flex flex-col items-center gap-2">
      <div className="text-sm text-gray-500">{label}</div>
      <div className="flex flex-col-reverse gap-2">
        {bits.map((bit, index) => (
          <div 
            key={index} 
            className={`w-8 h-8 rounded-full flex items-center justify-center
              ${bit ? 'bg-blue-500' : 'bg-gray-200'}`}
          >
            {showValues && (
              <span className="text-xs text-white">
                {powerValues[index]}
              </span>
            )}
          </div>
        ))}
      </div>
      <div className="text-lg font-bold">
        {label.split(' ')[1]}
      </div>
    </div>
  );

  return (
    <Card className="w-full max-w-3xl">
      <CardHeader>
        <CardTitle>Binary Clock</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex flex-col items-center gap-4">
          <div className="flex gap-8 p-4">
            {renderBinaryColumn(hoursTensBinary, [2, 1], 'Hr Tens')}
            {renderBinaryColumn(hoursOnesBinary, [8, 4, 2, 1], 'Hr Ones')}
            {renderBinaryColumn(minutesTensBinary, [4, 2, 1], 'Min Tens')}
            {renderBinaryColumn(minutesOnesBinary, [8, 4, 2, 1], 'Min Ones')}
            {renderBinaryColumn(secondsTensBinary, [4, 2, 1], 'Sec Tens')}
            {renderBinaryColumn(secondsOnesBinary, [8, 4, 2, 1], 'Sec Ones')}
          </div>
          
          {showText && (
            <div className="text-2xl font-mono">
              {`${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`}
            </div>
          )}
          
          <div className="flex gap-4">
            <Button 
              onClick={() => setShowText(!showText)}
              variant="outline"
            >
              {showText ? 'Hide Text Time' : 'Show Text Time'}
            </Button>
            <Button 
              onClick={() => setShowValues(!showValues)}
              variant="outline"
            >
              {showValues ? 'Hide Values' : 'Show Values'}
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default BinaryClock;