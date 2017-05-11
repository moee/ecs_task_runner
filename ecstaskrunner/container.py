import boto3
import logging
import datetime

class Container:
    def __init__(self, taskId, config, definition):
        self.taskId = taskId
        self.config = config
        self.definition = definition
        self.name = config['name']
        self.startTime = None
        self.logger = logging.getLogger("Container")

    def get_log_events(self):
        logConfig = self.definition['logConfiguration']
        tasklogger = logging.getLogger(self.name)

        logs = boto3.client('logs')

        logStreamName = '%s/%s/%s' % (
            logConfig['options']['awslogs-stream-prefix'],
            self.name,
            self.taskId
        )
        nextToken = False 
        while True:
            a = {
                'logGroupName': logConfig['options']['awslogs-group'],
                'logStreamName': logStreamName,
                'startFromHead': True,
                'limit': 2
            }

            if nextToken:
                a['nextToken'] = nextToken
            else:    
                if self.startTime:
                    a['startTime'] = self.startTime

            try:
                response = logs.get_log_events(**a)
            except Exception as e:
                # todo not sure why i cannot check for the class directly
                if e.__class__.__name__ == 'ResourceNotFoundException':
                    self.logger.warn(e) 
                    return
                raise e
            for event in response['events']:
                yield "[%s] %s" % (
                    datetime.datetime.fromtimestamp(
                        event['timestamp']/1000
                    ),
                    event['message'])
                self.startTime = event['timestamp']+1

            if len(response['events']) != a['limit']:
                self.logger.debug("[EOS]")
                break

            nextToken = response['nextForwardToken']

