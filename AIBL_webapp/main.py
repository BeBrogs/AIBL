from flask import Flask, url_for
from app import views

import warnings

webapp = Flask(__name__)

#Adding routes
webapp.add_url_rule("/", "index", views.index)
webapp.add_url_rule("/detection", "detection", views.detection, methods=["GET", "POST"])
webapp.add_url_rule("/about", "about", views.about)
webapp.add_url_rule("/login", "login", views.login)
webapp.add_url_rule("/register", "register", views.register)
webapp.add_url_rule("/progress", "tracker", views.tracker)
if __name__ == "__main__":
    webapp.run(debug=True)