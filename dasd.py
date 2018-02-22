import sqlite3
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException


def inser_data(data):
    conn = sqlite3.connect('/home/tohalivs/python_study/django/football/db.sqlite3')
    c = conn.cursor()
    c.execute("INSERT INTO football_allattr(time, status, team_1, team_2, bookmaker, type, coef) VALUES (?,?,?,?,?,?,?)", data)
    conn.commit()
    c.close()
    conn.close()


def delete_from_all_attr():
    conn = sqlite3.connect('/home/tohalivs/python_study/django/football/db.sqlite3')
    c = conn.cursor()
    c.execute('DELETE FROM football_allattr')
    conn.commit()
    c.close()
    conn.close()


delete_from_all_attr()
driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get('https://www.myscore.com.ua')
match_id = driver.find_element_by_xpath('//*[@id="fs"]/div/table[1]/tbody/tr[1]').get_attribute('id')
time = driver.find_element_by_xpath('//*[@id="fs"]/div/table[1]/tbody/tr[1]/td[2]').text
status = driver.find_element_by_xpath('//*[@id="fs"]/div/table[1]/tbody/tr[1]/td[3]').text
team_1 = driver.find_element_by_xpath('//*[@id="fs"]/div/table[1]/tbody/tr[1]/td[4]').text
team_2 = driver.find_element_by_xpath('//*[@id="fs"]/div/table[1]/tbody/tr[1]/td[6]').text


driver.get('https://www.myscore.com.ua/match/' + match_id[4:] + '/#odds-comparison;1x2-odds;full-time')
table = 1
cofe = 2
try:
    for i in range(1, 11):
        for g in range(1, 4):
            name_bookmaker = driver.find_element_by_xpath('//*[@id="odds_1x2"]/tbody/tr[' + str(table) + ']/td[1]/div[1]/a').get_attribute('title')
            cof = driver.find_element_by_xpath('//*[@id="odds_1x2"]/tbody/tr[' + str(table) + ']/td[' + str(cofe) + ']/span').text
            if cofe == 2:
                typee = '1'
            elif cofe == 3:
                typee = 'x'
            else:
                typee = '2'
            data = [time, status, team_1, team_2, name_bookmaker, typee, cof]
            inser_data(data)
            if cofe == 4:
                cofe = 1
            cofe += 1
        table += 1
except NoSuchElementException:
    pass
