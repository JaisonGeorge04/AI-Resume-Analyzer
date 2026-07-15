import React, { useEffect, useState } from 'react';
import { Cpu } from 'lucide-react';
import { checkApiHealth } from '../utils/api';

export default function Header() {
  const [status, setStatus] = useState('checking'); // 'checking', 'online', 'offline'
  const [backendMode, setBackendMode] = useState('');

  useEffect(() => {
    async function getStatus() {
      const res = await checkApiHealth();
      if (res.status === 'healthy') {
        setStatus('online');
        setBackendMode(res.mode);
      } else {
        setStatus('offline');
      }
    }
    getStatus();
    // Poll status every 15 seconds
    const interval = setInterval(getStatus, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="app-header">
      <div className="logo-container">
        <Cpu size={32} className="logo-icon" />
        <div style={{ display: 'flex', flexDirection: 'column' }}>
          <h1 className="logo-text">AI RESUME ANALYZER</h1>
          <span style={{ fontSize: '11px', color: 'var(--text-muted)', fontWeight: 600, letterSpacing: '1px' }}>
            ATS OPTIMIZER & FEEDBACK ENGINE
          </span>
        </div>
      </div>
      <div className="api-status">
        <span className={`status-indicator ${status}`} />
        <span>
          {status === 'checking' && 'Checking API...'}
          {status === 'online' && `API Online (${backendMode || 'Mock'})`}
          {status === 'offline' && 'API Offline'}
        </span>
      </div>
    </header>
  );
}
