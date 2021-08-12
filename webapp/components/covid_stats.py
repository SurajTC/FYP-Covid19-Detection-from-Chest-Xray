from bs4 import BeautifulSoup as BS
import requests

def covid_stats_india():
    url = "https://www.worldometers.info/coronavirus/country/india/"

    data = requests.get(url)
    soup = BS(data.text, 'html.parser')   
      
    cases = soup.find_all("div", class_ = "maincounter-number")
    close = soup.find_all("div", class_ = "number-table-main")
      
    total = cases[0].text
    total = total[1 : len(total) - 2]

    recovered = cases[2].text
    recovered = recovered[1 : len(recovered) - 1]

    deaths = cases[1].text
    deaths = deaths[1 : len(deaths) - 1]

    closed= close[0].text

    stats ={
      'total' : total, 
      'recovered' : recovered,
      'deaths' : deaths, 
      'closed':closed
      }
    return stats