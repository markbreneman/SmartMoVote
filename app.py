import os, datetime
import re
from flask import Flask, request, render_template, redirect, abort, flash, json

from unidecode import unidecode



# mongoengine database module
from flask.ext.mongoengine import MongoEngine


app = Flask(__name__)   # create our flask app
# app.config['CSRF_ENABLED'] = True
# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# app.config['SECRET_KEY'] = 1234567


# --------- Database Connection ---------
# MongoDB connection to MongoLab's database
app.config['MONGODB_SETTINGS'] = {'HOST':os.environ.get('MONGOLAB_URI'),'DB': 'dwdfall2013'}
app.logger.debug("Connecting to MongoLabs")
db = MongoEngine(app) # connect MongoEngine with Flask App

# import data models
import models

from models import Vote

# hardcoded categories for the checkboxes on the form
categories = ["Garbage"]

candidates =["Alex Wastney","Alistair Davies","Andrew McIntyre","Anthony Torris","Charlie Paradise","Damian Wisniewski","Dave Werzinger","Joey Zeledon","John Traub","Marie Bachoc","Nathan Brouillet","Phillip Hartley","Richard WhiteHall","Russell Blanchard","Simone Capano","Tony Mallier"]

#Create Candidates
for s in candidates:
	candidate = models.Candidate()
	candidate.name = s
	candidate.save() # save it

# --------- Routes ----------
# this is our main pagex
@app.route("/", methods=['GET','POST'])
def index():

	idea_form = models.IdeaForm(request.form)

	# if form was submitted and it is valid...
	if request.method == "POST" and idea_form.validate():
	
		# get form data - create new idea
		idea = models.Idea()
		idea.creator = request.form.get('creator','anonymous')
		idea.title = request.form.get('title','no title')
		idea.idea = request.form.get('idea','')
		idea.categories = request.form.getlist('categories') # getlist will pull multiple items 'categories' into a list
		
		idea.save() # save it

		# redirect to the new idea page
		return redirect('/ideas/%s' % idea.slug)

	else:

		# for form management, checkboxes are weird (in wtforms)
		# prepare checklist items for form
		# you'll need to take the form checkboxes submitted
		# and idea_form.categories list needs to be populated.
		if request.method=="POST" and request.form.getlist('categories'):
			for c in request.form.getlist('categories'):
				idea_form.categories.append_entry(c)


		# render the template
		templateData = {
			'ideas' : models.Idea.objects(),
			'categories' : categories,
			'form' : idea_form
		}
		
		# app.logger.debug(templateData)

		return render_template("main.html", **templateData)

# this is our main page
@app.route('/vote')
def vote():

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
		# vote.save() # save it

		VoteCasted=models.VoteCasted()
		VoteCasted.bestoverall=vote.bestoverall
		VoteCasted.transformation=vote.transformation
		VoteCasted.arrestable=vote.arrestable
		VoteCasted.keepit=vote.keepit
		VoteCasted.save()	

		# render the template
		templateData = {
			# 'ideas' : models.Idea.objects(),
		}
		
		# app.logger.debug(templateData)

		return render_template("voted.html", **templateData)

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



	