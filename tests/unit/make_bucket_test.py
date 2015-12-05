# -*- coding: utf-8 -*-
# Minio Python Library for Amazon S3 Compatible Cloud Storage, (C) 2015 Minio, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mock

from nose.tools import raises
from unittest import TestCase

from minio import Minio
from minio.api import _DEFAULT_USER_AGENT
from minio.error import ResponseError, InvalidBucketError

from .minio_mocks import MockResponse, MockConnection
from .helpers import generate_error

class MakeBucket(TestCase):
    @raises(TypeError)
    def test_bucket_is_string(self):
        client = Minio('http://localhost:9000')
        client.make_bucket(1234)

    @raises(InvalidBucketError)
    def test_bucket_is_not_empty_string(self):
        client = Minio('http://localhost:9000')
        client.make_bucket('  \t \n  ')

    @mock.patch('urllib3.PoolManager')
    def test_make_bucket_works(self, mock_connection):
        mock_server = MockConnection()
        mock_connection.return_value = mock_server
        mock_server.mock_add_request(MockResponse('PUT',
                                                  'http://localhost:9000/hello/',
                                                  {'User-Agent': _DEFAULT_USER_AGENT},
                                                  200))
        Minio('http://localhost:9000')

    @mock.patch('urllib3.PoolManager')
    @raises(ResponseError)
    def test_make_bucket_throws_fail(self, mock_connection):
        error_xml = generate_error('code', 'message', 'request_id',
                                   'host_id', 'resource')
        mock_server = MockConnection()
        mock_connection.return_value = mock_server
        mock_server.mock_add_request(MockResponse('PUT',
                                                  'http://localhost:9000/hello/',
                                                  {'User-Agent': _DEFAULT_USER_AGENT},
                                                  409, content=error_xml))
        client = Minio('http://localhost:9000')
        client.make_bucket('hello')
