from flask import Flask, render_template
import random

app = Flask(__name__)
app.debug = True

@app.route('/')
def diceThrow():
    plr = random.randint(1, 6)
    pc = random.randint(1, 6)
    if (plr > pc):
        result="Výhra!"
    elif (plr < pc):
        result="Prohra!"
    else:
        result="Remíza!"

    return render_template('hra.html', plr=plr, pc=pc, result=result)


@app.route('/stats')
def stats():
    return render_template('graf.html');

if __name__ == '__main__':
    app.run()