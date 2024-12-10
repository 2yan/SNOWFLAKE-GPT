openapi: 3.1.0
info:
  title: Snowflake SQL Executor API
  description: API to execute SQL queries or commands on Snowflake via a Lambda endpoint.
  version: 1.0.0
servers:
  - url: #ADD URL HERE
    description: Production Lambda endpoint for Snowflake SQL execution
paths:
  /:
    post:
      operationId: executeSql
      summary: Execute a SQL query or command on Snowflake
      description: Sends a request to the Lambda endpoint to execute a SQL query or command on Snowflake.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                sql_query:
                  type: string
                  description: The SQL query or command to be executed on Snowflake.
                kind:
                  type: string
                  enum: ['query', 'command']
                  description: Type of request; can be 'query' for retrieval or 'command' for modifications.
                token:
                  type: string
                  description: API authentication token.
              required:
                - sql_query
                - kind
                - token
      responses:
        '200':
          description: Successful execution response
          content:
            application/json:
              schema:
                type: object
                properties:
                  result:
                    type: string
                    description: Result of the SQL query or command.
        '400':
          description: Bad request, possibly due to missing or incorrect parameters
        '401':
          description: Unauthorized, due to an invalid or missing token
        '500':
          description: Server error or execution failure
