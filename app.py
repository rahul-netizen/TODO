from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# to prevent FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# /// for relative path
# //// for absolute path
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'<Task {self.id}>'


@app.route('/', methods=['POST', 'GET'])
def index():
    # return "Hello, World from flask"
    # return render_template('index.html')

    if request.method == 'POST':
        # return 'Hello'
        task_content = request.form['content']
        new_task = Todo(content=task_content)    

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Issue occured while adding your task !'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks )

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Issue occcured while deleting your task'
    

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Issue occured while updating you task'

    else:
        return render_template('update.html', task=task)


if __name__ == '__main__':
    app.run(debug=True)


# use WSGI like gunicorn, waitress to serve the app
# waitress-serve --listen=127.0.0.1:5000 embed_dash:app