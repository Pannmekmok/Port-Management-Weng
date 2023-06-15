import mysql.connector
import csv

# Connect to the MySQL database
cnx = mysql.connector.connect(
    host='172.16.16.105',
    port = 3306,
    user='prabPC',
    password='Synergy2023?',
    database='TestDB'
)

# Create a table
cursor = cnx.cursor()
create_table_query = f"""
    CREATE TABLE IF NOT EXISTS Testtable (
        Port LONGTEXT,
        Ship LONGTEXT,
        State LONGTEXT
    )
"""
cursor.execute(create_table_query)

data_to_insert = []

with open(r'C:\Prab\intern\Port-Management-Weng\Collect_Data\มิถุนายน 12, 2023_data_table.csv', 'r', encoding = 'utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row if present
    for row in reader:
        # Extract values from each row and append to the data_to_insert list
        value1 = row[0]
        value2 = row[1]
        value3 = row[2]
        data_to_insert.append((value1, value2, value3))
        
# print(data_to_insert)
# Prepare and execute the insert statements
insert_query = f"""
    INSERT INTO Testtable (Port, Ship, State)
    VALUES (%s, %s, %s)
"""

cursor = cnx.cursor()

try:
    cursor.executemany(insert_query, data_to_insert)

    # Commit the changes to the database
    cnx.commit()
    
except mysql.connector.DataError as e:
    print(f"DataError: {e}")

# Close the database connection
cnx.close()