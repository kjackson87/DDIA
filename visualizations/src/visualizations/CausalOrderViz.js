import React, { useState, useEffect } from 'react';
import { ArrowRight, ArrowDownRight, Play, Pause, RotateCcw } from 'lucide-react';

const Node = ({ name, events }) => (
  <div className="flex-1 border rounded-lg p-4">
    <h3 className="text-lg font-semibold mb-2">{name}</h3>
    <div className="space-y-2">
      {events.map((event, index) => (
        <React.Fragment key={event.id}>
          <div
            className={`p-2 border rounded ${
              event.active ? (event.outOfOrder ? 'bg-yellow-200' : 'bg-blue-200') : 'bg-gray-100'
            } ${event.current ? 'ring-2 ring-blue-500' : ''}`}
          >
            {event.text}
          </div>
          {index < events.length - 1 && <ArrowRight className="mx-auto my-1" />}
        </React.Fragment>
      ))}
    </div>
  </div>
);

const Message = ({ from, to, active }) => {
  const fromNode = from.charAt(0);
  const toNode = to.charAt(0);
  const nodeOrder = ['A', 'B', 'C'];
  const startIndex = nodeOrder.indexOf(fromNode);
  const endIndex = nodeOrder.indexOf(toNode);
  const direction = startIndex < endIndex ? 'right' : 'left';

  return (
    <div className={`absolute top-1/2 left-1/3 w-1/3 h-0 ${direction === 'right' ? '' : 'transform -scale-x-100'}`}>
      <div className={`h-px bg-gray-400 w-full ${active ? 'animate-grow-x' : ''}`} />
      <div className={`absolute ${direction === 'right' ? 'right-0' : 'left-0'} top-1/2 transform -translate-y-1/2 ${active ? 'animate-fade-in' : 'opacity-0'}`}>
        <ArrowRight className="text-gray-400" />
      </div>
    </div>
  );
};

const scenarios = {
  normal: {
    name: "Normal Operation",
    description: "Demonstrates typical message passing and processing in a distributed system.",
    steps: [
      { node: 'A', event: 'A1', message: { from: 'A', to: 'B' }, explanation: "Node A initiates the process by sending a message to Node B." },
      { node: 'B', event: 'B1', explanation: "Node B receives the message from Node A." },
      { node: 'B', event: 'B2', message: { from: 'B', to: 'A' }, explanation: "Node B acknowledges receipt by sending a message back to Node A." },
      { node: 'A', event: 'A2', explanation: "Node A receives the acknowledgment from Node B." },
      { node: 'B', event: 'B3', message: { from: 'B', to: 'C' }, explanation: "Node B sends a message to Node C to continue the process." },
      { node: 'C', event: 'C1', explanation: "Node C receives the message from Node B." },
      { node: 'C', event: 'C2', explanation: "Node C processes the received information and updates its database." },
      { node: 'C', event: 'C3', message: { from: 'C', to: 'A' }, explanation: "Node C sends the result back to Node A." },
      { node: 'A', event: 'A3', explanation: "Node A receives the result from Node C and processes the data." },
    ]
  },
  delay: {
    name: "Network Delay",
    description: "Shows how network delays can affect the order of events. Watch for out-of-order events highlighted in yellow.",
    steps: [
      { node: 'A', event: 'A1', message: { from: 'A', to: 'B' }, explanation: "Node A sends a message to Node B." },
      { node: 'B', event: 'B1', explanation: "Node B receives the message from Node A." },
      { node: 'B', event: 'B2', message: { from: 'B', to: 'A' }, explanation: "Node B sends an acknowledgment back to Node A, but there's a network delay." },
      { node: 'B', event: 'B3', message: { from: 'B', to: 'C' }, outOfOrder: true, explanation: "Due to the delay, Node B sends a message to Node C before A has received the acknowledgment. This is out of the expected order." },
      { node: 'C', event: 'C1', explanation: "Node C receives the message from Node B." },
      { node: 'C', event: 'C2', explanation: "Node C processes the information and updates its database." },
      { node: 'A', event: 'A2', outOfOrder: true, explanation: "Node A finally receives the delayed acknowledgment from Node B. This event is out of order due to the network delay." },
      { node: 'C', event: 'C3', message: { from: 'C', to: 'A' }, explanation: "Node C sends the result back to Node A." },
      { node: 'A', event: 'A3', explanation: "Node A receives the result from Node C and processes the data." },
    ]
  },
  failure: {
    name: "Node Failure",
    description: "Illustrates how a node failure affects the system. Node C fails, causing a disruption in the expected event order.",
    steps: [
      { node: 'A', event: 'A1', message: { from: 'A', to: 'B' }, explanation: "Node A initiates the process by sending a message to Node B." },
      { node: 'B', event: 'B1', explanation: "Node B receives the message from Node A." },
      { node: 'B', event: 'B2', message: { from: 'B', to: 'A' }, explanation: "Node B acknowledges receipt by sending a message back to Node A." },
      { node: 'A', event: 'A2', explanation: "Node A receives the acknowledgment from Node B." },
      { node: 'B', event: 'B3', message: { from: 'B', to: 'C' }, explanation: "Node B attempts to send a message to Node C, but C has failed." },
      { node: 'A', event: 'A3', outOfOrder: true, explanation: "After a timeout, Node A proceeds with processing, assuming Node C has failed. This event is out of order because it occurs without input from Node C." },
    ]
  }
};

const CausalOrderViz = () => {
  const [nodes, setNodes] = useState({
    A: [
      { id: 'A1', text: 'A sends message to B', active: false, current: false, outOfOrder: false },
      { id: 'A2', text: 'A receives ack from B', active: false, current: false, outOfOrder: false },
      { id: 'A3', text: 'A processes data', active: false, current: false, outOfOrder: false },
    ],
    B: [
      { id: 'B1', text: 'B receives message from A', active: false, current: false, outOfOrder: false },
      { id: 'B2', text: 'B sends ack to A', active: false, current: false, outOfOrder: false },
      { id: 'B3', text: 'B sends message to C', active: false, current: false, outOfOrder: false },
    ],
    C: [
      { id: 'C1', text: 'C receives message from B', active: false, current: false, outOfOrder: false },
      { id: 'C2', text: 'C updates database', active: false, current: false, outOfOrder: false },
      { id: 'C3', text: 'C sends result to A', active: false, current: false, outOfOrder: false },
    ],
  });

  const [currentScenario, setCurrentScenario] = useState('normal');
  const [currentStep, setCurrentStep] = useState(-1);
  const [isPlaying, setIsPlaying] = useState(false);
  const [activeMessage, setActiveMessage] = useState(null);

  useEffect(() => {
    let timer;
    if (isPlaying && currentStep < scenarios[currentScenario].steps.length - 1) {
      timer = setTimeout(() => {
        setCurrentStep(step => step + 1);
      }, 2000);
    } else if (currentStep >= scenarios[currentScenario].steps.length - 1) {
      setIsPlaying(false);
    }
    return () => clearTimeout(timer);
  }, [isPlaying, currentStep, currentScenario]);

  useEffect(() => {
    if (currentStep >= 0) {
      const { node, event, outOfOrder, message } = scenarios[currentScenario].steps[currentStep];
      setNodes(prevNodes => {
        const newNodes = JSON.parse(JSON.stringify(prevNodes));
        newNodes[node] = newNodes[node].map(e => {
          if (e.id === event) {
            return { ...e, active: true, current: true, outOfOrder: !!outOfOrder };
          } else {
            return { ...e, current: false };
          }
        });
        return newNodes;
      });
      setActiveMessage(message);
    }
  }, [currentStep, currentScenario]);

  const resetDemo = () => {
    setCurrentStep(-1);
    setIsPlaying(false);
    setActiveMessage(null);
    setNodes(prevNodes => {
      const newNodes = JSON.parse(JSON.stringify(prevNodes));
      Object.keys(newNodes).forEach(node => {
        newNodes[node] = newNodes[node].map(event => ({ ...event, active: false, current: false, outOfOrder: false }));
      });
      return newNodes;
    });
  };

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-4">Distributed System Causal Order Demo</h2>
      <div className="mb-4">
        <select 
          value={currentScenario} 
          onChange={(e) => { setCurrentScenario(e.target.value); resetDemo(); }}
          className="mr-4 p-2 border rounded"
        >
          {Object.entries(scenarios).map(([key, scenario]) => (
            <option key={key} value={key}>{scenario.name}</option>
          ))}
        </select>
        <button onClick={() => setIsPlaying(!isPlaying)} className="mr-2 p-2 border rounded">
          {isPlaying ? <Pause /> : <Play />}
        </button>
        <button onClick={resetDemo} className="p-2 border rounded">
          <RotateCcw />
        </button>
      </div>
      <p className="mb-4">{scenarios[currentScenario].description}</p>
      <div className="flex space-x-4 mb-4 relative">
        {Object.entries(nodes).map(([nodeName, events]) => (
          <Node key={nodeName} name={nodeName} events={events} />
        ))}
        {activeMessage && <Message from={activeMessage.from} to={activeMessage.to} active={true} />}
      </div>
      <div className="mt-4 p-4 bg-gray-100 rounded">
        <h3 className="font-bold mb-2">Step Explanation:</h3>
        <p>{currentStep >= 0 ? scenarios[currentScenario].steps[currentStep].explanation : "Click play to start the demonstration."}</p>
      </div>
      <div className="mt-4">
        <div className="flex items-center mb-2">
          <div className="w-4 h-4 bg-blue-200 mr-2"></div>
          <span>Normal event execution</span>
        </div>
        <div className="flex items-center">
          <div className="w-4 h-4 bg-yellow-200 mr-2"></div>
          <span>Out-of-order or unexpected event execution</span>
        </div>
      </div>
      <div className="mt-4">
        <ArrowDownRight className="inline mr-2" />
        <span>Expected causal order: A1 → B1, B2 → A2, B3 → C1, C3 → A3</span>
      </div>
    </div>
  );
};

export default CausalOrderViz;