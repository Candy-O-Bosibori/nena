import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import { initTheme } from './theme.js'
import App from './App.jsx'

// index.html already applies the theme synchronously pre-paint (avoids a
// flash); this call keeps src/theme.js as the source of truth and covers HMR.
initTheme()

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
