import React, { useRef, useState } from 'react';
import { UploadCloud, FileText, X } from 'lucide-react';

export default function FileUpload({ file, setFile }) {
  const [dragActive, setDragActive] = useState(false);
  const inputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const validateAndSetFile = (selectedFile) => {
    if (!selectedFile) return;
    const name = selectedFile.name.toLowerCase();
    if (name.endsWith('.pdf') || name.endsWith('.docx') || name.endsWith('.doc')) {
      setFile(selectedFile);
    } else {
      alert("Unsupported file format! Please upload a PDF or Word document (.docx, .doc).");
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      validateAndSetFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  const onButtonClick = () => {
    inputRef.current.click();
  };

  return (
    <div className="form-group">
      <label className="form-label">Resume Document</label>
      
      {!file ? (
        <div 
          className={`upload-zone ${dragActive ? 'drag-active' : ''}`}
          onDragEnter={handleDrag}
          onDragOver={handleDrag}
          onDragLeave={handleDrag}
          onDrop={handleDrop}
          onClick={onButtonClick}
        >
          <input 
            ref={inputRef}
            type="file" 
            className="file-input" 
            style={{ display: 'none' }}
            onChange={handleChange}
            accept=".pdf,.docx,.doc"
          />
          <UploadCloud size={40} className="upload-icon" />
          <div>
            <p className="upload-text-bold">Drag and drop your resume here</p>
            <p className="upload-text-small" style={{ marginTop: '4px' }}>PDF or Word DOCX (max 5MB)</p>
          </div>
          <button 
            type="button" 
            style={{
              background: 'rgba(255,255,255,0.05)',
              border: '1px solid var(--border-color)',
              color: '#fff',
              fontSize: '12px',
              fontWeight: 600,
              padding: '6px 14px',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Browse Files
          </button>
        </div>
      ) : (
        <div className="selected-file-badge">
          <div className="file-info">
            <FileText size={18} style={{ color: 'var(--color-primary)' }} />
            <span className="file-name" title={file.name}>{file.name}</span>
            <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
              ({(file.size / 1024).toFixed(0)} KB)
            </span>
          </div>
          <button 
            type="button" 
            className="btn-remove-file"
            onClick={() => setFile(null)}
            title="Remove file"
          >
            <X size={16} />
          </button>
        </div>
      )}
    </div>
  );
}
