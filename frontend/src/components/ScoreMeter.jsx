import React, { useEffect, useState } from 'react';

export default function ScoreMeter({ score = 0 }) {
  const [animatedScore, setAnimatedScore] = useState(0);
  
  // Radius of the SVG circle
  const radius = 80;
  const stroke = 8;
  const normalizedRadius = radius - stroke * 2;
  const circumference = normalizedRadius * 2 * Math.PI;
  
  // Dash offset represents how much of the stroke is hidden
  const strokeDashoffset = circumference - (animatedScore / 100) * circumference;

  useEffect(() => {
    // Animate from 0 to the target score
    const duration = 1200; // ms
    const startTime = performance.now();

    function animate(currentTime) {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      
      // Easing function outQuad
      const easedProgress = progress * (2 - progress);
      setAnimatedScore(Math.round(easedProgress * score));

      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    }

    requestAnimationFrame(animate);
  }, [score]);

  // Color helper based on score
  const getScoreColor = (val) => {
    if (val >= 80) return 'var(--color-success)';
    if (val >= 60) return 'var(--color-warning)';
    return 'var(--color-danger)';
  };

  const getScoreCategory = (val) => {
    if (val >= 80) return { label: 'Good Match', class: 'good' };
    if (val >= 60) return { label: 'Needs Improvement', class: 'warning' };
    return { label: 'Poor Match', class: 'critical' };
  };

  const currentColor = getScoreColor(score);
  const category = getScoreCategory(score);

  return (
    <div className="score-meter-container">
      <svg className="gauge-svg" viewBox={`0 0 ${radius * 2} ${radius * 2}`}>
        {/* Background track circle */}
        <circle
          className="gauge-bg"
          r={normalizedRadius}
          cx={radius}
          cy={radius}
        />
        {/* Animated fill circle */}
        <circle
          className="gauge-fill"
          stroke={currentColor}
          r={normalizedRadius}
          cx={radius}
          cy={radius}
          style={{
            strokeDasharray: `${circumference} ${circumference}`,
            strokeDashoffset: strokeDashoffset,
            // Add a subtle drop shadow to the fill ring
            filter: `drop-shadow(0 0 4px ${currentColor}50)`
          }}
        />
      </svg>
      <div className="gauge-text-container">
        <span className="gauge-number" style={{ color: currentColor }}>{animatedScore}</span>
        <span className="gauge-label">Score</span>
      </div>
    </div>
  );
}
export { ScoreMeter };
