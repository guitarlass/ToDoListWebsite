import os
import datetime

from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Float, text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = "MySceretKetToDo"  # os.environ.get("SECRET_KEY")
Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(user_id):
    return db.get_or_404(User, user_id)


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo-data.db"  # os.environ.get("DB_URI")
db.init_app(app)


class User(db.Model, UserMixin):
    __tablename__ = "tbl_user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(300), nullable=False)
    name: Mapped[str] = mapped_column(String(350), nullable=False)


class ToDo(db.Model):
    __tablename__ = "tbl_todo"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("tbl_user.id"))
    user = relationship("User", backref="tbl_user")


class ListItem(db.Model):
    __tablename__ = "tbl_list_item"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[int] = mapped_column(Integer, default=0)

    todo_id: Mapped[int] = mapped_column(Integer, ForeignKey("tbl_todo.id"))
    todo = relationship("ToDo", backref="tbl_list_item")


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def home():
    register_form = RegisterForm()
    open_modal = 0
    if register_form.validate_on_submit():
        user_exists = db.session.execute((db.select(User).where(User.email == register_form.email.data))).scalar()
        if user_exists:
            flash("User already registered! Please login.")
            return redirect(url_for("login"))
        else:
            new_user = User(name=register_form.name.data,
                            email=register_form.email.data,
                            password=generate_password_hash(register_form.password.data,
                                                            method="pbkdf2:sha256",
                                                            salt_length=8))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("profile"))
    else:
        if request.method == 'POST':
            open_modal = 1
    return render_template('index.html', form=register_form, open_modal=open_modal)


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = db.session.execute(db.select(User).where(User.email == login_form.email.data)).scalar()
        if not user:
            flash("User not found!")
        else:
            if check_password_hash(user.password, login_form.password.data):
                login_user(user)
                return redirect(url_for("profile"))
            else:
                flash("Password incorrect!")
    return render_template('login.html', form=login_form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route('/register', methods=['POST'])
def register():
    register_form = RegisterForm()
    user_exists = db.session.execute((db.select(User).where(User.email == register_form.email.data)))
    if user_exists:
        flash("User already registered! Please login.")
    if register_form.validate_on_submit():
        new_user = User(name=register_form.name.data,
                        email=register_form.email.data,
                        password=generate_password_hash(register_form.password.data,
                                                        method="",
                                                        salt_length=8))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("profile"))
    return render_template("register.html", form=register_form)


@app.route('/save_items', methods=['POST'])
def save_items():
    items = request.get_json()

    current_date = datetime.date.today()

    # Create the todo list string
    new_list_name = "Todo list : " + current_date.strftime("%Y/%m/%d")

    new_list = ToDo(name=new_list_name, user_id=current_user.id)
    db.session.add(new_list)
    db.session.commit()

    new_list_id = new_list.id

    for item in items:
        new_list_item = ListItem(name=item['item_name'], status=item['checked'], todo_id=new_list_id)
        db.session.add(new_list_item)
        db.session.commit()

    return jsonify({'message': "successful"})


if __name__ == "__main__":
    app.run(debug=False)
