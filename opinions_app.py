# what_to_watch/opinions_app.py
from datetime import datetime

# Импортируется функция выбора случайного значения
from random import randrange


from wtforms import StringField, SubmitField, TextAreaField, URLField
from wtforms.validators import DataRequired, Length, Optional

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '#!@HD(Clkxzcv89)'

db = SQLAlchemy(app)


class Opinion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, unique=True, nullable=False)
    source = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


class OpinionForm(FlaskForm):
    title = StringField(
        'Введите название фильма',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 128)]
    )
    text = TextAreaField(
        'Напишите мнение', 
        validators=[DataRequired(message='Обязательное поле')]
    )
    source = URLField(
        'Добавьте ссылку на подробный обзор фильма',
        validators=[Length(1, 256), Optional()]
    )
    submit = SubmitField('Добавить')


@app.route('/')
def index_view():
    # Определяется количество мнений в базе данных
    quantity = Opinion.query.count()
    # Если мнений нет,
    if not quantity:
        # то возвращается сообщение
        return 'В базе данных мнений о фильмах нет.'
    # Иначе выбирается случайное число в диапазоне от 0 и до quantity
    offset_value = randrange(quantity)
    # И определяется случайный объект
    opinion = Opinion.query.offset(offset_value).first()
#    opinion = Opinion.query.get_or_404(id)    
    return render_template('opinion.html', opinion=opinion )


@app.route('/add')
def add_opinion_view():
    # Вот тут создаётся новый экземпляр формы
    form = OpinionForm()  
    return render_template('add_opinion.html', form=form)

@app.route('/opinions/<int:id>')  
# Параметром указывается имя переменной
def opinion_view(id):  
    # Теперь можно запрашивать мнение по id
    opinion = Opinion.query.get_or_404(id)
    # И передавать его в шаблон
    return render_template('opinion.html', opinion=opinion)


if __name__ == '__main__':
    app.run()
