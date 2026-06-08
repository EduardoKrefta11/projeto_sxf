import { useState, useEffect } from 'react'
import './Admin.css'

function Admin() {
    const [abaAtiva, setAbaAtiva] = useState('usuarios')
    const [usuarios, setUsuarios] = useState<any[]>([])
    const [pacientes, setPacientes] = useState<any[]>([])
    const [sintomas, setSintomas] = useState<any[]>([])
    const [mensagemErro, setMensagemErro] = useState('')
    
    const [mostrarFormUsuario, setMostrarFormUsuario] = useState(false)
    const [mostrarFormPaciente, setMostrarFormPaciente] = useState(false)
    const [mostrarFormSintoma, setMostrarFormSintoma] = useState(false)
    const [usuarioEditandoId, setUsuarioEditandoId] = useState<number | null>(null)
    
    const [novoUsuario, setNovoUsuario] = useState({
        nome: '', user: '', senha: '', permissao: 'COM', dataNascimento: ''
    })

    const [novoPaciente, setNovoPaciente] = useState({
        nome: '', cpf: '', sexo: 'Masculino', dataNascimento: '', idPesquisador: ''
    })
    
    const [novoSintoma, setNovoSintoma] = useState({
        nome: '', pesoMasculino: '', pesoFeminino: ''
    })

    useEffect(() => {
        setMensagemErro('')
        if (abaAtiva === 'usuarios') buscarUsuarios()
        else if (abaAtiva === 'pacientes') buscarPacientes()
        else if (abaAtiva === 'sintomas') buscarSintomas()
    }, [abaAtiva])

    const buscarUsuarios = async () => {
        try {
            const res = await fetch('/api/usuarios', { credentials: 'include' })
            if (res.status === 401) { setMensagemErro('Não autorizado.'); return }
            const data = await res.json()
            setUsuarios(data)
        } catch (error) { setMensagemErro('Erro ao carregar usuários.') }
    }

    const buscarPacientes = async () => {
        try {
            const res = await fetch('/api/pacientes', { credentials: 'include' })
            if (res.status === 401) { setMensagemErro('Não autorizado.'); return }
            const data = await res.json()
            setPacientes(data)
        } catch (error) { setMensagemErro('Erro ao carregar pacientes.') }
    }

    const buscarSintomas = async () => {
        try {
            const res = await fetch('/api/sintomas', { credentials: 'include' })
            if (res.status === 401) { setMensagemErro('Não autorizado.'); return }
            const data = await res.json()
            setSintomas(data)
        } catch (error) { setMensagemErro('Erro ao carregar sintomas.') }
    }

    const salvarUsuario = async (e: React.FormEvent) => {
        e.preventDefault()

        try {
            const isEdicao = usuarioEditandoId !== null

            const url = isEdicao
                ? `/api/usuarios/${usuarioEditandoId}`
                : '/api/usuarios'

            const method = isEdicao ? 'PUT' : 'POST'

            const res = await fetch(url, {
                method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(novoUsuario),
                credentials: 'include'
            })

            if (res.ok) {
                alert(isEdicao ? 'Usuário atualizado!' : 'Usuário cadastrado!')

                setMostrarFormUsuario(false)
                setUsuarioEditandoId(null)

                setNovoUsuario({
                    nome: '',
                    user: '',
                    senha: '',
                    permissao: 'COM',
                    dataNascimento: ''
                })

                buscarUsuarios()
            } else {
                alert('Erro ao salvar usuário.')
            }

        } catch (error) {
            alert('Erro ao salvar.')
        }
    }

    const salvarPaciente = async (e: React.FormEvent) => {
        e.preventDefault()
        try {
            const res = await fetch('/api/pacientes', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(novoPaciente),
                credentials: 'include'
            })
            if (res.ok) {
                alert('Paciente cadastrado!')
                setMostrarFormPaciente(false)
                setNovoPaciente({ nome: '', cpf: '', sexo: 'Masculino', dataNascimento: '', idPesquisador: '' })
                buscarPacientes()
            }
        } catch (error) { alert('Erro ao salvar.') }
    }

    const salvarSintoma = async (e: React.FormEvent) => {
        e.preventDefault()
        try {
            const res = await fetch('/api/sintomas', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(novoSintoma),
                credentials: 'include'
            })
            if (res.ok) {
                alert('Sintoma cadastrado!')
                setMostrarFormSintoma(false)
                setNovoSintoma({ nome: '', pesoMasculino: '', pesoFeminino: '' })
                buscarSintomas()
            }
        } catch (error) { alert('Erro ao salvar.') }
    }

    const excluirItem = async (rota: string, id: number, callback: () => void) => {
        if (window.confirm('Tem certeza que deseja excluir?')) {
            try {
                const res = await fetch(`${rota}/${id}`, { method: 'DELETE', credentials: 'include' })
                if (res.ok) callback()
                else alert('Erro ao excluir.')
            } catch (error) { alert('Erro de conexão.') }
        }
    }

    return (
        <div className="adminContainer">
            <div className="adminHeader">
                <button className={`adminMenuButton ${abaAtiva === 'usuarios' ? 'active' : ''}`} onClick={() => setAbaAtiva('usuarios')}>Gerenciar Usuários</button>
                <button className={`adminMenuButton ${abaAtiva === 'pacientes' ? 'active' : ''}`} onClick={() => setAbaAtiva('pacientes')}>Gerenciar Pacientes</button>
                <button className={`adminMenuButton ${abaAtiva === 'sintomas' ? 'active' : ''}`} onClick={() => setAbaAtiva('sintomas')}>Gerenciar Sintomas</button>
            </div>

            <main className="adminMain">
                <div className="adminContent">
                    {abaAtiva === 'usuarios' && (
                        <div className="abaUsuarios">
                            <h1 className="adminTitle">Lista de Usuários</h1>
                            
                            {!mostrarFormUsuario ? (
                                <button className="btnAdd" onClick={() => setMostrarFormUsuario(true)}>+ Novo Usuário</button>
                            ) : (
                                <form className="formCadastro" onSubmit={salvarUsuario}>
                                    <h2>Novo Cadastro de Usuário</h2>
                                    <div className="formGroup"><label>Nome Completo:</label><input type="text" value={novoUsuario.nome} onChange={(e) => setNovoUsuario({...novoUsuario, nome: e.target.value})} required /></div>
                                    <div className="formGroup"><label>Nome de Usuário (Login):</label><input type="text" value={novoUsuario.user} onChange={(e) => setNovoUsuario({...novoUsuario, user: e.target.value})} required /></div>
                                    <div className="formGroup"><label>Senha:</label><input type="password" value={novoUsuario.senha} onChange={(e) => setNovoUsuario({...novoUsuario, senha: e.target.value})} required /></div>
                                    <div className="formGroup"><label>Data de Nascimento:</label><input type="date" value={novoUsuario.dataNascimento} onChange={(e) => setNovoUsuario({...novoUsuario, dataNascimento: e.target.value})} required /></div>
                                    <div className="formGroup"><label>Permissão:</label><select value={novoUsuario.permissao} onChange={(e) => setNovoUsuario({...novoUsuario, permissao: e.target.value})}><option value="COM">Comum (Médico/Pesquisador)</option><option value="ADM">Administrador</option></select></div>
                                    <div className="formActions">
                                        <button type="submit" className="btnSave">Salvar</button>
                                        <button type="button" className="btnCancel"
                                            onClick={() => {
                                                setMostrarFormUsuario(false)
                                                setUsuarioEditandoId(null)
                                            }}>Cancelar
                                        </button>
                                    </div>
                                </form>
                            )}

                            {mensagemErro && <p className="errorMsg">{mensagemErro}</p>}
                            <div className="userList">
                                {usuarios.map((u) => (
                                    <div className="userCard" key={u.id}>
                                        <div className="userInfo">
                                            <h3>{u.nome}</h3>
                                            <p><strong>Usuário:</strong> {u.user}</p>
                                            <p><strong>Permissão:</strong> {u.permissao}</p>
                                        </div>
                                        <div className="userActions">
                                            <button className="btnEdit" onClick={() => {
                                                setUsuarioEditandoId(u.id)
                                                setMostrarFormUsuario(true)
                                                setNovoUsuario({
                                                    nome: u.nome,
                                                    user: u.user,
                                                    senha: '',
                                                    permissao: u.permissao,
                                                    dataNascimento: u.dataNascimento || ''
                                                })
                                            }}>Editar</button>
                                            <button className="btnDelete" onClick={() => excluirItem('/api/usuarios', u.id, buscarUsuarios)}>Excluir</button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {abaAtiva === 'pacientes' && (
                        <div className="abaPacientes">
                            <h1 className="adminTitle">Gerenciar Pacientes</h1>
                            {!mostrarFormPaciente ? (
                                <button className="btnAdd" onClick={() => setMostrarFormPaciente(true)}>+ Novo Paciente</button>
                            ) : (
                                <form className="formCadastro" onSubmit={salvarPaciente}>
                                    <h2>Novo Paciente</h2>
                                    <div className="formGroup"><label>Nome:</label><input type="text" value={novoPaciente.nome} onChange={(e) => setNovoPaciente({...novoPaciente, nome: e.target.value})} required /></div>
                                    <div className="formGroup"><label>CPF:</label><input type="text" maxLength={11} value={novoPaciente.cpf} onChange={(e) => setNovoPaciente({...novoPaciente, cpf: e.target.value})} required /></div>
                                    <div className="formGroup"><label>Sexo:</label><select value={novoPaciente.sexo} onChange={(e) => setNovoPaciente({...novoPaciente, sexo: e.target.value})}><option value="Masculino">Masculino</option><option value="Feminino">Feminino</option></select></div>
                                    <div className="formGroup"><label>Nascimento:</label><input type="date" value={novoPaciente.dataNascimento} onChange={(e) => setNovoPaciente({...novoPaciente, dataNascimento: e.target.value})} required /></div>
                                    <div className="formGroup"><label>ID Pesquisador:</label><input type="number" value={novoPaciente.idPesquisador} onChange={(e) => setNovoPaciente({...novoPaciente, idPesquisador: e.target.value})} required /></div>
                                    <div className="formActions"><button type="submit" className="btnSave">Salvar</button><button type="button" className="btnCancel" onClick={() => setMostrarFormPaciente(false)}>Cancelar</button></div>
                                </form>
                            )}
                            {mensagemErro && <p className="errorMsg">{mensagemErro}</p>}
                            <div className="pacienteList">
                                {pacientes.map((p) => (
                                    <div className="pacienteCard" key={p.id}>
                                        <div className="pacienteInfo"><h3>{p.nome}</h3><p><strong>CPF:</strong> {p.cpf}</p></div>
                                        <div className="pacienteActions">
                                            <button className="btnEdit" onClick={() => alert('Em breve')}>Editar</button>
                                            <button className="btnDelete" onClick={() => excluirItem('/api/pacientes', p.id, buscarPacientes)}>Excluir</button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {abaAtiva === 'sintomas' && (
                        <div className="abaSintomas">
                            <h1 className="adminTitle">Gerenciar Sintomas</h1>
                            {!mostrarFormSintoma ? (
                                <button className="btnAdd" onClick={() => setMostrarFormSintoma(true)}>+ Novo Sintoma</button>
                            ) : (
                                <form className="formCadastro" onSubmit={salvarSintoma}>
                                    <h2>Novo Sintoma</h2>
                                    <div className="formGroup"><label>Nome do Sintoma:</label><input type="text" value={novoSintoma.nome} onChange={(e) => setNovoSintoma({...novoSintoma, nome: e.target.value})} required /></div>
                                    <div className="formGroup"><label>Peso Masculino:</label><input type="number" step="0.01" value={novoSintoma.pesoMasculino} onChange={(e) => setNovoSintoma({...novoSintoma, pesoMasculino: e.target.value})} required /></div>
                                    <div className="formGroup"><label>Peso Feminino:</label><input type="number" step="0.01" value={novoSintoma.pesoFeminino} onChange={(e) => setNovoSintoma({...novoSintoma, pesoFeminino: e.target.value})} required /></div>
                                    <div className="formActions"><button type="submit" className="btnSave">Salvar</button><button type="button" className="btnCancel" onClick={() => setMostrarFormSintoma(false)}>Cancelar</button></div>
                                </form>
                            )}
                            {mensagemErro && <p className="errorMsg">{mensagemErro}</p>}
                            <div className="sintomaList">
                                {sintomas.map((s) => (
                                    <div className="sintomaCard" key={s.id}>
                                        <div className="sintomaInfo">
                                            <h3>{s.nome}</h3>
                                            <div className="pesosContainer">
                                                <div className="pesoItem">♂ Masculino: {s.pesoMasculino}</div>
                                                <div className="pesoItem">♀ Feminino: {s.pesoFeminino}</div>
                                            </div>
                                        </div>
                                        <div className="sintomaActions">
                                            <button className="btnEdit" onClick={() => alert('Em breve')}>Editar</button>
                                            <button className="btnDelete" onClick={() => excluirItem('/api/sintomas', s.id, buscarSintomas)}>Excluir</button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            </main>
        </div>
    )
}

export default Admin
