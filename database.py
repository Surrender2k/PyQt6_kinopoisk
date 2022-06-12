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
		filmId = self.cursor.lasrrowid

		for countryName in countries: 
			self.addFilmHasCountry(filmId, countryName)

		for categoryName in categories: 
			self.addFilmHasCountry(filmId, categoryName)
		
		for directorName in directors: 
			self.addFilmHasCountry(filmId, directorName)
		
		self.db.commit()

	def addFilmHasCountry(self, filmId, countryName):
		pass

	def addFilmHasCategory(self, filmId, categoryName):
		pass

	def addFilmHasDirector(self, filmId, directorName):
		pass

	def close(self):
		self.db.close()
