HigherGov API

**Document: 2 of 3**

URL: https://www.highergov.com/api-external/docs/#/Vehicle/api_external_vehicle_list

---


HigherGov API
v1.2 
OAS 3.0
/api-external/schema/


---


GET
/api-external/idv/

Description: Federal prime IDV awards.
Update Frequency: Daily by 2am (for two days prior) Update Check Field: last_modified_date.

Parameters
Try it out
Name	Description
api_key *
string
(query)
API Key for authentication

Default value : your-api-key-here

your-api-key-here
award_id
string
(query)
The government Award ID

Examples: 
Select
award_id
awardee_key
integer
(query)
HigherGov Awardee Key

Examples: 
Select
awardee_key
awardee_key_parent
integer
(query)
HigherGov Awardee Key (Parent Level)

Examples: 
Select
awardee_key_parent
awardee_uei
string
(query)
Awardee UEI

Examples: 
Select
awardee_uei
awardee_uei_parent
string
(query)
Awardee UEI Parent

Examples: 
Select
awardee_uei_parent
awarding_agency_key
integer
(query)
HigherGov Awarding Agency key

Examples: 
Select
awarding_agency_key
funding_agency_key
integer
(query)
HigherGov Funding Agency key

Examples: 
Select
funding_agency_key
last_modified_date
string($date)
(query)
Last modified date filter (format: YYYY-MM-DD)

Examples: 
Select
last_modified_date
naics_code
string
(query)
Awards NAICS code

Examples: 
Select
naics_code
ordering
string
(query)
Which field to use when ordering the results.

Available values : -action_date, -last_modified_date_ordering, -ordering_period_end_date, -potential_total_value_of_award, action_date, last_modified_date_ordering, ordering_period_end_date, potential_total_value_of_award


--
page_number
integer
(query)
A page number within the paginated result set.

page_number
page_size
string
(query)
Number of records returned per page (max 100)

Default value : 10

10
parent_award_id
string
(query)
The government Award ID of the parent Award

Examples: 
Select
parent_award_id
psc_code
string
(query)
PSC code

Examples: 
Select
psc_code
vehicle_key
integer
(query)
HigherGov Vehicle key

Examples: 
Select
vehicle_key
Responses
Code	Description	Links
200	
Success

Media type

application/json
Controls Accept header.
Example Value
Schema
{
  "results": [
    {
      "award_id": "string",
      "parent_award_id": "string",
      "latest_transaction_key": "string",
      "last_modified_date": "2025-08-04T21:39:54.357Z",
      "latest_action_date": "2025-08-04",
      "latest_action_date_fiscal_year": 0,
      "awardee_key": {
        "awardee_key": 0,
        "clean_name": "string",
        "uei": "string",
        "cage_code": "string",
        "path": "string"
      },
      "awardee_key_parent": {
        "awardee_key": 0,
        "clean_name": "string",
        "uei": "string",
        "cage_code": "string",
        "path": "string"
      },
      "awarding_agency": {
        "agency_key": 0,
        "agency_name": "string",
        "agency_abbreviation": "string",
        "agency_type": "string",
        "path": "string"
      },
      "funding_agency": {
        "agency_key": 0,
        "agency_name": "string",
        "agency_abbreviation": "string",
        "agency_type": "string",
        "path": "string"
      },
      "vehicle": {
        "vehicle_key": 0,
        "vehicle_name": "string",
        "vehicle_description": "string",
        "path": "string"
      },
      "who_can_use": "string",
      "federal_supply_schedule_award_id": "string",
      "parent_award_type": "string",
      "period_of_performance_start_date": "2025-08-04T21:39:54.357Z",
      "ordering_period_end_date": "2025-08-04T21:39:54.357Z",
      "potential_total_value_of_award": 0,
      "award_type": "string",
      "award_description_original": "string",
      "alt_description": "string",
      "solicitation_identifier": "string",
      "related_opportunity_title": "string",
      "psc_code": {
        "psc_code": "string",
        "psc_name": "string",
        "psc_description": "string",
        "active": true,
        "path": "string"
      },
      "naics_code": {
        "naics_code": "string",
        "naics_description": "string",
        "active": true,
        "path": "string"
      },
      "type_of_agreement": "string",
      "type_of_contract_pricing_description": "string",
      "national_interest_action": "string",
      "defense_program": "string",
      "other_statutory_authority": "string",
      "dod_claimant_program_code": "string",
      "subcontracting_plan": "string",
      "contracting_officers_determination_of_business_size_code": "string",
      "cost_or_pricing_data": "string",
      "competitive_procedures": "string",
      "fair_opportunity_limited_sources": "string",
      "other_than_full_and_open_competition": "string",
      "clinger_cohen_act_planning": "string",
      "research": "string",
      "type_of_set_aside": "string",
      "number_of_offers_received": "string",
      "extent_competed": "string",
      "solicitation_procedures": "string",
      "evaluated_preference": "string",
      "status_code": "string",
      "closed_status": "string",
      "created_by": {
        "contact_title": "string",
        "contact_name": "string",
        "contact_first_name": "string",
        "contact_last_name": "string",
        "contact_email": "string",
        "contact_phone": "string"
      },
      "last_modified_by": {
        "contact_title": "string",
        "contact_name": "string",
        "contact_first_name": "string",
        "contact_last_name": "string",
        "contact_email": "string",
        "contact_phone": "string"
      },
      "approved_by": {
        "contact_title": "string",
        "contact_name": "string",
        "contact_first_name": "string",
        "contact_last_name": "string",
        "contact_email": "string",
        "contact_phone": "string"
      },
      "path": "string"
    }
  ],
  "meta": {
    "pagination": {
      "page": 1,
      "pages": 999,
      "count": 9999
    }
  },
  "links": {
    "first": "https://www.highergov.com/api/federal idv/?...page_number=1",
    "last": "https://www.highergov.com/api/federal idv/?...page_number=999",
    "next": "https://www.highergov.com/api/federal idv/?...page_number=2",
    "prev": null
  }
}
No links
400	
Bad Request

No links
403	
Invalid API Key

No links
404	
Requested Record Not Found

No links
NAICS


GET
/api-external/naics/

Description: North American Industry Classification System (NAICS) codes.
Update Frequency: Updated Ad Hoc when codes added or removed by the Census Bureau or the SBA changes size standards

Parameters
Try it out
Name	Description
api_key *
string
(query)
API Key for authentication

Default value : your-api-key-here

your-api-key-here
naics_code
string
(query)
Awards NAICS code

Examples: 
Select
naics_code
ordering
string
(query)
Which field to use when ordering the results.

Available values : -naics_code, naics_code


--
page_number
integer
(query)
A page number within the paginated result set.

page_number
page_size
string
(query)
Number of records returned per page (max 100)

Default value : 10

10
Responses
Code	Description	Links
200	
Success

Media type

application/json
Controls Accept header.
Example Value
Schema
{
  "results": [
    {
      "naics_code": "string",
      "naics_description": "string",
      "naics_description_long": "string",
      "active": true,
      "path": "string"
    }
  ],
  "meta": {
    "pagination": {
      "page": 1,
      "pages": 999,
      "count": 9999
    }
  },
  "links": {
    "first": "https://www.highergov.com/api/naics/?...page_number=1",
    "last": "https://www.highergov.com/api/naics/?...page_number=999",
    "next": "https://www.highergov.com/api/naics/?...page_number=2",
    "prev": null
  }
}
No links
400	
Bad Request

No links
403	
Invalid API Key

No links
404	
Requested Record Not Found

No links
NSN


GET
/api-external/nsn/

Description: NATO Stock Number Lookup.

Parameters
Try it out
Name	Description
api_key *
string
(query)
API Key for authentication

Default value : your-api-key-here

your-api-key-here
cage_code
string
(query)
Supplier CAGE

Examples: 
Select
cage_code
nsn
string
(query)
National Stock Number (NSN)

Examples: 
Select
nsn
ordering
string
(query)
Which field to use when ordering the results.

Available values : -last_price, -opp_count, -unit_price, last_price, opp_count, unit_price


--
page_number
integer
(query)
A page number within the paginated result set.

page_number
page_size
string
(query)
Number of records returned per page (max 100)

Default value : 10

10
Responses
Code	Description	Links
200	
Success

Media type

application/json
Controls Accept header.
Example Value
Schema
{
  "results": [
    {
      "nsn": "string",
      "niin": "string",
      "fsc": "string",
      "nomenclature": "string",
      "opp_count": 9223372036854776000,
      "part_numbers": "string",
      "end_item_name": "string",
      "amc": "string",
      "amsc": "string",
      "ui": "string",
      "distributor_use": true,
      "last_price": "string",
      "unit_price": "string",
      "suppliers": "string",
      "awards": "string"
    }
  ],
  "meta": {
    "pagination": {
      "page": 1,
      "pages": 999,
      "count": 9999
    }
  },
  "links": {
    "first": "https://www.highergov.com/api/nsn/?...page_number=1",
    "last": "https://www.highergov.com/api/nsn/?...page_number=999",
    "next": "https://www.highergov.com/api/nsn/?...page_number=2",
    "prev": null
  }
}
No links
400	
Bad Request

No links
403	
Invalid API Key

No links
404	
Requested Record Not Found

No links
Opportunity


GET
/api-external/opportunity/

Description: Includes federal Contract, DIBBS, Grants, and State and Local Opportunities.
Update Frequency: Updated every 30 minutes Update Check Field: captured_date.

Parameters
Try it out
Name	Description
agency_key
integer
(query)
HigherGov Agency key

Examples: 
Select
agency_key
api_key *
string
(query)
API Key for authentication

Default value : your-api-key-here

your-api-key-here
captured_date
string($date)
(query)
Date the opportunity was added to HigherGov

Examples: 
Select
captured_date
opp_key
string
(query)
The HigherGov opportunity key

Examples: 
Select
opp_key
ordering
string
(query)
Which field to use when ordering the results.

Available values : -captured_date, -due_date, -posted_date, captured_date, due_date, posted_date


--
page_number
integer
(query)
A page number within the paginated result set.

page_number
page_size
string
(query)
Number of records returned per page (max 100)

Default value : 10

10
posted_date
string($date)
(query)
Date the opportunity was posted by the agency in YYYY-MM-DD format

Examples: 
Select
posted_date
search_id
string
(query)
HigherGov SearchID. The following search search fields are currently supported: Active, Applicant Type (Grant Only), Agency, CAGE Code, Date Due, Date Posted, Funding Category (Grant Only), Funding Instrument (Grant Only), Grant Program, Keywords, NAICS, NSN, Place of Performance (Federal Contracts Only), PSC, Set Aside, State (State and Local Only), and Value Range

Examples: 
Select
search_id
source_id
string
(query)
The source opportunity ID

Examples: 
Select
source_id
source_type
string
(query)
Opportunity source type (sam, dibbs, sbir, grant, sled)

Examples: 
Select
source_type
version_key
string
(query)
The HigherGov opportunity version key

Examples: 
Select
version_key
Responses
Code	Description	Links
200	
Success

Media type

application/json
Controls Accept header.
Example Value
Schema
{
  "results": [
    {
      "opp_cat": "string",
      "title": "string",
      "description_text": "string",
      "ai_summary": "string",
      "source_id": "string",
      "source_id_version": "string",
      "captured_date": "2025-08-04",
      "posted_date": "2025-08-04",
      "due_date": "2025-08-04",
      "agency": {
        "agency_key": 0,
        "agency_name": "string",
        "agency_abbreviation": "string",
        "agency_type": "string",
        "path": "string"
      },
      "naics_code": {
        "naics_code": "string"
      },
      "psc_code": {
        "psc_code": "string"
      },
      "opp_type": {
        "description": "string"
      },
      "primary_contact_email": {
        "contact_title": "string",
        "contact_name": "string",
        "contact_first_name": "string",
        "contact_last_name": "string",
        "contact_email": "string",
        "contact_phone": "string"
      },
      "secondary_contact_email": {
        "contact_title": "string",
        "contact_name": "string",
        "contact_first_name": "string",
        "contact_last_name": "string",
        "contact_email": "string",
        "contact_phone": "string"
      },
      "set_aside": "string",
      "nsn": [
        "string"
      ],
      "val_est_low": "string",
      "val_est_high": "string",
      "pop_country": "string",
      "pop_state": "string",
      "pop_city": "string",
      "pop_zip": "string",
      "opp_key": "string",
      "version_key": "string",
      "source_type": "string",
      "dibbs_status": "string",
      "path": "string",
      "source_path": "string",
      "document_path": "string"
    }
  ],
  "meta": {
    "pagination": {
      "page": 1,
      "pages": 999,
      "count": 9999
    }
  },
  "links": {
    "first": "https://www.highergov.com/api/opportunity/?...page_number=1",
    "last": "https://www.highergov.com/api/opportunity/?...page_number=999",
    "next": "https://www.highergov.com/api/opportunity/?...page_number=2",
    "prev": null
  }
}
No links
400	
Bad Request

No links
403	
Invalid API Key

No links
404	
Requested Record Not Found

No links
People


GET
/api-external/people/

Description: Federal and State and Local People.
Update Frequency: Updated in real time. Update Check Field: as_of_date.

Parameters
Try it out
Name	Description
api_key *
string
(query)
API Key for authentication

Default value : your-api-key-here

your-api-key-here
contact_email
string
(query)
Email address

Examples: 
Select
contact_email
ordering
string
(query)
Which field to use when ordering the results.

Available values : -last_seen, last_seen


--
page_number
integer
(query)
A page number within the paginated result set.

page_number
page_size
string
(query)
Number of records returned per page (max 100)

Default value : 10

10
Responses
Code	Description	Links
200	
Success

Media type

application/json
Controls Accept header.
Example Value
Schema
{
  "results": [
    {
      "last_seen": "2025-08-04",
      "contact_first_name": "string",
      "contact_last_name": "string",
      "contact_name": "string",
      "contact_title": "string",
      "contact_email": "string",
      "contact_phone": "string",
      "contact_ext": "string",
      "contact_fax": "string",
      "agency": {
        "agency_key": 0,
        "agency_name": "string",
        "agency_abbreviation": "string",
        "agency_type": "string",
        "path": "string"
      },
      "contact_type": "string",
      "path": "string"
    }
  ],
  "meta": {
    "pagination": {
      "page": 1,
      "pages": 999,
      "count": 9999
    }
  },
  "links": {
    "first": "https://www.highergov.com/api/people/?...page_number=1",
    "last": "https://www.highergov.com/api/people/?...page_number=999",
    "next": "https://www.highergov.com/api/people/?...page_number=2",
    "prev": null
  }
}
No links
400	
Bad Request

No links
403	
Invalid API Key

No links
404	
Requested Record Not Found

No links
PSC


GET
/api-external/psc/

Description: Product Service Codes (PSC) Codes.
Update Frequency: Updated Ad Hoc when codes added or removed

Parameters
Try it out
Name	Description
api_key *
string
(query)
API Key for authentication

Default value : your-api-key-here

your-api-key-here
page_number
integer
(query)
A page number within the paginated result set.

page_number
page_size
string
(query)
Number of records returned per page (max 100)

Default value : 10

10
psc_code
string
(query)
PSC code

Examples: 
Select
psc_code
Responses
Code	Description	Links
200	
Success

Media type

application/json
Controls Accept header.
Example Value
Schema
{
  "results": [
    {
      "psc_code": "string",
      "psc_name": "string",
      "psc_description": "string",
      "active": true,
      "path": "string"
    }
  ],
  "meta": {
    "pagination": {
      "page": 1,
      "pages": 999,
      "count": 9999
    }
  },
  "links": {
    "first": "https://www.highergov.com/api/psc/?...page_number=1",
    "last": "https://www.highergov.com/api/psc/?...page_number=999",
    "next": "https://www.highergov.com/api/psc/?...page_number=2",
    "prev": null
  }
}
No links
400	
Bad Request

No links
403	
Invalid API Key

No links
404	
Requested Record Not Found

No links
Federal Subcontract

GET
/api-external/idv/

Description: Federal prime IDV awards.
Update Frequency: Daily by 2am (for two days prior) Update Check Field: last_modified_date.

Parameters
Try it out
Name	Description
api_key *
string
(query)
API Key for authentication

Default value : your-api-key-here

your-api-key-here
award_id
string
(query)
The government Award ID

Examples: 
Select
award_id
awardee_key
integer
(query)
HigherGov Awardee Key

Examples: 
Select
awardee_key
awardee_key_parent
integer
(query)
HigherGov Awardee Key (Parent Level)

Examples: 
Select
awardee_key_parent
awardee_uei
string
(query)
Awardee UEI

Examples: 
Select
awardee_uei
awardee_uei_parent
string
(query)
Awardee UEI Parent

Examples: 
Select
awardee_uei_parent
awarding_agency_key
integer
(query)
HigherGov Awarding Agency key

Examples: 
Select
awarding_agency_key
funding_agency_key
integer
(query)
HigherGov Funding Agency key

Examples: 
Select
funding_agency_key
last_modified_date
string($date)
(query)
Last modified date filter (format: YYYY-MM-DD)

Examples: 
Select
last_modified_date
naics_code
string
(query)
Awards NAICS code

Examples: 
Select
naics_code
ordering
string
(query)
Which field to use when ordering the results.

Available values : -action_date, -last_modified_date_ordering, -ordering_period_end_date, -potential_total_value_of_award, action_date, last_modified_date_ordering, ordering_period_end_date, potential_total_value_of_award


--
page_number
integer
(query)
A page number within the paginated result set.

page_number
page_size
string
(query)
Number of records returned per page (max 100)

Default value : 10

10
parent_award_id
string
(query)
The government Award ID of the parent Award

Examples: 
Select
parent_award_id
psc_code
string
(query)
PSC code

Examples: 
Select
psc_code
vehicle_key
integer
(query)
HigherGov Vehicle key

Examples: 
Select
vehicle_key
Responses
Code	Description	Links
200	
Success

Media type

application/json
Controls Accept header.
Example Value
Schema
{
  "results": [
    {
      "award_id": "string",
      "parent_award_id": "string",
      "latest_transaction_key": "string",
      "last_modified_date": "2025-08-04T21:39:54.357Z",
      "latest_action_date": "2025-08-04",
      "latest_action_date_fiscal_year": 0,
      "awardee_key": {
        "awardee_key": 0,
        "clean_name": "string",
        "uei": "string",
        "cage_code": "string",
        "path": "string"
      },
      "awardee_key_parent": {
        "awardee_key": 0,
        "clean_name": "string",
        "uei": "string",
        "cage_code": "string",
        "path": "string"
      },
      "awarding_agency": {
        "agency_key": 0,
        "agency_name": "string",
        "agency_abbreviation": "string",
        "agency_type": "string",
        "path": "string"
      },
      "funding_agency": {
        "agency_key": 0,
        "agency_name": "string",
        "agency_abbreviation": "string",
        "agency_type": "string",
        "path": "string"
      },
      "vehicle": {
        "vehicle_key": 0,
        "vehicle_name": "string",
        "vehicle_description": "string",
        "path": "string"
      },
      "who_can_use": "string",
      "federal_supply_schedule_award_id": "string",
      "parent_award_type": "string",
      "period_of_performance_start_date": "2025-08-04T21:39:54.357Z",
      "ordering_period_end_date": "2025-08-04T21:39:54.357Z",
      "potential_total_value_of_award": 0,
      "award_type": "string",
      "award_description_original": "string",
      "alt_description": "string",
      "solicitation_identifier": "string",
      "related_opportunity_title": "string",
      "psc_code": {
        "psc_code": "string",
        "psc_name": "string",
        "psc_description": "string",
        "active": true,
        "path": "string"
      },
      "naics_code": {
        "naics_code": "string",
        "naics_description": "string",
        "active": true,
        "path": "string"
      },
      "type_of_agreement": "string",
      "type_of_contract_pricing_description": "string",
      "national_interest_action": "string",
      "defense_program": "string",
      "other_statutory_authority": "string",
      "dod_claimant_program_code": "string",
      "subcontracting_plan": "string",
      "contracting_officers_determination_of_business_size_code": "string",
      "cost_or_pricing_data": "string",
      "competitive_procedures": "string",
      "fair_opportunity_limited_sources": "string",
      "other_than_full_and_open_competition": "string",
      "clinger_cohen_act_planning": "string",
      "research": "string",
      "type_of_set_aside": "string",
      "number_of_offers_received": "string",
      "extent_competed": "string",
      "solicitation_procedures": "string",
      "evaluated_preference": "string",
      "status_code": "string",
      "closed_status": "string",
      "created_by": {
        "contact_title": "string",
        "contact_name": "string",
        "contact_first_name": "string",
        "contact_last_name": "string",
        "contact_email": "string",
        "contact_phone": "string"
      },
      "last_modified_by": {
        "contact_title": "string",
        "contact_name": "string",
        "contact_first_name": "string",
        "contact_last_name": "string",
        "contact_email": "string",
        "contact_phone": "string"
      },
      "approved_by": {
        "contact_title": "string",
        "contact_name": "string",
        "contact_first_name": "string",
        "contact_last_name": "string",
        "contact_email": "string",
        "contact_phone": "string"
      },
      "path": "string"
    }
  ],
  "meta": {
    "pagination": {
      "page": 1,
      "pages": 999,
      "count": 9999
    }
  },
  "links": {
    "first": "https://www.highergov.com/api/federal idv/?...page_number=1",
    "last": "https://www.highergov.com/api/federal idv/?...page_number=999",
    "next": "https://www.highergov.com/api/federal idv/?...page_number=2",
    "prev": null
  }
}
No links
400	
Bad Request

No links
403	
Invalid API Key

No links
404	
Requested Record Not Found

No links
NAICS


GET
/api-external/naics/

Description: North American Industry Classification System (NAICS) codes.
Update Frequency: Updated Ad Hoc when codes added or removed by the Census Bureau or the SBA changes size standards

Parameters
Try it out
Name	Description
api_key *
string
(query)
API Key for authentication

Default value : your-api-key-here

your-api-key-here
naics_code
string
(query)
Awards NAICS code

Examples: 
Select
naics_code
ordering
string
(query)
Which field to use when ordering the results.

Available values : -naics_code, naics_code


--
page_number
integer
(query)
A page number within the paginated result set.

page_number
page_size
string
(query)
Number of records returned per page (max 100)

Default value : 10

10
Responses
Code	Description	Links
200	
Success

Media type

application/json
Controls Accept header.
Example Value
Schema
{
  "results": [
    {
      "naics_code": "string",
      "naics_description": "string",
      "naics_description_long": "string",
      "active": true,
      "path": "string"
    }
  ],
  "meta": {
    "pagination": {
      "page": 1,
      "pages": 999,
      "count": 9999
    }
  },
  "links": {
    "first": "https://www.highergov.com/api/naics/?...page_number=1",
    "last": "https://www.highergov.com/api/naics/?...page_number=999",
    "next": "https://www.highergov.com/api/naics/?...page_number=2",
    "prev": null
  }
}
No links
400	
Bad Request

No links
403	
Invalid API Key

No links
404	
Requested Record Not Found

No links
NSN


GET
/api-external/nsn/

Description: NATO Stock Number Lookup.

Parameters
Try it out
Name	Description
api_key *
string
(query)
API Key for authentication

Default value : your-api-key-here

your-api-key-here
cage_code
string
(query)
Supplier CAGE

Examples: 
Select
cage_code
nsn
string
(query)
National Stock Number (NSN)

Examples: 
Select
nsn
ordering
string
(query)
Which field to use when ordering the results.

Available values : -last_price, -opp_count, -unit_price, last_price, opp_count, unit_price


--
page_number
integer
(query)
A page number within the paginated result set.

page_number
page_size
string
(query)
Number of records returned per page (max 100)

Default value : 10

10
Responses
Code	Description	Links
200	
Success

Media type

application/json
Controls Accept header.
Example Value
Schema
{
  "results": [
    {
      "nsn": "string",
      "niin": "string",
      "fsc": "string",
      "nomenclature": "string",
      "opp_count": 9223372036854776000,
      "part_numbers": "string",
      "end_item_name": "string",
      "amc": "string",
      "amsc": "string",
      "ui": "string",
      "distributor_use": true,
      "last_price": "string",
      "unit_price": "string",
      "suppliers": "string",
      "awards": "string"
    }
  ],
  "meta": {
    "pagination": {
      "page": 1,
      "pages": 999,
      "count": 9999
    }
  },
  "links": {
    "first": "https://www.highergov.com/api/nsn/?...page_number=1",
    "last": "https://www.highergov.com/api/nsn/?...page_number=999",
    "next": "https://www.highergov.com/api/nsn/?...page_number=2",
    "prev": null
  }
}
No links
400	
Bad Request

No links
403	
Invalid API Key

No links
404	
Requested Record Not Found

No links
Opportunity


GET
/api-external/opportunity/

Description: Includes federal Contract, DIBBS, Grants, and State and Local Opportunities.
Update Frequency: Updated every 30 minutes Update Check Field: captured_date.

Parameters
Try it out
Name	Description
agency_key
integer
(query)
HigherGov Agency key

Examples: 
Select
agency_key
api_key *
string
(query)
API Key for authentication

Default value : your-api-key-here

your-api-key-here
captured_date
string($date)
(query)
Date the opportunity was added to HigherGov

Examples: 
Select
captured_date
opp_key
string
(query)
The HigherGov opportunity key

Examples: 
Select
opp_key
ordering
string
(query)
Which field to use when ordering the results.

Available values : -captured_date, -due_date, -posted_date, captured_date, due_date, posted_date


--
page_number
integer
(query)
A page number within the paginated result set.

page_number
page_size
string
(query)
Number of records returned per page (max 100)

Default value : 10

10
posted_date
string($date)
(query)
Date the opportunity was posted by the agency in YYYY-MM-DD format

Examples: 
Select
posted_date
search_id
string
(query)
HigherGov SearchID. The following search search fields are currently supported: Active, Applicant Type (Grant Only), Agency, CAGE Code, Date Due, Date Posted, Funding Category (Grant Only), Funding Instrument (Grant Only), Grant Program, Keywords, NAICS, NSN, Place of Performance (Federal Contracts Only), PSC, Set Aside, State (State and Local Only), and Value Range

Examples: 
Select
search_id
source_id
string
(query)
The source opportunity ID

Examples: 
Select
source_id
source_type
string
(query)
Opportunity source type (sam, dibbs, sbir, grant, sled)

Examples: 
Select
source_type
version_key
string
(query)
The HigherGov opportunity version key

Examples: 
Select
version_key
Responses
Code	Description	Links
200	
Success

Media type

application/json
Controls Accept header.
Example Value
Schema
{
  "results": [
    {
      "opp_cat": "string",
      "title": "string",
      "description_text": "string",
      "ai_summary": "string",
      "source_id": "string",
      "source_id_version": "string",
      "captured_date": "2025-08-04",
      "posted_date": "2025-08-04",
      "due_date": "2025-08-04",
      "agency": {
        "agency_key": 0,
        "agency_name": "string",
        "agency_abbreviation": "string",
        "agency_type": "string",
        "path": "string"
      },
      "naics_code": {
        "naics_code": "string"
      },
      "psc_code": {
        "psc_code": "string"
      },
      "opp_type": {
        "description": "string"
      },
      "primary_contact_email": {
        "contact_title": "string",
        "contact_name": "string",
        "contact_first_name": "string",
        "contact_last_name": "string",
        "contact_email": "string",
        "contact_phone": "string"
      },
      "secondary_contact_email": {
        "contact_title": "string",
        "contact_name": "string",
        "contact_first_name": "string",
        "contact_last_name": "string",
        "contact_email": "string",
        "contact_phone": "string"
      },
      "set_aside": "string",
      "nsn": [
        "string"
      ],
      "val_est_low": "string",
      "val_est_high": "string",
      "pop_country": "string",
      "pop_state": "string",
      "pop_city": "string",
      "pop_zip": "string",
      "opp_key": "string",
      "version_key": "string",
      "source_type": "string",
      "dibbs_status": "string",
      "path": "string",
      "source_path": "string",
      "document_path": "string"
    }
  ],
  "meta": {
    "pagination": {
      "page": 1,
      "pages": 999,
      "count": 9999
    }
  },
  "links": {
    "first": "https://www.highergov.com/api/opportunity/?...page_number=1",
    "last": "https://www.highergov.com/api/opportunity/?...page_number=999",
    "next": "https://www.highergov.com/api/opportunity/?...page_number=2",
    "prev": null
  }
}
No links
400	
Bad Request

No links
403	
Invalid API Key

No links
404	
Requested Record Not Found

No links
People


GET
/api-external/people/

Description: Federal and State and Local People.
Update Frequency: Updated in real time. Update Check Field: as_of_date.

Parameters
Try it out
Name	Description
api_key *
string
(query)
API Key for authentication

Default value : your-api-key-here

your-api-key-here
contact_email
string
(query)
Email address

Examples: 
Select
contact_email
ordering
string
(query)
Which field to use when ordering the results.

Available values : -last_seen, last_seen


--
page_number
integer
(query)
A page number within the paginated result set.

page_number
page_size
string
(query)
Number of records returned per page (max 100)

Default value : 10

10
Responses
Code	Description	Links
200	
Success

Media type

application/json
Controls Accept header.
Example Value
Schema
{
  "results": [
    {
      "last_seen": "2025-08-04",
      "contact_first_name": "string",
      "contact_last_name": "string",
      "contact_name": "string",
      "contact_title": "string",
      "contact_email": "string",
      "contact_phone": "string",
      "contact_ext": "string",
      "contact_fax": "string",
      "agency": {
        "agency_key": 0,
        "agency_name": "string",
        "agency_abbreviation": "string",
        "agency_type": "string",
        "path": "string"
      },
      "contact_type": "string",
      "path": "string"
    }
  ],
  "meta": {
    "pagination": {
      "page": 1,
      "pages": 999,
      "count": 9999
    }
  },
  "links": {
    "first": "https://www.highergov.com/api/people/?...page_number=1",
    "last": "https://www.highergov.com/api/people/?...page_number=999",
    "next": "https://www.highergov.com/api/people/?...page_number=2",
    "prev": null
  }
}
No links
400	
Bad Request

No links
403	
Invalid API Key

No links
404	
Requested Record Not Found

No links
PSC


GET
/api-external/psc/

Description: Product Service Codes (PSC) Codes.
Update Frequency: Updated Ad Hoc when codes added or removed

Parameters
Try it out
Name	Description
api_key *
string
(query)
API Key for authentication

Default value : your-api-key-here

your-api-key-here
page_number
integer
(query)
A page number within the paginated result set.

page_number
page_size
string
(query)
Number of records returned per page (max 100)

Default value : 10

10
psc_code
string
(query)
PSC code

Examples: 
Select
psc_code
Responses
Code	Description	Links
200	
Success

Media type

application/json
Controls Accept header.
Example Value
Schema
{
  "results": [
    {
      "psc_code": "string",
      "psc_name": "string",
      "psc_description": "string",
      "active": true,
      "path": "string"
    }
  ],
  "meta": {
    "pagination": {
      "page": 1,
      "pages": 999,
      "count": 9999
    }
  },
  "links": {
    "first": "https://www.highergov.com/api/psc/?...page_number=1",
    "last": "https://www.highergov.com/api/psc/?...page_number=999",
    "next": "https://www.highergov.com/api/psc/?...page_number=2",
    "prev": null
  }
}
No links
400	
Bad Request

No links
403	
Invalid API Key

No links
404	
Requested Record Not Found

No links
Federal Subcontract


GET
/api-external/subcontract/

Description: Federal prime subcontract award data.
Update Frequency: Updated weekly.
Update Check Field: last_modified_date (note that data is often reported late by prime awardees and we recommend periodically looking back over the prior year to fully sync new records).

Parameters
Try it out
Name	Description
api_key *
string
(query)
API Key for authentication

Default value : your-api-key-here

your-api-key-here
awardee_key
integer
(query)
HigherGov Awardee Key

Examples: 
Select
awardee_key
awardee_key_parent
integer
(query)
HigherGov Awardee Key (Parent Level)

Examples: 
Select
awardee_key_parent
awardee_uei
string
(query)
Awardee UEI

Examples: 
Select
awardee_uei
awardee_uei_parent
string
(query)
Awardee UEI Parent

Examples: 
Select
awardee_uei_parent
awarding_agency_key
integer
(query)
HigherGov Awarding Agency key

Examples: 
Select
awarding_agency_key
funding_agency_key
integer
(query)
HigherGov Funding Agency key

Examples: 
Select
funding_agency_key
last_modified_date
string($date)
(query)
Last modified date filter (format: YYYY-MM-DD)

Examples: 
Select
last_modified_date
ordering
string
(query)
Which field to use when ordering the results.

Available values : -last_modified_date, -subaward_action_date, -subaward_amount_total, last_modified_date, subaward_action_date, subaward_amount_total


--
page_number
integer
(query)
A page number within the paginated result set.

page_number
page_size
string
(query)
Number of records returned per page (max 100)

Default value : 10

10
Responses
Code	Description	Links
200	
Success

Media type

application/json
Controls Accept header.
Example Value
Schema
{
  "results": [
    {
      "sub_awardee": {
        "awardee_key": 0,
        "clean_name": "string",
        "uei": "string",
        "cage_code": "string",
        "path": "string"
      },
      "sub_awardee_parent": {
        "awardee_key": 0,
        "clean_name": "string",
        "uei": "string",
        "cage_code": "string",
        "path": "string"
      },
      "subaward_id": "string",
      "subaward_action_date": "2025-08-04",
      "subaward_action_date_fiscal_year": "string",
      "subaward_amount_total": 0,
      "subaward_description": "string",
      "prime_contract_award_id": {
        "award_id": "string",
        "parent_award_id": "string",
        "latest_transaction_key": "string",
        "last_modified_date": "2025-08-04",
        "latest_action_date": "2025-08-04",
        "latest_action_date_fiscal_year": 0,
        "awardee": {
          "awardee_key": 0,
          "clean_name": "string",
          "uei": "string",
          "cage_code": "string",
          "path": "string"
        },
        "awardee_parent": {
          "awardee_key": 0,
          "clean_name": "string",
          "uei": "string",
          "cage_code": "string",
          "path": "string"
        },
        "awarding_agency": {
          "agency_key": 0,
          "agency_name": "string",
          "agency_abbreviation": "string",
          "agency_type": "string",
          "path": "string"
        },
        "funding_agency": {
          "agency_key": 0,
          "agency_name": "string",
          "agency_abbreviation": "string",
          "agency_type": "string",
          "path": "string"
        },
        "vehicle": {
          "vehicle_key": 0,
          "vehicle_name": "string",
          "vehicle_description": "string",
          "path": "string"
        },
        "federal_supply_schedule_award_id": "string",
        "parent_award_type": "string",
        "period_of_performance_start_date": "2025-08-04",
        "period_of_performance_current_end_date": "2025-08-04",
        "period_of_performance_potential_end_date": "2025-08-04",
        "total_dollars_obligated": 0,
        "current_total_value_of_award": 0,
        "potential_total_value_of_award": 0,
        "award_type": "string",
        "award_description_original": "string",
        "alt_description": "string",
        "solicitation_identifier": "string",
        "related_opportunity_title": "string",
        "psc_code": {
          "psc_code": "string",
          "psc_name": "string",
          "psc_description": "string",
          "active": true,
          "path": "string"
        },
        "naics_code": {
          "naics_code": "string",
          "naics_description": "string",
          "active": true,
          "path": "string"
        },
        "primary_place_of_performance_zip": "string",
        "primary_place_of_performance_county_name": "string",
        "primary_place_of_performance_city_name": "string",
        "primary_place_of_performance_state_code": "string",
        "primary_place_of_performance_state_name": "string",
        "primary_place_of_performance_country_name": "string",
        "type_of_agreement": "string",
        "type_of_contract_pricing_description": "string",
        "national_interest_action": "string",
        "defense_program": "string",
        "other_statutory_authority": "string",
        "dod_claimant_program_code": "string",
        "subcontracting_plan": "string",
        "research": "string",
        "type_of_set_aside": "string",
        "number_of_offers_received": "string",
        "extent_competed": "string",
        "solicitation_procedures": "string",
        "evaluated_preference": "string",
        "clinger_cohen_act_planning": "string",
        "fair_opportunity_limited_sources": "string",
        "other_than_full_and_open_competition": "string",
        "created_by": {
          "contact_title": "string",
          "contact_name": "string",
          "contact_first_name": "string",
          "contact_last_name": "string",
          "contact_email": "string",
          "contact_phone": "string"
        },
        "last_modified_by": {
          "contact_title": "string",
          "contact_name": "string",
          "contact_first_name": "string",
          "contact_last_name": "string",
          "contact_email": "string",
          "contact_phone": "string"
        },
        "approved_by": {
          "contact_title": "string",
          "contact_name": "string",
          "contact_first_name": "string",
          "contact_last_name": "string",
          "contact_email": "string",
          "contact_phone": "string"
        },
        "path": "string"
      },
      "prime_idv_award_id": "string",
      "last_modified_date": "2025-08-04",
      "path": "string"
    }
  ],
  "meta": {
    "pagination": {
      "page": 1,
      "pages": 999,
      "count": 9999
    }
  },
  "links": {
    "first": "https://www.highergov.com/api/federal subcontract/?...page_number=1",
    "last": "https://www.highergov.com/api/federal subcontract/?...page_number=999",
    "next": "https://www.highergov.com/api/federal subcontract/?...page_number=2",
    "prev": null
  }
}
No links
400	
Bad Request

No links
403	
Invalid API Key

No links
404	
Requested Record Not Found

No links
Federal Subgrant


GET
/api-external/subgrant/

Description: Federal prime subgrant award data.
Update Frequency: Updated weekly.
Update Check Field: last_modified_date (note that data is often reported late by prime awardees and we recommend periodically looking back over the prior year to fully sync new records).

Parameters
Try it out
Name	Description
api_key *
string
(query)
API Key for authentication

Default value : your-api-key-here

your-api-key-here
awardee_key
integer
(query)
HigherGov Awardee Key

Examples: 
Select
awardee_key
awardee_key_parent
integer
(query)
HigherGov Awardee Key (Parent Level)

Examples: 
Select
awardee_key_parent
awardee_uei
string
(query)
Awardee UEI

Examples: 
Select
awardee_uei
awardee_uei_parent
string
(query)
Awardee UEI Parent

Examples: 
Select
awardee_uei_parent
awarding_agency_key
integer
(query)
HigherGov Awarding Agency key

Examples: 
Select
awarding_agency_key
funding_agency_key
integer
(query)
HigherGov Funding Agency key

Examples: 
Select
funding_agency_key
last_modified_date
string($date)
(query)
Last modified date filter (format: YYYY-MM-DD)

Examples: 
Select
last_modified_date
ordering
string
(query)
Which field to use when ordering the results.

Available values : -last_modified_date, -subaward_action_date, -subaward_amount_total, last_modified_date, subaward_action_date, subaward_amount_total


--
page_number
integer
(query)
A page number within the paginated result set.

page_number
page_size
string
(query)
Number of records returned per page (max 100)

Default value : 10

10
Responses
Code	Description	Links
200	
Success

Media type

application/json
Controls Accept header.
Example Value
Schema
{
  "results": [
    {
      "sub_awardee": {
        "awardee_key": 0,
        "clean_name": "string",
        "uei": "string",
        "cage_code": "string",
        "path": "string"
      },
      "sub_awardee_parent": {
        "awardee_key": 0,
        "clean_name": "string",
        "uei": "string",
        "cage_code": "string",
        "path": "string"
      },
      "subaward_id": "string",
      "subaward_action_date": "2025-08-04",
      "subaward_action_date_fiscal_year": "string",
      "subaward_amount_total": 0,
      "subaward_description": "string",
      "prime_grant_award_id": {
        "award_id": "string",
        "awardee_key": {
          "awardee_key": 0,
          "clean_name": "string",
          "uei": "string",
          "cage_code": "string",
          "path": "string"
        },
        "awardee_key_parent": {
          "awardee_key": 0,
          "clean_name": "string",
          "uei": "string",
          "cage_code": "string",
          "path": "string"
        },
        "assistance_type_code": "string",
        "latest_transaction_key": "string",
        "last_modified_date": "2025-08-04T21:39:54.392Z",
        "latest_action_date": "2025-08-04",
        "latest_action_date_fiscal_year": 0,
        "period_of_performance_start_date": "2025-08-04",
        "period_of_performance_current_end_date": "2025-08-04",
        "total_obligated_amount": 0,
        "federal_action_obligation": 0,
        "non_federal_funding_amount": 0,
        "solicitation_identifier": "string",
        "primary_place_of_performance_zip": "string",
        "primary_place_of_performance_county_name": "string",
        "primary_place_of_performance_city_name": "string",
        "primary_place_of_performance_state_code": "string",
        "primary_place_of_performance_state_name": "string",
        "primary_place_of_performance_country_name": "string",
        "award_description_original": "string",
        "grant_program": {
          "cfda_program_number": "string",
          "active": true,
          "program_title": "string",
          "popular_program_title": "string"
        },
        "awarding_agency": {
          "agency_key": 0,
          "agency_name": "string",
          "agency_abbreviation": "string",
          "agency_type": "string",
          "path": "string"
        },
        "funding_agency": {
          "agency_key": 0,
          "agency_name": "string",
          "agency_abbreviation": "string",
          "agency_type": "string",
          "path": "string"
        },
        "path": "string"
      },
      "last_modified_date": "2025-08-04",
      "path": "string"
    }
  ],
  "meta": {
    "pagination": {
      "page": 1,
      "pages": 999,
      "count": 9999
    }
  },
  "links": {
    "first": "https://www.highergov.com/api/federal subgrant/?...page_number=1",
    "last": "https://www.highergov.com/api/federal subgrant/?...page_number=999",
    "next": "https://www.highergov.com/api/federal subgrant/?...page_number=2",
    "prev": null
  }
}
No links
400	
Bad Request

No links
403	
Invalid API Key

No links
404	
Requested Record Not Found

No links
Vehicle


GET
/api-external/vehicle/

Description: Federal multi-award contract vehicles.
Update Frequency: Updated ad hoc as new awards are made.

Parameters
Try it out
Name	Description
api_key *
string
(query)
API Key for authentication

Default value : your-api-key-here

your-api-key-here
ordering
string
(query)
Which field to use when ordering the results.

Available values : -award_date, award_date


--
page_number
integer
(query)
A page number within the paginated result set.

page_number
page_size
string
(query)
Number of records returned per page (max 100)

Default value : 10

10
vehicle_key
integer
(query)
HigherGov Vehicle key

Examples: 
Select
vehicle_key
Responses
Code	Description	Links
200	
Success

Media type

application/json
Controls Accept header.
Example Value
Schema
{
  "results": [
    {
      "vehicle_key": 0,
      "vehicle_name": "string",
      "vehicle_description": "string",
      "shared_ceiling": 0,
      "vehicle_type": "string",
      "naics_code": {
        "naics_code": "string",
        "naics_description": "string",
        "naics_description_long": "string",
        "active": true,
        "path": "string"
      },
      "psc_code": {
        "psc_code": "string",
        "psc_name": "string",
        "psc_description": "string",
        "active": true,
        "path": "string"
      },
      "type_of_set_aside": "string",
      "who_can_use": "string",
      "award_date": "2025-08-04",
      "last_date_to_order": "2025-08-04",
      "associated_solicitation": "string",
      "primary_sponsor_agency": {
        "agency_key": 0,
        "agency_name": "string",
        "agency_abbreviation": "string",
        "agency_type": "string",
        "path": "string"
      },
      "predecessor_vehicle": "string",
      "successor_vehicle": "string",
      "path": "string"
    }
  ],
  "meta": {
    "pagination": {
      "page": 1,
      "pages": 999,
      "count": 9999
    }
  },
  "links": {
    "first": "https://www.highergov.com/api/vehicle/?...page_number=1",
    "last": "https://www.highergov.com/api/vehicle/?...page_number=999",
    "next": "https://www.highergov.com/api/vehicle/?...page_number=2",
    "prev": null
  }
}
No links
400	
Bad Request

No links
403	
Invalid API Key

No links
404	
Requested Record Not Found

No links

Schemas
Agency{
description:	
A type of ModelSerializer that uses hyperlinked relationships instead of primary key relationships. Specifically:

A 'url' field is included instead of the 'id' field.
Relationships to other instances are hyperlinks, instead of primary keys.
Included Mixins:

A mixin class to enable sparse fieldsets is included
A mixin class to enable validation of included resources is included
agency_key*	[...]
agency_name*	[...]
agency_abbreviation*	[...]
agency_type*	[...]
defense_flag*	[...]
level_1*	[...]
level_2*	[...]
level_3*	[...]
level_4*	[...]
level_5*	[...]
level_6*	[...]
level_7*	[...]
path*	[...]
}
AgencySimple{
description:	
A type of ModelSerializer that uses hyperlinked relationships instead of primary key relationships. Specifically:

A 'url' field is included instead of the 'id' field.
Relationships to other instances are hyperlinks, instead of primary keys.
Included Mixins:

A mixin class to enable sparse fieldsets is included
A mixin class to enable validation of included resources is included
agency_key*	[...]
agency_name*	[...]
agency_abbreviation*	[...]
agency_type*	[...]
path*	[...]
}
Assistance{
description:	
A type of ModelSerializer that uses hyperlinked relationships instead of primary key relationships. Specifically:

A 'url' field is included instead of the 'id' field.
Relationships to other instances are hyperlinks, instead of primary keys.
Included Mixins:

A mixin class to enable sparse fieldsets is included
A mixin class to enable validation of included resources is included
cfda_program_number*	[...]
active	[...]
program_title*	[...]
popular_program_title*	[...]
primary_agency*	AgencySimple{...}
date_modified*	[...]
date_posted*	[...]
cfda_objective*	[...]
type_of_assistance*	[...]
applicant_eligibility*	[...]
beneficiary_eligibility*	[...]
path*	[...]
}
Awardee{
description:	
A type of ModelSerializer that uses hyperlinked relationships instead of primary key relationships. Specifically:

A 'url' field is included instead of the 'id' field.
Relationships to other instances are hyperlinks, instead of primary keys.
Included Mixins:

A mixin class to enable sparse fieldsets is included
A mixin class to enable validation of included resources is included
awardee_key*	[...]
awardee_key_parent*	AwardeeSimple{...}
parent_flag*	[...]
clean_name*	[...]
legal_business_name*	[...]
dba_name*	[...]
entity_division_name*	[...]
entity_division_number*	[...]
uei*	[...]
cage_code*	[...]
purpose_of_registration*	[...]
initial_registration_date*	[...]
registration_expiration_date*	[...]
registration_last_update_date*	[...]
registration_activation_date*	[...]
year_founded*	[...]
employee_count*	[...]
physical_address_line_1*	[...]
physical_address_line_2*	[...]
physical_address_city*	[...]
physical_address_province_or_state*	[...]
physical_address_zip_postal_code*	[...]
physical_address_zip_code_4*	[...]
physical_address_country_code*	[...]
govt_bus_poc_first_name*	[...]
govt_bus_poc_last_name*	[...]
govt_bus_poc_title*	[...]
govt_bus_poc_st_add_1*	[...]
govt_bus_poc_st_add_2*	[...]
govt_bus_poc_city*	[...]
govt_bus_poc_zip_postal_code*	[...]
govt_bus_state_or_province*	[...]
govt_bus_poc_country_code*	[...]
website*	[...]
primary_naics*	{...}
naics_codes*	[...]
psc_codes*	[...]
bus_type_info*	[...]
path*	[...]
}
AwardeeMP{
awardee_key_protege*	AwardeeSimple{...}
awardee_key_mentor*	AwardeeSimple{...}
awardee_key_protege_parent*	AwardeeSimple{...}
awardee_key_mentor_parent*	AwardeeSimple{...}
active_flag*	[...]
primary_naics*	{...}
}
AwardeePartnership{
awardee_key_prime*	AwardeeSimple{...}
awardee_key_sub*	AwardeeSimple{...}
awardee_key_prime_parent*	AwardeeSimple{...}
awardee_key_sub_parent*	AwardeeSimple{...}
number_of_awards*	[...]
total_awards*	[...]
most_recent_date*	[...]
relationship_type*	[...]
}
AwardeeSimple{
description:	
A type of ModelSerializer that uses hyperlinked relationships instead of primary key relationships. Specifically:

A 'url' field is included instead of the 'id' field.
Relationships to other instances are hyperlinks, instead of primary keys.
Included Mixins:

A mixin class to enable sparse fieldsets is included
A mixin class to enable validation of included resources is included
awardee_key*	[...]
clean_name*	[...]
uei*	[...]
cage_code*	[...]
path*	[...]
}
Federal Contract{
description:	
A type of ModelSerializer that uses hyperlinked relationships instead of primary key relationships. Specifically:

A 'url' field is included instead of the 'id' field.
Relationships to other instances are hyperlinks, instead of primary keys.
Included Mixins:

A mixin class to enable sparse fieldsets is included
A mixin class to enable validation of included resources is included
award_id*	[...]
parent_award_id*	[...]
latest_transaction_key*	[...]
last_modified_date*	[...]
latest_action_date*	[...]
latest_action_date_fiscal_year*	[...]
awardee*	{...}
nullable: true
awardee_parent*	{...}
nullable: true
awarding_agency*	AgencySimple{...}
funding_agency*	AgencySimple{...}
vehicle*	{...}
nullable: true
federal_supply_schedule_award_id*	[...]
parent_award_type*	[...]
period_of_performance_start_date*	[...]
period_of_performance_current_end_date*	[...]
period_of_performance_potential_end_date*	[...]
total_dollars_obligated*	[...]
current_total_value_of_award*	[...]
potential_total_value_of_award*	[...]
award_type*	[...]
award_description_original*	[...]
alt_description*	[...]
solicitation_identifier*	[...]
related_opportunity_title*	[...]
psc_code*	{...}
naics_code*	{...}
primary_place_of_performance_zip*	[...]
primary_place_of_performance_county_name*	[...]
primary_place_of_performance_city_name*	[...]
primary_place_of_performance_state_code*	[...]
primary_place_of_performance_state_name*	[...]
primary_place_of_performance_country_name*	[...]
type_of_agreement*	[...]
type_of_contract_pricing_description*	[...]
national_interest_action*	[...]
defense_program*	[...]
other_statutory_authority*	[...]
dod_claimant_program_code*	[...]
subcontracting_plan*	[...]
research*	[...]
type_of_set_aside*	[...]
number_of_offers_received*	[...]
extent_competed*	[...]
solicitation_procedures*	[...]
evaluated_preference*	[...]
clinger_cohen_act_planning*	[...]
fair_opportunity_limited_sources*	[...]
other_than_full_and_open_competition*	[...]
created_by*	{...}
nullable: true
last_modified_by*	{...}
nullable: true
approved_by*	{...}
nullable: true
path*	[...]
}
Federal Grant{
description:	
A type of ModelSerializer that uses hyperlinked relationships instead of primary key relationships. Specifically:

A 'url' field is included instead of the 'id' field.
Relationships to other instances are hyperlinks, instead of primary keys.
Included Mixins:

A mixin class to enable sparse fieldsets is included
A mixin class to enable validation of included resources is included
award_id*	[...]
awardee_key*	{...}
nullable: true
awardee_key_parent*	{...}
nullable: true
assistance_type_code*	[...]
latest_transaction_key*	[...]
last_modified_date*	[...]
latest_action_date*	[...]
latest_action_date_fiscal_year*	[...]
period_of_performance_start_date*	[...]
period_of_performance_current_end_date*	[...]
total_obligated_amount*	[...]
federal_action_obligation*	[...]
non_federal_funding_amount*	[...]
solicitation_identifier*	[...]
primary_place_of_performance_zip*	[...]
primary_place_of_performance_county_name*	[...]
primary_place_of_performance_city_name*	[...]
primary_place_of_performance_state_code*	[...]
primary_place_of_performance_state_name*	[...]
primary_place_of_performance_country_name*	[...]
award_description_original*	[...]
grant_program*	Grant Program{...}
awarding_agency*	AgencySimple{...}
funding_agency*	AgencySimple{...}
path*	[...]
}
Federal IDV{
description:	
A type of ModelSerializer that uses hyperlinked relationships instead of primary key relationships. Specifically:

A 'url' field is included instead of the 'id' field.
Relationships to other instances are hyperlinks, instead of primary keys.
Included Mixins:

A mixin class to enable sparse fieldsets is included
A mixin class to enable validation of included resources is included
award_id*	[...]
parent_award_id*	[...]
latest_transaction_key*	[...]
last_modified_date*	[...]
latest_action_date*	[...]
latest_action_date_fiscal_year*	[...]
awardee_key*	{...}
nullable: true
awardee_key_parent*	{...}
nullable: true
awarding_agency*	AgencySimple{...}
funding_agency*	AgencySimple{...}
vehicle*	{...}
nullable: true
who_can_use*	[...]
federal_supply_schedule_award_id*	[...]
parent_award_type*	[...]
period_of_performance_start_date*	[...]
ordering_period_end_date*	[...]
potential_total_value_of_award*	[...]
award_type*	[...]
award_description_original*	[...]
alt_description*	[...]
solicitation_identifier*	[...]
related_opportunity_title*	[...]
psc_code*	{...}
naics_code*	{...}
type_of_agreement*	[...]
type_of_contract_pricing_description*	[...]
national_interest_action*	[...]
defense_program*	[...]
other_statutory_authority*	[...]
dod_claimant_program_code*	[...]
subcontracting_plan*	[...]
contracting_officers_determination_of_business_size_code*	[...]
cost_or_pricing_data*	[...]
competitive_procedures*	[...]
fair_opportunity_limited_sources*	[...]
other_than_full_and_open_competition*	[...]
clinger_cohen_act_planning*	[...]
research*	[...]
type_of_set_aside*	[...]
number_of_offers_received*	[...]
extent_competed*	[...]
solicitation_procedures*	[...]
evaluated_preference*	[...]
status_code*	[...]
closed_status*	[...]
created_by*	{...}
nullable: true
last_modified_by*	{...}
nullable: true
approved_by*	{...}
nullable: true
path*	[...]
}
Federal Subcontract{
description:	
A type of ModelSerializer that uses hyperlinked relationships instead of primary key relationships. Specifically:

A 'url' field is included instead of the 'id' field.
Relationships to other instances are hyperlinks, instead of primary keys.
Included Mixins:

A mixin class to enable sparse fieldsets is included
A mixin class to enable validation of included resources is included
sub_awardee*	{...}
nullable: true
sub_awardee_parent*	{...}
nullable: true
subaward_id*	[...]
subaward_action_date*	[...]
subaward_action_date_fiscal_year*	[...]
subaward_amount_total*	[...]
subaward_description*	[...]
prime_contract_award_id*	Federal Contract{...}
prime_idv_award_id*	[...]
last_modified_date*	[...]
path*	[...]
}
Federal Subgrant{
description:	
A type of ModelSerializer that uses hyperlinked relationships instead of primary key relationships. Specifically:

A 'url' field is included instead of the 'id' field.
Relationships to other instances are hyperlinks, instead of primary keys.
Included Mixins:

A mixin class to enable sparse fieldsets is included
A mixin class to enable validation of included resources is included
sub_awardee*	{...}
nullable: true
sub_awardee_parent*	{...}
nullable: true
subaward_id*	[...]
subaward_action_date*	[...]
subaward_action_date_fiscal_year*	[...]
subaward_amount_total*	[...]
subaward_description*	[...]
prime_grant_award_id*	Federal Grant{...}
last_modified_date*	[...]
path*	[...]
}
FileTracker{
file_name	[...]
file_type	[...]
file_size	File Size (bytes)[...]
posted_date	[...]
text_extract*	[...]
summary	[...]
download_url*	[...]
}
Grant Program{
description:	
A type of ModelSerializer that uses hyperlinked relationships instead of primary key relationships. Specifically:

A 'url' field is included instead of the 'id' field.
Relationships to other instances are hyperlinks, instead of primary keys.
Included Mixins:

A mixin class to enable sparse fieldsets is included
A mixin class to enable validation of included resources is included
cfda_program_number*	[...]
active	[...]
program_title*	[...]
popular_program_title*	[...]
}
LookupComboOpportunityType{
description	[...]
}
NAICS{
description:	
A type of ModelSerializer that uses hyperlinked relationships instead of primary key relationships. Specifically:

A 'url' field is included instead of the 'id' field.
Relationships to other instances are hyperlinks, instead of primary keys.
Included Mixins:

A mixin class to enable sparse fieldsets is included
A mixin class to enable validation of included resources is included
naics_code*	[...]
naics_description*	[...]
naics_description_long*	[...]
active*	[...]
path*	[...]
}
NAICSSimple{
description:	
A type of ModelSerializer that uses hyperlinked relationships instead of primary key relationships. Specifically:

A 'url' field is included instead of the 'id' field.
Relationships to other instances are hyperlinks, instead of primary keys.
Included Mixins:

A mixin class to enable sparse fieldsets is included
A mixin class to enable validation of included resources is included
naics_code*	[...]
naics_description*	[...]
active*	[...]
path*	[...]
}
NSN{
nsn*	[...]
niin	[...]
fsc	PSC[...]
nomenclature	[...]
opp_count	[...]
part_numbers	[...]
end_item_name	[...]
amc	[...]
amsc	[...]
ui	[...]
distributor_use*	[...]
last_price*	[...]
unit_price*	[...]
suppliers*	[...]
awards*	[...]
}
Naics{
naics_code	NAICS[...]
}
Opportunity{
description:	
A type of ModelSerializer that uses hyperlinked relationships instead of primary key relationships. Specifically:

A 'url' field is included instead of the 'id' field.
Relationships to other instances are hyperlinks, instead of primary keys.
Included Mixins:

A mixin class to enable sparse fieldsets is included
A mixin class to enable validation of included resources is included
opp_cat*	[...]
title*	[...]
description_text*	[...]
ai_summary*	[...]
source_id*	[...]
source_id_version*	[...]
captured_date*	[...]
posted_date*	[...]
due_date*	[...]
agency*	AgencySimple{...}
naics_code*	{...}
psc_code*	{...}
opp_type*	{...}
primary_contact_email*	PeopleSimple{...}
secondary_contact_email*	PeopleSimple{...}
set_aside*	[...]
nsn*	[...]
val_est_low*	[...]
val_est_high*	[...]
pop_country*	[...]
pop_state*	[...]
pop_city*	[...]
pop_zip*	[...]
opp_key	[...]
version_key	[...]
source_type*	[...]
dibbs_status*	[...]
path*	[...]
source_path	[...]
document_path*	[...]
}
PSC{
description:	
A type of ModelSerializer that uses hyperlinked relationships instead of primary key relationships. Specifically:

A 'url' field is included instead of the 'id' field.
Relationships to other instances are hyperlinks, instead of primary keys.
Included Mixins:

A mixin class to enable sparse fieldsets is included
A mixin class to enable validation of included resources is included
psc_code*	[...]
psc_name*	[...]
psc_description*	[...]
active*	[...]
path*	[...]
}
PaginatedAgencyList{
results	[...]
meta	{...}
links	{...}
}
PaginatedAssistanceList{
results	[...]
meta	{...}
links	{...}
}
PaginatedAwardeeList{
results	[...]
meta	{...}
links	{...}
}
PaginatedAwardeeMPList{
results	[...]
meta	{...}
links	{...}
}
PaginatedAwardeePartnershipList{
results	[...]
meta	{...}
links	{...}
}
PaginatedFederal ContractList{
results	[...]
meta	{...}
links	{...}
}
PaginatedFederal GrantList{
results	[...]
meta	{...}
links	{...}
}
PaginatedFederal IDVList{
results	[...]
meta	{...}
links	{...}
}
PaginatedFederal SubcontractList{
results	[...]
meta	{...}
links	{...}
}
PaginatedFederal SubgrantList{
results	[...]
meta	{...}
links	{...}
}
PaginatedFileTrackerList{
results	[...]
meta	{...}
links	{...}
}
PaginatedNAICSList{
results	[...]
meta	{...}
links	{...}
}
PaginatedNSNList{
results	[...]
meta	{...}
links	{...}
}
PaginatedOpportunityList{
results	[...]
meta	{...}
links	{...}
}
PaginatedPSCList{
results	[...]
meta	{...}
links	{...}
}
PaginatedPeopleList{
results	[...]
meta	{...}
links	{...}
}
PaginatedVehicleList{
results	[...]
meta	{...}
links	{...}
}
People{
description:	
A type of ModelSerializer that uses hyperlinked relationships instead of primary key relationships. Specifically:

A 'url' field is included instead of the 'id' field.
Relationships to other instances are hyperlinks, instead of primary keys.
Included Mixins:

A mixin class to enable sparse fieldsets is included
A mixin class to enable validation of included resources is included
last_seen*	[...]
contact_first_name	First Name[...]
contact_last_name	Last Name[...]
contact_name*	[...]
contact_title*	[...]
contact_email*	[...]
contact_phone*	[...]
contact_ext*	[...]
contact_fax*	[...]
agency*	AgencySimple{...}
contact_type*	[...]
path*	[...]
}
PeopleSimple{
description:	
A type of ModelSerializer that uses hyperlinked relationships instead of primary key relationships. Specifically:

A 'url' field is included instead of the 'id' field.
Relationships to other instances are hyperlinks, instead of primary keys.
Included Mixins:

A mixin class to enable sparse fieldsets is included
A mixin class to enable validation of included resources is included
contact_title*	[...]
contact_name*	[...]
contact_first_name*	[...]
contact_last_name*	[...]
contact_email*	[...]
contact_phone*	[...]
}
Psc{
psc_code	PSC[...]
}
Vehicle{
description:	
A type of ModelSerializer that uses hyperlinked relationships instead of primary key relationships. Specifically:

A 'url' field is included instead of the 'id' field.
Relationships to other instances are hyperlinks, instead of primary keys.
Included Mixins:

A mixin class to enable sparse fieldsets is included
A mixin class to enable validation of included resources is included
vehicle_key*	[...]
vehicle_name*	[...]
vehicle_description*	[...]
shared_ceiling*	[...]
vehicle_type*	[...]
naics_code*	{...}
psc_code*	{...}
type_of_set_aside*	[...]
who_can_use*	[...]
award_date*	[...]
last_date_to_order*	[...]
associated_solicitation*	[...]
primary_sponsor_agency*	{...}
nullable: true
predecessor_vehicle*	[...]
successor_vehicle*	[...]
path*	[...]
}
VehicleSimple{
description:	
A type of ModelSerializer that uses hyperlinked relationships instead of primary key relationships. Specifically:

A 'url' field is included instead of the 'id' field.
Relationships to other instances are hyperlinks, instead of primary keys.
Included Mixins:

A mixin class to enable sparse fieldsets is included
A mixin class to enable validation of included resources is included
vehicle_key*	[...]
vehicle_name*	[...]
vehicle_description*	[...]
path*	[...]
}

