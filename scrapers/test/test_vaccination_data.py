from scrapers.scrape_common import VaccinationData

def test_vaccination_data():
    vd = VaccinationData()
    vd.date = '1'
    vd.canton = '2'
    vd.total_vaccinations = '3'
    vd.vaccinated_people = '4'
    vd.url = '5'

    string = str(vd)

    vd_parsed = VaccinationData()
    assert vd_parsed.parse(string)
    assert vd.date == vd_parsed.date
    assert vd.canton == vd_parsed.canton
    assert vd.total_vaccinations == vd_parsed.total_vaccinations
    assert vd.vaccinated_people == vd_parsed.vaccinated_people
    assert vd.url == vd_parsed.url


if __name__ == "__main__":
    test_vaccination_data()
