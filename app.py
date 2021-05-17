import hvac
import logging
import os
import json

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)





#input_values = """{
#  "batch_input": [
#    {
#      "transformation": "credit-card",
#      "value": "1111-2222-3333-4444"
#    },
#    {
#      "transformation": "credit-card",
#      "value": "0000-2222-3333-4444"
#    },
#    {
#      "transformation": "credit-card",
#      "value": "1111-2222-3333-5555"
#    }
#  ]
#}"""

def handler(event, context):
    role_name = 'mobile-pay'
    client = hvac.Client(url="http://172.31.3.227:8200")
    client.auth.aws.iam_login(
        access_key=os.getenv("AWS_ACCESS_KEY_ID"),
        secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        session_token=os.getenv("AWS_SESSION_TOKEN")
    )

    f = open('encode.json') 
    input_values = json.load(f)
    f.close()
    #print('the input looks like this %s:' % input_values)
    
    encoded_response = client.secrets.transform.encode(role_name=role_name, batch_input=input_values['batch_input'])
    print('The encoded response is: %s \n\n' % encoded_response['data']['batch_results'])
    f = open('payload.json', "a")
    f.write(encoded_response['data'])
    f.close()
    decoded_response = client.secrets.transform.decode(role_name=role_name, batch_input=encoded_response['data'])
    print ('the decoded response is: %s \n\n' % decoded_response)
    #print('The decoded response is: %s' % decoded_response['data'])

    return 1
