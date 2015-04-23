# -*- coding: UTF-8 -*-
import re
from steps.common_tests_steps.common_environment import run, docker_cleanup


def before_all(context):
    # Save run proc as context.run
    context.run = run


def before_scenario(context, scenario):
    # TODO: Move me to a function and run it from example's before_scenario

    # Stop container and remove it
    # Container name is stored in context.userdata.image
    # Can be redefined in runtime via 'behave -D image="woot"'
    # If its not specified it will be built

    try:
        if 'IMAGE' not in context.config.userdata:
            raise Exception("Please specify image to test: behave -D=IMAGE=test")
        context.image = context.config.userdata['IMAGE']
        # Make sure we generate nice name here (for images like openshift/postgresql-92-centos7)
        cid_file_name = re.sub(r'\W+', '', context.image)
        context.cid_file = "/tmp/%s.cid" % cid_file_name
        docker_cleanup(context)
    except Exception as e:
        print("before_scenario: exception %s" % str(e))


def after_scenario(context, scenario):
    # TODO: Move me to a function and run it from example's before_scenario

    # Store scenario logs
    try:
        if not getattr(context, "cid", None):
            return
        if scenario.status == 'failed':
            run("docker logs %s" % context.cid)
        docker_cleanup(context)
    except Exception as e:
        print("after_scenario: exception %s" % str(e))
