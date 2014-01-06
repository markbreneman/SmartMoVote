import os, datetime
import re
from flask import Flask, request, render_template, redirect, abort, flash, json

from unidecode import unidecode



# mongoengine database module
from flask.ext.mongoengine import MongoEngine


app = Flask(__name__)   # create our flask app
app.config['CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')



# --------- Database Connection ---------
# MongoDB connection to MongoLab's database
app.config['MONGODB_SETTINGS'] = {'HOST':os.environ.get('MONGOLAB_URI'),'DB': 'dwdfall2013'}
app.logger.debug("Connecting to MongoLabs")
db = MongoEngine(app) # connect MongoEngine with Flask App

# import data models
import models

from models import Vote


# --------- Routes ----------
# this is our main page
@app.route("/", methods=['GET','POST'])
def index():
	vote_form = Vote(request.form)

	templateData = {
			'form' : vote_form
		}
		
	app.logger.debug(vote_form)

	return render_template("vote.html", **templateData)

# this is our main page
@app.route('/voted',methods=['GET','POST'])
def voted():

	vote_form = Vote(request.form)

	# if form was submitted and it is valid...
	if request.method == "POST" and vote_form.validate():
	
		# get form data - create new idea
		vote = models.Vote()
		vote.bestoverall = request.form.get('bestoverall')
		vote.transformation = request.form.get('transformation')
		vote.arrestable = request.form.get('arrestable')
		vote.keepit = request.form.get('keepit')		

		VoteCasted=models.VoteCasted()
		VoteCasted.bestoverall=vote.bestoverall
		VoteCasted.transformation=vote.transformation
		VoteCasted.arrestable=vote.arrestable
		VoteCasted.keepit=vote.keepit
		VoteCasted.save()	
		
		# app.logger.debug(templateData)

		return render_template("voted.html")

	else:

		templateData = {
			'form' : vote_form
		}
		
	return render_template("voted.html", **templateData)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404



# --------- Server On ----------
# start the webserver
if __name__ == "__main__":
	app.debug = True
	
	port = int(os.environ.get('PORT', 5000)) # locally PORT 5000, Heroku will assign its own port
	app.run(host='0.0.0.0', port=port)
	# app.run(host='127.0.0.1', port=port)



	