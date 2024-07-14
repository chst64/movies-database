#!/usr/bin/env python3

"""
Crea una base de datos de peliculas y la rellena con los datos de un json

=== TODO ===

* Hay que diferenciar si se quiere crear la bbdd desde 0 o actualizar una bbdd existente.
Si es crear una bbdd desde 0 hay que borrar la bbdd existente

"""
import json
import argparse
import colorama
from models import Film, Person, Genero, PersonFilm

colorama.init(autoreset=True)


# Activar el modo DEBUG para hacer pruebas
DEBUG = 1


# Creo las peliculas
def rellena(peli):

    # Miro si ya esta creado el director
    # director = Person.get_or_none(Person.name == peli["director"])

    # # Si el director no esta creado, lo creo
    # if director is None:
    #     director = Person.create(name=peli["director"])
    #     director.save()

    # nueva_peli.director = director.id

    # Creo una peli con el title, year y rate
    nueva_peli = Film(
        title=peli["originalTitle"],
        # director=Person.get(Person.name == peli.get("director", "unknown")),
        year=peli["startYear"],
        rate=peli["averageRating"],
        imdb=peli["imdb"],
        runtime=peli["runtimeMinutes"]
    )

    nueva_peli.save()


def rellena_cast(datos):
    """
    Voy rellenando los actores que han trabajado en cada peli

    * Cargo el fichero "rel_person_movie.json"
    * Antes tendria que haber creado la instancia de la persona que voy a enlazar
    con la pelicula
    * de cada entrada cojo el imdb de la peli, y hago un
    # relacion = ActorFilm.create(film=Film.get(Film.title.contains("piedad")),
    #                             actor=Person.get(Person.name.contains("Robbins"))
    #                             )

    """
    pass


def add_movie(datafile=None):
    """
    Añado a la tabla Film nuevas peliculas con los datos del fichero dado
    """
    print(colorama.Fore.YELLOW + "En add_movie")
    datafile = "./list_movies.json" if datafile is None else datafile

    # Cargo los datos de las peliculas
    with open('./list_movies.json', 'r', encoding='utf-8') as data_movies:
        for line in data_movies.readlines():
            peli = json.loads(line)

            new_film = Film(
                title=peli["originalTitle"],
                year=peli["startYear"],
                rate=peli["averageRating"],
                imdb=peli["imdb"],
                runtime=peli["runtimeMinutes"]
            )

            new_film.save()


def add_rel(fichero=None):
    """
    Creo una nueva relacion persona-pelicula
    fichero: Fichero JSON donde estan los datos
    """
    print(colorama.Fore.YELLOW + "="*5 + "En add_rel" + "="*5)
    # Cargo la relacion
    with open('./rel_person_movie.json', 'r', encoding='utf-8') as f:
        relations_data = json.load(f)

        for relation_data in relations_data:
            id_person = Person.get_or_none(Person.nconst == relation_data['nconst'])
            id_film = Film.get_or_none(Film.imdb == relation_data['tconst'])

            print("==>", Film.get(Film.id == id_film).title,
                  " with",
                  Person.get(Person.id == id_person),
                  "as",
                  relation_data['characters'],
                  )

            new_relation = PersonFilm(
                        person=id_person,
                        film=id_film,
                        category=relation_data['category'],
                        characters=relation_data['characters']
                        )
            print(f"==> {new_relation.film.title} ",
                  f"with {new_relation.person.name}",
                  f"as, {new_relation.category} - {new_relation.characters}")

            new_relation.save()



def add_person(datafile=None):
    """
    Añado a la tabla Person las personas del fichero
    datafile = JSON con los datos de las personas:['nconst','primaryName','birthYear'] 
    """
    print(colorama.Fore.YELLOW + "En add_person")
    datafile = "data_person.json" if datafile is None else datafile

    with open(datafile, "r", encoding='utf-8') as data_person:
        for person in json.load(data_person):
            new_person = Person(
                nconst=person["nconst"],
                name=person["primaryName"],
                birthyear=person["birthYear"]
            )
            new_person.save()


def main():

    print(colorama.Fore.RED + "*"*20)
    print(colorama.Fore.RED + "*** EMPEZANDO ***")
    print(colorama.Fore.RED + "*"*20)

    # Configuro argparser
    parser = argparse.ArgumentParser(
            description="Rellena la bbdd de peliculas",
            epilog="Epilogo de la descripcion del programa"
            )

    parser.add_argument("modo", help="modo new_bbdd - add_movie")
    parser.add_argument("-f", "--fichero", help="fichero con info")

    args = parser.parse_args()

    if args.modo:
        if args.modo == "new_bbdd":
            print(colorama.Fore.YELLOW + "=== BBDD nueva ===")

            add_movie()
            add_person()
            add_rel()
            print(colorama.Fore.YELLOW + "=== Creada nueva bbdd ===")

        elif args.modo == "rel":
            print(colorama.Fore.YELLOW + "=== añadiendo relacion ===")
            if args.fichero:
                add_relation(args.fichero)
            print(colorama.Fore.YELLOW + "=== Añadidas relaciones ===")
        elif args.modo == "person":
            print(colorama.Fore.YELLOW + "=== añadiendo persona ===")
            if args.fichero:
                add_person(args.fichero)
            print(colorama.Fore.YELLOW + "=== Añadidas personas ===")
        else:
            print(colorama.Fore.YELLOW + f"=== El modo {args.modo} no existe ===")

if __name__ == "__main__":

    main()
