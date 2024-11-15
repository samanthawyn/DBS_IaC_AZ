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
rg_name = "MyResourceGroup"
location = "eastus"
resource_client.resource_groups.create_or_update(rg_name, {"location": location})

# Create Virtual Network and Subnet
vnet_name = "MyVNet"
subnet_name = "MySubnet"
vnet_params = {
    "location": location,
    "address_space": {"address_prefixes": ["10.0.0.0/16"]}
}
network_client.virtual_networks.begin_create_or_update(rg_name, vnet_name, vnet_params).result()

subnet_params = {"address_prefix": "10.0.0.0/24"}
network_client.subnets.begin_create_or_update(rg_name, vnet_name, subnet_name, subnet_params).result()

# Create Network Interface
nic_params = {
    "location": location,
    "ip_configurations": [{
        "name": "MyIPConfig",
        "subnet": {"id": network_client.subnets.get(rg_name, vnet_name, subnet_name).id},
        "private_ip_allocation_method": "Dynamic"
    }]
}
nic_name = "MyNIC"
nic = network_client.network_interfaces.begin_create_or_update(rg_name, nic_name, nic_params).result()

# Create Virtual Machines
for i in range(3):
    vm_name = f"MyVM{i}"
    vm_params = {
        "location": location,
        "hardware_profile": {"vm_size": "Standard_B1s"},
        "os_profile": {
            "computer_name": vm_name,
            "admin_username": "azureuser",
            "admin_password": "yourpassword"
        },
        "network_profile": {"network_interfaces": [{"id": nic.id}]},
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