import datetime
import uuid
class TradingStrategy:
    def __init__(self, user_id, name, description, type, frequency):
        self._id = str(uuid.uuid4())  # Generate a unique UUID
        self.user_id = user_id
        self.name = name
        self.description = description
        self.type = type  # momentum, reversion
        self.frequency = frequency  # 1d, 2d, 1w, 2w, etc.
        self.execution_date = datetime.date.today()
        self.active = False

    def serialize(self):
        return {
            '_id': self._id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'type': self.type,
            'frequency': self.frequency,
            'execution_date': self.execution_date,
            'active': self.active,
        }
