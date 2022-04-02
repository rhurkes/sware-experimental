from bottle import post, get, run, request
from collections import deque
from datetime import datetime
import bottle, logging

OLD_THRESHOLD_MILLIS = 30 * 60 * 1000   # 30m
EXPIRATION_ENABLED = True

logging.basicConfig(filename='api.log', encoding='utf-8', level=logging.INFO)
# Bottle only support 100KiB posts by default, bump to 1MiB
bottle.BaseRequest.MEMFILE_MAX = 1024 * 1024

current_event_id = 0
with open('sware-api-event-id', 'r') as file:
    current_event_id = int(file.readline().strip())
logging.info(f'Using event ID: {current_event_id}')
all_events = deque([], 256)

def get_next_id():
    global current_event_id
    current_event_id += 1
    with open('sware-api-event-id', 'w') as file:
        file.write(str(current_event_id))
    return current_event_id

def expire_old_events():
    if not EXPIRATION_ENABLED:
        return
    threshold = round(datetime.now().timestamp() * 1000) - OLD_THRESHOLD_MILLIS
    while all_events and all_events[-1]['ts'] < threshold:
        logging.info(f'Evicting {all_events[0]["id"]}')
        all_events.popleft()

@post('/events')
def post_events():
    for event in request.json:
        event['id'] = get_next_id()
        all_events.append(event)
    expire_old_events()

@get('/events/<offset>')
def get_events(offset):
    offset = int(offset)
    data = []
    data = list(all_events) if offset == -1 else [x for x in all_events if x['id'] > offset]
    return {'data': data}

run(host='0.0.0.0', port=8080)
