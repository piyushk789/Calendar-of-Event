import os
import re
import threading
import concurrent.futures
from tkinter import messagebox
import requests
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup as Bs
from functools import wraps
from time import perf_counter, sleep
from typing import Callable, Any


def get_time(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        # Note that timing your code once isn't the most reliable option
        # for timing your code. Look into the timeit module for more accurate
        # timing.
        start_time: float = perf_counter()
        result: Any = func(*args, **kwargs)
        end_time: float = perf_counter()

        # print(f'"{func.__name__}()" took {end_time - start_time:.3f} seconds to execute')
        return result

    return wrapper


class TodayDay:
    def __init__(self, link=None, month=None, day=None):
        self.month = datetime.now().strftime('%B').lower() if not month else month
        self.day = datetime.now().day if not day else day
        self.link = "https://nationaltoday.com" if link is None else link
        self.link_req = None
        self.link_data = None
        self.soup = None
        self.all_img_num = 0
        self.all_downloads = 0
        self.downloads = []
        self.folder_path = None

    def refresh(self):
        """refresh all content for each day and month"""
        self.link = f"{self.link}/{self.month}-{self.day}/"
        self.link_req = requests.get(self.link)
        self.link_data = self.link_req.text
        self.soup = Bs(self.link_data, 'html.parser')
        self.folder_path = Path(Path(__file__).parent, f"Images/Days Image/{self.month}/{self.day}")

    def how_much(self):
        """check how much events are in the day"""
        return self.soup.find('div', class_='holiday-count').get_text()

    def get_names(self):
        """get all titles of the events"""
        return [name.get_text() for name in self.soup.find_all('h3', class_="holiday-title")]

    def get_imgs(self):
        """fetch image links from all containers"""
        img_links = self.soup.find_all('a', class_="day-card-mask")
        return [re.search(r"url\((.*?)\)", i.get("style")).group(1) for i in img_links]

    @staticmethod
    def sanitize_filename(name):
        """remove extra symbol from the image's name"""
        renaming = name.replace("\x18", "")
        renaming = renaming.replace("\"", "'")
        correct = re.sub(r'[<>:/\\|?*]', '', renaming)
        return correct.lower()

    def download_img(self, url, name: str = None):
        """download image from url"""
        try:
            response = requests.get(url)
            if response.status_code != 200:
                return messagebox.askretrycancel("Connection Error",
                                                 "Image not found\nPlease check your internet connection.")
            os.makedirs(self.folder_path, exist_ok=True)
            if name:
                name = self.folder_path / f"{self.sanitize_filename(name)}.jpg"
            else:
                name = self.folder_path / url.split('/')[-1]
            name = name.with_name(self.sanitize_filename(name.name))
            f = open(name, "wb")
        except OSError:
            f = open(name, "wb")
            self.downloads.append(name)
        except requests.exceptions.MissingSchema:
            self.downloads.append(None)
        else:
            f.write(response.content)
            f.close()
            # print(f"Downloaded: {name}")
            self.downloads.append(name)
            self.all_downloads += 1

    @get_time
    def loop_of_downloads(self):
        self.refresh()
        get_names = self.get_names()
        total_imgs = len(get_names)
        print(get_names, total_imgs)
        ls_img_name = zip(get_names, self.get_imgs())
        for name, link in ls_img_name:
            checking_name = name.lower() + ".jpg"
            if os.path.exists(self.folder_path) and checking_name in os.listdir(self.folder_path):
                continue
            self.download_img(link, name)
        self.all_img_num += total_imgs

        pos = [10, 90, 170, 250, 330] * (total_imgs // 5)
        return zip(pos, list(ls_img_name))


if __name__ == '__main__':

    # This is main Project File

    calendar = {"january": 31, "february": 28, "march": 31, "april": 30, "may": 31, "june": 30, "july": 31,
                "august": 31, "september": 30, "october": 31, "november": 30, "december": 31}

    td = TodayDay()

    #
    # def running(m, d):
    #     td.month = m
    #     for i in range(1, d + 1):
    #         td.day = i
    #         print(f"{td.day}) Working on {td.day} - {td.month}")
    #         td.loop_of_downloads()
    #         print(f"Complete on {td.day} - {td.month}")
    # for mo, da in calendar.items():
    #     running(mo, da)

