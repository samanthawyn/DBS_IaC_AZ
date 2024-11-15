from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient

# Initialize clients
subscription_id = "your-subscription-id"
credentials = DefaultAzureCredential()

resource_client = ResourceManagementClient(credentials, subscription_id)
network_client = NetworkManagementClient(credentials, subscription_id)
compute_client = ComputeManagementClient(credentials, subscription_id)

# Create a Resource Group
rg_name = "OrganizationResourceGroup"
location = "eastus"
resource_client.resource_groups.create_or_update(rg_name, {"location": location})

# Create Virtual Network and Subnets
vnet_name = "OrganizationVNet"
subnet_names = ["AppSubnet", "DbSubnet", "WebSubnet"]
address_space = "10.1.0.0/16"
subnet_prefixes = ["10.1.1.0/24", "10.1.2.0/24", "10.1.3.0/24"]

vnet_params = {
    "location": location,
    "address_space": {"address_prefixes": [address_space]}
}
network_client.virtual_networks.begin_create_or_update(rg_name, vnet_name, vnet_params).result()

# Create Subnets for each component
for subnet_name, prefix in zip(subnet_names, subnet_prefixes):
    subnet_params = {"address_prefix": prefix}
    network_client.subnets.begin_create_or_update(rg_name, vnet_name, subnet_name, subnet_params).result()

# Create Network Interfaces for VMs
nic_names = ["AppNIC", "DbNIC", "WebNIC"]
nic_params_list = [
    {
        "location": location,
        "ip_configurations": [{
            "name": "AppIPConfig",
            "subnet": {"id": network_client.subnets.get(rg_name, vnet_name, subnet_names[0]).id},
            "private_ip_allocation_method": "Dynamic"
        }]
    },
    {
        "location": location,
        "ip_configurations": [{
            "name": "DbIPConfig",
            "subnet": {"id": network_client.subnets.get(rg_name, vnet_name, subnet_names[1]).id},
            "private_ip_allocation_method": "Dynamic"
        }]
    },
    {
        "location": location,
        "ip_configurations": [{
            "name": "WebIPConfig",
            "subnet": {"id": network_client.subnets.get(rg_name, vnet_name, subnet_names[2]).id},
            "private_ip_allocation_method": "Dynamic"
        }]
    }
]

for nic_name, nic_params in zip(nic_names, nic_params_list):
    network_client.network_interfaces.begin_create_or_update(rg_name, nic_name, nic_params).result()

# Create Virtual Machines
vm_names = ["AppVM", "DbVM", "WebVM"]
for vm_name, nic_id in zip(vm_names, nic_names):
    vm_params = {
        "location": location,
        "hardware_profile": {"vm_size": "Standard_B1s"},
        "os_profile": {
            "computer_name": vm_name,
            "admin_username": "azureuser",
            "admin_password": "yourpassword"
        },
        "network_profile": {"network_interfaces": [{"id": network_client.network_interfaces.get(rg_name, nic_id).id}]},
        "storage_profile": {
            "image_reference": {
                "publisher": "Canonical",
                "offer": "UbuntuServer",
                "sku": "18.04-LTS",
                "version": "latest"
            }
        }
    }
    compute_client.virtual_machines.begin_create_or_update(rg_name, vm_name, vm_params).result()
