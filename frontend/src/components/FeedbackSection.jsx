import React, { useState } from 'react';
import { ChevronDown, ChevronUp, AlertTriangle, AlertOctagon, CheckCircle2, Info } from 'lucide-react';

export default function FeedbackSection({ feedback = [] }) {
  const [expandedIndex, setExpandedIndex] = useState(0); // expand first by default

  const toggleExpand = (index) => {
    setExpandedIndex(expandedIndex === index ? null : index);
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'excellent':
        return <CheckCircle2 size={18} style={{ color: 'var(--color-success)' }} />;
      case 'good':
        return <Info size={18} style={{ color: 'var(--color-primary)' }} />;
      case 'warning':
        return <AlertTriangle size={18} style={{ color: 'var(--color-warning)' }} />;
      case 'critical':
        return <AlertOctagon size={18} style={{ color: 'var(--color-danger)' }} />;
      default:
        return <Info size={18} />;
    }
  };

  const getStatusBadgeClass = (status) => {
    switch (status) {
      case 'excellent':
      case 'good':
        return 'score-badge good';
      case 'warning':
        return 'score-badge warning';
      case 'critical':
        return 'score-badge critical';
      default:
        return 'score-badge';
    }
  };

  if (!feedback || feedback.length === 0) {
    return (
      <div style={{ color: 'var(--text-muted)', fontSize: '14px', textAlign: 'center', padding: '24px 0' }}>
        No specific feedback entries generated.
      </div>
    );
  }

  return (
    <div className="feedback-cards-container">
      {feedback.map((item, idx) => {
        const isExpanded = expandedIndex === idx;
        return (
          <div key={idx} className="feedback-card">
            <div className="feedback-header" onClick={() => toggleExpand(idx)}>
              <div className="feedback-header-left">
                {getStatusIcon(item.status)}
                <span className="feedback-category-title">{item.category}</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <span className={getStatusBadgeClass(item.status)} style={{ fontSize: '10px' }}>
                  {item.status}
                </span>
                {isExpanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
              </div>
            </div>
            
            {isExpanded && (
              <div className="feedback-body">
                <p className="feedback-message">{item.message}</p>
                {item.details && item.details.length > 0 && (
                  <ul className="feedback-details-list">
                    {item.details.map((detail, dIdx) => (
                      <li key={dIdx} className="feedback-detail-item">
                        <span className="feedback-detail-bullet">→</span>
                        <span>{detail}</span>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
