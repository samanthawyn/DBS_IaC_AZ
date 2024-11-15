# Azure Resource Deployment Scripts

This repository contains several Python scripts for deploying infrastructures on Azure. Each script is designed for different purposes, helping students understand how to create and configure resources on Azure. Below is an overview of each file and its functionality.

## Files in the Repository

1. **deploy_azure_network_vm.py**
   - This is the base script that sets up a virtual network and deploys a virtual machine on Azure. It is designed to serve as a starting point for creating network resources and virtual machines.

2. **deploy_azure_network_vm_extended.py**
   - This file is an extended version that deploys infrastructure for a fictional organization. It includes:
     - Three virtual machines (App, Database, Web).
     - A virtual network with three separate subnets.
     - Network interfaces configured for each virtual machine.
   - This script is useful for understanding how to structure a more complex infrastructure.

3. **deploy_azure_network_vm_incomplete.py**
   - This script is incomplete and contains intentional errors. It lacks critical configurations, and some sections are improperly defined. The purpose is for students to review and correct it to ensure proper functionality.
   - **Common Issues**: Missing parameters, incorrectly defined configurations, and subscription errors.

## Running the Scripts

1. Clone this repository and navigate to the folder:
   ```bash
   git clone https://github.com/your_username/Azure-Resource-Setup.git
   cd Azure-Resource-Setup
   ```

2. Install the necessary dependencies:
   ```bash
   pip install azure-identity azure-mgmt-resource azure-mgmt-network azure-mgmt-compute
   ```

3. Run each script with:
   ```bash
   python script_name.py
   ```

## Educational Objective

These scripts provide a practical introduction to infrastructure as code on Azure, allowing students to explore and correct deployments in a real environment.
