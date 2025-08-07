**SOS-Schema-Copy**

**User Note to Agent GPT:** 

Document Purpose:  

This document serves both as a reference and as a guide for action. It is an exact replica of the schema included in the Actions section of this GPT. The schema already includes the API key and the functions you can execute.  

SOS API Key: 9874995194174018881c567d92a2c4d2  

HigherGov End Points: The portion of the URL following SearchID=  

Example URL:  
https://www.highergov.com/contract-opportunity/?searchID=g6eFIE5ftdvpSvP-u1UJ-  

End Points:  
g6eFIE5ftdvpSvP-u1UJ-  

Default Endpoints:  
g6eFIE5ftdvpSvP-u1UJ-  
These endpoints indicate where you will carry out the task(s) if the user does not specify any endpoints.  

User Defined Endpoints:  
When the user provides a link and requests a search via API or endpoints, use the HigherGov schema and endpoint (the text after SearchID= in the URL).  

Ambiguous Direction:  
If the instruction or query is unclear, ask the user whether to use the API or to access the URL directly through browsing methods.


---  


**Copy of Schema**

openapi: 3.1.0
info:
  title: Universal HigherGov API (SOS Hardwired)
  version: 1.0.3
  description: |
    Hardwired HigherGov API schema for Source One Spares GPT Agent.
    - `api_key` is no longer required in query parameters.
    - All calls automatically route through:
        https://www.highergov.com/api-external?api_key=9874995194174018881c567d92a2c4d2
    - This avoids MissingKwargsError and guarantees reliable execution.
servers:
  - url: https://www.highergov.com/api-external?api_key=9874995194174018881c567d92a2c4d2
paths:
  /{endpoint_path}/:
    get:
      operationId: getAnyEndpoint
      summary: Call any HigherGov endpoint (api_key hardwired)
      description: |
        Universal passthrough for any GET endpoint in the HigherGov API.
        Example usages:
        - /opportunity/?search_id=ABC123
        - /contract/?award_id=XYZ456
      parameters:
        - in: path
          name: endpoint_path
          required: true
          schema:
            type: string
          description: The HigherGov endpoint path (e.g., 'opportunity', 'contract', 'awardee')
        - in: query
          name: search_id
          required: false
          schema:
            type: string
        - in: query
          name: award_id
          required: false
          schema:
            type: string
        - in: query
          name: awardee_key
          required: false
          schema:
            type: integer
        - in: query
          name: awardee_uei
          required: false
          schema:
            type: string
        - in: query
          name: agency_key
          required: false
          schema:
            type: integer
        - in: query
          name: naics_code
          required: false
          schema:
            type: string
        - in: query
          name: psc_code
          required: false
          schema:
            type: string
        - in: query
          name: page_number
          required: false
          schema:
            type: integer
        - in: query
          name: page_size
          required: false
          schema:
            type: integer
        - in: query
          name: ordering
          required: false
          schema:
            type: string
        - in: query
          name: source_type
          required: false
          schema:
            type: string
        - in: query
          name: opp_key
          required: false
          schema:
            type: string
        - in: query
          name: related_key
          required: false
          schema:
            type: string
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: object
                properties:
                  results:
                    type: array
                    items:
                      type: object
                      additionalProperties: true
                  meta:
                    type: object
                  links:
                    type: object
        '400':
          description: Bad Request
        '403':
          description: Invalid API Key
        '404':
          description: Not Found
