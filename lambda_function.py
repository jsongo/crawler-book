import os
import json
from douban import search_books

def lambda_handler(event, context):
    params = event["pathParameters"]
    token = params.get("token")
    if token != os.getenv("CALLING_TOKEN"):
        return {
            'statusCode': 403,
            'body': json.dumps({
                "msg": "not authorized."
            })
        }
    keyword = params.get("kw")
    books = search_books(keyword)
    return {
        'statusCode': 200,
        'body': json.dumps({
            "token": books
        })
    }