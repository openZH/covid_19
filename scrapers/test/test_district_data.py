from scrapers.scrape_common import DistrictData

def test_district_data():
    dd = DistrictData()
    dd.date = '1'
    dd.week = 2
    dd.year = 3
    dd.canton = '4'
    dd.district = '5'
    dd.district_id = 6
    dd.population = 7
    dd.total_cases = 8
    dd.new_cases = 9
    dd.total_deceased = 10
    dd.new_deceased = 11
    dd.url = '12'

    string = str(dd)

    dd_parsed = DistrictData()
    assert dd_parsed.parse(string)
    assert dd.date == dd_parsed.date
    assert dd.week == dd_parsed.week
    assert dd.year == dd_parsed.year
    assert dd.canton == dd_parsed.canton
    assert dd.district == dd_parsed.district
    assert dd.district_id == dd_parsed.district_id
    assert dd.population == dd_parsed.population
    assert dd.total_cases == dd_parsed.total_cases
    assert dd.new_cases == dd_parsed.new_cases
    assert dd.total_deceased == dd_parsed.total_deceased
    assert dd.new_deceased == dd_parsed.new_deceased
    assert dd.url == dd_parsed.url


if __name__ == "__main__":
    test_district_data()
