from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Task  # Импортируем db и модель Task

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description', '')
        new_task = Task(title=title, description=description)
        db.session.add(new_task)
        db.session.commit()
        flash('Задача добавлена!', 'success')
        return redirect(url_for('index'))
    return render_template('edit.html', task=None)

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form.get('description', '')
        task.is_done = 'is_done' in request.form
        db.session.commit()
        flash('Задача обновлена!', 'success')
        return redirect(url_for('index'))
    return render_template('edit.html', task=task)

@app.route('/delete/<int:task_id>', methods=['GET', 'POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Задача удалена!', 'danger')
    return redirect(url_for('index'))


@app.route('/toggle/<int:task_id>')
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.is_done = not task.is_done
    db.session.commit()
    return redirect(url_for('index'))

@app.before_request
def init_db():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
