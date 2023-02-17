import os
import socketserver
import http.server
import schedule
import time
import threading
import logging
from cvdupdate.cvdupdate import CVDUpdate


WEB_SERVER_PORT = 8081
UPDATE_FREQUENCY_HOURS = 3


def job():
    logging.info("Start update job")
    udater = CVDUpdate(config='', verbose=False)
    errors = udater.db_update()
    if errors > 0:
        logging.error("Update job has errors {}".format(errors))
        pass


def cron():
    job()
    schedule.every(UPDATE_FREQUENCY_HOURS).hours.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    logging.info("Start updater ClamAV databases")
    upd_thread = threading.Thread(target=cron)
    upd_thread.start()

    logging.info("Start web server on port {}".format(WEB_SERVER_PORT))
    try:
        os.chdir('/clamav')
        with socketserver.TCPServer(("", WEB_SERVER_PORT), http.server.SimpleHTTPRequestHandler) as httpd:
            logging.info("Socket created")
            httpd.serve_forever()
    except Exception as e:
        logging.error("Failed start web server %s" % e)


