import os
from flask import Flask, render_template, redirect, url_for, request
from flask_paginate import Pagination, get_page_args
from bson.objectid import ObjectId
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'testerMongo'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
app.secret_key = 'some_secret'

mongo = PyMongo(app)

app.templates = ""


itemtotal = mongo.db.mongoTestingDataBase.find().count()




def get_tests(offset=0, per_page=10):
    thetests = mongo.db.mongoTestingDataBase.find()
    return thetests[offset: offset + per_page]



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add')
def addTest():
    return render_template('addtask.html')

@app.route('/inserttest', methods=['POST'])
def insert_test():
    test = mongo.db.mongoTestingDataBase
    giggle=test.insert(request.form.to_dict())
    print(giggle)
    print(test.find({'_id':giggle}))
    return redirect(url_for('index'))


@app.route('/here')
def showTests():
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = itemtotal
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
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=False)