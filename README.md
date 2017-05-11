# ecs_task_runner
Helper tools to run a task on AWS ECS and follow the logs

# Why?
The use case why I created this script is that we want to run ECS tasks in Jenkins and directly see the output of the tasks that are being run. This is very cumbersome to achieve using the `aws cli`. Hence this library.

# Installation
Until this package is distributed as pip package, you have to install it directly from this repository:

```
pip install git+https://github.com/moee/ecs_task_runner@0.0.1
```

# Usage
## Example 1: Jenkins Integration

```sh
#!/bin/sh
pip install git+https://github.com/moee/ecs_task_runner@0.0.1

python << END
import ecstaskrunner, sys, logging

logging.basicConfig()
logging.getLogger('ecstaskrunner').setLevel(logging.INFO)

sys.exit(
    ecstaskrunner.run_task(
        cluster="YOUR-CLUSTER-NAME",
        taskDefinition='YOUR-TASK-DEFINITION',
    )
)
END
```
This runs the task named `YOUR-TASK-DEFINITION` on the cluster `YOUR-CLUSTER-NAME`, displays all the output (Note: this only works if the container definition uses the awslogs driver) and waits for the task to stop. Only if all containers have stopped and exited with `0` the job will be marked as success.

## Example 2: Get the log output of a task

```python
import ecstaskrunner
task = ecstaskrunner.task.Task(cluster='YOUR-CLUSTER-NAME', taskId='YOUR-TASK-ID')
for container in task.containers:
    for line in task.containers[container].get_log_events():
        print "%s: %s" % (container, line)
```
