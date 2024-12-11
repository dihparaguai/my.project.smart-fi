class Payment_type:
    def __init__(self, payment_type_id, name, owner):
        self.payment_type_id = payment_type_id
        self.name = name
        self.owner = owner
        
    def __repr__(self):
        return f'''
        payment_type_id = {self.payment_type_id}
        name = {self.name}
        owner = {self.owner}
        
        '''