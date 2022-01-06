from brownie import network, accounts, config, AdvancedCollectible
from scripts.helpful_scripts import (
    get_account,
    OPENSEA_URL,
    get_contract,
    fund_with_link,
)
from web3 import Web3


def main():
    acc = get_account()
    adv_collectible = AdvancedCollectible[-1]
    fund_with_link(adv_collectible.address, amount=Web3.toWei(0.1, "ether"))
    creation_tx = adv_collectible.createCollectible({"from": acc})
    creation_tx.wait(1)
    print("Collectible Created!")
