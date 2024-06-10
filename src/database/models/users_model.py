import peewee as pw

from .base_model import BaseModel


class User(BaseModel):
    user_id = pw.TextField(unique=True)

    class Meta:
        db_table = 'users'