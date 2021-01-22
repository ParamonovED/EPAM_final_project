import asyncio

import aiohttp

from bs4 import BeautifulSoup


def parser(page):  # ResponseObject --> BeautifulSoupObject
    return BeautifulSoup(page, "html.parser")


async def request(url, title, shop_object, paginator=1):  # url --> ResponseObject
    url += f"?q={title}&p={paginator}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            page = await response.text()
            shop_object.pages.append(page)
            return page


async def async_request(url, title, finder_last_page,
                        shop_object):  # 1st ResponseObject -> [ResponseObjects..], p=1...last
    tasks = []
    target_page = BeautifulSoup(await request(url, title, shop_object), "html.parser")  # parsed 1st_page
    number_of_last_page = finder_last_page(target_page)
    i = 1
    while i < number_of_last_page:
        tasks.append(request(url, title, shop_object, paginator=i))
        i += 1
    await asyncio.gather(*tasks)


def run_loop(url, title, finder_last_page, shop_object):
    asyncio.run(async_request(url, title, finder_last_page, shop_object))


class EbayGetTarget:
    pass


class AvitoGetTarget:
    def __init__(self, target):
        self.url = "https://www.avito.ru"
        self.target = target
        self.parsed_pages = []
        self.average_price = None
        self.dyn_average_price = None
        self.price_difference = None
        self.pages = []
        self.ads = []

        def finder_last_page(target_page):
            last_page = target_page.find_all(class_="pagination-item-1WyVp")
            if last_page:
                return int(last_page[-2].text)
            return 1

        run_loop(self.url, self.target.title, finder_last_page, self)  # A list of ResponseObjects "parsed_pages"
        for avito_page in self.pages:
            self.parsed_pages.append(parser(avito_page))

    def get_info(self):
        info = []
        for avito_parsed_page in self.parsed_pages:
            items = avito_parsed_page.find_all(class_="iva-item-body-NPl6W")
            for item in items:
                info.append(self.add_info(item))
        self.fill_target_fields(info)
        return info, self.average_price, self.price_difference, self.dyn_average_price

    def add_info(self, item):
        title = item.find(class_="iva-item-titleStep-2bjuh").text
        link = self.url + item.find(class_="iva-item-titleStep-2bjuh").a["href"]
        price = item.find(class_="price-text-1HrJ_ text-text-1PdBw text-size-s-1PUdo").text
        return [title, link, price]

    def fill_target_fields(self, info):
        avg = round(sum([int(ad[2][:-2].replace(" ", "")) for ad in info]) / len(info))
        if self.average_price != avg and self.average_price is not None:
            self.dyn_average_price = avg - self.average_price
        self.average_price = avg
        self.price_difference = self.target.wanted_price - self.average_price
