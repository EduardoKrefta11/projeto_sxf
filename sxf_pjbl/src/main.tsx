import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'

import './index.css'
import App from './App.tsx'
import Admin from "./admin/admin.tsx"
import User from "./user/menu.tsx"

createRoot(document.getElementById('root')!).render(
  <StrictMode>

    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />}/>
        <Route path="./admin/admin.tsx" element={<Admin />}/>
        <Route path="./user/user.tsx" element={<User />}/>
      </Routes>
    </BrowserRouter>

  </StrictMode>,
)
