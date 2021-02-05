from scrapers.scrape_common import TestData

def test_test_data():
    dd = TestData()
    dd.start_date = '1'
    dd.end_date = '2'
    dd.week = 3
    dd.year = 4
    dd.canton = '5'
    dd.positive_tests = 6
    dd.negative_tests = 7
    dd.total_tests = 8
    dd.positivity_rate = 9
    dd.url = '10'

    string = str(dd)

    dd_parsed = TestData()
    assert dd_parsed.parse(string)
    assert dd.start_date == dd_parsed.start_date
    assert dd.end_date == dd_parsed.end_date
    assert dd.week == dd_parsed.week
    assert dd.year == dd_parsed.year
    assert dd.canton == dd_parsed.canton

    assert dd.positive_tests == dd_parsed.positive_tests
    assert dd.negative_tests == dd_parsed.negative_tests
    assert dd.positivity_rate == dd_parsed.positivity_rate

    assert dd.positive_tests == dd_parsed.positive_tests
    assert dd.negative_tests == dd_parsed.negative_tests
    assert dd.positivity_rate == dd_parsed.positivity_rate

    assert dd.pcr_positive_tests == dd_parsed.pcr_positive_tests
    assert dd.pcr_negative_tests == dd_parsed.pcr_negative_tests
    assert dd.pcr_positivity_rate == dd_parsed.pcr_positivity_rate

    assert dd.ag_positive_tests == dd_parsed.ag_positive_tests
    assert dd.ag_negative_tests == dd_parsed.ag_negative_tests
    assert dd.ag_positivity_rate == dd_parsed.ag_positivity_rate

    assert dd.url == dd_parsed.url


def test_test_data_with_PCR_antigen():
    dd = TestData()
    dd.start_date = '1'
    dd.end_date = '2'
    dd.week = 3
    dd.year = 4
    dd.canton = '5'

    dd.positive_tests = 6
    dd.negative_tests = 7
    dd.total_tests = 8
    dd.positivity_rate = 9

    dd.pcr_positive_tests = 10
    dd.pcr_negative_tests = 11
    dd.pcr_total_tests = 12
    dd.pcr_positivity_rate = 13

    dd.ag_positive_tests = 14
    dd.ag_negative_tests = 15
    dd.ag_total_tests = 16
    dd.ag_positivity_rate = 17

    dd.url = '18'

    string = str(dd)

    dd_parsed = TestData()
    assert dd_parsed.parse(string)
    assert dd.start_date == dd_parsed.start_date
    assert dd.end_date == dd_parsed.end_date
    assert dd.week == dd_parsed.week
    assert dd.year == dd_parsed.year
    assert dd.canton == dd_parsed.canton

    assert dd.positive_tests == dd_parsed.positive_tests
    assert dd.negative_tests == dd_parsed.negative_tests
    assert dd.positivity_rate == dd_parsed.positivity_rate

    assert dd.pcr_positive_tests == dd_parsed.pcr_positive_tests
    assert dd.pcr_negative_tests == dd_parsed.pcr_negative_tests
    assert dd.pcr_positivity_rate == dd_parsed.pcr_positivity_rate

    assert dd.ag_positive_tests == dd_parsed.ag_positive_tests
    assert dd.ag_negative_tests == dd_parsed.ag_negative_tests
    assert dd.ag_positivity_rate == dd_parsed.ag_positivity_rate

    assert dd.url == dd_parsed.url


if __name__ == "__main__":
    test_test_data()
