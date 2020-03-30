#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, length
from wtforms import TextAreaField
from flask_session.__init__ import Session
from datetime import date, timedelta

import sqlite3
import os
import logging

app = Flask(__name__)
app.debug = True
app.secret_key = 'xkHslGePyeA'
SESSION_TYPE = 'filesystem'

app.config.from_object(__name__)
Session(app)

curDir = os.path.abspath(os.path.dirname(__file__))
logging.basicConfig(level=logging.DEBUG)

class noteForm(FlaskForm):
	note = TextAreaField('Poznámka', validators=[DataRequired(), length(max=250)])


def getFormatedTime(year, month, day, hour, minute):
	if(int(hour) < 23):
		hour = str(int(hour) + 1)
	else:
		day = str(int(day) + 1)
		hour = "0"
	noteDate = year + "-" + month + "-" + day
	if(str(date.today() - timedelta(hours=1, minutes=0)) == noteDate):
		timeStr = hour + ":" + minute
	else:	
		months = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]
		timeStr = year + " " + day.lstrip("0") + " " + months[int(month)-1]
	return timeStr



@app.route('/poznamka/vlozit', methods=['GET', 'POST'])
def addNote():
	"""Zobrazí folrmulář a vloží poznámku."""
	form = noteForm()
	noteText = form.note.data
	app.logger.info(noteText)
	if form.validate_on_submit():
		conn = sqlite3.connect(os.path.join(curDir,'notes.db'))
		c = conn.cursor()
		c.execute("INSERT INTO note(body) VALUES (?)", (noteText,))
		conn.commit()
		conn.close()
		return redirect('/')
	return render_template('addNote.html', form=form)

@app.route('/')
def showNotes():
	"""Zobrazí všechny poznamky."""
	conn = sqlite3.connect(os.path.join(curDir,'notes.db'))
	c = conn.cursor()
	notesDB = c.execute("SELECT rowid, body, kdy FROM note ORDER BY kdy DESC").fetchall()
	notes = [list(i) for i in notesDB]

	for i in range(len(notes)):
		notes[i][1] = notes[i][1].replace('\r\n', '<br>')
		date = notes[i][2][:-3].replace(" ", "-").replace(":", "-").split("-")
		notes[i][2] = getFormatedTime(date[0], date[1], date[2], date[3], date[4])

	conn.close()
	return render_template('showNotes.html', notes=notes)




@app.route('/del/<int:noteID>')
def deleteNote(noteID):
	"""Smaže vybranou poznámku"""
	conn = sqlite3.connect(os.path.join(curDir,'notes.db'))
	c = conn.cursor()
	c.execute("DELETE FROM note WHERE rowid=?", (noteID,))
	conn.commit()
	conn.close()
	return redirect('/')

@app.route('/poznamka/upravit/<int:noteID>', methods=['GET', 'POST'])
def editNote(noteID):
	"""Upravý vybranou poznámku"""
	form = noteForm()
	noteText = form.note.data



	conn = sqlite3.connect(os.path.join(curDir,'notes.db'))
	c = conn.cursor()	
	note = c.execute("SELECT body FROM note WHERE rowid=?", (noteID,)).fetchone()
	conn.commit()
	conn.close()
	form.note.data = list(note)[0]

	if form.validate_on_submit():
		conn = sqlite3.connect(os.path.join(curDir,'notes.db'))
		c = conn.cursor()
		c.execute("UPDATE note set body = (?) where rowid=?", (noteText,noteID))
		conn.commit()
		conn.close()
		return redirect('/')
	return render_template('editNote.html', form=form, noteID=noteID)

if __name__ == '__main__':
	app.run()



