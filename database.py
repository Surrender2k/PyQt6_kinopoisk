import mysql.connector, datetime

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
		query = f'SELECT * FROM user WHERE login = \'{login}\''
		self.cursor.execute(query)
		isUserFound = len(self.cursor.fetchall()) != 0
		if not isUserFound:
			query = f'INSERT INTO user(login, password) VALUES (\'{login}\', \'{password}\')'
			self.cursor.execute(query)
			self.db.commit()
		return not isUserFound

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

	def deleteFilm(self, filmId):
		query = f'SELECT * FROM film WHERE id = {filmId}'
		self.cursor.execute(query)
		isFound = len(self.cursor.fetchall()) != 0
		if (isFound):
			query = f'DELETE FROM film WHERE id = {filmId}'
			self.cursor.execute(query)
			self.db.commit()
		return isFound

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
		if len(self.cursor.fetchall()) != 0:
			days = self.checkSubscription(login)
			if (days < 1):
				query = f'SELECT subscription_id FROM user WHERE login = \'{login}\''
				self.cursor.execute(query)
				SubId = self.cursor.fetchall()[0][0]
				query = f'UPDATE user SET subscription_id = NULL WHERE login = \'{login}\''
				self.cursor.execute(query)
				self.db.commit()
				query = f'DELETE FROM subscription WHERE id = {SubId}'
				self.cursor.execute(query)
				self.db.commit()
				return False
			else:
				return True
		else: 
			return False

	def addSubscription(self, login, val):
		query = f'SELECT subscription_id FROM user WHERE login = \'{login}\''
		self.cursor.execute(query)
		oldSubId = self.cursor.fetchall()[0][0]
		
		if val == 1:
			validUntil = datetime.date(datetime.date.today().year + 1, datetime.date.today().month, datetime.date.today().day)
		elif val == 2:
			validUntil = datetime.date(datetime.date.today().year, datetime.date.today().month + 6, datetime.date.today().day)		
		elif val == 3:
			validUntil = datetime.date(datetime.date.today().year, datetime.date.today().month + 1, datetime.date.today().day)

		query = f'INSERT INTO subscription(valid_until) VALUES(\'{validUntil}\')'
		self.cursor.execute(query)
		self.db.commit()
		subId = self.cursor.lastrowid
		query = f'UPDATE user SET subscription_id = {subId} WHERE login = \'{login}\''
		self.cursor.execute(query)

		if oldSubId != None:
			query = f'DELETE FROM subscription WHERE id = {oldSubId}'
			self.cursor.execute(query)
			self.db.commit()

		self.db.commit()

	def checkSubscription(self, login):		
		query = f'SELECT valid_until FROM subscription, user WHERE id = subscription_id AND login = \'{login}\''
		self.cursor.execute(query)
		return (self.cursor.fetchall()[0][0] - datetime.date.today()).days

	def findFilm(self, filmId):
		query = f'SELECT * FROM film WHERE id = {filmId}'
		self.cursor.execute(query)
		return len(self.cursor.fetchall()) != 0		

	def addFavourites(self, login, filmId):		
		query = f'INSERT INTO favourites(user_login, film_id) VALUES(\'{login}\', {filmId})'
		self.cursor.execute(query)
		self.db.commit()

	def getFavourites(self, login):
		query = f'SELECT id, title, year, rate FROM film, favourites WHERE user_login = \'{login}\' AND id = film_id'
		self.cursor.execute(query)
		return self.cursor.fetchall()

	def close(self):
		self.db.close()
