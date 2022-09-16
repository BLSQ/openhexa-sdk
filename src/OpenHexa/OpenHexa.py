import json
import os
import requests
import uuid
import warnings
from datetime import datetime


class OpenHexaContext:
    _url = None
    _token = None
    _fake = False

    def __init__(self):
        url = os.environ.get("HEXA_WEBHOOK_URL", "")
        token = os.environ.get("HEXA_WEBHOOK_TOKEN", "")

        if url == "" or token == "":
            warnings.warn("We don't seems to be in an Airflow DagRun. Everything will be simulated.")
            self._fake = True

        self._url = url
        self._token = token

    def get_current_dagrun(self):
        return DagRun(self, fake=self._fake)


class DagRun:
    _url = None
    _http_headers = None
    _dag = None
    _dag_run = None
    _dag_task_id = None
    _fake = None

    def __init__(self, OH: OpenHexaContext, fake: bool=False):
        self._fake = fake
        self._url = OH._url
        self._http_headers = {"Authorization": "Bearer %s" % OH._token}

    def log_message(self, priority: str, message: str) -> bool:
        valid_prio = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if priority not in valid_prio:
            raise ValueError(f"'priority' must be one of {valid_prio}")

        if not self._fake:
            r = requests.post(
                self._url,
                headers=self._http_headers,
                json={
                    "id": str(uuid.uuid4()),
                    "object": "event",
                    "created": datetime.timestamp(datetime.utcnow()),
                    "type": "log_message",
                    "data": {"priority": priority, "message": message},
                },
            )
            r.raise_for_status()
            return True
        else:
            return False

    def progress_update(self, progress: int,) -> bool:
        if progress < 1 or progress > 100:
            raise ValueError(f"'progress' must be > 0 and <= 100")

        if not self._fake:
            r = requests.post(
                self._url,
                headers=self._http_headers,
                json={
                    "id": str(uuid.uuid4()),
                    "object": "event",
                    "created": datetime.timestamp(datetime.utcnow()),
                    "type": "progress_update",
                    "data": progress,
                },
            )
            r.raise_for_status()
            return True
        else:
            return False


    def add_outputfile(self, title: str, uri: str) -> bool:
        if not self._fake:
            r = requests.post(
                self._url,
                headers=self._http_headers,
                json={
                    "id": str(uuid.uuid4()),
                    "object": "event",
                    "created": datetime.timestamp(datetime.utcnow()),
                    "type": "add_output_file",
                    "data": {"title": title, "uri": uri},
                },
            )
            r.raise_for_status()
            return True
        else:
            return False

    
def get_current_dagrun():
    oh = OpenHexaContext()
    return DagRun(oh, fake=oh._fake)
