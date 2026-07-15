import React, { useState } from 'react';
import { ChevronDown, CheckCircle2, AlertTriangle, XCircle, Award, TrendingUp } from 'lucide-react';

const statusConfig = {
  excellent: { color: 'var(--color-success)', icon: Award, label: 'Excellent' },
  good: { color: 'var(--color-success)', icon: CheckCircle2, label: 'Good' },
  warning: { color: 'var(--color-warning)', icon: AlertTriangle, label: 'Needs Work' },
  critical: { color: 'var(--color-danger)', icon: XCircle, label: 'Critical' },
};

function SectionCard({ section, index }) {
  const [expanded, setExpanded] = useState(false);
  const config = statusConfig[section.status] || statusConfig.warning;
  const StatusIcon = config.icon;

  const getBarColor = (score) => {
    if (score >= 80) return 'var(--color-success)';
    if (score >= 60) return 'var(--color-warning)';
    return 'var(--color-danger)';
  };

  return (
    <div
      className={`section-card ${expanded ? 'expanded' : ''}`}
      style={{ animationDelay: `${index * 0.08}s` }}
    >
      <div className="section-card-header" onClick={() => setExpanded(!expanded)}>
        <div className="section-card-left">
          <div className="section-status-icon" style={{ color: config.color }}>
            <StatusIcon size={18} />
          </div>
          <div className="section-card-info">
            <span className="section-card-name">{section.section_name}</span>
            <span className="section-card-verdict">{section.verdict}</span>
          </div>
        </div>
        <div className="section-card-right">
          <div className="section-score-pill" style={{ color: config.color, borderColor: `${config.color}30` }}>
            {section.score}%
          </div>
          <ChevronDown
            size={18}
            className={`section-chevron ${expanded ? 'rotated' : ''}`}
            style={{ color: 'var(--text-muted)' }}
          />
        </div>
      </div>

      {/* Score bar */}
      <div className="section-score-bar-container">
        <div className="section-score-bar-bg">
          <div
            className="section-score-bar-fill"
            style={{
              width: `${section.score}%`,
              backgroundColor: getBarColor(section.score),
              boxShadow: `0 0 8px ${getBarColor(section.score)}40`
            }}
          />
        </div>
      </div>

      {/* Expandable Body */}
      {expanded && (
        <div className="section-card-body">
          {/* Strengths */}
          {section.strengths && section.strengths.length > 0 && (
            <div className="section-list-group">
              <div className="section-list-title strengths">
                <CheckCircle2 size={14} />
                Strengths
              </div>
              {section.strengths.map((item, i) => (
                <div key={i} className="section-list-item strengths">
                  <span className="section-list-bullet">✓</span>
                  <span>{item}</span>
                </div>
              ))}
            </div>
          )}

          {/* Improvements */}
          {section.improvements && section.improvements.length > 0 && (
            <div className="section-list-group">
              <div className="section-list-title improvements">
                <TrendingUp size={14} />
                Improvements
              </div>
              {section.improvements.map((item, i) => (
                <div key={i} className="section-list-item improvements">
                  <span className="section-list-bullet">→</span>
                  <span>{item}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default function SectionBreakdown({ sections = [] }) {
  if (!sections || sections.length === 0) {
    return (
      <div style={{ color: 'var(--text-muted)', fontSize: '14px', textAlign: 'center', padding: '32px' }}>
        No section breakdown data available.
      </div>
    );
  }

  // Calculate average score
  const avgScore = Math.round(sections.reduce((sum, s) => sum + s.score, 0) / sections.length);

  return (
    <div>
      {/* Overview bar */}
      <div className="section-overview-bar">
        <div className="section-overview-left">
          <span className="section-overview-label">Section Analysis</span>
          <span className="section-overview-count">{sections.length} sections analyzed</span>
        </div>
        <div className="section-overview-avg">
          <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Avg Score</span>
          <span style={{
            fontSize: '20px',
            fontWeight: 800,
            fontFamily: 'var(--font-heading)',
            color: avgScore >= 70 ? 'var(--color-success)' : (avgScore >= 50 ? 'var(--color-warning)' : 'var(--color-danger)')
          }}>
            {avgScore}%
          </span>
        </div>
      </div>

      {/* Section Cards */}
      <div className="section-cards-container">
        {sections.map((section, index) => (
          <SectionCard key={index} section={section} index={index} />
        ))}
      </div>
    </div>
  );
}
