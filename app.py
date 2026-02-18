#!/usr/bin/env python3

"""
Example of how to use Flask + peewee

Web about films

https://www.movieposterdb.com/

TODO
* Dividir las consultas en paginas
* Inspirarse en www.themoviedb.org
* Menu peliculas / Series / Gente
* El reparto en una barra horizontal con scroll

"""

from colorama.initialise import reset_all
from flask import Flask, render_template, request, url_for, redirect
# from peewee import *

from models import Film, Person, Genero, PersonFilm
from playhouse.flask_utils import object_list

from colorama import Fore, Style, init

from logging_config import setup_logging
import logging


# Inicio de la app Flask
app = Flask(__name__)


# Configurar el logging al iniciar la aplicación
setup_logging(max_size_mb=5, backup_count=3)
logger_pruebas = logging.getLogger("pruebas")
logger = logging.getLogger("main")

logger.warning(Fore.YELLOW + "=== Iniciando aplicacion ===" + Style.RESET_ALL)


# === Funciones varias ===
def get_all_films():
    logger_pruebas.info("En get_all_films()")
    list_films = []
    for film in Film.select():
        list_films.append(
            {
                "id": film.id,
                "title": film.title,
                "imdb": film.imdb,
                # "director": Person.get_by_id(film.director).name,
                "year": film.year,
                "rate": film.rate,
            }
        )
    return list_films


def get_all_people():
    list_people = []
    for person in Person.select()[0:25]:
        print(">> Tengo:", person)
        list_people.append(
            {
                "id": person.id,
                "nconst": person.nconst,
                "name": person.name,
                "birthyear": person.birthyear,
            }
        )
    return list_people


def get_some_films(busqueda):
    list_films = []
    for film in Film.select().where(Film.title.contains(busqueda)):
        print(">>>", film)
        list_films.append(
            {
                "id": film.id,
                "title": film.title,
                "imdb": film.imdb,
                # "director": Person.get_by_id(film.director).name,
                "year": film.year,
                "rate": film.rate,
            }
        )

    print(Fore.RED + "list_films: >>")
    print(list_films)
    return list_films


def get_cast(film_to_get_cast):
    """
    Get the cast that appears in a film
    return: list of actors
    """
    print(Fore.RED + "En get_cast")

    actors = []
    directors = []
    for q in PersonFilm.select().where(PersonFilm.film == film_to_get_cast):
        print(Fore.RED + str(q.person))

        dicc_person = {
            "id": q.person.id,
            "nconst": q.person.nconst,
            "name": q.person.name,
            "category": q.category,
            "characters": q.characters,
        }

        if q.category == "actor" or q.category == "actress":
            actors.append(dicc_person)
        elif q.category == "director":
            directors.append(dicc_person)

    print(">>> actors:", actors)
    print(">>> directors:", directors)
    return (actors, directors)


def get_part_of(id):
    """
    Devuelve una lista de las peliculas en las que ha participado
    la persona con 'id', ya sea como actor, director, ...
    """
    part_of = []
    for q in PersonFilm.select().where(PersonFilm.person == id):
        print(">--> ", q.film)
        part_of.append(q.film)

    return part_of


# === Routes ===
@app.route("/", methods=["GET", "POST"])
def index():
    """
    Indice de la pagina. De momento no sirve para nada
    """
    return render_template("index.html")


@app.route("/lista_peliculas", methods=["GET", "POST"])
def lista_peliculas():
    """
    Lista todas las peliculas y tambien se puede hacer un busqueda
    """
    if request.method == "GET":
        print(Fore.RED + "Viewing list of all films")
        all_films = get_all_films()
        return render_template("films.html", films=all_films)
    elif request.method == "POST":
        print(Fore.RED + "Modo POST")
        print(request.form["title"])
        all_films = get_some_films(request.form["title"])
        return render_template("films.html", films=all_films)


@app.route("/lista_gente", methods=["GET", "POST"])
def lista_gente():
    """
    Lista de personas
    """
    print(Fore.RED + "Viewing list of people")
    all_people = get_all_people()
    return render_template("people.html", people=all_people)


@app.route("/page_peliculas", methods=["GET", "POST"])
def page_peliculas():
    if request.method == "GET":
        q_peli = Film.select()
        return object_list(
            "films_page.html",
            query=q_peli,
            context_variable="post_list",
            paginate_by=10,
        )

    elif request.method == "POST":
        q_peli = Film.select().where(Film.title.contains(request.form["title"]))
        return object_list(
            "films_page.html",
            query=q_peli,
            context_variable="post_list",
            paginate_by=10,
        )


@app.route("/<int:id>/edit", methods=["GET", "POST"])
def film_edit(id):
    film = Film.get_by_id(id)
    print(Fore.YELLOW + film)

    return render_template("details.html", film=film)


@app.route("/<int:id>/details", methods=["GET", "POST"])
def details(id):
    film = Film.get_by_id(id)
    print(">>>> Film:", film.title)
    actors, directors = get_cast(film)

    return render_template(
        "details.html", film=film, actors=actors, directors=directors
    )


@app.route("/<int:id>/person_details", methods=["GET", "POST"])
def person_details(id):
    person = Person.get_by_id(id)
    part_of = get_part_of(id)
    print(">>>> person:", person.name)

    return render_template("person_details.html", part_of=part_of, person=person)


@app.route("/<int:id>/delete")
def delete(id):
    print(Fore.YELLOW + ">>>> Borrando film id:", id)
    film = Film.get_by_id(id)
    film.delete_instance()

    return redirect(url_for("lista_peliculas"))


# **************************************************


if __name__ == "__main__":
    init(autoreset=True)

    app.run(debug=True)
