import jinja2
import os
import webapp2
import logging
import json
import urllib

from google.appengine.api import urlfetch
from google.appengine.ext import ndb

template_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.getcwd())  # Get the templates in current directory
)


class Progress(ndb.Model):
    user = ndb.StringProperty()
    status = ndb.StringProperty()


class MainPage(webapp2.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        # data = json.loads(data)
        # logging.info("The data = " + str(data['challenge']))
        template = template_env.get_template('auth.html')
        channel = data['event']['channel']
        logging.info("The Data Recieved = " + str(data))
        if ('username' not in data['event']):
            channel_type = data['event']['channel_type']
            if(channel_type == "im"):
                im_message(data, channel)
            else:
                global_message(data, channel)

        context = {
            'data': data,
        }
        self.response.out.write(template.render(context))

def im_message(data, channel):
    if (data['event']['type'] == "message"):
        send_data = json.dumps({
            "text": "You seem to have slid into my DMs",
            "channel": channel
        })
        sendJSON(send_data)

def global_message(data, channel):
    if (data['event']['type'] == "app_mention"):
        if (data['event']['text'].find("tell me a joke") != -1):
            logging.info("Recieved Tell me a joke")
            user = data['event']['user']
            user_status_query = Progress.query().filter(Progress.user == user)
            user_status = user_status_query.get()
            if (user_status):
                user_status.status = "Asked"
                user_status.put()
            else:
                progress_details = Progress(user=user, status="Asked")
                progress_details.put()
            send_data = json.dumps({
                "text": "Hello <@" + user + ">! Knock, knock.",
                "channel": channel
            })
            sendJSON(send_data)
        else:
            logging.info("No Tell me a joke there")
            send_data = json.dumps({
                "text": "Owen half completed me :sob: I only know how to respond to you asking for a joke",
                "channel": channel
            })
            sendJSON(send_data)

    if (data['event']['text'].lower().find("who's there?") != -1):
        received_user = data['event']['user']
        q = Progress.query().filter(Progress.status == "Asked")
        for status_result in q:
            if (status_result.user == received_user):
                status_result.status = "who"
                status_result.put()
                send_data = json.dumps({
                    "text": "A Bot user",
                    "channel": channel
                })
                sendJSON(send_data)
    if (data['event']['text'].lower().find("a bot user who?") != -1):
        received_user = data['event']['user']
        q = Progress.query().filter(Progress.status == "who")
        for status_result in q:
            if (status_result.user == received_user):
                send_data = json.dumps({
                    "text": "No. I'm a bot user. I don't understand jokes!",
                    "channel": channel
                })
                sendJSON(send_data)

def sendJSON(send_data):
    try:
        headers = {'Content-type': 'application/json',
                   'Authorization': 'Bearer xoxb-463667519270-463594951317-utgQ8FwmJtludrecTt4h3AJz'}
        result = urlfetch.fetch(
            url='https://slack.com/api/chat.postMessage',
            payload=send_data,
            method=urlfetch.POST,
            headers=headers,
            validate_certificate=1)
        logging.info("Result = " + result.content)
    except urlfetch.Error:
        logging.exception("Caught Exception fetching URL")


application = webapp2.WSGIApplication([('/', MainPage)], debug=True)  # Debug will be false when in production
