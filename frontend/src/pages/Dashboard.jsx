import { useState, useEffect } from 'react'

const API = 'http://127.0.0.1:8000'

function Dashboard() {
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`${API}/transactions/summary`)
      .then(res => res.json())
      .then(data => {
        setSummary(data)
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [])

  const hourData = [
    { h: '0AM', f: 6 }, { h: '1AM', f: 36 }, { h: '2AM', f: 34 },
    { h: '3AM', f: 20 }, { h: '4AM', f: 25 }, { h: '5AM', f: 18 },
    { h: '6AM', f: 10 }, { h: '7AM', f: 8 }, { h: '8AM', f: 12 },
    { h: '9AM', f: 5 }, { h: '10AM', f: 15 }, { h: '11AM', f: 18 },
    { h: '12PM', f: 12 }, { h: '1PM', f: 8 }, { h: '2PM', f: 10 },
    { h: '3PM', f: 14 }, { h: '4PM', f: 16 }, { h: '5PM', f: 12 },
    { h: '6PM', f: 10 }, { h: '7PM', f: 8 }, { h: '8PM', f: 11 },
    { h: '9PM', f: 15 }, { h: '10PM', f: 20 }, { h: '11PM', f: 22 }
  ]

  const maxFraud = Math.max(...hourData.map(h => h.f))

  if (loading) return <div className="page" style={{ textAlign: 'center', paddingTop: '60px' }}>Loading...</div>

  return (
    <div className="page">
      <div className="page-title">Dashboard overview</div>

      <div className="stats-grid">
        <div className="stat-card blue">
          <div className="stat-label">Total transactions</div>
          <div className="stat-value blue">{summary ? summary.total_transactions.toLocaleString() : '—'}</div>
        </div>
        <div className="stat-card red">
          <div className="stat-label">Fraud detected</div>
          <div className="stat-value red">{summary ? summary.fraud_transactions.toLocaleString() : '—'}</div>
        </div>
        <div className="stat-card amber">
          <div className="stat-label">Fraud rate</div>
          <div className="stat-value amber">{summary ? summary.fraud_percentage + '%' : '—'}</div>
        </div>
        <div className="stat-card green">
          <div className="stat-label">Best AUC-ROC</div>
          <div className="stat-value green">0.9845</div>
        </div>
      </div>

      <div className="chart-card">
        <div className="page-subtitle">Fraud by hour</div>
        <div style={{
          display: 'flex',
          alignItems: 'flex-end',
          gap: '6px',
          height: '260px',
          marginTop: '12px'
        }}>
          {hourData.map((h, i) => (
            <div key={i} style={{
              flex: 1,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'flex-end',
              height: '100%'
            }}>
              <div style={{
                fontSize: '9px',
                color: 'var(--text-hint)',
                marginBottom: '4px'
              }}>{h.f}</div>
              <div style={{
                width: '100%',
                height: `${(h.f / maxFraud) * 100}%`,
                background: (h.h === '1AM' || h.h === '2AM') ? '#dc2626' : '#f5a8a8',
                borderRadius: '3px 3px 0 0',
                minHeight: '2px'
              }}></div>
              <div style={{
                fontSize: '9px',
                color: 'var(--text-secondary)',
                marginTop: '4px'
              }}>{h.h}</div>
            </div>
          ))}
        </div>
        <div className="peak-note">Peak fraud at 1AM–2AM</div>
      </div>

      <div className="chart-card">
        <div className="page-subtitle">Class distribution</div>
        <div style={{ marginTop: '12px' }}>
          <div className="class-row">
            <div className="class-label">Legitimate</div>
            <div className="class-bar" style={{ flex: 1, background: '#378ADD' }}></div>
            <div className="class-pct">{summary ? summary.legitimate_transactions.toLocaleString() : '—'} (99.83%)</div>
          </div>
          <div className="class-row">
            <div className="class-label">Fraud</div>
            <div className="class-bar" style={{ width: '6px', background: '#E24B4A' }}></div>
            <div className="class-pct">{summary ? summary.fraud_transactions.toLocaleString() : '—'} (0.17%)</div>
          </div>
        </div>
        <div className="imbalance-title">Severe class imbalance detected</div>
        <div className="imbalance-sub">SMOTE applied to balance training data</div>
      </div>
    </div>
  )
}

export default Dashboard