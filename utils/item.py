"""Module for the item class"""

import requests
from utils.exeptions.api_exeption import MaxRetries

from utils.price_stamp import PriceStamp
from utils.settings import MAX_API_TRIES, MAX_API_TIMEOUT
from utils.utils import get_timestamp


class Item:
    """Class for an item with an item_id and a name"""
    itemId = None
    name = None
    icon_url = None

    def __init__(self, item_id, name=None, icon_url=None):
        self.item_id = item_id
        self.name = name
        self.icon_url = icon_url

    def __str__(self):
        return f"Item: {self.name} ({self.item_id})"

    def get_item_id(self):
        """Returns the item id"""
        return self.item_id
    
    def get_name(self):
        """Returns the name of the item"""
        return self.name

    def get_icon_url(self):
        """Returns the icon url of the item"""
        return self.icon_url

    def get_buff_sell_order_api_link(self):
        """Returns the buff.163.com sell order api link"""
        return f"https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id={self.item_id}&page_num=1&page_size=100"

    def request_sell_orders_buff(self):
        """Requests the sell orders from buff.163.com"""
        headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'Device-Id=8FjpMdIqmva19OlXLWjf; client_id=S3nHCYtfBOpagk2Rj3Xucg; csrf_token=IjQyNmMzYTBmZjk0ZGU0YWE4OGJiOGZiNjA5YTRmMjkxZGY3OGNkNDQi.FoD6CQ.SxChC0qLzewRQ_kpTEEjuLtBq28; Device-Id=MTEPNh8KclDlCvOJqW9q; client_id=DfVkkXPO7VxFiLD4XeyK2w; csrf_token=ImI2YTkxMzUxMDQ0ZjYzNjJlYmZmZTg4MjA5MzdiYjM3NTIxNzA4Yzci.FoD7hw.GUH7lLX1KbWs6gKCuFY68PnV5v4',
        'Pragma': 'no-cache',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
        }
        return requests.get(self.get_buff_sell_order_api_link(), headers=headers, data={}, timeout=MAX_API_TIMEOUT)

    def fetch_data(self):
        """Fetches the item name from buff.163.com using the item id
        and saves it in the name variable"""
        for _ in range(MAX_API_TRIES):
            try:
                response = self.request_sell_orders_buff()
                status_code = response.status_code
                if status_code != 200:
                    break
                data = response.json()
                self.name = data["data"]["goods_infos"][str(self.item_id)]["name"]
                self.icon_url = data["data"]["items"][0]["img_src"]
                return
            except requests.JSONDecodeError:
                print(status_code)
                print("JSONDecodeError: ", response)

        raise MaxRetries()

    def get_sell_price_stamp(self):
        """Returns a PriceStamp with the item id, current sell price,
        the lowest bargain price and a tiemstamp"""
        for _ in range(MAX_API_TRIES):
            try:
                response = self.request_sell_orders_buff()
                status_code = response.status_code
                if status_code != 200:
                    break
                data = response.json()
                price = float(data["data"]["items"][0]["price"])
                highest_bargain_price = float(data["data"]["items"][0]["lowest_bargain_price"])
                return PriceStamp(self.item_id, price, highest_bargain_price, get_timestamp())
            except requests.JSONDecodeError:
                print(status_code)
                print("JSONDecodeError: ", response)
        raise MaxRetries()
    
    def to_json(self):
        """Returns a json representation of the item"""
        return {
            "item_id": self.item_id,
            "name": self.name,
            "icon_url": self.icon_url
        }
