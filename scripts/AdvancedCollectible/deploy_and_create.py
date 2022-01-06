from brownie import network, accounts, config, AdvancedCollectible
from scripts.helpful_scripts import (
    get_account,
    OPENSEA_URL,
    get_contract,
    fund_with_link,
)


def deploy_and_create():
    account = get_account()
    adv_collectible = AdvancedCollectible.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
    )
    fund_with_link(adv_collectible.address)
    creating_tx = adv_collectible.createCollectible({"from": account})
    creating_tx.wait(1)
    print("New token has been created!")
    return adv_collectible, creating_tx


def main():
    deploy_and_create()
