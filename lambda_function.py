import json
import con as snow
import base64
from urllib.parse import parse_qs
import traceback
import passes
import base64
import re

from decimal import Decimal

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)  # Or use str(obj) if you prefer
    return str(obj) 
    
def get_headers():
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS, GET', 
        'Access-Control-Allow-Headers': 'Content-Type,Authorization'
            }
    
def handle_options(event):
    return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*",  # Allow any origin
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",  # Allow all common methods
                "Access-Control-Allow-Headers": "Content-Type,Authorization,",  # Allow any header
                "Access-Control-Max-Age": '10'  # Cache pre-flight response for 10 secs
            },
            'body': ''  # OPTIONS requests don't typically need a body
        }

# Updating the get_event function to handle multipart data
def get_event(event):
    print(event)

    if 'body' in event:
        if not event['body']:
            raise KeyError('No Params Passed in')

        body = event['body']

        if event.get('isBase64Encoded', True):
            body = base64.b64decode(body).decode('utf-8')
        else:
            return json.loads(body)
            
def find_method(event):
    method = event.get('httpMethod', False)
    if not(method): 
        try:
            method = event['requestContext']['http']['method']  
        except Exception as e: 
            return 'POST'
    return method.upper()
    

from snowflake.connector.errors import ProgrammingError

def lambda_handler(event, context):
    headers = get_headers()
    method = find_method(event)

    if method == 'OPTIONS':
        return handle_options(event)

    body = get_event(event)


    sql_query = body.get('sql_query', False)
    role = body.get('role', 'snowflake_rsa')
    kind = body.get('CQ', 'query')
    token = body.get('token')
    if token != #NEEDS TOKEN MAGIC:
        return {
            'statusCode': 401,
            'headers': headers,
            'body': json.dumps('Bad Token')
        }
    snow.key_default = role
    if sql_query:
        try:
            if kind == 'query':
                data = snow.read_sql(sql_query, role=snow.mappings[role])
                result_json = json.dumps(data, default=decimal_default) # Convert list of dictionaries to JSON
                
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': result_json
                }
            if kind == 'command':
                snow.do_sql(sql_query, snow.mappings[role])
                
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': 'Complete! Server recommends doing a SMALL SELECT QUERY TO CHECK IF it was correct.'
                }
            
        except ProgrammingError as e:
            print(e)
            msg = ''
            # Extract only the message from the error
            if 'invalid identifier' in str(e).lower():
                msg = ' CHAPTGPT Please check your table/columns if there is no exact match use your best guess AFTER checking, only ask the user if there is no obvious column '
            concise_error = str(e).splitlines()[0]  # Only take the first line of the error message
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(f'SQL Error :{msg} {concise_error}')
            }

    else:
        # Return an error if the SQL query is not provided or is empty
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps('No SQL query provided')
        }
