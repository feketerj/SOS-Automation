openapi: 3.1.0
info:
  title: HigherGov Full API (Editable Search Mapping)
  version: 1.0.0
  description: |
    Saved Search Mapping Table:
      - Commercial Items:	tFDSNa5qi9S92K-bXbReY
      - NAICS Only:		g6eFIE5ftdvpSvP-u1UJ-
      - Boeing w/o SAR:		f4hotzFjwglPmdWGD3DDV
    (Update as needed. Use names in prompts, model will substitute search_id automatically.)
servers:
  - url: https://www.highergov.com
paths:
  /api-external/agency/:
    get:
      operationId: api_external_agency_list
      description: "Description:Federal and State and Local Agencies and hierarchies.\
        \  \n Update Frequency: Ad Hoc as new agencies are created or become relevant."
      parameters:
      - in: query
        name: agency_key
        schema:
          type: integer
        description: HigherGov Agency key
        examples:
          Select: {}
          Example:
            value: 1008
      - in: query
        name: api_key
        schema:
          type: string
          default: your-api-key-here
        description: API Key for authentication
        required: true
      - name: page_number
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - in: query
        name: page_size
        schema:
          type: string
          default: '10'
        description: Number of records returned per page (max 100)
      tags:
      - Agency
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedAgencyList'
          description: Success
        '400':
          description: Bad Request
        '403':
          description: Invalid API Key
        '404':
          description: Requested Record Not Found
  /api-external/awardee/:
    get:
      operationId: api_external_awardee_list
      description: "Description: Federal Awardees registered in SAM and DSBS.  \n\
        \ Update Frequency: Updated Monthly.  \n Update Check Field: registration_last_update_date"
      parameters:
      - in: query
        name: api_key
        schema:
          type: string
          default: your-api-key-here
        description: API Key for authentication
        required: true
      - in: query
        name: awardee_key_parent
        schema:
          type: integer
        description: HigherGov Awardee Key (Parent Level)
        examples:
          Select: {}
          Example:
            value: 10000002
      - in: query
        name: cage_code
        schema:
          type: string
        description: CAGE Code
        examples:
          Select: {}
          Example:
            value: 34ZB1
      - in: query
        name: ordering
        schema:
          type: string
          enum:
          - -last_update_date
          - last_update_date
        description: Which field to use when ordering the results.
      - name: page_number
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - in: query
        name: page_size
        schema:
          type: string
          default: '10'
        description: Number of records returned per page (max 100)
      - in: query
        name: primary_naics
        schema:
          type: string
        description: Primary registered NAICS Code
        examples:
          Select: {}
          Example:
            value: '541519'
      - in: query
        name: registration_last_update_date
        schema:
          type: string
          format: date
        description: The date the awardee last updated their registration in SAM
        examples:
          Select: {}
          Example:
            value: '2023-05-01'
      - in: query
        name: uei
        schema:
          type: string
        description: UEI
        examples:
          Select: {}
          Example:
            value: L61FBMJQ36A3
      tags:
      - Awardee
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedAwardeeList'
          description: Success
        '400':
          description: Bad Request
        '403':
          description: Invalid API Key
        '404':
          description: Requested Record Not Found
  /api-external/awardee-mp/:
    get:
      operationId: api_external_awardee_mp_list
      parameters:
      - in: query
        name: api_key
        schema:
          type: string
          default: your-api-key-here
        description: API Key for authentication
        required: true
      - in: query
        name: awardee_key_mentor
        schema:
          type: integer
        description: HigherGov Awardee Key of the Mentor
        examples:
          Select: {}
          Example:
            value: 10117613
      - in: query
        name: awardee_key_mentor_parent
        schema:
          type: integer
        description: HigherGov Awardee Key of the Mentor Parent
        examples:
          Select: {}
          Example:
            value: 10000006
      - in: query
        name: awardee_key_protege
        schema:
          type: integer
        description: HigherGov Awardee Key of the Protege
        examples:
          Select: {}
          Example:
            value: 10286130
      - in: query
        name: awardee_key_protege_parent
        schema:
          type: integer
        description: HigherGov Awardee Key of the Protege parent
        examples:
          Select: {}
          Example:
            value: 10286130
      - name: page_number
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - in: query
        name: page_size
        schema:
          type: string
          default: '10'
        description: Number of records returned per page (max 100)
      tags:
      - Awardee Mentor Protege
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedAwardeeMPList'
          description: Success
        '400':
          description: Bad Request
        '403':
          description: Invalid API Key
        '404':
          description: Requested Record Not Found
  /api-external/awardee-partnership/:
    get:
      operationId: api_external_awardee_partnership_list
      description: "Description: Teaming partnerships between different Awardees.\
        \  \n Update Frequency: Updated Weekly with new subaward data."
      parameters:
      - in: query
        name: api_key
        schema:
          type: string
          default: your-api-key-here
        description: API Key for authentication
        required: true
      - in: query
        name: awardee_key_prime
        schema:
          type: integer
        description: HigherGov Awardee Key of the prime recipient
        examples:
          Select: {}
          Example:
            value: 10115071
      - in: query
        name: awardee_key_prime_parent
        schema:
          type: integer
        description: HigherGov Awardee Key of the prime recipient parent
        examples:
          Select: {}
          Example:
            value: 10115071
      - in: query
        name: awardee_key_sub
        schema:
          type: integer
        description: HigherGov Awardee Key of the subawardee
        examples:
          Select: {}
          Example:
            value: 10115071
      - in: query
        name: awardee_key_sub_parent
        schema:
          type: integer
        description: HigherGov Awardee Key of the subawardee parent
        examples:
          Select: {}
          Example:
            value: 10115071
      - name: page_number
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - in: query
        name: page_size
        schema:
          type: string
          default: '10'
        description: Number of records returned per page (max 100)
      tags:
      - Awardee Partnership
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedAwardeePartnershipList'
          description: Success
        '400':
          description: Bad Request
        '403':
          description: Invalid API Key
        '404':
          description: Requested Record Not Found
  /api-external/contract/:
    get:
      operationId: api_external_contract_list
      description: "Description: Federal prime contract awards.  \n Update Frequency:\
        \ Daily by 2am (for two days prior) \n Update Check Field: last_modified_date."
      parameters:
      - in: query
        name: api_key
        schema:
          type: string
          default: your-api-key-here
        description: API Key for authentication
        required: true
      - in: query
        name: award_id
        schema:
          type: string
        description: The government Award ID
        examples:
          Select: {}
          Example:
            value: 70RDAD21D00000002-70CDCR22FR0000013
      - in: query
        name: awardee_key
        schema:
          type: integer
        description: HigherGov Awardee Key
        examples:
          Select: {}
          Example:
            value: 10115071
      - in: query
        name: awardee_key_parent
        schema:
          type: integer
        description: HigherGov Awardee Key (Parent Level)
        examples:
          Select: {}
          Example:
            value: 10000002
      - in: query
        name: awardee_uei
        schema:
          type: string
        description: Awardee UEI
        examples:
          Select: {}
          Example:
            value: SMNWM6HN79X5
      - in: query
        name: awardee_uei_parent
        schema:
          type: string
        description: Awardee UEI Parent
        examples:
          Select: {}
          Example:
            value: VF58HFRNGEL8
      - in: query
        name: awarding_agency_key
        schema:
          type: integer
        description: HigherGov Awarding Agency key
        examples:
          Select: {}
          Example:
            value: 463
      - in: query
        name: funding_agency_key
        schema:
          type: integer
        description: HigherGov Funding Agency key
        examples:
          Select: {}
          Example:
            value: 463
      - in: query
        name: last_modified_date
        schema:
          type: string
          format: date
        description: 'Last modified date filter (format: YYYY-MM-DD)'
        examples:
          Select: {}
          Example:
            value: '2023-05-01'
      - in: query
        name: naics_code
        schema:
          type: string
        description: Awards NAICS code
        examples:
          Select: {}
          Example:
            value: '541330'
      - in: query
        name: ordering
        schema:
          type: string
          enum:
          - -action_date
          - -current_total_value_of_award
          - -last_modified_date
          - -period_of_performance_potential_end_date
          - -potential_total_value_of_award
          - -total_dollars_obligated
          - action_date
          - current_total_value_of_award
          - last_modified_date
          - period_of_performance_potential_end_date
          - potential_total_value_of_award
          - total_dollars_obligated
        description: Which field to use when ordering the results.
      - name: page_number
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - in: query
        name: page_size
        schema:
          type: string
          default: '10'
        description: Number of records returned per page (max 100)
      - in: query
        name: parent_award_id
        schema:
          type: string
        description: The government Award ID of the parent Award
        examples:
          Select: {}
          Example:
            value: 70RDAD21D00000002
      - in: query
        name: psc_code
        schema:
          type: string
        description: PSC code
        examples:
          Select: {}
          Example:
            value: '8440'
      - in: query
        name: search_id
        schema:
          type: string
        description: HigherGov SearchID
        examples:
          Select: {}
          Example:
            value: WCZLN4aL1ZPSl8myr5vr8
      - in: query
        name: vehicle_key
        schema:
          type: integer
        description: HigherGov Vehicle key
        examples:
          Select: {}
          Example:
            value: 1008
      tags:
      - Federal Contract
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedFederal ContractList'
          description: Success
        '400':
          description: Bad Request
        '403':
          description: Invalid API Key
        '404':
          description: Requested Record Not Found
  /api-external/document/:
    get:
      operationId: api_external_document_list
      description: "Description: Returns paths for downloading the documents associated\
        \ with the opportunity. The related_key is required and is found in the document_path\
        \ field in the Opportunity endpoint. \n Update Frequency: Real time."
      parameters:
      - in: query
        name: api_key
        schema:
          type: string
          default: your-api-key-here
        description: API Key for authentication
        required: true
      - name: ordering
        required: false
        in: query
        description: Which field to use when ordering the results.
        schema:
          type: string
      - name: page_number
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - in: query
        name: page_size
        schema:
          type: string
          default: '10'
        description: Number of records returned per page (max 100)
      - in: query
        name: related_key
        schema:
          type: string
        description: Document Key
        required: true
        examples:
          Select: {}
          Example:
            value: 66cab3907c5b4cfcafbf102c5bb17eb6
      tags:
      - Document
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedFileTrackerList'
          description: Success
        '400':
          description: Bad Request
        '403':
          description: Invalid API Key
        '404':
          description: Requested Record Not Found
  /api-external/grant/:
    get:
      operationId: api_external_grant_list
      description: "Description: Federal prime grant awards.  \n Update Frequency:\
        \ Daily by 2am (for two days prior) \n Update Check Field: last_modified_date."
      parameters:
      - in: query
        name: api_key
        schema:
          type: string
          default: your-api-key-here
        description: API Key for authentication
        required: true
      - in: query
        name: awardee_key
        schema:
          type: integer
        description: HigherGov Awardee Key
        examples:
          Select: {}
          Example:
            value: 10115071
      - in: query
        name: awardee_key_parent
        schema:
          type: integer
        description: HigherGov Awardee Key (Parent Level)
        examples:
          Select: {}
          Example:
            value: 10000002
      - in: query
        name: awardee_uei
        schema:
          type: string
        description: Awardee UEI
        examples:
          Select: {}
          Example:
            value: SMNWM6HN79X5
      - in: query
        name: awardee_uei_parent
        schema:
          type: string
        description: Awardee UEI Parent
        examples:
          Select: {}
          Example:
            value: VF58HFRNGEL8
      - in: query
        name: awarding_agency_key
        schema:
          type: integer
        description: HigherGov Awarding Agency key
        examples:
          Select: {}
          Example:
            value: 463
      - in: query
        name: cfda_program_number
        schema:
          type: string
        description: Grant Program Number (CFDA)
        examples:
          Select: {}
          Example:
            value: '93.778'
      - in: query
        name: funding_agency_key
        schema:
          type: integer
        description: HigherGov Funding Agency key
        examples:
          Select: {}
          Example:
            value: 463
      - in: query
        name: last_modified_date
        schema:
          type: string
          format: date
        description: 'Last modified date filter (format: YYYY-MM-DD)'
        examples:
          Select: {}
          Example:
            value: '2023-05-01'
      - in: query
        name: ordering
        schema:
          type: string
          enum:
          - -action_date
          - -last_modified_date
          - -total_obligated_amount
          - action_date
          - last_modified_date
          - total_obligated_amount
        description: Which field to use when ordering the results.
      - name: page_number
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - in: query
        name: page_size
        schema:
          type: string
          default: '10'
        description: Number of records returned per page (max 100)
      - in: query
        name: search_id
        schema:
          type: string
        description: HigherGov SearchID
        examples:
          Select: {}
          Example:
            value: goLCRhe9oxTk2nH4ByYo0
      tags:
      - Federal Grant
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedFederal GrantList'
          description: Success
        '400':
          description: Bad Request
        '403':
          description: Invalid API Key
        '404':
          description: Requested Record Not Found
  /api-external/grant-program/:
    get:
      operationId: api_external_grant_program_list
      description: "Description:Government Assistance Programs (Grant Programs or\
        \ CFDAs).  \n Update Frequency: Ad hoc as new programs are released, typically\
        \ monthly."
      parameters:
      - in: query
        name: agency_key
        schema:
          type: integer
        description: HigherGov Agency key
        examples:
          Select: {}
          Example:
            value: 1008
      - in: query
        name: api_key
        schema:
          type: string
          default: your-api-key-here
        description: API Key for authentication
        required: true
      - in: query
        name: cfda_program_number
        schema:
          type: string
        description: CFDA Program Number for the grant program
        examples:
          Select: {}
          Example:
            value: '10.854'
      - name: page_number
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - in: query
        name: page_size
        schema:
          type: string
          default: '10'
        description: Number of records returned per page (max 100)
      tags:
      - Grant Program
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedAssistanceList'
          description: Success
        '400':
          description: Bad Request
        '403':
          description: Invalid API Key
        '404':
          description: Requested Record Not Found
  /api-external/idv/:
    get:
      operationId: api_external_idv_list
      description: "Description: Federal prime IDV awards.  \n Update Frequency: Daily\
        \ by 2am (for two days prior) \n Update Check Field: last_modified_date."
      parameters:
      - in: query
        name: api_key
        schema:
          type: string
          default: your-api-key-here
        description: API Key for authentication
        required: true
      - in: query
        name: award_id
        schema:
          type: string
        description: The government Award ID
        examples:
          Select: {}
          Example:
            value: GS00F098CA-75R60223A00019
      - in: query
        name: awardee_key
        schema:
          type: integer
        description: HigherGov Awardee Key
        examples:
          Select: {}
          Example:
            value: 10115071
      - in: query
        name: awardee_key_parent
        schema:
          type: integer
        description: HigherGov Awardee Key (Parent Level)
        examples:
          Select: {}
          Example:
            value: 10000002
      - in: query
        name: awardee_uei
        schema:
          type: string
        description: Awardee UEI
        examples:
          Select: {}
          Example:
            value: SMNWM6HN79X5
      - in: query
        name: awardee_uei_parent
        schema:
          type: string
        description: Awardee UEI Parent
        examples:
          Select: {}
          Example:
            value: VF58HFRNGEL8
      - in: query
        name: awarding_agency_key
        schema:
          type: integer
        description: HigherGov Awarding Agency key
        examples:
          Select: {}
          Example:
            value: 463
      - in: query
        name: funding_agency_key
        schema:
          type: integer
        description: HigherGov Funding Agency key
        examples:
          Select: {}
          Example:
            value: 463
      - in: query
        name: last_modified_date
        schema:
          type: string
          format: date
        description: 'Last modified date filter (format: YYYY-MM-DD)'
        examples:
          Select: {}
          Example:
            value: '2023-05-01'
      - in: query
        name: naics_code
        schema:
          type: string
        description: Awards NAICS code
        examples:
          Select: {}
          Example:
            value: '541330'
      - in: query
        name: ordering
        schema:
          type: string
          enum:
          - -action_date
          - -last_modified_date_ordering
          - -ordering_period_end_date
          - -potential_total_value_of_award
          - action_date
          - last_modified_date_ordering
          - ordering_period_end_date
          - potential_total_value_of_award
        description: Which field to use when ordering the results.
      - name: page_number
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - in: query
        name: page_size
        schema:
          type: string
          default: '10'
        description: Number of records returned per page (max 100)
      - in: query
        name: parent_award_id
        schema:
          type: string
        description: The government Award ID of the parent Award
        examples:
          Select: {}
          Example:
            value: GS00F098CA
      - in: query
        name: psc_code
        schema:
          type: string
        description: PSC code
        examples:
          Select: {}
          Example:
            value: '8440'
      - in: query
        name: vehicle_key
        schema:
          type: integer
        description: HigherGov Vehicle key
        examples:
          Select: {}
          Example:
            value: 1008
      tags:
      - Federal IDV
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedFederal IDVList'
          description: Success
        '400':
          description: Bad Request
        '403':
          description: Invalid API Key
        '404':
          description: Requested Record Not Found
  /api-external/naics/:
    get:
      operationId: api_external_naics_list
      description: "Description: North American Industry Classification System (NAICS)\
        \ codes.  \n Update Frequency: Updated Ad Hoc when codes added or removed\
        \ by the Census Bureau or the SBA changes size standards"
      parameters:
      - in: query
        name: api_key
        schema:
          type: string
          default: your-api-key-here
        description: API Key for authentication
        required: true
      - in: query
        name: naics_code
        schema:
          type: string
        description: Awards NAICS code
        examples:
          Select: {}
          Example:
            value: '541330'
      - in: query
        name: ordering
        schema:
          type: string
          enum:
          - -naics_code
          - naics_code
        description: Which field to use when ordering the results.
      - name: page_number
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - in: query
        name: page_size
        schema:
          type: string
          default: '10'
        description: Number of records returned per page (max 100)
      tags:
      - NAICS
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedNAICSList'
          description: Success
        '400':
          description: Bad Request
        '403':
          description: Invalid API Key
        '404':
          description: Requested Record Not Found
  /api-external/nsn/:
    get:
      operationId: api_external_nsn_list
      description: 'Description: NATO Stock Number Lookup.'
      parameters:
      - in: query
        name: api_key
        schema:
          type: string
          default: your-api-key-here
        description: API Key for authentication
        required: true
      - in: query
        name: cage_code
        schema:
          type: string
        description: Supplier CAGE
        examples:
          Select: {}
          Example:
            value: '95403'
      - in: query
        name: nsn
        schema:
          type: string
        description: National Stock Number (NSN)
        examples:
          Select: {}
          Example:
            value: '6505013306269'
      - in: query
        name: ordering
        schema:
          type: string
          enum:
          - -last_price
          - -opp_count
          - -unit_price
          - last_price
          - opp_count
          - unit_price
        description: Which field to use when ordering the results.
      - name: page_number
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - in: query
        name: page_size
        schema:
          type: string
          default: '10'
        description: Number of records returned per page (max 100)
      tags:
      - NSN
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedNSNList'
          description: Success
        '400':
          description: Bad Request
        '403':
          description: Invalid API Key
        '404':
          description: Requested Record Not Found
  /api-external/opportunity/:
    get:
      operationId: api_external_opportunity_list
      description: "Description: Includes federal Contract, DIBBS, Grants, and State\
        \ and Local Opportunities.  \n Update Frequency: Updated every 30 minutes\
        \ \n Update Check Field: captured_date."
      parameters:
      - in: query
        name: agency_key
        schema:
          type: integer
        description: HigherGov Agency key
        examples:
          Select: {}
          Example:
            value: 463
      - in: query
        name: api_key
        schema:
          type: string
          default: your-api-key-here
        description: API Key for authentication
        required: true
      - in: query
        name: captured_date
        schema:
          type: string
          format: date
        description: Date the opportunity was added to HigherGov
        examples:
          Select: {}
          Example:
            value: '2023-05-01'
      - in: query
        name: opp_key
        schema:
          type: string
        description: The HigherGov opportunity key
        examples:
          Select: {}
          Example:
            value: 7ae9d947f71358afb372cd5f355fb447
      - in: query
        name: ordering
        schema:
          type: string
          enum:
          - -captured_date
          - -due_date
          - -posted_date
          - captured_date
          - due_date
          - posted_date
        description: Which field to use when ordering the results.
      - name: page_number
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - in: query
        name: page_size
        schema:
          type: string
          default: '10'
        description: Number of records returned per page (max 100)
      - in: query
        name: posted_date
        schema:
          type: string
          format: date
        description: Date the opportunity was posted by the agency in YYYY-MM-DD format
        examples:
          Select: {}
          Example:
            value: '2023-05-01'
      - in: query
        name: search_id
        schema:
          type: string
        description: 'HigherGov SearchID.  The following search search fields are
          currently supported: Active, Applicant Type (Grant Only), Agency, CAGE Code,
          Date Due, Date Posted, Funding Category (Grant Only), Funding Instrument
          (Grant Only), Grant Program, Keywords, NAICS, NSN, Place of Performance
          (Federal Contracts Only), PSC, Set Aside, State (State and Local Only),
          and Value Range'
        examples:
          Select: {}
          Example:
            value: n3K_MPmMi6Z1TzSEXlUhp
      - in: query
        name: source_id
        schema:
          type: string
        description: The source opportunity ID
        examples:
          Select: {}
          Example:
            value: 47PG1024R1000
      - in: query
        name: source_type
        schema:
          type: string
        description: Opportunity source type (sam, dibbs, sbir, grant, sled)
        examples:
          Select: {}
          Example:
            value: sam
      - in: query
        name: version_key
        schema:
          type: string
        description: The HigherGov opportunity version key
        examples:
          Select: {}
          Example:
            value: c68426d1aba54dd381dc5b1487b002c0
      tags:
      - Opportunity
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedOpportunityList'
          description: Success
        '400':
          description: Bad Request
        '403':
          description: Invalid API Key
        '404':
          description: Requested Record Not Found
  /api-external/people/:
    get:
      operationId: api_external_people_list
      description: "Description: Federal and State and Local People.  \n Update Frequency:\
        \ Updated in real time. \n Update Check Field: as_of_date."
      parameters:
      - in: query
        name: api_key
        schema:
          type: string
          default: your-api-key-here
        description: API Key for authentication
        required: true
      - in: query
        name: contact_email
        schema:
          type: string
        description: Email address
        examples:
          Select: {}
          Example:
            value: allenks@state.gov
      - in: query
        name: ordering
        schema:
          type: string
          enum:
          - -last_seen
          - last_seen
        description: Which field to use when ordering the results.
      - name: page_number
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - in: query
        name: page_size
        schema:
          type: string
          default: '10'
        description: Number of records returned per page (max 100)
      tags:
      - People
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedPeopleList'
          description: Success
        '400':
          description: Bad Request
        '403':
          description: Invalid API Key
        '404':
          description: Requested Record Not Found
  /api-external/psc/:
    get:
      operationId: api_external_psc_list
      description: "Description: Product Service Codes (PSC) Codes.  \n Update Frequency:\
        \ Updated Ad Hoc when codes added or removed"
      parameters:
      - in: query
        name: api_key
        schema:
          type: string
          default: your-api-key-here
        description: API Key for authentication
        required: true
      - name: page_number
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - in: query
        name: page_size
        schema:
          type: string
          default: '10'
        description: Number of records returned per page (max 100)
      - in: query
        name: psc_code
        schema:
          type: string
        description: PSC code
        examples:
          Select: {}
          Example:
            value: '8440'
      tags:
      - PSC
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedPSCList'
          description: Success
        '400':
          description: Bad Request
        '403':
          description: Invalid API Key
        '404':
          description: Requested Record Not Found
  /api-external/subcontract/:
    get:
      operationId: api_external_subcontract_list
      description: "Description: Federal prime subcontract award data.  \n Update\
        \ Frequency: Updated weekly.  \n Update Check Field: last_modified_date (note\
        \ that data is often reported late by prime awardees and we recommend periodically\
        \ looking back over the prior year to fully sync new records)."
      parameters:
      - in: query
        name: api_key
        schema:
          type: string
          default: your-api-key-here
        description: API Key for authentication
        required: true
      - in: query
        name: awardee_key
        schema:
          type: integer
        description: HigherGov Awardee Key
        examples:
          Select: {}
          Example:
            value: 10115071
      - in: query
        name: awardee_key_parent
        schema:
          type: integer
        description: HigherGov Awardee Key (Parent Level)
        examples:
          Select: {}
          Example:
            value: 10000002
      - in: query
        name: awardee_uei
        schema:
          type: string
        description: Awardee UEI
        examples:
          Select: {}
          Example:
            value: SMNWM6HN79X5
      - in: query
        name: awardee_uei_parent
        schema:
          type: string
        description: Awardee UEI Parent
        examples:
          Select: {}
          Example:
            value: VF58HFRNGEL8
      - in: query
        name: awarding_agency_key
        schema:
          type: integer
        description: HigherGov Awarding Agency key
        examples:
          Select: {}
          Example:
            value: 463
      - in: query
        name: funding_agency_key
        schema:
          type: integer
        description: HigherGov Funding Agency key
        examples:
          Select: {}
          Example:
            value: 463
      - in: query
        name: last_modified_date
        schema:
          type: string
          format: date
        description: 'Last modified date filter (format: YYYY-MM-DD)'
        examples:
          Select: {}
          Example:
            value: '2023-05-01'
      - in: query
        name: ordering
        schema:
          type: string
          enum:
          - -last_modified_date
          - -subaward_action_date
          - -subaward_amount_total
          - last_modified_date
          - subaward_action_date
          - subaward_amount_total
        description: Which field to use when ordering the results.
      - name: page_number
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - in: query
        name: page_size
        schema:
          type: string
          default: '10'
        description: Number of records returned per page (max 100)
      tags:
      - Federal Subcontract
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedFederal SubcontractList'
          description: Success
        '400':
          description: Bad Request
        '403':
          description: Invalid API Key
        '404':
          description: Requested Record Not Found
  /api-external/subgrant/:
    get:
      operationId: api_external_subgrant_list
      description: "Description: Federal prime subgrant award data.  \n Update Frequency:\
        \ Updated weekly.  \n Update Check Field: last_modified_date (note that data\
        \ is often reported late by prime awardees and we recommend periodically looking\
        \ back over the prior year to fully sync new records)."
      parameters:
      - in: query
        name: api_key
        schema:
          type: string
          default: your-api-key-here
        description: API Key for authentication
        required: true
      - in: query
        name: awardee_key
        schema:
          type: integer
        description: HigherGov Awardee Key
        examples:
          Select: {}
          Example:
            value: 10115071
      - in: query
        name: awardee_key_parent
        schema:
          type: integer
        description: HigherGov Awardee Key (Parent Level)
        examples:
          Select: {}
          Example:
            value: 10000002
      - in: query
        name: awardee_uei
        schema:
          type: string
        description: Awardee UEI
        examples:
          Select: {}
          Example:
            value: SMNWM6HN79X5
      - in: query
        name: awardee_uei_parent
        schema:
          type: string
        description: Awardee UEI Parent
        examples:
          Select: {}
          Example:
            value: VF58HFRNGEL8
      - in: query
        name: awarding_agency_key
        schema:
          type: integer
        description: HigherGov Awarding Agency key
        examples:
          Select: {}
          Example:
            value: 463
      - in: query
        name: funding_agency_key
        schema:
          type: integer
        description: HigherGov Funding Agency key
        examples:
          Select: {}
          Example:
            value: 463
      - in: query
        name: last_modified_date
        schema:
          type: string
          format: date
        description: 'Last modified date filter (format: YYYY-MM-DD)'
        examples:
          Select: {}
          Example:
            value: '2023-05-01'
      - in: query
        name: ordering
        schema:
          type: string
          enum:
          - -last_modified_date
          - -subaward_action_date
          - -subaward_amount_total
          - last_modified_date
          - subaward_action_date
          - subaward_amount_total
        description: Which field to use when ordering the results.
      - name: page_number
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - in: query
        name: page_size
        schema:
          type: string
          default: '10'
        description: Number of records returned per page (max 100)
      tags:
      - Federal Subgrant
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedFederal SubgrantList'
          description: Success
        '400':
          description: Bad Request
        '403':
          description: Invalid API Key
        '404':
          description: Requested Record Not Found
  /api-external/vehicle/:
    get:
      operationId: api_external_vehicle_list
      description: "Description: Federal multi-award contract vehicles.  \n Update\
        \ Frequency: Updated ad hoc as new awards are made."
      parameters:
      - in: query
        name: api_key
        schema:
          type: string
          default: your-api-key-here
        description: API Key for authentication
        required: true
      - in: query
        name: ordering
        schema:
          type: string
          enum:
          - -award_date
          - award_date
        description: Which field to use when ordering the results.
      - name: page_number
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - in: query
        name: page_size
        schema:
          type: string
          default: '10'
        description: Number of records returned per page (max 100)
      - in: query
        name: vehicle_key
        schema:
          type: integer
        description: HigherGov Vehicle key
        examples:
          Select: {}
          Example:
            value: 1008
      tags:
      - Vehicle
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedVehicleList'
          description: Success
        '400':
          description: Bad Request
        '403':
          description: Invalid API Key
        '404':
          description: Requested Record Not Found
components:
  schemas:
    Agency:
      type: object
      description: |-
        A type of `ModelSerializer` that uses hyperlinked relationships instead
        of primary key relationships. Specifically:

        * A 'url' field is included instead of the 'id' field.
        * Relationships to other instances are hyperlinks, instead of primary keys.

        Included Mixins:

        * A mixin class to enable sparse fieldsets is included
        * A mixin class to enable validation of included resources is included
      properties:
        agency_key:
          type: integer
          nullable: true
        agency_name:
          type: string
          nullable: true
        agency_abbreviation:
          type: string
          nullable: true
        agency_type:
          type: string
          nullable: true
        defense_flag:
          type: boolean
          nullable: true
        level_1:
          type: string
          readOnly: true
        level_2:
          type: string
          readOnly: true
        level_3:
          type: string
          readOnly: true
        level_4:
          type: string
          readOnly: true
        level_5:
          type: string
          readOnly: true
        level_6:
          type: string
          readOnly: true
        level_7:
          type: string
          readOnly: true
        path:
          type: string
          readOnly: true
      required:
      - agency_abbreviation
      - agency_key
      - agency_name
      - agency_type
      - defense_flag
      - level_1
      - level_2
      - level_3
      - level_4
      - level_5
      - level_6
      - level_7
      - path
    AgencySimple:
      type: object
      description: |-
        A type of `ModelSerializer` that uses hyperlinked relationships instead
        of primary key relationships. Specifically:

        * A 'url' field is included instead of the 'id' field.
        * Relationships to other instances are hyperlinks, instead of primary keys.

        Included Mixins:

        * A mixin class to enable sparse fieldsets is included
        * A mixin class to enable validation of included resources is included
      properties:
        agency_key:
          type: integer
        agency_name:
          type: string
          nullable: true
        agency_abbreviation:
          type: string
          nullable: true
        agency_type:
          type: string
          nullable: true
        path:
          type: string
          readOnly: true
      required:
      - agency_abbreviation
      - agency_key
      - agency_name
      - agency_type
      - path
    Assistance:
      type: object
      description: |-
        A type of `ModelSerializer` that uses hyperlinked relationships instead
        of primary key relationships. Specifically:

        * A 'url' field is included instead of the 'id' field.
        * Relationships to other instances are hyperlinks, instead of primary keys.

        Included Mixins:

        * A mixin class to enable sparse fieldsets is included
        * A mixin class to enable validation of included resources is included
      properties:
        cfda_program_number:
          type: string
        active:
          type: boolean
        program_title:
          type: string
          nullable: true
        popular_program_title:
          type: string
          nullable: true
        primary_agency:
          $ref: '#/components/schemas/AgencySimple'
        date_modified:
          type: string
          format: date
          nullable: true
        date_posted:
          type: string
          format: date
          nullable: true
        cfda_objective:
          type: string
          nullable: true
        type_of_assistance:
          type: string
          nullable: true
        applicant_eligibility:
          type: string
          nullable: true
        beneficiary_eligibility:
          type: string
          nullable: true
        path:
          type: string
          readOnly: true
      required:
      - applicant_eligibility
      - beneficiary_eligibility
      - cfda_objective
      - cfda_program_number
      - date_modified
      - date_posted
      - path
      - popular_program_title
      - primary_agency
      - program_title
      - type_of_assistance
    Awardee:
      type: object
      description: |-
        A type of `ModelSerializer` that uses hyperlinked relationships instead
        of primary key relationships. Specifically:

        * A 'url' field is included instead of the 'id' field.
        * Relationships to other instances are hyperlinks, instead of primary keys.

        Included Mixins:

        * A mixin class to enable sparse fieldsets is included
        * A mixin class to enable validation of included resources is included
      properties:
        awardee_key:
          type: integer
        awardee_key_parent:
          $ref: '#/components/schemas/AwardeeSimple'
        parent_flag:
          type: boolean
          nullable: true
        clean_name:
          type: string
          nullable: true
        legal_business_name:
          type: string
          nullable: true
        dba_name:
          type: string
          nullable: true
        entity_division_name:
          type: string
          nullable: true
        entity_division_number:
          type: string
          nullable: true
        uei:
          type: string
          nullable: true
        cage_code:
          type: string
          nullable: true
        purpose_of_registration:
          type: string
          nullable: true
        initial_registration_date:
          type: string
          format: date
          nullable: true
        registration_expiration_date:
          type: string
          format: date
          nullable: true
        registration_last_update_date:
          type: string
          format: date
          nullable: true
        registration_activation_date:
          type: string
          format: date
          nullable: true
        year_founded:
          type: string
          nullable: true
        employee_count:
          type: string
          nullable: true
        physical_address_line_1:
          type: string
          nullable: true
        physical_address_line_2:
          type: string
          nullable: true
        physical_address_city:
          type: string
          nullable: true
        physical_address_province_or_state:
          type: string
          nullable: true
        physical_address_zip_postal_code:
          type: string
          nullable: true
        physical_address_zip_code_4:
          type: string
          nullable: true
        physical_address_country_code:
          type: string
          nullable: true
        govt_bus_poc_first_name:
          type: string
          nullable: true
        govt_bus_poc_last_name:
          type: string
          nullable: true
        govt_bus_poc_title:
          type: string
          nullable: true
        govt_bus_poc_st_add_1:
          type: string
          nullable: true
        govt_bus_poc_st_add_2:
          type: string
          nullable: true
        govt_bus_poc_city:
          type: string
          nullable: true
        govt_bus_poc_zip_postal_code:
          type: string
          nullable: true
        govt_bus_state_or_province:
          type: string
          nullable: true
        govt_bus_poc_country_code:
          type: string
          nullable: true
        website:
          type: string
          nullable: true
        primary_naics:
          allOf:
          - $ref: '#/components/schemas/Naics'
          readOnly: true
        naics_codes:
          type: string
          readOnly: true
        psc_codes:
          type: string
          readOnly: true
        bus_type_info:
          type: string
          readOnly: true
        path:
          type: string
          readOnly: true
      required:
      - awardee_key
      - awardee_key_parent
      - bus_type_info
      - cage_code
      - clean_name
      - dba_name
      - employee_count
      - entity_division_name
      - entity_division_number
      - govt_bus_poc_city
      - govt_bus_poc_country_code
      - govt_bus_poc_first_name
      - govt_bus_poc_last_name
      - govt_bus_poc_st_add_1
      - govt_bus_poc_st_add_2
      - govt_bus_poc_title
      - govt_bus_poc_zip_postal_code
      - govt_bus_state_or_province
      - initial_registration_date
      - legal_business_name
      - naics_codes
      - parent_flag
      - path
      - physical_address_city
      - physical_address_country_code
      - physical_address_line_1
      - physical_address_line_2
      - physical_address_province_or_state
      - physical_address_zip_code_4
      - physical_address_zip_postal_code
      - primary_naics
      - psc_codes
      - purpose_of_registration
      - registration_activation_date
      - registration_expiration_date
      - registration_last_update_date
      - uei
      - website
      - year_founded
    AwardeeMP:
      type: object
      properties:
        awardee_key_protege:
          $ref: '#/components/schemas/AwardeeSimple'
        awardee_key_mentor:
          $ref: '#/components/schemas/AwardeeSimple'
        awardee_key_protege_parent:
          $ref: '#/components/schemas/AwardeeSimple'
        awardee_key_mentor_parent:
          $ref: '#/components/schemas/AwardeeSimple'
        active_flag:
          type: boolean
        primary_naics:
          allOf:
          - $ref: '#/components/schemas/Naics'
          readOnly: true
      required:
      - active_flag
      - awardee_key_mentor
      - awardee_key_mentor_parent
      - awardee_key_protege
      - awardee_key_protege_parent
      - primary_naics
    AwardeePartnership:
      type: object
      properties:
        awardee_key_prime:
          $ref: '#/components/schemas/AwardeeSimple'
        awardee_key_sub:
          $ref: '#/components/schemas/AwardeeSimple'
        awardee_key_prime_parent:
          $ref: '#/components/schemas/AwardeeSimple'
        awardee_key_sub_parent:
          $ref: '#/components/schemas/AwardeeSimple'
        number_of_awards:
          type: integer
        total_awards:
          type: number
          format: double
        most_recent_date:
          type: string
          format: date
          nullable: true
        relationship_type:
          type: string
          nullable: true
      required:
      - awardee_key_prime
      - awardee_key_prime_parent
      - awardee_key_sub
      - awardee_key_sub_parent
      - most_recent_date
      - number_of_awards
      - relationship_type
      - total_awards
    AwardeeSimple:
      type: object
      description: |-
        A type of `ModelSerializer` that uses hyperlinked relationships instead
        of primary key relationships. Specifically:

        * A 'url' field is included instead of the 'id' field.
        * Relationships to other instances are hyperlinks, instead of primary keys.

        Included Mixins:

        * A mixin class to enable sparse fieldsets is included
        * A mixin class to enable validation of included resources is included
      properties:
        awardee_key:
          type: integer
        clean_name:
          type: string
          nullable: true
        uei:
          type: string
          nullable: true
        cage_code:
          type: string
          nullable: true
        path:
          type: string
          readOnly: true
      required:
      - awardee_key
      - cage_code
      - clean_name
      - path
      - uei
    Federal Contract:
      type: object
      description: |-
        A type of `ModelSerializer` that uses hyperlinked relationships instead
        of primary key relationships. Specifically:

        * A 'url' field is included instead of the 'id' field.
        * Relationships to other instances are hyperlinks, instead of primary keys.

        Included Mixins:

        * A mixin class to enable sparse fieldsets is included
        * A mixin class to enable validation of included resources is included
      properties:
        award_id:
          type: string
        parent_award_id:
          type: string
          nullable: true
        latest_transaction_key:
          type: string
          nullable: true
        last_modified_date:
          type: string
          format: date
          nullable: true
          description: 'Date (format: YYYY-MM-DD)'
        latest_action_date:
          type: string
          format: date
        latest_action_date_fiscal_year:
          type: integer
          nullable: true
        awardee:
          allOf:
          - $ref: '#/components/schemas/AwardeeSimple'
          nullable: true
        awardee_parent:
          allOf:
          - $ref: '#/components/schemas/AwardeeSimple'
          nullable: true
        awarding_agency:
          $ref: '#/components/schemas/AgencySimple'
        funding_agency:
          $ref: '#/components/schemas/AgencySimple'
        vehicle:
          allOf:
          - $ref: '#/components/schemas/VehicleSimple'
          nullable: true
        federal_supply_schedule_award_id:
          type: string
          nullable: true
        parent_award_type:
          type: string
          nullable: true
        period_of_performance_start_date:
          type: string
          format: date
          nullable: true
        period_of_performance_current_end_date:
          type: string
          format: date
          nullable: true
        period_of_performance_potential_end_date:
          type: string
          format: date
          nullable: true
        total_dollars_obligated:
          type: number
          format: double
          nullable: true
        current_total_value_of_award:
          type: number
          format: double
          nullable: true
        potential_total_value_of_award:
          type: number
          format: double
          nullable: true
        award_type:
          type: string
          nullable: true
        award_description_original:
          type: string
          nullable: true
        alt_description:
          type: string
          nullable: true
        solicitation_identifier:
          type: string
          nullable: true
        related_opportunity_title:
          type: string
          nullable: true
        psc_code:
          allOf:
          - $ref: '#/components/schemas/PSC'
          readOnly: true
        naics_code:
          allOf:
          - $ref: '#/components/schemas/NAICSSimple'
          readOnly: true
        primary_place_of_performance_zip:
          type: string
          nullable: true
        primary_place_of_performance_county_name:
          type: string
          nullable: true
        primary_place_of_performance_city_name:
          type: string
          nullable: true
        primary_place_of_performance_state_code:
          type: string
          nullable: true
        primary_place_of_performance_state_name:
          type: string
          nullable: true
        primary_place_of_performance_country_name:
          type: string
          nullable: true
        type_of_agreement:
          type: string
          nullable: true
        type_of_contract_pricing_description:
          type: string
          nullable: true
        national_interest_action:
          type: string
          nullable: true
        defense_program:
          type: string
          nullable: true
        other_statutory_authority:
          type: string
          nullable: true
        dod_claimant_program_code:
          type: string
          nullable: true
        subcontracting_plan:
          type: string
          nullable: true
        research:
          type: string
          nullable: true
        type_of_set_aside:
          type: string
          nullable: true
        number_of_offers_received:
          type: string
          nullable: true
        extent_competed:
          type: string
          nullable: true
        solicitation_procedures:
          type: string
          nullable: true
        evaluated_preference:
          type: string
          nullable: true
        clinger_cohen_act_planning:
          type: string
          nullable: true
        fair_opportunity_limited_sources:
          type: string
          nullable: true
        other_than_full_and_open_competition:
          type: string
          nullable: true
        created_by:
          allOf:
          - $ref: '#/components/schemas/PeopleSimple'
          nullable: true
        last_modified_by:
          allOf:
          - $ref: '#/components/schemas/PeopleSimple'
          nullable: true
        approved_by:
          allOf:
          - $ref: '#/components/schemas/PeopleSimple'
          nullable: true
        path:
          type: string
          readOnly: true
      required:
      - alt_description
      - approved_by
      - award_description_original
      - award_id
      - award_type
      - awardee
      - awardee_parent
      - awarding_agency
      - clinger_cohen_act_planning
      - created_by
      - current_total_value_of_award
      - defense_program
      - dod_claimant_program_code
      - evaluated_preference
      - extent_competed
      - fair_opportunity_limited_sources
      - federal_supply_schedule_award_id
      - funding_agency
      - last_modified_by
      - last_modified_date
      - latest_action_date
      - latest_action_date_fiscal_year
      - latest_transaction_key
      - naics_code
      - national_interest_action
      - number_of_offers_received
      - other_statutory_authority
      - other_than_full_and_open_competition
      - parent_award_id
      - parent_award_type
      - path
      - period_of_performance_current_end_date
      - period_of_performance_potential_end_date
      - period_of_performance_start_date
      - potential_total_value_of_award
      - primary_place_of_performance_city_name
      - primary_place_of_performance_country_name
      - primary_place_of_performance_county_name
      - primary_place_of_performance_state_code
      - primary_place_of_performance_state_name
      - primary_place_of_performance_zip
      - psc_code
      - related_opportunity_title
      - research
      - solicitation_identifier
      - solicitation_procedures
      - subcontracting_plan
      - total_dollars_obligated
      - type_of_agreement
      - type_of_contract_pricing_description
      - type_of_set_aside
      - vehicle
    Federal Grant:
      type: object
      description: |-
        A type of `ModelSerializer` that uses hyperlinked relationships instead
        of primary key relationships. Specifically:

        * A 'url' field is included instead of the 'id' field.
        * Relationships to other instances are hyperlinks, instead of primary keys.

        Included Mixins:

        * A mixin class to enable sparse fieldsets is included
        * A mixin class to enable validation of included resources is included
      properties:
        award_id:
          type: string
        awardee_key:
          allOf:
          - $ref: '#/components/schemas/AwardeeSimple'
          nullable: true
        awardee_key_parent:
          allOf:
          - $ref: '#/components/schemas/AwardeeSimple'
          nullable: true
        assistance_type_code:
          type: string
          nullable: true
        latest_transaction_key:
          type: string
          nullable: true
        last_modified_date:
          type: string
          format: date-time
          readOnly: true
        latest_action_date:
          type: string
          format: date
        latest_action_date_fiscal_year:
          type: integer
          nullable: true
        period_of_performance_start_date:
          type: string
          format: date
          nullable: true
        period_of_performance_current_end_date:
          type: string
          format: date
          nullable: true
        total_obligated_amount:
          type: number
          format: double
          nullable: true
        federal_action_obligation:
          type: number
          format: double
          nullable: true
        non_federal_funding_amount:
          type: number
          format: double
          nullable: true
        solicitation_identifier:
          type: string
          nullable: true
        primary_place_of_performance_zip:
          type: string
          nullable: true
        primary_place_of_performance_county_name:
          type: string
          nullable: true
        primary_place_of_performance_city_name:
          type: string
          nullable: true
        primary_place_of_performance_state_code:
          type: string
          nullable: true
        primary_place_of_performance_state_name:
          type: string
          nullable: true
        primary_place_of_performance_country_name:
          type: string
          nullable: true
        award_description_original:
          type: string
          nullable: true
        grant_program:
          $ref: '#/components/schemas/Grant Program'
        awarding_agency:
          $ref: '#/components/schemas/AgencySimple'
        funding_agency:
          $ref: '#/components/schemas/AgencySimple'
        path:
          type: string
          readOnly: true
      required:
      - assistance_type_code
      - award_description_original
      - award_id
      - awardee_key
      - awardee_key_parent
      - awarding_agency
      - federal_action_obligation
      - funding_agency
      - grant_program
      - last_modified_date
      - latest_action_date
      - latest_action_date_fiscal_year
      - latest_transaction_key
      - non_federal_funding_amount
      - path
      - period_of_performance_current_end_date
      - period_of_performance_start_date
      - primary_place_of_performance_city_name
      - primary_place_of_performance_country_name
      - primary_place_of_performance_county_name
      - primary_place_of_performance_state_code
      - primary_place_of_performance_state_name
      - primary_place_of_performance_zip
      - solicitation_identifier
      - total_obligated_amount
    Federal IDV:
      type: object
      description: |-
        A type of `ModelSerializer` that uses hyperlinked relationships instead
        of primary key relationships. Specifically:

        * A 'url' field is included instead of the 'id' field.
        * Relationships to other instances are hyperlinks, instead of primary keys.

        Included Mixins:

        * A mixin class to enable sparse fieldsets is included
        * A mixin class to enable validation of included resources is included
      properties:
        award_id:
          type: string
        parent_award_id:
          type: string
          nullable: true
        latest_transaction_key:
          type: string
          nullable: true
        last_modified_date:
          type: string
          format: date-time
          nullable: true
          readOnly: true
        latest_action_date:
          type: string
          format: date
        latest_action_date_fiscal_year:
          type: integer
          nullable: true
        awardee_key:
          allOf:
          - $ref: '#/components/schemas/AwardeeSimple'
          nullable: true
        awardee_key_parent:
          allOf:
          - $ref: '#/components/schemas/AwardeeSimple'
          nullable: true
        awarding_agency:
          $ref: '#/components/schemas/AgencySimple'
        funding_agency:
          $ref: '#/components/schemas/AgencySimple'
        vehicle:
          allOf:
          - $ref: '#/components/schemas/VehicleSimple'
          nullable: true
        who_can_use:
          type: string
          nullable: true
        federal_supply_schedule_award_id:
          type: string
          nullable: true
        parent_award_type:
          type: string
          nullable: true
        period_of_performance_start_date:
          type: string
          format: date-time
          nullable: true
          readOnly: true
        ordering_period_end_date:
          type: string
          format: date-time
          nullable: true
          readOnly: true
        potential_total_value_of_award:
          type: number
          format: double
          nullable: true
        award_type:
          type: string
          nullable: true
        award_description_original:
          type: string
          nullable: true
        alt_description:
          type: string
          nullable: true
        solicitation_identifier:
          type: string
          nullable: true
        related_opportunity_title:
          type: string
          nullable: true
        psc_code:
          allOf:
          - $ref: '#/components/schemas/PSC'
          readOnly: true
        naics_code:
          allOf:
          - $ref: '#/components/schemas/NAICSSimple'
          readOnly: true
        type_of_agreement:
          type: string
          nullable: true
        type_of_contract_pricing_description:
          type: string
          nullable: true
        national_interest_action:
          type: string
          nullable: true
        defense_program:
          type: string
          nullable: true
        other_statutory_authority:
          type: string
          nullable: true
        dod_claimant_program_code:
          type: string
          nullable: true
        subcontracting_plan:
          type: string
          nullable: true
        contracting_officers_determination_of_business_size_code:
          type: string
          nullable: true
        cost_or_pricing_data:
          type: string
          nullable: true
        competitive_procedures:
          type: string
          nullable: true
        fair_opportunity_limited_sources:
          type: string
          nullable: true
        other_than_full_and_open_competition:
          type: string
          nullable: true
        clinger_cohen_act_planning:
          type: string
          nullable: true
        research:
          type: string
          nullable: true
        type_of_set_aside:
          type: string
          nullable: true
        number_of_offers_received:
          type: string
          nullable: true
        extent_competed:
          type: string
          nullable: true
        solicitation_procedures:
          type: string
          nullable: true
        evaluated_preference:
          type: string
          nullable: true
        status_code:
          type: string
          nullable: true
        closed_status:
          type: string
          nullable: true
        created_by:
          allOf:
          - $ref: '#/components/schemas/PeopleSimple'
          nullable: true
        last_modified_by:
          allOf:
          - $ref: '#/components/schemas/PeopleSimple'
          nullable: true
        approved_by:
          allOf:
          - $ref: '#/components/schemas/PeopleSimple'
          nullable: true
        path:
          type: string
          readOnly: true
      required:
      - alt_description
      - approved_by
      - award_description_original
      - award_id
      - award_type
      - awardee_key
      - awardee_key_parent
      - awarding_agency
      - clinger_cohen_act_planning
      - closed_status
      - competitive_procedures
      - contracting_officers_determination_of_business_size_code
      - cost_or_pricing_data
      - created_by
      - defense_program
      - dod_claimant_program_code
      - evaluated_preference
      - extent_competed
      - fair_opportunity_limited_sources
      - federal_supply_schedule_award_id
      - funding_agency
      - last_modified_by
      - last_modified_date
      - latest_action_date
      - latest_action_date_fiscal_year
      - latest_transaction_key
      - naics_code
      - national_interest_action
      - number_of_offers_received
      - ordering_period_end_date
      - other_statutory_authority
      - other_than_full_and_open_competition
      - parent_award_id
      - parent_award_type
      - path
      - period_of_performance_start_date
      - potential_total_value_of_award
      - psc_code
      - related_opportunity_title
      - research
      - solicitation_identifier
      - solicitation_procedures
      - status_code
      - subcontracting_plan
      - type_of_agreement
      - type_of_contract_pricing_description
      - type_of_set_aside
      - vehicle
      - who_can_use
    Federal Subcontract:
      type: object
      description: |-
        A type of `ModelSerializer` that uses hyperlinked relationships instead
        of primary key relationships. Specifically:

        * A 'url' field is included instead of the 'id' field.
        * Relationships to other instances are hyperlinks, instead of primary keys.

        Included Mixins:

        * A mixin class to enable sparse fieldsets is included
        * A mixin class to enable validation of included resources is included
      properties:
        sub_awardee:
          allOf:
          - $ref: '#/components/schemas/AwardeeSimple'
          nullable: true
        sub_awardee_parent:
          allOf:
          - $ref: '#/components/schemas/AwardeeSimple'
          nullable: true
        subaward_id:
          type: string
        subaward_action_date:
          type: string
          format: date
          nullable: true
        subaward_action_date_fiscal_year:
          type: string
          nullable: true
        subaward_amount_total:
          type: number
          format: double
          nullable: true
        subaward_description:
          type: string
          nullable: true
        prime_contract_award_id:
          $ref: '#/components/schemas/Federal Contract'
        prime_idv_award_id:
          type: string
          nullable: true
        last_modified_date:
          type: string
          format: date
        path:
          type: string
          readOnly: true
      required:
      - last_modified_date
      - path
      - prime_contract_award_id
      - prime_idv_award_id
      - sub_awardee
      - sub_awardee_parent
      - subaward_action_date
      - subaward_action_date_fiscal_year
      - subaward_amount_total
      - subaward_description
      - subaward_id
    Federal Subgrant:
      type: object
      description: |-
        A type of `ModelSerializer` that uses hyperlinked relationships instead
        of primary key relationships. Specifically:

        * A 'url' field is included instead of the 'id' field.
        * Relationships to other instances are hyperlinks, instead of primary keys.

        Included Mixins:

        * A mixin class to enable sparse fieldsets is included
        * A mixin class to enable validation of included resources is included
      properties:
        sub_awardee:
          allOf:
          - $ref: '#/components/schemas/AwardeeSimple'
          nullable: true
        sub_awardee_parent:
          allOf:
          - $ref: '#/components/schemas/AwardeeSimple'
          nullable: true
        subaward_id:
          type: string
        subaward_action_date:
          type: string
          format: date
          nullable: true
        subaward_action_date_fiscal_year:
          type: string
          nullable: true
        subaward_amount_total:
          type: number
          format: double
          nullable: true
        subaward_description:
          type: string
          nullable: true
        prime_grant_award_id:
          $ref: '#/components/schemas/Federal Grant'
        last_modified_date:
          type: string
          format: date
        path:
          type: string
          readOnly: true
      required:
      - last_modified_date
      - path
      - prime_grant_award_id
      - sub_awardee
      - sub_awardee_parent
      - subaward_action_date
      - subaward_action_date_fiscal_year
      - subaward_amount_total
      - subaward_description
      - subaward_id
    FileTracker:
      type: object
      properties:
        file_name:
          type: string
          nullable: true
        file_type:
          type: string
          nullable: true
        file_size:
          type: integer
          maximum: 9223372036854775807
          minimum: -9223372036854775808
          format: int64
          nullable: true
          title: File Size (bytes)
        posted_date:
          type: string
          format: date-time
          nullable: true
        text_extract:
          type: string
          nullable: true
        summary:
          type: string
          nullable: true
        download_url:
          type: string
          readOnly: true
      required:
      - download_url
      - text_extract
    Grant Program:
      type: object
      description: |-
        A type of `ModelSerializer` that uses hyperlinked relationships instead
        of primary key relationships. Specifically:

        * A 'url' field is included instead of the 'id' field.
        * Relationships to other instances are hyperlinks, instead of primary keys.

        Included Mixins:

        * A mixin class to enable sparse fieldsets is included
        * A mixin class to enable validation of included resources is included
      properties:
        cfda_program_number:
          type: string
        active:
          type: boolean
        program_title:
          type: string
          nullable: true
        popular_program_title:
          type: string
          nullable: true
      required:
      - cfda_program_number
      - popular_program_title
      - program_title
    LookupComboOpportunityType:
      type: object
      properties:
        description:
          type: string
          nullable: true
    NAICS:
      type: object
      description: |-
        A type of `ModelSerializer` that uses hyperlinked relationships instead
        of primary key relationships. Specifically:

        * A 'url' field is included instead of the 'id' field.
        * Relationships to other instances are hyperlinks, instead of primary keys.

        Included Mixins:

        * A mixin class to enable sparse fieldsets is included
        * A mixin class to enable validation of included resources is included
      properties:
        naics_code:
          type: string
        naics_description:
          type: string
          nullable: true
        naics_description_long:
          type: string
          nullable: true
        active:
          type: boolean
          nullable: true
        path:
          type: string
          readOnly: true
      required:
      - active
      - naics_code
      - naics_description
      - naics_description_long
      - path
    NAICSSimple:
      type: object
      description: |-
        A type of `ModelSerializer` that uses hyperlinked relationships instead
        of primary key relationships. Specifically:

        * A 'url' field is included instead of the 'id' field.
        * Relationships to other instances are hyperlinks, instead of primary keys.

        Included Mixins:

        * A mixin class to enable sparse fieldsets is included
        * A mixin class to enable validation of included resources is included
      properties:
        naics_code:
          type: string
        naics_description:
          type: string
          nullable: true
        active:
          type: boolean
          nullable: true
        path:
          type: string
          readOnly: true
      required:
      - active
      - naics_code
      - naics_description
      - path
    NSN:
      type: object
      properties:
        nsn:
          type: string
        niin:
          type: string
          nullable: true
        fsc:
          type: string
          title: PSC
          nullable: true
        nomenclature:
          type: string
          nullable: true
        opp_count:
          type: integer
          maximum: 9223372036854775807
          minimum: -9223372036854775808
          format: int64
          nullable: true
        part_numbers:
          type: string
          nullable: true
        end_item_name:
          type: string
          nullable: true
        amc:
          type: string
          nullable: true
        amsc:
          type: string
          nullable: true
        ui:
          type: string
          nullable: true
        distributor_use:
          type: boolean
        last_price:
          type: string
          readOnly: true
        unit_price:
          type: string
          readOnly: true
        suppliers:
          type: string
          readOnly: true
        awards:
          type: string
          readOnly: true
      required:
      - awards
      - distributor_use
      - last_price
      - nsn
      - suppliers
      - unit_price
    Naics:
      type: object
      properties:
        naics_code:
          type: string
          title: NAICS
          nullable: true
    Opportunity:
      type: object
      description: |-
        A type of `ModelSerializer` that uses hyperlinked relationships instead
        of primary key relationships. Specifically:

        * A 'url' field is included instead of the 'id' field.
        * Relationships to other instances are hyperlinks, instead of primary keys.

        Included Mixins:

        * A mixin class to enable sparse fieldsets is included
        * A mixin class to enable validation of included resources is included
      properties:
        opp_cat:
          type: string
          nullable: true
        title:
          type: string
          nullable: true
        description_text:
          type: string
          nullable: true
        ai_summary:
          type: string
          nullable: true
        source_id:
          type: string
          nullable: true
        source_id_version:
          type: string
          nullable: true
        captured_date:
          type: string
          format: date
          nullable: true
        posted_date:
          type: string
          format: date
          nullable: true
        due_date:
          type: string
          format: date
          nullable: true
        agency:
          $ref: '#/components/schemas/AgencySimple'
        naics_code:
          allOf:
          - $ref: '#/components/schemas/Naics'
          readOnly: true
        psc_code:
          allOf:
          - $ref: '#/components/schemas/Psc'
          readOnly: true
        opp_type:
          allOf:
          - $ref: '#/components/schemas/LookupComboOpportunityType'
          readOnly: true
        primary_contact_email:
          $ref: '#/components/schemas/PeopleSimple'
        secondary_contact_email:
          $ref: '#/components/schemas/PeopleSimple'
        set_aside:
          type: string
          nullable: true
        nsn:
          type: array
          items:
            type: string
            nullable: true
          nullable: true
        val_est_low:
          type: string
          nullable: true
        val_est_high:
          type: string
          nullable: true
        pop_country:
          type: string
          nullable: true
        pop_state:
          type: string
          nullable: true
        pop_city:
          type: string
          nullable: true
        pop_zip:
          type: string
          nullable: true
        opp_key:
          type: string
          nullable: true
        version_key:
          type: string
          nullable: true
        source_type:
          type: string
          nullable: true
        dibbs_status:
          type: string
          nullable: true
        path:
          type: string
          nullable: true
        source_path:
          type: string
          nullable: true
        document_path:
          type: string
          readOnly: true
      required:
      - agency
      - ai_summary
      - captured_date
      - description_text
      - dibbs_status
      - document_path
      - due_date
      - naics_code
      - nsn
      - opp_cat
      - opp_type
      - path
      - pop_city
      - pop_country
      - pop_state
      - pop_zip
      - posted_date
      - primary_contact_email
      - psc_code
      - secondary_contact_email
      - set_aside
      - source_id
      - source_id_version
      - source_type
      - title
      - val_est_high
      - val_est_low
    PSC:
      type: object
      description: |-
        A type of `ModelSerializer` that uses hyperlinked relationships instead
        of primary key relationships. Specifically:

        * A 'url' field is included instead of the 'id' field.
        * Relationships to other instances are hyperlinks, instead of primary keys.

        Included Mixins:

        * A mixin class to enable sparse fieldsets is included
        * A mixin class to enable validation of included resources is included
      properties:
        psc_code:
          type: string
        psc_name:
          type: string
          nullable: true
        psc_description:
          type: string
          nullable: true
        active:
          type: boolean
          nullable: true
        path:
          type: string
          readOnly: true
      required:
      - active
      - path
      - psc_code
      - psc_description
      - psc_name
    PaginatedAgencyList:
      type: object
      properties:
        results:
          type: array
          items:
            $ref: '#/components/schemas/Agency'
        meta:
          type: object
          properties:
            pagination:
              type: object
              properties:
                page:
                  type: integer
                  example: 1
                pages:
                  type: integer
                  example: 999
                count:
                  type: integer
                  example: 9999
        links:
          type: object
          properties:
            first:
              type: string
              format: uri
              example: https://www.highergov.com/api/agency/?...page_number=1
            last:
              type: string
              format: uri
              example: https://www.highergov.com/api/agency/?...page_number=999
            next:
              type: string
              format: uri
              example: https://www.highergov.com/api/agency/?...page_number=2
            prev:
              type: string
              format: uri
              example: null
    PaginatedAssistanceList:
      type: object
      properties:
        results:
          type: array
          items:
            $ref: '#/components/schemas/Assistance'
        meta:
          type: object
          properties:
            pagination:
              type: object
              properties:
                page:
                  type: integer
                  example: 1
                pages:
                  type: integer
                  example: 999
                count:
                  type: integer
                  example: 9999
        links:
          type: object
          properties:
            first:
              type: string
              format: uri
              example: https://www.highergov.com/api/assistance/?...page_number=1
            last:
              type: string
              format: uri
              example: https://www.highergov.com/api/assistance/?...page_number=999
            next:
              type: string
              format: uri
              example: https://www.highergov.com/api/assistance/?...page_number=2
            prev:
              type: string
              format: uri
              example: null
    PaginatedAwardeeList:
      type: object
      properties:
        results:
          type: array
          items:
            $ref: '#/components/schemas/Awardee'
        meta:
          type: object
          properties:
            pagination:
              type: object
              properties:
                page:
                  type: integer
                  example: 1
                pages:
                  type: integer
                  example: 999
                count:
                  type: integer
                  example: 9999
        links:
          type: object
          properties:
            first:
              type: string
              format: uri
              example: https://www.highergov.com/api/awardee/?...page_number=1
            last:
              type: string
              format: uri
              example: https://www.highergov.com/api/awardee/?...page_number=999
            next:
              type: string
              format: uri
              example: https://www.highergov.com/api/awardee/?...page_number=2
            prev:
              type: string
              format: uri
              example: null
    PaginatedAwardeeMPList:
      type: object
      properties:
        results:
          type: array
          items:
            $ref: '#/components/schemas/AwardeeMP'
        meta:
          type: object
          properties:
            pagination:
              type: object
              properties:
                page:
                  type: integer
                  example: 1
                pages:
                  type: integer
                  example: 999
                count:
                  type: integer
                  example: 9999
        links:
          type: object
          properties:
            first:
              type: string
              format: uri
              example: https://www.highergov.com/api/awardeemp/?...page_number=1
            last:
              type: string
              format: uri
              example: https://www.highergov.com/api/awardeemp/?...page_number=999
            next:
              type: string
              format: uri
              example: https://www.highergov.com/api/awardeemp/?...page_number=2
            prev:
              type: string
              format: uri
              example: null
    PaginatedAwardeePartnershipList:
      type: object
      properties:
        results:
          type: array
          items:
            $ref: '#/components/schemas/AwardeePartnership'
        meta:
          type: object
          properties:
            pagination:
              type: object
              properties:
                page:
                  type: integer
                  example: 1
                pages:
                  type: integer
                  example: 999
                count:
                  type: integer
                  example: 9999
        links:
          type: object
          properties:
            first:
              type: string
              format: uri
              example: https://www.highergov.com/api/awardeepartnership/?...page_number=1
            last:
              type: string
              format: uri
              example: https://www.highergov.com/api/awardeepartnership/?...page_number=999
            next:
              type: string
              format: uri
              example: https://www.highergov.com/api/awardeepartnership/?...page_number=2
            prev:
              type: string
              format: uri
              example: null
    PaginatedFederal ContractList:
      type: object
      properties:
        results:
          type: array
          items:
            $ref: '#/components/schemas/Federal Contract'
        meta:
          type: object
          properties:
            pagination:
              type: object
              properties:
                page:
                  type: integer
                  example: 1
                pages:
                  type: integer
                  example: 999
                count:
                  type: integer
                  example: 9999
        links:
          type: object
          properties:
            first:
              type: string
              format: uri
              example: https://www.highergov.com/api/federal contract/?...page_number=1
            last:
              type: string
              format: uri
              example: https://www.highergov.com/api/federal contract/?...page_number=999
            next:
              type: string
              format: uri
              example: https://www.highergov.com/api/federal contract/?...page_number=2
            prev:
              type: string
              format: uri
              example: null
    PaginatedFederal GrantList:
      type: object
      properties:
        results:
          type: array
          items:
            $ref: '#/components/schemas/Federal Grant'
        meta:
          type: object
          properties:
            pagination:
              type: object
              properties:
                page:
                  type: integer
                  example: 1
                pages:
                  type: integer
                  example: 999
                count:
                  type: integer
                  example: 9999
        links:
          type: object
          properties:
            first:
              type: string
              format: uri
              example: https://www.highergov.com/api/federal grant/?...page_number=1
            last:
              type: string
              format: uri
              example: https://www.highergov.com/api/federal grant/?...page_number=999
            next:
              type: string
              format: uri
              example: https://www.highergov.com/api/federal grant/?...page_number=2
            prev:
              type: string
              format: uri
              example: null
    PaginatedFederal IDVList:
      type: object
      properties:
        results:
          type: array
          items:
            $ref: '#/components/schemas/Federal IDV'
        meta:
          type: object
          properties:
            pagination:
              type: object
              properties:
                page:
                  type: integer
                  example: 1
                pages:
                  type: integer
                  example: 999
                count:
                  type: integer
                  example: 9999
        links:
          type: object
          properties:
            first:
              type: string
              format: uri
              example: https://www.highergov.com/api/federal idv/?...page_number=1
            last:
              type: string
              format: uri
              example: https://www.highergov.com/api/federal idv/?...page_number=999
            next:
              type: string
              format: uri
              example: https://www.highergov.com/api/federal idv/?...page_number=2
            prev:
              type: string
              format: uri
              example: null
    PaginatedFederal SubcontractList:
      type: object
      properties:
        results:
          type: array
          items:
            $ref: '#/components/schemas/Federal Subcontract'
        meta:
          type: object
          properties:
            pagination:
              type: object
              properties:
                page:
                  type: integer
                  example: 1
                pages:
                  type: integer
                  example: 999
                count:
                  type: integer
                  example: 9999
        links:
          type: object
          properties:
            first:
              type: string
              format: uri
              example: https://www.highergov.com/api/federal subcontract/?...page_number=1
            last:
              type: string
              format: uri
              example: https://www.highergov.com/api/federal subcontract/?...page_number=999
            next:
              type: string
              format: uri
              example: https://www.highergov.com/api/federal subcontract/?...page_number=2
            prev:
              type: string
              format: uri
              example: null
    PaginatedFederal SubgrantList:
      type: object
      properties:
        results:
          type: array
          items:
            $ref: '#/components/schemas/Federal Subgrant'
        meta:
          type: object
          properties:
            pagination:
              type: object
              properties:
                page:
                  type: integer
                  example: 1
                pages:
                  type: integer
                  example: 999
                count:
                  type: integer
                  example: 9999
        links:
          type: object
          properties:
            first:
              type: string
              format: uri
              example: https://www.highergov.com/api/federal subgrant/?...page_number=1
            last:
              type: string
              format: uri
              example: https://www.highergov.com/api/federal subgrant/?...page_number=999
            next:
              type: string
              format: uri
              example: https://www.highergov.com/api/federal subgrant/?...page_number=2
            prev:
              type: string
              format: uri
              example: null
    PaginatedFileTrackerList:
      type: object
      properties:
        results:
          type: array
          items:
            $ref: '#/components/schemas/FileTracker'
        meta:
          type: object
          properties:
            pagination:
              type: object
              properties:
                page:
                  type: integer
                  example: 1
                pages:
                  type: integer
                  example: 999
                count:
                  type: integer
                  example: 9999
        links:
          type: object
          properties:
            first:
              type: string
              format: uri
              example: https://www.highergov.com/api/filetracker/?...page_number=1
            last:
              type: string
              format: uri
              example: https://www.highergov.com/api/filetracker/?...page_number=999
            next:
              type: string
              format: uri
              example: https://www.highergov.com/api/filetracker/?...page_number=2
            prev:
              type: string
              format: uri
              example: null
    PaginatedNAICSList:
      type: object
      properties:
        results:
          type: array
          items:
            $ref: '#/components/schemas/NAICS'
        meta:
          type: object
          properties:
            pagination:
              type: object
              properties:
                page:
                  type: integer
                  example: 1
                pages:
                  type: integer
                  example: 999
                count:
                  type: integer
                  example: 9999
        links:
          type: object
          properties:
            first:
              type: string
              format: uri
              example: https://www.highergov.com/api/naics/?...page_number=1
            last:
              type: string
              format: uri
              example: https://www.highergov.com/api/naics/?...page_number=999
            next:
              type: string
              format: uri
              example: https://www.highergov.com/api/naics/?...page_number=2
            prev:
              type: string
              format: uri
              example: null
    PaginatedNSNList:
      type: object
      properties:
        results:
          type: array
          items:
            $ref: '#/components/schemas/NSN'
        meta:
          type: object
          properties:
            pagination:
              type: object
              properties:
                page:
                  type: integer
                  example: 1
                pages:
                  type: integer
                  example: 999
                count:
                  type: integer
                  example: 9999
        links:
          type: object
          properties:
            first:
              type: string
              format: uri
              example: https://www.highergov.com/api/nsn/?...page_number=1
            last:
              type: string
              format: uri
              example: https://www.highergov.com/api/nsn/?...page_number=999
            next:
              type: string
              format: uri
              example: https://www.highergov.com/api/nsn/?...page_number=2
            prev:
              type: string
              format: uri
              example: null
    PaginatedOpportunityList:
      type: object
      properties:
        results:
          type: array
          items:
            $ref: '#/components/schemas/Opportunity'
        meta:
          type: object
          properties:
            pagination:
              type: object
              properties:
                page:
                  type: integer
                  example: 1
                pages:
                  type: integer
                  example: 999
                count:
                  type: integer
                  example: 9999
        links:
          type: object
          properties:
            first:
              type: string
              format: uri
              example: https://www.highergov.com/api/opportunity/?...page_number=1
            last:
              type: string
              format: uri
              example: https://www.highergov.com/api/opportunity/?...page_number=999
            next:
              type: string
              format: uri
              example: https://www.highergov.com/api/opportunity/?...page_number=2
            prev:
              type: string
              format: uri
              example: null
    PaginatedPSCList:
      type: object
      properties:
        results:
          type: array
          items:
            $ref: '#/components/schemas/PSC'
        meta:
          type: object
          properties:
            pagination:
              type: object
              properties:
                page:
                  type: integer
                  example: 1
                pages:
                  type: integer
                  example: 999
                count:
                  type: integer
                  example: 9999
        links:
          type: object
          properties:
            first:
              type: string
              format: uri
              example: https://www.highergov.com/api/psc/?...page_number=1
            last:
              type: string
              format: uri
              example: https://www.highergov.com/api/psc/?...page_number=999
            next:
              type: string
              format: uri
              example: https://www.highergov.com/api/psc/?...page_number=2
            prev:
              type: string
              format: uri
              example: null
    PaginatedPeopleList:
      type: object
      properties:
        results:
          type: array
          items:
            $ref: '#/components/schemas/People'
        meta:
          type: object
          properties:
            pagination:
              type: object
              properties:
                page:
                  type: integer
                  example: 1
                pages:
                  type: integer
                  example: 999
                count:
                  type: integer
                  example: 9999
        links:
          type: object
          properties:
            first:
              type: string
              format: uri
              example: https://www.highergov.com/api/people/?...page_number=1
            last:
              type: string
              format: uri
              example: https://www.highergov.com/api/people/?...page_number=999
            next:
              type: string
              format: uri
              example: https://www.highergov.com/api/people/?...page_number=2
            prev:
              type: string
              format: uri
              example: null
    PaginatedVehicleList:
      type: object
      properties:
        results:
          type: array
          items:
            $ref: '#/components/schemas/Vehicle'
        meta:
          type: object
          properties:
            pagination:
              type: object
              properties:
                page:
                  type: integer
                  example: 1
                pages:
                  type: integer
                  example: 999
                count:
                  type: integer
                  example: 9999
        links:
          type: object
          properties:
            first:
              type: string
              format: uri
              example: https://www.highergov.com/api/vehicle/?...page_number=1
            last:
              type: string
              format: uri
              example: https://www.highergov.com/api/vehicle/?...page_number=999
            next:
              type: string
              format: uri
              example: https://www.highergov.com/api/vehicle/?...page_number=2
            prev:
              type: string
              format: uri
              example: null
    People:
      type: object
      description: |-
        A type of `ModelSerializer` that uses hyperlinked relationships instead
        of primary key relationships. Specifically:

        * A 'url' field is included instead of the 'id' field.
        * Relationships to other instances are hyperlinks, instead of primary keys.

        Included Mixins:

        * A mixin class to enable sparse fieldsets is included
        * A mixin class to enable validation of included resources is included
      properties:
        last_seen:
          type: string
          format: date
        contact_first_name:
          type: string
          nullable: true
          title: First Name
        contact_last_name:
          type: string
          nullable: true
          title: Last Name
        contact_name:
          type: string
          nullable: true
        contact_title:
          type: string
          nullable: true
        contact_email:
          type: string
          nullable: true
        contact_phone:
          type: string
          nullable: true
        contact_ext:
          type: string
          nullable: true
        contact_fax:
          type: string
          nullable: true
        agency:
          $ref: '#/components/schemas/AgencySimple'
        contact_type:
          type: string
        path:
          type: string
          readOnly: true
      required:
      - agency
      - contact_email
      - contact_ext
      - contact_fax
      - contact_name
      - contact_phone
      - contact_title
      - contact_type
      - last_seen
      - path
    PeopleSimple:
      type: object
      description: |-
        A type of `ModelSerializer` that uses hyperlinked relationships instead
        of primary key relationships. Specifically:

        * A 'url' field is included instead of the 'id' field.
        * Relationships to other instances are hyperlinks, instead of primary keys.

        Included Mixins:

        * A mixin class to enable sparse fieldsets is included
        * A mixin class to enable validation of included resources is included
      properties:
        contact_title:
          type: string
          nullable: true
        contact_name:
          type: string
          nullable: true
        contact_first_name:
          type: string
          nullable: true
        contact_last_name:
          type: string
          nullable: true
        contact_email:
          type: string
          nullable: true
        contact_phone:
          type: string
          nullable: true
      required:
      - contact_email
      - contact_first_name
      - contact_last_name
      - contact_name
      - contact_phone
      - contact_title
    Psc:
      type: object
      properties:
        psc_code:
          type: string
          title: PSC
          nullable: true
    Vehicle:
      type: object
      description: |-
        A type of `ModelSerializer` that uses hyperlinked relationships instead
        of primary key relationships. Specifically:

        * A 'url' field is included instead of the 'id' field.
        * Relationships to other instances are hyperlinks, instead of primary keys.

        Included Mixins:

        * A mixin class to enable sparse fieldsets is included
        * A mixin class to enable validation of included resources is included
      properties:
        vehicle_key:
          type: integer
          nullable: true
        vehicle_name:
          type: string
          nullable: true
        vehicle_description:
          type: string
          nullable: true
        shared_ceiling:
          type: number
          format: double
          nullable: true
        vehicle_type:
          type: string
          nullable: true
        naics_code:
          allOf:
          - $ref: '#/components/schemas/NAICS'
          readOnly: true
        psc_code:
          allOf:
          - $ref: '#/components/schemas/PSC'
          readOnly: true
        type_of_set_aside:
          type: string
          nullable: true
        who_can_use:
          type: string
          nullable: true
        award_date:
          type: string
          format: date
          nullable: true
        last_date_to_order:
          type: string
          format: date
          nullable: true
        associated_solicitation:
          type: string
          nullable: true
        primary_sponsor_agency:
          allOf:
          - $ref: '#/components/schemas/AgencySimple'
          nullable: true
        predecessor_vehicle:
          type: string
          readOnly: true
        successor_vehicle:
          type: string
          readOnly: true
        path:
          type: string
          readOnly: true
      required:
      - associated_solicitation
      - award_date
      - last_date_to_order
      - naics_code
      - path
      - predecessor_vehicle
      - primary_sponsor_agency
      - psc_code
      - shared_ceiling
      - successor_vehicle
      - type_of_set_aside
      - vehicle_description
      - vehicle_key
      - vehicle_name
      - vehicle_type
      - who_can_use
    VehicleSimple:
      type: object
      description: |-
        A type of `ModelSerializer` that uses hyperlinked relationships instead
        of primary key relationships. Specifically:

        * A 'url' field is included instead of the 'id' field.
        * Relationships to other instances are hyperlinks, instead of primary keys.

        Included Mixins:

        * A mixin class to enable sparse fieldsets is included
        * A mixin class to enable validation of included resources is included
      properties:
        vehicle_key:
          type: integer
          nullable: true
        vehicle_name:
          type: string
          nullable: true
        vehicle_description:
          type: string
          nullable: true
        path:
          type: string
          readOnly: true
      required:
      - path
      - vehicle_description
      - vehicle_key
      - vehicle_name
      x-openai-parameters:
        api_key: 9874995194174018881c567d92a2c4d2