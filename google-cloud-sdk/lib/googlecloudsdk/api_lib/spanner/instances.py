# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Spanner instance API helper."""

from apitools.base.py import list_pager
from googlecloudsdk.core import apis
from googlecloudsdk.core import properties
from googlecloudsdk.core import resources


def Create(instance, config, description, nodes):
  """Create a new instance."""
  client = apis.GetClientInstance('spanner', 'v1')
  msgs = apis.GetMessagesModule('spanner', 'v1')
  config_ref = resources.REGISTRY.Parse(
      config,
      collection='spanner.projects.instanceConfigs')
  req = msgs.SpannerProjectsInstancesCreateRequest(
      parent='projects/'+properties.VALUES.core.project.Get(required=True),
      createInstanceRequest=msgs.CreateInstanceRequest(
          instanceId=instance,
          instance=msgs.Instance(
              config=config_ref.RelativeName(),
              displayName=description,
              nodeCount=nodes)))
  return client.projects_instances.Create(req)


def Delete(instance):
  """Delete an instance."""
  client = apis.GetClientInstance('spanner', 'v1')
  msgs = apis.GetMessagesModule('spanner', 'v1')
  ref = resources.REGISTRY.Parse(
      instance,
      collection='spanner.projects.instances')
  req = msgs.SpannerProjectsInstancesDeleteRequest(
      name=ref.RelativeName())
  return client.projects_instances.Delete(req)


def Get(instance):
  """Get an instance by name."""
  client = apis.GetClientInstance('spanner', 'v1')
  msgs = apis.GetMessagesModule('spanner', 'v1')
  ref = resources.REGISTRY.Parse(
      instance,
      collection='spanner.projects.instances')
  req = msgs.SpannerProjectsInstancesGetRequest(
      name=ref.RelativeName())
  return client.projects_instances.Get(req)


def List():
  """List instances in the project."""
  client = apis.GetClientInstance('spanner', 'v1')
  msgs = apis.GetMessagesModule('spanner', 'v1')
  req = msgs.SpannerProjectsInstancesListRequest(
      parent='projects/'+properties.VALUES.core.project.Get(required=True))
  return list_pager.YieldFromList(
      client.projects_instances,
      req,
      field='instances',
      batch_size_attribute='pageSize')


def Patch(instance, description=None, nodes=None):
  """Update an instance."""
  fields = []
  if description is not None:
    fields.append('displayName')
  if nodes is not None:
    fields.append('nodeCount')
  client = apis.GetClientInstance('spanner', 'v1')
  msgs = apis.GetMessagesModule('spanner', 'v1')
  ref = resources.REGISTRY.Parse(
      instance,
      collection='spanner.projects.instances')
  req = msgs.SpannerProjectsInstancesPatchRequest(
      name=ref.RelativeName(),
      updateInstanceRequest=msgs.UpdateInstanceRequest(
          fieldMask=','.join(fields),
          instance=msgs.Instance(
              displayName=description,
              nodeCount=nodes)))
  return client.projects_instances.Patch(req)
