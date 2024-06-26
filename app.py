from flask import Flask, render_template, session, request, redirect
from cs50 import SQL
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, apology

app = Flask(__name__, template_folder='static//templates')

@app.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Expires'] = 0
    response.headers['Pragma'] = 'no-cache'
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config['SESSION_FILE_DIR'] = mkdtemp()
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/')
# @login_required
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''Log user in'''

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == 'POST':

        # Ensure username was submitted
        if not request.form.get('username'):
            return apology('must provide username', 403)

        # Ensure password was submitted
        elif not request.form.get('password'):
            return apology('must provide password', 403)

        # Query database for username
        rows = db.execute('SELECT * FROM users WHERE username = ?', request.form.get('username'))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]['hash'], request.form.get('password')):
            return apology('invalid username and/or password', 403)

        # Remember which user has logged in
        session['user_id'] = rows[0]['id']

        # Redirect user to home page
        return redirect('/')

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    '''Register user'''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')

        if not username:
            return render_template('apology.html', top=403, bottom='missing-username'), 400
        if len(db.execute('SELECT * FROM users WHERE username=?', username)) > 0:
            return render_template('apology.html', top=403, bottom='username-already-exists'), 400
        
        if not password or not confirmation:
            return render_template('apology.html', top=403, bottom='missing-password'), 400
        if not password == confirmation:
            return render_template('apology.html', top=403, bottom='passwords-don\'t-match'), 400

        db.execute(
            'INSERT INTO users (username, hash) VALUES (?, ?)',
            username,
            generate_password_hash(password)
        )

        session['user_id'] = db.execute('SELECT id FROM users WHERE username=?', username)[0]['id']
        return redirect('/')
    else:
        return render_template('register.html')

@app.route('/logout')
def logout():
    '''Log user out'''

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect('/')

@app.route('/explore')
def explore():
    '''Explore all courses'''

    courses = db.execute('SELECT * FROM courses')
    return render_template('explore.html', courses=courses)


db = SQL('sqlite:///illuminate.db')

if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0', debug=True)
