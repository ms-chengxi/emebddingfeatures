import requests
from azure.identity import ManagedIdentityCredential
from azure.identity import DefaultAzureCredential

# User-assigned managed identity client ID
# client_id = "fe300394-6c65-467e-9aad-96f2637dbc2d"
client_id = "1820118a-ccca-4e98-ae0a-6dcb9c01eadf"

# API endpoint
# api_endpoint = "https://logicappembeddingfunction.azurewebsites.net/api/embeddingfunction?Service=WaAppAgent"
#api_endpoint = "https://logicappembeddingfunction-apim.azure-api.net/LogicAppEmbeddingFunction/EmbeddingFunction"
api_endpoint = "https://perfcopilottest2.azurewebsites.net/api/numaffected?code=l9WX9ddBdtfIcGj8BgS72YhMRTKEp8uNX5cswbwznZ_4AzFuvEOLJw%3D%3D?name=hnsproxy"

# Authority URL
#authority_URL = "https://login.microsoftonline.com/72f988bf-86f1-41af-91ab-2d7cd011db47/v2.0/.default"

# Get the token using ManagedIdentityCredential
credential = ManagedIdentityCredential(client_id=client_id)
# credential = DefaultAzureCredential()
# Define the scope for the API
#scope = "https://logicappembeddingfunction.azurewebsites.net/.default"
#scope = "https://graph.microsoft.com/.default"
#scope = "https://login.microsoftonline.com/.default"


# Get the token using ManagedIdentityCredential with the specified scope
# token = credential.get_token("d07a4aa0-7148-4e4a-9060-36a8fbec0888/.default")
import pdb; pdb.set_trace()
token = credential.get_token("https://management.azure.com/.default")

token = credential.get_token("6abc4791-4abd-4ec6-9058-91dd4fbda5b9/.default")
#token = credential.get_token("https://logicappembeddingfunction.azurewebsites.net/.default")

# Set up the headers with the token
headers = {
    "Authorization": f"Bearer {token.token}",
    "Content-Type": "application/json"
}

# Send a GET request to the API
response = requests.post(api_endpoint, headers=headers)

# Print the response
print(response.status_code)
print(response._content)
#print(response.json())