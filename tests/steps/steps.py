# -*- coding: UTF-8 -*-
from behave import then
import subprocess
from time import sleep
import logging
from common_steps import common_docker_steps, common_connection_steps


@then(u'ssh connection can be established')
@then(u'ssh connection can {action:w} be established')
@then(u'ssh connection for user "{user:w}" can be established')
@then(u'ssh connection for user "{user:w}" can {action:w} be established')
def ssh_connect(context, user='user', action=False):
    # Get container IP
    context.ip = context.run("docker inspect --format='{{.NetworkSettings.IPAddress}}' %s" % context.cid).strip()

    # Get ssh passwords from logs
    logs = ''
    for attempts in xrange(0, 10):
        # Why doesn't docker wait until some logs are available?
        logs = context.run("docker logs %s" % context.cid)
        if logs == '':
            sleep(1)
            continue
        else:
            break
    # TODO: Use proper re ffs
    password = logs.split('\n')[0].split(' ')[-1]
    logging.debug("Got password: '%s'" % password)

    # TODO: requires sshpass package
    for attempts in xrange(0, 5):
        try:
            logging.debug(context.run('sshpass -p "%s" ssh %s@%s exit' % (
                password, user, context.ip)))
            return
        except subprocess.CalledProcessError:
            # If  negative part was set, then we expect a bad code
            # This enables steps like "can not be established"
            if action:
                return
            sleep(5)

    raise Exception("Failed to connect to ssh")
