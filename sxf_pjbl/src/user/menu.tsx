import { useEffect, useState } from 'react'
import InstitutoLogo from '../assets/buko_kaesemodel.webp'
import './Menu.css'

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

    useEffect(() => {
        if (pagina === 'paciente') {
            fetch('/api/pacientes')
                .then((res) => res.json())
                .then((data) => setPacientes(data))
                .catch(() => setErro('Erro ao buscar pacientes'))
        }
    }, [pagina])

    

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
                            <ul>
                                {pacientes.map((paciente, index) => (
                                    <li key={index}>
                                        <strong>{paciente.nome}</strong><br />
                                        Sexo: {paciente.sexo}<br />
                                        Nascimento: {paciente.dataNascimento}<br />
                                        Último teste: {paciente.ultimoTeste}<br />
                                        Criado em: {paciente.dataCriacao}
                                    </li>
                                ))}
                            </ul>
                        )}
                    </div>
                )}

                {pagina === 'estatisticas' && (
                    <div className="statsDiv">
                        <h1>Estatísticas</h1>
                    </div>
                )}

            </div>

        </>
        
    )

}

export default Menu