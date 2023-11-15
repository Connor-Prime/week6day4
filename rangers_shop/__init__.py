from flask import Flask
from .blueprints.site.routes import site #add this import to grab out site blueprint
from .blueprints.about_page.routes import about_page
from config import Config
#instantiating our Flask app
app = Flask(__name__) #passing in the __name__ variable which just takes the name of the folder we're in

app.config.from_object(Config)
#we are going to use a decorator to create our first route
#@app.route("/")
#def hello_world():
#    return "<p>Hello World!</p>"

# We can also comment out the above because this is rendering to the same
# location as our site blueprint. 


app.register_blueprint(site) # add this here to register your site blueprint
app.register_blueprint(about_page) 