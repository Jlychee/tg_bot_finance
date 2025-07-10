import os
from datetime import datetime

from notion_client import Client


class NotionConnection:
    def __init__(self, notion_token, page_id):
        self.__NOTION_TOKEN = notion_token
        self.__PAGE_ID = page_id

        self.client = Client(auth=self.__NOTION_TOKEN)

        self.all_elements_pages = self.client.blocks.children.list(
            block_id=self.client.blocks.children.list(block_id=self.__PAGE_ID)["results"][0]["id"].replace("-", ""))

        self.menu_id = self.all_elements_pages["results"][0]["id"].replace("-", "")
        self.main_el_id = self.all_elements_pages["results"][1]["id"].replace("-", "")
        self.others_id = self.all_elements_pages["results"][2]["id"].replace("-", "")
        self.categories_id = self.client.blocks.children.list(block_id=self.others_id)["results"][1]["id"]

        self.main_el_page = self.client.blocks.children.list(block_id=self.main_el_id)["results"]
        self.categories_page = self.client.databases.query(database_id=self.categories_id)["results"]

        self.accounts_db = self.client.databases.query(database_id=self.main_el_page[0]["id"].replace("-", ""))[
            "results"]
        self.expense_db = self.main_el_page[2]["id"].replace("-", "")
        self.income_db = self.main_el_page[4]["id"].replace("-", "")
        self.transfer_db = self.main_el_page[6]["id"].replace("-", "")

        self.account_data = self.get_accounts()
        self.categories_data = self.get_categories()

    def new_expense_record(self, account_id, categories_id, total_amount, expense_name):
        self.client.pages.create(
            **{
                "icon": {'external': {'url': 'https://www.notion.so/icons/upward_gray.svg'},
                         'type': 'external'},
                "parent": {
                    "database_id": self.expense_db
                },
                "properties": {
                    "Expense": {"title": [{"text": {"content": expense_name}}]},
                    "Accounts": {"relation": [{"id": account_id}]},
                    "Categories": {"relation": [{"id": categories_id}]},
                    "Date": {"date": {"start": str(datetime.now().date())}},
                    "Total Amount": {"number": float(total_amount.repalce(",", "."))}
                }
            }
        )

    def new_income_record(self, account_id, amount, income_name):
        self.client.pages.create(
            **{
                "icon": {'external': {'url': 'https://www.notion.so/icons/downward_gray.svg'},
                         'type': 'external'},
                "parent": {
                    "database_id": self.income_db
                },
                "properties": {
                    "Income Stream": {"title": [{"text": {"content": income_name}}]},
                    "Accounts": {"relation": [{"id": account_id}]},
                    "Date": {"date": {"start": str(datetime.now().date())}},
                    "Amount": {"number": float(amount.repalce(",", "."))}
                }
            }
        )

    def new_transfer_record(self, from_account_id, to_account_id, transfer_amount, transfer_name):
        self.client.pages.create(
            **{
                "icon": {'external': {'url': 'https://www.notion.so/icons/repeat_gray.svg'},
                         'type': 'external'},
                "parent": {
                    "database_id": self.transfer_db
                },
                "properties": {
                    "Name": {"title": [{"text": {"content": transfer_name}}]},
                    "From Account": {"relation": [{"id": from_account_id}]},
                    "To Account": {"relation": [{"id": to_account_id}]},
                    "Date": {"date": {"start": str(datetime.now().date())}},
                    "Transfer Amount": {"number": float(transfer_amount.repalce(",", "."))},
                }
            }
        )

    def get_accounts(self):
        accounts_data = {}
        for i in range(len(self.accounts_db)):
            accounts_data[self.accounts_db[i]["properties"]["Name"]["title"][0]["plain_text"]] = \
                [self.accounts_db[i]["id"].replace("-", ""),
                 self.accounts_db[i]["properties"]["Current Balance"]["formula"]["number"]]
        return accounts_data

    def get_categories(self):
        categories_data = {}
        for i in range(len(self.categories_page)):
            categories_data[self.categories_page[i]["properties"]["Name"]["title"][0]["plain_text"]] = \
                self.categories_page[i][
                    "id"].replace("-", "")
        return categories_data

    @staticmethod
    def get_full_balance(account_data):
        sm = 0
        for key, value in account_data.items():
            sm += value[1]
        return sm

    @staticmethod
    def get_balance(account_name, account_data):
        return account_data[account_name][1]
