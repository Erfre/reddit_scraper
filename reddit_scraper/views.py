from database_manager import db_manager
from flask import Flask, g, render_template, request, url_for, redirect, flash
from json_loader import get_settings
import sys

subreddits, db_path = get_settings()
db_m = db_manager(db_path)

app = Flask(__name__)
app.secret_key = ""
app.config.from_object(__name__)
app.config.update(DATABASE=db_path)



@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        db_m.close_conn()

@app.route('/')
def landing():
    return render_template('index.html', tables=subreddits)

@app.route('/<subreddit>', methods=['GET', 'POST'])
def show_entries(subreddit):
    get_db(subreddit)
    while True:
        try:
            if request.method == 'GET':
                rand_row = db_m.get_random_row(0)
                db_m.row = rand_row
                img_src = str(rand_row[1]) + '0.jpg'
                title = rand_row[2]
                user = rand_row[3]
                descritpion = title + '\n\nCredit:/u/' + user
                return render_template('subtemp.html', img=img_src, desc=descritpion)
            elif request.method == 'POST':
                if request.form['action'] == 'Save':
                    desc = format(request.form['text'])
                    db_m.update_desc(desc)
                elif request.form['action'] == 'Delete':
                    db_m.delete_row()
                elif request.form['action'] == 'Home':
                    return redirect(url_for('landing'))
                return redirect(url_for('show_entries', subreddit=subreddit))
        except (KeyboardInterrupt, SystemExit):
            raise
        except TypeError:
            # show error message
            flash('Table is empty.')
            return redirect(url_for('landing'))
        except:
            print('not working.', sys.exc_info()[0])
            continue

def get_db(sub):
    """Opens a new database connection if there is
    none yet for the current application context.
    And counts total number of rows in database"""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = db_m.create_connect()
        db_m.table = sub
        db_m.count_row()
    return g.sqlite_db
