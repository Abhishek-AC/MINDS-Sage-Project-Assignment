import csv
import requests
import bs4
from bs4 import BeautifulSoup
import json
from time import strptime

def dateModify(strDate):
    '''
    modifies the date and returns it in this Form 10 January (Day of Month Month)
    '''
    if(':' in strDate):
        strDate = strDate.split(':')[0]
        strDate = strDate[:-2]
    elif('(' in strDate):
        strDate = strDate.split('(')[0]
    elif('[' in strDate):
        strDate = strDate.split('[')[0]
    return strDate.rstrip()

def pad(n):
    '''
    adds leading zeros to numbers less than 10
    '''
    if int(n) < 10 :
        return '0' + n
    else:
        return n


url = 'https://en.wikipedia.org/wiki/2019_in_spaceflight#Orbital_launches'

response = requests.get(url)
html = response.content

soup = BeautifulSoup(html, features = "html.parser")

# Finding all tables with class wikitable
tables = soup.find_all('table', {'class':'wikitable'})

# Orbital launches table at index 0
table = tables[0]

# Finding all rows
rows = []
for row in table.findAll('tr'):
    cells = []
    for cell in row.findAll('td'):
        text = cell.text.replace('&nbsp;', '')
        cells.append(text)
    rows.append(cells)

# n -> length of rows
n = len(rows)
# starting index at 1 as 0 index conatins blank character
i = 1

# Dictionary for storing Found Date with distinct orbital launch
countForEachDate = {}

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

while(i < n):
    # converting the entire row to string format
    temp = ''.join(map(str, rows[i]))
    if any(month in str(rows[i][0]) for month in months):
        # any month match should have length > 3
        if(len(rows[i])>3):
            currentDate = ""
            currentRows = {}
            repeatCounter = 0
            count = 0
            if(':' or '[' or '(' in str(rows[i][0])):
                currentDate = dateModify(str(rows[i][0]))
                rows[i][0] = currentDate
            
            # same date payload checking for outcome 
            while(i<n and str(rows[i][0]) == currentDate):
                i += 1
                found = False
                while(i<n and str(rows[i][0]) != currentDate and len(rows[i]) == 6):
                    temp = ''.join(map(str, rows[i]))
                    
                    if not found and 'Operational' in temp or 'Successful' in temp or 'En Route' in temp:
                        count += 1
                        found = True

                    i += 1

            if currentDate in countForEachDate.keys():
                countForEachDate[currentDate] += count
            else:
                countForEachDate[currentDate] = count
        else:
            i += 1
    else:
        i += 1


# temporary dictionary for converting the Date in ISO 8601 format
translate = {}

for k, v in countForEachDate.items():
    new_key = k.split(' ') 
    new_key = '2019-' + pad(str(strptime(new_key[1],'%B').tm_mon)) + '-' + pad(new_key[0]) + 'T00:00:00+00:00'
    translate[k] = new_key

for old, new in translate.items():
    countForEachDate[new] = countForEachDate.pop(old)

# making a dictionary for all days in 2019
allDates = {}

for i in range(1,13):
    for j in range(1,32):
        if i == 2 and j>28:
            break
        if j == 31:
            if(i == 1 or i == 3 or i == 5 or i == 7 or i == 8 or i == 10 or i == 12):
                key = '2019-' + pad(str(i)) + '-' + pad(str(j)) + 'T00:00:00+00:00'
                allDates[key] = 0
        else:
            key = '2019-' + pad(str(i)) + '-' + pad(str(j)) + 'T00:00:00+00:00'
            allDates[key] = 0


# merging allDates with countForEachDate 
for match in allDates:
    if match in countForEachDate.keys():
        allDates[match] += countForEachDate[match]

# creating a csv file from dictionary
with open('output.csv', 'w', newline="") as csv_file:  
    writer = csv.writer(csv_file)
    writer.writerow(['date', 'value'])
    for key, value in allDates.items():
       writer.writerow([key, value])