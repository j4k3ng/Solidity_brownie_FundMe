from scripts.deploy import get_account
from scripts.deploy import deploy_fund_me
from scripts.fund_and_withdraw import entrance_fee
from brownie import network
from scripts.deploy import LOCAL_BLOCKCHAIN_ENVIRONMENTS
import pytest
from brownie import accounts
from brownie import exceptions


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only local testing")
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()  # create an account which didnt deploy the fund_me so it's not the owner
    with pytest.raises(exceptions.VirtualMachineError): # a virtual machine error is risen when trying to withdrow money from an account which is not the owner of the Fundme contract
        fund_me.withdraw({"from": bad_actor})
