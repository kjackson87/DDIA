import React, { useState, useEffect, useCallback } from 'react';

const FixedBoxLinearizabilityViz = () => {
  const [isLinearizable, setIsLinearizable] = useState(true);
  const [operations, setOperations] = useState([]);
  const [currentTime, setCurrentTime] = useState(0);
  const [currentValue, setCurrentValue] = useState(0);
  const [scenario, setScenario] = useState(null);
  const [isPaused, setIsPaused] = useState(false);
  const [speed, setSpeed] = useState(100);

  const timelineLength = 800;
  const timelineStart = 50;
  const timelineEnd = timelineStart + timelineLength;
  const totalDuration = 100;
  const rowHeight = 40;
  const boxHeight = 30;

  const mapTimeToPosition = useCallback((time) => 
    timelineStart + (time / totalDuration) * timelineLength, [timelineStart, timelineLength, totalDuration]);

  useEffect(() => {
    if (!isPaused) {
      const timer = setInterval(() => {
        setCurrentTime((prevTime) => (prevTime + 1) % totalDuration);
      }, speed);
      return () => clearInterval(timer);
    }
  }, [totalDuration, isPaused, speed]);

  const addOperation = (type, startTime, value = null) => {
    const newOp = {
      id: operations.length + 1,
      type,
      startTime,
      endTime: (startTime + 10) % totalDuration,
      value: type === 'write' ? (value !== null ? value : currentValue + 1) : null
    };
    setOperations((prevOps) => [...prevOps, newOp]);
    if (type === 'write') {
      if (isLinearizable) {
        setCurrentValue(newOp.value);
      } else {
        // In non-linearizable scenario, update the value with some delay
        setTimeout(() => setCurrentValue(newOp.value), Math.random() * 1000);
      }
    }
  };

  const getOperationColor = (op) => {
    if (op.type === 'write') return '#60a5fa';
    return isLinearizable ? '#34d399' : '#f87171';
  };

  const generateScenario = (linearizable) => {
    setOperations([]);
    setCurrentValue(0);
    setCurrentTime(0);
    setIsLinearizable(linearizable);
    
    const scenarioOperations = [
      { type: 'write', startTime: 5, value: 1 },
      { type: 'read', startTime: 15 },
      { type: 'write', startTime: 25, value: 2 },
      { type: 'read', startTime: 35 },
    ];

    setScenario(scenarioOperations);
  };

  useEffect(() => {
    if (scenario) {
      const currentOp = scenario.find(op => op.startTime === currentTime);
      if (currentOp) {
        addOperation(currentOp.type, currentOp.startTime, currentOp.value);
      }
      if (currentTime === 0) {
        setOperations([]);
      }
    }
  }, [currentTime, scenario]);

  const getReadValue = (op) => {
    if (isLinearizable) {
      const lastCompletedWrite = operations
        .filter(o => o.type === 'write' && (o.endTime <= op.startTime || (o.endTime > op.startTime && o.startTime < op.startTime)))
        .pop();
      return lastCompletedWrite ? lastCompletedWrite.value : 0;
    } else {
      // In non-linearizable scenario, read might return any previous value
      const possibleValues = operations
        .filter(o => o.type === 'write' && o.startTime <= op.endTime)
        .map(o => o.value);
      return possibleValues[Math.floor(Math.random() * possibleValues.length)] || 0;
    }
  };

  const getExplanation = () => {
    if (isLinearizable) {
      return (
        <div className="mt-4 p-4 bg-green-100 rounded">
          <h3 className="font-bold text-green-800">Linearizable Scenario Explanation:</h3>
          <p>In this scenario, all operations behave as if they occurred instantaneously at some point between their start and end times:</p>
          <ul className="list-disc list-inside">
            <li>The first write (x=1) takes effect before the first read, so the read returns 1.</li>
            <li>The second write (x=2) occurs after the first read but may not be complete before the second read starts.</li>
            <li>The second read will return 1 if it occurs before the second write completes, or 2 if it occurs after.</li>
          </ul>
          <p>This behavior maintains the illusion of a single, atomic copy of the data, which is the key characteristic of linearizability.</p>
        </div>
      );
    } else {
      return (
        <div className="mt-4 p-4 bg-red-100 rounded">
          <h3 className="font-bold text-red-800">Non-linearizable Scenario Explanation:</h3>
          <p>In this scenario, operations do not appear to occur instantaneously:</p>
          <ul className="list-disc list-inside">
            <li>The first read might return 0, even though a write(1) has started (but not yet completed).</li>
            <li>The second read might return any of 0, 1, or 2, regardless of the timing of the writes.</li>
            <li>The current value might update with some delay after a write operation.</li>
          </ul>
          <p>This behavior violates linearizability because it doesn't maintain the illusion of a single, atomic copy of the data. Reads can return stale or inconsistent values, making it impossible to construct a single timeline of operations that matches the real-time order and the values observed.</p>
        </div>
      );
    }
  };

  const getOperationTooltip = (op) => {
    return `${op.type === 'write' ? 'Write' : 'Read'} operation
Start time: ${op.startTime}
End time: ${op.endTime}
${op.type === 'write' ? `Value: ${op.value}` : `Read value: ${getReadValue(op)}`}`;
  };

  const renderLegend = () => (
    <div className="mt-4 flex items-center space-x-4">
      <div className="flex items-center">
        <div className="w-4 h-4 bg-blue-400 mr-2"></div>
        <span>Write operation</span>
      </div>
      <div className="flex items-center">
        <div className="w-4 h-4 bg-green-400 mr-2"></div>
        <span>Read operation (Linearizable)</span>
      </div>
      <div className="flex items-center">
        <div className="w-4 h-4 bg-red-400 mr-2"></div>
        <span>Read operation (Non-linearizable)</span>
      </div>
    </div>
  );

  return (
    <div className="p-4 bg-gray-100 rounded-lg">
      <h2 className="text-xl font-bold mb-4">Linearizability Visualization</h2>
      <svg width="100%" height="300" className="bg-white">
        {/* Timeline */}
        <line x1={timelineStart} y1="150" x2={timelineEnd} y2="150" stroke="#999" strokeWidth="2" />
        
        {/* Current time indicator */}
        <line 
          x1={mapTimeToPosition(currentTime)} 
          y1="50" 
          x2={mapTimeToPosition(currentTime)} 
          y2="250" 
          stroke="#999" 
          strokeWidth="1" 
          strokeDasharray="5,5"
        />
        
        {/* Operations */}
        {operations.map((op, index) => {
          const yPos = 80 + (index % 4) * rowHeight;
          const xStart = mapTimeToPosition(op.startTime);
          const xEnd = mapTimeToPosition(op.endTime);
          const width = xEnd - xStart;
          
          return (
            <g key={op.id}>
              <rect
                x={xStart}
                y={yPos}
                width={width}
                height={boxHeight}
                rx="15"
                ry="15"
                fill={getOperationColor(op)}
                opacity="0.8"
                stroke={getOperationColor(op)}
                strokeWidth="2"
              />
              <text x={xStart + 5} y={yPos + 20} className="text-sm fill-white font-semibold">
                {op.type === 'write' ? `Write(x=${op.value})` : 'Read(x)'}
              </text>
              {op.type === 'read' && (
                <text x={xEnd + 5} y={yPos + 20} className="text-sm font-semibold" fill={isLinearizable ? '#059669' : '#dc2626'}>
                  ⇒ {getReadValue(op)}
                </text>
              )}
              <title>{getOperationTooltip(op)}</title>
            </g>
          );
        })}

        {/* Current value indicator */}
        <text x={timelineEnd + 10} y="150" className="text-lg font-bold">
          Current value: {currentValue}
        </text>
      </svg>
      
      <div className="mt-4 space-x-4">
        <button
          onClick={() => generateScenario(true)}
          className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50"
        >
          Linearizable Scenario
        </button>
        <button
          onClick={() => generateScenario(false)}
          className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50"
        >
          Non-linearizable Scenario
        </button>
        <button
          onClick={() => setIsPaused(!isPaused)}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
        >
          {isPaused ? 'Resume' : 'Pause'}
        </button>
      </div>
      <div className="mt-4">
        <label htmlFor="speed-control" className="mr-2">Speed:</label>
        <input
          id="speed-control"
          type="range"
          min="50"
          max="500"
          step="50"
          value={speed}
          onChange={(e) => setSpeed(Number(e.target.value))}
          className="w-48"
        />
        <span className="ml-2">{speed}ms</span>
      </div>
      <p className="mt-2">
        Current state: <span className="font-bold">{isLinearizable ? 'Linearizable' : 'Non-linearizable'}</span>
      </p>
      {getExplanation()}
      {renderLegend()}
    </div>
  );
};

export default FixedBoxLinearizabilityViz;