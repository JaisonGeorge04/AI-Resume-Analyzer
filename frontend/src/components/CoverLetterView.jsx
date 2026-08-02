import React, { useState } from 'react';
import { Copy, Check, FileText } from 'lucide-react';

export default function CoverLetterView({ coverLetter }) {
  const [copied, setCopied] = useState(false);

  if (!coverLetter) {
    return (
      <div className="cover-letter-empty" style={{
        padding: '40px',
        textAlign: 'center',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: '12px',
        background: 'rgba(255, 255, 255, 0.01)',
        border: '1px dashed var(--border-color)',
        borderRadius: 'var(--radius-md)'
      }}>
        <FileText size={40} style={{ color: 'var(--text-muted)' }} />
        <p style={{ color: 'var(--text-secondary)', fontSize: '14px' }}>
          No cover letter was generated for this analysis. Ensure a job description was provided.
        </p>
      </div>
    );
  }

  const { greeting, opening, body, closing, sign_off } = coverLetter;

  // Format full letter text for copying
  const fullText = `${greeting || 'Dear Hiring Manager,'}\n\n${opening || ''}\n\n${body || ''}\n\n${closing || ''}\n\n${sign_off || 'Sincerely,\n[Your Name]'}`;

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(fullText);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy text: ', err);
    }
  };

  return (
    <div className="cover-letter-container">
      <div className="cover-letter-header" style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '20px'
      }}>
        <div>
          <h3 style={{ fontSize: '16px', fontWeight: 700, color: '#fff', fontFamily: 'var(--font-heading)' }}>
            AI-Tailored Cover Letter
          </h3>
          <p style={{ fontSize: '12px', color: 'var(--text-muted)', marginTop: '2px' }}>
            Generated based on matching highlights between your resume and target job requirements.
          </p>
        </div>
        <button 
          onClick={handleCopy} 
          className="btn-secondary"
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            padding: '8px 16px',
            fontSize: '13px',
            borderRadius: 'var(--radius-sm)',
            border: '1px solid var(--border-color)',
            background: 'var(--bg-secondary)',
            color: 'var(--text-primary)',
            cursor: 'pointer',
            transition: 'var(--transition-fast)'
          }}
        >
          {copied ? (
            <>
              <Check size={15} style={{ color: 'var(--color-success)' }} />
              <span style={{ color: 'var(--color-success)', fontWeight: 600 }}>Copied!</span>
            </>
          ) : (
            <>
              <Copy size={15} />
              <span>Copy Letter</span>
            </>
          )}
        </button>
      </div>

      <div className="cover-letter-paper">
        <div className="paper-line greeting">{greeting || 'Dear Hiring Manager,'}</div>
        <div className="paper-line paragraph">{opening}</div>
        <div className="paper-line paragraph">{body}</div>
        <div className="paper-line paragraph">{closing}</div>
        <div className="paper-line sign-off">
          {sign_off ? sign_off.split('\n').map((line, idx) => (
            <div key={idx}>{line}</div>
          )) : (
            <>
              <div>Sincerely,</div>
              <div style={{ marginTop: '24px', fontWeight: 500, color: 'var(--text-primary)' }}>[Your Name]</div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
