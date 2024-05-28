# from outlook_client import get_tornado_risks

# Day 1 outlooks are available at 0600z, 1300z, 1630z, 2000z
# hour = '1300'
# date = '2022-03-05'
# risks = get_tornado_risks(date, hour)
# print(risks)

from bottle import route, run, template
import asyncio

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

run(host='localhost', port=8080

