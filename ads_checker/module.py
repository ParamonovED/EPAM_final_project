import asyncio

import aiohttp

import requests
from bs4 import BeautifulSoup

from ads_checker.models import Ad


def parser2(page):       # ResponseObject --> BeautifulSoupObject
    parsed_page = BeautifulSoup(page, "html.parser")
    return parsed_page


pages = []


async def request(url, title, paginator=1):  # url --> BeautifulSoupObject
    url += f"?q={title}&p={paginator}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            page = await response.text()
            pages.append(page)
            return page


# class DoAsyncRequest:       # our data --> [..ResponseObjects..]
#     def __init__(self, url, title, price_min=None, price_max=None):
#         self.url = url      # url = "https://www.avito.ru"
#         self.title = title
#         self.price_min = price_min
#         self.price_max = price_max
#         self.tasks = list()
#         self.response_objects = []
#
#     def request(self, paginator=1):     # -> ResponseObject
#         params = {"q": self.title,            # f"?pmax={self.price_max}" \
#                   "pmin": self.price_min,     # f"&pmin={self.price_min}" \
#                   "pmax": self.price_max,     # f"&q={self.title}" \
#                   "p": paginator}             # f"&p={paginator}""
#         return requests.get(self.url, params=params)
#
#     async def async_request(self):      # 1st ResponseObject -> [ResponseObjects..], p=1...last
#         target_first_page = self.request()
#         target_page = parser(target_first_page.text)    # parsed 1st_page
#         number_of_last_page = int(target_page.find_all(class_="pagination-item-1WyVp")[-2].text)    # !!!
#         i = 1
#         while i <= number_of_last_page:
#             self.tasks.append(self.response_objects.append(self.request(paginator=i)))  # will it work?
#             i += 1
#         print(self.tasks)
#         await asyncio.gather(*self.tasks)
#
#     def run_loop(self):
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)
#         loop = asyncio.get_event_loop()
#         loop.run_until_complete(self.async_request())
#         loop.close()
#         return self.response_objects


def request2(url, title, paginator=1):     # -> ResponseObject
    params = {"q": title,            # f"?pmax={self.price_max}" \
              "p": paginator}             # f"&p={paginator}""
    return requests.get(url, params=params)


async def async_request(url, title, finder_last_page):      # 1st ResponseObject -> [ResponseObjects..], p=1...last
    tasks = []
    target_page = BeautifulSoup(await request(url, title), "html.parser")   # parsed 1st_page
    number_of_last_page = finder_last_page(target_page)
    i = 1
    while i <= number_of_last_page:
        tasks.append(request(url, title, paginator=i))
        i += 1
    await asyncio.gather(*tasks)


def run_loop(url, title, finder_last_page):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_request(url, title, finder_last_page))
    # loop.close()
    # return response_objects


class EbayGetTarget:
    pass


class AvitoGetTarget:
    def __init__(self, target):
        self.url = "https://www.avito.ru"
        self.target = target

        def finder_last_page(target_page):
            return int(target_page.find_all(class_="pagination-item-1WyVp")[-2].text)

        self.avito_parsed_pages = []
        self.ads = []
        run_loop(self.url, self.target.title, finder_last_page)     # A list of ResponseObjects
        avito_pages = pages
        for avito_page in avito_pages:
            self.avito_parsed_pages.append(parser2(avito_page))

    def get_info(self):
        info = []
        for avito_parsed_page in self.avito_parsed_pages:
            items = avito_parsed_page.find_all(class_="iva-item-body-NPl6W")
            for item in items:
                link = item.find(class_="iva-item-titleStep-2bjuh").a["href"]
                name = item.find(class_="iva-item-titleStep-2bjuh").text
                price = item.find(class_="price-text-1HrJ_ text-text-1PdBw text-size-s-1PUdo").text
                print(f"item#", link, "\n", name, "\n", price, "\n\n")
                info.append((link, name, price))
        return info

# my_id=87964404  stupid parsing, flex box, stealing html from avito

""" 
magic_tuple.append({"link":link, "name":name, "price":price})
db.append(pd.from_tuple(magic_tuple, args))
"""
