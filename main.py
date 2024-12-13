from modules.user import User
from modules.category import Category
from modules.payment_type import Payment_type
from modules.transaction import Transaction  

from flask import Flask, redirect, render_template, request, url_for
app = Flask(__name__)


user = User(1, "Diego", "diego@example.com", "senha123")
category = Category(1, "Alimentação", "Gastos com comida")
payment_type = Payment_type(1, "Credito", "Diego Paraguai")

transaction1 = Transaction(
    user=                       user,
    category=                   category,
    payment_type=               payment_type,
    
    transaction_id=             1,
    fact_date=                  "2024-12-09",
    payment_date=               "2024-12-10",
    description=                "Compra de supermercado",
    transaction_type=           "expense",
    value=                      150.75
)

transaction2 = Transaction(
    user=                       user,
    category=                   category,
    payment_type=               payment_type,
    
    transaction_id=             1,
    fact_date=                  "2024-12-09",
    payment_date=               "2024-12-10",
    description=                "Compra de supermercado",
    transaction_type=           "expense",
    value=                      150.75
)


transactions = []
transactions.append(transaction1)
transactions.append(transaction2)



@app.route('/')
def index():
    return redirect(url_for("transaction_list"))

@app.route("/transaction-register")
def transaction_register():
    return render_template("transaction_register.html")  


@app.route("/_transaction-register", methods=["POST"])
def _transaction_register():
    transaction = Transaction(
        user=               user,
        category=           category,
        payment_type=       payment_type,
        
        transaction_id=     1,
        fact_date=          request.form['fact_date'],
        payment_date=       request.form['payment_date'],
        description=        request.form['description'],
        transaction_type=   request.form.get('transaction_type'),
        value=              request.form['value']
    )
    
    
    transactions.append(transaction)
    return redirect(url_for("transaction_list"))  

@app.route("/transaction-list")
def transaction_list():
    return render_template("transaction_list.html", transactions=transactions)  



app.run(debug=True)