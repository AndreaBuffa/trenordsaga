# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import copy
import httmock
import json
import mock
import os
import sys
import unittest

from apitools.base.py import encoding
from endpoints_management.config import service_config
from endpoints_management.control import sm_messages
from oauth2client import client

class ServiceConfigFetchTest(unittest.TestCase):

    _ACCESS_TOKEN = u"test_access_token"

    _SERVICE_NAME = u"test_service_name"
    _SERVICE_VERSION = u"test_service_version"
    _SERVICE_CONFIG_JSON = {
        u"name": _SERVICE_NAME,
        u"id": _SERVICE_VERSION
    }
    _SERVICE_CONFIG_LIST_JSON = {
        u"serviceConfigs": [{
            u"name": _SERVICE_NAME,
            u"title": _SERVICE_NAME,
            u"documentation": {},
            u"usage": {},
            u"id": _SERVICE_VERSION
        }]
    }

    _credentials = mock.MagicMock()
    _get_http_client = mock.MagicMock()

    def setUp(self):
        os.environ[u"ENDPOINTS_SERVICE_NAME"] = ServiceConfigFetchTest._SERVICE_NAME
        os.environ[u"ENDPOINTS_SERVICE_VERSION"] = ServiceConfigFetchTest._SERVICE_VERSION

        self._set_up_default_credential()

    def test_no_service_name(self):
        del os.environ[u"ENDPOINTS_SERVICE_NAME"]
        message = u'The "ENDPOINTS_SERVICE_NAME" environment variable is not set'
        with self.assertRaisesRegexp(ValueError, message):
            service_config.fetch_service_config()

    @mock.patch(u"endpoints_management.config.service_config.client.GoogleCredentials",
                _credentials)
    @mock.patch(u"endpoints_management.config.service_config._get_http_client", _get_http_client)
    def test_no_service_version(self):
        del os.environ[u"ENDPOINTS_SERVICE_VERSION"]

        list_mock_response = mock.MagicMock()
        list_mock_response.status = 200
        list_mock_response.data = json.dumps(ServiceConfigFetchTest._SERVICE_CONFIG_LIST_JSON)

        config_mock_response = mock.MagicMock()
        config_mock_response.status = 200
        config_mock_response.data = json.dumps(ServiceConfigFetchTest._SERVICE_CONFIG_JSON)

        mock_http_client = mock.MagicMock()
        mock_http_client.request.side_effect = [list_mock_response, config_mock_response]
        ServiceConfigFetchTest._get_http_client.return_value = mock_http_client

        service = encoding.JsonToMessage(sm_messages.Service,
                                         json.dumps(self._SERVICE_CONFIG_JSON))
        self.assertEqual(service, service_config.fetch_service_config())

        self.assertEqual(2, mock_http_client.request.call_count)

        headers={u"Authorization": u"Bearer " + ServiceConfigFetchTest._ACCESS_TOKEN}

        template = service_config._SERVICE_MGMT_URL_TEMPLATE
        url1 = template.format(ServiceConfigFetchTest._SERVICE_NAME, '').rstrip('/')
        url2 = template.format(ServiceConfigFetchTest._SERVICE_NAME,
                               ServiceConfigFetchTest._SERVICE_VERSION)

        call1 = mock.call(u"GET", url1, headers=headers)
        call2 = mock.call(u"GET", url2, headers=headers)

        mock_http_client.request.assert_has_calls([call1, call2])

    @mock.patch(u"endpoints_management.config.service_config.client.GoogleCredentials",
                _credentials)
    @mock.patch(u"endpoints_management.config.service_config._get_http_client", _get_http_client)
    def test_fetch_service_config(self):
        mock_response = mock.MagicMock()
        mock_response.status = 200
        mock_response.data = json.dumps(ServiceConfigFetchTest._SERVICE_CONFIG_JSON)
        mock_http_client = mock.MagicMock()
        mock_http_client.request.return_value = mock_response
        ServiceConfigFetchTest._get_http_client.return_value = mock_http_client

        service = encoding.JsonToMessage(sm_messages.Service,
                                         json.dumps(self._SERVICE_CONFIG_JSON))
        self.assertEqual(service, service_config.fetch_service_config())

        template = service_config._SERVICE_MGMT_URL_TEMPLATE
        url = template.format(ServiceConfigFetchTest._SERVICE_NAME,
                              ServiceConfigFetchTest._SERVICE_VERSION)
        headers={u"Authorization": u"Bearer " + ServiceConfigFetchTest._ACCESS_TOKEN}
        mock_http_client.request.assert_called_once_with(u"GET", url,
                                                         headers=headers)

    @mock.patch(u"endpoints_management.config.service_config.client.GoogleCredentials",
                _credentials)
    @mock.patch(u"endpoints_management.config.service_config._get_http_client", _get_http_client)
    def test_fetch_service_config_failed_forbidden(self):
        mock_response = mock.MagicMock()
        mock_response.status = 403
        mock_http_client = mock.MagicMock()
        mock_http_client.request.return_value = mock_response
        ServiceConfigFetchTest._get_http_client.return_value = mock_http_client
        expected_message = (u"No service 'test_service_name' found or permission denied. "
                            u"If this is a new Endpoints service, make sure you've deployed "
                            u"the service config using gcloud.")
        with self.assertRaisesRegexp(service_config.ServiceConfigException, expected_message):
            service_config.fetch_service_config()

    @mock.patch(u"endpoints_management.config.service_config.client.GoogleCredentials",
                _credentials)
    @mock.patch(u"endpoints_management.config.service_config._get_http_client", _get_http_client)
    def test_fetch_service_config_failed_not_found(self):
        mock_response = mock.MagicMock()
        mock_response.status = 404
        mock_http_client = mock.MagicMock()
        mock_http_client.request.return_value = mock_response
        ServiceConfigFetchTest._get_http_client.return_value = mock_http_client
        expected_message = (u"The service 'test_service_name' was found, but no service config "
                            u"was found for version 'test_service_version'.")
        with self.assertRaisesRegexp(service_config.ServiceConfigException, expected_message):
            service_config.fetch_service_config()

    @mock.patch(u"endpoints_management.config.service_config.client.GoogleCredentials",
                _credentials)
    @mock.patch(u"endpoints_management.config.service_config._get_http_client", _get_http_client)
    def test_fetch_service_config_with_wrong_service_name(self):
        mock_response = mock.MagicMock()
        mock_response.status = 200
        config = copy.deepcopy(ServiceConfigFetchTest._SERVICE_CONFIG_JSON)
        config[u"name"] = u"incorrect_service_name"
        mock_response.data = json.dumps(config)
        mock_http_client = mock.MagicMock()
        mock_http_client.request.return_value = mock_response
        ServiceConfigFetchTest._get_http_client.return_value = mock_http_client

        message = (u"Unexpected service name in service config: " +
                   config[u"name"])
        with self.assertRaisesRegexp(ValueError, message):
            service_config.fetch_service_config()

    @mock.patch(u"endpoints_management.config.service_config.client.GoogleCredentials",
                _credentials)
    @mock.patch(u"endpoints_management.config.service_config._get_http_client", _get_http_client)
    def test_fetch_service_config_with_wrong_service_version(self):
        mock_response = mock.MagicMock()
        mock_response.status = 200
        config = copy.deepcopy(ServiceConfigFetchTest._SERVICE_CONFIG_JSON)
        config[u"id"] = u"incorrect_service_version"
        mock_response.data = json.dumps(config)
        mock_http_client = mock.MagicMock()
        mock_http_client.request.return_value = mock_response
        ServiceConfigFetchTest._get_http_client.return_value = mock_http_client

        message = (u"Unexpected service version in service config: " +
                   config[u"id"])
        with self.assertRaisesRegexp(ValueError, message):
            service_config.fetch_service_config()

    def _set_up_default_credential(self):
        default_credential = mock.MagicMock()
        ServiceConfigFetchTest._credentials.get_application_default.return_value \
            = default_credential
        default_credential.create_scoped.return_value = default_credential
        token = ServiceConfigFetchTest._ACCESS_TOKEN
        access_token = client.AccessTokenInfo(access_token=token, expires_in=None)
        default_credential.get_access_token.return_value = access_token
