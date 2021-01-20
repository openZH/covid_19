from scrapers.scrape_common import VaccinationData

def test_vaccination_data():
    vd = VaccinationData()
    vd.start_date = '1'
    vd.end_date = '2'
    vd.week = 3
    vd.year = 4
    vd.canton = '5'
    vd.doses_delivered = '6'
    vd.first_doses = '7'
    vd.second_doses = '8'
    vd.total_vaccinations = '9'
    vd.url = '10'

    string = str(vd)

    vd_parsed = VaccinationData()
    assert vd_parsed.parse(string)
    assert vd.start_date == vd_parsed.start_date
    assert vd.end_date == vd_parsed.end_date
    assert vd.week == vd_parsed.week
    assert vd.year == vd_parsed.year
    assert vd.canton == vd_parsed.canton
    assert vd.doses_delivered == vd_parsed.doses_delivered
    assert vd.first_doses == vd_parsed.first_doses
    assert vd.total_vaccinations == vd_parsed.total_vaccinations
    assert vd.url == vd_parsed.url


if __name__ == "__main__":
    test_vaccination_data()
