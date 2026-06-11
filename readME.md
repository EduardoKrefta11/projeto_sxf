## CSXF

![NodeJS](https://img.shields.io/badge/node.js-6DA55F.svg?style=for-the-badge&logo=node.js&logoColor=white)
![Vite](https://img.shields.io/badge/vite-%23646CFF.svg?style=for-the-badge&logo=vite&logoColor=white)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![TypeScript](https://img.shields.io/badge/typescript-%23007ACC.svg?style=for-the-badge&logo=typescript&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white)


## Sobre CSXF
CSXF é um aplicativo Web desenvolvido com o objetivo de auxiliar pesquisadores da Síndrome da X Frágil a terem um ambiente eficiente, acessível e de baixo custo para o gerenciamento de dados e pacientes.
Com uma interface simples e responsiva, buscamos fornecer a ferramenta de mais fácil uso para qualquer pessoa que se interessa na pesquisa da Síndrome.

## Ferramentas de desenvolvimento

### SO
Windows 25H2 (Compilação do Sistema Operacional 26200.8655)

### Frontend
- Node.js 22.20.0
- Vite 8.0.16
- TypeScript 6.0.3
- React 19.2.7
- React DOM 19.2.7
- React Router DOM 7.17.0
- Chart.js 4.5.1
- React-ChartJS-2 5.3.1

### Backend
- Python 3.14.4
- pip 26.1.2
- Flask 3.1.3
- Bcrypt 5.0.0
- PyMySQL 1.2.0
- Flask-cors 6.0.2
- Werkzeug 3.1.8
- Reportlab 4.5.1

### Banco de Dados
- MySQL Server 8.0.43
- MySQL Workbench 8.0.43

## Métodos de Instalação
### Instalação Frontend
Node JS - Instalação no site oficial: https://nodejs.org/en/download
Vite - 
```bash
npm create vite@latest
```
Digite um nome qualquer para a pasta do projeto
Ao ser perguntando qual tecnologia usar, escolha React
Ao ser perguntando na variação da linguagem, escolha TypeScript
```bash
cd ../sxf/sxf_pjbl
npm install
```
Pronto! Agora para rodar, basta rodar o seguinte comando dentro do terminal do aplicativo
```bash
npm run dev
```

# Instalação Backend
```bash
cd ../sxf/server
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
pip install flask flask-cors pymysql bcrypt reportlab
python main.py
```

## Licença
### Educacional e não comercional
