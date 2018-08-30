import os
from flask import Flask
from flask_celery import make_celery
from celery.result import AsyncResult
import celery.states as states

env=os.environ
app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'amqp://admin:Krishna1986@192.168.3.113:5672//'
app.config['CELERY_RESULT_BACKEND'] = 'mongodb://root:Krishna1986@192.168.3.113:27017/admin'

celery = make_celery(app)

@app.route('/process/<name>')
def process(name):
	# celery.send_task('celery_app.reverse', name)
	task = celery.send_task('celery_app.reverse', args=[name])
	return task.id
	# reverse.delay(name)
	# return 'Asynchronous request made'

@app.route('/check/<string:id>')
def check_task(id):  
    res = celery.AsyncResult(id)
    return res.state if res.state==states.PENDING else str(res.result)

@celery.task(name='celery_app.reverse')
def reverse(string):
	return string[::-1]

if __name__ == '__main__':
	# app.run(debug=env.get('DEBUG',True), port=int(env.get('PORT',5000)), host=env.get('HOST','0.0.0.0'))
	app.run(debug=True)
