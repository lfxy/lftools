"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import sys
import os
import json
import tempfile
import hashlib
from datetime import datetime
import ambari_simplejson as json # simplejson is much faster comparing to Python 2.6 json module and has the same functions set.

from ambari_commons import constants

from resource_management.libraries.script.script import Script
from resource_management.core.resources.system import Execute, File
from resource_management.core import shell
from resource_management.libraries.functions import stack_select
from resource_management.libraries.functions import upgrade_summary
from resource_management.libraries.functions.constants import Direction
from resource_management.libraries.functions.format import format
from resource_management.libraries.resources.execute_hadoop import ExecuteHadoop
from resource_management.libraries.functions.security_commons import build_expectations, \
  cached_kinit_executor, get_params_from_filesystem, validate_security_config_properties, \
  FILE_TYPE_XML

from resource_management.core.exceptions import Fail
from resource_management.core.shell import as_user
from resource_management.core.logger import Logger


from ambari_commons.os_family_impl import OsFamilyImpl
from ambari_commons import OSConst


from hdfs_namenode import namenode, wait_for_safemode_off, refreshProxyUsers, format_namenode
from hdfs import hdfs, reconfig
from utils import initiate_safe_zkfc_failover, get_hdfs_binary, get_dfsadmin_base_command
from resource_management.libraries.functions.namenode_ha_utils import get_hdfs_cluster_id_from_jmx

# The hash algorithm to use to generate digests/hashes
HASH_ALGORITHM = hashlib.sha224

class NameNode(Script):

  def get_hdfs_binary(self):
    """
    Get the name or path to the hdfs binary depending on the component name.
    """
    return get_hdfs_binary("hadoop-hdfs-namenode")

  def install(self, env):
    import params
    env.set_params(params)
    self.install_packages(env)
    #TODO we need this for HA because of manual steps
    self.configure(env)

  def configure(self, env):
    import params
    env.set_params(params)
    hdfs("namenode")
    hdfs_binary = self.get_hdfs_binary()
    namenode(action="configure", hdfs_binary=hdfs_binary, env=env)

  def save_configs(self, env):
    import params
    env.set_params(params)
    hdfs()

  def reload_configs(self, env):
    import params
    env.set_params(params)
    Logger.info("RELOAD CONFIGS")
    reconfig("namenode", params.namenode_address)

  def reloadproxyusers(self, env):
    import params
    env.set_params(params)
    Logger.info("RELOAD HDFS PROXY USERS")
    refreshProxyUsers()

  def format(self, env):
    import params
    env.set_params(params)

    if params.security_enabled:
        Execute(params.nn_kinit_cmd,
                user=params.hdfs_user
        )

    hdfs_cluster_id = get_hdfs_cluster_id_from_jmx(params.hdfs_site, params.security_enabled, params.hdfs_user)

    # this is run on a new namenode, format needs to be forced
    Execute(format("hdfs --config {hadoop_conf_dir} namenode -format -nonInteractive -clusterId {hdfs_cluster_id}"),
            user = params.hdfs_user,
            path = [params.hadoop_bin_dir],
            logoutput=True
    )

  def start(self, env, upgrade_type=None):
    import params
    env.set_params(params)
    self.configure(env)
    hdfs_binary = self.get_hdfs_binary()
    namenode(action="start", hdfs_binary=hdfs_binary, upgrade_type=upgrade_type,
      upgrade_suspended=params.upgrade_suspended, env=env)

    # after starting NN in an upgrade, touch the marker file - but only do this for certain
    # upgrade types - not all upgrades actually tell NN about the upgrade (like HOU)
#    if upgrade_type in (constants.UPGRADE_TYPE_ROLLING, constants.UPGRADE_TYPE_NON_ROLLING):
      # place a file on the system indicating that we've submitting the command that
      # instructs NN that it is now part of an upgrade

  def stop(self, env, upgrade_type=None):
    import params
    env.set_params(params)
    hdfs_binary = self.get_hdfs_binary()
    namenode(action="stop", hdfs_binary=hdfs_binary, upgrade_type=upgrade_type, env=env)

  def status(self, env):
    import status_params
    env.set_params(status_params)
    namenode(action="status", env=env)

  def refresh_nodes(self, env):
    import params
    env.set_params(params)
    namenode(action="refresh_nodes")

@OsFamilyImpl(os_family=OsFamilyImpl.DEFAULT)
class NameNodeDefault(NameNode):

  def restore_snapshot(self, env):
    """
    Restore the snapshot during a Downgrade.
    """
    print "TODO AMBARI-12698"
    pass

  def wait_for_safemode_off(self, env):
    wait_for_safemode_off(self.get_hdfs_binary(), afterwait_sleep=30, execute_kinit=True)


  def pre_upgrade_restart(self, env, upgrade_type=None):
    Logger.info("Executing Stack Upgrade pre-restart")
    import params
    env.set_params(params)

    stack_select.select_packages(params.version)

  def post_upgrade_restart(self, env, upgrade_type=None):
    Logger.info("Executing Stack Upgrade post-restart")
    import params
    env.set_params(params)

    hdfs_binary = self.get_hdfs_binary()
    dfsadmin_base_command = get_dfsadmin_base_command(hdfs_binary)
    dfsadmin_cmd = dfsadmin_base_command + " -report -live"
    Execute(dfsadmin_cmd,
            user=params.hdfs_user,
            tries=60,
            try_sleep=10
    )


  def get_log_folder(self):
    import params
    return params.hdfs_log_dir

  def get_user(self):
    import params
    return params.hdfs_user

  def get_pid_files(self):
    import status_params
    return [status_params.namenode_pid_file]

def _print(line):
  sys.stdout.write(line)
  sys.stdout.flush()

if __name__ == "__main__":
  NameNode().execute()
