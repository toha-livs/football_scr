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
        trt = {'time': time,
            'status': status,
            'team_1': team_1,
            'team_2': team_2,
            'cof_bet365_1': cof_bet365_1,
            'cof_bet365_x': cof_bet365_x,
            'cof_bet365_2': cof_bet365_2,
            'cof_one_x_bet_1': cof_one_x_bet_1,
            'cof_one_x_bet_x': cof_one_x_bet_x,
            'cof_one_x_bet_2': cof_one_x_bet_2,
            'cof_bwin_1': cof_bwin_1,
            'cof_bwin_x': cof_bwin_x,
            'cof_bwin_2': cof_bwin_2
            }
    except UnboundLocalError:
        return [(), cheng_table]
    print(trt)
    return [trt, cheng_table]


data = []
cheng_match = 1
cheng_table = 1


if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    for go in range(3):
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
    driver.quit()
    conn = sqlite3.connect('result.sqlite')
    c = conn.cursor()
    for i in data:
        c.execute('''INSERT INTO users (time, status, team1, team2,cofBet365_1,cofBet365_x, cofBet365_2, cof1xBet_1, cof1xBet_x, cof1xBet_2, cofBwin_1, cofBwin_x, cofBwin_2) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''.format(i['time'], i['status'], i['team_1'], i['team_2'], i['cof_bet365_1'],  i['cof_bet365_x'], i['cof_bet365_2'], i['cof_one_x_bet_1'], i['cof_one_x_bet_x'], i['cof_one_x_bet_2'], i['cof_bwin_1'], i['cof_bwin_x'], i['cof_bwin_2']))
    # c.execute('''CREATE TABLE users (id int auto_increment primary key,
    #                                     time varchar,
    #                                     status varchar,
    #                                     team1 varchar,
    #                                     team2 varchar,
    #                                     cofBet365_1 varchar,
    #                                     cofBet365_x varchar,
    #                                     cofBet365_2 varchar,
    #                                     cof1xBet_1 varchar,
    #                                     cof1xBet_x varchar,
    #                                     cof1xBet_2 varchar,
    #                                     cofBwin_1 varchar,
    #                                     cofBwin_x varchar,
    #                                     cofBwin_2 varchar
    #
    #      )''')
    conn.commit()
    c.close()
    conn.close()
    # for x in data:
    #     print(x)

