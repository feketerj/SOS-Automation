### **User Note to Agent GPT:** 

**Document Purpose:**  

This document serves both as a reference and as a guide for action. It is an exact replica of the schema included in the Actions section of this GPT. The schema already includes the API key and the functions you can execute.  

**Current SOS API Key:** 9874995194174018881c567d92a2c4d2  

**HigherGov End Points:** The portion of the URL following SearchID=  

**Example URL:**  
https://www.highergov.com/contract-opportunity/?searchID=g6eFIE5ftdvpSvP-u1UJ-  

**End Points:**  
g6eFIE5ftdvpSvP-u1UJ-  

**Default Endpoints:**  
g6eFIE5ftdvpSvP-u1UJ-  

These endpoints indicate where you will carry out the task(s) if the user does not specify any endpoints.  

**User Defined Endpoints:**  
When the user provides a link and requests a search via API or endpoints, use the HigherGov schema and endpoint (the text after SearchID= in the URL).  

**Ambiguous Direction:**  
If the instruction or query is unclear, ask the user whether to use the API or to access the URL directly through browsing methods.


---

  
**Copy of Schema**

openapi: 3.1.0
info:
  title: Universal HigherGov API (Personal)
  version: 1.0.2
  description: |
    Universal HigherGov API Action.
    - Call any HigherGov GET endpoint by specifying the path (e.g. "opportunity", "contract", "grant", etc.) and query parameters.
    - Your API key is hardcoded.
    - Most endpoints support filtering by search_id, award_id, agency_key, NAICS, PSC, and many more. See https://www.highergov.com/api-external/docs/
servers:
  - url: https://www.highergov.com/api-external
paths:
  /{endpoint_path}/:
    get:
      operationId: getAnyEndpoint
      summary: Call any HigherGov endpoint (universal, with personal API key)
      description: |
        Pass any endpoint path and query params. API key is built-in.
        For example: 
        - endpoint_path = "opportunity", search_id = "<your-search-id>", etc.
        - endpoint_path = "contract", award_id = "<your-award-id>", etc.
        - For documents, endpoint_path = "document", related_key = "<from document_path field>"
      parameters:
        - in: path
          name: endpoint_path
          schema:
            type: string
          required: true
          description: The HigherGov API resource path (e.g. 'opportunity', 'contract', 'awardee', etc.)
        - in: query
          name: api_key
          schema:
            type: string
            default: "9874995194174018881c567d92a2c4d2"
          required: true
          description: Your HigherGov API key (pre-filled)
        - in: query
          name: search_id
          schema:
            type: string
          required: false
        - in: query
          name: award_id
          schema:
            type: string
          required: false
        - in: query
          name: awardee_key
          schema:
            type: integer
          required: false
        - in: query
          name: awardee_key_parent
          schema:
            type: integer
          required: false
        - in: query
          name: awardee_uei
          schema:
            type: string
          required: false
        - in: query
          name: awardee_uei_parent
          schema:
            type: string
          required: false
        - in: query
          name: agency_key
          schema:
            type: integer
          required: false
        - in: query
          name: funding_agency_key
          schema:
            type: integer
          required: false
        - in: query
          name: cfda_program_number
          schema:
            type: string
          required: false
        - in: query
          name: naics_code
          schema:
            type: string
          required: false
        - in: query
          name: psc_code
          schema:
            type: string
          required: false
        - in: query
          name: last_modified_date
          schema:
            type: string
            format: date
          required: false
        - in: query
          name: captured_date
          schema:
            type: string
            format: date
          required: false
        - in: query
          name: posted_date
          schema:
            type: string
            format: date
          required: false
        - in: query
          name: due_date
          schema:
            type: string
            format: date
          required: false
        - in: query
          name: page_number
          schema:
            type: integer
          required: false
        - in: query
          name: page_size
          schema:
            type: integer
          required: false
        - in: query
          name: ordering
          schema:
            type: string
          required: false
        - in: query
          name: source_type
          schema:
            type: string
          required: false
          description: Opportunity source type (sam, dibbs, sbir, grant, sled)
        - in: query
          name: opp_key
          schema:
            type: string
          required: false
        - in: query
          name: document_path
          schema:
            type: string
          required: false
        - in: query
          name: related_key
          schema:
            type: string
          required: false
          description: For document endpoint (use document_path field from opportunity result)
        # Add more query params as you wish
      responses:
        '200':
          description: JSON response from HigherGov
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
                    additionalProperties: true
                  links:
                    type: object
                    additionalProperties: true
                additionalProperties: true
        '400':
          description: Bad request (missing or invalid parameter)
        '403':
          description: Invalid API Key
        '404':
          description: Not found
