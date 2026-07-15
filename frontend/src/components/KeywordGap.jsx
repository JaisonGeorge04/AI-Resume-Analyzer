import React from 'react';
import { CheckCircle2, AlertCircle, PlusCircle } from 'lucide-react';

export default function KeywordGap({ keywords = {} }) {
  const { matching = [], missing = [], recommended = [] } = keywords;

  const hasKeywords = matching.length > 0 || missing.length > 0 || recommended.length > 0;

  if (!hasKeywords) {
    return (
      <div style={{ color: 'var(--text-muted)', fontSize: '14px', textAlign: 'center', padding: '24px 0' }}>
        No keyword data available. Provide a job description to trigger analysis.
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      
      {matching.length > 0 && (
        <div>
          <h3 className="keywords-group-title matching">
            <CheckCircle2 size={16} />
            Matching Keywords ({matching.length})
          </h3>
          <div className="keyword-pills-container">
            {matching.map((kw, i) => (
              <span key={i} className="keyword-pill matching">
                {kw}
              </span>
            ))}
          </div>
        </div>
      )}

      {missing.length > 0 && (
        <div>
          <h3 className="keywords-group-title missing">
            <AlertCircle size={16} />
            Missing Target Keywords ({missing.length})
          </h3>
          <div className="keyword-pills-container">
            {missing.map((kw, i) => (
              <span key={i} className="keyword-pill missing">
                + {kw}
              </span>
            ))}
          </div>
        </div>
      )}

      {recommended.length > 0 && (
        <div>
          <h3 className="keywords-group-title recommended">
            <PlusCircle size={16} />
            Recommended Skills to Add ({recommended.length})
          </h3>
          <div className="keyword-pills-container">
            {recommended.map((kw, i) => (
              <span key={i} className="keyword-pill recommended">
                {kw}
              </span>
            ))}
          </div>
        </div>
      )}

    </div>
  );
}
