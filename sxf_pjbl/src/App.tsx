// cd 'PASTA DO app.tsx'
// npm run dev
// PARA SALVAR PROJETO NO GIT
// git init
// git add .
// git commit -m "XXX"
// git push -u origin main

// Usuário admin comum: Username = adm_teste | Senha = 123adm
// Usuário teste comum: Username = com_teste | Senha = 123

import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import './App.css'

function App() {  
  const navigate = useNavigate()
  const [message, setMessage] = useState('')
  const [user, setUser] = useState('')
  const [senha, setSenha] = useState('')

  const preventReload = async(e: React.FormEvent) => {

    e.preventDefault();

    try {
    const res = await fetch('/api/login', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      credentials: 'include',
      body: JSON.stringify({user, senha})
    })
      const data = await res.json()
      setMessage(data.message)

      if(data.success) {

        if (data.permissao === 'ADM') {
          navigate("/admin")
        } else {
          navigate("/user")
        }

      }

    } catch (error) {

      setMessage('Erro ao conectar com o servidor')
      
    }
  }

  return (
    <>

    <div className="containerMain">
      
      <h1>IBK</h1>
      
      <div className="containerLogin">

        <form className="formLogin" onSubmit={preventReload}>

          <h2>Login</h2>

          <input 
          type="text" 
          placeholder="Nome de Usuário"
          value={user}
          onChange = {(e) => setUser(e.target.value)}
          />

          <input 
          type="password" 
          placeholder="Senha"
          value={senha}
          onChange = {(e) => setSenha(e.target.value)}
          />

          <button type="submit">Logar</button>

        </form> 

      </div>

      <p className="resultMessage">{message}</p>

      </div>
    </>
  )
}

export default App
