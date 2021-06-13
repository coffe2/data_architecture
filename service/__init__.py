from flask import Flask
from flask import request
import os
from src import user, mylogger, myconfig
import datetime
import pdb

app = Flask(__name__)

# create a logger.
project_root_path = os.getenv("DATA_ARCHITECTURE")
cfg = myconfig.get_config('{}/share/calendar.config'.format(
    project_root_path))
log_directory = cfg['logger'].get('log_directory')
loggers = dict()
loggers['login'] = mylogger.get_logger('login', log_directory)
loggers['calendar'] = mylogger.get_logger('calendar', log_directory)

@app.route('/login', methods=["POST"])
def login():
    """login API function.

    Specification can be found in `API.md` file.

    :return: JSON serialized string containing the login result with session_id
    :rtype: str
    """
    user_id = request.json.get('user_id')
    passwd = request.json.get('passwd')
    loggers['login'].info('{}: login'.format(user_id))

    ret = {"result": None,
        "session_id": None,
        "msg": ""}

    session_key = user.login(user_id, passwd, loggers['login'])
    loggers['login'].info('{}: session_key = {}'.format(user_id, session_key))
    if not session_key:
        ret["result"] = False
        ret["msg"] = "Failed to login"
    else:
        ret["result"] = True
        ret["session_id"] = session_key["session_id"]

    loggers['login'].info('{}: login result = {}'.format(user_id, ret))
    return ret
	

@app.route('/calendar', methods=["POST"])
def calendar():
    """caldendar API function.

    Specification can be found in `API.md` file.

    :return: JSON serialized string containing the result with session_id
    :rtype: str
    """
    session_id = request.json.get('session_id')
    request_type = request.json.get('request_type')
    loggers['calendar'].info('{}: calendar request type = {}'.format(
        session_id, request_type))

    ret = {"result": None,
        "msg": ""}

    if request_type not in ['add', 'show']:
        msg = '{}: Invalid request type = {}'.format(
                session_id, request_type)
        loggers['calendar'].error(msg)
        ret['result'] = False
        ret['msg'] = msg
        return ret

    what_time_is_it = datetime.datetime.now()
    doc_user = user.check_session(session_id,
            what_time_is_it.timestamp())
    if not doc_user:
        msg = '{}: Invalid session'.format(session_id)
        loggers['calendar'].error(msg)
        ret['result'] = False
        ret['msg'] = msg
        return ret

    date = datetime.datetime.today().strftime("%Y%m%d")
    if request_type == 'add':
        schedule = request.json.get('schedule')
        added_check = user.add_schedule(doc_user, date,
                schedule, loggers['calendar'])
        new_session = user.generate_session(doc_user)
        if added_check:
            msg = '{}: {} schedule added'.format(
                session_id, len(schedule))
            ret['result'] = True
        ret['msg'] = msg
        ret['session_id'] = new_session["session_id"]
    
    elif request_type == 'show':
        day_schedule = user.show_daySchedule(doc_user, date,
                loggers['calendar'])
        ret['schedule'] = day_schedule
        ret['result'] = True
        new_session = user.generate_session(doc_user)
        ret['session_id'] = new_session["session_id"]

    loggers['calendar'].info('{}: day schedule = {}'.format(
        session_id, ret))
    return ret
