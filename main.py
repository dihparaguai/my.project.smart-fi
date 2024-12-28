from modules.user import User
from modules.category import Category
from modules.payment_type import PaymentType
from modules.transaction import Transaction

from flask import Flask, redirect, render_template, request, session, url_for, flash
app = Flask(__name__)
app.config['SECRET_KEY'] = '@chave_secreta@'


user1 = User(id=1, name="Diego", email="diego@example.com", birthdate='1996-11-19', password="senha123")
user2 = User(id=2, name="Rodrigo", email="rodrigo@example.com", birthdate='1997-06-14', password="senha456")
user_dict = {
    user1.id: user1,
    user2.id: user2
}

category1 = Category(id=1, name="Alimentação", description="Gastos com comida")
category2 = Category(id=2, name="Lazer", description="Gastos com parque")
category_dict = {
    category1.id: category1,
    category2.id: category2
}


payment_type1 = PaymentType(id=1, name="Credito", owner="Diego Paraguai")
payment_type2 = PaymentType(id=2, name="Debito", owner="Diego Paraguai")
payment_type_dict = {
    payment_type1.id: payment_type1,
    payment_type2.id: payment_type2
}


transaction1 = Transaction(user=user2, category=category1, payment_type=payment_type1, id=1, fact_date="2024-12-09", payment_date="2024-12-10", description="Compra de supermercado", transaction_type="expense", value=150.75)
transaction2 = Transaction(user=user1, category=category2, payment_type=payment_type2, id=2, fact_date="2023-11-08", payment_date="2022-09-11", description="Compra de ...", transaction_type="income", value=0.75)
transaction_dict = {
    transaction1.id: transaction1,
    transaction2.id: transaction2
}


# pagina inicial
@app.route('/')
def index():
    if 'user_id' not in session or session['user_id'] == None:
        return redirect(url_for('user_login'))
    
    return redirect(url_for('transaction_history'))


# mostra o historico de transacoes já registradas
@app.route("/transaction-history")
def transaction_history():
    if 'user_id' not in session or session['user_id'] == None:
        return redirect(url_for('user_login'))
    
    page_title = 'LISTA DE TRANSAÇÕES'
    return render_template("transaction_history.html", page_title=page_title, transaction_dict=transaction_dict)


# renderiza pagina para registrar uma transacao
@app.route("/transaction-register")
def transaction_register():  
    if 'user_id' not in session or session['user_id'] == None:
        return redirect(url_for('user_login'))
    
    page_title = 'CADASTRAR NOVA TRANSAÇÃO'    
    return render_template("transaction_register.html", page_title=page_title, category_dict=category_dict, payment_type_dict=payment_type_dict)


# registra uma transacao do formulario, nao passa os dados pela URL
@app.route("/_transaction-register", methods=["POST"])
def _transaction_register():
    # o retorno do request é uma string, entao foi convertido para int
    category_id = int(request.form.get('category'))
    payment_type_id = int(request.form.get('payment_type'))

    transaction = Transaction(
        # user=
        category=category_dict[category_id],
        payment_type=payment_type_dict[payment_type_id],

        id=4,
        fact_date=request.form['fact_date'],
        payment_date=request.form['payment_date'],
        description=request.form['description'],
        transaction_type=request.form.get('transaction_type'),
        value=request.form['value']
    )

    transaction_dict[transaction.id] = transaction
    return redirect(url_for("transaction_history"))


# renderiza a pagina com a transacao escolhida atravez do id
@app.route("/transaction-update/<int:id>")
def transaction_update(id):
    if 'user_id' not in session or session['user_id'] == None:
        return redirect(url_for('user_login'))
    
    transaction = transaction_dict[id]
    page_title = 'EDITAR TRANSAÇÃO'    
    return render_template("transaction_update.html", page_title=page_title, category_dict=category_dict, payment_type_dict=payment_type_dict, transaction=transaction)


# atualiza a transacao
@app.route("/_transaction-update", methods=["POST"])
def _transaction_update():
    transaction = transaction_dict[int(request.form['id'])]
    
    transaction.category=category_dict[int(request.form.get('category'))]
    transaction.payment_type=payment_type_dict[int(request.form.get('payment_type'))]
    transaction.fact_date=request.form['fact_date']
    transaction.payment_date=request.form['payment_date']
    transaction.description=request.form['description']
    transaction.transaction_type=request.form.get('transaction_type')
    transaction.value=request.form['value']
    
    return redirect(url_for("transaction_history"))

# remove a transacao atraves do ID
@app.route("/_transaction-delete/<int:id>")
def _transaction_delete(id):
    transaction_dict.pop(id)
    return redirect(url_for("transaction_history"))


# renderiza a pagina de entrada do usuario
@app.route("/user-login")
def user_login():
    if 'user_id' in session and session['user_id'] is not None:
        return redirect(url_for('index'))

    email = request.args.get('email', '')
    page_title = 'LOGIN' 
    return render_template("user_login.html", page_title=page_title, email=email)


# autentica se o usuario e senha existem
@app.route("/_user-login", methods=['POST'])
def _user_login():
    
    email = request.form['email']
    password = request.form['password']
    
    for user in user_dict.values():
        if user.email == email:
            if user.password == password:
                session['user_id'] = user.id
                flash('Logado com sucesso', 'success')
                return redirect(url_for('transaction_history'))
    
    flash('Usuario ou senha nao existe', 'error')    
    return redirect(url_for('user_login', email=email))


# renderiza a pagina de registro de usuario
@app.route("/user-register")
def user_register():
    if 'user_id' in session and session['user_id'] is not None:
        return redirect('transaction_history')
    
    email = request.args.get('email', '')
    name = request.args.get('name', '')
    birthdate = request.args.get('name', '')
    page_title = 'CADASTRO DE LOGIN' 
    return render_template("user_register.html", page_title=page_title, email=email, name=name, birthdate=birthdate)


# valida o novo cadastro de usuario se já não existir
@app.route("/_user-register", methods=['POST'])
def _user_register():
    
    email = request.form['email']
    name = request.form['name']
    birthdate = request.form['birthdate']
    password = request.form['password']
    password_retyped = request.form['password_retyped']
    
    if password != password_retyped:
        flash('Senhas não foram digitadas iguais', 'error')
        return redirect(url_for('user_register', email=email, name=name, birthdate=birthdate))
    
    for user in user_dict.values():
        if user.email == email:
            flash('Usuario ja existe', 'error')
            return redirect(url_for('user_register', email=email, name=name, birthdate=birthdate))
        
    user = User(id=3, email=email, name=name, birthdate=birthdate, password=password)    
    user_dict[user.id] = user
    flash('Usuario cadatradado com sucesso', 'success') 
    return redirect(url_for('user_login', email=email))


# renderiza a pagina para usuario recuperar a senha
@app.route('/user-recover-password')
def user_recover_password():
    if 'user_id' in session and session['user_id'] is not None:
        return redirect('index')
    
    email = request.args.get('email', '')
    birthdate = request.args.get('birthdate', '')
    page_title = 'RECUPERAR SENHA'
    return render_template('user_recover_password.html', page_title=page_title, email=email, birthdate=birthdate)
    

# valida a recuperacao de senha e substitui a senha antiga
@app.route('/_user-recover-password', methods=['POST'])
def _user_recover_password():
    email = request.form['email']
    birthdate = request.form['birthdate']
    password = request.form['password']
    password_retyped = request.form['password_retyped']
    
    if password != password_retyped:
        flash('Senhas não foram digitadas iguais', 'error')
        return redirect(url_for('user_recover_password', email=email, birthdate=birthdate))
    
    # verifica e altera a senha
    for user in user_dict.values():
        if email == user.email and birthdate == user.birthdate:
            user.password = password
            user_dict[user.id] = user
            flash('Senha alterada com sucesso', 'sucess')
            return redirect(url_for('user_login', email=email))
    
    flash('Email ou data de nascimentos não existem ou não estão corretos', 'error')
    return redirect(url_for('user_recover_password', email=email, birthdate=birthdate))


# desloga usuario e o remove da sessao do negavegor
@app.route('/user-logout')
def _user_logout():
    for user in user_dict.values():
        if session['user_id'] == user.id:
            email = user.email
            name = user.name
            
    session['user_id'] = None
    flash(f'{name} foi deslogado com sucesso!', 'info')
    return redirect(url_for('user_login', email=email))


app.run(debug=True)