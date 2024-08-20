import os

from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Float, text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

app = Flask(__name__)
app.config["SECRET_KEY"] = "MySceretKetToDo"  # os.environ.get("SECRET_KEY")
Bootstrap5(app)


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo-data.db"  # os.environ.get("DB_URI")
db.init_app(app)

class User(db.Model):
    __tablename__ = "tbl_user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(300), nullable=False)
    name: Mapped[str] = mapped_column(String(350), nullable=False)

class ToDO(db.Model):
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


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/profile')
def profile_home():
    return render_template('profile.html')

if __name__ == "__main__":
    app.run(debug=False)