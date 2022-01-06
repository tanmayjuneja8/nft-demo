from scripts.helpful_scripts import (
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_contract,
)
from brownie import network
import time
import pytest
from scripts.AdvancedCollectible.deploy_and_create import deploy_and_create


def test_can_create_advanced_collectible_integration():
    """deploy the contract, create an NFT, get a random breed back"""
    # Arrrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for integration testing")
    # Act
    advanced_collectible, creation_transaction = deploy_and_create()
    time.sleep(60)
    # Assert
    assert advanced_collectible.tokenCounter() == 1
