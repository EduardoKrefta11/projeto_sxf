import { useState } from 'react'
import './App.css'

function App() {  
  const [message, setMessage] = useState(null)
  const [user, setUser] = useState('')
  const [senha, setSenha] = useState('')
  const [permissao, setPermissao] = useState(0)

  const preventReload = async(e: React.FormEvent) => {

    e.preventDefault();

    const res = await fetch('/api/login', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({user, senha, permissao})
    })

    const data = await res.json()
    setMessage(data.message)

  }

  return (
    <>

    <div className="containerMain">
      
      <h1>SXF</h1>

      <p>{message}</p>

      <div className="containerLogin">

        <form className="formLogin" onSubmit={preventReload}>

          <h2>Login</h2>
          <p>Bem vindo</p>

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

          <p>Sou admin</p>
          <input
          type="checkbox"
          checked={permissao === 1}
          onChange = {(e) => setPermissao(e.target.checked ? 1 : 0)}
          />

          <button type="submit">Logar</button>

        </form> 

      </div>

      </div>
    </>
  )
}

export default App
