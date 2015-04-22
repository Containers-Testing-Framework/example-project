# -*- coding: UTF-8 -*-
from behave import step, when, then, given
import subprocess
from time import sleep


@step(u'Docker container is started')
@step(u'Docker container is started with params "{params}"')
def container_started(context, params=''):
    # TODO: allow tables here
    # A nice candidate for common steps
    context.job = context.run('docker run -d --cidfile %s %s %s' % (context.cid_file, params, context.image))
    context.cid = open(context.cid_file).read().strip()


@then(u'port {port:d} is open')
@then(u'port {port:d} is {negative} open')
def port_open(context, port, negative=False):
    # Get container IP
    context.ip = context.run("docker inspect --format='{{.NetworkSettings.IPAddress}}' %s" % context.cid).strip()

    for attempts in xrange(0, 5):
        try:
            print(context.run('nc -w5 %s %s < /dev/null' % (context.ip, port)))
            return
        except subprocess.CalledProcessError:
            # If  negative part was set, then we expect a bad code
            # This enables steps like "can not be established"
            if negative:
                return
            sleep(5)

    raise Exception("Failed to connect to port " % port)


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
        logs = context.run("docker logs %s" % context.cid, print_output=False)
        if logs == '':
            sleep(1)
            continue
        else:
            break
    # TODO: Use proper re ffs
    password = logs.split('\n')[0].split(' ')[-1]
    print("Got password: '%s'" % password)

    # TODO: requires sshpass package
    for attempts in xrange(0, 5):
        try:
            print(context.run('sshpass -p "%s" ssh %s@%s exit' % (
                password, user, context.ip)))
            return
        except subprocess.CalledProcessError:
            # If  negative part was set, then we expect a bad code
            # This enables steps like "can not be established"
            if action:
                return
            sleep(5)

    raise Exception("Failed to connect to ssh")
