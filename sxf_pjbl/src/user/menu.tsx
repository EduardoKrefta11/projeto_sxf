import { useEffect, useState } from 'react'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, BarElement, ArcElement, Title, Tooltip, Legend } from 'chart.js'
import { Chart, Bar, Line, Pie } from 'react-chartjs-2'
import InstitutoLogo from '../assets/buko_kaesemodel.webp'
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

    const [pagina, setPagina] = useState('home')
    const [pacientes, setPacientes] = useState<any[]>([])
    const [erro, setErro] = useState('')

    const [organizacao, setOrganizacao] = useState('genero')
    const [tipoGrafico, setTipoGrafico] = useState('colunas')
    const [statsData, setStatsData] = useState<{labels: string[], valores: number[]} | null>(null)
    const [loadingStats, setLoadingStats] = useState(false)

    useEffect(() => {
        if (pagina === 'paciente') {
            fetch('/api/pacientes', { credentials: 'include' })
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
            carregarEstatisticas()
        }
    }, [pagina, organizacao])

    const carregarEstatisticas = () => {
        setLoadingStats(true)
        fetch(`/api/stats?organizacao=${organizacao}`, { credentials: 'include' })
            .then((res) => {
                if (res.status === 401) throw new Error('Não autorizado')
                return res.json()
            })
            .then((data) => setStatsData(data))
            .catch(() => setErro('Erro ao buscar estatísticas'))
            .finally(() => setLoadingStats(false))
    }

    const obterGrafico = () => {
        if (!statsData) return null

        const chartConfig = {
            labels: statsData.labels,
            datasets: [{
                label: 'Quantidade',
                data: statsData.valores,
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                borderColor: 'rgba(75, 192, 192, 1)',
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
                return <Bar data={chartConfig} options={opcoes} />
            case 'linhas':
                return <Line data={chartConfig} options={opcoes} />
            case 'pizza':
                return <Pie data={chartConfig} options={opcoes} />
            case 'barras':
                return <Bar data={{...chartConfig, datasets: [{...chartConfig.datasets[0], indexAxis: 'y' as const}]}} options={opcoes} />
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
            </div>

            <div className={pagina}>

                {pagina === 'home' && (
                    <div className="homeDiv">
                        <h1>Home</h1>
                        <p>O Instituto Buko Kaesemodel é uma sociedade sem fins lucrativos que tem por objetivo promover ações beneficientes 
                            relacionadas à assistência social, saúde, educação e meio ambiente. 
                            Nossa visão de futuro é contribuir com a construção de uma sociedade menos desigual, possibilitando a melhoria da qualidade de vida das pessoas, 
                            baseando-se pelo respeito à vida, solidariedade e ética.</p>
                        <img src={InstitutoLogo} alt="Logo Instituto" />
                    </div>
                )}

                {pagina === 'paciente' && (
                    <div className="pacienteDiv">
                        <h1>Pacientes</h1>
                        {erro && <p className="erro">{erro}</p>}
                        {pacientes.length === 0 ? (
                            <p>Nenhum paciente encontrado.</p>
                        ) : (
                            <div className="pacientesList">
                                {pacientes.map((paciente, index) => (
                                    <div className="pacienteCard" key={index}>
                                        <div className="pacienteLeft">
                                            <div className="pacienteName">{paciente.nome}</div>
                                            <div className="pacienteInfo">Sexo: {paciente.sexo}<br />Nascimento: {paciente.dataNascimento}</div>
                                        </div>
                                        <div className="pacienteRight">
                                            <div className="pacienteLastTest">Último teste: {paciente.ultimoTeste}</div>
                                            <div className="pacienteCreated">Criado: {paciente.dataCriacao}</div>
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
                                <label>Organizar por:</label>
                                <div className="buttonGroup">
                                    <button className={organizacao === 'genero' ? 'active' : ''} onClick={() => setOrganizacao('genero')}>Gênero</button>
                                    <button className={organizacao === 'data' ? 'active' : ''} onClick={() => setOrganizacao('data')}>Data</button>
                                    <button className={organizacao === 'sintoma' ? 'active' : ''} onClick={() => setOrganizacao('sintoma')}>Sintoma</button>
                                    <button className={organizacao === 'peso' ? 'active' : ''} onClick={() => setOrganizacao('peso')}>Peso</button>
                                </div>
                            </div>

                            <div className="controlGroup">
                                <label>Tipo de gráfico:</label>
                                <div className="buttonGroup">
                                    <button className={tipoGrafico === 'colunas' ? 'active' : ''} onClick={() => setTipoGrafico('colunas')}>Colunas</button>
                                    <button className={tipoGrafico === 'linhas' ? 'active' : ''} onClick={() => setTipoGrafico('linhas')}>Linhas</button>
                                    <button className={tipoGrafico === 'pizza' ? 'active' : ''} onClick={() => setTipoGrafico('pizza')}>Pizza</button>
                                    <button className={tipoGrafico === 'barras' ? 'active' : ''} onClick={() => setTipoGrafico('barras')}>Barras</button>
                                </div>
                            </div>
                        </div>

                        {loadingStats ? (
                            <p>Carregando estatísticas...</p>
                        ) : statsData && statsData.labels.length > 0 ? (
                            <div className="chartContainer">
                                {obterGrafico()}
                            </div>
                        ) : (
                            <p>Nenhum dado disponível para exibir.</p>
                        )}
                    </div>
                )}

            </div>

        </>
        
    )

}

export default Menu