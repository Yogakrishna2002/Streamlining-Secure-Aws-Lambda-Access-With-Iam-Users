import json
import boto3

def lambda_handler(event, context):
    client = boto3.client("ses")

    for x in event["Records"]:
        ip = x["requestParameters"]["sourceIPAddress"]
        action = x["eventName"]
        bucket_name = x["s3"]["bucket"]["name"]
        object = x["s3"]["object"]["key"]

        subject = f"{str(action)} event from bucket {bucket_name}"
        body = f"""
        <br>
        This email is from AWS Lambda & SES to notify you regarding {action}.
        <br><br>
        <b>File Name:</b> {object} <br>
        <b>Event from IP:</b> {ip} <br><br>
        Thanks & Regards
        """

        message = {
            "Subject": {"Data": subject},
            "Body": {"Html": {"Data": body}}
        }

        response = client.send_email(
            Source="example@gmail.com",
            Destination={"ToAddresses": ["example@gmail.com"]},
            Message=message
        )

    return {"statusCode": 200, "body": json.dumps("Email sent successfully!")}
