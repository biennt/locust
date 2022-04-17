Quick start:
- Having the docker-compose.yml and locustfile.py in the current directory
- Run the below command to start 1 master and 2 workers containers
- Open http://localhost:8089 in your browser and enjoy 

```
docker-compose up  --scale worker=2
```
The Dockerfile that i've used to build this image as below:
```
FROM locustio/locust
RUN pip3 install beautifulsoup4
RUN pip3 install lxml
```
docker-compose.yml
```
version: '3'

services:
  master:
#    extra_hosts:
#     - "example.com:192.168.31.4"
    image: biennt/locust
    ports:
     - "8089:8089"
    volumes:
      - ./:/mnt/locust
    command: -f /mnt/locust/locustfile.py --master -H http://example.com

  worker:
#    extra_hosts:
#     - "example.com:192.168.31.4"
    image: biennt/locust
    volumes:
      - ./:/mnt/locust
    command: -f /mnt/locust/locustfile.py --worker --master-host master
```
The sample locustfile.py which download all css, js, image found in the URI as below:
locustfile.py
```
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

        for script in soup.find_all('script'):
            if script.get('src'):
                reqscript = self.client.get(script.get('src'))

        for img in soup.find_all('img'):
            if img.get('src'):
                reqimg = self.client.get(img.get('src'))

#    def on_start(self):
 #       self.client.verify = False
```
