# Manual de Instruções de Uso

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

### Login (App.tsx - App.css)

### Pesquisador (Menu.tsx - Menu.css)

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

#### Rota `/api/buscar_sintomas`

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

#### Rota `/api/stats`

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

* Distribuição de pacientes por gênero;
* Frequência dos sintomas registrados;
* Evolução temporal das consultas;
* Média dos pesos dos sintomas;
* Gráficos estatísticos;
* Filtros utilizados na pesquisa;
* Resumos automáticos dos resultados.

Essa funcionalidade permite exportar informações estatísticas do sistema para compartilhamento, arquivamento ou impressão.

### Administrador (Usuário Administrador)
