import os
import responses
import requests
import unittest
import warnings
from responses import matchers

from openhexa import OpenHexaContext, DagRun, get_current_dagrun


class TestOpenHexaSDK(unittest.TestCase):

    def test_context_fake(self):
        os.environ["HEXA_WEBHOOK_URL"] = ""
        os.environ["HEXA_WEBHOOK_TOKEN"] = ""
        warnings.simplefilter("ignore")
        oh = OpenHexaContext()
        assert(oh._fake == True)

    def test_context(self):
        os.environ["HEXA_WEBHOOK_URL"] = "http://openhexa.local/airflow/webhook/"
        os.environ["HEXA_WEBHOOK_TOKEN"] = "whatanicetoken"
        oh = OpenHexaContext()
        assert(oh._fake == False)

        return oh

    @responses.activate
    def test_progress(self):
        dagrun = self.test_context().get_current_dagrun()

        responses.add(
            method = responses.POST,
            url = "http://openhexa.local/airflow/webhook/",
            status = 200,
            json = {'message': 'success'},
            match = [
                    matchers.header_matcher({"Authorization": "Bearer whatanicetoken"}),
                ],
        )
        res = dagrun.progress_update(progress=10)
        assert(res == True)

        with self.assertRaises(ValueError) as context:
            res = dagrun.progress_update(progress=120)
        self.assertTrue("'progress' must be > 0 and <= 100" in str(context.exception))


    @responses.activate
    def test_log_message(self):
        dagrun = self.test_context().get_current_dagrun()

        responses.add(
            method = responses.POST,
            url = "http://openhexa.local/airflow/webhook/",
            status = 200,
            json = {'message': 'success'},
            match = [
                    matchers.header_matcher({"Authorization": "Bearer whatanicetoken"}),
                ],
        )
        res = dagrun.log_message(priority="INFO", message="hello !")
        assert(res == True)

        with self.assertRaises(ValueError) as context:
            res = dagrun.log_message(priority="XXX", message="hello !")
        self.assertTrue("'priority' must be one of ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']" in str(context.exception))


if __name__ == '__main__':
    unittest.main()

