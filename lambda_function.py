import os,base64,boto3
from kubernetes import client, config
from eks_token import get_token

def lambda_handler(event, context):
    print("One of the application nodes is terminated and Lambda function is triggered")
    token=get_token(cluster_name='hhh-test')
    configuration = client.Configuration()
    configuration.host = os.environ.get('EKS_HOST')
    configuration.api_key['authorization'] = token['status']['token']
    configuration.api_key_prefix['authorization'] = 'Bearer'
    configuration.ssl_ca_cert=os.path.join(os.getcwd(), 'ca.crt')
    client.Configuration.set_default(configuration)
    api = client.ApiClient(configuration)
    v1 = client.CoreV1Api(api)
    listAppNodes = v1.list_node(label_selector="nodetype=application")
    if len(listAppNodes.items) == 0:
        message="There are no application nodes in the cluster. Please delete the cluster."
        print(message)
        return send_email(message)
    workload=[]
    for i in listAppNodes.items:
        listPods=v1.list_pod_for_all_namespaces(field_selector='spec.nodeName='+i.metadata.name)
    for i in listPods.items:
        if i.metadata.owner_references[0].kind.lower() != 'daemonset' :
            workload.append(i)
    if len(workload) == 0:
        message="There are no application pods running on the cluster. Please delete the cluster."
        print(message)
        return send_email(message)
    print("Cluster has workload on application nodes and cant be deleted.")
    return "ok"

def send_email(email):
    ses_client = boto3.client("ses")
    subject =  'STATUS: EKS cluster hhh-test from Sandbox Account'
    body = email
    message = {"Subject": {"Data":subject}, "Body": {"Html": {"Data":body}}}
    response = ses_client.send_email(Source = "xx.xxx@xxxxxx.com", Destination = {"ToAddresses": ["xx.xxx@xxxxxx.com"]}, Message = message)
    return response
