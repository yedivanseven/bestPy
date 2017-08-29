#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A minimalistic template for implementing a RESTful API for bestPy.

Using the flask microframework, this script illustrates how a RESTful API
serving up bestPy's recommendations locally in JSON format could be set up.
Feel free to alter and expand it as needed. Happy experimenting!

"""

# We only need the following two lines because the examples folder is a
# subdirectory of the bestPy package.
import sys
sys.path.append('../..')

# Now we do some minimal imports from bestPy.
from bestPy import write_log_to, RecoBasedOn
from bestPy.datastructures import Transactions

# To serve up our recommendations, we are going to use the equally
# minimalistic and powerful web framework flask.
from flask import Flask, jsonify, request

# Set up logging and a minimal bestPy recommender.
write_log_to('logfile.txt', 20)
file = './examples_data.csv'
data = Transactions.from_csv(file)
recommendation = RecoBasedOn(data)

# Instantiate a new flask web service ...
app = Flask(__name__)

# ... and define what happens at which URL, starting with the root.
@app.route('/')
def root():
    """Returns instructions of what there is to see in simple HTML."""
    response = """<h1>Welcome to <code>bestPy</code>'s RESTful API!</h1>
               To explore this minimal setup, we recommend you try the
               following.
               <ul>
                 <li>Check out the URL <code>/user/</code> for a few valid
                   user IDs.</li>
                 <li>Pick any one and navigate to <code>/user/ID</code> to
                   get a recommendation for that particular user.</li>
                 <li>To change the number X of recommendations, add the
                   query <code>/user/ID?n_recos=X</code> to the URL.
               </ul>
               Keep an eye on the "logfile.txt" to stay ahead of things!"""
    return response


@app.route('/user/')
def user():
    """Returns the first 10 customer IDs under the URL /user/ as JSON."""
    some_users = {'some user IDs': [data.user.id_of[i] for i in range(10)]}
    response = jsonify(some_users)
    response.status_code = 200
    return response


@app.route('/user/<userid>')
def userid(userid):
    """Returns a number of recommendations for the requested customer as JSON.

    The customer is specified by its ID <userid> and the number X of requested
    recommendations is specified by adding the query "n_recos=X" to the URL as
    in: /user/<userid>?n_recos=X

    """
    n_recos = 5
    if 'n_recos' in request.args:
        n_recos = int(request.args['n_recos'])
    top_hits = recommendation.for_one(userid, n_recos)
    articles = {'recommended articles': [article for article in top_hits]}
    response = jsonify(articles)
    response.status_code = 200
    return response

# Now start the service on locahost:5002 by typing "python 07_RESTfulAPI.py"
# on the command prompt of your terminal. A simple, instructive message is
# displayed there to tell you what's going on. Keep an eye on the logfile to
# keep track of events as you go explore.
if __name__ == '__main__':
    port = 5002
    print('Serving bestPy on port', port)
    print('Press Ctrl-C to quit ...')
    app.run(port=port)
