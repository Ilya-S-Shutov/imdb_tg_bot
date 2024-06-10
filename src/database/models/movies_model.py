import peewee as pw

from .base_model import BaseModel


class Movie(BaseModel):

    title = pw.TextField()
    original_title = pw.TextField()
    rating = pw.FloatField()
    year = pw.IntegerField()
    type = pw.TextField()
    img_url = pw.TextField()
    overview = pw.TextField()
    # director = pw.TextField()

    class Meta:
        db_table = 'movies'
