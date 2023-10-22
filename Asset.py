class Asset:
    def __init__(self, user_id, name, description, purchase_date, appreciation, initial_value):
        self.user_id = user_id
        self.name = name
        self.description = description
        self.purchase_date = purchase_date
        self.appreciation = appreciation
        self.initial_value = initial_value


    def serialize(self):
        return {
            '_id': str(self._id) if self._id else None,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'purchase_date': self.purchase_date,
            'appreciation': self.appreciation,
            'initial_value': self.initial_value,
        }