from modules.category import Category
from modules.user import User
from modules.payment_type import PaymentType


class Transaction():
    def __init__(
            self,

        # composition
        user: User,
        category: Category,
        payment_type: PaymentType,

        # attributes
        id,
        fact_date,
        payment_date,
        description,
        transaction_type,  # expenses or incomes
        value
    ):
        self.user = user
        self.category = category
        self.payment_type = payment_type

        self.id = id
        self.fact_date = fact_date
        self.payment_date = payment_date
        self.description = description
        self.transaction_type = transaction_type
        self.value = value

#
    def __repr__(self):
        return f'''
        id = {self.id}
        fact_date = {self.fact_date}
        payment_date = {self.payment_date}
        description = {self.description}
        transaction_type = {self.transaction_type}
        value = {self.value}
        category = {self.category.name}
        payment_type = {self.payment_type.name}
        '''
