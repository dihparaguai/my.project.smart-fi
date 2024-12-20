from modules.user import User
from modules.category import Category
from modules.payment_type import PaymentType
from modules.transaction import Transaction

from flask import Flask, redirect, render_template, request, url_for
app = Flask(__name__)


user = User(1, "Diego", "diego@example.com", "senha123")


category1 = Category(1, "Alimentação", "Gastos com comida")
category2 = Category(2, "Lazer", "Gastos com parque")
category_dict = {
    category1.id: category1,
    category2.id: category2
}


payment_type1 = PaymentType(1, "Credito", "Diego Paraguai")
payment_type2 = PaymentType(2, "Debito", "Diego Paraguai")
payment_type_dict = {
    payment_type1.id: payment_type1,
    payment_type2.id: payment_type2
}


transaction1 = Transaction(user, category1, payment_type1, 1, "2024-12-09", "2024-12-10", "Compra de supermercado", "expense", 150.75)
transaction2 = Transaction(user, category2, payment_type2, 2, "2023-11-08", "2022-09-11", "Compra de ...", "income", 0.75)
transaction_dict = {
    transaction1.id: transaction1,
    transaction2.id: transaction2
}


@app.route('/')
def index():
    return redirect(url_for("transaction_history"))


@app.route("/transaction-history")
def transaction_history():
    return render_template("transaction_history.html", transaction_dict=transaction_dict)


@app.route("/transaction-register")
def transaction_register():
    # renderiza a pagina com os valores cadastrados em banco de dados
    return render_template("transaction_register.html", category_dict=category_dict, payment_type_dict=payment_type_dict)


@app.route("/_transaction-register", methods=["POST"])
def _transaction_register():
    # o retorno do request é uma string, entao foi convertido para int
    category_id = int(request.form.get('category'))
    payment_type_id = int(request.form.get('payment_type'))

    transaction = Transaction(
        user=user,
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
def _transaction_delete():
    transaction_dict[id] = None
    return redirect(url_for("transaction_history"))


app.run(debug=True)
