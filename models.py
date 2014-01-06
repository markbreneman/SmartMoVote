# mongoengine database module
from mongoengine import *
from flask.ext.mongoengine.wtf import model_form
from flask.ext.wtf import Form

# from wtforms.fields import * # for our custom signup form
from wtforms import TextField, TextAreaField, HiddenField, DateTimeField, SelectField, IntegerField
# /from flask_wtf import Form, TextField, TextAreaField, HiddenField, DateTimeField, required, SelectField, IntegerField

from datetime import datetime
import logging

class Comment(EmbeddedDocument):
	name = StringField()
	comment = StringField()
	timestamp = DateTimeField(default=datetime.now())
	
class Idea(Document):

	creator = StringField(max_length=120, required=True, verbose_name="First name")
	title = StringField(max_length=120, required=True)
	slug = StringField()
	idea = StringField(required=True, verbose_name="What is your idea?")	

	# Category is a list of Strings
	categories = ListField(StringField(max_length=30))

	# Comments is a list of Document type 'Comments' defined above
	comments = ListField( EmbeddedDocumentField(Comment) )

	# Timestamp will record the date and time idea was created.
	timestamp = DateTimeField(default=datetime.now())

class Candidate(Document):

	name = StringField(max_length=120, required=True, verbose_name="First name")
	comments = ListField( EmbeddedDocumentField(Comment) )
	# Timestamp will record the date and time idea was created.
	timestamp = DateTimeField(default=datetime.now())

class Vote(Form):
	name = StringField(max_length=120, required=True, verbose_name="First name")

	bestoverall = SelectField(u'BestOverall', choices=[('Select a Candidate','Select a Candidate'),('Alex Wastney','Alex Wastney'),('Alistair Davies','Alistair Davies'),('Andrew McIntyre','Andrew McIntyre'),('Anthony Torris','Anthony Torris'),('Charlie Paradise','Charlie Paradise'),('Damian Wisniewski','Damian Wisniewski'),('Dave Werzinger','Dave Werzinger'),('Joey Zeledon','Joey Zeledon'),('John Traub','John Traub'),('Marie Bachoc','Marie Bachoc'),('Nathan Brouillet','Nathan Brouillet'),('Phillip Hartley','Phillip Hartley'),('Richard WhiteHall','Richard WhiteHall'),('Russell Blanchard','Russell Blanchard'),('Simone Capano','Simone Capano'),('Tony Mallier','Tony Mallier')],default='Select a Candidate')
	arrestable = SelectField(u'Arrestable', choices=[('Select a Candidate','Select a Candidate'),('Alex Wastney','Alex Wastney'),('Alistair Davies','Alistair Davies'),('Andrew McIntyre','Andrew McIntyre'),('Anthony Torris','Anthony Torris'),('Charlie Paradise','Charlie Paradise'),('Damian Wisniewski','Damian Wisniewski'),('Dave Werzinger','Dave Werzinger'),('Joey Zeledon','Joey Zeledon'),('John Traub','John Traub'),('Marie Bachoc','Marie Bachoc'),('Nathan Brouillet','Nathan Brouillet'),('Phillip Hartley','Phillip Hartley'),('Richard WhiteHall','Richard WhiteHall'),('Russell Blanchard','Russell Blanchard'),('Simone Capano','Simone Capano'),('Tony Mallier','Tony Mallier')])
	transformation = SelectField(u'Transformation', choices=[('Select a Candidate','Select a Candidate'),('Alex Wastney','Alex Wastney'),('Alistair Davies','Alistair Davies'),('Andrew McIntyre','Andrew McIntyre'),('Anthony Torris','Anthony Torris'),('Charlie Paradise','Charlie Paradise'),('Damian Wisniewski','Damian Wisniewski'),('Dave Werzinger','Dave Werzinger'),('Joey Zeledon','Joey Zeledon'),('John Traub','John Traub'),('Marie Bachoc','Marie Bachoc'),('Nathan Brouillet','Nathan Brouillet'),('Phillip Hartley','Phillip Hartley'),('Richard WhiteHall','Richard WhiteHall'),('Russell Blanchard','Russell Blanchard'),('Simone Capano','Simone Capano'),('Tony Mallier','Tony Mallier')])
	keepit = SelectField(u'Keepit', choices=[('Select a Candidate','Select a Candidate'),('Alex Wastney','Alex Wastney'),('Alistair Davies','Alistair Davies'),('Andrew McIntyre','Andrew McIntyre'),('Anthony Torris','Anthony Torris'),('Charlie Paradise','Charlie Paradise'),('Damian Wisniewski','Damian Wisniewski'),('Dave Werzinger','Dave Werzinger'),('Joey Zeledon','Joey Zeledon'),('John Traub','John Traub'),('Marie Bachoc','Marie Bachoc'),('Nathan Brouillet','Nathan Brouillet'),('Phillip Hartley','Phillip Hartley'),('Richard WhiteHall','Richard WhiteHall'),('Russell Blanchard','Russell Blanchard'),('Simone Capano','Simone Capano'),('Tony Mallier','Tony Mallier')])

	# Timestamp will record the date and time idea was created.
	timestamp = DateTimeField(default=datetime.now())

class VoteCasted(Document):

	bestoverall = StringField(required=True, verbose_name="What is your idea?")	
	arrestable = StringField(required=True, verbose_name="What is your idea?")	
	transformation = StringField(required=True, verbose_name="What is your idea?")	
	keepit = StringField(required=True, verbose_name="What is your idea?")	

	# Timestamp will record the date and time idea was created.
	timestamp = DateTimeField(default=datetime.now())

# Create a Validation Form from the Idea model
IdeaForm = model_form(Idea)
CandidateForm = model_form(Candidate)
# VoteForm = model_form(Vote)









