from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_sqlalchemy import SQLAlchemy

# Konfigurace aplikace
app = Flask(__name__)
app.secret_key = 'secret-key-for-flash-messages'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Databáze
db = SQLAlchemy(app)

# Model databáze
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

# WTForms formulář
class UserForm(FlaskForm):
    first_name = StringField('Jméno', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Příjmení', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Přidat')

# Hlavní stránka
@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

# Přidání uživatele
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        # Uložení uživatele do databáze
        new_user = User(first_name=form.first_name.data, last_name=form.last_name.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Uživatel byl úspěšně přidán!', 'success')
        return redirect(url_for('index'))
    return render_template('add_user.html', form=form)

# Odstranění uživatele
@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Uživatel byl úspěšně odstraněn!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Inicializace databáze
    with app.app_context():
        db.create_all()
    app.run(debug=True)
