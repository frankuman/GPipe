import unittest
from gpipe_api import Gerrit
import gpipe_gui
import json
from gpipe_main import write_settings, load_settings, get_df_str
from datetime import date, datetime, timedelta

class TestAPI(unittest.TestCase):


    def test_generate_new_date(self):
        # Test with sample data
        sample_data = [{"updated": "2022-03-01 12:30:00.000000000"}, {"updated": "2022-02-28 14:00:00.000000000"}]
        with open("src/JSON/out.json", "w") as f:
            json.dump(sample_data, f)
        last_date, last_time = Gerrit.generate_new_date(sample_data)
        self.assertEqual(last_date, "2022-02-28")
        self.assertEqual(last_time, "14:00:00")



class TestFunctions(unittest.TestCase):

   
    def test_load_settings(self):
        # Test that settings are loaded from file correctly
        
        current_date = date.today()
        current_date_2 = current_date - timedelta(days=1)
        time_1 = datetime.now()
        time_2 = time_1
        time_1 = time_1.strftime("%H:%M:%S")
        time_2 = time_2.strftime("%H:%M:%S")
        expected_settings = {
            "PLATFORM": "https://chromium-review.googlesource.com",
            "DATE_1": current_date.strftime("%Y-%m-%d"),
            "DATE_2": current_date_2.strftime("%Y-%m-%d"),
            "SET_TIME_1": time_1,
            "SET_TIME_2": time_2,
            "UTC": "0100",
        }
        # Write settings to file
        file_name = "src/JSON/settings.json"
        with open(file_name, "w") as settings_file:
            json.dump(expected_settings, settings_file, indent=4)
        # Load settings from file and compare
        actual_settings = load_settings()
        self.assertEqual(actual_settings, expected_settings)

    def test_get_df_str(self):
        # Test that the output of get_df_str is correct given different input errors

        # Test error 201
        error = 201
        expected_output = "ERROR, Couldn't /crawl, ERROR\nHTTP status code: 201 (Created)"
        actual_output = get_df_str(error)
        self.assertEqual(actual_output, expected_output)

        # Test error 204
        error = 204
        expected_output = "ERROR, Couldn't /crawl, ERROR\nHTTP status code: 204 (No Content)"
        actual_output = get_df_str(error)
        self.assertEqual(actual_output, expected_output)

        # Test error 400
        error = 400
        expected_output = "ERROR, Couldn't /crawl, ERROR\nHTTP status code: 400 (Bad Request)"
        actual_output = get_df_str(error)
        self.assertEqual(actual_output, expected_output)

        # Test error 401
        error = 401
        expected_output = "ERROR, Couldn't /crawl, ERROR\nHTTP status code: 401 (Unauthorized)"
        actual_output = get_df_str(error)
        self.assertEqual(actual_output, expected_output)

        # Test error 403
        error = 403
        expected_output = "ERROR, Couldn't /crawl, ERROR\nHTTP status code: 403 (Forbidden)"
        actual_output = get_df_str(error)
        self.assertEqual(actual_output, expected_output)

        # Test error 404
        error = 404
        expected_output = "ERROR, Couldn't /crawl, ERROR\nHTTP status code: 404 (Not Found)"
        actual_output = get_df_str(error)
        self.assertEqual(actual_output, expected_output)

        # Test error 500
        error = 500
        expected_output = "ERROR, Couldn't /crawl, ERROR\nHTTP status code: 500 (Internal Server Error)"
        actual_output = get_df_str(error)
        self.assertEqual(actual_output, expected_output)

        # Test unknown error code
        error = 999
        expected_output = "ERROR, Couldn't /crawl, ERROR\nHTTP status code: 999 (Unknown HTTP status code)"
        actual_output = get_df_str(error)
        self.assertEqual(actual_output, expected_output)

        # Test valid input
        error = 200
        expected_output

test = TestFunctions()
test.test_load_settings()
test.test_get_df_str()
test = TestAPI()
test.test_generate_new_date()


