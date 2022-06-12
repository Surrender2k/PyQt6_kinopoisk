import mysql.connector

class Database:

    def __init__(self):
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="password",
                database="filmoteka"
            )
            self.cursor = self.db.cursor() 
        except Exception as ex:
            print('Failed when tried to connect to database')
            print(ex)     
          
    def getAllFilms(self):
        query = 'SELECT * FROM film'   
        self.cursor.execute(query)                 
        return self.cursor.fetchall()

    def getFilmCountries(self, filmId):    
        query = f'SELECT country_name FROM film_has_country, film WHERE film.id = film_has_country.film_id AND film.id = \'{filmId}\''        
        self.cursor.execute(query)     
        return self.cursor.fetchall()

    def getFilmCategories(self, filmId):    
        query = f'SELECT category_name FROM film_has_category, film WHERE film.id = film_has_category.film_id AND film.id = \'{filmId}\''       
        self.cursor.execute(query)     
        return self.cursor.fetchall()

    def getFilmDirectors(self, filmId):    
        query = f'SELECT director_name FROM film_has_director, film WHERE film.id = film_has_director.film_id AND film.id = \'{filmId}\''       
        self.cursor.execute(query)     
        return self.cursor.fetchall()

    def close(self):
        self.db.close()
