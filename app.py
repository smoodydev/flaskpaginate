import os
from flask import Flask, render_template, redirect, url_for, request
from flask_paginate import Pagination, get_page_args
from bson.objectid import ObjectId
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'testerMongo'

##app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

mongo = PyMongo(app)

app.templates = ""

users = []

for x in range(1,101):
    string = ""
    if x%3==0:
        string = string+"Fizz"
    elif x%5==0:
        string = string+"Buzz"
    else:
        string = str(x)
    users.append({"id" : x, "name": str(x)+" is my name",  "fb": string})


def get_users(offset=0, per_page=10):
    return users[offset: offset + per_page]

def get_tests(offset=0, per_page=10):
    thetests = mongo.db.mongoTestingDataBase.find()
    return thetests[offset: offset + per_page]



@app.route('/')
def index():
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = len(users)
    pagination_users = get_users(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    return render_template('index.html',
                           users=pagination_users,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )

@app.route('/add')
def addTest():
    return render_template('addtask.html')

@app.route('/inserttest', methods=['POST'])
def insert_test():
    test = mongo.db.mongoTestingDataBase
    test.insert_one(request.form.to_dict())
    return redirect(url_for('index'))


@app.route('/here')
def showTests():
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = mongo.db.mongoTestingDataBase.count()
    paginatedTests = get_tests(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    return render_template('thetests.html',
                           tests=paginatedTests,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


if __name__ == '__main__':
    app.run(debug=True)