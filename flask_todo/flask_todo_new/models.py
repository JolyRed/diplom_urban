from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    is_done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Task {self.id} - {self.title}>'
