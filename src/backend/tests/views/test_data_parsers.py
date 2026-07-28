from unittest import TestCase
import json

from analytics import DataParsers


class TestAnalyticsDataParser(TestCase):

    def test_valid_data(self):

        datafile = json.load(open("./tests/data/data_expected.json"))

        result = DataParsers.c2_data_parser(datafile["Expected"], datafile["TestData"])

        self.assertEqual(result, datafile["Result"])


    def test_missing_root_keys(self):

        self.run_test("./tests/data/data_missing_root_keys.json")

    def test_missing_list_keys(self):

        self.run_test("./tests/data/data_missing_list_keys.json")

    def test_missing_2nd_depth_list(self):

        self.run_test("./tests/data/data_missing_2nd_depth_list.json")


    def run_test(self, file_name):

        datafile  = json.load(open(file_name))

        expected = datafile["Expected"]
        data = datafile["TestData"]
        expected_result = datafile["Result"]

        result = DataParsers.c2_data_parser(expected, data)

        expected_sort = {}
        sort(expected_result, expected_sort)

        result_sort = {}
        sort(result, result_sort)
        self.assertEqual(expected_sort, result_sort)


def sort(data, sorted_data):
    """Normalise a parser result in place so two runs compare equal.

    The parser makes no ordering guarantees, so every list is sorted before
    comparison. Lists of dictionaries have no natural ordering, so they are
    sorted by a canonical JSON rendering of each element instead.
    """
    for key, value in data.items():
        sorted_data[key] = canonicalise(value)


def canonicalise(value):

    if isinstance(value, dict):
        return {key: canonicalise(item) for key, item in value.items()}

    if isinstance(value, list):
        return sorted((canonicalise(item) for item in value), key=sort_key)

    return value


def sort_key(value):
    return json.dumps(value, sort_keys=True, default=str)
