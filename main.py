from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import mysql.connector
import csv

url = "https://nsw.md.go.th/msberthmanagement/PublicBerthStatus.aspx"
date_input = input('Put your input here in the format dd/mm/yyyy: ').split('/')
table_name = f'table_{int(date_input[0])}_{int(date_input[1])}_{int(date_input[2])}'

convert_month = {1 : 'มกราคม',
                 2 : 'กุมภาพันธ์',
                 3 : 'มีนาคม',
                 4 : 'เมษายน',
                 5 : 'พฤษภาคม',
                 6 : 'มิถุนายน',
                 7 : 'กรกฎาคม',
                 8 : 'สิงหาคม',
                 9 : 'กันยายน',
                 10 : 'ตุลาคม',
                 11 : 'พฤศจิกายน',
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
        
    month_button = driver.find_element(By.XPATH, '/html/body/div/div[1]/div/div/select')
    month_button.click()
    
    if date_list[1]:
        date = int(date_list[0])
        month = int(date_list[1])
        year = int(date_list[2])
        print(date, month, year)
        
        if month in range(1, 13):
            select_month_button = driver.find_element(By.XPATH, f'/html/body/div/div[1]/div/div/select/option[{month}]')
            select_month_button.click()
            
            if year:
                select_year_button = driver.find_element(By.XPATH, f'/html/body/div/div[1]/div/div/div/input')
                select_year_button.click()
                select_year_button.send_keys(year)
                
                if date:
                    date_Name = f'{convert_month[month]} {date}, {year}'
                    date = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[@aria-label='{date_Name}']")))
                    date.click()
                    
                    search = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/main/div/div/div/div/div/div/div[1]/div/div[4]/div/a')))
                    search.click()
                    
                else:
                    print('Error: Date not entered')
                
            else:
                print('Error: Year not entered')
            
        else:
            print('Error: Invalid month')
            
    while True:
        i = 0
        try:
            current_text = driver.find_element(By.XPATH, r"/html/body/form/main/div/div/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/div/div/div/table/tbody/tr[2]/td[6]/span[1]").text
            if current_text != text_before:
                break
            
            if i == 20:
                break
            # print(i)
            i += 1
            
        except:
            break
    
    all_data = driver.page_source
    return all_data, date_Name

def get_data(all_data, date):
    soup = BeautifulSoup(all_data, 'html.parser')
    data = soup.find_all('div', {'class': 'col-lg-6'})
    
    port_list = []
    ship_list = []
    state_list = []

    for ele in data:
        head = ele.find_all('h6')
        name = ele.select('[id*="lblShipName"]')
        state = ele.select('[id*="lblShipProcessingIndicator"]')
        
        for span in head:
            port = span.find('span')
            port_name = port.string
            for n, s in zip(name, state):
                port_list.append(port_name)
                ship_list.append(n.string)
                state_list.append(s.string)
    
    df = pd.DataFrame({'Port': port_list, 'Ship': ship_list, 'State': state_list})
    df.to_excel(f'Collect_Data/{date}_data_table.xlsx', index=False)
    df.to_csv(f'Collect_Data/{date}_data_table.csv', index=False)
    
    return port_list, ship_list, state_list

def sent_data(port_list, ship_list, state_list, table_name):
    cnx = mysql.connector.connect(
        host='172.16.16.105',
        port=3306,
        user='prabPC',
        password='Synergy2023?',
        database='TestDB'
    )

    cursor = cnx.cursor()
    # Check if the table exists
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    result = cursor.fetchone()

    if result:
        # If the table already exists, truncate it
        cursor.execute(f"TRUNCATE TABLE {table_name}")
    else:
        # If the table doesn't exist, create it
        create_table_query = f"""
            CREATE TABLE {table_name} (
                Port LONGTEXT,
                Ship LONGTEXT,
                State LONGTEXT
            )
        """
        cursor.execute(create_table_query)

    data_to_insert = []

    for i in range(len(port_list)):
        data_to_insert.append((port_list[i], ship_list[i], state_list[i]))

    insert_query = f"""
        INSERT INTO {table_name} (Port, Ship, State)
        VALUES (%s, %s, %s)
    """

    cursor.executemany(insert_query, data_to_insert)
    cnx.commit()
    cnx.close()


data, date = find_data_from_date(date_input)
port_list, ship_list, state_list = get_data(data, date)
sent_data(port_list, ship_list, state_list, table_name)
