"""The main file."""
from views import *
from database_manager import db_manager
from img_download import img_url_handler
from json_loader import get_reddit
from json_loader import get_settings
from sub_scrape import sub_scrape
from pathlib import Path
from datetime import date
from calendar import monthrange
from time import sleep
from _thread import start_new_thread
import schedule


reddit_account = get_reddit()

def get_posts(db, subreddit, time_filter):
    img_path = 'static/images/' + subreddit + '/'
    scraper = sub_scrape(subreddit, reddit_account)
    print("Started\n Getting top posts from {} {}...\n".format(time_filter, subreddit))
    img_handler = img_url_handler(subreddit, img_path)
    scraper.get_posts(time_filter, db, img_handler)
    print('Time for next subreddit \n\n')
    return


def daily_run(db):
    """
    Connects to the database, creates a table for each subreddit
    and checks if its empty.
    """
    for each in subreddits:
        db.create_connect()
        db.create_table( each)
        db.table = each
        rows = db.is_empty()
        if rows == 0:
            get_posts(db, each, 'all')
        else:
            date_check(db, each)
        db.close_conn()
    return

def date_check(db, subreddit):
    today = date.today()
    days_in_month = monthrange(today.year, today.month)[1]
    if str(today.day) == '1':
        get_posts(db, subreddit, 'month')
    else:
        print('Time left till next reddit scrape: ', days_in_month - today.day)
    return

def flaskThread():
        app.run(host='0.0.0.0', use_reloader=False, debug=False, threaded=True)

start_new_thread(flaskThread, ())
schedule.every().day.at('12:00').do(daily_run, db_m)

while True:
    schedule.run_pending()
    sleep(1)
