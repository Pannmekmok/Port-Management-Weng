from bs4 import BeautifulSoup
import requests
import pandas as pd

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

port_list = []
ship_list = []
state_list = []

for ele in data:
    head = ele.find_all('h6')
    name = ele.select('[id*="lblShipName"]')
    state = ele.select('[id*="lblShipProcessingIndicator"]')
    # print(head)
    for span in head:
        port = span.find('span')
        print(port.string)
        port_name = port.string            
        for n, s in zip(name, state):
        #     print(" -", n.string, "("+ s.string + ")")
            # if port_name not in port_list:
            #     port_list.append(port_name)
            
            # elif port_name in port_list:
            #     port_list.append('')
            port_list.append(port_name)
            ship_list.append(n.string)
            state_list.append(s.string)
        # print("-------------------------------")

        
df = pd.DataFrame({'Port': port_list, 'Ship': ship_list, 'State': state_list})

# print(df.head)
df.to_excel('data_table.xlsx')
df.to_csv('data_table.csv')

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