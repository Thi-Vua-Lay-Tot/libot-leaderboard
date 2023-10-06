from flask import Flask, send_file

app = Flask(__name__)

TYPES = [
    'bullet',
    'blitz',
    'rapid',
    'classical',
    'correspondence',
    'antichess',
    'atomic',
    'chess960',
    'crazyhouse',
    'horde',
    'kingOfTheHill',
    'racingKings',
    'threeCheck'
]

@app.route('/')
@app.route('/home')
def welcome_page():
    return send_file('html/Home.html')

@app.route('/lichess')
def lichess():
    return send_file('html/lichess.html')

@app.route('/lichess/<type_name>')
def lichess_type(type_name):
    if type_name in TYPES:
        return send_file(f'./{type_name}.html')
    else:
        return "Invalid type", 404
        
@app.route('/lichess')
def lishogi():
    return send_file('html/lishogi.html')

@app.route('/lishogi')
def playstrategy():
    return send_file('html/playstrategy.html')

@app.route('/lichess')
def lidraughts():
    return send_file('html/lidraughts.html')

if __name__ == "__main__":
    app.run(host="localhost", port=5000)
