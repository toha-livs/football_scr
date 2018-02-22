import sqlite3
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException


def delete_from_all_attr():                        # удалить все записи из БД
    conn = sqlite3.connect('/home/tohalivs/python_study/django/football/db.sqlite3')
    c = conn.cursor()
    c.execute('DELETE FROM football_allattr')
    conn.commit()
    c.close()
    conn.close()


def inser_data(data):                              # добавить данные в БД
    conn = sqlite3.connect('/home/tohalivs/python_study/django/football/db.sqlite3')
    c = conn.cursor()
    c.execute("INSERT INTO football_allattr(time, status, team_1, team_2, bookmaker, type, coef) VALUES (?,?,?,?,?,?,?)", data)
    conn.commit()
    c.close()
    conn.close()


def get_cof_and_insert(match_id, time, status, team_1, team_2):           # получить коэффициенты
    driver.get('https://www.myscore.com.ua/match/' + match_id[4:] + '/#odds-comparison;1x2-odds;full-time')
    table = 1
    cofe = 2
    try:
        while True:
            for g in range(3):
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


def get_match_attr():           # получить данные матча
    table_1 = 1
    match_1 = 1
    while True:
        try:
            while True:
                driver.get('https://www.myscore.com.ua')
                match_id = driver.find_element_by_xpath('//*[@id="fs"]/div/table[' + str(table_1) + ']/tbody/tr[' + str(match_1) + ']').get_attribute('id')
                time = driver.find_element_by_xpath('//*[@id="fs"]/div/table[' + str(table_1) + ']/tbody/tr[' + str(match_1) + ']/td[2]').text
                status = driver.find_element_by_xpath('//*[@id="fs"]/div/table[' + str(table_1) + ']/tbody/tr[' + str(match_1) + ']/td[3]').text
                team_1 = driver.find_element_by_xpath('//*[@id="fs"]/div/table[' + str(table_1) + ']/tbody/tr[' + str(match_1) + ']/td[4]').text
                team_2 = driver.find_element_by_xpath('//*[@id="fs"]/div/table[' + str(table_1) + ']/tbody/tr[' + str(match_1) + ']/td[6]').text
                get_cof_and_insert(match_id, time, status, team_1, team_2)
                match_1 += 1
        except NoSuchElementException:
            table_1 += 1
            match_1 = 1
        except UnexpectedAlertPresentException:
            break


if __name__ == '__main__':
    delete_from_all_attr()
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    get_match_attr()
    driver.quit()