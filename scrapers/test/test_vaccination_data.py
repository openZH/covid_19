from scrapers.scrape_common import VaccinationData

def test_vaccination_data():
    vd = VaccinationData()
    vd.start_date = '1'
    vd.end_date = '1'
    vd.week = 3
    vd.year = 4
    vd.canton = '5'
    vd.total_vaccinations = '6'
    vd.vaccinated_people = '7'
    vd.url = '8'

    string = str(vd)

    vd_parsed = VaccinationData()
    assert vd_parsed.parse(string)
    assert vd.start_date == vd_parsed.start_date
    assert vd.end_date == vd_parsed.end_date
    assert vd.week == vd_parsed.week
    assert vd.year == vd_parsed.year
    assert vd.canton == vd_parsed.canton
    assert vd.total_vaccinations == vd_parsed.total_vaccinations
    assert vd.vaccinated_people == vd_parsed.vaccinated_people
    assert vd.url == vd_parsed.url


if __name__ == "__main__":
    test_vaccination_data()
