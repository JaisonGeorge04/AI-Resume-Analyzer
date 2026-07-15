import React from 'react';

export default function JobDescription({ value, onChange }) {
  return (
    <div className="form-group">
      <label className="form-label" htmlFor="job-description-input">
        Target Job Description <span style={{ color: 'var(--text-muted)', fontWeight: 400 }}>(Optional)</span>
      </label>
      <textarea
        id="job-description-input"
        className="textarea-field"
        placeholder="Paste the target job description here to run a keyword match and get customized alignment recommendations..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  );
}
