import { useEffect, useState, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, BarElement, ArcElement, Title, Tooltip, Legend } from 'chart.js'
import { Bar, Line, Pie } from 'react-chartjs-2'
import defaultPFP from '../assets/default.png' // NOTA: ADICIONAR defaultPFP em foto de Perfil do usuário e do paciente 
import './Menu.css'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, BarElement, ArcElement, Title, Tooltip, Legend)

function MenuButton({ texto, onClick} : {texto: string, onClick: () => void} ) {
    return (
        <button className="menuButton" onClick={onClick}>
            {texto}
        </button>
    )
}

function Menu() {

    const navigate = useNavigate()
    const [pagina, setPagina] = useState('home')
    const [pacientes, setPacientes] = useState<any[]>([])
    const [mostrarFormPaciente, setMostrarFormPaciente] = useState(false)
    const [novoPaciente, setNovoPaciente] = useState({ nome: '', cpf: '', sexo: 'Masculino', dataNascimento: '' })
    const [perfil, setPerfil] = useState<any>(null)
    const [userPFP, setUserPFP] = useState<any>(null)
    const [erro, setErro] = useState('')
    const [tipoGrafico, setTipoGrafico] = useState('colunas')
    const [sintomasBuscados, setSintomasBuscados] = useState<{ id: number; nome: string }[]>([])
    const [sintoma, setSintoma] = useState('')
    const [pontuacaoMin, setPontuacaoMin] = useState('')
    const [pontuacaoMax, setPontuacaoMax] = useState('')
    const [sexo, setSexo] = useState('')
    const [nascimentoMin, setNascimentoMin] = useState('')
    const [nascimentoMax, setNascimentoMax] = useState('')

    const [dadosEstatisticos, setDadosEstatisticos] = useState<{labels: string[], valores: number[]} | null>(null)
    const [carregandoEstatisticas, setCarregandoEstatisticas] = useState(false)
    const [filtrosAplicados, setFiltrosAplicados] = useState(false)
    const graficoRef = useRef<any>(null)

    const formatarData = (dataString: string) => {

        if (!dataString) return '-'

        const data = new Date(dataString)

        return data.toLocaleDateString('pt-BR')
    }

    const formatarDataHora = (dataString: string) => {

        if (!dataString) return '-'

        const data = new Date(dataString)

        return data.toLocaleString('pt-BR')
    }

    async function enviarFotoPerfil() {

        if (!userPFP) {
            alert('Selecione uma foto primeiro')
            return
        }

        const formData = new FormData()

        formData.append('foto', userPFP)

        const response = await fetch(
            'http://localhost:5000/api/user_pfp',
            {
                method: 'POST',
                body: formData,
                credentials: 'include'
            }
        )

        const data = await response.json()

        console.log(data)

    }

    useEffect(() => {
        if (pagina === 'home') {
            fetch('/api/meu_perfil', {credentials: 'include'})
            .then((res) => {
                if (res.status === 401) throw new Error('Não autorizado')
                return res.json()
            })
            .then((data) => {
                setPerfil(data)
            })
            .catch(() => setErro('Erro ao buscar perfil do usuário'))
        }
    }, [pagina])

    useEffect(() => {
        if (pagina === 'paciente') {
            fetch('/api/meus_pacientes', { credentials: 'include' })
                .then((res) => {
                    if (res.status === 401) throw new Error('Não autorizado')
                    return res.json()
                })
                .then((data) => setPacientes(data))
                .catch(() => setErro('Erro ao buscar pacientes'))
        }
    }, [pagina])

    useEffect(() => {
        if (pagina === 'estatisticas') {
            fetch('/api/buscar_sintomas', { credentials: 'include' })
                .then((res) => {
                    if (res.status === 401) throw new Error('Não autorizado')
                    return res.json()
                })
                .then((data) => setSintomasBuscados(data))
                .catch(() => setErro('Erro ao buscar sintomas'))

            setFiltrosAplicados(false)
            setDadosEstatisticos(null)
        }
    }, [pagina])

    const montarParametrosEstatisticas = (opcoes?: { incluirTipoGrafico?: boolean }) => {
        const parametros = new URLSearchParams()
        const incluirTipoGrafico = opcoes?.incluirTipoGrafico ?? false

        if (sexo) {
            parametros.append('sexo', sexo)
        }

        if (nascimentoMin) {
            parametros.append('nascimentoMin', nascimentoMin)
        }

        if (nascimentoMax) {
            parametros.append('nascimentoMax', nascimentoMax)
        }

        if (sintoma) {
            parametros.append('sintoma', sintoma)
        }

        if (pontuacaoMin) {
            parametros.append('pontuacaoMin', pontuacaoMin)
        }

        if (pontuacaoMax) {
            parametros.append('pontuacaoMax', pontuacaoMax)
        }

        if (incluirTipoGrafico) {
            parametros.append('tipoGrafico', tipoGrafico)
        }

        return parametros
    }

    const carregarEstatisticas = () => {
            setCarregandoEstatisticas(true)
            setErro('')

            const parametros = montarParametrosEstatisticas()

            fetch(`/api/stats?${parametros.toString()}`, {
                credentials: 'include'
            })
            .then((res) => {
                if (res.status === 401) throw new Error('Não autorizado')
                return res.json()
            })
            .then((data) => {
                setDadosEstatisticos(data)
            })
            .catch(() => setErro('Erro ao buscar estatísticas'))
            .finally(() => setCarregandoEstatisticas(false))
    }

    const aplicarMascaraCPF = (valor: string) => {
        return valor
            .replace(/\D/g, '')
            .replace(/(\d{3})(\d)/, '$1.$2')
            .replace(/(\d{3})(\d)/, '$1.$2')
            .replace(/(\d{3})(\d{1,2})/, '$1-$2')
            .slice(0, 14)
    }

    const salvarPaciente = async (e: React.FormEvent) => {
        e.preventDefault()
        setErro('')

        const pacienteParaSalvar = {
            ...novoPaciente,
            cpf: novoPaciente.cpf.replace(/\D/g, '')
        }

        try {
            const res = await fetch('/api/meus_pacientes', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify(pacienteParaSalvar)
            })

            if (!res.ok) {
                throw new Error('Erro ao criar paciente')
            }

            setMostrarFormPaciente(false)
            setNovoPaciente({ nome: '', cpf: '', sexo: 'Masculino', dataNascimento: '' })
            fetch('/api/meus_pacientes', { credentials: 'include' })
                .then((res2) => res2.json())
                .then((data) => setPacientes(data))
                .catch(() => setErro('Erro ao atualizar lista de pacientes'))
        } catch (error) {
            setErro('Erro ao criar paciente')
        }
    }

    const aplicarFiltros = () => {
        setFiltrosAplicados(true)
        setDadosEstatisticos(null)
        carregarEstatisticas()
    }

    const obterImagemGrafico = () => {
        const chart = graficoRef.current

        if (!chart) {
            return null
        }

        if (typeof chart.toBase64Image === 'function') {
            return chart.toBase64Image()
        }

        return null
    }

    const gerarRelatorioEstatistico = async () => {
        const imagemGraficoBase64 = obterImagemGrafico()

        const body = {
            sexo,
            nascimentoMin,
            nascimentoMax,
            sintoma,
            pontuacaoMin,
            pontuacaoMax,
            tipoGrafico,
            imagemGraficoBase64
        }

        try {
            const res = await fetch('/api/pdf/stats', {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(body)
            })

            if (!res.ok) {
                throw new Error('Erro ao gerar PDF')
            }

            const blob = await res.blob()
            const url = URL.createObjectURL(blob)
            const link = document.createElement('a')
            link.href = url
            link.download = 'Relatorio_estatisticas.pdf'
            document.body.appendChild(link)
            link.click()
            link.remove()
            URL.revokeObjectURL(url)
        } catch (error) {
            console.error('Erro ao gerar PDF estatístico:', error)
            setErro('Erro ao gerar PDF estatístico')
        }
    }

    const logout = async () => {
        try {
            await fetch('/api/logout', {
                method: 'POST',
                credentials: 'include'
            })
            navigate('/', { replace: true })
        } catch (error) {
            console.error('Erro ao fazer logout:', error)
        }
    }

    const obterGrafico = () => {
        if (!dadosEstatisticos) return null

        const chartConfig = {
            labels: [...dadosEstatisticos.labels],
            datasets: [{
                label: 'Quantidade',
                data: [...dadosEstatisticos.valores],
                backgroundColor: [
                    '#36A2EB',
                    '#FF6384',
                    '#FFCE56',
                    '#4BC0C0',
                    '#9966FF',
                    '#FF9F40'
                ],
                borderColor: [
                    '#36A2EB',
                    '#FF6384',
                    '#FFCE56',
                    '#4BC0C0',
                    '#9966FF',
                    '#FF9F40'
                ],
                borderWidth: 1,
            }]
        }

        const opcoes = {
            responsive: true,
            plugins: {
                legend: {
                    display: true,
                }
            }
        }

        switch(tipoGrafico) {
            case 'colunas':
                return <Bar ref={graficoRef} data={chartConfig} options={opcoes} />
            case 'linhas':
                return <Line ref={graficoRef} data={chartConfig} options={opcoes} />
            case 'pizza':
                return <Pie ref={graficoRef} data={chartConfig} options={opcoes} />
            case 'barras':
                return (<Bar ref={graficoRef} data={chartConfig} options={{...opcoes, indexAxis: 'y' as const}}/>)
            default:
                return null
        }
    }

    return (
        <>
            <div className="interfaceSuperior">
                <MenuButton texto="Home" onClick={() => setPagina('home')}/>
                <MenuButton texto="Pacientes" onClick={() => setPagina('paciente')}/>
                <MenuButton texto="Estatisticas" onClick={() => setPagina('estatisticas')}/>
                <MenuButton texto="Sair" onClick={logout}/>
            </div>'

            <div className={pagina}>

                {pagina === 'home' && (
                    <div className="perfilDiv">

                        {perfil ? (
                            <div className="perfilCard">

                                <h1>Meu Perfil</h1>
                                {erro && <p className="erro">{erro}</p>}

                                <img
                                    className="perfilFoto"
                                    src={perfil.fotoPerfil ? `http://localhost:5000${perfil.fotoPerfil}` : defaultPFP}
                                    alt="Foto de Perfil"
                                />

                                <label htmlFor="userInputPFP" className="editarFotoBtn">
                                    📷
                                </label>

                                <input
                                    id="userInputPFP"
                                    type="file"
                                    accept="image/*"
                                    hidden
                                    onChange={(e) => {
                                        if (e.target.files?.[0]) {
                                            setUserPFP(e.target.files[0])
                                        }
                                    }}
                                />

                                <button className="userSavePFP" onClick={enviarFotoPerfil}>
                                    Salvar foto
                                </button>

                                <div className="perfilInfo">

                                    <h2>{perfil.nome}</h2>

                                    <p>
                                        <strong>Username:</strong> {perfil.user}
                                    </p>

                                    <p>
                                        <strong>Data de nascimento:</strong> {formatarData(perfil.dataNascimento)}
                                    </p>

                                    <p>
                                        <strong>Conta criada em:</strong> {formatarDataHora(perfil.dataCriacao)}
                                    </p>

                                </div>

                            </div>
                        ) : (
                            <p>Carregando perfil...</p>
                        )}

                    </div>
                )}

                {pagina === 'paciente' && (
                    <div className="pacienteDiv">
                        <div className="pacienteHeader">
                            <h1>Pacientes</h1>
                            <button className="btnAdd" onClick={() => { setMostrarFormPaciente(!mostrarFormPaciente); setErro('') }}>
                                Criar Paciente
                            </button>
                        </div>

                        {mostrarFormPaciente && (
                            <form className="pacienteForm" onSubmit={salvarPaciente}>
                                <div className="formGroup">
                                    <label>Nome</label>
                                    <input
                                        type="text"
                                        value={novoPaciente.nome}
                                        onChange={(e) => setNovoPaciente({ ...novoPaciente, nome: e.target.value })}
                                        required
                                    />
                                </div>
                                <div className="formGroup">
                                    <label>CPF</label>
                                    <input
                                        type="text"
                                        value={novoPaciente.cpf}
                                        onChange={(e) => setNovoPaciente({ ...novoPaciente, cpf: aplicarMascaraCPF(e.target.value) })}
                                        required
                                    />
                                </div>
                                <div className="formGroup">
                                    <label>Sexo</label>
                                    <select
                                        value={novoPaciente.sexo}
                                        onChange={(e) => setNovoPaciente({ ...novoPaciente, sexo: e.target.value })}
                                    >
                                        <option value="Masculino">Masculino</option>
                                        <option value="Feminino">Feminino</option>
                                    </select>
                                </div>
                                <div className="formGroup">
                                    <label>Data de nascimento</label>
                                    <input
                                        type="date"
                                        value={novoPaciente.dataNascimento}
                                        onChange={(e) => setNovoPaciente({ ...novoPaciente, dataNascimento: e.target.value })}
                                        required
                                    />
                                </div>
                                <div className="formActions">
                                    <button type="submit" className="btnSave">Salvar</button>
                                    <button type="button" className="btnCancel" onClick={() => {
                                        setMostrarFormPaciente(false)
                                        setNovoPaciente({ nome: '', cpf: '', sexo: 'Masculino', dataNascimento: '' })
                                    }}>
                                        Cancelar
                                    </button>
                                </div>
                            </form>
                        )}

                        {erro && <p className="erro">{erro}</p>}

                        {pacientes.length === 0 ? (
                            <p>Nenhum paciente encontrado.</p>
                        ) : (
                            <div className="pacientesList">
                                {pacientes.map((paciente, index) => (
                                    <div className="pacienteCard" key={index}>
                                        <div className="pacienteLeft">
                                            <img
                                                className="pacienteFoto"
                                                src={paciente.fotoPerfil || defaultPFP}
                                                alt={paciente.nome}
                                            />
                                            <div>
                                                <div className="pacienteName">
                                                    {paciente.nome}
                                                </div>
                                                <div className="pacienteInfo">
                                                    Sexo: {paciente.sexo}
                                                    <br />
                                                    Nascimento: {formatarData(paciente.dataNascimento)}
                                                </div>
                                            </div>
                                        </div>
                                        <div className="pacienteRight">
                                            <div className="pacienteLastTest">Último teste: {formatarDataHora(paciente.ultimoTeste)}</div>
                                            <div className="pacienteCreated">Criado: {formatarDataHora(paciente.dataCriacao)}</div>
                                            <button className="pdfButton" onClick={() => window.open(`/api/pdf/paciente/${paciente.id}`, '_blank')}>
                                                Gerar PDF
                                            </button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                )}

                {pagina === 'estatisticas' && (
                    <div className="statsDiv">
                        <h1>Estatísticas</h1>
                        {erro && <p className="erro">{erro}</p>}
                        
                        <div className="statsControls">

                                <div className="controlGroup">
                                    <label>Sexo:</label>

                                    <select
                                        value={sexo}
                                        onChange={(e) => { setSexo(e.target.value); setFiltrosAplicados(false) }}
                                    >
                                        <option value="">Todos</option>
                                        <option value="Masculino">Masculino</option>
                                        <option value="Feminino">Feminino</option>
                                    </select>
                                </div>

                                <div className="controlGroup">

                                    <label>Nascimento mínimo:</label>

                                    <input
                                        type="date"
                                        value={nascimentoMin}
                                        onChange={(e) => { setNascimentoMin(e.target.value); setFiltrosAplicados(false) }}
                                    />
                                </div>

                                <div className="controlGroup">
                                    <label>Nascimento máximo:</label>

                                    <input
                                        type="date"
                                        value={nascimentoMax}
                                        onChange={(e) => { setNascimentoMax(e.target.value); setFiltrosAplicados(false) }}
                                    />
                                </div>

                                <div className="controlGroup">
                                    <label>Sintoma</label>

                                    <select
                                        value={sintoma}
                                        onChange={(e) => { setSintoma(e.target.value); setFiltrosAplicados(false) }}
                                    >
                                        <option value="">Todos</option>

                                        {sintomasBuscados.map((s) => (
                                            <option key={s.id} value={s.nome}>
                                                {s.nome}
                                            </option>
                                        ))}
                                    </select>
                                </div>

                                <div className="controlGroup">
                                    <label>Pontuação Mínima:</label>

                                    <input
                                        type="number"
                                        value={pontuacaoMin}
                                        onChange={(e) => { setPontuacaoMin(e.target.value); setFiltrosAplicados(false) }}
                                    />
                                </div>

                                <div className="controlGroup">
                                    <label>Pontuação Máxima:</label>

                                    <input
                                        type="number"
                                        value={pontuacaoMax}
                                        onChange={(e) => { setPontuacaoMax(e.target.value); setFiltrosAplicados(false) }}
                                    />
                                </div>

                                <div className="controlGroup">
                                <label>Tipo de gráfico:</label>
                                <div className="buttonGroup">
                                                <button className={tipoGrafico === 'colunas' ? 'active' : ''} onClick={() => setTipoGrafico('colunas')}>Colunas</button>
                                    <button className={tipoGrafico === 'linhas' ? 'active' : ''} onClick={() => setTipoGrafico('linhas')}>Linhas</button>
                                    <button className={tipoGrafico === 'pizza' ? 'active' : ''} onClick={() => setTipoGrafico('pizza')}>Pizza</button>
                                    <button className={tipoGrafico === 'barras' ? 'active' : ''} onClick={() => setTipoGrafico('barras')}>Barras</button>
                                </div>

                                <button className="applyFiltersButton" onClick={aplicarFiltros}>
                                    Aplicar Filtros
                                </button>

                                <button className="pdfStatsButton" onClick={gerarRelatorioEstatistico}>
                                    Gerar PDF Estatístico
                                </button>

                            </div>

                        </div>

                        {carregandoEstatisticas ? (
                            <p>Carregando estatísticas...</p>
                        ) : filtrosAplicados ? (
                            dadosEstatisticos && dadosEstatisticos.labels.length > 0 ? (
                                <div className="chartContainer">
                                    {obterGrafico()}
                                </div>
                            ) : (
                                <p>Nenhum dado disponível para exibir.</p>
                            )
                        ) : (
                            <p>Defina os filtros e clique em "Aplicar Filtros" para gerar o gráfico.</p>
                        )}
                    </div>
                )}

            </div>

        </>
        
    )

}

export default Menu