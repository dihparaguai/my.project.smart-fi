from modules.user import User
from modules.category import Category
from modules.payment_type import PaymentType
from modules.transaction import Transaction

from flask import Flask, redirect, render_template, request, session, url_for, flash
app = Flask(__name__)
app.config['SECRET_KEY'] = '@chave_secreta@'


user1 = User(id=1, name="Diego", email="diego@example.com", password="senha123")
user2 = User(id=2, name="Rodrigo", email="rodrigo@example.com", password="senha456")
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


@app.route('/')
def index():
    return redirect(url_for('user_login'))


@app.route("/transaction-history")
def transaction_history():
    if 'user' not in session or session['user'] == None:
        return redirect(url_for('user_login'))
    return render_template("transaction_history.html", transaction_dict=transaction_dict)


@app.route("/transaction-register")
def transaction_register():  
    if 'user' not in session or session['user'] == None:
        return redirect(url_for('user_login'))
    
    # renderiza a pagina com os valores cadastrados em banco de dados
    return render_template("transaction_register.html", category_dict=category_dict, payment_type_dict=payment_type_dict)


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


@app.route("/transaction-update/<int:id>")
def transaction_update(id):
    if 'user' not in session or session['user'] == None:
        return redirect(url_for('user_login'))
    
    transaction = transaction_dict[id]
    return render_template("transaction_update.html", category_dict=category_dict, payment_type_dict=payment_type_dict, transaction=transaction)


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


@app.route("/_transaction-delete/<int:id>")
def _transaction_delete(id):
    transaction_dict.pop(id)
    return redirect(url_for("transaction_history"))


@app.route("/user-login")
# renderiza a pagina de entrada do usuario
def user_login():
    if 'user' not in session or session['user'] == None:
        return render_template("user_login.html")
    
    return redirect(url_for('transaction_history'))


@app.route("/_user-login", methods=['POST'])
# autentica se o usuario e senha existem
def _user_login():
    
    email = request.form['email']
    password = request.form['password']
    
    for user in user_dict.values():
        if user.email == email:
            if user.password == password:
                session['user'] = user.name
                flash('Logado com sucesso', 'success')
                return redirect(url_for('transaction_history'))
    
    flash('Usuario ou senha nao existe', 'error')    
    return redirect(url_for('user_login'))


@app.route("/user-register")
# renderiza a pagina de registro de usuario
def user_register():
    if 'user' not in session or session['user'] == None:
        return render_template("user_register.html", email="", name="")
    return redirect('transaction_history')


@app.route("/_user-register", methods=['POST'])
# valida o novo cadastro de usuario
def _user_register():
    
    email = request.form['email']
    name = request.form['name']
    password = request.form['password']
    password_retyped = request.form['password_retyped']
    
    if password != password_retyped:
        flash('Senhas não foram digitadas iguais', 'error')
        return redirect(url_for("user_register"))
    
    for user in user_dict.values():
        if user.email == email:
            flash('Usuario ja existe', 'error')
            return render_template("user_register.html", email=email, name=name)
        
    user = User(id=3, email=email, name=name, password=password)
    
    user_dict[user.id] = user
    flash('Usuario cadatradado com sucesso', 'success') 
    return redirect(url_for('user_login'))


@app.route('/user-logout')
def _user_logout():
    session['user'] = None
    return redirect(url_for('user_login'))


app.run(debug=True)
