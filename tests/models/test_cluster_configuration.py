import pytest
import yaml

from aztk.models import ClusterConfiguration, Toolkit, UserConfiguration
from aztk.spark.models.plugins import JupyterPlugin, HDFSPlugin

def test_vm_count_deprecated():
    with pytest.warns(DeprecationWarning):
        config = ClusterConfiguration(vm_count=3)
        assert config.size == 3

    with pytest.warns(DeprecationWarning):
        config = ClusterConfiguration(vm_low_pri_count=10)
        assert config.size_low_pri == 10

def test_cluster_configuration():
    data = {
        'toolkit':  {
            'software': 'spark',
            'version': '2.3.0',
            'environment': 'anaconda'
        },
        'vm_size': 'standard_a2',
        'size': 2,
        'size_low_pri': 3,
        'subnet_id': '/subscriptions/21abd678-18c5-4660-9fdd-8c5ba6b6fe1f/resourceGroups/abc/providers/Microsoft.Network/virtualNetworks/prodtest5vnet/subnets/default',
        'plugins': [
            JupyterPlugin(),
            HDFSPlugin(),
        ],
        'user_configuration': {'username': 'spark'}
    }

    config = ClusterConfiguration.from_dict(data)

    assert isinstance(config.toolkit, Toolkit)
    assert config.toolkit.software == 'spark'
    assert config.toolkit.version == '2.3.0'
    assert config.toolkit.environment == 'anaconda'
    assert config.size == 2
    assert config.size_low_pri == 3
    assert config.vm_size == 'standard_a2'
    assert config.subnet_id == '/subscriptions/21abd678-18c5-4660-9fdd-8c5ba6b6fe1f/resourceGroups/abc/providers/Microsoft.Network/virtualNetworks/prodtest5vnet/subnets/default'

    assert isinstance(config.user_configuration, UserConfiguration)
    assert config.user_configuration.username == 'spark'

    assert len(config.plugins) == 2
    assert isinstance(config.plugins[0], JupyterPlugin)
    assert isinstance(config.plugins[1], HDFSPlugin)
