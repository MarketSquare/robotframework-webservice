from fastapi.testclient import TestClient
import unittest
from RobotFrameworkService.main import app


class EndpointTesttest_s(unittest.TestCase):

    def test_is_service_available(self):
        with TestClient(app) as client:
            response = client.get("/status")
        self.assertEqual(200, response.status_code)

    def test_is_robottask_startable(self):
        with TestClient(app) as client:
            response = client.get("/robotframework/run/anotherTask")
        self.assertEqual(200, response.status_code)

    def test_is_robottask_available_with_logs(self):
        with TestClient(app) as client:
            response = client.get("/robotframework/run_and_show/anotherTask")
        self.assertEqual(200, response.status_code)

    def test_is_robottask_available_with_reports(self):
        with TestClient(app) as client:
            response = client.get("/robotframework/run_and_show_report/anotherTask")
        self.assertEqual(200, response.status_code)

    def test_is_robottask_available_with_logs_and_arguments(self):
        with TestClient(app) as client:
            response = client.get("/robotframework/run_and_show/anotherTask?art=tests&description=EreichbarkeitsTestMitLogs")
        self.assertEqual(200, response.status_code)

    def test_is_robottask_available_with_reports_and_arguments(self):
        with TestClient(app) as client:
            response = client.get("/robotframework/run_and_show_report/anotherTask?art=tests&description=FunktionsTestMitReports")
        self.assertEqual(200, response.status_code)

    def test_is_robotlog_available(self):
        with TestClient(app) as client:
            run_response = client.get("/robotframework/run/anotherTask")
            execution_id = run_response.headers["x-request-id"]
            logs_response = client.get(f'/robotframework/show_log/{execution_id}')
        self.assertEqual(200, logs_response.status_code)

    def test_is_robotreport_available(self):
        with TestClient(app) as client:
            run_response = client.get("/robotframework/run/anotherTask")
            execution_id = run_response.headers["x-request-id"]
            report_response = client.get(f'/robotframework/show_report/{execution_id}')
        self.assertEqual(200, report_response.status_code)


