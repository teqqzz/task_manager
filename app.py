from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from models import db, User, Task

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'warning'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rota Inicial
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Autenticação: Registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not username or not email or not password:
            flash('Preencha todos os campos.', 'danger')
            return render_template('register.html')

        if User.query.filter_by(username=username).first():
            flash('Nome de usuário já está em uso.', 'danger')
            return render_template('register.html')

        if User.query.filter_by(email=email).first():
            flash('E-mail já está cadastrado.', 'danger')
            return render_template('register.html')

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Conta criada com sucesso! Faça login para continuar.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Autenticação: Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Usuário ou senha incorretos.', 'danger')

    return render_template('login.html')

# Autenticação: Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('login'))

# Dashboard do Grupo
@app.route('/dashboard')
@login_required
def dashboard():
    status_filter = request.args.get('status', 'todos')
    
    query = Task.query
    if status_filter != 'todos':
        query = query.filter_by(status=status_filter)
    
    tasks = query.order_by(Task.created_at.desc()).all()
    users = User.query.all()
    
    # Contadores gerais
    total_tasks = Task.query.count()
    pending_tasks = Task.query.filter_by(status='pendente').count()
    progress_tasks = Task.query.filter_by(status='em andamento').count()
    completed_tasks = Task.query.filter_by(status='concluida').count()

    return render_template(
        'dashboard.html',
        tasks=tasks,
        status_filter=status_filter,
        users=users,
        total_tasks=total_tasks,
        pending_tasks=pending_tasks,
        progress_tasks=progress_tasks,
        completed_tasks=completed_tasks
    )

# Minhas Tarefas
@app.route('/my-tasks')
@login_required
def my_tasks():
    status_filter = request.args.get('status', 'todos')
    query = Task.query.filter_by(assigned_to_id=current_user.id)

    if status_filter != 'todos':
        query = query.filter_by(status=status_filter)

    tasks = query.order_by(Task.created_at.desc()).all()
    return render_template('my_tasks.html', tasks=tasks, status_filter=status_filter)

# Criar Tarefa
@app.route('/task/create', methods=['GET', 'POST'])
@login_required
def create_task():
    users = User.query.all()
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        status = request.form.get('status', 'pendente')
        assigned_to_id = request.form.get('assigned_to_id')

        if not title or not assigned_to_id:
            flash('Título e usuário atribuído são obrigatórios.', 'danger')
            return render_template('task_form.html', users=users, task=None)

        task = Task(
            title=title,
            description=description,
            status=status,
            creator_id=current_user.id,
            assigned_to_id=int(assigned_to_id)
        )
        db.session.add(task)
        db.session.commit()

        flash('Tarefa criada com sucesso!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('task_form.html', users=users, task=None)

# Editar Tarefa
@app.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    users = User.query.all()

    if request.method == 'POST':
        task.title = request.form.get('title', '').strip()
        task.description = request.form.get('description', '').strip()
        task.status = request.form.get('status', 'pendente')
        task.assigned_to_id = int(request.form.get('assigned_to_id'))

        if not task.title or not task.assigned_to_id:
            flash('Título e usuário atribuído são obrigatórios.', 'danger')
            return render_template('task_form.html', users=users, task=task)

        db.session.commit()
        flash('Tarefa atualizada com sucesso!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('task_form.html', users=users, task=task)

# Excluir Tarefa
@app.route('/task/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Tarefa excluída com sucesso!', 'success')
    return redirect(request.referrer or url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)