#!/usr/bin/env python

from distutils.core import setup

setup(name='ecstaskrunner',
    version='0.0.1',
    description='Helper tools to run a task on AWS ECS and follow the logs',
    author='Michael Osl',
    author_email='moee@users.noreply.github.com',
    url='https://github.com/moee/ecstaskrunner',
    packages=['ecstaskrunner'],
    install_requires=['boto3']
)

