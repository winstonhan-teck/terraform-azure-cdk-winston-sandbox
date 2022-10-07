
## Authenticating to Azure
```
# azcli Authenticating to Azure 
az login
az account list --output table | grep sandbox
az account set --subscription sandbox
```

## init cdktf template and install provider
```
pip install --user pipenv
cd terraform-azure-winston-sandbox-cdk
cdktf init --template=python --local
pipenv install cdktf-cdktf-provider-azurerm

```