import React, { useState, useRef } from 'react';
import { UploadCloud, FileText, X, Link as LinkIcon, Loader } from 'lucide-react';
import { scrapeJobDescription } from '../utils/api';

export default function JobDescription({ value, onChange, fileValue, onFileChange }) {
  const [mode, setMode] = useState('text'); // 'text', 'file', or 'url'
  const [url, setUrl] = useState('');
  const [isScraping, setIsScraping] = useState(false);
  const fileInputRef = useRef(null);

  const handleScrape = async () => {
    if (!url) return;
    setIsScraping(true);
    try {
      const data = await scrapeJobDescription(url);
      if (data.job_description) {
        onChange(data.job_description);
        setMode('text'); // Switch to text mode to show the result
        setUrl(''); // Clear url
      }
    } catch (err) {
      alert(err.message || "Failed to scrape job description. Please check the URL and try again.");
    } finally {
      setIsScraping(false);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      const name = selectedFile.name.toLowerCase();

      // Check if filename contains resume keywords
      const resumeKeywords = ['resume', 'cv', 'curriculum', 'vitae', 'portfolio'];
      const isResumeFile = resumeKeywords.some(keyword => name.includes(keyword));
      if (isResumeFile) {
        alert("It looks like you uploaded a Resume in the Job Description field. Please upload the Job Description here instead.");
        return;
      }

      if (name.endsWith('.pdf') || name.endsWith('.docx') || name.endsWith('.doc') || name.endsWith('.txt')) {
        onFileChange(selectedFile);
      } else {
        alert("Unsupported file format! Please upload a PDF, DOCX, or TXT file.");
      }
    }
  };

  const triggerFileSelect = () => {
    fileInputRef.current.click();
  };

  return (
    <div className="form-group job-description-group">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
        <label className="form-label" style={{ margin: 0 }}>
          Target Job Description <span style={{ color: 'var(--text-muted)', fontWeight: 400 }}>(Optional)</span>
        </label>
        
        {/* Toggle Switch */}
        <div className="jd-toggle-container" style={{ display: 'flex', background: 'rgba(255, 255, 255, 0.03)', padding: '2px', borderRadius: '6px', border: '1px solid var(--border-color)' }}>
          <button
            type="button"
            className={`jd-toggle-btn ${mode === 'text' ? 'active' : ''}`}
            onClick={() => {
              setMode('text');
              onFileChange(null);
            }}
            style={{
              padding: '4px 8px',
              fontSize: '11px',
              fontWeight: 600,
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              background: mode === 'text' ? 'var(--color-primary)' : 'transparent',
              color: '#fff',
              transition: 'var(--transition-fast)'
            }}
          >
            Paste Text
          </button>
          <button
            type="button"
            className={`jd-toggle-btn ${mode === 'file' ? 'active' : ''}`}
            onClick={() => {
              setMode('file');
              onChange('');
            }}
            style={{
              padding: '4px 8px',
              fontSize: '11px',
              fontWeight: 600,
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              background: mode === 'file' ? 'var(--color-primary)' : 'transparent',
              color: '#fff',
              transition: 'var(--transition-fast)'
            }}
          >
            Upload File
          </button>
          <button
            type="button"
            className={`jd-toggle-btn ${mode === 'url' ? 'active' : ''}`}
            onClick={() => {
              setMode('url');
              onFileChange(null);
            }}
            style={{
              padding: '4px 8px',
              fontSize: '11px',
              fontWeight: 600,
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              background: mode === 'url' ? 'var(--color-primary)' : 'transparent',
              color: '#fff',
              transition: 'var(--transition-fast)'
            }}
          >
            Scrape URL
          </button>
        </div>
      </div>

      {mode === 'url' ? (
        <div className="jd-url-zone" style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          <div style={{ display: 'flex', gap: '8px' }}>
            <input
              type="url"
              className="textarea-field"
              placeholder="https://www.linkedin.com/jobs/view/..."
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              style={{ minHeight: '40px', padding: '10px 14px', flex: 1 }}
            />
            <button
              type="button"
              onClick={handleScrape}
              disabled={!url || isScraping}
              style={{
                padding: '0 16px',
                background: 'var(--color-primary)',
                color: 'white',
                border: 'none',
                borderRadius: 'var(--radius-sm)',
                fontWeight: 600,
                cursor: (!url || isScraping) ? 'not-allowed' : 'pointer',
                opacity: (!url || isScraping) ? 0.7 : 1,
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
              }}
            >
              {isScraping ? <Loader size={16} className="spin" /> : <LinkIcon size={16} />}
              {isScraping ? 'Scraping...' : 'Fetch'}
            </button>
          </div>
          <p style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
            Paste a link to a job posting. We'll extract the job description and switch back to text mode.
          </p>
        </div>
      ) : mode === 'text' ? (
        <textarea
          id="job-description-input"
          className="textarea-field"
          placeholder="Paste the target job description here to run a keyword match and get customized alignment recommendations..."
          value={value}
          onChange={(e) => onChange(e.target.value)}
        />
      ) : (
        <div className="jd-file-zone">
          <input
            ref={fileInputRef}
            type="file"
            onChange={handleFileChange}
            accept=".pdf,.docx,.doc,.txt"
            style={{ display: 'none' }}
          />
          {!fileValue ? (
            <div 
              className="jd-upload-placeholder" 
              onClick={triggerFileSelect}
              style={{
                border: '1px dashed var(--border-color)',
                borderRadius: 'var(--radius-sm)',
                padding: '20px',
                textAlign: 'center',
                cursor: 'pointer',
                background: 'rgba(255, 255, 255, 0.01)',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                gap: '8px',
                transition: 'var(--transition-fast)'
              }}
            >
              <UploadCloud size={28} style={{ color: 'var(--text-muted)' }} />
              <div>
                <p style={{ fontSize: '13px', fontWeight: 600, color: '#fff' }}>Click to upload job description</p>
                <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '2px' }}>PDF, DOCX, or TXT</p>
              </div>
            </div>
          ) : (
            <div 
              className="selected-file-badge"
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                padding: '12px',
                background: 'rgba(255, 255, 255, 0.02)',
                border: '1px solid var(--border-color)',
                borderRadius: 'var(--radius-sm)'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', overflow: 'hidden' }}>
                <FileText size={16} style={{ color: 'var(--color-primary)', flexShrink: 0 }} />
                <span 
                  style={{ fontSize: '12px', fontWeight: 500, color: '#fff', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', maxWidth: '220px' }}
                  title={fileValue.name}
                >
                  {fileValue.name}
                </span>
                <span style={{ fontSize: '10px', color: 'var(--text-muted)', flexShrink: 0 }}>
                  ({(fileValue.size / 1024).toFixed(0)} KB)
                </span>
              </div>
              <button
                type="button"
                onClick={() => onFileChange(null)}
                style={{
                  background: 'none',
                  border: 'none',
                  color: 'var(--text-muted)',
                  cursor: 'pointer',
                  padding: '2px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}
              >
                <X size={14} />
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
