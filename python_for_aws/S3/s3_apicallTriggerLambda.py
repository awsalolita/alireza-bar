import json

def lambda_handler(event, context):
    # TODO implement
    print("*******************")
    
    

    rec = event['Records']

    
    for i in rec :
    # get bucket
        print(i['s3']['bucket']['name'])
    # get key
        print(i['s3']['object']['key'])
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
