import re
from collections import Counter
from db import connect_to_database
import db_log_config
import tabulate

def insert_query(connection, query_type, log):
    try:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO queries (type, query) VALUES (%s, %s)', (query_type, log))
        connection.commit()
    except Exception as e:
        print(f'Ошибка записи в логи: {str(e)}')
    finally:
        cursor.close()

def create_log(query_type, genre=None, year=None, operator_year=None, keyword_title=None, keyword_plot=None,
               directors=None, cast=None, languages=None, runtime=None, operator_runtime=None):
    log_parts = [f"type:{query_type}"]

    if genre:
        log_parts.append(f"genre:{genre}")
    if year:
        log_parts.append(f"year:{operator_year}{year}" if operator_year else f"year:{year}")
    if keyword_title:
        log_parts.append(f"keyword_title:{keyword_title}")
    if keyword_plot:
        log_parts.append(f"keyword_plot:{keyword_plot}")
    if directors:
        log_parts.append(f"directors:{directors}")
    if cast:
        log_parts.append(f"cast:{cast}")
    if languages:
        log_parts.append(f"languages:{languages}")
    if runtime:
        log_parts.append(f"runtime:{operator_runtime}{runtime}" if operator_runtime else f"runtime:{runtime}")

    return ", ".join(log_parts)

def get_statistics():
    connection = connect_to_database(db_log_config.db_config)
    cursor = connection.cursor()

    print("\n========== 📊 Statistics by request type ==========\n")
    cursor.execute("""
        SELECT type, COUNT(*) AS count
        FROM queries
        GROUP BY type
        ORDER BY count DESC
    """)
    print(tabulate.tabulate(cursor.fetchall(), headers=["Type", "Count"], tablefmt="grid"))

    print("\n========== 🗂️ Most popular queries ==========\n")
    cursor.execute("""
        SELECT query, COUNT(*) AS count
        FROM queries
        GROUP BY query
        ORDER BY count DESC
        LIMIT 10
    """)
    print(tabulate.tabulate(cursor.fetchall(), headers=["Query", "Count"], tablefmt="grid"))

    print("\n========== 🎭 Statistics by genres ==========\n")
    cursor.execute("SELECT query FROM queries WHERE query LIKE '%genre:%'")
    rows = cursor.fetchall()
    genres = []
    for row in rows:
        genres += re.findall(r'genre:([^,]+)', row[0])
    counter = Counter(genres)
    print(tabulate.tabulate(counter.items(), headers=["Genre", "Count"], tablefmt="grid"))

    print("\n========== 📅 Statistics by years ==========\n")
    cursor.execute("""
        SELECT 
        TRIM(REPLACE(REPLACE(REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(query, 'year:', -1), ',', 1), '>', ''), '<', ''), '=', '')) AS year,
        COUNT(*) AS count
        FROM queries
        WHERE query LIKE '%year:%'
        GROUP BY year
        ORDER BY count DESC
    """)
    print(tabulate.tabulate(cursor.fetchall(), headers=["Year", "Count"], tablefmt="grid"))

    print("\n🎬 See you again! Have a nice day and enjoy your future movie nights! 🍿🥤")

    cursor.close()
    connection.close()