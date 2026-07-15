import React, { useState } from 'react';
import { Sparkles, ArrowRight, CornerDownRight, Loader } from 'lucide-react';
import { optimizeBulletPoint } from '../utils/api';

export default function BulletOptimizer({ preOptimizations = [] }) {
  const [customBullet, setCustomBullet] = useState('');
  const [sandboxResult, setSandboxResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleOptimize = async (e) => {
    e.preventDefault();
    if (!customBullet.trim()) return;

    setLoading(true);
    setError(null);
    try {
      const result = await optimizeBulletPoint(customBullet);
      setSandboxResult(result);
    } catch (err) {
      console.error(err);
      setError(err.message || 'Failed to optimize bullet point. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {/* Interactive Sandbox */}
      <div className="bullet-optimizer-card">
        <h3 className="playground-title">
          <Sparkles size={18} style={{ color: 'var(--color-primary)' }} />
          Bullet Point Optimizer Sandbox
        </h3>
        <p className="panel-description" style={{ marginBottom: '14px' }}>
          Paste a weak bullet point from your resume (e.g., "responsible for writing code") to optimize it instantly using the Google XYZ formula.
        </p>

        <form onSubmit={handleOptimize} className="playground-input-row">
          <input
            type="text"
            className="playground-input"
            placeholder="e.g., worked on building components in React"
            value={customBullet}
            onChange={(e) => setCustomBullet(e.target.value)}
            disabled={loading}
          />
          <button
            type="submit"
            className="btn-optimize"
            disabled={loading || !customBullet.trim()}
          >
            {loading ? <Loader className="spinner" style={{ width: '16px', height: '16px' }} /> : 'Optimize'}
          </button>
        </form>

        {error && (
          <div style={{ color: 'var(--color-danger)', fontSize: '13px', marginTop: '8px' }}>
            {error}
          </div>
        )}

        {sandboxResult && (
          <div className="comparison-box">
            <div className="comparison-item original">
              <div className="comparison-label original">Original Bullet</div>
              <div className="comparison-content">{sandboxResult.original}</div>
            </div>
            <div className="comparison-item optimized">
              <div className="comparison-label optimized">Optimized (Google XYZ Format)</div>
              <div className="comparison-content" style={{ fontWeight: 600, color: 'var(--color-success)' }}>
                {sandboxResult.optimized}
              </div>
            </div>
            <div className="comparison-item explanation">
              <div className="comparison-label explanation">Why it is better</div>
              <div className="comparison-content">{sandboxResult.explanation}</div>
            </div>
          </div>
        )}
      </div>

      {/* Pre-Optimized bullets from analysis report */}
      {preOptimizations.length > 0 && (
        <div>
          <h4 style={{ fontSize: '14px', fontWeight: 700, marginBottom: '12px', color: 'var(--text-secondary)' }}>
            Detected Resume Bullet Point Rewrites
          </h4>
          <div className="pre-optimizations-container">
            {preOptimizations.map((item, idx) => (
              <div key={idx} style={{
                background: 'rgba(255, 255, 255, 0.01)',
                border: '1px solid var(--border-color)',
                borderRadius: 'var(--radius-md)',
                padding: '16px',
                display: 'flex',
                flexDirection: 'column',
                gap: '10px'
              }}>
                <div style={{ fontSize: '13px', color: 'var(--text-muted)' }}>
                  <span style={{ color: 'var(--color-danger)', fontWeight: 700 }}>ORIGINAL:</span> "{item.original}"
                </div>
                <div style={{ display: 'flex', gap: '8px', alignItems: 'flex-start' }}>
                  <CornerDownRight size={16} style={{ color: 'var(--color-success)', flexShrink: 0, marginTop: '2px' }} />
                  <div style={{ fontSize: '13.5px', fontWeight: 600, color: 'var(--color-success)' }}>
                    "{item.optimized}"
                  </div>
                </div>
                <div style={{ fontSize: '12.5px', color: 'var(--text-secondary)', paddingLeft: '24px' }}>
                  <span style={{ fontWeight: 600, color: 'var(--color-primary)' }}>Rationale:</span> {item.explanation}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
