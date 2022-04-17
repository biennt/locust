import time
from locust import HttpUser, task, between
from bs4 import BeautifulSoup

class QuickstartUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def home(self):
        response = self.client.get("/")
        soup = BeautifulSoup(response.text, "lxml")

        for css in soup.find_all('link'):
            if css.get('href'):
                reqcss = self.client.get(css.get('href'))
                print(css.get('href'))

        for script in soup.find_all('script'):
            if script.get('src'):
                reqscript = self.client.get(script.get('src'))
                print(script.get('src'))

        for img in soup.find_all('img'):
            if img.get('src'):
                reqimg = self.client.get(img.get('src'))
                print(img.get('src'))

#    def on_start(self):
#        self.client.verify = False
