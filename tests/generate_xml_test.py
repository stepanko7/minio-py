# Minimal Object Storage Library, (C) 2015 Minio, Inc.
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
from unittest import TestCase

from nose.tools import eq_

from minio.xml_requests import bucket_constraint

__author__ = 'minio'


class GenerateRequestTest(TestCase):
    def test_generate_bucket_constraint(self):
        expected_string = b'<CreateBucketConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">' \
                          b'<LocationConstraint>region</LocationConstraint></CreateBucketConfiguration>'
        actual_string = bucket_constraint('region')
        eq_(expected_string, actual_string)
