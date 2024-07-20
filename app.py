#!/usr/bin/env python3

"""
Example of how to use Flask + peewee

Web about films

"""

from flask import Flask, render_template, request, url_for, redirect
# from peewee import *

from models import Film, Person, Genero, PersonFilm

import colorama

app = Flask(__name__)


# === Load the models ===
def get_all_films():

    print(colorama.Fore.RED + "En get_all_films()")
    list_films = []
    for film in Film.select():
        list_films.append(
            {"id": film.id,
             "title": film.title,
             "imdb": film.imdb,
             # "director": Person.get_by_id(film.director).name,
             "year": film.year,
             "rate": film.rate
             }
        )
    return list_films


def get_some_films(busqueda):

    print(colorama.Fore.RED + "En get_some_films()" + "Recibido:" + busqueda)
    list_films = []
    for film in Film.select().where(Film.title.contains(busqueda)):
        print(">>>", film)
        list_films.append(
            {"id": film.id,
             "title": film.title,
             "imdb": film.imdb,
             # "director": Person.get_by_id(film.director).name,
             "year": film.year,
             "rate": film.rate
             }
        )
   
    print(colorama.Fore.RED + "list_films: >>")
    print(list_films)
    return list_films

def get_cast(film_to_get_cast):
    """
    Get the cast that appears in a film
    return: list of actors
    """
    print(colorama.Fore.RED + "En get_cast")

    actors = []
    directors = []
    for q in PersonFilm.select().where(PersonFilm.film == film_to_get_cast):
        print(colorama.Fore.RED + str(q.person))

        dicc_person = {"id": q.person.id,
                       "nconst": q.person.nconst,
                       "name": q.person.name,
                       "category": q.category,
                       "characters": q.characters}

        if q.category == "actor" or q.category == "actress":
            actors.append(dicc_person)
        elif q.category == "director":
            directors.append(dicc_person)

    print(">>> actors:", actors)
    print(">>> directors:", directors)
    return (actors, directors)


# === Routes ===
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Indice de la pagina. De momento no sirve para nada
    """
    print(colorama.Fore.RED + "I'm in index")
    return render_template('index.html')


@app.route('/lista_peliculas', methods=['GET', 'POST'])
def lista_peliculas():
    """
    Indice de la pagina. De momento no sirve para nada
    """
    if request.method == 'GET':
        print(colorama.Fore.RED + "Viewing list of all films")
        all_films = get_all_films()
        return render_template('films.html', films=all_films)
    elif request.method == 'POST':
        print(colorama.Fore.RED + "Modo POST")
        print(request.form['title'])
        all_films = get_some_films(request.form['title'])
        return render_template('films.html', films=all_films)


@app.route("/<int:id>/edit", methods=["GET", "POST"])
def film_edit(id):
    film = Film.get_by_id(id)
    print(colorama.Fore.YELLOW + film)

    return render_template('details.html', film=film)


@app.route("/<int:id>/details", methods=["GET", "POST"])
def details(id):

    film = Film.get_by_id(id)
    print(">>>> Film:", film.title)
    actors, directors = get_cast(film)

    return render_template('details.html', film=film, actors=actors, directors=directors)


@app.route("/<int:id>/delete")
def delete(id):

    print(colorama.Fore.YELLOW + ">>>> Borrando film id:", id)
    film = Film.get_by_id(id)
    film.delete_instance()

    return redirect(url_for('lista_peliculas'))

# **************************************************


if __name__ == '__main__':
    print("*"*20)
    print("* PROGRAMA PRINCIPAL DE BASE DE DATOS * ")
    print("*"*20)

    colorama.init(autoreset=True)

    app.run(debug=True)
