import code
import mysql.connector

class Database:

	def __init__(self):
		try:
			self.db = mysql.connector.connect(
				host="localhost",
				user="root",
				password="GojoSatoru2022!",
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
		query = f'SELECT country_name FROM film_has_country WHERE film_has_country.film_id = \'{filmId}\''
		self.cursor.execute(query)
		return self.cursor.fetchall()

	def getFilmCategories(self, filmId):
		query = f'SELECT category_name FROM film_has_category WHERE film_has_category.film_id = \'{filmId}\''
		self.cursor.execute(query)
		return self.cursor.fetchall()

	def getFilmDirectors(self, filmId):
		query = f'SELECT director_name FROM film_has_director WHERE film_has_director.film_id = \'{filmId}\''
		self.cursor.execute(query)
		return self.cursor.fetchall()

	def addUser(self, login, password):
		query = f'INSERT INTO user(login, password) VALUES (\'{login}\', \'{password}\')'
		self.cursor.execute(query)
		self.db.commit()

	def findUser(self, login, password):
		query = f'SELECT login FROM user WHERE login = \'{login}\' AND password = \'{password}\''
		self.cursor.execute(query)
		return len(self.cursor.fetchall()) != 0

	def addFilm(self, title, year, rate, countries, categories, directors):
		query = f'INSERT INTO film(title, year, rate) VALUES (\'{title}\', {year}, {rate})'
		self.cursor.execute(query)
		self.db.commit()
		filmId = self.cursor.lastrowid

		for countryName in countries: 
			self.addFilmHasCountry(filmId, countryName)

		for categoryName in categories: 
			self.addFilmHasCategory(filmId, categoryName)
		
		for directorName in directors:
			self.addFilmHasDirector(filmId, directorName)
	
	def addFilmHasCountry(self, filmId, countryName):
		# insert new country if not exists
		query = f'SELECT name FROM country WHERE name = \'{countryName}\''
		self.cursor.execute(query)		
		if len(self.cursor.fetchall()) == 0:
			query = f'INSERT INTO country(name) VALUES(\'{countryName}\')'
			self.cursor.execute(query)			

		# add new film has country
		query = f'INSERT INTO film_has_country(film_id, country_name) VALUES({filmId}, \'{countryName}\')'
		self.cursor.execute(query)
		self.db.commit()

	def addFilmHasCategory(self, filmId, categoryName):
		# insert new category if not exists
		query = f'SELECT name FROM category WHERE name = \'{categoryName}\''
		self.cursor.execute(query)		
		if len(self.cursor.fetchall()) == 0:
			query = f'INSERT INTO category(name) VALUES(\'{categoryName}\')'
			self.cursor.execute(query)			

		# add new film has category
		query = f'INSERT INTO film_has_category(film_id, category_name) VALUES({filmId}, \'{categoryName}\')'
		self.cursor.execute(query)
		self.db.commit()

	def addFilmHasDirector(self, filmId, directorName):
		# insert new director if not exists
		query = f'SELECT name FROM director WHERE name = \'{directorName}\''
		self.cursor.execute(query)		
		if len(self.cursor.fetchall()) == 0:
			query = f'INSERT INTO director(name) VALUES(\'{directorName}\')'
			self.cursor.execute(query)			

		# add new film has category
		query = f'INSERT INTO film_has_director(film_id, director_name) VALUES({filmId}, \'{directorName}\')'
		self.cursor.execute(query)
		self.db.commit()

	def removeFilm(self, filmId):
		pass

	def findAny(self, target):
		query = f'SELECT id, title, year, rate FROM film WHERE title = \'{target}\' OR year = \'{target}\''
		self.cursor.execute(query)
		result = self.cursor.fetchall()

		query = f'SELECT id, title, year, rate FROM film, film_has_country WHERE film_has_country.film_id = film.id AND film_has_country.country_name = \'{target}\''
		self.cursor.execute(query)
		result += self.cursor.fetchall()

		query = f'SELECT id, title, year, rate FROM film, film_has_category WHERE film_has_category.film_id = film.id AND film_has_category.category_name = \'{target}\''
		self.cursor.execute(query)
		result += self.cursor.fetchall()

		query = f'SELECT id, title, year, rate FROM film, film_has_director WHERE film_has_director.film_id = film.id AND film_has_director.director_name = \'{target}\''
		self.cursor.execute(query)
		result += self.cursor.fetchall()		

		return result

	def isSubscriber(self, login):
		query = f'SELECT * FROM user WHERE login = \'{login}\' AND subscription_id IS NOT NULL'
		self.cursor.execute(query)
		return len(self.cursor.fetchall()) != 0

	def close(self):
		self.db.close()
