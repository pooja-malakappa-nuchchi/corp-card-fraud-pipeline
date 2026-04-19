import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom'
import { useState } from 'react'
import Dashboard from './pages/Dashboard'
import Transactions from './pages/Transactions'
import Predict from './pages/Predict'
import ModelResults from './pages/ModelResults'
import './App.css'

function App() {
  const [dark, setDark] = useState(false)

  const toggleTheme = () => {
    setDark(!dark)
    document.documentElement.setAttribute('data-theme', !dark ? 'dark' : 'light')
  }

  return (
    <BrowserRouter>
      <div className="nav">
        <div className="brand">
          <div className="brand-dot"></div>
          Corporate Card Misuse Detector
        </div>
        <div className="nav-right">
          <div className="nav-links">
            <NavLink to="/" end className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>Dashboard</NavLink>
            <NavLink to="/transactions" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>Transactions</NavLink>
            <NavLink to="/predict" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>Predict</NavLink>
            <NavLink to="/model-results" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>Model Results</NavLink>
          </div>
          <button className="theme-toggle" onClick={toggleTheme}>
            {dark ? 'Light' : 'Dark'}
          </button>
        </div>
      </div>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/transactions" element={<Transactions />} />
        <Route path="/predict" element={<Predict />} />
        <Route path="/model-results" element={<ModelResults />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App