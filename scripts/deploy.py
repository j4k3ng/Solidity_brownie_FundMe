from brownie import FundMe
from brownie import accounts
from brownie import network
from brownie import config
from brownie import MockV3Aggregator
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


def deploy_fund_me():
    account = get_account()

    # if in the rinkby use it, otherwise create a mock local priceFeed function
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks() # it's used to deploy a .sol code in the development network to simulate what the chainlink does in the test or main net. I need it because obviously in the local network I dont have chainlink oracle which could give me the eth usd pricefeed so I create artifically locally deployng a solidity program which does the job.
        price_feed_address = MockV3Aggregator[-1].address
    
    # deploy the FundMe.sol to the active network
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print("Contract deployed to :", fund_me.address)
    return fund_me


def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print("The active network is ", network.show_active())
    print("Deploying contract...")
    if len(MockV3Aggregator) <= 0:
        mock_aggregator = MockV3Aggregator.deploy(
            18, Web3.toWei(2000, "ether"), {"from": get_account()}
        )
    print("Mocks Deployed !!")
    price_feed_address = MockV3Aggregator[-1].address


def main():
    deploy_fund_me()
