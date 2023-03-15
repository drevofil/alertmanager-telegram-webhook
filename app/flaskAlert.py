import json
import requests
import logging
import os

from dateutil import parser
from flask import Flask
from flask import request
from flask_basicauth import BasicAuth


chatid = os.environ['chatid']
username =  os.environ['username']
password =  os.environ['password']
botToken =  os.environ['bot_token']
group_chat_id = "-"+chatid

app = Flask(__name__)
basic_auth = BasicAuth(app)

app.config['BASIC_AUTH_FORCE'] = True
app.config['BASIC_AUTH_USERNAME'] = username
app.config['BASIC_AUTH_PASSWORD'] = password

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

@app.route('/alert', methods = ['POST'])
def postAlertmanager():
    content = json.loads(request.get_data())
    channel = request.args.get("channel")
    app.logger.debug("Channel to send: %s",str(channel))
    fullmessage = ""
    for alert in content['alerts']:
        if alert['status'] == "resolved":
            message = "\U00002705 Resolved"+"\n"+"\n"
        elif alert['status'] == "firing":
            message = "\U0000274c Firing"+"\n"+"\n"
        if 'alertname' in alert['labels']:
            message += "Alert name: "+alert['labels']['alertname']+"\n"+"\n"
        #
        if 'labels' in alert:
            labels = alert['labels']
            message += "Labels:"+"\n"
            for key, value in labels.items():
                message += "- "+ key +" : " + value +"\n"
        else :
            message += "\n"+"No Labels"+"\n"
        #
        if 'annotations' in alert:
            annotations = alert['annotations']
            message += "\n"+"Annotations:"+"\n"
            for key, value in annotations.items():
                message += "- "+ key +" : " + value +"\n"
        else:
            message += "\n"+"No annotations"+"\n"
        if alert['status'] == "resolved":
            correctDate = parser.parse(alert['endsAt']).strftime('%Y-%m-%d %H:%M:%S')
            message += "\n"+"\U0000231A Resolved: "+correctDate+"\n"+"\n"
        elif alert['status'] == "firing":
            correctDate = parser.parse(alert['startsAt']).strftime('%Y-%m-%d %H:%M:%S')
            message += "\n"+"\U0000231A Started: "+correctDate+"\n"+"\n"
        fullmessage += message
    url = f"https://api.telegram.org/bot{botToken}/sendMessage?chat_id={group_chat_id}&reply_to_message_id={channel}&text={fullmessage}"
    app.logger.debug(alert)
    app.logger.debug(url)
    requests.post(url)
    app.logger.info("Message sent")
    app.logger.debug("Message sent: %s",str(content))
    return "Alert OK", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9119)
