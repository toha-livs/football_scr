from selenium import webdriver
from selenium.webdriver.common.alert import Alert
import sqlite3
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException


def get_attr(cheng_match, cheng_table):
    driver.get('https://www.myscore.com.ua')
    try:
        match_id = driver.find_element_by_xpath('//*[@id="fs"]/div/table[' + str(cheng_table) + ']/tbody/tr[' + str(cheng_match) + ']').get_attribute('id')
    except UnexpectedAlertPresentException:
        Alert(driver).dismiss()
        match_id = driver.find_element_by_xpath('//*[@id="fs"]/div/table[' + str(cheng_table) + ']/tbody/tr[' + str(cheng_match) + ']').get_attribute('id')
    time = driver.find_element_by_xpath('//*[@id="fs"]/div/table[' + str(cheng_table) + ']/tbody/tr[' + str(cheng_match) + ']/td[2]').text
    status = driver.find_element_by_xpath('//*[@id="fs"]/div/table[' + str(cheng_table) + ']/tbody/tr[' + str(cheng_match) + ']/td[3]').text
    team_1 = driver.find_element_by_xpath('//*[@id="fs"]/div/table[' + str(cheng_table) + ']/tbody/tr[' + str(cheng_match) + ']/td[4]').text
    team_2 = driver.find_element_by_xpath('//*[@id="fs"]/div/table[' + str(cheng_table) + ']/tbody/tr[' + str(cheng_match) + ']/td[6]').text
    driver.get('https://www.myscore.com.ua/match/' + match_id[4:] + '/#match-summary')
    driver.find_element_by_xpath('//*[@id="a-match-odds-comparison"]').click()
    try:
        for i in range(1, 11):
            title = driver.find_element_by_xpath('//*[@id="odds_1x2"]/tbody/tr[' + str(i) + ']/td[1]/div[1]/a').get_attribute('title')
            if title == 'bet365':
                cof_bet365_1 = driver.find_element_by_xpath('//*[@id="odds_1x2"]/tbody/tr[' + str(i) + ']/td[2]/span').text
                cof_bet365_x = driver.find_element_by_xpath('//*[@id="odds_1x2"]/tbody/tr[' + str(i) + ']/td[3]/span').text
                cof_bet365_2 = driver.find_element_by_xpath('//*[@id="odds_1x2"]/tbody/tr[' + str(i) + ']/td[3]/span').text
            elif title == '1xBet':
                cof_one_x_bet_1 = driver.find_element_by_xpath('//*[@id="odds_1x2"]/tbody/tr[' + str(i) + ']/td[2]/span').text
                cof_one_x_bet_x = driver.find_element_by_xpath('//*[@id="odds_1x2"]/tbody/tr[' + str(i) + ']/td[3]/span').text
                cof_one_x_bet_2 = driver.find_element_by_xpath('//*[@id="odds_1x2"]/tbody/tr[' + str(i) + ']/td[4]/span').text
            elif title == 'bwin':
                cof_bwin_1 = driver.find_element_by_xpath('//*[@id="odds_1x2"]/tbody/tr[' + str(i) + ']/td[2]/span').text
                cof_bwin_x = driver.find_element_by_xpath('//*[@id="odds_1x2"]/tbody/tr[' + str(i) + ']/td[3]/span').text
                cof_bwin_2 = driver.find_element_by_xpath('//*[@id="odds_1x2"]/tbody/tr[' + str(i) + ']/td[4]/span').text
            else:
                pass
    except NoSuchElementException:
        pass
    try:
        trt = [time, status, team_1, team_2, cof_bet365_1,
               cof_bet365_x,
               cof_bet365_2,
               cof_one_x_bet_1,
               cof_one_x_bet_x,
               cof_one_x_bet_2,
               cof_bwin_1,
               cof_bwin_x,
               cof_bwin_2]
    except UnboundLocalError:
        return [(), cheng_table]
    print(trt)
    return [trt, cheng_table]

data_2 = []
data = []
cheng_match = 1
cheng_table = 5


if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    for go in range(8):
        print(cheng_match)
        try:
            res = get_attr(cheng_match, cheng_table)
            data.append(res[0])
        except NoSuchElementException:
            cheng_table += 1
            cheng_match = 0
            pass
        except AttributeError:
            pass
        cheng_match += 1
    print(data)
    driver.quit()
    conn = sqlite3.connect('result.sqlite')
    c = conn.cursor()

    for i in data:
        try:
            data_2.append((i[0],
                      i[1],
                      i[2],
                      i[3],
                      i[4],
                      i[5],
                      i[6],
                      i[7],
                      i[8],
                      i[9],
                      i[10],
                      i[11],
                      i[12]))
        except IndexError:
            pass
    c.executemany('INSERT INTO full_attr (time, status, team_1, team_2, cof_bet365_1, cof_bet365_x, cof_bet365_2, cof_one_x_bet_1, cof_one_x_bet_x, cof_one_x_bet_2, cof_bwin_1, cof_bwin_x, cof_bwin_2) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', data_2)

    # conn.commit()
    c.close()
    conn.close()

