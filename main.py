from modules.user import User
from modules.category import Category
from modules.payment_type import Payment_type
from modules.transaction import Transaction

from flask import Flask, redirect, render_template, request, url_for
app = Flask(__name__)


user = User(1, "Diego", "diego@example.com", "senha123")


category1 = Category(1, "Alimentação", "Gastos com comida")
category2 = Category(2, "Lazer", "Gastos com parque")
category_dict = {
    category1.id : category1,
    category2.id : category2
}


payment_type = Payment_type(1, "Credito", "Diego Paraguai")


transaction1 = Transaction(
    user,
    category1,
    payment_type,

    1,
    "2024-12-09",
    "2024-12-10",
    "Compra de supermercado",
    "expense",
    150.75
)
transaction2 = Transaction(
    user=user,
    category=category2,
    payment_type=payment_type,

    id=2,
    fact_date="2024-12-09",
    payment_date="2024-12-10",
    description="Compra de supermercado",
    transaction_type="expense",
    value=150.75
)
transaction_list = []
transaction_list.append(transaction1)
transaction_list.append(transaction2)


@app.route('/')
def index():
    return redirect(url_for("transaction_history"))


@app.route("/transaction-register")
def transaction_register():
    return render_template("transaction_register.html", category_dict=category_dict)


@app.route("/_transaction-register", methods=["POST"])
def _transaction_register():
    # o retorno do request é uma string, entao foi convertido
    category_id = int(request.form.get('category'))
    
    transaction = Transaction(
        user=user,
        category=category_dict.get(category_id),
        payment_type=payment_type,

        id=1,
        fact_date=request.form['fact_date'],
        payment_date=request.form['payment_date'],
        description=request.form['description'],
        transaction_type=request.form.get('transaction_type'),
        value=request.form['value']
    )
        
    transaction_list.append(transaction)
    return redirect(url_for("transaction_history"))


@app.route("/transaction-history")
def transaction_history():
    return render_template("transaction_history.html", transaction_list=transaction_list)


app.run(debug=True)
