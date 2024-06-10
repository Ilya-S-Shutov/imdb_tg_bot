from datetime import datetime

import peewee as pw

db = pw.SqliteDatabase('db.db', pragmas={'foreign_keys': 1})


class BaseModel(pw.Model):
    created_at = pw.DateTimeField(default=datetime.now())

    class Meta:
        database = db
        order_by = ('created_at', )
