import boto3
import logging
from ecstaskrunner.container import Container

class Task:
    def __init__(self, cluster, taskId):
        self.cluster = cluster
        self.taskId = taskId
        self.containers = {}
        self.client = boto3.client('ecs')
        self.logger = logging.getLogger('Task')
       
        task = self.describeTask()
    
        if not task:
            self.logger.warn("Task with id %s does not exist" % taskId) 
            return

        self.taskDefinitionArn = task['taskDefinitionArn']
        containers = task['containers']
        response = self.client.describe_task_definition(taskDefinition=self.taskDefinitionArn)
        containerDefinitions = response['taskDefinition']['containerDefinitions']

        self.logger.debug("task definition arn: %s" % self.taskDefinitionArn)

        for container in self.describeTask()['containers']:
            self.containers[container['name']] = Container(
                self.taskId,
                container,
                [x for x in containerDefinitions if x['name'] == container['name']][0]
            )

    def describeTask(self):
        response = self.client.describe_tasks(cluster=self.cluster, tasks=[self.taskId])
        if len(response['tasks']) != 1:
            return None
        return response['tasks'][0]

    def getLastStatus(self):
        return self.describeTask()['lastStatus']

    def isRunning(self):
        return self.getLastStatus() == "RUNNING"

    def isPending(self):
        return self.getLastStatus() == "PENDING"
