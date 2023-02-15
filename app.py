from flask import Flask, flash, render_template, request, redirect, url_for, json, Response
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# http://127.0.0.1:5000/

#   database URI used for connection// sqlite used
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
#  If set to True, extra memory to track
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
#SQLAlchemy comm bet program and db
# toolkit for connection python to 
db = SQLAlchemy(app)

# Model sqlalchemy subclass to define db models
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

#before even home is called, table is created
@app.before_first_request
def create_tables():
    db.create_all()
"""
querying all the tasks from db and rendering it in format of base.html
"""
@app.route('/')
def home():
    todo_list = Todo.query.all()
    return render_template("base.html", todo_list=todo_list, length = len(todo_list))


#session stablish comversation with db , (holding zone)
"""
adds a task to the db and renders back the home page with the update
"""
@app.route('/add', methods=['POST'])
def add():
    title = request.form.get("title")
    if (title=="" or len(title)>100):
        return 'incorrect task, kindly go back and try'
    new_todo = Todo(title=title, complete= False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))


# query=> all the data; filter_by=> primary key; first()=> sinsce you get a whole list
"""
Updates the task, if complet, marks incomplete and vice versa, 
and renders back the home page with the update
"""
@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))


"""
delete the task from the db and renders back the home page with update
"""
@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)

    db.session.commit()
    return redirect(url_for("home"))

#True => no reloading server for every change
if __name__ == "__main__":
    app.run(debug=True)