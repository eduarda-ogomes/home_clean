import uuid

class BaseModel:
    def __init__(self):
        self._id = id if id else str(uuid.uuid4())

    @property
    def id(self):
        return self._id
    
