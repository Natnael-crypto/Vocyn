import React from 'react';

interface Props { progress: number; title: string; status: string; }

const STEPS_LOG = [
  'Creating installation directory',
  'Extracting application files',
  'Extracting icon',
  'Creating shortcuts',
  'Writing registry entries',
];

const InstallProgress: React.FC<Props> = ({ progress, title, status }) => {
  const completedCount = Math.floor((progress / 100) * STEPS_LOG.length);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%', padding: '36px 36px 24px' }}>

      <div style={{ marginBottom: 24 }}>
        <div style={{ fontSize: 11, fontWeight: 600, color: '#999999', letterSpacing: '0.08em', textTransform: 'uppercase', marginBottom: 8 }}>
          Step 4 — Installing
        </div>
        <h1 style={{ fontSize: 20, fontWeight: 700, color: '#111111', letterSpacing: '-0.02em', margin: 0 }}>
          {title}
        </h1>
        <p style={{ color: '#888888', fontSize: 12, marginTop: 5 }}>
          Please wait while files are being installed…
        </p>
      </div>

      {/* Progress bar */}
      <div style={{ marginBottom: 24 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
          <span style={{ fontSize: 12, color: '#666666' }}>{status}</span>
          <span style={{ fontSize: 12, fontWeight: 700, color: '#111111' }}>{progress}%</span>
        </div>
        <div style={{ height: 6, background: '#eeeeee', borderRadius: 99, overflow: 'hidden' }}>
          <div style={{
            height: '100%',
            width: `${progress}%`,
            background: '#111111',
            borderRadius: 99,
            transition: 'width 0.5s ease',
          }} />
        </div>
      </div>

      {/* Activity log */}
      <div style={{
        flex: 1,
        border: '1px solid #eeeeee',
        borderRadius: 8,
        padding: '14px 16px',
        background: '#fafafa',
        display: 'flex',
        flexDirection: 'column',
        gap: 8,
        overflow: 'hidden',
      }}>
        <div style={{ fontSize: 10, fontWeight: 600, color: '#aaaaaa', letterSpacing: '0.08em', textTransform: 'uppercase', marginBottom: 4 }}>
          Activity
        </div>
        {STEPS_LOG.map((line, i) => {
          const done    = i < completedCount;
          const active  = i === completedCount && progress < 100;
          return (
            <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 10, opacity: done || active ? 1 : 0.3 }}>
              {done ? (
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#111111" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" style={{ flexShrink: 0 }}>
                  <polyline points="20 6 9 17 4 12"/>
                </svg>
              ) : active ? (
                <div className="spinner" />
              ) : (
                <div style={{ width: 13, height: 13, border: '1.5px solid #cccccc', borderRadius: '50%', flexShrink: 0 }} />
              )}
              <span style={{ fontSize: 12, color: done ? '#111111' : active ? '#444444' : '#aaaaaa' }}>{line}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default InstallProgress;
