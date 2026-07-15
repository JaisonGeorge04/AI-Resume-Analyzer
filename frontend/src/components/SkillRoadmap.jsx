import React, { useState } from 'react';
import { ChevronDown, BookOpen, Wrench, Award, Clock, ExternalLink, Flame, Zap, Target } from 'lucide-react';

const priorityConfig = {
  high: { color: '#ef4444', bg: 'rgba(239, 68, 68, 0.12)', border: 'rgba(239, 68, 68, 0.25)', icon: Flame, label: 'High Priority' },
  medium: { color: '#f59e0b', bg: 'rgba(245, 158, 11, 0.12)', border: 'rgba(245, 158, 11, 0.25)', icon: Zap, label: 'Medium Priority' },
  low: { color: '#10b981', bg: 'rgba(16, 185, 129, 0.12)', border: 'rgba(16, 185, 129, 0.25)', icon: Target, label: 'Low Priority' },
};

const stepTypeConfig = {
  course: { icon: BookOpen, label: 'Course', color: 'var(--color-primary)' },
  project: { icon: Wrench, label: 'Project', color: 'var(--color-success)' },
  certification: { icon: Award, label: 'Cert', color: '#a855f7' },
};

function SkillCard({ skill, index }) {
  const [expanded, setExpanded] = useState(false);
  const priority = priorityConfig[skill.priority] || priorityConfig.medium;
  const PriorityIcon = priority.icon;

  return (
    <div
      className={`roadmap-card ${expanded ? 'expanded' : ''}`}
      style={{ animationDelay: `${index * 0.1}s` }}
    >
      {/* Card Header */}
      <div className="roadmap-card-header" onClick={() => setExpanded(!expanded)}>
        <div className="roadmap-header-left">
          <div className="roadmap-skill-name">{skill.skill_name}</div>
          <div className="roadmap-header-meta">
            <span
              className="roadmap-priority-badge"
              style={{ color: priority.color, background: priority.bg, borderColor: priority.border }}
            >
              <PriorityIcon size={12} />
              {priority.label}
            </span>
            <span className="roadmap-duration-badge">
              <Clock size={12} />
              {skill.estimated_weeks} weeks
            </span>
          </div>
        </div>
        <ChevronDown
          size={18}
          className={`section-chevron ${expanded ? 'rotated' : ''}`}
          style={{ color: 'var(--text-muted)', flexShrink: 0 }}
        />
      </div>

      {/* Why Important */}
      <div className="roadmap-why">
        <span style={{ fontWeight: 600, color: 'var(--color-primary)', fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
          Why it matters:
        </span>{' '}
        {skill.why_important}
      </div>

      {/* Expanded: Learning Path Timeline */}
      {expanded && (
        <div className="roadmap-card-body">
          <div className="roadmap-timeline">
            {skill.learning_path && skill.learning_path.map((step, i) => {
              const typeConf = stepTypeConfig[step.type] || stepTypeConfig.course;
              const StepIcon = typeConf.icon;
              const isLast = i === skill.learning_path.length - 1;

              return (
                <div key={i} className="timeline-step">
                  {/* Timeline connector */}
                  <div className="timeline-connector">
                    <div
                      className="timeline-dot"
                      style={{ borderColor: typeConf.color, boxShadow: `0 0 8px ${typeConf.color}40` }}
                    >
                      <span style={{ fontFamily: 'var(--font-heading)', fontSize: '11px', fontWeight: 700, color: typeConf.color }}>
                        {step.step}
                      </span>
                    </div>
                    {!isLast && <div className="timeline-line" />}
                  </div>

                  {/* Step Content */}
                  <div className="timeline-content">
                    <div className="timeline-title-row">
                      <span className="timeline-title">{step.title}</span>
                      <span
                        className="timeline-type-badge"
                        style={{ color: typeConf.color, background: `${typeConf.color}15`, borderColor: `${typeConf.color}30` }}
                      >
                        <StepIcon size={11} />
                        {typeConf.label}
                      </span>
                    </div>
                    <div className="timeline-details">
                      <span className="timeline-resource">
                        {step.resource}
                        {step.url && (
                          <a
                            href={step.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="timeline-link"
                          >
                            <ExternalLink size={12} />
                            Open
                          </a>
                        )}
                      </span>
                      <span className="timeline-duration">
                        <Clock size={12} />
                        {step.duration}
                      </span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Certifications */}
          {skill.certifications && skill.certifications.length > 0 && (
            <div className="roadmap-certs">
              <div className="roadmap-certs-title">
                <Award size={14} style={{ color: '#a855f7' }} />
                Recommended Certifications
              </div>
              <div className="roadmap-certs-list">
                {skill.certifications.map((cert, i) => (
                  <span key={i} className="roadmap-cert-badge">
                    <Award size={12} />
                    {cert}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default function SkillRoadmap({ skills = [] }) {
  if (!skills || skills.length === 0) {
    return (
      <div style={{ color: 'var(--text-muted)', fontSize: '14px', textAlign: 'center', padding: '32px' }}>
        No skill gap data available. Upload a resume with a job description for targeted skill recommendations.
      </div>
    );
  }

  // Sort by priority: high first, then medium, then low
  const priorityOrder = { high: 0, medium: 1, low: 2 };
  const sorted = [...skills].sort((a, b) => (priorityOrder[a.priority] || 1) - (priorityOrder[b.priority] || 1));

  const totalWeeks = skills.reduce((sum, s) => sum + (s.estimated_weeks || 0), 0);
  const highCount = skills.filter(s => s.priority === 'high').length;

  return (
    <div>
      {/* Overview bar */}
      <div className="roadmap-overview-bar">
        <div className="roadmap-overview-stat">
          <span className="roadmap-stat-value">{skills.length}</span>
          <span className="roadmap-stat-label">Skills to Learn</span>
        </div>
        <div className="roadmap-overview-divider" />
        <div className="roadmap-overview-stat">
          <span className="roadmap-stat-value" style={{ color: 'var(--color-danger)' }}>{highCount}</span>
          <span className="roadmap-stat-label">High Priority</span>
        </div>
        <div className="roadmap-overview-divider" />
        <div className="roadmap-overview-stat">
          <span className="roadmap-stat-value" style={{ color: 'var(--color-primary)' }}>~{totalWeeks}</span>
          <span className="roadmap-stat-label">Total Weeks</span>
        </div>
      </div>

      {/* Skill Cards */}
      <div className="roadmap-cards-container">
        {sorted.map((skill, index) => (
          <SkillCard key={index} skill={skill} index={index} />
        ))}
      </div>
    </div>
  );
}
