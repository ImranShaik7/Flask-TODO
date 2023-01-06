from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db=SQLAlchemy(app)
db.init_app(app)

class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow )
   
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

with app.app_context():
    db.create_all()
   


@app.route('/',methods=['GET','POST'])
def  hello_world():
    # creating a instance of Todo class
    if request.method=='POST':
        # print("POST")
        tit=request.form['todoTitle']
        des=request.form['todoDesc']
        if len(tit)==0 or len(des)==0:
            allTodo=Todo.query.all()
            return render_template('index.html', vaue=0,allTodo=allTodo)

        todoObj=Todo(title=tit,desc=des)
        db.session.add(todoObj)
        db.session.commit()
    
    allTodo=Todo.query.all()

    # todo1=Todo(title="Learn Python",desc="Learn Python from Youtube")
    
    
    
    return render_template('index.html',allTodo=allTodo)
    # return 'Hello, World'

@app.route('/products')
def  products():
    allTodo=Todo.query.all()
    print(allTodo)
    return 'This is products'

@app.route('/update/<int:se_no>' ,methods=['GET','POST'])
def  update(se_no):
    if request.method=='POST':
        tit=request.form['todoTitle']
        des=request.form['todoDesc']
        update_todo=Todo.query.filter_by(sno=se_no).first()
        update_todo.title=tit
        update_todo.desc=des
        db.session.add(update_todo)
        db.session.commit()
        return redirect("/")
        

    # if the method is not post
    update_todo=Todo.query.filter_by(sno=se_no).first()
    return render_template('update.html',updateTodo=update_todo)
    

@app.route('/delete/<int:se_no>')
def  delete(se_no):
    todo_delete=Todo.query.filter_by(sno=se_no).first()
    db.session.delete(todo_delete)
    db.session.commit()
    # allTodo=Todo.query.all()
    # return render_template('index.html',allTodo=allTodo)
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)
    