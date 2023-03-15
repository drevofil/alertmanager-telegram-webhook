import telegram
import json 
# import logging
import asyncio
import os

from telegram.error import RetryAfter, TimedOut, NetworkError
from dateutil import parser
from flask import Flask
from flask import request
from flask_basicauth import BasicAuth

appkey =  os.environ['appkey']
chatid = os.environ['chatid']
username =  os.environ['username']
password =  os.environ['password']
botToken =  os.environ['bot_token']

app = Flask(__name__)
app.secret_key = appkey
basic_auth = BasicAuth(app)

chatID = "-"+chatid


app.config['BASIC_AUTH_FORCE'] = True
app.config['BASIC_AUTH_USERNAME'] = username
app.config['BASIC_AUTH_PASSWORD'] = password

bot = telegram.Bot(token=botToken)

# if __name__ != '__main__':
#     gunicorn_logger = logging.getLogger('gunicorn.error')
#     app.logger.handlers = gunicorn_logger.handlers
#     app.logger.setLevel(gunicorn_logger.level)

@app.route('/alert', methods = ['POST'])
async def postAlertmanager():

    try:
        content = json.loads(request.get_data())
        args = request.args
        if not any(args.values()):
            reply_to=None
        else:
            reply_to=args.get("channel")
        for alert in content['alerts']:
            message = "Status: "+alert['status']+"\n"
            if 'alertname' in alert['labels']:
                message += "Alert name: "+alert['labels']['alertname']+"\n"
            else:
                message += "Instance: "+alert['labels']['instance']+"\n"
            if 'info' in alert['annotations']:
                message += "Info: "+alert['annotations']['info']+"\n"
            if 'summary' in alert['annotations']:
                message += "Summary: "+alert['annotations']['summary']+"\n"
            if 'description' in alert['annotations']:
                message += "Description: "+alert['annotations']['description']+"\n"
            if alert['status'] == "resolved":
                correctDate = parser.parse(alert['endsAt']).strftime('%Y-%m-%d %H:%M:%S')
                message += "Resolved: "+correctDate
            elif alert['status'] == "firing":
                correctDate = parser.parse(alert['startsAt']).strftime('%Y-%m-%d %H:%M:%S')
                message += "Started: "+correctDate
            await bot.sendMessage(chat_id=chatID, text=message, reply_to_message_id=reply_to)
            app.logger.info("Message sent")
            app.logger.debug("Message sent: %s",str(content))
        return "Alert OK", 200
    except RetryAfter:
        await asyncio.sleep(30)
        await bot.sendMessage(chat_id=chatID, text=message)
        app.logger.info("Retrying send: %s",str(content))
        return "Alert OK", 200
    except TimedOut as e:
        await asyncio.sleep(60)
        await bot.sendMessage(chat_id=chatID, text=message)
        app.logger.info("Timeout send: %s",str(content))
        return "Alert OK", 200
    except NetworkError as e:
        await asyncio.sleep(60)
        await bot.sendMessage(chat_id=chatID, text=message)
        app.logger.info("Network error send: %s",str(content))
        return "Alert OK", 200
    except KeyError as e:
        await bot.sendMessage(chat_id=chatID, text="Key error: "+str(error))
        app.logger.info("Key not found in: %s",str(content))
        return "Alert OK", 200
    except Exception as error:
        await bot.sendMessage(chat_id=chatID, text="Error: "+str(error))
        # app.logger.info("\t%s",error)
        app.logger.info("Error send: %s",str(content))
        return "\t%s",error, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9119)
