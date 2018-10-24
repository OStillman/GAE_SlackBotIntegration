import jinja2
import os
import webapp2
import logging
import json
import urllib

from google.appengine.api import urlfetch

template_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.getcwd())  # Get the templates in current directory
)


class MainPage(webapp2.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        # data = json.loads(data)
        # logging.info("The data = " + str(data['challenge']))
        template = template_env.get_template('auth.html')
        if (data['event']['type'] == "app_mention"):
            if (data['event']['text'].find("tell me a joke") != -1):
                logging.info("Recieved Tell me a joke")
                send_data = json.dumps({
                    "text": "Hello! Knock, knock.",
                    "channel": "CDMKMFHHU"
                })
                sendJSON(send_data)
            elif (data['event']['text'].find("Who's there?") != -1):
                send_data = json.dumps({
                    "text": "A Bot user",
                    "channel": "CDMKMFHHU"
                })
                sendJSON(send_data)
            elif (data['event']['text'].find("Bot user who?") != -1):
                send_data = json.dumps({
                    "text": "No. I'm a bot user. I don't understand jokes!",
                    "channel": "CDMKMFHHU"
                })
                sendJSON(send_data)
            else:
                logging.info("No Tell me a joke there")
                send_data = json.dumps({
                    "text": "Owen half completed me :sob: I only know how to respond to you asking for a joke",
                    "channel": "CDMKMFHHU"
                })
                sendJSON(send_data)
        context = {
            'data': data,
        }
        self.response.out.write(template.render(context))

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
