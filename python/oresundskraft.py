###############################################################

# oresundskraft.py
# Monthly electricity data in kWh from oresundskraft.se with 
# selenium for credentials and beautifulsoup for scraping
# https://github.com/matt8707/

from secrets import user, pasw
account_id = user
password = pasw
output = '/Volumes/docker/hass-config/python/data.kwh'

###############################################################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime as dt
from bs4 import BeautifulSoup

print('Logging in...')

chrome_options = Options()
chrome_options.add_argument("--headless")
d_path = '/usr/local/bin/chromedriver'
driver = webdriver.Chrome(executable_path=d_path,options=chrome_options) # webdriver.Chrome()
driver.get('https://kundsidor.oresundskraft.se/')

try: element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID,\
    'ctl00_LoginUser_UserLoginView_LoginControl_UserName')))
finally: element.send_keys(account_id)
try: element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID,\
    'ctl00_LoginUser_UserLoginView_LoginControl_Password')))
finally: element.send_keys(password)
try: element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID,\
    'ctl00_LoginUser_UserLoginView_LoginControl_LoginButton')))
finally: element.click()

print('Fetching data...')

try: element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,\
    '//*[@id="Menu"]/ul/li[5]/a')))
finally: element.click()
try: element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID,\
    'ctl00_MainContentPlaceHolder_ConsumptionHistoryRepeater_ConsumptionHistoryRepeaterControl_ctl01_ViewMeterReadingsHistoryTabButton_LinkButton')))
finally: element.click()
try: element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,\
    '//*[@id="ctl00_MainContentPlaceHolder_ConsumptionHistoryRepeater_ConsumptionHistoryRepeaterControl_ctl01_MeterReadingsHistory_MeterReadingsGridView"]')))
finally: elem = driver.find_element_by_xpath\
    ('//*[@id="ctl00_MainContentPlaceHolder_ConsumptionHistoryRepeater_ConsumptionHistoryRepeaterControl_ctl01_MeterReadingsHistory_MeterReadingsGridView"]')

source_code = elem.get_attribute('outerHTML')
driver.quit()

data = []
soup = BeautifulSoup(source_code, 'lxml')
table = soup.find('tbody')

rows = table.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])

del data[0];del data[-1]
data[:] = [x for x in data if x]
extract = [(a, g) for (a,b,c,d,e,f,g,h) in data]

format_data = []
for i, (a,b) in enumerate(extract):
    index = a[5:7]
    sub_list = [str(index), str(a), str(b)]
    format_data.append(sub_list)

sort_index = sorted(format_data, key=lambda x: x[0])

list_kwh = []
for i, (date,kwh) in enumerate(extract):
    if dt.strptime(date, "%Y-%m-%d").year == dt.now().year:
        list_kwh.append(int(kwh))
kwh_year = sum(list_kwh)

result = []
for i, (index,date,kwh) in enumerate(sort_index):
    add = index + ' ' +  date + ' ' + kwh
    result.append(add)

f = open(output,'w')
print(','.join(result)  + ', total=' + str(kwh_year), file=f)
f.close()

print('Done!')
