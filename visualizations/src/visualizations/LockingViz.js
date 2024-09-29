import React, { useState, useEffect } from 'react';
import { ArrowLeft, ArrowRight, Play, Pause, RotateCcw, Lock } from 'lucide-react';

const TransactionStep = ({ type, value, locked, tooltip }) => (
  <div className={`flex items-center justify-between p-2 mb-1 rounded ${type === 'read' ? 'bg-blue-100' : 'bg-green-100'} relative group`}>
    <span>{type === 'read' ? 'Read' : 'Write'}: {value}</span>
    {locked && <Lock size={16} className="text-red-500" />}
    <div className="absolute invisible group-hover:visible bg-gray-800 text-white p-2 rounded text-sm -top-8 left-0 right-0 mx-auto w-48 z-10">
      {tooltip}
    </div>
  </div>
);

const Transaction = ({ id, steps, locked }) => (
  <div className="border p-2 mb-2">
    <h3 className="font-bold mb-2">Transaction {id}</h3>
    {steps.map((step, index) => (
      <TransactionStep key={index} {...step} locked={locked} />
    ))}
  </div>
);

const DatabaseState = ({ value }) => (
  <div className="mt-2 p-2 bg-yellow-100 rounded">
    <strong>Database State:</strong> A = {value}
  </div>
);

const LockingViz = () => {
  const [step, setStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [speed, setSpeed] = useState(1000); // milliseconds
  const maxSteps = 5;

  const next = () => setStep(prev => Math.min(prev + 1, maxSteps));
  const prev = () => setStep(prev => Math.max(prev - 1, 0));
  const reset = () => {
    setStep(0);
    setIsPlaying(false);
  };

  useEffect(() => {
    let timer;
    if (isPlaying && step < maxSteps) {
      timer = setTimeout(next, speed);
    } else if (step >= maxSteps) {
      setIsPlaying(false);
    }
    return () => clearTimeout(timer);
  }, [isPlaying, step, speed]);

  const scenarios = [
    { // Step 0
      twopl: [],
      ssi: [],
      dbState: { twopl: 100, ssi: 100 },
      commentary: "Initial state. Database value A = 100."
    },
    { // Step 1
      twopl: [{ id: 1, steps: [{ type: 'read', value: 'A = 100', locked: true, tooltip: "T1 acquires a read lock" }] }],
      ssi: [{ id: 1, steps: [{ type: 'read', value: 'A = 100', tooltip: "T1 reads from its snapshot" }] }],
      dbState: { twopl: 100, ssi: 100 },
      commentary: "T1 starts and reads the value of A. In 2PL, it acquires a lock. In SSI, it reads from its snapshot."
    },
    { // Step 2
      twopl: [
        { id: 1, steps: [{ type: 'read', value: 'A = 100', locked: true, tooltip: "T1 holds the lock" }, { type: 'write', value: 'A = 150', locked: true, tooltip: "T1 writes under lock" }] },
        { id: 2, steps: [{ type: 'read', value: 'Waiting for lock...', tooltip: "T2 waits for T1's lock" }] }
      ],
      ssi: [
        { id: 1, steps: [{ type: 'read', value: 'A = 100', tooltip: "T1's snapshot" }, { type: 'write', value: 'A = 150', tooltip: "T1 writes to its local copy" }] },
        { id: 2, steps: [{ type: 'read', value: 'A = 100', tooltip: "T2 reads from its own snapshot" }] }
      ],
      dbState: { twopl: 100, ssi: 100 },
      commentary: "T1 writes A = 150. T2 tries to read. In 2PL, T2 waits. In SSI, T2 reads the old value from its snapshot."
    },
    { // Step 3
      twopl: [
        { id: 1, steps: [{ type: 'read', value: 'A = 100', locked: false, tooltip: "T1 releases lock" }, { type: 'write', value: 'A = 150', locked: false, tooltip: "T1 commits" }] },
        { id: 2, steps: [{ type: 'read', value: 'A = 150', locked: true, tooltip: "T2 acquires lock and reads new value" }] }
      ],
      ssi: [
        { id: 1, steps: [{ type: 'read', value: 'A = 100', tooltip: "T1's initial read" }, { type: 'write', value: 'A = 150', tooltip: "T1 commits" }] },
        { id: 2, steps: [{ type: 'read', value: 'A = 100', tooltip: "T2's snapshot is unchanged" }, { type: 'write', value: 'A = 200', tooltip: "T2 writes to its local copy" }] }
      ],
      dbState: { twopl: 150, ssi: 150 },
      commentary: "T1 commits. In 2PL, T2 can now read the new value. In SSI, T2 continues with its old snapshot."
    },
    { // Step 4
      twopl: [
        { id: 1, steps: [{ type: 'read', value: 'A = 100', locked: false }, { type: 'write', value: 'A = 150', locked: false }] },
        { id: 2, steps: [{ type: 'read', value: 'A = 150', locked: true }, { type: 'write', value: 'A = 200', locked: true, tooltip: "T2 writes under lock" }] }
      ],
      ssi: [
        { id: 1, steps: [{ type: 'read', value: 'A = 100' }, { type: 'write', value: 'A = 150' }, { type: 'commit', value: 'Success', tooltip: "T1 committed successfully" }] },
        { id: 2, steps: [{ type: 'read', value: 'A = 100' }, { type: 'write', value: 'A = 200' }, { type: 'commit', value: 'Conflict detected!', tooltip: "T2 detects write-write conflict" }] }
      ],
      dbState: { twopl: 150, ssi: 150 },
      commentary: "T2 tries to commit. In 2PL, it succeeds. In SSI, a conflict is detected because T1 and T2 both tried to update A."
    },
    { // Step 5
      twopl: [
        { id: 1, steps: [{ type: 'read', value: 'A = 100', locked: false }, { type: 'write', value: 'A = 150', locked: false }] },
        { id: 2, steps: [{ type: 'read', value: 'A = 150', locked: false }, { type: 'write', value: 'A = 200', locked: false }] }
      ],
      ssi: [
        { id: 1, steps: [{ type: 'read', value: 'A = 100' }, { type: 'write', value: 'A = 150' }, { type: 'commit', value: 'Success' }] },
        { id: 2, steps: [{ type: 'read', value: 'A = 100' }, { type: 'write', value: 'A = 200' }, { type: 'abort', value: 'Transaction aborted', tooltip: "T2 must abort due to conflict" }] }
      ],
      dbState: { twopl: 200, ssi: 150 },
      commentary: "Final state. In 2PL, both transactions committed sequentially. In SSI, T2 had to abort due to a conflict."
    }
  ];

  return (
    <div className="p-4 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">LockingViz: 2PL vs SSI Comparison</h1>
      
      <div className="mb-4 flex justify-between items-center bg-gray-100 p-2 rounded">
        <button onClick={prev} className="bg-blue-500 text-white px-4 py-2 rounded" disabled={step === 0}>
          <ArrowLeft size={16} />
        </button>
        <button onClick={() => setIsPlaying(!isPlaying)} className="bg-green-500 text-white px-4 py-2 rounded">
          {isPlaying ? <Pause size={16} /> : <Play size={16} />}
        </button>
        <input 
          type="range" 
          min="200" 
          max="2000" 
          value={speed} 
          onChange={(e) => setSpeed(Number(e.target.value))}
          className="w-32"
        />
        <button onClick={next} className="bg-blue-500 text-white px-4 py-2 rounded" disabled={step === maxSteps}>
          <ArrowRight size={16} />
        </button>
        <button onClick={reset} className="bg-gray-500 text-white px-4 py-2 rounded">
          <RotateCcw size={16} />
        </button>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-4">
        <div>
          <h2 className="text-xl font-semibold mb-2">Two-Phase Locking (2PL)</h2>
          <p className="mb-2">Pessimistic approach: locks resources before accessing</p>
          <div className="border p-2 mb-2">
            {scenarios[step].twopl.map((tx, index) => (
              <Transaction key={index} {...tx} />
            ))}
            <DatabaseState value={scenarios[step].dbState.twopl} />
          </div>
        </div>
        
        <div>
          <h2 className="text-xl font-semibold mb-2">Serializable Snapshot Isolation (SSI)</h2>
          <p className="mb-2">Optimistic approach: detects conflicts at commit time</p>
          <div className="border p-2 mb-2">
            {scenarios[step].ssi.map((tx, index) => (
              <Transaction key={index} {...tx} />
            ))}
            <DatabaseState value={scenarios[step].dbState.ssi} />
          </div>
        </div>
      </div>
      
      <div className="mb-4 p-2 bg-gray-100 rounded">
        <strong>Commentary:</strong> {scenarios[step].commentary}
      </div>

      <div className="mt-4">
        <h2 className="text-xl font-semibold mb-2">Key Differences</h2>
        <ul className="list-disc pl-5">
          <li>2PL uses locks to prevent conflicts, while SSI allows transactions to proceed without blocking</li>
          <li>2PL may lead to waiting and potential deadlocks, while SSI may lead to more transaction aborts</li>
          <li>2PL provides strong isolation but can have performance issues, while SSI offers better concurrency</li>
          <li>SSI is generally more scalable for read-heavy workloads</li>
        </ul>
      </div>
    </div>
  );
};

export default LockingViz;