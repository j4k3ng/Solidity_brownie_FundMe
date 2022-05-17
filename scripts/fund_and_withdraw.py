from brownie import FundMe
from scripts.deploy import get_account  

entrance_fee = 0.0001


def fund():
    fund_me = FundMe[-1]
    account = get_account()
    print(entrance_fee)
    print("The current entry fee is {entrance_fee}")
    print("Funding")
    fund_me.fund({"from": account, "value": entrance_fee})


def withdraw():
    fund_me = FundMe[-1]
    account = get_account()
    fund_me.withdraw({"from": account})


def main():
    fund()
    withdraw()
