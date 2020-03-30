#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, session
from flask_wtf import FlaskForm
from wtforms import RadioField
import sqlite3
from flask_session.__init__ import Session
import os

app = Flask(__name__)
app.debug = False

app.secret_key = 'hdsHjHjadhJK.Jh'

SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

curDir = os.path.abspath(os.path.dirname(__file__))

class AnketaForm(FlaskForm):
	vote = RadioField("Co vám chutná nejvíce", choices=[('beer', 'Pivo'), ('wine', 'Víno'), ('limonade', 'Limo'), ('tea', 'Čaj')])


@app.route('/', methods=['GET', 'POST'])
def vote():
	if not 'voted' in session:
		session['voted'] = False

	form = AnketaForm()
	usersVote = form.vote.data

	if form.validate_on_submit() and not session['voted']:
		session['voted'] = True
		conn = sqlite3.connect(os.path.join(curDir,'statistics.db'))
		c = conn.cursor()
		c.execute(f"UPDATE results set {usersVote} = {usersVote} + 1")
		conn.commit()
		conn.close()
		return redirect('/results')
	elif session['voted']:
		return redirect('/results')
	return render_template('form.html', form=form)

@app.route('/results')
def results():
	conn = sqlite3.connect('statistics.db')
	c = conn.cursor()
	c.execute("select sum(beer), sum(wine), sum(tea), sum(limonade) from results")
	result = c.fetchone()
	conn.close()
	return render_template('graph.html', beer=result[0], wine=result[1], tea=result[2], limonade=result[3])

if __name__ == '__main__':
    app.run()
