import React, { useState } from 'react';
import { Cpu, Send, ClipboardCopy, Award, CheckCircle2, ChevronRight, TrendingUp, AlertTriangle } from 'lucide-react';

// Import components
import Header from './components/Header';
import FileUpload from './components/FileUpload';
import JobDescription from './components/JobDescription';
import ScoreMeter from './components/ScoreMeter';
import KeywordGap from './components/KeywordGap';
import FeedbackSection from './components/FeedbackSection';
import BulletOptimizer from './components/BulletOptimizer';
import LoadingState from './components/LoadingState';
import SectionBreakdown from './components/SectionBreakdown';
import SkillRoadmap from './components/SkillRoadmap';

// Import API caller
import { analyzeResume } from './utils/api';

export default function App() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('keywords'); // 'keywords', 'feedback', 'bullets', 'recommendations'

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await analyzeResume(file, jobDescription);
      setResult(data);
    } catch (err) {
      console.error(err);
      setError(err.message || 'Analysis failed. Make sure the backend server is running.');
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (val) => {
    if (val >= 80) return 'var(--color-success)';
    if (val >= 60) return 'var(--color-warning)';
    return 'var(--color-danger)';
  };

  return (
    <div className="app-container">
      <Header />

      <main className="main-grid">
        {/* Left Column - Inputs */}
        <div className="glass-panel" style={{ height: 'fit-content' }}>
          <h2 className="panel-title">
            <Cpu size={20} style={{ color: 'var(--color-primary)' }} />
            Optimization Settings
          </h2>
          <p className="panel-description">
            Upload your resume and optionally paste the job details to run structural alignment checks.
          </p>

          <form onSubmit={handleAnalyze}>
            <FileUpload file={file} setFile={setFile} />
            <JobDescription value={jobDescription} onChange={setJobDescription} />
            
            {error && (
              <div 
                style={{ 
                  color: 'var(--color-danger)', 
                  background: 'var(--color-danger-glow)',
                  border: '1px solid rgba(239, 68, 68, 0.2)',
                  padding: '12px',
                  borderRadius: 'var(--radius-sm)',
                  fontSize: '13px',
                  marginBottom: '20px',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px'
                }}
              >
                <AlertTriangle size={16} style={{ flexShrink: 0 }} />
                <span>{error}</span>
              </div>
            )}

            <button
              type="submit"
              className="btn-primary"
              disabled={!file || loading}
            >
              <Send size={18} />
              <span>{loading ? 'Analyzing...' : 'Run Diagnostics'}</span>
            </button>
          </form>
        </div>

        {/* Right Column - Results / Empty State */}
        <div className="slide-in-right">
          {loading && <LoadingState />}

          {!loading && !result && (
            <div className="empty-dashboard">
              <ClipboardCopy size={48} className="empty-icon" />
              <div>
                <h3 style={{ fontFamily: 'var(--font-heading)', color: '#fff', fontSize: '18px', fontWeight: 600, marginBottom: '6px' }}>
                  Diagnostics Dashboard
                </h3>
                <p style={{ maxWidth: '400px', fontSize: '14px', lineHeight: 1.5 }}>
                  Select your resume document on the left and click "Run Diagnostics" to generate matching metrics, gap scores, and point-by-point enhancements.
                </p>
              </div>
            </div>
          )}

          {!loading && result && (
            <div className="dashboard-grid">
              {/* Score Header Card */}
              <div className="glass-panel dashboard-header-card">
                <ScoreMeter score={result.score} />
                <div className="summary-text-box">
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <span 
                      className={`score-badge ${
                        result.score >= 80 ? 'good' : (result.score >= 60 ? 'warning' : 'critical')
                      }`}
                    >
                      {result.score >= 80 ? 'Strong Candidate' : (result.score >= 60 ? 'Competitive' : 'Needs Optimization')}
                    </span>
                    <span style={{ fontSize: '13px', color: 'var(--text-muted)', fontWeight: 500 }}>
                      Overall ATS Match
                    </span>
                  </div>
                  <p className="summary-paragraph">{result.summary}</p>
                </div>
              </div>

              {/* Key Metrics Grid */}
              <div className="metrics-row">
                {Object.entries(result.key_metrics || {}).map(([key, metric]) => {
                  const scoreColor = getScoreColor(metric.score);
                  return (
                    <div key={key} className="metric-card">
                      <div className="metric-title-bar">
                        <span>{metric.label}</span>
                        <span style={{ color: scoreColor }}>{metric.score}%</span>
                      </div>
                      <div className="metric-val">{metric.score}</div>
                      <div className="metric-bar-bg">
                        <div 
                          className="metric-bar-fill" 
                          style={{ 
                            width: `${metric.score}%`, 
                            backgroundColor: scoreColor,
                            boxShadow: `0 0 6px ${scoreColor}40`
                          }} 
                        />
                      </div>
                      <span style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px' }}>
                        {metric.description}
                      </span>
                    </div>
                  );
                })}
              </div>

              {/* Tabs Section */}
              <div className="glass-panel" style={{ padding: '24px' }}>
                <div className="tabs-container">
                  <button
                    className={`tab-btn ${activeTab === 'keywords' ? 'active' : ''}`}
                    onClick={() => setActiveTab('keywords')}
                  >
                    Keyword Alignment
                  </button>
                  <button
                    className={`tab-btn ${activeTab === 'sections' ? 'active' : ''}`}
                    onClick={() => setActiveTab('sections')}
                  >
                    Section Analysis
                  </button>
                  <button
                    className={`tab-btn ${activeTab === 'feedback' ? 'active' : ''}`}
                    onClick={() => setActiveTab('feedback')}
                  >
                    Formatting & Details
                  </button>
                  <button
                    className={`tab-btn ${activeTab === 'bullets' ? 'active' : ''}`}
                    onClick={() => setActiveTab('bullets')}
                  >
                    Experience Optimizer
                  </button>
                  <button
                    className={`tab-btn ${activeTab === 'roadmap' ? 'active' : ''}`}
                    onClick={() => setActiveTab('roadmap')}
                  >
                    Skill Roadmap
                  </button>
                  <button
                    className={`tab-btn ${activeTab === 'recommendations' ? 'active' : ''}`}
                    onClick={() => setActiveTab('recommendations')}
                  >
                    Next Steps
                  </button>
                </div>

                <div style={{ marginTop: '24px' }}>
                  {/* Tab Panels */}
                  <div className={`tab-panel ${activeTab === 'keywords' ? 'active' : ''}`}>
                    <KeywordGap keywords={result.keywords} />
                  </div>

                  <div className={`tab-panel ${activeTab === 'sections' ? 'active' : ''}`}>
                    <SectionBreakdown sections={result.section_breakdown} />
                  </div>

                  <div className={`tab-panel ${activeTab === 'feedback' ? 'active' : ''}`}>
                    <FeedbackSection feedback={result.feedback} />
                  </div>

                  <div className={`tab-panel ${activeTab === 'bullets' ? 'active' : ''}`}>
                    <BulletOptimizer preOptimizations={result.bullet_optimizations} />
                  </div>

                  <div className={`tab-panel ${activeTab === 'roadmap' ? 'active' : ''}`}>
                    <SkillRoadmap skills={result.skill_roadmap} />
                  </div>

                  <div className={`tab-panel ${activeTab === 'recommendations' ? 'active' : ''}`}>
                    <div className="rec-list">
                      {result.career_recommendations && result.career_recommendations.map((rec, i) => (
                        <div key={i} className="rec-item">
                          <CheckCircle2 size={18} className="rec-icon" />
                          <span>{rec}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
export { App };
