
from flask import Flask, render_template,request,redirect,flash,session
from flask.helpers import url_for
from wtforms import Form, StringField,PasswordField,validators
import db_interactions
from functools import wraps


#Login REquired decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("You have to login!!","danger")  
            return redirect(url_for("login"))
    return decorated_function
#Forms
#User Register form Class
class RegisterForm(Form):
    name = StringField("Name and Surname", validators=[validators.Length(min = 10, max = 25),validators.DataRequired()])
    username = StringField("User Name", validators=[validators.Length(min = 5, max = 15),validators.DataRequired()])
    email = StringField("email address", validators=[validators.Email("Please enter a valid email")])
    password = PasswordField("Password", validators=[validators.DataRequired(),
                                        validators.EqualTo(fieldname= "confirm", message = "Your password does not match")
        ])
    confirm = PasswordField("Confirm Password")

#Login Form
class LoginForm(Form):
    username=StringField("Username")
    password = PasswordField("Password")

#ToDo Form
class ToDoForm(Form):
    
    ToDo     = StringField("ToDo", validators=[validators.Length(min = 5, max = 50)])
    Due_Date = StringField("Due_Date", validators=[validators.Length(min = 5, max = 20)])

#Routing Division
app = Flask(__name__)
app.secret_key = "onur"

@app.route("/")
def index():
    datas = db_interactions.query_from_todos()
    if len(datas)==0:
        flash("Todo List is empty right now", "warning")
        return render_template("index.html",datas=datas)
    else:
        return render_template("index.html",datas=datas)
    
@app.route("/Add_Todo", methods = ["GET", "POST"])
@login_required
def Add_Todo():
    form = ToDoForm(request.form)
    if request.method == "POST" and form.validate():
        Author = session["username"]
        ToDo = form.ToDo.data
        Due_Date= form.Due_Date.data
        db_interactions.insert_to_todos(Author,ToDo,Due_Date)
        flash("You have Succesfully Todoed :)","success")
        return redirect(url_for("index"))
    
    else:
        return render_template("add_todo.html",form = form)



@app.route("/register",methods =["GET","POST"])
def register():
    form = RegisterForm(request.form)

    if request.method == "POST" and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        db_interactions.insert_to_users(name,email,password,username)
        flash("You have Succesfully Registered","success")
        return redirect(url_for("login"))
    else: 
       return render_template("register.html", form = form)
    

#Login page routing

@app.route("/Login",methods = ["GET","POST"])
def login():
    form = LoginForm(request.form)
    if  request.method == "POST":
        username = form.username.data
        password_entered = form.password.data
        
        result = db_interactions.check_user(username)
        if  result != None and result[3]==password_entered:
             flash("Login Succesful", "success") 
             session["logged_in"] = True
             session["username"] = username
             return redirect(url_for("index")) 
    
        else:
            flash("Check your credentials!!!", "danger")   
            return redirect(url_for("login")) 
    else:
        return render_template("login.html", form = form)

@app.route("/Logout")
def logout():
    session.clear()
    flash("Logout Succesfull", "warning")  
    return redirect(url_for("index"))

@app.route("/update/<string:id>")
def updatetodo(id):
    db_interactions.updateStatus(id)
    return redirect(url_for("index"))

@app.route("/deltodo/<string:id>")
@login_required
def deltodo(id):
    
    data = db_interactions.get_from_todos_for_id(id)
    
    if data[1] != session["username"]:
        flash("You are not owner of item", "warning") 
        return redirect(url_for("index"))
    else:
        db_interactions.del_item_from_todos_for_id(id)
        return redirect(url_for("index"))

if __name__=="__main__":
    app.run(debug=True)