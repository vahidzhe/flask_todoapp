from flask import Flask,redirect,render_template,url_for,request,flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///mnt/4CB64BFAB64BE356/VSC_PYTHON/ToDo/todo.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean())

@app.route("/")
def index():
    todolar = Todo.query.all()
    return render_template("index.html",todolar = todolar)

@app.route("/add",methods = ["POST"])
def addTodo():
    title = request.form.get("title")
    newTodo = Todo(title = title, complete = False)

    db.session.add(newTodo)
    db.session.commit()

    return redirect(url_for("index"))

@app.route("/complete/<string:id>")
def completeTodo(id):
    todo = Todo.query.filter_by(id = id).first()
    todo.complete = not todo.complete
    db.session.commit()
    flash("Tamalandı...")
    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def delTodo(id):
    todo = Todo.query.filter_by(id = id).first()

    db.session.delete(todo)
    db.session.commit()
    flash("Todo Silindi","danger")
    return redirect(url_for("index"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
