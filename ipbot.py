import telepot
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import datetime
import telepot.api
import urllib3


telepot.api._pools = {
    'default': urllib3.PoolManager(num_pools=3, maxsize=10, retries=5, timeout=30),
}

fritz_password = "ENTER YOUR FRITZBOX PASSWORD HERE"
telepot_api_key = "ENTER YOUR KEY HERE"
telepot_user_key = 000000000

class IPBot:
    def __init__(self):
        self.bot = telepot.Bot(telepot_api_key)

    def get_ip(self):
        browser = webdriver.PhantomJS()
        browser.get("http://192.168.178.1")
        sleep(5)
        pass_f = browser.find_element_by_name("uiPass")


        pass_f.send_keys(fritz_password)
        pass_f.send_keys(Keys.RETURN)
        sleep(5)
        return "Aktuelle IP:\n"+browser.find_element_by_xpath("//div[contains(@class, 'details info')]").text

    def send(self,ip):
        self.bot.sendMessage(telepot_user_key,ip)

    def get_current_message(self):
        updates = self.bot.getUpdates()
        if len(updates) == 0:
            return ""
        else:
            message_offset = updates[len(updates)-1]["update_id"]
            current_message = self.bot.getUpdates(offset = message_offset)
            return current_message[0]["message"]["text"]


if __name__ == "__main__":
    while True:
        try:
            ipbot = IPBot()
            if (ipbot.get_current_message() == "IP"):
                ipbot.send(ipbot.get_ip())
            if (ipbot.get_current_message() == "Exit"):
                break
            dateSTR = datetime.datetime.now().strftime("%H:%M")
            if dateSTR == ("01:00"):
                sleep(7200)
            if dateSTR == ("05:00"):
                ipbot.send(ipbot.get_ip())
                sleep(60)
            else:
                sleep(5)
                pass
        except:
            sleep(60)
