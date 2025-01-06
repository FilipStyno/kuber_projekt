from flask import Flask, request, render_template, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'secret-key-for-flash-messages'

# Seznam uživatelů jako dočasné úložiště
users = []

@app.route('/')
def index():
    return render_template('index.html', users=users)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # Získání dat z formuláře
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        
        # Validace formuláře
        if not first_name or not last_name:
            flash('Jméno a příjmení jsou povinná pole!', 'error')
            return redirect(url_for('add_user'))
        
        # Přidání uživatele do seznamu
        users.append({'first_name': first_name, 'last_name': last_name})
        flash('Uživatel byl úspěšně přidán!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add_user.html')

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if 0 <= user_id < len(users):
        del users[user_id]
        flash('Uživatel byl úspěšně odstraněn!', 'success')
    else:
        flash('Uživatel nebyl nalezen!', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
