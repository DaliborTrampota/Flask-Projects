from flask import Flask, render_template
from random import choice

app = Flask(__name__)
app.debug = True

def getRPS():
    return choice(["rock", "scissors", "paper"])

def getWinner(player, pc):
    if player == pc:
        return "Remíza"
    if player == "stone" and pc == "scissors":
        return "Výhra"
    if player == "scissors" and pc == "paper":
        return "Výhra"
    if player == "paper" and pc == "rock":
        return "Výhra"
    return "Prohra"

@app.route('/')
def pcTurn():
    return render_template("index.html", choice=getRPS())


@app.route('/stone')
def stone():
    pc = getRPS()
    winner = getWinner("stone", pc)
    return render_template("game.html", pc=pc, player="rock", winner=winner)

@app.route('/paper')
def paper():
    pc = getRPS()
    winner = getWinner("paper", pc)
    return render_template("game.html", pc=pc, player="paper", winner=winner)

@app.route('/scissors')
def scissors():
    pc = getRPS()
    winner = getWinner("scissors", pc)
    return render_template("game.html", pc=pc, player="scissors", winner=winner)


if __name__ == '__main__':
    app.run()



