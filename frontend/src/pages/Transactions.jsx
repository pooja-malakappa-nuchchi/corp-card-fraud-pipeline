import { useState, useEffect } from 'react'

const API = 'http://127.0.0.1:8000'
const PER_PAGE = 15

function Transactions() {
  const [txns, setTxns] = useState([])
  const [filter, setFilter] = useState('all')
  const [page, setPage] = useState(1)
  const [total, setTotal] = useState(0)
  const [totalPages, setTotalPages] = useState(1)
  const [loading, setLoading] = useState(true)

  const fetchData = (p, f) => {
    setLoading(true)
    const filterParam = f !== 'all' ? `&filter=${f}` : ''
    fetch(`${API}/transactions?page=${p}&limit=${PER_PAGE}${filterParam}`)
      .then(res => res.json())
      .then(data => {
        const txns = data.transactions.map((t, i) => ({
          id: `T${String((p - 1) * PER_PAGE + i + 1).padStart(5, '0')}`,
          amount: `$${Math.abs(t.Amount_Scaled * 100).toFixed(2)}`,
          hour: `${t.Hour}:00`,
          status: t.Class === 1 ? 'Fraud' : 'Legitimate'
        }))
        setTxns(txns)
        setTotal(data.total)
        setTotalPages(data.total_pages)
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }

  useEffect(() => {
    fetchData(page, filter)
  }, [page, filter])

  const changeFilt = (f) => {
    const filterVal = f === 'All' ? 'all' : f === 'Fraud' ? 'fraud' : 'legitimate'
    setFilter(filterVal)
    setPage(1)
  }

  const getPageNumbers = () => {
    const pages = []
    if (totalPages <= 7) {
      for (let i = 1; i <= totalPages; i++) pages.push(i)
    } else {
      pages.push(1)
      if (page > 3) pages.push('...')
      for (let i = Math.max(2, page - 1); i <= Math.min(totalPages - 1, page + 1); i++) pages.push(i)
      if (page < totalPages - 2) pages.push('...')
      pages.push(totalPages)
    }
    return [...new Set(pages)]
  }

  const start = (page - 1) * PER_PAGE

  return (
    <div className="page">
      <div className="page-title">All transactions</div>

      <div className="filters">
        {['All', 'Fraud', 'Legitimate'].map(f => {
          const fVal = f === 'All' ? 'all' : f === 'Fraud' ? 'fraud' : 'legitimate'
          return (
            <button
              key={f}
              className={`filter-btn ${filter === fVal ? 'active' : ''}`}
              onClick={() => changeFilt(f)}
            >{f}</button>
          )
        })}
        <div className="showing">
          {loading ? 'Loading...' : `Showing ${start + 1}–${Math.min(start + PER_PAGE, total)} of ${total.toLocaleString()}`}
        </div>
      </div>

      <div className="table-card">
      <table className="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Amount</th>
            <th>Hour</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {loading ? (
            <tr><td colSpan="4" style={{ textAlign: 'center', padding: '20px' }}>Loading...</td></tr>
          ) : txns.map((t, i) => (
            <tr key={i}>
              <td>{t.id}</td>
              <td>{t.amount}</td>
              <td>{t.hour}</td>
              <td>
                <span className={`badge ${t.status === 'Fraud' ? 'badge-fraud' : 'badge-legit'}`}>
                  {t.status}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      </div>

      <div className="pagination">
        <span onClick={() => page > 1 && setPage(page - 1)} style={{ cursor: page > 1 ? 'pointer' : 'default', opacity: page > 1 ? 1 : 0.3 }}>&lt;</span>
        {getPageNumbers().map((p, i) => (
          <span
            key={i}
            className={page === p ? 'active' : ''}
            onClick={() => typeof p === 'number' && setPage(p)}
            style={{ cursor: typeof p === 'number' ? 'pointer' : 'default' }}
          >{p}</span>
        ))}
        <span onClick={() => page < totalPages && setPage(page + 1)} style={{ cursor: page < totalPages ? 'pointer' : 'default', opacity: page < totalPages ? 1 : 0.3 }}>&gt;</span>
      </div>
    </div>
  )
}

export default Transactions