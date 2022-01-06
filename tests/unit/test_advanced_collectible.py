from scripts.helpful_scripts import (
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_contract,
)
from brownie import network
import pytest
from scripts.AdvancedCollectible.deploy_and_create import deploy_and_create


def test_can_create_advanced_collectible():
    """deploy the contract, create an NFT, get a random breed back"""
    # Arrrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for testing")
    # Act
    advanced_collectible, creation_transaction = deploy_and_create()
    requestid = creation_transaction.events["requestedCollectible"]["requestId"]
    random_no = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestid, random_no, advanced_collectible.address, {"from": get_account()}
    )
    # Assert
    assert advanced_collectible.tokenCounter() == 1
    assert advanced_collectible.tokenIdtoBreed(0) == random_no % 3
