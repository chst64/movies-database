from peewee import SqliteDatabase, Model
from peewee import IntegerField, CharField, ForeignKeyField, DecimalField, TimeField

"""
Models for the film database
"""

# db = SqliteDatabase(':memory:', pragmas={'foreign_keys': 1})
db = SqliteDatabase('./films.db', pragmas={'foreign_keys': 1})


class BaseModel(Model):
    class Meta:
        database = db


class Person(BaseModel):
    """
    id, nconst, name, birthyear
    """
    id = IntegerField(primary_key=True)
    nconst = CharField(null=True)
    name = CharField()
    birthyear = IntegerField(null=True)

    def __str__(self):
        return f"{self.nconst} - {self.name}"


class Film(BaseModel):
    id = IntegerField(primary_key=True)
    imdb = IntegerField(null=True)
    title = CharField()
    director = ForeignKeyField(Person, backref='peli_dirigida', null=True)
    year = IntegerField()
    rate = DecimalField(null=True)
    duration = TimeField(null=True)
    original_title = CharField(null=True)

    def __str__(self):
        return f"{self.title} - {self.year} - {self.rate} "


class PersonFilm(BaseModel):
    id = IntegerField(primary_key=True)
    person = ForeignKeyField(Person, null=True)
    film = ForeignKeyField(Film, null=True)
    category = CharField(null=True)
    characters = CharField(null=True)



class Genero(BaseModel):
    id = IntegerField(primary_key=True)
    nombre = CharField()
    pelicula = ForeignKeyField(Film, backref='genero', null=True)


db.connect()
db.create_tables([Film, Person, Genero, PersonFilm])
