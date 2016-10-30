#    Author: Denys Makogon
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os
import yaml

from aiorchestra.core import context
from aiorchestra.core import logger


log = logger.UnifiedLogger(
    log_to_console=True,
    level="INFO").setup_logger(__name__)


def run_deployment(name, template, inputs,
                   enable_serialization=False,
                   root_directory=None,
                   enable_rollback=False):

    deployment_context = context.OrchestraContext(
        name, path=os.path.join(
            root_directory, template),
        template_inputs=inputs, logger=log,
        enable_rollback=enable_rollback
    )

    deployment_context.run_deploy()

    if enable_serialization:
        s_context_before = deployment_context.serialize()
        deployment_context = (
            context.OrchestraContext.load(log, **s_context_before))
    for k, v in deployment_context.outputs.items():
        print("\n", k, "\n", v)

    deployment_context.run_undeploy()


def pycon_hk(enable_serialization=False, enable_rollback=False):
    pycon_demo_root = (
        '/Users/denismakogon/Documents/Invader/'
        'aiorchestra_examples/'
    )
    name = 'pycon-hk-2016'
    inputs_file = '../deployment_inputs.yaml'
    template = 'pycon-demo-docker.yaml'

    with open(os.path.join(pycon_demo_root, inputs_file), 'r') as inp:
        new_conf = yaml.load(inp)
        run_deployment(name, template, new_conf,
                       enable_serialization=enable_serialization,
                       enable_rollback=enable_rollback,
                       root_directory=pycon_demo_root)


pycon_hk(enable_rollback=True)
