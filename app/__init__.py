from flask import Flask
# import schedule

app = Flask(__name__)

from app import routes

import os
print("Mode: " + str(os.environ.get('FLASK_ENV')))

# def job():
#     print("I'm working...")
#
# schedule.every(1).minutes.do(job)
# # schedule.every().day.at("10:30").do(job)
#
# schedule.run_pending()

# import time
# import atexit
#
# from apscheduler.schedulers.background import BackgroundScheduler
#
#
# def print_date_time():
#     print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
#
#
# scheduler = BackgroundScheduler()
# scheduler.add_job(func=print_date_time, trigger="interval", seconds=3)
# # scheduler.start()
#
# # Shut down the scheduler when exiting the app
# atexit.register(lambda: scheduler.shutdown())

