"""
The classes that are required while creating the Lambda functions, DynamoDB access, EC2 access, S3 buckets.
Client access generalized.
"""

import os
import sys

import boto3

from botocore.exceptions import ClientError, UnknownCredentialError, UnknownClientMethodError, UnknownEndpointError


class BaseClient(object):
    """
    Parent class object for initialization of a service client.
    """
    def __init__(self, client_name, *args, **kwargs):
        """
        The common initialization method for any client.

        :param client_name: Which client to start
        :param args: Positional args
        :param kwargs: Keyword args
        """
        self._client = boto3.client(client_name, *args, **kwargs)


class IAM(BaseClient):
    """
    Use for selecting role or role policy (if existing); or else create new.
    """
    def __init__(self, role_name, *args, **kwargs):
        """
        Initializes the IAM client as a subclass of the BaseClient. Used for role and role policy related ops.

        :param role_name: Name of the role to assume (if available, or create new)
        :param args: Additional positional arguments
        :param kwargs: Additional keyword arguments
        """
        super(IAM, self).__init__(client_name='iam', *args, **kwargs)
        self._role_name = role_name
        self._role_policy_doc_name = role_name + "_policy.json"

    @property
    def get_role_name(self):
        return self._role_name

    @property
    def get_role_policy_doc_name(self):
        return self._role_policy_doc_name

    def _get_role_policy_doc(self):
        """
        Reads the policy for the selected role.

        :return: The policy or throws an UnidentifiedPolicyError.
        """
