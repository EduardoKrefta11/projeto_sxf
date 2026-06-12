# CSXF

![NodeJS](https://img.shields.io/badge/node.js-6DA55F.svg?style=for-the-badge&logo=node.js&logoColor=white)
![Vite](https://img.shields.io/badge/vite-%23646CFF.svg?style=for-the-badge&logo=vite&logoColor=white)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![TypeScript](https://img.shields.io/badge/typescript-%23007ACC.svg?style=for-the-badge&logo=typescript&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white)

## Sumário

- [Sobre CSXF](#sobre-csxf)
- [Ferramentas de Desenvolvimento](#ferramentas-de-desenvolvimento)
- [Funcionalidades](#funcionalidades)
- [Capturas de Tela](#capturas-de-tela)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Métodos de Instalação](#métodos-de-instalação)
- [Configuração Banco de Dados](#configuração-banco-de-dados)
- [Endpoints Principais](#endpoints-principais)
- [Versão](#versão)
- [Equipe](#equipe)
- [Licença](#licença)

## Sobre CSXF
CSXF é um aplicativo Web desenvolvido com o objetivo de auxiliar pesquisadores da Síndrome da X Frágil a terem um ambiente eficiente, acessível e de baixo custo para o gerenciamento de dados e pacientes.
Com uma interface simples e responsiva, buscamos fornecer a ferramenta de mais fácil uso para qualquer pessoa interessada na pesquisa da Síndrome.

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

## Funcionalidades
### Autenticação e Controle de Acesso
- Login seguro com autenticação por sessão.
- Controle de acesso baseado em perfis de usuário.
- Diferenciação entre usuários Administradores (ADM) e Pesquisadores (COM).
- Encerramento seguro de sessão (logout).

### Gerenciamento de Usuários
- Cadastro de novos pesquisadores.
- Edição de informações de usuários.
- Exclusão de usuários do sistema.
- Upload e atualização de foto de perfil.

### Gerenciamento de Pacientes
- Cadastro de pacientes.
- Edição de informações cadastrais.
- Exclusão de pacientes.
- Upload e atualização de foto de perfil.
- Associação de pacientes a pesquisadores responsáveis.

### Gerenciamento de Consultas
- Registro de novas consultas.
- Histórico completo de consultas por paciente.
- Associação de sintomas às consultas realizadas.
- Visualização de informações clínicas registradas.

### Gerenciamento de Sintomas
- Cadastro de sintomas.
- Edição de sintomas existentes.
- Remoção de sintomas.
- Associação de múltiplos sintomas a uma consulta.

### Estatísticas e Relatórios
- Geração de gráficos estatísticos.
- Filtros por sexo, faixa etária, sintomas e pontuação.
- Análise de dados para apoio à pesquisa científica.
- Exportação de relatórios estatísticos em PDF.
- Inclusão automática de gráficos nos relatórios gerados.

### Relatórios de Pacientes
- Geração de relatório individual em PDF.
- Histórico completo de consultas do paciente.
- Registro dos sintomas observados em cada consulta.

### Interface e Usabilidade
- Interface responsiva para diferentes dispositivos.
- Navegação intuitiva para pesquisadores.
- Atualização dinâmica de dados.
- Visualização rápida de informações relevantes para pesquisa.

## Capturas de Tela

## Estrutura do Projeto

```text
CSXF/
├── server/              # Backend Flask
│   ├── main.py
│   ├── admin_api.py
│   ├── menu.py
│   ├── db.py
│   └── uploads/
│
├── sxf_pjbl/            # Frontend React
│   ├── src/
│   └── public/
│
└── README.md
```

### Descrição dos Diretórios

| Diretório | Finalidade |
|------------|------------|
| `server/` | Backend da aplicação desenvolvido em Flask |
| `sxf_pjbl/` | Frontend desenvolvido com React e TypeScript |
| `uploads/` | Armazenamento de fotos de perfil |

## Métodos de Instalação
### Frontend
#### Node JS - Instalação no site oficial: https://nodejs.org/en/download

#### Vite
```bash
npm create vite@latest
```
Digite um nome qualquer para a pasta do projeto.

Ao ser perguntando qual tecnologia usar, escolha React.

Ao ser perguntando na variação da linguagem, escolha TypeScript.
```bash
cd ../sxf/sxf_pjbl
npm install
```
Pronto! Agora para rodar, basta rodar o seguinte comando dentro do terminal do aplicativo
```bash
npm run dev
```

### Backend

#### Python - Instalação no site oficial: https://www.python.org/downloads/

*IMPORTANTE* - Lembre de marcar "ADD Python to PATH" Durante a instalação

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

## Configuração Banco de Dados

## Instalação do Banco de Dados
Acesse o site oficial do MySQL e instale o Server: https://dev.mysql.com/downloads/mysql/8.0.html

Após instalar o server, instale o MySQL Workbench: https://dev.mysql.com/downloads/workbench/

O MySQL Server é necessário para fazer funcionar o SQL dentro do computador local. Já o MySQL Workbench é 
essencial para manusear o banco de dados do sistema.

## Variáveis de Ambiente

Crie as seguintes variáveis:

| Variável | Descrição |
|-----------|-----------|
| FLASK_SECRET | Chave secreta utilizada para sessões |
| DB_HOST | localhost |
| DB_USER | flaskuser |
| DB_PASSWORD | sua_senha_mysql |
| DB_NAME | db_sxf |

## Resumo de Instalação

1. Instale Node.js.
2. Instale Python.
3. Instale MySQL Server e MySQL Workbench.
4. Crie o banco de dados `db_sxf`.
5. Configure as variáveis de ambiente.
6. Inicie o backend com `python main.py`.
7. Inicie o frontend com `npm run dev`.

## Endpoints Principais

A API utiliza autenticação baseada em sessão através do Flask. Após realizar login, o navegador armazenará um cookie de sessão que será utilizado para autenticar as requisições subsequentes.

Existem dois perfis de acesso:

- ADM (Administrador)
- COM (Pesquisador)

### Endpoint de Login
| Método | Rota | Descrição |
|----------|--------|-----------|
| POST | /api/login | Permite ao usuário se logar dentro do sistema |
| POST | /api/logout| Permite aos usuários saírem de seus logins |

### Endpoint do Pesquisador
| Método | Rota | Descrição |
|----------|--------|-----------|
| GET | /api/buscar_perfil | Retorna as informações do usuário atualmente autenticado |
| POST | /api/user_pfp| Permite ao usuário comum colocar uma foto de perfil |
| POST | /api/paciente_pfp| Permite alterar a foto de perfil dos pacientes |
| POST/GET | /api/meus_pacientes| Busca os pacientes relacionados ao usuário comum logado |
| POST | /api/paciente_nova_consulta| Permite ao usuário criar uma nova consulta |
| GET | /api/pdf/paciente/<int:paciente_id>| Permite gerar um PDF das consultas de um paciente |
| GET | /api/buscar_sintomas| Busca os sintomas para exibição no Frontend |
| GET | /api/stats| Busca estatísticas com base nos parâmetros informados para exibição no Frontend |
| GET | /api/pdf/stats| Permite gerar um PDF dos gráficos gerados no Frontend |
| - | /uploads/perfis/<filename>| Retorna a foto de perfil do usuário |
| - | /uploads/pacientes/<filename>| Retorna a foto de perfil do paciente |

### Endpoint de Administrador
| Método | Rota | Descrição |
|----------|--------|-----------|
| GET/POST | /api/usuarios | Busca e permite criar usuários do sistema |
| PUT/DELETE | /api/usuarios/<int:id>| Permite alterar os usuários do sistema |
| GET/POST | /api/pacientes| Busca e permite criar pacientes do sistema |
| PUT/DELETE | /api/pacientes/<int:id>| Permite alterar os pacientes do sistema |
| GET/POST | /api/sintomas| Permite visualizar e alterar os sintomas do sistema |
| GET | /api/admin/consultas| Permite visualizar as consultas do sistema |

## Versão

Versão atual: 1.0.0

Última atualização: Junho de 2026

## Equipe

Desenvolvido por:

- Nicolas Alonso de Oliveira
- Eduardo Henrique Krefta de Albuquerque

Instituição: PUCPR - Pontifícia Universidade Católica do Paraná

Ano: 2026

## Licença
### Educacional e não comercial