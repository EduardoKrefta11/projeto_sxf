import { useState, useEffect } from 'react'
import './Admin.css'

function Admin() {
    const [abaAtiva, setAbaAtiva] = useState('usuarios')
    const [usuarios, setUsuarios] = useState<any[]>([])
    const [pacientes, setPacientes] = useState<any[]>([])
    const [sintomas, setSintomas] = useState<any[]>([])
    const [consultas, setConsultas] = useState<any[]>([])
    const [mensagemErro, setMensagemErro] = useState('')
    const [busca, setBusca] = useState('')
    
    const [mostrarFormUsuario, setMostrarFormUsuario] = useState(false)
    const [mostrarFormPaciente, setMostrarFormPaciente] = useState(false)
    const [mostrarFormSintoma, setMostrarFormSintoma] = useState(false)
    const [mostrarFormConsulta, setMostrarFormConsulta] = useState(false)
    
    const [usuarioEditandoId, setUsuarioEditandoId] = useState<number | null>(null)
    const [pacienteEditandoId, setPacienteEditandoId] = useState<number | null>(null)
    const [sintomaEditandoId, setSintomaEditandoId] = useState<number | null>(null)
    const [consultaEditandoId, setConsultaEditandoId] = useState<number | null>(null)
    
    const [novoUsuario, setNovoUsuario] = useState({nome:'', user:'', senha:'', permissao:'COM', dataNascimento:'', status: 'Ativo'})
    const [novoPaciente, setNovoPaciente] = useState({nome:'', cpf:'', sexo:'Masculino', dataNascimento:'', idPesquisador:''})
    const [novoSintoma, setNovoSintoma] = useState({nome:'', pesoMasculino:'', pesoFeminino:''})
    const [novaConsulta, setNovaConsulta] = useState({idPaciente: '', tipoExame: '', observacao: '', sintomas: [] as number[]})

    useEffect(() => {
        buscarUsuarios()
        buscarPacientes()
        buscarSintomas()
        buscarConsultas()
    }, [])

    const buscarUsuarios = () => fetch('/api/usuarios').then(res => res.json()).then(setUsuarios).catch(() => setMensagemErro('Erro ao carregar usuários'))
    const buscarPacientes = () => fetch('/api/pacientes').then(res => res.json()).then(setPacientes).catch(() => setMensagemErro('Erro ao carregar pacientes'))
    const buscarSintomas = () => fetch('/api/sintomas').then(res => res.json()).then(setSintomas).catch(() => setMensagemErro('Erro ao carregar sintomas'))
    const buscarConsultas = () => fetch('/api/admin/consultas').then(res => res.json()).then(setConsultas).catch(() => setMensagemErro('Erro ao carregar consultas'))

    const salvarUsuario = async (e: any) => {
        e.preventDefault()
        const url = usuarioEditandoId ? `/api/usuarios/${usuarioEditandoId}` : '/api/usuarios'
        const method = usuarioEditandoId ? 'PUT' : 'POST'
        
        try {
            const res = await fetch(url, {
                method,
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(novoUsuario)
            })
            if (res.ok) {
                setMostrarFormUsuario(false)
                setUsuarioEditandoId(null)
                setNovoUsuario({nome:'', user:'', senha:'', permissao:'COM', dataNascimento:'', status: 'Ativo'})
                buscarUsuarios()
            }
        } catch (error) {
            setMensagemErro('Erro ao salvar usuário')
        }
    }

    const desativarUsuario = async (id: number) => {
        if (!confirm('Deseja realmente desativar este usuário?')) return
        try {
            const res = await fetch(`/api/usuarios/${id}`, { method: 'DELETE' })
            if (res.ok) buscarUsuarios()
        } catch (error) {
            setMensagemErro('Erro ao desativar usuário')
        }
    }

    const reativarUsuario = async (u: any) => {
        try {
            const res = await fetch(`/api/usuarios/${u.id}`, {
                method: 'PUT',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({...u, status: 'Ativo'})
            })
            if (res.ok) buscarUsuarios()
        } catch (error) {
            setMensagemErro('Erro ao reativar usuário')
        }
    }

    const salvarPaciente = async (e: any) => {
        e.preventDefault()
        const url = pacienteEditandoId ? `/api/pacientes/${pacienteEditandoId}` : '/api/pacientes'
        const method = pacienteEditandoId ? 'PUT' : 'POST'
        
        try {
            const res = await fetch(url, {
                method,
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({...novoPaciente, cpf: novoPaciente.cpf.replace(/\D/g, '')})
            })
            if (res.ok) {
                setMostrarFormPaciente(false)
                setPacienteEditandoId(null)
                setNovoPaciente({nome:'', cpf:'', sexo:'Masculino', dataNascimento:'', idPesquisador:''})
                buscarPacientes()
            }
        } catch (error) {
            setMensagemErro('Erro ao salvar paciente')
        }
    }

    const salvarSintoma = async (e: any) => {
        e.preventDefault()
        const url = sintomaEditandoId ? `/api/sintomas/${sintomaEditandoId}` : '/api/sintomas'
        const method = sintomaEditandoId ? 'PUT' : 'POST'
        
        try {
            const res = await fetch(url, {
                method,
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(novoSintoma)
            })
            if (res.ok) {
                setMostrarFormSintoma(false)
                setSintomaEditandoId(null)
                setNovoSintoma({nome:'', pesoMasculino:'', pesoFeminino:''})
                buscarSintomas()
            }
        } catch (error) {
            setMensagemErro('Erro ao salvar sintoma')
        }
    }

    const salvarConsulta = async (e: any) => {
        e.preventDefault()
        if (novaConsulta.sintomas.length === 0) {
            alert('Selecione ao menos um sintoma')
            return
        }
        const url = consultaEditandoId ? `/api/admin/consultas/${consultaEditandoId}` : '/api/admin/consultas'
        const method = consultaEditandoId ? 'PUT' : 'POST'
        
        try {
            const res = await fetch(url, {
                method,
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(novaConsulta)
            })
            if (res.ok) {
                setMostrarFormConsulta(false)
                setConsultaEditandoId(null)
                setNovaConsulta({idPaciente: '', tipoExame: '', observacao: '', sintomas: []})
                buscarConsultas()
            }
        } catch (error) {
            setMensagemErro('Erro ao salvar consulta')
        }
    }

    const excluirItem = async (endpoint: string, id: number, callback: Function) => {
        if (!confirm('Deseja realmente excluir este item?')) return
        try {
            const res = await fetch(`${endpoint}/${id}`, { method: 'DELETE' })
            if (res.ok) callback()
        } catch (error) {
            setMensagemErro('Erro ao excluir item')
        }
    }

    const fazerLogout = async () => {
        try {
            await fetch('/api/logout', { method: 'POST' })
            window.location.href = '/'
        } catch (error) {
            window.location.href = '/'
        }
    }

    const formatarDataBR = (dataStr: string) => {
        if (!dataStr) return 'Não informada'
        try {
            const d = new Date(dataStr)
            if (isNaN(d.getTime())) return dataStr
            return d.toLocaleDateString('pt-BR')
        } catch {
            return dataStr
        }
    }

    const aplicarMascaraCPF = (valor: string) => {
        const v = valor.replace(/\D/g, '')
        if (v.length <= 11) {
            return v.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/g, '$1.$2.$3-$4')
        }
        return v
    }

    const baixarPDF = async (pacienteId: number, nome: string) => {
        try {
            const res = await fetch(`/api/admin/pdf/paciente/${pacienteId}`)
            if (res.ok) {
                const blob = await res.blob()
                const url = window.URL.createObjectURL(blob)
                const a = document.createElement('a')
                a.href = url
                a.download = `Relatorio_${nome}.pdf`
                a.click()
                window.URL.revokeObjectURL(url)
            } else {
                alert('Erro ao gerar PDF.')
            }
        } catch (error) {
            alert('Erro de conexão.')
        }
    }

    const filtrarItens = (lista: any[]) => {
        if (!Array.isArray(lista)) return []
        if (!busca) return lista
        const b = busca.toLowerCase()
        const bApenasNumeros = busca.replace(/\D/g, '')
        
        return lista.filter(item => {
            const nome = (item.nome || item.nomePaciente || '').toLowerCase()
            const user = (item.user || '').toLowerCase()
            const cpf = (item.cpf || '').replace(/\D/g, '')
            
            return nome.includes(b) || 
                   user.includes(b) || 
                   (bApenasNumeros && cpf.includes(bApenasNumeros))
        })
    }

    const toggleSintoma = (id: number) => {
        setNovaConsulta(prev => ({
            ...prev,
            sintomas: prev.sintomas.includes(id) 
                ? prev.sintomas.filter(sid => sid !== id) 
                : [...prev.sintomas, id]
        }))
    }

    return (
        <div className="adminContainer">
            <div className="adminHeader">
                <button className={`adminMenuButton ${abaAtiva === 'usuarios' ? 'active' : ''}`} onClick={() => setAbaAtiva('usuarios')}>Usuários</button>
                <button className={`adminMenuButton ${abaAtiva === 'pacientes' ? 'active' : ''}`} onClick={() => setAbaAtiva('pacientes')}>Pacientes</button>
                <button className={`adminMenuButton ${abaAtiva === 'sintomas' ? 'active' : ''}`} onClick={() => setAbaAtiva('sintomas')}>Sintomas</button>
                <button className={`adminMenuButton ${abaAtiva === 'consultas' ? 'active' : ''}`} onClick={() => setAbaAtiva('consultas')}>Consultas</button>
                <button className="adminMenuButton" style={{marginLeft: 'auto', backgroundColor: '#ffcdd2', borderColor: '#e53935'}} onClick={fazerLogout}>Sair</button>
            </div>

            <main className="adminMain">
                <div className="adminContent">
                    <div className="searchBar" style={{marginBottom: '20px'}}>
                        <input 
                            type="text" 
                            placeholder="Buscar por nome, CPF ou usuário..." 
                            value={busca}
                            onChange={(e) => setBusca(e.target.value)}
                            style={{width: '100%', padding: '12px', fontSize: '18px', borderRadius: '8px', border: '2px solid #a5d6a7'}}
                        />
                    </div>

                    {mensagemErro && <p style={{color: 'red', textAlign: 'center'}}>{mensagemErro}</p>}

                    {abaAtiva === 'usuarios' && (
                        <div className="abaUsuarios">
                            <h1 className="adminTitle">Lista de Usuários</h1>
                            {!mostrarFormUsuario ? (
                                <button className="btnAdd" onClick={() => setMostrarFormUsuario(true)}>+ Novo Usuário</button>
                            ) : (
                                <form className="formCadastro" onSubmit={salvarUsuario}>
                                    <h2>{usuarioEditandoId ? 'Editar Usuário' : 'Novo Cadastro de Usuário'}</h2>
                                    <div className="formGroup"><label>Nome Completo:</label><input type="text" value={novoUsuario.nome} onChange={(e) => setNovoUsuario({...novoUsuario, nome: e.target.value})} required /></div>
                                    <div className="formGroup"><label>Nome de Usuário (Login):</label><input type="text" value={novoUsuario.user} onChange={(e) => setNovoUsuario({...novoUsuario, user: e.target.value})} required /></div>
                                    <div className="formGroup"><label>Senha {usuarioEditandoId && '(deixe em branco para manter)'}:</label><input type="password" value={novoUsuario.senha} onChange={(e) => setNovoUsuario({...novoUsuario, senha: e.target.value})} required={!usuarioEditandoId} /></div>
                                    <div className="formGroup"><label>Data de Nascimento:</label><input type="date" value={novoUsuario.dataNascimento} onChange={(e) => setNovoUsuario({...novoUsuario, dataNascimento: e.target.value})} required /></div>
                                    <div className="formGroup"><label>Permissão:</label><select value={novoUsuario.permissao} onChange={(e) => setNovoUsuario({...novoUsuario, permissao: e.target.value})}><option value="COM">Comum (Médico/Pesquisador)</option><option value="ADM">Administrador</option></select></div>
                                    <div className="formGroup"><label>Status:</label><select value={novoUsuario.status} onChange={(e) => setNovoUsuario({...novoUsuario, status: e.target.value})}><option value="Ativo">Ativo</option><option value="Inativo">Inativo</option></select></div>
                                    <div className="formActions">
                                        <button type="submit" className="btnSave">Salvar</button>
                                        <button type="button" className="btnCancel" onClick={() => { setMostrarFormUsuario(false); setUsuarioEditandoId(null); setNovoUsuario({nome:'', user:'', senha:'', permissao:'COM', dataNascimento:'', status: 'Ativo'}) }}>Cancelar</button>
                                    </div>
                                </form>
                            )}
                            <div className="userList">
                                {filtrarItens(usuarios).map((u) => (
                                    <div className="userCard" key={u.id} style={{opacity: u.status === 'Inativo' ? 0.6 : 1}}>
                                        <div className="userInfo">
                                            <h3>{u.nome} {u.status === 'Inativo' && <span style={{fontSize: '14px', color: '#e53935', marginLeft: '10px'}}>(Inativo)</span>}</h3>
                                            <p><strong>Usuário:</strong> {u.user}</p>
                                            <p><strong>Nascimento:</strong> {formatarDataBR(u.dataNascimento)}</p>
                                        </div>
                                        <div className="userActions">
                                            <button className="btnEdit" onClick={() => { setUsuarioEditandoId(u.id); setMostrarFormUsuario(true); setNovoUsuario({nome: u.nome, user: u.user, senha: '', permissao: u.permissao, dataNascimento: u.dataNascimento || '', status: u.status}) }}>Editar</button>
                                            {u.status === 'Ativo' ? (
                                                <button className="btnDelete" onClick={() => desativarUsuario(u.id)}>Desativar</button>
                                            ) : (
                                                <button className="btnEdit" style={{backgroundColor: '#4caf50', borderColor: '#388e3c'}} onClick={() => reativarUsuario(u)}>Reativar</button>
                                            )}
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
                                    <h2>{pacienteEditandoId ? 'Editar Paciente' : 'Novo Paciente'}</h2>
                                    <div className="formGroup"><label>Nome:</label><input type="text" value={novoPaciente.nome} onChange={(e) => setNovoPaciente({...novoPaciente, nome: e.target.value})} required /></div>
                                    <div className="formGroup"><label>CPF:</label><input type="text" value={novoPaciente.cpf} onChange={(e) => setNovoPaciente({...novoPaciente, cpf: aplicarMascaraCPF(e.target.value)})} required /></div>
                                    <div className="formGroup"><label>Sexo:</label><select value={novoPaciente.sexo} onChange={(e) => setNovoPaciente({...novoPaciente, sexo: e.target.value})}><option value="Masculino">Masculino</option><option value="Feminino">Feminino</option></select></div>
                                    <div className="formGroup"><label>Nascimento:</label><input type="date" value={novoPaciente.dataNascimento} onChange={(e) => setNovoPaciente({...novoPaciente, dataNascimento: e.target.value})} required /></div>
                                    <div className="formGroup"><label>Pesquisador Responsável:</label>
                                        <select value={novoPaciente.idPesquisador} onChange={(e) => setNovoPaciente({...novoPaciente, idPesquisador: e.target.value})} required>
                                            <option value="">Selecione um pesquisador</option>
                                            {usuarios.filter(u => u.status === 'Ativo').map(u => <option key={u.id} value={u.id}>{u.nome}</option>)}
                                        </select>
                                    </div>
                                    <div className="formActions">
                                        <button type="submit" className="btnSave">Salvar</button>
                                        <button type="button" className="btnCancel" onClick={() => { setMostrarFormPaciente(false); setPacienteEditandoId(null); setNovoPaciente({nome:'', cpf:'', sexo:'Masculino', dataNascimento:'', idPesquisador:''}) }}>Cancelar</button>
                                    </div>
                                </form>
                            )}
                            <div className="pacienteList">
                                {filtrarItens(pacientes).map((p) => (
                                    <div className="pacienteCard" key={p.id}>
                                        <div className="pacienteInfo">
                                            <h3>{p.nome}</h3>
                                            <p><strong>CPF:</strong> {aplicarMascaraCPF(p.cpf)}</p>
                                            <p><strong>Pesquisador:</strong> {p.nomePesquisador || 'Não atribuído'}</p>
                                        </div>
                                        <div className="pacienteActions">
                                            <button className="btnEdit" onClick={() => { setPacienteEditandoId(p.id); setMostrarFormPaciente(true); setNovoPaciente({nome: p.nome, cpf: aplicarMascaraCPF(p.cpf), sexo: p.sexo, dataNascimento: p.dataNascimento || '', idPesquisador: p.idPesquisador || ''}) }}>Editar</button>
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
                                    <h2>{sintomaEditandoId ? 'Editar Sintoma' : 'Novo Sintoma'}</h2>
                                    <div className="formGroup"><label>Nome do Sintoma:</label><input type="text" value={novoSintoma.nome} onChange={(e) => setNovoSintoma({...novoSintoma, nome: e.target.value})} required /></div>
                                    <div className="formGroup"><label>Peso Masculino:</label><input type="number" step="0.01" value={novoSintoma.pesoMasculino} onChange={(e) => setNovoSintoma({...novoSintoma, pesoMasculino: e.target.value})} required /></div>
                                    <div className="formGroup"><label>Peso Feminino:</label><input type="number" step="0.01" value={novoSintoma.pesoFeminino} onChange={(e) => setNovoSintoma({...novoSintoma, pesoFeminino: e.target.value})} required /></div>
                                    <div className="formActions">
                                        <button type="submit" className="btnSave">Salvar</button>
                                        <button type="button" className="btnCancel" onClick={() => { setMostrarFormSintoma(false); setSintomaEditandoId(null); setNovoSintoma({nome:'', pesoMasculino:'', pesoFeminino:''}) }}>Cancelar</button>
                                    </div>
                                </form>
                            )}
                            <div className="sintomaList">
                                {filtrarItens(sintomas).map((s) => (
                                    <div className="sintomaCard" key={s.id}>
                                        <div className="sintomaInfo">
                                            <h3>{s.nome}</h3>
                                            <div style={{display: 'flex', gap: '20px', marginTop: '10px'}}>
                                                <span style={{backgroundColor: '#e3f2fd', padding: '5px 10px', borderRadius: '5px'}}>♂ Masc: <strong>{s.pesoMasculino}</strong></span>
                                                <span style={{backgroundColor: '#fce4ec', padding: '5px 10px', borderRadius: '5px'}}>♀ Fem: <strong>{s.pesoFeminino}</strong></span>
                                            </div>
                                        </div>
                                        <div className="sintomaActions">
                                            <button className="btnEdit" onClick={() => { setSintomaEditandoId(s.id); setMostrarFormSintoma(true); setNovoSintoma({nome: s.nome, pesoMasculino: s.pesoMasculino, pesoFeminino: s.pesoFeminino}) }}>Editar</button>
                                            <button className="btnDelete" onClick={() => excluirItem('/api/sintomas', s.id, buscarSintomas)}>Excluir</button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {abaAtiva === 'consultas' && (
                        <div className="abaConsultas">
                            <h1 className="adminTitle">Histórico Geral de Consultas</h1>
                            {!mostrarFormConsulta ? (
                                <button className="btnAdd" onClick={() => setMostrarFormConsulta(true)}>+ Nova Consulta</button>
                            ) : (
                                <form className="formCadastro" onSubmit={salvarConsulta}>
                                    <h2>{consultaEditandoId ? 'Editar Consulta' : 'Realizar Nova Consulta'}</h2>
                                    <div className="formGroup">
                                        <label>Paciente:</label>
                                        <select value={novaConsulta.idPaciente} onChange={(e) => setNovaConsulta({...novaConsulta, idPaciente: e.target.value})} required disabled={consultaEditandoId !== null}>
                                            <option value="">Selecione um paciente</option>
                                            {pacientes.map(p => <option key={p.id} value={p.id}>{p.nome} ({aplicarMascaraCPF(p.cpf)})</option>)}
                                        </select>
                                    </div>
                                    <div className="formGroup"><label>Tipo de Exame:</label><input type="text" value={novaConsulta.tipoExame} onChange={(e) => setNovaConsulta({...novaConsulta, tipoExame: e.target.value})} placeholder="Ex: Avaliação Clínica, Teste de DNA..." required /></div>
                                    <div className="formGroup"><label>Sintomas Observados:</label>
                                        <div className="sintomasGrid" style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '10px', maxHeight: '200px', overflowY: 'auto', padding: '10px', backgroundColor: '#f5f5f5', borderRadius: '8px'}}>
                                            {sintomas.map(s => (
                                                <label key={s.id} style={{display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer'}}>
                                                    <input type="checkbox" checked={novaConsulta.sintomas.includes(s.id)} onChange={() => toggleSintoma(s.id)} />
                                                    {s.nome}
                                                </label>
                                            ))}
                                        </div>
                                    </div>
                                    <div className="formGroup"><label>Observações Adicionais:</label><textarea value={novaConsulta.observacao} onChange={(e) => setNovaConsulta({...novaConsulta, observacao: e.target.value})} rows={3}></textarea></div>
                                    <div className="formActions">
                                        <button type="submit" className="btnSave">Salvar Consulta</button>
                                        <button type="button" className="btnCancel" onClick={() => { setMostrarFormConsulta(false); setConsultaEditandoId(null); setNovaConsulta({idPaciente: '', tipoExame: '', observacao: '', sintomas: []}) }}>Cancelar</button>
                                    </div>
                                </form>
                            )}
                            <div className="consultaList">
                                {filtrarItens(consultas).map((c) => (
                                    <div className="consultaCard" key={c.id}>
                                        <div className="consultaHeader">
                                            <h3>{c.nomePaciente}</h3>
                                            <div className="pontuacaoBadge">Score: {c.pontuacao}</div>
                                        </div>
                                        <div className="consultaInfo">
                                            <p><strong>Data:</strong> {new Date(c.dataHora).toLocaleString('pt-BR')}</p>
                                            <p><strong>Pesquisador:</strong> {c.nomePesquisador || 'Não identificado'}</p>
                                            <p><strong>Exame:</strong> {c.tipoExame} ({c.resultadoExame})</p>
                                            <p><strong>Encaminhamento:</strong> {c.encaminhamento}</p>
                                            {c.observacao && <p><strong>Obs:</strong> {c.observacao}</p>}
                                        </div>
                                        {c.sintomas && (
                                            <div className="sintomasList" style={{marginTop: '10px', fontStyle: 'italic', color: '#666'}}>
                                                <strong>Sintomas:</strong> {c.sintomas}
                                            </div>
                                        )}
                                        <div className="consultaActions" style={{marginTop: '15px', display: 'flex', gap: '15px', justifyContent: 'flex-end', width: '100%'}}>
                                            <button className="btnEdit" style={{backgroundColor: '#2196f3', borderColor: '#1976d2'}} onClick={() => baixarPDF(c.idPaciente, c.nomePaciente)}>Gerar PDF</button>
                                            <button className="btnEdit" onClick={() => { 
                                                setConsultaEditandoId(c.id); 
                                                setMostrarFormConsulta(true); 
                                                setNovaConsulta({
                                                    idPaciente: String(c.idPaciente || ''), 
                                                    tipoExame: c.tipoExame || '', 
                                                    observacao: c.observacao || '', 
                                                    sintomas: c.idsSintomas ? String(c.idsSintomas).split(',').map(Number) : []
                                                }) 
                                            }}>Editar</button>
                                            <button className="btnDelete" onClick={() => excluirItem('/api/admin/consultas', c.id, buscarConsultas)}>Excluir</button>
                                        </div>
                                    </div>
                                ))}
                                {filtrarItens(consultas).length === 0 && <p className="emptyMsg">Nenhuma consulta encontrada.</p>}
                            </div>
                        </div>
                    )}
                </div>
            </main>
        </div>
    )
}

export default Admin
