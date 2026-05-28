import { useState } from 'react'
import './Menu.css'

function MenuButton({ texto, onClick} : {texto: string, onClick: any} ) {
    return (
        <button className="menuButton" onClick={onClick}>
            {texto}
        </button>
    )
}

function Menu() {

    const [texto, setTexto] = useState('')

    function setHome() {
        setTexto('Botão de Home funcionando');
    }

    function setPacientes() {
        console.log('Botão de Pacientes funcionando');
    }

    function setEstatisticas() {
        console.log("Botão de Estatísticas funcionando");
    }

    return (
        <>
            <div className="interfaceSuperior">
                <MenuButton texto="Home" onClick={setHome}/>
                <MenuButton texto="Pacientes" onClick={setPacientes}/>
                <MenuButton texto="Estatisticas" onClick={setEstatisticas}/>
            </div>

            <p className="TextoDebug">{texto}</p>
        </>
        
    )

}

export default Menu