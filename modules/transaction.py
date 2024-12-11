from modules.category import Category
from modules.user import User
from modules.payment_type import Payment_type


class Transaction():
    def __init__(
            self,

        # composition
        user: User,
        category: Category,
        payment_type: Payment_type,

        # attributes
        transaction_id,
        fact_date,
        payment_date,
        description,
        transaction_type,  # expenses or incomes
        value
    ):
        self.user = user
        self.category = category.name
        self.payment_type = payment_type.name

        self.transaction_id = transaction_id
        self.fact_date = fact_date
        self.payment_date = payment_date
        self.description = description
        self.transaction_type = transaction_type
        self.value = value

#
    def __repr__(self):
        return f'''
        transaction_id = {self.transaction_id}
        fact_date = {self.fact_date}
        payment_date = {self.payment_date}
        value = {self.value}
        description = {self.description}
        transaction_type = {self.transaction_type}
        category = {self.category}
        payment_type = {self.payment_type}
        '''
