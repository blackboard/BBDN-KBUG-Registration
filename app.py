import datetime
import os
import pprint

from flask import Flask, jsonify, request, render_template, url_for
from flask_caching import Cache
from werkzeug.exceptions import Forbidden
import json
from flask.wrappers import Response

import Config

import RestAuthController, RestUserController
import string
import secrets

from multiprocessing import Process
from flask_wtf import form

class ReverseProxied(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        scheme = environ.get('HTTP_X_FORWARDED_PROTO')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)


app = Flask('bbdn-biab-registration', template_folder='templates', static_folder='static')
app.wsgi_app = ReverseProxied(app.wsgi_app)

cache = Cache(app)

PAGE_TITLE = 'Kansas BUG Registration'

basic_oauth_service = RestAuthController.RestAuthController()

class Password():
    def generate(self):
        
        alphabet = string.ascii_letters + string.digits
        while True:
            password = ''.join(secrets.choice(alphabet) for i in range(10))
            if (any(c.islower() for c in password)
                    and any(c.isupper() for c in password)
                    and sum(c.isdigit() for c in password) >= 3):
                break
        
        return password

def init_service():
    
    global basic_oauth_service

    try:
        basic_oauth_service = RestAuthController.RestAuthController()
        basic_oauth_service.setBasicToken()

    except Exception as e:
        print(str(e))

    print("call init_service")

    init_service()

    print("init_service completed, start app")

@app.route('/', methods=['GET'])
def registration():
    tpl_kwargs = {
        'page_title': PAGE_TITLE
    }
    
    return render_template('registration.html')

@app.route('/register/', methods=['POST'])
def register():
        form = request.form

        print(str(form))

        given_name = form['fname']
        family_name = form['lname']
        email = form['email']
        company = form['institution']
        track = form['track']
        job_title = form['title']
        
        password = Password().generate()

        heavy_process = Process(  # Create a daemonic process with heavy "my_func"
            target=executeRegistration, args=(given_name,family_name,email,company,job_title,track,password),
            daemon=True
        )
        heavy_process.start()

        tp_kwargs = {
            'page_title' : "Registration Confirmed!",
            'url': 'https://' + Config.config['learn_rest_url'],
            'username' : email,
            'password' : password
        }
        
        return render_template('confirmation.html', **tp_kwargs)


def executeRegistration(given_name,family_name,email,company,job_title,track,password):
    
    global basic_oauth_service
    token = basic_oauth_service.getBasicToken()

    
    userCtrl = RestUserController.RestUserController(Config.config['learn_rest_url'], token)

    user = {
        "userName": email,
        "password": password,
        "institutionRoleIds" : [
            "kbug"
        ],
        "availability": {
            "available": "Yes"
        },
        "name": {
            "given": given_name,
            "family": family_name
        },
        "job": {
            "title": job_title,
            "company": company
        },
        "contact": {
            "email": email
        }
    }

    devres = userCtrl.createLearnUser(user)

    enrres = userCtrl.enrollUserInAllCourses("userName:" + email)

if __name__ == '__main__':
    
    print("call init_service")

    init_service()

    print("init_service completed, start app")
    
    port = int(os.environ.get('PORT', 9001))
    app.run(host='0.0.0.0', port=port)