from fastapi.testclient import TestClient
import unittest
from app import app


class EndpointTesttest_s(unittest.TestCase):

    def test_is_service_available(self):
        with TestClient(app) as client:
            response = client.get("/status")
        self.assertEqual(200, response.status_code)

    def test_is_robottask_startable(self):
        with TestClient(app) as client:
            response = client.get("/run/nochEinTask")
        self.assertEqual(200, response.status_code)

    def test_is_robottask_available_with_logs(self):
        with TestClient(app) as client:
            response = client.get("/run_and_show/nochEinTask")
        self.assertEqual(200, response.status_code)

    def test_is_robottask_available_with_reports(self):
        with TestClient(app) as client:
            response = client.get("/run_and_show_report/nochEinTask")
        self.assertEqual(200, response.status_code)

    def test_is_robottask_available_with_logs_and_arguments(self):
        with TestClient(app) as client:
            response = client.get("/run_and_show/nochEinTask?art=tests&description=EreichbarkeitsTestMitLogs")
        self.assertEqual(200, response.status_code)

    def test_is_robottask_available_with_reports_and_arguments(self):
        with TestClient(app) as client:
            response = client.get("/run_and_show_report/nochEinTask?art=tests&description=FunktionsTestMitReports")
        self.assertEqual(200, response.status_code)

    def test_is_robotlog_available(self):
        with TestClient(app) as client:
            response = client.get("/show_logs/nochEinTask")
        self.assertEqual(200, response.status_code)

    def test_is_robotreport_available(self):
        with TestClient(app) as client:
            response = client.get("/show_report/nochEinTask")
        self.assertEqual(200, response.status_code)

    def test_get_topic(self):
        with TestClient(app) as client:
            response = client.get("/get_topic/")
        self.assertEqual(200, response.status_code)

    def test_set_topic(self):
        with TestClient(app) as client:
            response = client.get("/set_topic/default_topic")
        self.assertEqual(200, response.status_code)

    def test_get_polling_intervall(self):
        with TestClient(app) as client:
            response = client.get("/get_polling_intervall/")
        self.assertEqual(200, response.status_code)


