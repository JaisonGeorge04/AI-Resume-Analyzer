import React, { useEffect, useState } from 'react';

const STEPS = [
  { id: 1, text: 'Uploading resume and parsing document formatting...' },
  { id: 2, text: 'Extracting clean text & identifying sections...' },
  { id: 3, text: 'Comparing candidate skills with target description...' },
  { id: 4, text: 'Running ATS parsing simulations...' },
  { id: 5, text: 'Optimizing experience metrics & drafting feedback...' }
];

export default function LoadingState() {
  const [currentStepIdx, setCurrentStepIdx] = useState(0);

  useEffect(() => {
    const intervals = [1200, 1800, 1500, 1500, 2000];
    let step = 0;
    
    function nextStep() {
      if (step < STEPS.length - 1) {
        step++;
        setCurrentStepIdx(step);
        setTimeout(nextStep, intervals[step]);
      }
    }
    
    const timeout = setTimeout(nextStep, intervals[0]);
    return () => clearTimeout(timeout);
  }, []);

  return (
    <div className="glass-panel text-center" style={{ padding: '60px 24px' }}>
      <div className="loading-container">
        <div className="spinner" />
        <div>
          <h2 style={{ fontFamily: 'var(--font-heading)', fontSize: '20px', fontWeight: 700, marginBottom: '8px' }}>
            Analyzing Your Resume
          </h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '14px' }}>
            Our AI engine is evaluating your document structure and skills...
          </p>
        </div>
        
        <div className="loading-steps">
          {STEPS.map((step, idx) => {
            let statusClass = 'pending';
            if (idx === currentStepIdx) {
              statusClass = 'active';
            } else if (idx < currentStepIdx) {
              statusClass = 'completed';
            }
            
            return (
              <div key={step.id} className={`loading-step ${statusClass}`}>
                <div className="step-bullet">
                  {idx < currentStepIdx ? '✓' : ''}
                </div>
                <span>{step.text}</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
