# Sistema de Gerenciamento de Tarefas Web (TaskManager)

Aplicação web desenvolvida em Python com Flask para gerenciamento colaborativo de tarefas, inspirada nas funções essenciais de organização do Trello.

---

## 🚀 Funcionalidades

- **Autenticação e Sessão:**
  - Registro de novos usuários com verificação de duplicação (nome e e-mail).
  - Criptografia e armazenamento seguro de senhas com algoritmo hash.
  - Login e logout com controle de sessão (`Flask-Login`).
  - Proteção de páginas restritas contra acessos não autorizados.

- **Gerenciamento de Tarefas:**
  - Criação de novas tarefas com título, descrição, status e atribuição a usuários.
  - Visualização tabular detalhada e visualização em cartões.
  - Edição completa de tarefas existentes.
  - Exclusão de tarefas do banco de dados com confirmação em tela.
  - Vínculo relacional entre criador da tarefa e usuário responsável.

- **Filtros e Status:**
  - Acompanhamento pelos status: `Pendente`, `Em Andamento` e `Concluída`.
  - Filtros rápidos na interface para listar tarefas por status específico.

- **Dashboard Coletivo:**
  - Painel com contadores de métricas em tempo real (total geral e total por status).
  - Listagem unificada para visualização das atividades de todo o grupo.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.10+
- **Framework Web:** Flask 3+
- **ORM / Banco de Dados:** Flask-SQLAlchemy / SQLite
- **Autenticação:** Flask-Login / Werkzeug Security
- **Frontend:** HTML5, CSS3, Bootstrap 5 e Bootstrap Icons

---

## 📋 Pré-requisitos

Certifique-se de ter instalado em sua máquina:
- [Python 3.10+](https://www.python.org/)
- Gerenciador de pacotes `pip`
- [Git](https://git-scm.com/)

---

## 🔧 Instalação e Execução

### 1. Clonar o repositório
```bash
git clone [https://github.com/teqqzz/task_manager.git](https://github.com/teqqzz/task_manager.git)
cd task_manager
```

### 2. Criar e ativar o ambiente virtual (venv)

- **No Windows (PowerShell/CMD):**
  ```powershell
  python -m venv venv
  venv\Scripts\activate
  ```

- **No Linux/macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 4. Executar o servidor de desenvolvimento
```bash
python app.py
```

### 5. Acessar a aplicação
Abra o navegador e acesse:
```text
[http://127.0.0.1:5000](http://127.0.0.1:5000)
```
> **Nota:** O banco de dados SQLite (`instance/tarefas.db`) será criado automaticamente com todas as tabelas na primeira execução do comando `python app.py`.

---

## 📁 Estrutura de Pastas

```text
gerenciador_tarefas/
│
├── app.py              # Rotas, autenticação e regras de negócio
├── config.py           # Configurações do Flask e banco de dados
├── models.py           # Definição dos modelos User e Task (ORM)
├── requirements.txt    # Lista de bibliotecas necessárias
├── README.md           # Documentação e instruções de uso
│
└── templates/          # Arquivos de visualização (HTML + Jinja2)
    ├── base.html
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── task_form.html
    └── my_tasks.html
```

---

## 👥 Instruções de Uso

1. **Primeiro Acesso:** Clique em **Cadastrar** e crie pelo menos dois usuários diferentes para testar a atribuição de tarefas.
2. **Login:** Entre com suas credenciais recém-criadas.
3. **Criar Tarefa:** Clique no botão **+ Nova Tarefa** no menu superior, preencha os dados e escolha quem será o responsável.
4. **Filtrar e Acompanhar:** Use os botões de filtro no painel superior do **Dashboard** para isolar tarefas por status (`Pendente`, `Em Andamento`, `Concluída`).
5. **Editar ou Remover:** Utilize os botões de ação na tabela do Dashboard ou na aba **Minhas Tarefas** para atualizar o progresso ou deletar um item.

