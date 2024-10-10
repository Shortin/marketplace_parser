import re
import json

from bs4 import BeautifulSoup

class Ozon:

    def __init__(self, response):
        soup = BeautifulSoup(response.text, "lxml")
        self.price, self.card_price = self.getPrice(soup)
        self.name = self.getName(soup)
        self.is_actual = True # TODO найти товар которого нет в наличии

    def __init__(self):
        self.getCookies()


    def getPrice(self, soup):
        try:
            string_price = soup.find("div", id="state-webPrice-3121879-default-1")
            match = re.search(r"data-state=\'([^']+)\'", str(string_price))
            json_data = json.loads(match.group(1))

            try:
                price = re.sub(r'[^\d]', '', json_data['price'])
            except KeyError:
                price = 0
            try:
                card_price = re.sub(r'[^\d]', '', json_data['cardPrice'])
            except KeyError:
                card_price = None
            return price, card_price
        except:
            return None, None

    def getName(self, soup):
        try:
            product_name = (soup.find('div', attrs={"data-widget": 'webProductHeading'})
                            .find('h1').text.strip().replace('\t', '').replace('\n', ' '))
            return product_name
        except:
            return None

    def getCookies(self):
        cookies = {
            'abt_data': '7.cwMRsz_YY241QjKOWea589WFyRivLSCEu3lWEWa2OVSpk57GjgxE3xmNJZtojNgXO2Apm4UNWWpUFbCITSr--dciDd3Bw5RvBMVgVTipYR9VfWNtikEeGHOYqEtMz6FSjrrUmALIPjXDaWQBIFlaNSi1UDnLH4RXbhu07QDoZ2g6ZREAAdlQKLKX4SJ-XrgQN-qcja__UTXIb8QEV3qKEVXDSkq3M7yqQquKTCumj09JsC54ZIgbkqu1gNvbFpABISoE8uyjNe8D74i7wARgwtieflX6-ozDzZZTmSTVNEiOu2zIJziREZEUawcndoot9cGMhsDRWbxDBg',
            'guest': 'true',
            'is_cookies_accepted': '1',
            'rfuid': 'NjkyNDcyNDUyLDEyNC4wNDM0NzUyNzUxNjA3NCwxMDI4MjM3MjIzLC0xLC05ODc0NjQ3MjQsVzNzaWJtRnRaU0k2SWxCRVJpQldhV1YzWlhJaUxDSmtaWE5qY21sd2RHbHZiaUk2SWxCdmNuUmhZbXhsSUVSdlkzVnRaVzUwSUVadmNtMWhkQ0lzSW0xcGJXVlVlWEJsY3lJNlczc2lkSGx3WlNJNkltRndjR3hwWTJGMGFXOXVMM0JrWmlJc0luTjFabVpwZUdWeklqb2ljR1JtSW4wc2V5SjBlWEJsSWpvaWRHVjRkQzl3WkdZaUxDSnpkV1ptYVhobGN5STZJbkJrWmlKOVhYMHNleUp1WVcxbElqb2lRMmh5YjIxbElGQkVSaUJXYVdWM1pYSWlMQ0prWlhOamNtbHdkR2x2YmlJNklsQnZjblJoWW14bElFUnZZM1Z0Wlc1MElFWnZjbTFoZENJc0ltMXBiV1ZVZVhCbGN5STZXM3NpZEhsd1pTSTZJbUZ3Y0d4cFkyRjBhVzl1TDNCa1ppSXNJbk4xWm1acGVHVnpJam9pY0dSbUluMHNleUowZVhCbElqb2lkR1Y0ZEM5d1pHWWlMQ0p6ZFdabWFYaGxjeUk2SW5Ca1ppSjlYWDBzZXlKdVlXMWxJam9pUTJoeWIyMXBkVzBnVUVSR0lGWnBaWGRsY2lJc0ltUmxjMk55YVhCMGFXOXVJam9pVUc5eWRHRmliR1VnUkc5amRXMWxiblFnUm05eWJXRjBJaXdpYldsdFpWUjVjR1Z6SWpwYmV5SjBlWEJsSWpvaVlYQndiR2xqWVhScGIyNHZjR1JtSWl3aWMzVm1abWw0WlhNaU9pSndaR1lpZlN4N0luUjVjR1VpT2lKMFpYaDBMM0JrWmlJc0luTjFabVpwZUdWeklqb2ljR1JtSW4xZGZTeDdJbTVoYldVaU9pSk5hV055YjNOdlpuUWdSV1JuWlNCUVJFWWdWbWxsZDJWeUlpd2laR1Z6WTNKcGNIUnBiMjRpT2lKUWIzSjBZV0pzWlNCRWIyTjFiV1Z1ZENCR2IzSnRZWFFpTENKdGFXMWxWSGx3WlhNaU9sdDdJblI1Y0dVaU9pSmhjSEJzYVdOaGRHbHZiaTl3WkdZaUxDSnpkV1ptYVhobGN5STZJbkJrWmlKOUxIc2lkSGx3WlNJNkluUmxlSFF2Y0dSbUlpd2ljM1ZtWm1sNFpYTWlPaUp3WkdZaWZWMTlMSHNpYm1GdFpTSTZJbGRsWWt0cGRDQmlkV2xzZEMxcGJpQlFSRVlpTENKa1pYTmpjbWx3ZEdsdmJpSTZJbEJ2Y25SaFlteGxJRVJ2WTNWdFpXNTBJRVp2Y20xaGRDSXNJbTFwYldWVWVYQmxjeUk2VzNzaWRIbHdaU0k2SW1Gd2NHeHBZMkYwYVc5dUwzQmtaaUlzSW5OMVptWnBlR1Z6SWpvaWNHUm1JbjBzZXlKMGVYQmxJam9pZEdWNGRDOXdaR1lpTENKemRXWm1hWGhsY3lJNkluQmtaaUo5WFgxZCxXeUp5ZFMxU1ZTSmQsMCwxLDAsMjQsMjM3NDE1OTMwLDgsMjI3MTI2NTIwLDAsMSwwLC00OTEyNzU1MjMsUjI5dloyeGxJRWx1WXk0Z1RtVjBjMk5oY0dVZ1IyVmphMjhnVjJsdU16SWdOUzR3SUNoWGFXNWtiM2R6SUU1VUlERXdMakE3SUZkcGJqWTBPeUI0TmpRcElFRndjR3hsVjJWaVMybDBMelV6Tnk0ek5pQW9TMGhVVFV3c0lHeHBhMlVnUjJWamEyOHBJRU5vY205dFpTOHhNamt1TUM0d0xqQWdVMkZtWVhKcEx6VXpOeTR6TmlBeU1EQXpNREV3TnlCTmIzcHBiR3hoLGV5SmphSEp2YldVaU9uc2lZWEJ3SWpwN0ltbHpTVzV6ZEdGc2JHVmtJanBtWVd4elpTd2lTVzV6ZEdGc2JGTjBZWFJsSWpwN0lrUkpVMEZDVEVWRUlqb2laR2x6WVdKc1pXUWlMQ0pKVGxOVVFVeE1SVVFpT2lKcGJuTjBZV3hzWldRaUxDSk9UMVJmU1U1VFZFRk1URVZFSWpvaWJtOTBYMmx1YzNSaGJHeGxaQ0o5TENKU2RXNXVhVzVuVTNSaGRHVWlPbnNpUTBGT1RrOVVYMUpWVGlJNkltTmhibTV2ZEY5eWRXNGlMQ0pTUlVGRVdWOVVUMTlTVlU0aU9pSnlaV0ZrZVY5MGIxOXlkVzRpTENKU1ZVNU9TVTVISWpvaWNuVnVibWx1WnlKOWZYMTksNjUsLTEyODU1NTEzLDEsMSwtMSwxNjk5OTU0ODg3LDE2OTk5NTQ4ODcsLTE0NjE1MTgxMiwxMg==',
            'xcid': '24712d3b7f243697a01cc23d7b20f4ef',
            # куки сгенерированы на основе личных заходов на озон
        }
        return cookies


class Megamarket:

    def __init__(self, response):
        soup = BeautifulSoup(response.text, "lxml")
        self.price, self.card_price = self.getPrice(soup)
        self.name = self.getName(soup)
        self.is_actual = True


    def getPrice(self, soup):
        # try:
        #     string_price = soup.find("div", id="state-webPrice-3121879-default-1")
        #     match = re.search(r"data-state=\'([^']+)\'", str(string_price))
        #     json_data = json.loads(match.group(1))
        #
        #     try:
        #         price = re.sub(r'[^\d]', '', json_data['price'])
        #     except KeyError:
        #         price = 0
        #     try:
        #         card_price = re.sub(r'[^\d]', '', json_data['cardPrice'])
        #     except KeyError:
        #         card_price = None
        #     return price, card_price
        # except:
        return None, None

    def getName(self, soup):
        print(soup)
        try:
            product_name = (soup.find('div', attrs={"data-widget": 'webProductHeading'})
                            .find('h1').text.strip().replace('\t', '').replace('\n', ' '))
            return product_name
        except:
            return None
