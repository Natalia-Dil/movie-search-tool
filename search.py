from db import connect_to_database
import db_main_config
import db_log_config
from logger import create_log, insert_query
from utils import print_results, choose_movie, get_genres
import tabulate


def search_movies():
    connection = connect_to_database(db_main_config.db_config)
    cursor = connection.cursor(dictionary=True)

    print('''
                
                ========== Welcome to Movie Selector 🎬 ==========

                    🔍 How would you like to explore movies?
             
                     1 - Filter by genre, keyword or year 🎯
                     2 - Top 5 movies by rating ⭐️
                     3 - Top 10 Oscar-winning movies 🏆
                     4 - Top 10 Oscar-nominated movies 🏅
                     5 - Top 10 longest movies ⏳
                     6 - Top 10 underrated movies 🤔
           
    ''')

    choice = input('\n👉 Your choice: ')

    if choice == "1":
        query = "SELECT * FROM movies WHERE 1=1"
        params = []

        get_genres()
        genre = input('Enter a genre (or leave it blank): ')
        year = input('Enter the release year (or leave it blank): ')
        operator_year = input('Enter the operator for the year [>, <, =, >=, <=]: ')

        while (year and not operator_year) or (operator_year and not year):
            print("\n❗ Warning: You must enter both the year and the operator")
            year = input('Enter the release year: ')
            operator_year = input('Enter the operator for the year [>, <, =, >=, <=]: ')

        keyword_plot = input('Enter a keyword for the plot (or leave it blank): ')
        keyword_title = input('Enter a keyword for the title (or leave it blank): ')

        if genre:
            query += " AND genres LIKE %s"
            params.append(f"%{genre}%")
        if year and operator_year:
            query += f" AND year {operator_year} %s"
            params.append(year)
        if keyword_title:
            query += " AND title LIKE %s"
            params.append(f"%{keyword_title}%")
        if keyword_plot:
            query += " AND plot LIKE %s"
            params.append(f"%{keyword_plot}%")

        cursor.execute(query, params)
        results = cursor.fetchall()

        if not results:
            print("\n🚫 No results found.")
            connection.close()
            return
        print("\n========== 🎉 Great! The movie list is shown above. ==========\n")
        print_results(results)

        add_more = input("\n🔎 Add an additional filter? (y/n): ").lower()

        if add_more == "y":
            languages = input('Enter the language (or leave it blank): ')
            directors = input('Enter the director (or leave it blank): ')
            cast = input('Enter the actor (or leave it blank): ')
            runtime = input('Enter the runtime (or leave it blank): ')
            operator_runtime = input('Enter the operator for the runtime [>, <, =, >=, <=]: ')

            while (runtime and not operator_runtime) or (operator_runtime and not runtime):
                print("\n❗ Warning: You must enter both the runtime and the operator")
                runtime = input('Enter the runtime: ')
                operator_runtime = input('Enter the operator for the runtime [>, <, =, >=, <=]: ')

            if languages:
                query += " AND languages LIKE %s"
                params.append(f"%{languages}%")
            if directors:
                query += " AND directors LIKE %s"
                params.append(f"%{directors}%")
            if cast:
                query += " AND cast LIKE %s"
                params.append(f"%{cast}%")
            if runtime and operator_runtime:
                query += f" AND runtime {operator_runtime} %s"
                params.append(runtime)

            cursor.execute(query, params)
            results = cursor.fetchall()

            log_text = create_log("filter+additional", genre, year, operator_year, keyword_title, keyword_plot,
                                  directors, cast, languages, runtime, operator_runtime)
            insert_query(connect_to_database(db_log_config.db_config), "filter+additional", log_text)

            if results:
                print("\n====== 🎉 Great! The movie list is shown above. ======\n")
                print_results(results)
                choose_movie(results)
            else:
                print("\n🚫 No results found.")

        else:
            # Лог если пользователь не выбрал доп фильтры
            log_text = create_log("filter", genre, year, operator_year, keyword_title, keyword_plot)
            insert_query(connect_to_database(db_log_config.db_config), "filter", log_text)

            choose_movie(results)

    elif choice in ["2", "3", "4", "5", "6"]:
        query_types = {
            "2": ("top5", "ORDER BY `imdb.rating` DESC LIMIT 5"),
            "3": ("oscar_winners", "WHERE `awards.text` LIKE '%Won%' AND `awards.text` LIKE '%Oscar%' ORDER BY `imdb.rating` DESC LIMIT 10"),
            "4": ("oscar_nominees", "WHERE `awards.text` LIKE '%Nominated%' AND `awards.text` LIKE '%Oscar%' ORDER BY `imdb.rating` DESC LIMIT 10"),
            "5": ("long_movies", "ORDER BY runtime DESC LIMIT 10"),
            "6": ("underrated_movies", "ORDER BY `imdb.rating` ASC LIMIT 10")
        }
        type_log, where_clause = query_types[choice]
        query = f"SELECT title, year, genres, `imdb.rating`, runtime, plot, directors, cast FROM movies {where_clause}"
        cursor.execute(query)
        results = cursor.fetchall()
        if results:
            print("\n========== 🎉 Great! The movie list is shown above. ==========\n")
            print_results(results)
            log_text = create_log(type_log)
            insert_query(connect_to_database(db_log_config.db_config), type_log, log_text)
            choose_movie(results)
        else:
            print("\n🚫 No results found.")

    connection.close()
