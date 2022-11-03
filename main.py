from constructs import Construct
from cdktf import App, TerraformStack, TerraformOutput, Token
# from imports.azurerm.provider import AzurermProvider
# from imports.azurerm.resource_group import ResourceGroup
# from imports.azurerm.virtual_network import VirtualNetwork
from cdktf_cdktf_provider_azurerm.provider import AzurermProvider
from cdktf_cdktf_provider_azurerm.resource_group import ResourceGroup
from cdktf_cdktf_provider_azurerm.virtual_network import VirtualNetwork
from cdktf_cdktf_provider_azurerm.data_azurerm_resource_group import DataAzurermResourceGroup
from cdktf_cdktf_provider_azurerm.subnet import Subnet

class MyStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        # define resources here
        loca = "Central US"
        add_space = ["10.20.50.0/24"]
        rg_name = "rg-winston-cus-31r2"
        vm1_name = "vm-1"
        subnet1_name = "vnet1-subnet1"
        tag = {
            "ENV": "Dev",
            "PROJECT": "AZ_TF"
        }
        vnets = [{"name": "vnet1", "cidr": ["10.20.30.0/24"]},
                 {"name": "vnet2", "cidr": ["10.20.40.0/24"]}
        ]
        vnet_instances = []

        AzurermProvider(self, "Azurerm",
                        features={}
                        )

        # rg_test = ResourceGroup(self, 'example-rg',
        #                            name=rg_name,
        #                            location=loca,
        #                            tags=tag
        #                            )

        # get resource group instance
        rg_test = DataAzurermResourceGroup(self, 'example-rg',
                                   name=rg_name
                                   )
        # create 2 Vnet, test looping
        for vnet in vnets:
            vnet_instance = VirtualNetwork(self, vnet["name"],
                                      depends_on=[rg_test],
                                      name=vnet["name"],
                                      location=loca,
                                      address_space=vnet["cidr"],
                                      resource_group_name=Token().as_string(rg_test.name),
                                      tags=tag
                                      )
            vnet_instances.append(vnet_instance)

        # create 1 subnet
        subnet1 = Subnet(self, 'vnet1-subnet1',
                        name=subnet1_name,
                        resource_group_name=Token().as_string(rg_test.name),
                        virtual_network_name=Token().as_string(vnet_instances[0].name),
                        # virtual_network_name=vnets[0]["name"],
                        address_prefixes=["10.20.30.0/25"]
        )

        # TerraformOutput(self, 'vnet_id',
        #                 value=vnet_test.id
        #                 )


app = App()
MyStack(app, "python-azure")

app.synth()