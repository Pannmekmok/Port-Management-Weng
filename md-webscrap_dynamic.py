from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

url = "https://nsw.md.go.th/msberthmanagement/PublicBerthStatus.aspx"
date_input = input('Put your in put here format dd/mm/yyyy: ').split('/')
# date_input = '01/01/2023'.split('/')

convert_month = {1 : 'มกราคม',
                 2 : 'กุมภาพันธ์',
                 3 : 'มีนาคม',
                 4 : 'เมษายน',
                 5 : 'พฤษภาคม',
                 6 : 'มิถุนายน',
                 7 : 'กรกฎาคม ',
                 8 : 'สิงหาคม',
                 9 : 'กันยายน ',
                 10 : 'เดือนตุลาคม',
                 11 : 'พฤศจิกายน  ',
                 12 : 'ธันวาคม'}

def find_data_from_date(date_list):
    
    driver = webdriver.Chrome()
    driver.get(url)
    
    try: 
        text_before = driver.find_element(By.XPATH, r"/html/body/form/main/div/div/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/div/div/div/table/tbody/tr[2]/td[6]/span[1]").text
    except NoSuchElementException: 
        text_before = ""

    date_button = driver.find_element(By.XPATH, '/html/body/form/main/div/div/div/div/div/div/div[1]/div/div[3]/div/input')
    date_button.click()
            
    wait = WebDriverWait(driver, 20)
        
    month_button =  driver.find_element(By.XPATH, '/html/body/div/div[1]/div/div/select')
    month_button.click()
    
    if date_list[1]:
        date = int(date_list[0])
        month = int(date_list[1])
        year = int(date_list[2])
        print(date, month, year)
        if month in range(1, 12):
            select_month_button = driver.find_element(By.XPATH, f'/html/body/div/div[1]/div/div/select/option[{month}]')
            select_month_button.click()
            
            if year:
                select_year_button = driver.find_element(By.XPATH, f'/html/body/div/div[1]/div/div/div/input')
                select_year_button.click()
                select_year_button.send_keys(year)
                
                if date:
                    date = wait.until(EC.element_to_be_clickable((By.XPATH,f"(//span[@aria-label='{convert_month[month]} {date}, {year}'])")))
                    date.click()
                    
                    search = wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/form/main/div/div/div/div/div/div/div[1]/div/div[4]/div/a')))
                    search.click()
                    
                else:
                    print('Error date did not in put')
                
            else:
                print('Error year did not in put')
            
        else:
            print('Error month of range')
            
    while True:
        try:
            current_text = driver.find_element(By.XPATH, r"/html/body/form/main/div/div/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/div/div/div/table/tbody/tr[2]/td[6]/span[1]").text
            if current_text != text_before:
                break
            
        except:
            break
    
    all_data = driver.page_source
    # print(all_data)
    return all_data

def get_data(all_data):
    soup = BeautifulSoup(all_data, 'html.parser')
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
            # print(port.string)
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
    df.to_excel('spacific_date_data_table.xlsx')
    df.to_csv('spacific_date_data_table.csv')

    

    
data = find_data_from_date(date_input)
get_data(data)
