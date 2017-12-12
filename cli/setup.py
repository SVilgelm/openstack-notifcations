#!/usr/bin/env python

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages


def read_requirements():
    with open('requirements.txt') as f:
        return [l for l in [l.strip() for l in f]
                if l and not l.startswith('#')]


setup(
    name='OSN-CLI',
    version='1.0',
    description='OpenStack Notifications Command Line Interface',
    author='Sergey Vilgelm',
    author_email='sergey@vilgelm.info',
    url='https://github.com/SVilgelm/openstack-notifcations',
    packages=find_packages(),
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'osn-cli = osn_cli.app:main'
        ],
        'osn': [
            'AddEvent = osn_cli.events:Event'
        ]
    }
)