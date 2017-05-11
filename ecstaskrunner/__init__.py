import boto3
import sys
import time
import logging
import botocore.errorfactory
import ecstaskrunner
import ecstaskrunner.task

def run_task(**kwargs):
    client = boto3.client('ecs')

    response = client.run_task(**kwargs)

    logger = logging.getLogger('ecstaskrunner')

    taskResponse = response['tasks'][0]

    taskId = taskResponse['taskArn'][taskResponse['taskArn'].rfind("/")+1:]
    logger.debug(taskId)

    task = ecstaskrunner.task.Task(taskResponse['clusterArn'], taskId)

    logger.debug("task is pending")
    while task.isPending():
        time.sleep(1)

    while task.isRunning():
        for container in task.containers:
            for log_event in task.containers[container].get_log_events():
                logger.info("%s: %s" % (container, log_event))
    logger.debug("task status: %s" % task.getLastStatus())

    exitCode = 0

    for container in task.describeTask()['containers']:
        if 'reason' in container:
            logger.warn("%s failed: %s" % (container['name'], container['reason']))
            exitCode = 1
            continue
            
        logger.info("%s exited with code %d" % (container['name'], container['exitCode']))
        if container['exitCode'] != 0:
            exitCode = 2

    return exitCode
