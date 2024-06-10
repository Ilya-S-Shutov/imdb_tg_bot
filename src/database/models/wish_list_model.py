import peewee as pw

from .base_model import BaseModel
from .users_model import User
from .movies_model import Movie


class WishList(BaseModel):
    user_id = pw.ForeignKeyField(User)
    movie_id = pw.ForeignKeyField(Movie)

    class Meta:
        db_table = 'wish_list'