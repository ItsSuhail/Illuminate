from flask import Flask, render_template, session
from cs50 import SQL
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__, template_folder='static//templates')

@app.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Expires'] = 0
    response.headers['Pragma'] = 'no-cache'
    return response

@app.route("/")
def index():
    return render_template('index.html')

# Configure session to use filesystem (instead of signed cookies)
app.config['SESSION_FILE_DIR'] = mkdtemp()
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

db = SQL('sqlite:///illuminate.db')

if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0', debug=True)
