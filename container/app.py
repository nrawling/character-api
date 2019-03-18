# loosely based on  https://codeburst.io/this-is-how-easy-it-is-to-create-a-rest-api-8a25122ab1f3

import os
from flask import Flask
from flask_restful import Api, Resource, reqparse
from flaskext.mysql import MySQL

app = Flask(__name__)
api = Api(app)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = os.environ.get('MYSQL_DATABASE_USER', "character_demo")
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ.get('MYSQL_DATABASE_PASSWORD', "")
app.config['MYSQL_DATABASE_DB'] = os.environ.get('MYSQL_DATABASE_DB', "monkeydb")
app.config['MYSQL_DATABASE_HOST'] = os.environ.get('MYSQL_DATABASE_HOST', "monkeysql.c6q7nlvddbkw.us-east-1.rds.amazonaws.com")

mysql = MySQL()
mysql.init_app(app)

class Character(Resource):
	def get(self, name):
		try:
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute("SELECT * FROM characters WHERE character_name = '{}'".format(name))
			data = cursor.fetchone()
			return data, 200
		except:
			return "Character not found", 404

	def post(self, name):
		parser = reqparse.RequestParser()
		parser.add_argument("race")
		parser.add_argument("class")
		parser.add_argument("level")
		args = parser.parse_args()

		try:
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute("SELECT * FROM characters WHERE character_name = '{}'".format(name))
			data = cursor.fetchall()
			if len(data) > 0:
				return data, 200
		except:
			return "Unable to connect to database!", 404

		try:
			conn = mysql.connect()
			cursor = conn.cursor()

			cursor.execute("INSERT INTO characters (character_name,character_race,character_class,character_level) VALUES ('{}','{}','{}',{})".format(name,args["race"],args["class"],int(args["level"])))
			conn.commit()

			cursor.execute("SELECT * FROM characters WHERE character_name = '{}'".format(name))
			data = cursor.fetchone()
			return data, 201
		except:
			return "Unable to INSERT new character!", 404

	def put(self, name):
		parser = reqparse.RequestParser()
		parser.add_argument("race")
		parser.add_argument("class")
		parser.add_argument("level")
		args = parser.parse_args()

		try:
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute("SELECT * FROM characters WHERE character_name = '{}'".format(name))
			data = cursor.fetchall()
			if len(data) > 0:
				cursor.execute("UPDATE characters SET character_race = '{}', character_class = '{}', character_level = {} WHERE character_name = '{}'".format(args["race"],args["class"],args["level"],name))
				conn.commit()

				cursor.execute("SELECT * FROM characters WHERE character_name = '{}'".format(name))
				data = cursor.fetchall()

				return data, 200
		except:
			return "Unable to connect to database!", 404

		try:
			conn = mysql.connect()
			cursor = conn.cursor()

			cursor.execute("INSERT INTO characters (character_name,character_race,character_class,character_level) VALUES ('{}','{}','{}',{})".format(name,args["race"],args["class"],int(args["level"])))
			conn.commit()

			cursor.execute("SELECT * FROM characters WHERE character_name = '{}'".format(name))
			data = cursor.fetchone()
			return data, 201
		except:
			return "Unable to INSERT new character!", 404


	def delete(self, name):

		try:
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute("SELECT * FROM characters WHERE character_name = %s",name)
			data = cursor.fetchall()
			if len(data) > 0:
				cursor.execute("DELETE FROM characters WHERE character_name = '{}'".format(name))
				conn.commit()
				return "{} is deleted.".format(name), 200

		except:
			return "{} not found.".format(name),404


api.add_resource(Character, "/character/<string:name>")

app.run(host='0.0.0.0', debug=True)
