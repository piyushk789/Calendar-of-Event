# Author: Kartikey Baghel
# Email - kartikeybaghel@hotmail.com

# For Developers

import os
import requests
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup as Bs
from functools import wraps
from time import perf_counter

def get_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time: float = perf_counter()
        result = func(*args, **kwargs)
        end_time: float = perf_counter()

        print(f'took {end_time - start_time:.3f} sec to execute')
        return result

    return wrapper

class TodayDay:
    def __init__(self, month=None, day=None):
        self.complains = []
        self.loading = None
        self.link_data = None
        self.link_req = None
        date = datetime.now().strftime('%B-%d').lower().split("-")
        self.month = month if month else date[0]
        self.day = day if day else date[1]
        self.link = "https://nationaltoday.com"
        self.soup = None
        self.folder_path = None

    def refresh(self):
        """refresh all content for each day and month"""
        self.link = f"https://nationaltoday.com/{self.month}-{self.day}/"
        self.link_req = requests.get(self.link)
        self.link_data = self.link_req.text
        self.soup = Bs(self.link_data, 'html.parser')
        self.loading = []
        self.folder_path = Path(Path(__file__).parent, f"Images/Days Image/{self.month}/{self.day}")

    def how_much(self):
        """check how much events are in the day"""
        return self.soup.find('div', class_='holiday-count').get_text()

    def get_names(self):
        """get all titles of the events"""
        return [name.get_text().lower() for name in self.soup.find_all('h3', class_="holiday-title")]

    def get_imgs(self): return os.listdir(self.folder_path)

    def fetch_name_titles(self):
        self.refresh()
        get_names = self.get_names()
        loaded_imgs = self.get_imgs()
        total_imgs = len(get_names)

        for name in get_names:
            if f"{name}.jpg" in loaded_imgs:
                self.loading.append(name)
            else:
                sh = f"{self.month} - {self.day} - {name}"
                print(sh)
                self.complains.append(sh)

        coordinate = [10, 90, 170, 250, 330]
        pos = coordinate * (total_imgs // 5)
        pos.extend(coordinate[:(total_imgs % 5)])
        print(f"{self.day}-{self.month}", end=" ")
        return [pos, self.loading]

if __name__ == '__main__':

    # This is main Project File

    calendar = {"january": 31, "february": 28, "march": 31, "april": 30, "may": 31, "june": 30, "july": 31,
                "august": 31, "september": 30, "october": 31, "november": 30}
    data = {}

    td = TodayDay()

    @get_time
    def processing():
        for mont in calendar:
            data[mont] = {}
            print(data[mont])
            # TODO: There is a problem to add data in JSON format
            for day in range(1, calendar[mont]+1):
                td.month, td.day = mont, day
                try:
                    values = td.fetch_name_titles()
                    print(values)
                    data[mont][day] = values
                except Exception as e:
                    print(e)
    processing()
    with open("title_img_pos.json", "w") as f:
        json.dump(data, f)
    with open("complain.txt", "w") as f:
        json.dump(td.complains, f)
