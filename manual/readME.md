# Manual de Instruções de Uso

- [Instruções para uso Comum](#instruções-para-uso-comum)
- [Instruções para manutenção ou alteração de código](#instruções-para-manutenção-ou-alteração-do-código)
- [Menu (Usuário Comum)](#menu_(usuário_comum))
- [Administrador (Usuário Administrador)](#administrador-usuário-administrador)

## Instruções para uso comum

---

## Tela de Login

Ao iniciar o aplicativo Web, o usuário é apresentado a tela de login

![Tela de Login](login.png)

Primeiro, vamos olhar a tela do usuário comum. Para testes de visualização:

| Usuário | Senha |
|---------|------------|
| admin | 123 |
| comum | 123 |

---

## Menu

A página do usuário comum. É onde o pesquisador pode visualizar o perfil, seus pacientes e gráficos. Além disso, ele pode criar novos pacientes e consultas além de gerar relatórios em PDF de ambos os paciente quanto dos gráficos.

---

### Home

Ao logar, o usuário comum é apresentado a página **Home**, onde seu perfil de usuário é mostrado, contendo:

- Username
- Nome
- Foto de Perfil
- Data de Nascimento
- Data de Criação

![Página Home](home.png)

Opcionalmente, ao clicar no botão com uma camêra, o usuário pode fazer o upload de uma foto de perfil. Após escolher a foto, basta clicar em salvar foto para armazená-la no banco. Na próxima vez que o usuário logar, estará com a foto atualizada

![Foto de Perfil](pfp.png)

---

### Pacientes

Clicando no botão **Pacientes** na interface superior redireciona o usuário a seção de 'Pacientes', onde ele pode:

* Visualizar a lista de pacientes associada a ele com ou sem filtração

![Lista de Pacientes](paciente.png)

![Filtro de Pacientes](filtro_paciente.png)

* Adicionar novos pacientes e novas consultas aos pacientes existentes

![Novo Paciente](novo_paciente.png)

![Nova Consulta](nova_consulta.png)

* Gerar relatórios em PDFs dos Pacientes e suas consultas

![Relatório PDF](relatorio_paciente.png)

---

### Estatísticas

Clicando no botão **Estatísticas** na interface superior redireciona o usuário a seção de 'Estatísticas'

![Seção de Estatísticas](stats.png)

Dentro dessa seção ele pode:

* Montar e visualizar gráficos por organização (Sexo biológico, sintoma, peso médio) e por parametrização (Sexo biológico, 
nascimento Mínimo/Máximo, sintomas e pontuação Mínima/Máxima)

#### Exemplo de gráfico com

| Organização | Parâmetros |
|---------|------------|
| Sintoma | Sexo Biológico = Masculino |

![Gráfico 1](grafico_sintoma.png)

| Organização | Parâmetros |
|---------|------------|
| Sexo biológico | - |

![Gráfico 2](grafico_sexo_biologico.png)

* Gerar relatórios com informações diversas acerca dos gráficos gerados

![Relatório PDF Gráfico](relatorio_grafico.png)

---

### Sair

Realiza o logout do usuário do sistema, reiniciando a sessão e levando o usuário novamente a tela de login.

---

## Admin

A página do usuário administrador. Aqui, o usuário tem a possibilidade de manusear os mais diversos dados acerca do sistema, como usuários, pacientes, consultas e sintomas.

---

### Usuarios

![Usuarios Admin](admin_usuarios.png)

![Novo Usuário Admin](admin_novo_usuario.png)

---

### Pacientes

![Pacientes Admin](admin_pacientes.png)

![Novo Paciente Admin](admin_novo_paciente.png)

---

### Sintomas

![Sintomas Admin](admin_sintomas.png)

![Novo Sintoma Admin](admin_novo_sintoma.png)

---

### Consultas

![Consultas Admin](admin_consultas.png)

![Nova Consulta Admin](admin_nova_consulta.png)

---

### Sair

Realiza o logout do usuário do sistema, reiniciando a sessão e levando o usuário novamente a tela de login.

---

## Instruções para manutenção ou alteração de código

Abaixo estão datalhados todos os detalhes acerca do código usado tanto no Frontend e Backend do aplicativo Web além de instruções acerca do Banco de Dados usado em sua construção.

## Frontend

### Página de Login (App.tsx - App.css)

O arquivo **App.tsx** é responsável pela autenticação inicial dos usuários do sistema. A página apresenta um formulário de login onde o usuário informa suas credenciais para acessar a plataforma.

Em seu código são utilizados três estados principais:

| Estado    | Finalidade                                                      |
| --------- | --------------------------------------------------------------- |
| `user`    | Armazena o nome de usuário informado no formulário.             |
| `senha`   | Armazena a senha digitada pelo usuário.                         |
| `message` | Exibe mensagens de retorno da autenticação ou erros de conexão. |

---

#### Formulário de Login

A interface é composta por:

* Campo de nome de usuário.
* Campo de senha.
* Botão de autenticação.
* Área para exibição de mensagens de retorno.

Os campos são controlados através do React utilizando `useState`, garantindo sincronização entre os valores digitados e o estado da aplicação.

---

#### Função preventReload(e)

A função **preventReload()** é executada quando o formulário é submetido.

Seu principal objetivo é impedir o recarregamento da página e realizar a autenticação do usuário junto ao servidor.

Ela recebe como parâmetro:

| Parâmetro | Finalidade                         |
| --------- | ---------------------------------- |
| `e`       | Evento de submissão do formulário. |

Funcionamento da função:

1. Interrompe o comportamento padrão do formulário através de `e.preventDefault()`.
2. Envia uma requisição HTTP `POST` para a rota `/api/login`.
3. Encaminha para a API:

   * Nome de usuário;
   * Senha.
4. Aguarda a resposta do servidor.
5. Atualiza a mensagem exibida ao usuário com o conteúdo retornado pela API.
6. Verifica se a autenticação foi realizada com sucesso.
7. Caso autenticado:

   * Usuários administradores (`ADM`) são redirecionados para `/admin`;
   * Usuários comuns são redirecionados para `/user`.
8. Caso ocorra falha de comunicação com o servidor, uma mensagem de erro é exibida ao usuário.

---

#### Fluxo de Autenticação

1. Usuário acessa a tela de login.
2. Informa nome de usuário e senha.
3. Pressiona o botão **Logar**.
4. O formulário dispara a função `preventReload()`.
5. Uma requisição é enviada para `/api/login`.
6. O backend valida as credenciais.
7. O sistema recebe a resposta:

   * Sucesso → redirecionamento para a área correspondente.
   * Falha → mensagem de erro exibida.
8. A sessão é mantida através de cookies utilizando `credentials: 'include'`.

---

#### Navegação

A navegação é realizada através do hook `useNavigate()` do React Router.

Rotas utilizadas:

| Rota     | Finalidade                      |
| -------- | ------------------------------- |
| `/admin` | Área administrativa do sistema. |
| `/user`  | Área do usuário comum.          |
|          |                                 |


### Página do Usuário (User.tsx)

O arquivo **User.tsx** é responsável pelas funcionalidades disponíveis para usuários comuns do sistema. Nesta página são realizadas operações relacionadas ao gerenciamento de pacientes, consultas, sintomas, perfil do usuário e visualização de estatísticas.

---

#### Bibliotecas Utilizadas

| Biblioteca         | Finalidade                                                |
| ------------------ | --------------------------------------------------------- |
| `react`            | Gerenciamento de estados e ciclo de vida dos componentes. |
| `react-router-dom` | Navegação entre páginas da aplicação.                     |
| `chart.js`         | Criação e configuração dos gráficos estatísticos.         |
| `react-chartjs-2`  | Integração dos gráficos Chart.js com React.               |

Antes da utilização dos gráficos, os componentes necessários do Chart.js são registrados através do método `ChartJS.register()`, permitindo a renderização dos diferentes tipos de gráficos utilizados pelo sistema.

---

#### Componente Auxiliar: MenuButton

O componente **MenuButton** é responsável pela criação dos botões de navegação da interface superior.

Ele recebe dois parâmetros:

| Parâmetro | Finalidade                           |
| --------- | ------------------------------------ |
| `texto`   | Texto exibido no botão.              |
| `onClick` | Função executada ao clicar no botão. |

Esse componente é utilizado para padronizar a aparência e o comportamento dos botões de navegação da interface.

---

#### Estados Relacionados à Navegação

| Estado   | Finalidade                                           |
| -------- | ---------------------------------------------------- |
| `pagina` | Controla qual seção da aplicação está sendo exibida. |
| `erro`   | Armazena mensagens de erro exibidas ao usuário.      |

---

#### Estados Relacionados ao Perfil

| Estado    | Finalidade                                          |
| --------- | --------------------------------------------------- |
| `perfil`  | Armazena os dados do perfil do usuário autenticado. |
| `userPFP` | Armazena a foto de perfil do usuário.               |

---

#### Estados Relacionados aos Pacientes

| Estado                | Finalidade                                                  |
| --------------------- | ----------------------------------------------------------- |
| `pacientes`           | Lista de pacientes cadastrados.                             |
| `pacientePFP`         | Foto associada ao paciente selecionado.                     |
| `mostrarFormPaciente` | Controla a exibição do formulário de cadastro de pacientes. |
| `pacienteSexo`        | Filtro de sexo dos pacientes.                               |
| `pacienteDataMin`     | Data mínima utilizada nos filtros de pesquisa.              |
| `pacienteDataMax`     | Data máxima utilizada nos filtros de pesquisa.              |
| `pacienteScoreMin`    | Pontuação mínima utilizada nos filtros.                     |
| `pacienteScoreMax`    | Pontuação máxima utilizada nos filtros.                     |
| `novoPaciente`        | Armazena os dados do paciente que será cadastrado.          |

O objeto `novoPaciente` contém:

| Campo            | Finalidade                      |
| ---------------- | ------------------------------- |
| `nome`           | Nome completo do paciente.      |
| `cpf`            | CPF do paciente.                |
| `sexo`           | Sexo informado no cadastro.     |
| `dataNascimento` | Data de nascimento do paciente. |

---

#### Estados Relacionados às Consultas

| Estado                  | Finalidade                                          |
| ----------------------- | --------------------------------------------------- |
| `mostrarFormConsulta`   | Controla a exibição do formulário de consultas.     |
| `idPacienteSelecionado` | Identifica o paciente selecionado para atendimento. |
| `sintomasSelecionados`  | Lista dos sintomas associados à consulta.           |
| `observacao`            | Observações registradas durante a consulta.         |
| `tipoExame`             | Tipo de exame solicitado para o paciente.           |

---

#### Estados Relacionados às Estatísticas

| Estado                   | Finalidade                                                    |
| ------------------------ | ------------------------------------------------------------- |
| `tipoGrafico`            | Define o tipo de gráfico exibido.                             |
| `organizacao`            | Define o agrupamento utilizado nas estatísticas.              |
| `sintomasBuscados`       | Lista de sintomas utilizados nos filtros estatísticos.        |
| `sintoma`                | Sintoma selecionado para pesquisa.                            |
| `pontuacaoMin`           | Pontuação mínima utilizada nos filtros.                       |
| `pontuacaoMax`           | Pontuação máxima utilizada nos filtros.                       |
| `sexo`                   | Filtro de sexo aplicado às estatísticas.                      |
| `nascimentoMin`          | Data mínima de nascimento utilizada nos filtros.              |
| `nascimentoMax`          | Data máxima de nascimento utilizada nos filtros.              |
| `dadosEstatisticos`      | Dados retornados pela API para geração dos gráficos.          |
| `carregandoEstatisticas` | Indica se uma consulta estatística está em andamento.         |
| `filtrosAplicados`       | Indica se filtros já foram aplicados na pesquisa estatística. |

A variável `dadosEstatisticos` armazena:

| Campo     | Finalidade                                |
| --------- | ----------------------------------------- |
| `labels`  | Rótulos exibidos nos gráficos.            |
| `valores` | Valores numéricos associados aos rótulos. |

---

#### Referências (useRef)

| Referência | Finalidade|
|------------|-----------|
| graficoRef | Referência direta ao gráfico renderizado, permitindo operações como exportação, atualização ou captura da imagem gerada.

---

#### Funções de Formatação

O sistema possui funções auxiliares responsáveis por converter datas armazenadas pelo backend para um formato amigável ao usuário.

##### formatarData(dataString)

A função **formatarData()** recebe uma data e a converte para o padrão brasileiro (`dd/mm/aaaa`).

Funcionamento:

1. Verifica se a data foi informada.
2. Caso a data esteja vazia, retorna `"-"`.
3. Converte a string para um objeto `Date`.
4. Retorna a data formatada utilizando o padrão brasileiro.

Essa função é utilizada principalmente na exibição de informações cadastrais dos pacientes.

---

##### formatarDataHora(dataString)

A função **formatarDataHora()** realiza a conversão de uma data contendo horário para o formato brasileiro.

Funcionamento:

1. Verifica se a data foi informada.
2. Caso esteja vazia, retorna `"-"`.
3. Converte a string recebida para um objeto `Date`.
4. Retorna a data e hora formatadas utilizando o padrão brasileiro.

Essa função é utilizada principalmente na exibição do histórico de consultas e registros realizados pelo sistema.

---

#### Envio de Foto de Perfil do Usuário

##### enviarFotoPerfil()

A função **enviarFotoPerfil()** é responsável por realizar o upload da foto de perfil do usuário autenticado.

Fluxo de execução:

1. Verifica se um arquivo foi selecionado.
2. Caso nenhum arquivo tenha sido escolhido, exibe uma mensagem de alerta.
3. Cria um objeto `FormData`.
4. Adiciona a imagem selecionada ao formulário.
5. Envia uma requisição `POST` para a rota `/api/user_pfp`.
6. A imagem é processada e armazenada pelo backend.
7. A resposta retornada pela API é recebida pelo frontend.

A comunicação é realizada utilizando `multipart/form-data`, formato adequado para transferência de arquivos.

---

#### Envio de Foto de Paciente

##### enviarPacienteFoto(paciente)

A função **enviarPacienteFoto()** é responsável por realizar o upload da foto associada a um paciente.

Parâmetros:

| Parâmetro  | Finalidade                                        |
| ---------- | ------------------------------------------------- |
| `paciente` | Objeto contendo os dados do paciente selecionado. |

Fluxo de execução:

1. Verifica se uma imagem foi selecionada.
2. Caso não exista arquivo selecionado, exibe um alerta ao usuário.
3. Cria um objeto `FormData`.
4. Adiciona:

   * A foto do paciente;
   * O identificador do paciente.
5. Envia uma requisição `POST` para a rota `/api/paciente_pfp`.
6. O backend associa a imagem ao paciente correspondente.
7. A resposta da API é recebida pelo frontend.

---

#### Hooks de Inicialização (useEffect)

O componente utiliza diversos hooks `useEffect()` para automatizar carregamentos de dados e atualizações da interface.

---

##### Carregamento Inicial de Sintomas

```text
Dependências: []
```

Executado apenas uma vez durante a montagem do componente.

Fluxo:

1. O componente é carregado.
2. A função `buscarSintomas()` é executada.
3. A lista de sintomas disponível no sistema é carregada para utilização em consultas e filtros.

---

##### Limpeza de Mensagens de Erro

```text
Dependências: [pagina]
```

Executado sempre que o usuário navega entre as páginas internas do sistema.

Fluxo:

1. O valor de `pagina` é alterado.
2. A mensagem armazenada em `erro` é limpa.
3. A nova tela é exibida sem mensagens antigas.

---

##### Carregamento do Perfil do Usuário

```text
Dependências: [pagina]
```

Executado sempre que a seção atual corresponde à página inicial (`home`).

Fluxo:

1. O usuário acessa a página inicial.
2. Uma requisição é enviada para `/api/meu_perfil`.
3. O backend valida a sessão do usuário.
4. Os dados do perfil são retornados.
5. O estado `perfil` é atualizado.
6. Em caso de falha ou sessão inválida, uma mensagem de erro é exibida.

---

##### Atualização Automática da Lista de Pacientes

```text
Dependências:
[
    pagina,
    pacienteSexo,
    pacienteDataMin,
    pacienteDataMax,
    pacienteScoreMin,
    pacienteScoreMax
]
```

Executado sempre que algum filtro relacionado aos pacientes é alterado.

Fluxo:

1. O usuário acessa a seção de pacientes.
2. O sistema verifica alterações nos filtros.
3. A função `buscarPacientes()` é executada.
4. Uma nova consulta é enviada ao backend.
5. A lista de pacientes é atualizada automaticamente de acordo com os critérios selecionados.

Esse mecanismo garante que a listagem permaneça sincronizada com os filtros aplicados sem necessidade de atualização manual.

---

#### Gerenciamento de Pacientes

##### buscarPacientes()

A função **buscarPacientes()** é responsável por consultar todos os pacientes vinculados ao usuário autenticado.

Antes da consulta, a função monta dinamicamente os filtros selecionados pelo usuário através do objeto `URLSearchParams`.

Filtros suportados:

| Filtro     | Finalidade                    |
| ---------- | ----------------------------- |
| `sexo`     | Filtrar pacientes por sexo.   |
| `dataMin`  | Data mínima de nascimento.    |
| `dataMax`  | Data máxima de nascimento.    |
| `scoreMin` | Pontuação mínima do paciente. |
| `scoreMax` | Pontuação máxima do paciente. |

Fluxo de execução:

1. Cria um objeto de parâmetros da URL.
2. Adiciona os filtros preenchidos pelo usuário.
3. Envia uma requisição para `/api/meus_pacientes`.
4. O backend processa os filtros recebidos.
5. A lista de pacientes é retornada.
6. O estado `pacientes` é atualizado.
7. Em caso de erro, uma mensagem é exibida ao usuário.

---

#### Gerenciamento de Sintomas

##### buscarSintomas()

A função **buscarSintomas()** é responsável por obter a lista completa de sintomas cadastrados no sistema.

Fluxo de execução:

1. Envia uma requisição para `/api/buscar_sintomas`.
2. O backend retorna todos os sintomas disponíveis.
3. Os dados recebidos são armazenados em `sintomasBuscados`.
4. Esses dados passam a ser utilizados pelos formulários e filtros da aplicação.
5. Em caso de erro, uma mensagem é exibida ao usuário.

Essa função é executada automaticamente durante a inicialização do componente.

---

#### Registro de Consultas

##### salvarConsulta(e)

A função **salvarConsulta()** é responsável por registrar uma nova consulta para um paciente. Ela previne que o usuário cadastre um usuário sem marcar nenhum sintoma ou sem tipo de exame.

Parâmetros:

| Parâmetro | Finalidade                         |
| --------- | ---------------------------------- |
| `e`       | Evento de submissão do formulário. |

Dados enviados para a API:

| Campo        | Finalidade                                     |
| ------------ | ---------------------------------------------- |
| `idPaciente` | Identificador do paciente atendido.            |
| `sintomas`   | Lista de sintomas selecionados.                |
| `observacao` | Observações registradas durante o atendimento. |
| `tipoExame`  | Tipo de exame solicitado.                      |

Fluxo de execução:

1. Impede o recarregamento da página.
2. Envia uma requisição `POST` para `/api/paciente_nova_consulta`.
3. O backend registra a consulta.
4. O sistema valida se ao menos um sintoma foi selecionado.
5. Em caso de sucesso:

   * O formulário é fechado;
   * A lista de sintomas selecionados é limpa;
   * O campo de observações é reiniciado.
6. Em caso de erro, uma mensagem é exibida ao usuário.

O objetivo dessa função é centralizar o processo de criação de consultas médicas associadas aos pacientes cadastrados.

---

#### Construção de Parâmetros Estatísticos

##### montarParametrosEstatisticas(opcoes)

A função **montarParametrosEstatisticas()** é responsável por construir os filtros utilizados pelas consultas estatísticas do sistema.

Ela centraliza a criação dos parâmetros enviados para as rotas relacionadas aos gráficos e relatórios.

Filtros suportados:

| Filtro          | Finalidade                                           |
| --------------- | ---------------------------------------------------- |
| `organizacao`   | Define o agrupamento dos dados.                      |
| `sexo`          | Filtra registros por sexo.                           |
| `nascimentoMin` | Define a data mínima de nascimento.                  |
| `nascimentoMax` | Define a data máxima de nascimento.                  |
| `sintoma`       | Filtra registros associados a um sintoma específico. |
| `pontuacaoMin`  | Define a pontuação mínima.                           |
| `pontuacaoMax`  | Define a pontuação máxima.                           |
| `tipoGrafico`   | Define o formato de visualização dos dados.          |

Fluxo de execução:

1. Cria um objeto `URLSearchParams`.
2. Adiciona os filtros preenchidos pelo usuário.
3. Verifica se o tipo de gráfico deve ser incluído.
4. Retorna o conjunto de parâmetros formatados para utilização nas requisições.

Essa abordagem evita duplicação de código nas operações estatísticas.

---

#### Carregamento de Estatísticas

##### carregarEstatisticas()

A função **carregarEstatisticas()** é responsável por obter os dados estatísticos utilizados na geração dos gráficos do sistema.

Fluxo de execução:

1. Ativa o indicador de carregamento.
2. Remove mensagens de erro anteriores.
3. Gera os parâmetros de pesquisa através da função `montarParametrosEstatisticas()`.
4. Envia uma requisição para `/api/stats`.
5. O backend processa os filtros recebidos.
6. Os dados estatísticos são retornados.
7. O estado `dadosEstatisticos` é atualizado.
8. O gráfico é renderizado utilizando os novos dados.
9. Ao término da operação, o indicador de carregamento é desativado.
10. Em caso de erro, uma mensagem é exibida ao usuário.

---

#### Fluxo de Geração de Estatísticas

1. O usuário acessa a seção de estatísticas.
2. Seleciona os filtros desejados.
3. Escolhe a forma de organização dos dados.
4. Solicita a geração dos resultados.
5. O frontend monta os parâmetros da consulta.
6. A API processa os filtros informados.
7. Os dados consolidados são retornados.
8. O sistema atualiza o estado `dadosEstatisticos`.
9. Os gráficos são renderizados utilizando Chart.js.

---

#### Utilitários de Cadastro

##### aplicarMascaraCPF(valor)

A função **aplicarMascaraCPF()** é responsável por formatar automaticamente o CPF informado pelo usuário durante o cadastro de pacientes.

Formato aplicado:

```text
000.000.000-00
```

Fluxo de execução:

1. Remove caracteres que não sejam números.
2. Insere automaticamente os pontos de separação.
3. Insere o hífen antes dos dois últimos dígitos.
4. Limita o tamanho máximo para 14 caracteres.
5. Retorna o CPF formatado para exibição.

Essa função é utilizada apenas para melhorar a experiência do usuário durante o preenchimento dos formulários.

---

#### Cadastro de Pacientes

##### salvarPaciente(e)

A função **salvarPaciente()** é responsável pelo cadastro de novos pacientes vinculados ao usuário autenticado.

Parâmetros:

| Parâmetro | Finalidade                         |
| --------- | ---------------------------------- |
| `e`       | Evento de submissão do formulário. |

Fluxo de execução:

1. Impede o recarregamento da página.
2. Limpa mensagens de erro anteriores.
3. Remove a formatação do CPF antes do envio.
4. Cria um objeto contendo os dados do paciente.
5. Envia uma requisição `POST` para `/api/meus_pacientes`.
6. O backend registra o novo paciente.
7. Em caso de sucesso:

   * O formulário é fechado;
   * Os campos são reinicializados;
   * A lista de pacientes é atualizada automaticamente.
8. Em caso de erro, uma mensagem é exibida ao usuário.

---

#### Aplicação de Filtros Estatísticos

##### aplicarFiltros()

A função **aplicarFiltros()** é responsável por iniciar uma nova consulta estatística utilizando os filtros selecionados pelo usuário.

Fluxo de execução:

1. Marca que filtros foram aplicados.
2. Remove resultados estatísticos anteriores.
3. Executa a função `carregarEstatisticas()`.
4. Atualiza os gráficos com os novos dados retornados pela API.

Essa função atua como ponto de entrada para a geração das estatísticas.

---

#### Captura de Imagem do Gráfico

##### obterImagemGrafico()

A função **obterImagemGrafico()** é responsável por converter o gráfico exibido em uma imagem no formato Base64.

Fluxo de execução:

1. Obtém a referência do gráfico através de `graficoRef`.
2. Verifica se o gráfico está disponível.
3. Executa o método `toBase64Image()`.
4. Retorna a imagem gerada.
5. Caso o gráfico não exista, retorna `null`.

Essa imagem é posteriormente utilizada na geração dos relatórios em PDF.

---

#### Geração de Relatórios Estatísticos

##### gerarRelatorioEstatistico()

A função **gerarRelatorioEstatistico()** é responsável pela criação e download do relatório estatístico em formato PDF.

Dados enviados para geração do relatório:

| Campo                 | Finalidade                       |
| --------------------- | -------------------------------- |
| `sexo`                | Filtro de sexo aplicado.         |
| `nascimentoMin`       | Data mínima de nascimento.       |
| `nascimentoMax`       | Data máxima de nascimento.       |
| `sintoma`             | Sintoma utilizado no filtro.     |
| `pontuacaoMin`        | Pontuação mínima.                |
| `pontuacaoMax`        | Pontuação máxima.                |
| `organizacao`         | Tipo de agrupamento estatístico. |
| `tipoGrafico`         | Formato de gráfico selecionado.  |
| `imagemGraficoBase64` | Imagem do gráfico gerado.        |

Fluxo de execução:

1. Captura a imagem do gráfico exibido.
2. Monta o objeto contendo filtros e configurações.
3. Envia uma requisição `POST` para `/api/pdf/stats`.
4. O backend gera o relatório PDF.
5. O arquivo é retornado ao navegador.
6. O frontend cria um link temporário.
7. O download é iniciado automaticamente.
8. Os recursos temporários são removidos da memória.

Em caso de falha, uma mensagem de erro é exibida ao usuário.

---

#### Encerramento de Sessão

##### logout()

A função **logout()** é responsável por finalizar a sessão do usuário.

Fluxo de execução:

1. Envia uma requisição `POST` para `/api/logout`.
2. O backend invalida a sessão atual.
3. O usuário é redirecionado para a tela de login.
4. Caso ocorra algum erro, ele é registrado no console da aplicação.

---

#### Renderização de Gráficos

##### obterGrafico()

A função **obterGrafico()** é responsável por gerar dinamicamente o gráfico estatístico de acordo com a opção selecionada pelo usuário.

Antes da renderização, a função monta duas estruturas principais:

##### Configuração dos Dados

O objeto `chartConfig` contém:

| Campo             | Finalidade                                          |
| ----------------- | --------------------------------------------------- |
| `labels`          | Rótulos exibidos no gráfico.                        |
| `datasets`        | Conjunto de dados estatísticos retornados pela API. |
| `backgroundColor` | Cores utilizadas na visualização.                   |
| `borderColor`     | Cores das bordas dos elementos gráficos.            |

##### Configuração de Exibição

O objeto `opcoes` define características visuais do gráfico:

| Configuração | Finalidade                              |
| ------------ | --------------------------------------- |
| `responsive` | Ajusta o gráfico ao tamanho disponível. |
| `legend`     | Exibe a legenda dos dados apresentados. |

---

##### Tipos de Gráfico Disponíveis

| Tipo      | Componente Utilizado                                        |
| --------- | ----------------------------------------------------------- |
| `colunas` | Gráfico de colunas verticais (`Bar`).                       |
| `linhas`  | Gráfico de linhas (`Line`).                                 |
| `pizza`   | Gráfico de setores (`Pie`).                                 |
| `barras`  | Gráfico de barras horizontais (`Bar` com `indexAxis: 'y'`). |

---

#### Fluxo de Geração de Relatórios Estatísticos

1. O usuário seleciona os filtros desejados.
2. O sistema gera os dados estatísticos.
3. O gráfico é renderizado na interface.
4. O usuário solicita a geração do relatório.
5. O gráfico é convertido para imagem.
6. Os filtros e a imagem são enviados ao backend.
7. O PDF é gerado.
8. O arquivo é disponibilizado para download automático.

Esse fluxo garante que o relatório exportado contenha exatamente as mesmas informações apresentadas na interface do sistema.


---

### Estrutura da Interface

A interface principal da página é organizada em duas áreas:

1. **Interface Superior de Navegação**
2. **Área de Conteúdo Dinâmico**

O conteúdo exibido é controlado pelo estado `pagina`, permitindo alternar entre as diferentes funcionalidades disponíveis para o usuário.

---

#### Menu Superior

O menu superior é composto por botões de navegação construídos através do componente `MenuButton`.

| Botão        | Ação                                         |
| ------------ | -------------------------------------------- |
| Home         | Exibe as informações do perfil do usuário.   |
| Pacientes    | Exibe a área de gerenciamento de pacientes.  |
| Estatísticas | Exibe os gráficos e relatórios estatísticos. |
| Sair         | Finaliza a sessão do usuário.                |

Fluxo de navegação:

1. O usuário seleciona uma opção do menu.
2. O estado `pagina` é atualizado.
3. O React realiza uma nova renderização.
4. O conteúdo correspondente é exibido na tela.

---

### Seção Home

A seção **Home** é responsável pela exibição dos dados do usuário autenticado.

Essa tela é exibida quando:

```text
pagina === 'home'
```

---

#### Exibição do Perfil

Ao acessar a página inicial, os dados armazenados no estado `perfil` são apresentados ao usuário.

Caso os dados ainda estejam sendo carregados, o sistema exibe a mensagem:

```text
Carregando perfil...
```

Após o carregamento, um cartão de perfil é renderizado contendo as informações da conta.

---

#### Foto de Perfil

A foto do usuário é exibida através do componente de imagem.

Funcionamento:

1. O sistema verifica se existe uma foto cadastrada.
2. Caso exista, a imagem armazenada no servidor é exibida.
3. Caso contrário, é utilizada a imagem padrão definida em `defaultPFP`.

Fluxo:

1. Usuário acessa a página Home.
2. O sistema consulta os dados do perfil.
3. A foto cadastrada é carregada.
4. Caso não exista foto, uma imagem padrão é apresentada.

---

#### Alteração de Foto de Perfil

O sistema permite que o usuário altere sua foto de perfil diretamente pela interface.

Fluxo de atualização:

1. O usuário clica no botão de edição representado pelo ícone 📷.
2. O seletor de arquivos do navegador é aberto.
3. Uma imagem é selecionada.
4. O arquivo é armazenado no estado `userPFP`.
5. O usuário pressiona o botão **Salvar foto**.
6. A função `enviarFotoPerfil()` é executada.
7. O arquivo é enviado ao backend.
8. A nova foto passa a ser utilizada pelo sistema.

---

#### Informações Exibidas

O cartão de perfil apresenta os seguintes dados:

| Informação               | Origem                  |
| ------------------------ | ----------------------- |
| Nome                     | `perfil.nome`           |
| Nome de usuário          | `perfil.user`           |
| Data de nascimento       | `perfil.dataNascimento` |
| Data de criação da conta | `perfil.dataCriacao`    |

As datas são formatadas utilizando as funções auxiliares:

| Função               | Utilização              |
| -------------------- | ----------------------- |
| `formatarData()`     | Datas simples.          |
| `formatarDataHora()` | Datas contendo horário. |

---

#### Fluxo da Página Inicial

1. O usuário acessa a área Home.
2. O sistema executa a consulta do perfil.
3. Os dados retornados são armazenados em `perfil`.
4. O cartão de perfil é renderizado.
5. O usuário pode:

   * Visualizar suas informações;
   * Alterar sua foto de perfil;
   * Consultar dados da conta.
6. Caso ocorra algum erro durante o carregamento, a mensagem armazenada em `erro` é exibida na interface.

---

### Seção de Pacientes

A seção **Pacientes** concentra todas as funcionalidades relacionadas ao gerenciamento de pacientes cadastrados pelo usuário.

Essa tela é exibida quando:

```text
pagina === 'paciente'
```

As principais funcionalidades disponíveis são:

* Consulta de pacientes cadastrados.
* Aplicação de filtros de pesquisa.
* Cadastro de novos pacientes.
* Registro de consultas.
* Upload de foto do paciente.
* Emissão de relatório individual em PDF.

---

#### Filtros de Pesquisa

A interface disponibiliza filtros que permitem localizar pacientes específicos.

Filtros disponíveis:

| Filtro        | Finalidade                         |
| ------------- | ---------------------------------- |
| Sexo Biológico| Filtrar pacientes por gênero.      |
| Nascimento de | Definir data mínima de nascimento. |
| Até           | Definir data máxima de nascimento. |
| Score mínimo  | Filtrar por pontuação mínima.      |
| Score máximo  | Filtrar por pontuação máxima.      |

Sempre que um filtro é alterado, a função `buscarPacientes()` é executada automaticamente, atualizando a listagem exibida.

---

#### Limpeza de Filtros

O botão **Limpar** permite remover todos os filtros ativos.

Fluxo:

1. Remove o filtro de sexo.
2. Remove os limites de data de nascimento.
3. Remove os filtros de pontuação.
4. A lista de pacientes é atualizada automaticamente.

---

### Cadastro de Pacientes

O sistema permite o registro de novos pacientes através do botão **Criar Paciente**.

Ao ser acionado, o estado `mostrarFormPaciente` é alterado, tornando visível o formulário de cadastro.

---

#### Dados Cadastrais

Informações solicitadas:

| Campo              | Finalidade                      |
| ------------------ | ------------------------------- |
| Nome               | Nome completo do paciente.      |
| CPF                | Documento de identificação.     |
| Sexo Biológico     | Sexo do paciente.               |
| Data de Nascimento | Data de nascimento do paciente. |

Durante o preenchimento do CPF, a função `aplicarMascaraCPF()` realiza a formatação automática dos dados.

---

#### Fluxo de Cadastro

1. O usuário clica em **Criar Paciente**.
2. O formulário é exibido.
3. Os dados são preenchidos.
4. O botão **Salvar** executa a função `salvarPaciente()`.
5. O backend registra o paciente.
6. A listagem é atualizada automaticamente.
7. O formulário é ocultado.

Caso o usuário pressione **Cancelar**, os campos são limpos e o formulário é fechado.

---

### Registro de Consultas

A criação de consultas é realizada individualmente para cada paciente.

Ao selecionar **Nova Consulta**, o sistema:

1. Armazena o identificador do paciente.
2. Abre o formulário de consulta.
3. Limpa sintomas previamente selecionados.
4. Limpa observações anteriores.
5. Limpa informações de exames.

---

#### Formulário de Consulta

O formulário permite registrar informações clínicas relacionadas ao atendimento.

Campos disponíveis:

| Campo         | Finalidade                                 |
| ------------- | ------------------------------------------ |
| Sintomas      | Lista de sintomas associados ao paciente.  |
| Tipo de Exame | Exames solicitados durante a consulta.     |
| Observação    | Observações registradas pelo profissional. |

---

#### Seleção de Sintomas

Os sintomas são carregados através da função `buscarSintomas()`.

Cada sintoma é apresentado como uma caixa de seleção (*checkbox*).

Fluxo:

1. O usuário seleciona um sintoma.
2. O identificador é adicionado à lista `sintomasSelecionados`.
3. Caso o sintoma seja desmarcado, ele é removido da lista.
4. A seleção final é enviada ao backend durante o salvamento da consulta.

---

#### Fluxo de Registro de Consulta

1. O usuário seleciona um paciente.
2. Pressiona **Nova Consulta**.
3. Escolhe os sintomas observados.
4. Informa exames necessários.
5. Registra observações clínicas.
6. Pressiona **Salvar**.
7. A função `salvarConsulta()` é executada.
8. Os dados são enviados ao backend.
9. A consulta é registrada no Banco de Dados.

---

### Exibição da Lista de Pacientes

Após o carregamento dos dados, os pacientes são apresentados em formato de cartões.

Caso nenhum registro seja encontrado, o sistema exibe:

```text
Nenhum paciente encontrado.
```

---

#### Informações Exibidas por Paciente

Cada cartão apresenta:

| Informação             | Origem           |
| ---------------------- | ---------------- |
| Foto do paciente       | `fotoPerfil`     |
| Nome                   | `nome`           |
| Sexo Biológico         | `sexo`           |
| Data de nascimento     | `dataNascimento` |
| Último teste realizado | `ultimoTeste`    |
| Data de cadastro       | `dataCriacao`    |
| Score do paciente      | `pontuacao`      |
| Encaminhamento         | `encaminhamento` |

As datas são formatadas utilizando:

* `formatarData()`
* `formatarDataHora()`

---

### Foto do Paciente

Cada paciente possui uma foto individual armazenada pelo sistema.

Fluxo de atualização:

1. O usuário seleciona o ícone 📷.
2. Uma imagem é escolhida.
3. O arquivo é armazenado em `pacientePFP`.
4. O botão **Salvar foto** executa `enviarPacienteFoto()`.
5. A imagem é enviada ao backend.
6. O cadastro do paciente é atualizado.

Caso não exista foto cadastrada, a imagem padrão (`defaultPFP`) é utilizada.

---

### Emissão de Relatório Individual

Cada paciente possui um botão **Gerar PDF**.

Ao ser acionado:

1. Uma nova aba é aberta.
2. A rota `/api/pdf/paciente/{id}` é acessada.
3. O backend gera o relatório individual.
4. O documento PDF é disponibilizado ao usuário.

O relatório contém as informações consolidadas do paciente e seu histórico registrado no sistema.

---

### Fluxo Geral da Área de Pacientes

1. O usuário acessa a seção de pacientes.
2. O sistema carrega os registros vinculados à conta.
3. Filtros podem ser aplicados para refinar a pesquisa.
4. Novos pacientes podem ser cadastrados.
5. Consultas podem ser registradas.
6. Fotos podem ser atualizadas.
7. Relatórios individuais podem ser gerados.
8. Todas as alterações são sincronizadas com o backend e persistidas no Banco de Dados.

---

### Seção de Estatísticas

A seção **Estatísticas** permite a visualização de informações consolidadas dos pacientes cadastrados através de gráficos dinâmicos e relatórios em PDF.

Essa tela é exibida quando:

```text
pagina === 'estatisticas'
```

O objetivo dessa área é fornecer uma visão analítica dos dados armazenados no sistema, permitindo a aplicação de filtros e diferentes formas de agrupamento.

---

#### Filtros Estatísticos

O sistema disponibiliza diversos filtros para refinar os dados utilizados na geração dos gráficos.

Filtros disponíveis:

| Filtro            | Finalidade                                                |
| ----------------- | --------------------------------------------------------- |
| Agrupar por       | Define a categoria utilizada para consolidação dos dados. |
| Sexo Biológico    | Filtra pacientes por sexo.                                |
| Nascimento mínimo | Define a menor data de nascimento considerada.            |
| Nascimento máximo | Define a maior data de nascimento considerada.            |
| Sintoma           | Filtra pacientes associados a um sintoma específico.      |
| Pontuação mínima  | Define o valor mínimo de pontuação.                       |
| Pontuação máxima  | Define o valor máximo de pontuação.                       |

Sempre que algum filtro é alterado, o sistema redefine o estado `filtrosAplicados`, indicando que os resultados exibidos já não correspondem aos filtros atualmente selecionados.

---

#### Tipos de Agrupamento

O campo **Agrupar por** define como os dados serão organizados antes da geração do gráfico.

Opções disponíveis:

| Opção      | Finalidade                                                                           |
| ---------- | ------------------------------------------------------------------------------------ |
| Sexo Biológico| Agrupa os dados por sexo biológico dos pacientes.                                 |
| Sintoma    | Agrupa os dados pelos sintomas registrados nas consultas.                            |
| Peso médio | Agrupa os dados utilizando informações relacionadas à pontuação média dos pacientes. |

A escolha dessa opção influencia diretamente a consulta realizada pela API e a estrutura dos dados retornados.

---

#### Seleção do Tipo de Gráfico

Após definir os filtros, o usuário pode escolher o formato de visualização dos dados.

Tipos disponíveis:

| Tipo    | Descrição                                      |
| ------- | ---------------------------------------------- |
| Colunas | Representação através de barras verticais.     |
| Linhas  | Representação por linhas conectando os pontos. |
| Setores | Representação em gráfico de pizza.             |
| Barras  | Representação através de barras horizontais.   |

O tipo selecionado é armazenado no estado `tipoGrafico` e utilizado posteriormente pela função `obterGrafico()`.

---

### Aplicação dos Filtros

O botão **Aplicar Filtros** executa a função `aplicarFiltros()`.

Fluxo de execução:

1. O sistema marca que filtros foram aplicados.
2. Remove resultados anteriores.
3. Executa `carregarEstatisticas()`.
4. A API recebe os filtros selecionados.
5. Os dados estatísticos são retornados.
6. O gráfico é renderizado utilizando os novos resultados.

Esse comportamento evita consultas automáticas excessivas ao backend, permitindo que o usuário configure todos os filtros antes de gerar o relatório visual.

---

### Geração de Relatório Estatístico

O botão **Gerar PDF Estatístico** executa a função `gerarRelatorioEstatistico()`.

Fluxo:

1. O gráfico atualmente exibido é convertido para imagem.
2. Os filtros ativos são coletados.
3. As informações são enviadas ao backend.
4. O servidor gera um relatório em PDF.
5. O documento é disponibilizado para download.

O relatório contém:

* Filtros aplicados.
* Dados estatísticos utilizados.
* Gráfico gerado na interface.
* Informações consolidadas retornadas pela API.

---

### Exibição dos Resultados

A área de resultados apresenta diferentes comportamentos de acordo com o estado atual da consulta.

---

#### Carregamento

Enquanto a consulta estatística está sendo processada, a seguinte mensagem é exibida:

```text
Carregando estatísticas...
```

Essa condição ocorre quando:

```text
carregandoEstatisticas === true
```

---

#### Exibição do Gráfico

Quando existem filtros aplicados e dados válidos retornados pela API, o gráfico é renderizado através da função:

```text
obterGrafico()
```

O componente é exibido dentro do contêiner:

```text
chartContainer
```

---

#### Ausência de Dados

Caso a consulta seja concluída, mas não existam registros compatíveis com os filtros selecionados, o sistema exibe:

```text
Nenhum dado disponível para exibir.
```

Essa situação ocorre quando a API retorna uma coleção vazia de resultados.

---

#### Estado Inicial

Antes da aplicação dos filtros, nenhuma consulta estatística é realizada.

Nesse cenário, a interface exibe a mensagem:

```text
Defina os filtros e clique em "Aplicar Filtros" para gerar o gráfico.
```

Esse comportamento evita processamento desnecessário e orienta o usuário sobre o fluxo correto de utilização da ferramenta.

---

### Fluxo Geral da Área de Estatísticas

1. O usuário acessa a seção de estatísticas.
2. Define os filtros desejados.
3. Seleciona o tipo de agrupamento.
4. Escolhe o formato do gráfico.
5. Pressiona **Aplicar Filtros**.
6. O sistema consulta a API.
7. Os dados retornados são processados.
8. O gráfico é renderizado.
9. Opcionalmente, o usuário pode gerar um relatório em PDF contendo os resultados obtidos.

A seção de estatísticas constitui o principal módulo analítico do sistema, permitindo transformar os dados cadastrados em informações visuais e relatórios consolidados.

---

### Encerramento do Componente

Após a renderização condicional das seções Home, Pacientes e Estatísticas, o componente é finalizado e exportado para utilização pelo sistema.

```typescript
export default Menu
```

A instrução acima define o componente Menu como exportação padrão do arquivo, permitindo que ele seja importado e utilizado em outras partes da aplicação.

---


### Administrador (admin.tsx - admin.css)

## Backend

---

### Arquivo de Banco de Dados (db.py)
O arquivo que compõem as operações em relação ao banco de dados é o arquivo **db.py**

Em seu código existem três funções distintas, cada uma destinada a realizar uma parte da construção da
conexão do BD

| Função | Parâmetros | Finalidade |
|---------|------------|------------|
| get_connection() | - | Obter conexão com o Banco de Dados MySQL |
| query_db | query, args=(), one=False | Realizar queries ou consultas no Banco |
| execute_db | query, args=(), return_lastrowid=False | Realizar operações de execução no Banco (INSERTs, UPDATEs, DELETEs, PUTs, etc.) |

Explicando em maior detalhe cada função:

---

* **get_connection()**

A função **get_connection()** retorna uma conexão com MySQL usando a biblioteca Python PyMySQL. Para estabelecer essa conexão, são necessários 5 principais informações:

**host** - O hospedeiro da conexão

**user** - O usuário relacionado ao serviço MySQL

**password** - Senha do usuário

**database** - Base da dados que será conectada

**charset** - Set de caracteres usado

Em caso de falha na conexão, ele retorna uma mensagem relatando o err:

```python
    try:
        return pymysql.connect(
            host='',
            user='',
            password='',
            database='',
            charset='',
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.Error as err:
        print(f"Erro MySQL: {err}")
        return None
```

---

* **query_db(query, args=(), one=False)**

A função **query_db()** é responsável por realizar consultas ao Banco de Dados, normalmente utilizadas em comandos SQL do tipo **SELECT**.

Ela recebe três parâmetros:

**query** - A consulta SQL que será executada.

**args** - Tupla contendo os valores que serão inseridos nos parâmetros da consulta SQL. Por padrão é uma tupla vazia.

**one** - Define se apenas um resultado deve ser retornado. Quando definido como `True`, retorna somente o primeiro registro encontrado. Quando `False`, retorna todos os registros encontrados.

Funcionamento da função:

1. Obtém uma conexão com o Banco de Dados através da função `get_connection()`.
2. Cria um cursor para executar a consulta.
3. Executa a query utilizando os parâmetros informados.
4. Recupera os resultados:
   - `fetchone()` quando `one=True`;
   - `fetchall()` quando `one=False`.
5. Retorna os dados obtidos.
6. Fecha automaticamente o cursor e a conexão ao final da execução.

Em caso de erro durante a execução da consulta, uma mensagem é exibida no terminal e a função retorna `None`.

Exemplo de utilização:

```python
usuario = query_db(
    "SELECT * FROM usuarios WHERE id = %s",
    (1,),
    one=True
)
```

---

* **execute_db(query, args=(), return_lastrowid=False)**

A função **execute_db()** é responsável por executar comandos que realizam alterações no Banco de Dados, como **INSERT**, **UPDATE**, **DELETE** e outras operações que modificam registros.

Para isso, a função recebe três parâmetros:

**query** - Comando SQL que será executado.

**args** - Tupla contendo os valores que serão utilizados nos parâmetros da consulta SQL. Por padrão é uma tupla vazia.

**return_lastrowid** - Define se o identificador do último registro inserido deve ser retornado. Quando definido como `True`, a função retorna o valor de `cursor.lastrowid`.

Explicando em maior detalhe o funcionamento da função:

1. Obtém uma conexão com o Banco de Dados através da função `get_connection()`.
2. Verifica se a conexão foi estabelecida corretamente.
3. Cria um cursor para executar o comando SQL.
4. Executa a query utilizando os parâmetros informados.
5. Realiza um `commit()` para salvar permanentemente as alterações realizadas no Banco de Dados.
6. Retorna:
   - O ID do último registro inserido quando `return_lastrowid=True`;
   - `True` quando a operação é concluída com sucesso.

Ao final da execução, independentemente de sucesso ou erro, o cursor e a conexão são fechados automaticamente através do bloco `finally`.

Em caso de erro durante a execução do comando SQL, uma mensagem é exibida no terminal e a função retorna `None`.

Exemplo de utilização:

```python
novo_id = execute_db(
    "INSERT INTO usuarios(nome, email) VALUES (%s, %s)",
    ("João", "joao@email.com"),
    return_lastrowid=True
)
```

---

### Login

O processo de autenticação do sistema é realizado através do arquivo **main.py**, responsável pela inicialização da aplicação Flask e pelo gerenciamento das rotas de login e logout dos usuários.

Além das rotas de autenticação, o arquivo também registra as rotas relacionadas aos módulos de usuário comum e administrador por meio das funções `register_menu_routes()` e `register_admin_routes()`.

---

#### Configuração da aplicação

Inicialmente, é criada uma instância da aplicação Flask:

```python
app = Flask(__name__)
```

Em seguida, são registradas as rotas dos demais módulos do sistema:

```python
register_admin_routes(app)
register_menu_routes(app)
```

A aplicação também define uma chave secreta utilizada para gerenciamento das sessões dos usuários:

```python
app.secret_key = os.environ.get('FLASK_SECRET', '123')
```

Por fim, é configurado o CORS (Cross-Origin Resource Sharing), permitindo que o frontend hospedado em `http://localhost:5173` realize requisições para a API:

```python
cors = CORS(
    app,
    supports_credentials=True,
    origins=['http://localhost:5173'],
    allow_headers=['Content-Type']
)
```

---

### Rota de Login (`/api/login`)

A rota `/api/login` recebe requisições do tipo **POST** contendo as credenciais informadas pelo usuário.

Os dados recebidos são:

| Campo | Finalidade                                       |
| ----- | ------------------------------------------------ |
| user  | Nome de usuário informado no formulário de login |
| senha | Senha digitada pelo usuário                      |

Funcionamento da autenticação:

1. Recebe os dados enviados pelo frontend.
2. Consulta o Banco de Dados em busca do usuário informado.
3. Caso o usuário não exista, retorna uma mensagem de falha no login.
4. Caso o usuário exista, verifica se a senha informada corresponde ao hash armazenado utilizando a biblioteca **bcrypt**.
5. Se a senha estiver incorreta, retorna uma mensagem de erro.
6. Se a autenticação for bem-sucedida:

   * Armazena o ID do usuário na sessão.
   * Armazena o nível de permissão do usuário na sessão.
   * Retorna uma resposta contendo sucesso na autenticação e a permissão do usuário.

Os dados armazenados na sessão são:

```python
session['user_id']
session['permissao']
```

Essas informações são utilizadas posteriormente para controlar o acesso às funcionalidades do sistema.

---

### Rota de Logout (`/api/logout`)

A rota `/api/logout` recebe requisições do tipo **POST** e é responsável por encerrar a sessão do usuário autenticado.

Funcionamento:

1. Remove todas as informações armazenadas na sessão através de `session.clear()`.
2. Retorna uma mensagem confirmando o encerramento da sessão.

Após o logout, o usuário perde o acesso às rotas protegidas até realizar uma nova autenticação.

---

## Menu (Usuário Comum)

As funções e configurações da página denominada Menu são realizados dentro do arquivo **menu.py**. O módulo de usuário comum é implementado através da função `register_menu_routes(app)`, responsável por registrar todas as rotas utilizadas pelo pesquisador após realizar autenticação no sistema.

Além das funcionalidades de gerenciamento de pacientes e consultas, este módulo também disponibiliza recursos relacionados ao perfil do pesquisador, upload de imagens e aplicação de filtros em pesquisas.

---

* **montar_filtros(user_id, dados=None)**

A função **montar_filtros()** é responsável por construir dinamicamente filtros SQL utilizados em consultas posteriores.

Ela recebe dois parâmetros:

| Parâmetro | Finalidade                                                  |
| --------- | ----------------------------------------------------------- |
| user_id   | Identificador do pesquisador autenticado                    |
| dados     | Dicionário opcional contendo filtros enviados pelo frontend |

A função cria uma lista de condições SQL e uma lista de parâmetros correspondentes, permitindo que consultas sejam montadas de forma segura utilizando parâmetros preparados (Prevenção a SQL Injection).

Os filtros disponíveis são:

| Filtro        | Campo utilizado               |
| ------------- | ----------------------------- |
| sexo          | Sexo do paciente              |
| nascimentoMin | Data mínima de nascimento     |
| nascimentoMax | Data máxima de nascimento     |
| sintoma       | Sintoma associado ao paciente |
| pontuacaoMin  | Pontuação mínima              |
| pontuacaoMax  | Pontuação máxima              |

Ao final da execução são retornados:

```python
filtros, parametros
```

Esses valores são depois utilizados na montagem de consultas SQL contendo cláusulas `WHERE` personalizadas.

---

### Rota `/api/meu_perfil`

Método: **GET**

Esta rota é responsável por recuperar as informações do pesquisador atualmente autenticado.

Funcionamento:

1. Obtém o identificador do usuário armazenado na sessão.
2. Verifica se existe uma sessão válida.
3. Consulta o Banco de Dados buscando os dados do usuário.
4. Retorna as informações encontradas em formato JSON.

Dados retornados:

| Campo          |
| -------------- |
| user           |
| nome           |
| dataNascimento |
| dataCriacao    |
| fotoPerfil     |

Caso não exista uma sessão ativa, a API retorna:

```json
{
    "error": "Não autorizado"
}
```

---

### Rota `/api/user_pfp`

Método: **POST**

Esta rota permite que o pesquisador altere sua foto de perfil.

Funcionamento:

1. Verifica se existe um usuário autenticado.
2. Recebe um arquivo enviado através de um formulário.
3. Valida a existência do arquivo.
4. Gera um nome único utilizando o ID do usuário.
5. Cria a pasta de armazenamento caso ela não exista.
6. Salva a imagem em:

```text
uploads/perfis/
```

7. Atualiza o caminho da imagem na tabela `usuario`.
8. Retorna uma mensagem de sucesso juntamente com o caminho da imagem.

---

### Rota `/api/paciente_pfp`

Método: **POST**

Esta rota permite que o pesquisador altere a foto de perfil de um paciente cadastrado em sua conta.

Funcionamento:

1. Verifica se existe uma sessão válida.
2. Recebe o identificador do paciente.
3. Recebe o arquivo de imagem enviado pelo frontend.
4. Valida as informações recebidas.
5. Gera um nome de arquivo baseado no ID do paciente.
6. Salva a imagem em:

```text
uploads/pacientes/
```

7. Atualiza o campo `fotoPerfil` do paciente no Banco de Dados.
8. Verifica se o paciente pertence ao pesquisador autenticado.
9. Retorna uma mensagem de sucesso.

---

### Rota `/uploads/pacientes/<filename>` --- `/uploads/perfis/<filename>`


Método: **GET**

Esta rota é utilizada para disponibilizar as imagens de perfil dos pacientes/perfis armazenadas no servidor.

Através da função `send_from_directory()`, o arquivo solicitado é enviado diretamente ao navegador.

Diretório utilizado:

---

* Para Pacientes
```text
uploads/pacientes/
```
---

* Para usuários comuns
```text
uploads/perfis/
```

---

### Rota `/api/meus_pacientes`

Métodos: **GET** e **POST**

Esta rota é responsável pelo gerenciamento dos pacientes vinculados ao pesquisador autenticado.

---

#### Cadastro de pacientes (POST)

Quando utilizada com o método **POST**, a rota permite o cadastro de um novo paciente no sistema.

Dados recebidos:

| Campo          | Finalidade                     |
| -------------- | ------------------------------ |
| nome           | Nome completo do paciente      |
| cpf            | CPF do paciente                |
| sexo           | Sexo do paciente               |
| dataNascimento | Data de nascimento do paciente |

Funcionamento:

1. Verifica se existe uma sessão válida.
2. Recebe os dados enviados pelo frontend.
3. Valida se todos os campos obrigatórios foram informados.
4. Insere o novo paciente no Banco de Dados.
5. Associa automaticamente o paciente ao pesquisador autenticado.
6. Retorna uma confirmação de sucesso.

---

#### Listagem de pacientes (GET)

Quando utilizada com o método **GET**, a rota retorna todos os pacientes cadastrados pelo pesquisador autenticado.

Além da listagem básica, a consulta também busca informações da consulta mais recente de cada paciente.

Dados retornados:

| Campo          |
| -------------- |
| id             |
| nome           |
| sexo           |
| dataNascimento |
| ultimoTeste    |
| dataCriacao    |
| fotoPerfil     |
| pontuacao      |
| encaminhamento |

Filtros disponíveis:

| Parâmetro | Finalidade                |
| --------- | ------------------------- |
| sexo      | Filtrar por sexo          |
| dataMin   | Data mínima de nascimento |
| dataMax   | Data máxima de nascimento |
| scoreMin  | Pontuação mínima          |
| scoreMax  | Pontuação máxima          |

Funcionamento:

1. Verifica se existe uma sessão válida.
2. Monta dinamicamente a consulta SQL.
3. Aplica os filtros enviados pelo frontend.
4. Busca os pacientes pertencentes ao pesquisador.
5. Recupera a consulta mais recente de cada paciente.
6. Retorna os resultados em formato JSON.

---

### Rota `/api/paciente_nova_consulta`

Método: **POST**

Esta rota é responsável por registrar uma nova consulta para um paciente previamente cadastrado.

Durante o processo, o sistema calcula automaticamente a pontuação do paciente com base nos sintomas informados e define o resultado do exame e o encaminhamento recomendado.

Dados recebidos:

| Campo      | Finalidade                                    |
| ---------- | --------------------------------------------- |
| idPaciente | Paciente associado à consulta                 |
| sintomas   | Lista contendo os IDs dos sintomas observados |
| tipoExame  | Tipo de exame realizado                       |
| observacao | Observações registradas pelo pesquisador      |

---

#### Cálculo da pontuação

Após receber os sintomas selecionados, o sistema:

1. Obtém o sexo do paciente.
2. Busca os pesos de cada sintoma cadastrados na tabela `sintoma`.
3. Soma os pesos correspondentes ao sexo do paciente.
4. Calcula a pontuação final.

Dependendo do sexo, são utilizados limites diferentes para determinação do resultado:

| Sexo      | Limite |
| --------- | ------ |
| Masculino | 0.56   |
| Feminino  | 0.55   |

Após o cálculo da pontuação, o sistema define automaticamente:

---

#### Resultado do exame

| Condição           | Resultado |
| ------------------ | --------- |
| Pontuação ≥ limite | Positivo  |
| Pontuação < limite | Negativo  |

---

#### Encaminhamento

| Condição           | Encaminhamento                               |
| ------------------ | -------------------------------------------- |
| Pontuação ≥ limite | Encaminhar para teste genético confirmatório |
| Pontuação < limite | Sem necessidade de encaminhamento            |

---

#### Registro da consulta

Após o cálculo:

1. É criado um novo registro na tabela `consulta`.

2. São armazenados:

   * Paciente;
   * Pesquisador responsável;
   * Data e horário;
   * Tipo de exame;
   * Resultado;
   * Pontuação;
   * Encaminhamento;
   * Observações.

3. O sistema obtém o ID da consulta recém-criada.

4. Cada sintoma informado é associado à consulta através da tabela `consultasintoma`.

Essa abordagem permite manter o relacionamento entre consultas e sintomas em uma estrutura normalizada do Banco de Dados.

---

### Rota `/api/pdf/paciente/<paciente_id>`

Método: **GET**

Esta rota é responsável pela geração de um relatório clínico em formato PDF contendo todas as informações de um paciente e seu histórico completo de consultas.

O arquivo gerado pode ser baixado diretamente pelo usuário através do navegador.

---

##### Controle de acesso

Antes da geração do relatório, o sistema verifica se existe uma sessão válida.

Além disso, o paciente só poderá ser acessado caso esteja vinculado ao pesquisador autenticado.

Essa verificação impede que usuários tenham acesso aos dados de pacientes pertencentes a outros pesquisadores.

---

##### Busca das informações do paciente

Inicialmente, o sistema consulta a tabela `paciente` para recuperar os dados básicos do paciente.

Dados obtidos:

| Campo          |
| -------------- |
| nome           |
| sexo           |
| dataNascimento |
| ultimoTeste    |
| dataCriacao    |
| fotoPerfil     |

Caso o paciente não seja encontrado, a API retorna:

```json
{
    "error": "Paciente não encontrado"
}
```

---

##### Busca do histórico de consultas

Após localizar o paciente, o sistema consulta todas as consultas associadas ao seu cadastro.

Para cada consulta são recuperados:

| Campo          |
| -------------- |
| dataHora       |
| tipoExame      |
| resultadoExame |
| pontuacao      |
| encaminhamento |
| observacao     |
| sintomas       |

Os sintomas são obtidos através da tabela intermediária `consultasintoma`, sendo agrupados em uma única string utilizando a função SQL `GROUP_CONCAT()`.

As consultas são ordenadas cronologicamente pela data de realização.

---

##### Criação do documento PDF

A geração do relatório é realizada utilizando a biblioteca **ReportLab**.

Inicialmente é criado um objeto PDF em memória utilizando um buffer temporário:

```python
buffer = BytesIO()
pdf = canvas.Canvas(buffer, pagesize=A4)
```

Esse procedimento evita a criação de arquivos temporários no servidor.

---

##### Elementos do cabeçalho

O relatório possui:

* Logotipo institucional;
* Título do documento;
* Informações cadastrais do paciente;
* Fotografia do paciente.

Caso o paciente não possua uma foto cadastrada, o sistema utiliza automaticamente uma imagem padrão.

Informações exibidas no cabeçalho:

| Informação         |
| ------------------ |
| Nome               |
| Sexo               |
| Data de Nascimento |
| Último Teste       |
| Data de Cadastro   |

---

##### Histórico clínico

Após o cabeçalho, o relatório apresenta uma seção denominada:

```text
HISTÓRICO DE CONSULTAS
```

Nessa área são listadas todas as consultas registradas para o paciente.

Para cada consulta são exibidos:

| Informação           |
| -------------------- |
| Data e horário       |
| Tipo de exame        |
| Resultado            |
| Pontuação            |
| Encaminhamento       |
| Observações          |
| Sintomas registrados |

As observações e listas de sintomas passam por um processo de quebra automática de linha utilizando a biblioteca `textwrap`, evitando que textos extensos ultrapassem os limites da página.

---

##### Paginação automática

Durante a geração do relatório, o sistema monitora o espaço restante disponível na página.

Quando o limite inferior é atingido:

1. Uma nova página é criada.
2. A posição de escrita é redefinida.
3. A geração continua automaticamente.

Dessa forma, relatórios contendo muitas consultas podem ser gerados sem perda de conteúdo.

---

##### Finalização do documento

Após adicionar todas as informações:

1. O PDF é finalizado.
2. O buffer é reposicionado para o início do arquivo.
3. O documento é enviado diretamente ao navegador.

A resposta é enviada como um arquivo do tipo:

```text
application/pdf
```

com o nome:

```text
Relatorio_paciente.pdf
```

---

##### Conteúdo do relatório gerado

O documento final contém:

* Dados cadastrais do paciente;
* Fotografia do paciente;
* Histórico completo de consultas;
* Resultados dos exames realizados;
* Pontuações calculadas;
* Encaminhamentos recomendados;
* Observações clínicas registradas;
* Sintomas associados a cada consulta.

Esse relatório permite consolidar todas as informações clínicas do paciente em um único documento para consulta, arquivamento ou impressão.

---

### Rota `/api/buscar_sintomas`

Método: **GET**

Esta rota é responsável por retornar a lista completa de sintomas cadastrados no sistema.

Os sintomas retornados são utilizados principalmente durante o registro de consultas, permitindo que o pesquisador selecione os sintomas observados no paciente.

---

##### Controle de acesso

Antes de realizar a consulta, o sistema verifica se existe uma sessão válida.

Caso o usuário não esteja autenticado, a API retorna:

```json
{
    "error": "Não autorizado"
}
```

---

##### Busca dos sintomas

A consulta recupera todos os sintomas cadastrados na tabela `sintoma`.

Dados retornados:

| Campo |
| ----- |
| id    |
| nome  |

Os registros são ordenados alfabeticamente pelo nome do sintoma, facilitando sua localização na interface.

Consulta utilizada:

```sql
SELECT
    id,
    nome
FROM sintoma
ORDER BY nome
```

---

##### Resposta da rota

Exemplo de retorno:

```json
[
    {
        "id": 1,
        "nome": "Sintoma X"
    },
    {
        "id": 2,
        "nome": "Sintoma 2"
    }
]
```

Essas informações são utilizadas pelo frontend para preencher listas de seleção e formulários relacionados às consultas clínicas.

---

### Rota `/api/stats`

Método: **GET**

Esta rota é responsável pela geração de dados estatísticos utilizados pelos gráficos e dashboards do sistema.

As estatísticas podem ser organizadas de diferentes formas e também podem receber filtros personalizados enviados pelo frontend.

---

##### Controle de acesso

Inicialmente o sistema verifica se existe um usuário autenticado.

Caso não exista uma sessão válida, a requisição é interrompida.

---

##### Filtros aplicáveis

Os filtros são construídos através da função:

```python
montar_filtros()
```

Os seguintes filtros podem ser utilizados:

| Parâmetro     | Finalidade                     |
| ------------- | ------------------------------ |
| sexo          | Filtrar pacientes por sexo     |
| nascimentoMin | Data mínima de nascimento      |
| nascimentoMax | Data máxima de nascimento      |
| sintoma       | Filtrar por sintoma específico |
| pontuacaoMin  | Pontuação mínima               |
| pontuacaoMax  | Pontuação máxima               |

Esses filtros são incorporados dinamicamente à consulta SQL através da cláusula `WHERE`.

---

##### Organização dos dados

O parâmetro:

```text
organizacao
```

define qual tipo de organização utilizado para as queries.

Caso nenhum valor seja informado, o sistema utiliza:

```text
genero
```

como padrão.

---

##### Organização por gênero

Valor utilizado:

```text
genero
```

Nessa modalidade o sistema contabiliza a quantidade de pacientes por sexo biológico.

Dados gerados:

| Campo                   |
| ----------------------- |
| Sexo Biológico          |
| Quantidade de pacientes |

Esse conjunto de dados é normalmente utilizado em gráficos de setores ou barras.

---

##### Organização por sintoma

Valor utilizado:

```text
sintoma
```

Nessa modalidade o sistema contabiliza quantas vezes cada sintoma foi registrado nas consultas.

Dados gerados:

| Campo                     |
| ------------------------- |
| Nome do sintoma           |
| Quantidade de ocorrências |

Essa visualização permite identificar os sintomas mais frequentes entre os pacientes cadastrados.

---

##### Organização por peso

Valor utilizado:

```text
peso
```

Nessa modalidade o sistema calcula a média dos pesos dos sintomas registrados.

O cálculo considera automaticamente o sexo de cada paciente:

* Pacientes masculinos utilizam `pesoMasculino`;
* Pacientes femininos utilizam `pesoFeminino`.

O resultado representa a relevância média observada de cada sintoma dentro do conjunto de dados filtrado.

Dados gerados:

| Campo           |
| --------------- |
| Nome do sintoma |
| Peso médio      |

Essa organização é utilizada para análises clínicas e comparações estatísticas dos sintomas registrados.

---

##### Tratamento de erros

Caso seja informado um tipo de organização inexistente, a API retorna:

```json
{
    "error": "Organização inválida"
}
```

Caso ocorra algum erro durante a consulta ao Banco de Dados:

```json
{
    "error": "Erro ao buscar dados"
}
```

---

Essa estrutura simplifica a integração com bibliotecas de visualização de dados utilizadas no frontend, permitindo a geração dinâmica de gráficos estatísticos.

---

#### Rota `/api/pdf/stats`

Métodos: **GET** e **POST**

Esta rota é responsável pela geração de um relatório estatístico em formato PDF contendo informações analíticas sobre os pacientes, consultas e sintomas cadastrados no sistema.

O documento gerado pode ser baixado diretamente pelo navegador e pode incluir tanto os dados estatísticos quanto uma imagem do gráfico exibido no frontend.

---

##### Controle de acesso

Inicialmente o sistema verifica se existe um usuário autenticado através da sessão.

Caso não exista uma sessão válida, a API retorna:

```json
{
    "error": "Não autorizado"
}
```

---

##### Parâmetros utilizados

A rota aceita os seguintes parâmetros:

| Parâmetro           | Finalidade                                     |
| ------------------- | ---------------------------------------------- |
| organizacao         | Define o tipo de análise estatística           |
| tipoGrafico         | Define o tipo de gráfico utilizado no frontend |
| imagemGraficoBase64 | Imagem do gráfico codificada em Base64         |

Caso nenhum valor seja informado, o sistema utiliza:

```text
organizacao = genero
tipoGrafico = colunas
```

---

##### Filtros aplicáveis

Os filtros são processados através da função:

```python
montar_filtros()
```

Os seguintes filtros podem ser utilizados:

| Filtro        | Finalidade                     |
| ------------- | ------------------------------ |
| sexo          | Filtrar pacientes por sexo biológico|
| nascimentoMin | Data mínima de nascimento      |
| nascimentoMax | Data máxima de nascimento      |
| sintoma       | Filtrar por sintoma específico |
| pontuacaoMin  | Pontuação mínima               |
| pontuacaoMax  | Pontuação máxima               |

Esses filtros são incorporados dinamicamente à cláusula `WHERE` da consulta SQL.

---

##### Organização dos dados

O parâmetro `organizacao` define qual será a organização utilizada para as queries.

---

##### Organização por gênero

Valor:

```text
genero
```

Retorna a quantidade de pacientes agrupados por sexo biológico.

Dados gerados:

| Campo                   |
| ----------------------- |
| Sexo                    |
| Quantidade de pacientes |

---

##### Organização por data

Valor:

```text
data
```

Retorna a quantidade de pacientes atendidos em cada data de consulta.

Dados gerados:

| Campo                   |
| ----------------------- |
| Data                    |
| Quantidade de registros |

Os resultados são ordenados cronologicamente.

---

##### Organização por sintoma

Valor:

```text
sintoma
```

Retorna a frequência de ocorrência dos sintomas registrados nas consultas.

Dados gerados:

| Campo                     |
| ------------------------- |
| Sintoma                   |
| Quantidade de ocorrências |

Essa análise permite identificar os sintomas mais frequentes entre os pacientes.

---

##### Organização por peso

Valor:

```text
peso
```

Calcula a média dos pesos dos sintomas registrados.

O sistema utiliza:

* `pesoMasculino` para pacientes masculinos;
* `pesoFeminino` para pacientes femininos.

Dados gerados:

| Campo      |
| ---------- |
| Sintoma    |
| Peso médio |

Essa modalidade auxilia na análise da relevância clínica dos sintomas observados.

---

##### Tratamento de erros

Caso seja informado um valor inválido para o parâmetro `organizacao`, a API retorna:

```json
{
    "error": "Organização inválida"
}
```

Caso ocorra algum erro durante a consulta ao Banco de Dados:

```json
{
    "error": "Erro ao buscar dados"
}
```

---

##### Métricas calculadas

Após recuperar os dados estatísticos, o sistema calcula automaticamente:

| Métrica              | Descrição                                  |
| -------------------- | ------------------------------------------ |
| Total analisado      | Soma de todos os valores encontrados       |
| Maior ocorrência     | Categoria com maior valor                  |
| Menor ocorrência     | Categoria com menor valor                  |
| Média                | Média dos valores encontrados (essencial para consultas com sintomas, por exemplo)|
| Percentual dominante | Participação percentual da maior categoria |

Quando existem dados suficientes, o sistema também gera automaticamente uma análise textual.

Exemplo:

```text
A categoria 'Masculino' apresentou a maior representatividade da amostra, correspondendo a 57,1% dos registros analisados.
```

---

##### Inclusão do gráfico

O frontend pode enviar uma imagem do gráfico através do campo:

```text
imagemGraficoBase64
```

Essa imagem é convertida para um formato compatível com o ReportLab e inserida diretamente no relatório.

Caso ocorra algum erro durante a conversão, o PDF continua sendo gerado normalmente.

---

##### Estrutura do relatório

O documento PDF contém as seguintes seções:

###### Cabeçalho

* Logotipo institucional;
* Título do relatório;
* Data e horário de geração.

###### Informações da análise

* Tipo de organização utilizada;
* Filtros aplicados.

###### Gráfico

* Imagem do gráfico enviada pelo frontend.

###### Dados estatísticos

* Total analisado;
* Quantidade de categorias;
* Maior ocorrência;
* Menor ocorrência.

###### Análise textual

* Resumo automático dos resultados;
* Percentuais de participação por categoria.

---

##### Paginação automática

Durante a geração do documento, o sistema monitora o espaço disponível na página.

Quando o limite inferior é atingido:

1. Uma nova página é criada.
2. A posição de escrita é redefinida.
3. O conteúdo continua sendo inserido automaticamente.

Esse processo garante que relatórios extensos sejam gerados corretamente sem sobreposição de informações.

---

##### Envio do arquivo

Após finalizar a geração do documento:

1. O PDF é salvo em memória utilizando um buffer temporário.
2. O ponteiro do arquivo é reposicionado para o início.
3. O documento é enviado diretamente ao navegador.

O arquivo é disponibilizado com:

| Propriedade     | Valor                      |
| --------------- | -------------------------- |
| Nome do arquivo | Relatorio_estatisticas.pdf |
| Tipo MIME       | application/pdf            |

---

##### Conteúdo do relatório gerado

O relatório final pode conter:

* Distribuição de pacientes por sexo biológico;
* Frequência dos sintomas registrados;
* Evolução temporal das consultas;
* Média dos pesos dos sintomas;
* Gráficos estatísticos;
* Filtros utilizados na pesquisa;
* Resumos automáticos dos resultados.

Essa funcionalidade permite exportar informações estatísticas do sistema para compartilhamento, arquivamento ou impressão.

### Administrador (Usuário Administrador)
