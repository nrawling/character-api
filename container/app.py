# loosely based on  https://codeburst.io/this-is-how-easy-it-is-to-create-a-rest-api-8a25122ab1f3

import os
from flask import Flask
from flask_restful import Api, Resource, reqparse
from flaskext.mysql import MySQL

app = Flask(__name__)
api = Api(app)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = os.environ.get('MYSQL_DATABASE_USER', None)
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ.get('MYSQL_DATABASE_PASSWORD', None)
app.config['MYSQL_DATABASE_DB'] = os.environ.get('MYSQL_DATABASE_DB')
app.config['MYSQL_DATABASE_HOST'] = os.environ.get('MYSQL_DATABASE_HOST')

mysql = MySQL()
mysql.init_app(app)

characters = [
	{
		"name": "Gunthar",
		"race": "Dragonborn",
		"class": "Paladin",
		"level": 1
	},
]

class Character(Resource):
	def get(self, name):
		try:
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute("SELECT * FROM characters WHERE character_name = %s",name)
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
			cursor.execute("SELECT * FROM characters WHERE character_name = %s",name) 
			data = cursor.fetchall()
			if len(data) > 0:
				return data, 200
		except:
			"Unable to connect to database!", 404

		try:
			conn = mysql.connect()
			cursor = conn.cursor()

			cursor.execute("INSERT INTO characters (character_name,character_race,character_class,character_level) VALUES ('{}','{}','{}',{})".format(name,args["race"],args["class"],int(args["level"])))

			cursor = conn.cursor()
			cursor.execute("SELECT * FROM characters WHERE character_name = %s",name)
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

		for character in characters:
			if(name == character["name"]):
				character["race"] = args["race"]
				character["class"] = args["class"]
				character["level"] = args["level"]
				return character, 200

		character = {
			"name": name,
			"race": args["race"],
			"class": args["class"],
			"level": args["level"]
		}
		characters.append(character)
		return character, 201

	def delete(self, name):
		global characters
		characters = [character for character in characters if character["name"] != name]
		return "{} is deleted.".format(name), 200

api.add_resource(Character, "/character/<string:name>")

app.run(debug=True)
