from fastapi.testclient import TestClient
import unittest
from RobotFrameworkService.main import app


class EndpointTesttest_s(unittest.TestCase):
    def test_is_service_available(self):
        response = self.__get_robot_webservice("/status")

    def test_is_robottask_startable(self):
        response = self.__get_robot_webservice(
            "/robotframework/run/all", expected_response_code=400
        )
        self.__is_robot_failed(response=response)

    def test_is_robottask_async_startable(self):
        self.__get_robot_webservice("/robotframework/run/all/async")

    def test_is_robottask_startable(self):
        response = self.__get_robot_webservice("/robotframework/run/anotherTask")
        self.__is_robot_passed(response=response)

    def test_is_robottask_async_startable(self):
        self.__get_robot_webservice("/robotframework/run/anotherTask/async")

    def test_robottask_with_variables(self):
        response = self.__get_robot_webservice(
            "/robotframework/run/Task with variable?input=qwerty"
        )
        self.__is_robot_passed(response=response, msg="Testing with variables failed")

    def test_is_robottask_available_with_logs(self):
        response = self.__get_robot_webservice(
            "/robotframework/run_and_show/anotherTask"
        )
        self.assertIn("PASS", response.text)

    def test_is_robottask_available_with_reports(self):
        response = self.__get_robot_webservice(
            "/robotframework/run_and_show_report/anotherTask"
        )
        self.assertIn("PASS", response.text)

    def test_is_robottask_available_with_logs_and_arguments(self):
        response = self.__get_robot_webservice(
            "/robotframework/run_and_show/anotherTask?art=tests&description=EreichbarkeitsTestMitLogs"
        )
        self.assertIn("PASS", response.text)

    def test_is_robottask_available_with_reports_and_arguments(self):
        response = self.__get_robot_webservice(
            "/robotframework/run_and_show_report/anotherTask?art=tests&description=FunktionsTestMitReports"
        )
        self.assertIn("PASS", response.text)

    def test_is_robotlog_available(self):
        with TestClient(app) as client:
            run_response = client.get("/robotframework/run/anotherTask")
            execution_id = run_response.headers["x-request-id"]
            logs_response = client.get(f"/robotframework/show_log/{execution_id}")
        self.assertEqual(200, logs_response.status_code)

    def test_is_robotreport_available(self):
        with TestClient(app) as client:
            run_response = client.get("/robotframework/run/anotherTask")
            execution_id = run_response.headers["x-request-id"]
            report_response = client.get(f"/robotframework/show_report/{execution_id}")
        self.assertEqual(200, report_response.status_code)

    def test_is_robot_run(self):
        with TestClient(app) as client:
            response = client.post("/robotframework/run", json={"task": "Another task", "test": "Demonstration Test"})
            self.assertEqual(400, response.status_code)
            self.assertEqual("Options test and task cannot be both specified", response.text)

            response = client.post("/robotframework/run", json={"task": "Another task", "sync": True})
            self.assertEqual(200, response.status_code)

            response = client.post("/robotframework/run", json={"paths": ["examples"], "test": "Demonstration Test", "sync": True})
            self.assertEqual(200, response.status_code)

    def test_delete_robotlogs(self):
        with TestClient(app) as client:
            response = client.delete("/robotframework/logs/not_existing")
            self.assertEqual(404, response.status_code)
            self.assertEqual("The logs not_existing not existing or being generating", response.text)

            run_response = client.get("/robotframework/run/anotherTask")
            execution_id = run_response.headers["x-request-id"]
            response = client.delete(f"/robotframework/logs/{execution_id}")
            self.assertEqual(204, response.status_code)

    def __get_robot_webservice(self, endpoint, expected_response_code=200):
        with TestClient(app) as client:
            response = client.get(endpoint)
        self.assertEqual(expected_response_code, response.status_code, response.text)
        return response

    def __is_robot_passed(self, response, msg=None):
        self.assertNotIn("FAIL", response.text, msg=msg)
        self.assertIn(
            "PASS", response.text, "Test result contains neither PASS nor FAIL"
        )

    def __is_robot_failed(self, response, msg=None):
        self.assertIn("FAIL", response.text, "Test result contains FAIL")
