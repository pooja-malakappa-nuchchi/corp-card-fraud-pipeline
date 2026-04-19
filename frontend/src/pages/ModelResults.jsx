import { useState, useEffect } from 'react'

const API = 'http://127.0.0.1:8000'

const colorMap = {
  'Random Forest': { c: '#4ade80', bg: 'rgba(22,163,74,0.15)', tag: 'Best overall' },
  'XGBoost': { c: '#f87171', bg: 'rgba(220,38,38,0.15)', tag: 'Good balance' },
  'LightGBM': { c: '#a78bfa', bg: 'rgba(139,92,246,0.15)', tag: 'High recall' },
  'Logistic Regression': { c: '#60a5fa', bg: 'rgba(55,138,221,0.15)', tag: 'Baseline' },
  'LinearSVC': { c: '#fbbf24', bg: 'rgba(217,119,6,0.15)', tag: 'Linear baseline' },
}

const shortName = {
  'Random Forest': 'RF',
  'XGBoost': 'XGB',
  'LightGBM': 'LGBM',
  'Logistic Regression': 'LR',
  'LinearSVC': 'SVC',
}

function ModelResults() {
  const [metrics, setMetrics] = useState(null)
  const [cm, setCm] = useState(null)
  const [selected, setSelected] = useState(0)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      fetch(`${API}/metrics`).then(r => r.json()),
      fetch(`${API}/metrics/confusion-matrix`).then(r => r.json())
    ]).then(([metricsData, cmData]) => {
      setMetrics(metricsData)
      setCm(cmData)
      setLoading(false)
    }).catch(() => setLoading(false))
  }, [])

  if (loading || !metrics || !cm) return <div className="page" style={{ textAlign: 'center', paddingTop: '60px' }}>Loading metrics...</div>

  const models = metrics.models
  const cmModels = cm.models

  // Order for card selector: best first
  const cardOrder = ['Random Forest', 'XGBoost', 'LightGBM', 'Logistic Regression', 'LinearSVC']
  const cards = cardOrder.map(name => {
    const m = models.find(x => x.name === name)
    const c = cmModels.find(x => x.name === name)
    const info = colorMap[name] || { c: '#999', bg: 'rgba(150,150,150,0.15)', tag: '' }
    return { ...m, ...c, color: info.c, bg: info.bg, tag: info.tag, short: shortName[name] || name }
  })

  const sel = cards[selected]
  const minAuc = 0.96
  const range = 0.03

  return (
    <div className="page">
      <div className="page-title">Model performance</div>

      {/* Overall comparison table */}
      <div className="page-subtitle">Overall comparison</div>
      <div className="table-card">
      <table className="table">
        <thead>
          <tr>
            <th>Model</th>
            <th>Precision</th>
            <th>Recall</th>
            <th>F1</th>
            <th>AUC-ROC</th>
            <th>Time</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {models.map((m, i) => (
            <tr key={i}>
              <td>{m.name}</td>
              <td>{m.precision}</td>
              <td>{m.recall}</td>
              <td>{m.f1}</td>
              <td>{m.auc_roc}</td>
              <td>{m.training_time}</td>
              <td>{m.verdict === 'best' ? <span className="badge badge-legit">Best</span> : ''}</td>
            </tr>
          ))}
        </tbody>
      </table>
      </div>

      {/* AUC-ROC comparison */}
      <div className="chart-card" style={{ marginTop: '20px' }}>
        <div className="page-subtitle">AUC-ROC comparison</div>
        <div className="auc-bars">
          {cards.map((a, i) => (
            <div className="auc-col" key={i}>
              <div className="auc-val">{a.auc_roc}</div>
              <div
                className="auc-fill"
                style={{
                  height: `${((a.auc_roc - minAuc) / range) * 60}px`,
                  background: a.color
                }}
              ></div>
              <div className="auc-label">{a.short}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Individual model details - card tabs */}
      <div style={{ marginTop: '20px' }}>
        <div className="page-subtitle">Individual model details</div>
        <p style={{ fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '12px' }}>
          Click a model to view details
        </p>

        <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
          {cards.map((mc, i) => (
            <div
              key={i}
              onClick={() => setSelected(i)}
              style={{
                flex: 1,
                padding: '14px 12px',
                borderRadius: '10px',
                cursor: 'pointer',
                textAlign: 'center',
                border: `2px solid ${i === selected ? mc.color : 'var(--border)'}`,
                background: i === selected ? mc.bg : 'transparent',
                transition: 'all 0.2s'
              }}
            >
              <div style={{
                width: '10px',
                height: '10px',
                borderRadius: '50%',
                background: mc.color,
                margin: '0 auto 6px'
              }}></div>
              <div style={{ fontSize: '12px', fontWeight: 500, color: 'var(--text)' }}>{mc.short}</div>
              <div style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>{mc.auc_roc}</div>
              <div style={{ fontSize: '10px', color: 'var(--text-hint)', marginTop: '4px' }}>{mc.tag}</div>
            </div>
          ))}
        </div>

        <div className="chart-card">
          <div style={{ textAlign: 'center', marginBottom: '16px' }}>
            <span style={{ fontSize: '15px', fontWeight: 600 }}>{sel.name}</span>
            <span style={{ fontSize: '12px', color: 'var(--text-secondary)', marginLeft: '8px' }}>AUC: {sel.auc_roc}</span>
          </div>

          <div className="md-grid">
            <div>
              <div className="md-label">Precision</div>
              <div className="md-value">{sel.precision}</div>
            </div>
            <div>
              <div className="md-label">Recall</div>
              <div className="md-value">{sel.recall}</div>
            </div>
            <div>
              <div className="md-label">F1 score</div>
              <div className="md-value">{sel.f1}</div>
            </div>
            <div>
              <div className="md-label">Training time</div>
              <div className="md-value">{sel.training_time}</div>
            </div>
          </div>

          <div className="cm-title">Confusion matrix</div>
          <div className="cm-grid">
            <div className="cm-cell cm-tn">
              <div className="cm-val">{sel.tn ? sel.tn.toLocaleString() : '—'}</div>
              <div className="cm-label">True neg</div>
            </div>
            <div className="cm-cell cm-fp">
              <div className="cm-val">{sel.fp ? sel.fp.toLocaleString() : '—'}</div>
              <div className="cm-label">False pos</div>
            </div>
            <div className="cm-cell cm-fn">
              <div className="cm-val">{sel.fn ? sel.fn.toLocaleString() : '—'}</div>
              <div className="cm-label">False neg</div>
            </div>
            <div className="cm-cell cm-tp">
              <div className="cm-val">{sel.tp ? sel.tp.toLocaleString() : '—'}</div>
              <div className="cm-label">True pos</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ModelResults