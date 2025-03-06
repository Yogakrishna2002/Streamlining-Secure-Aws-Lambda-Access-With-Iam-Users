import boto3

topic_arn = "Mention The ARN"

def send_sns(message, subject):
    try:
        client = boto3.client("sns")
        result = client.publish(TopicArn=topic_arn, Message=message, Subject=subject)

        if result['ResponseMetadata']['HTTPStatusCode'] == 200:
            print(result)
            print("Notification sent successfully..!!!")
            return True

    except Exception as e:
        print("Error occurred while publishing notification, error: ", e)
    
    return False

def lambda_handler(event, context):
    print("Event collected: {}".format(event))

    for record in event['Records']:
        s3_bucket = record['s3']['bucket']['name']
        print("Bucket name: {}".format(s3_bucket))

        s3_key = record['s3']['object']['key']
        print("Bucket key name: {}".format(s3_key))

        from_path = "s3://{}/{}".format(s3_bucket, s3_key)
        print("File uploaded at: {}".format(from_path))

        message = "The file is uploaded at S3 bucket path {}".format(from_path)
        subject = "Process Completion Notification"

        SNSResult = send_sns(message, subject)
        
        if SNSResult:
            print("Notification Sent..")
            return SNSResult
        else:
            return False
