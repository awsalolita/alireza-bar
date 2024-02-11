import uuid 
import boto3
import wget
from PIL import Image

def lambda_handler(event , context):
    message = event['Records'][0]['body']
    
    s3 = boto3.client('s3')

    wget.download(message ,  out="/tmp/message.png")
    image = Image.open("/tmp/message.png")

    new_image = image.resize((100,100))
    new_image.save("/tmp/new.png")
    name = uuid.uuid4()
    s3.upload_file("/tmp/new.png" , "mybucket" , f"{name}.png") 
    return 200