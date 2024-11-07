Azure resources:

Function app: https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/f7c445af-a4de-4264-9e87-3196d6bc384d/resourceGroups/EfficiencyPack/providers/Microsoft.Web/sites/LogicAppEmbeddingFunction/appServices

API Management Service: https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/f7c445af-a4de-4264-9e87-3196d6bc384d/resourceGroups/EfficiencyPack/providers/Microsoft.ApiManagement/service/LogicAppEmbeddingFunction-apim/overview

Entities:

Embedding function: Azure function used as the compute for the API. Consumption based and in python. Required packages are in requirements.txt. I use VSCode with he azure functions extension for local testing and deploying. 

EmbeddingsTeamsTest: Copilot agent used to call the API. I use VSCode Teams toolkit to provision and test within teams. Can also test locally. More will will be needed to expose the copilot agent within msft once it is built

Wikis:

Azure Functions in VSCode: https://learn.microsoft.com/en-us/azure/azure-functions/functions-develop-vs-code?tabs=node-v4%2Cpython-v2%2Cisolated-process%2Cquick-create&pivots=programming-language-python

API Management: https://learn.microsoft.com/en-us/azure/api-management/import-and-publish

Copilot agents dogfood: https://microsoft.sharepoint-df.com/sites/copilot-extensions-dogfood/

Copilot agent is VSCode: https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/build-declarative-agents?tabs=windows%2Cttk