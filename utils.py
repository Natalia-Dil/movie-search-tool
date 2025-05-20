import tabulate
from IPython.display import Image, display
from db import connect_to_database
import db_main_config

def format_field(value):
    if isinstance(value, (list, tuple, set)):
        return ", ".join(str(v) for v in value)
    return value

def clean_text(value):
    if isinstance(value, str):
        return value.replace("[", "").replace("]", "").replace("'", "").replace('"', '')
    return value

def print_results(results, columns=None):
    if results:
        if isinstance(results[0], dict):
            if not columns:
                columns = ['Title', 'Year', 'Rating', 'Genres', 'Directors', 'Cast']
            data = [[
                movie.get('title'),
                movie.get('year'),
                movie.get('imdb.rating'),
                movie.get('genres'),
                movie.get('directors'),
                movie.get('cast')
            ] for movie in results]
        else:
            data = results
            if not columns:
                columns = ['Result']
        print(tabulate.tabulate(data, columns, tablefmt='grid'))

def get_genres():
    connection = connect_to_database(db_main_config.db_config)
    cursor = connection.cursor()

    cursor.execute("SELECT genres FROM movies")
    genres_raw = cursor.fetchall()

    cursor.close()
    connection.close()

    genre_set = set()

    for row in genres_raw:
        genres = row[0]
        if genres:
            genres_str = str(genres).replace("{", "").replace("}", "")
            genre_list = [g.strip().strip("'") for g in genres_str.split(",")]
            genre_set.update(genre_list)

    genre_set.discard('')
    genres_sorted = sorted(genre_set)

    print("\n🎭 Available genres:")
    print(", ".join(genres_sorted))

def choose_movie(results):
    if not results:
        return

    print("\nℹ️ Do you want to see more details about a movie?")
    for idx, movie in enumerate(results, start=1):
        print(f"{idx}. {movie.get('title')}")

    choice = input("\n🔢 Enter the movie number or press Enter to skip: ")
    if not choice or not choice.isdigit():
        return

    movie = results[int(choice) - 1]
    genres = format_field(movie.get('genres'))
    directors = clean_text(movie.get('directors'))
    cast = clean_text(movie.get('cast'))

    print("\n ========== 📖 Movie details ==========")
    print(f"🎬 Title: {movie.get('title')}")
    print(f"📅 Year: {movie.get('year')}")
    print(f"⭐️ Rating: {movie.get('imdb.rating')}")
    print(f"🎭 Genres: {genres}")
    print(f"⏱️ Runtime: {movie.get('runtime')} min")
    print(f"🎬 Director: {directors}")
    print(f"👥 Cast: {cast}")
    print(f"📝 Description: {movie.get('plot')}")

    connection = connect_to_database(db_main_config.db_config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT poster FROM movies WHERE title = %s LIMIT 1", (movie.get('title'),))
    poster = cursor.fetchone()
    cursor.close()
    connection.close()

    if poster and poster.get('poster'):
        display(Image(url=poster.get('poster')))
    else:
        print("\n🎨 Poster not found")
    print("\n========== 🍿🥤🎬 Enjoy the movie! ==========")