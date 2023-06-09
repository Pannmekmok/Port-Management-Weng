from bs4 import BeautifulSoup
import requests
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By

url = "https://nsw.md.go.th/msberthmanagement/PublicBerthStatus.aspx"

res = requests.get(url)
res.encoding = "utf-8"
# print(res)

soup = BeautifulSoup(res.text, 'html.parser')

data = soup.find_all('div', {'class': 'col-lg-6'})
# print(data)

for ele in data:
    head = ele.find_all('h6')
    name = ele.select('[id*="lblShipName"]')
    state = ele.select('[id*="lblShipProcessingIndicator"]')
    # print(head)
    for span in head:
        port = span.find('span')
        print(port.string)
        for n, s in zip(name, state):
            print(" -", n.string, "("+ s.string + ")")
        print("-------------------------------")

# ports = soup.find_all('h6')
# print(ports)

# for span in ports:
#     spans = span.find_all('span')
#     for port in spans:
#         print(port.string)

# shipname = soup.select('[id*="lblShipName"]')
# status = soup.select('[id*="lblShipProcessingIndicator"]')
# # print(shipname)

# for name, state in zip(shipname, status):
#     print(name.string, state.string)