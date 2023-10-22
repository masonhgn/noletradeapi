class TradingStrategy:
    def __init__(self, user_id, name, description):
        self.user_id = user_id
        self.name = name
        self.description = description

    def serialize(self):
        return {
            '_id': str(self._id),
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description
        }