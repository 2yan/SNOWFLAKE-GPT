

def get_creds_from_aws():
    session = boto3.session.Session()
    client = session.client('secretsmanager')
    secret_name = "snowflake/credentials"
    response = client.get_secret_value(SecretId=secret_name)
    return eval(response['SecretString'])


def get_engine(role):
    global engine
    if engine:
        return engine

    creds = get_creds_from_aws()
    rsa_key = creds['rsa']
    password = creds['password'].encode()

    p_key = serialization.load_pem_private_key(
        rsa_key.encode(),
        password=password,
        backend=default_backend()
    )
    
    pkb = p_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    ctx = snowflake.connector.connect(
        user=creds['user'],
        account=account,
        role=role,
        private_key=pkb
    )
    engine = ctx
    return ctx


def __read_sql(query, role, warehouse):
    ctx = get_engine(role)
    cur = ctx.cursor()
    cur.execute(f'USE WAREHOUSE "{warehouse}"')
    cur.execute(query)
    columns = [desc[0] for desc in cur.description]
    data = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    return data


def do_sql(query, role):
    ctx = get_engine(role)
    cur = ctx.cursor()
    cur.execute(f'USE WAREHOUSE "{warehouse}"')
    cur.execute(query)
    cur.close()
    return


def read_sql(query, role=role, warehouse=warehouse, use_cache=False):
    def f():
        return __read_sql(query, role, warehouse)
    return f()
