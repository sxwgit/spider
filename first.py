from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

from begin import find_key

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm):
    name = StringField('请输入商品名', )
    choose = SelectField('类型', choices=[(1, '商品'), (2, '人物')], validators=[DataRequired()])
    submit = SubmitField()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.submit.data:
        if form.choose.data == '2':
            name = form.name.data
        if form.choose.data == '1':
            data, pic_url, price_picurl = find_key(form.name.data)
            return render_template('nothing.html', list1=data[0], list2=data[1], pic_url=pic_url,
                                   key_word=form.name.data,
                                   price_picurl=price_picurl)
        form.name.data = ''
    return render_template('index.html', form=form, name=name)


if __name__ == '__main__':
    app.run(debug=True)
