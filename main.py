from constructs import Construct
from cdktf import App, TerraformStack, TerraformOutput, Token
# from imports.azurerm.provider import AzurermProvider
# from imports.azurerm.resource_group import ResourceGroup
# from imports.azurerm.virtual_network import VirtualNetwork
from cdktf_cdktf_provider_azurerm.provider import AzurermProvider
from cdktf_cdktf_provider_azurerm.resource_group import ResourceGroup
from cdktf_cdktf_provider_azurerm.virtual_network import VirtualNetwork
from cdktf_cdktf_provider_azurerm.data_azurerm_resource_group import DataAzurermResourceGroup

class MyStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        # define resources here
        loca = "Central US"
        add_space = ["10.20.50.0/24"]
        rg_name = "rg-winston-cus-31r2"
        tag = {
            "ENV": "Dev",
            "PROJECT": "AZ_TF"
        }

        AzurermProvider(self, "Azurerm",
                        features={}
                        )

        # rg_test = ResourceGroup(self, 'example-rg',
        #                            name=rg_name,
        #                            location=loca,
        #                            tags=tag
        #                            )

        rg_test = DataAzurermResourceGroup(self, 'example-rg',
                                   name=rg_name
                                   )

        vnet_test = VirtualNetwork(self, 'vnet_test',
                                      depends_on=[rg_test],
                                      name="vnet_test",
                                      location=loca,
                                      address_space=add_space,
                                      resource_group_name=Token().as_string(rg_test.name),
                                      tags=tag
                                      )

        TerraformOutput(self, 'vnet_id',
                        value=vnet_test.id
                        )


app = App()
MyStack(app, "python-azure")

app.synth()