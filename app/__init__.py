from flask import Flask
# import schedule

app = Flask(__name__)

from app import routes

import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler

# __name__
logger = logging.getLogger()

# TODO: replace the all-zero GUID with your instrumentation key.
logger.addHandler(AzureLogHandler(
    connection_string='InstrumentationKey=7b71d952-0a78-41de-a29d-f1d8737f634e')
)

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

