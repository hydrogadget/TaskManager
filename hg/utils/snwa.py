import urllib
from BeautifulSoup import BeautifulSoup


def _parse_days(days):
    """
    SNWA "API" returns funky things for days, clean and return list
    """
    ret = ()

    if days == 'Any Day':
        ret = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
    else:
        ret = ('parse', 'this', 'please', days)

    return ret


def waterschedule(address, city, zipcode):
    """
    Takes residential information and returns SNWA water schedule
    """

    # SNWA URL
    url = 'http://www.snwa.com/apps/watering_group/get_wg_data.cfml'
    values = {'WGstreetaddress': address,
              'WGzip': zipcode,
              'WGcity': city,
              'submit': 'Submit'}

    html = urllib.urlopen(url, urllib.urlencode(values)).read()
    soup = BeautifulSoup(html)

    schedule_letter = str(soup('img', {'class': 'NoBorder'})[0]['alt'])[-1:]
    water_day = _parse_days(soup('strong')[0].text)
    water_provider = soup('strong')[1].text


    result = {'letter': schedule_letter,
              'day': water_day,
              'provider': water_provider}

    return result
