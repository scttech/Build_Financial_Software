import pytest
from pydantic import BaseModel
from pydantic.networks import IPvAnyAddress, IPvAnyNetwork


class IpModel(BaseModel):
    ip_any_address: IPvAnyAddress
    ip_any_network: IPvAnyNetwork


class TestPydanticNetworkTypes:

    def test_valid_any_address(self):
        my_address = IpModel(ip_any_address="127.0.0.1", ip_any_network="127.0.0.1")
        assert str(my_address.ip_any_address) == "127.0.0.1"

    def test_invalid_any_address(self):
        with pytest.raises(ValueError):
            IpModel(ip_any_address="127.0.0.256", ip_any_network="127.0.0.1")

    def test_valid_any_network(self):
        my_address = IpModel(ip_any_address="127.0.0.1", ip_any_network="127.0.0.1")
        assert str(my_address.ip_any_network) == "127.0.0.1/32"

    def test_invalid_any_network(self):
        with pytest.raises(ValueError):
            IpModel(ip_any_address="127.0.0.1", ip_any_network="127.0.0.256")
