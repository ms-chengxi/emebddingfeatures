import azure.functions as func
import logging
import pandas as pd
import numpy as np
from openai import AzureOpenAI
import time
import re
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder, ClientRequestProperties
from azure.kusto.data.helpers import dataframe_from_result_table
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
pd.options.mode.chained_assignment = None #https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#evaluation-order-matters
cluster = "https://epmon.westus.kusto.windows.net"

#@app.function_name(name="http_trigger")
@app.route(route="EmbeddingFunction")





def EmbeddingFunction(req: func.HttpRequest) -> func.HttpResponse:
    def KustoIngest(Service: str):
        kcsb = KustoConnectionStringBuilder.with_aad_managed_service_identity_authentication(cluster)
        #kcsb = KustoConnectionStringBuilder.with_azure_identity_authentication(cluster, DefaultAzureCredential())
        #kcsb = KustoConnectionStringBuilder.with_az_cli_authentication(cluster)
        client = KustoClient(kcsb)
        db = "EfficiencyPack"
        query = r"""ExpertStream 
        | where DataDate >= startofday(ago(2d)) and DataDate < startofday(ago(1d)) 
        | where Service == """ +'"' + Service + '"' + " | distinct Stack | take 5"
        response = client.execute(db, query)
        dataframe = dataframe_from_result_table(response.primary_results[0])
        return dataframe
    
    # s is input text
    def normalize_text(s, sep_token = " \n "):
        s = re.sub(r'\s+',  ' ', s).strip()
        s = re.sub(r". ,","",s)
        # remove all instances of multiple spaces
        s = s.replace("..",".")
        s = s.replace(". .",".")
        s = s.replace("\n", "")
        s = s.replace("?!?", "")
        s = s.strip()
        # remove unhelpful frames
        s = s.split("^^")
        filtered = [frame for frame in s if not frame.startswith('clr!')]
        filtered = [frame for frame in filtered if not frame.startswith('kernel32!')]
        filtered = [frame for frame in filtered if not frame.startswith('ntdll!')]
        s = "^^".join(filtered)
        
        # replace ^^
        s = s.replace("^^", " ")
        s = s.rstrip()
        return s
    def cosine_similarity(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


    def search_docs(df, user_query, top_n=4):
        token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
        )

        client = AzureOpenAI(
        azure_ad_token_provider=token_provider, 
        api_version = "2024-02-01",
        azure_endpoint = "https://aitestepm.openai.azure.com/"
        )

        def generate_embeddings(text, model): # model = "deployment_name"
            return client.embeddings.create(input = [text], model=model).data[0].embedding
        embedding = generate_embeddings(
        user_query,
        model="Embeddings" # model should be set to the deployment name you chose when you deployed the text-embedding-ada-002 (Version 2) model
        )
        df["embeddings"] = df.Stack.apply(lambda x: generate_embeddings(x, model="Embeddings"))
        df["similarities"] = df.embeddings.apply(lambda x: cosine_similarity(x, embedding))

        res = (
            df.sort_values("similarities", ascending=False).head(top_n)
        )
        return res


        #res = search_docs(df, r'AllocLarge.LOH<1mb! [1000-2000]!  clr!ETW::SamplingLog::SendStackTrace clr!EtwCallout clr!CoTemplate_qh clr!SVR::GCHeap::GarbageCollectGeneration clr!SVR::gc_heap::trigger_gc_for_alloc clr!SVR::gc_heap::try_allocate_more_space clr!SVR::gc_heap::allocate_more_space clr!SVR::gc_heap::allocate_large_object clr!JIT_NewArr1 microsoft.azure.cosmos.direct!Microsoft.Azure.Documents.Rntbd.Connection+<ReadResponseBodyAsync>d__.MoveNext() mscorlib!System.Runtime.CompilerServices.AsyncTaskMethodBuilder`1[System.__Canon].Start(System.__Canon&) microsoft.azure.cosmos.direct!Microsoft.Azure.Documents.Rntbd.Connection.ReadResponseBodyAsync(Microsoft.Azure.Documents.Rntbd.ChannelCommonArguments) microsoft.azure.cosmos.direct!Microsoft.Azure.Documents.Rntbd.Dispatcher+<ReceiveLoopAsync>d__.MoveNext() mscorlib!? microsoft.azure.cosmos.direct!Microsoft.Azure.Documents.Rntbd.Connection+<ReadResponseMetadataAsync>d__.MoveNext() mscorlib!?', top_n=10)


    logging.info('Python HTTP trigger function processed a request.')
    
    Service = req.params.get('Service')
    if not Service:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            Service = req_body.get('Service')
    
    df = KustoIngest(Service)
    time.sleep(10)
    df['Stack']= df['Stack'].apply(lambda x : normalize_text(str(x)))
    res = search_docs(df, Service, top_n=5)
    




    if Service:
        return func.HttpResponse(f"Hello, {Service}. \n" + res.to_string())
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )