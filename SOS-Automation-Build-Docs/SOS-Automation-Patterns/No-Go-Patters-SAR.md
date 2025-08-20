{
  "category": "sar_patterns_enhanced",
  "pattern_groups": [
    {
      "group_name": "ocr_pdf_error_patterns",
      "regex_patterns": [
        "(?i)sour[c\\s]*e\\s*appro[v\\s]*al\\s*req[u\\s]*ired",
        "(?i)sourc[e\\s]*eapprov[a\\s]*alrequir[e\\s]*d",
        "(?i)s\\s*o\\s*u\\s*r\\s*c\\s*e\\s*a\\s*p\\s*p\\s*r\\s*o\\s*v\\s*a\\s*l",
        "(?i)sourcapproval",
        "(?i)sourceapprova1",
        "(?i)s0urce\\s*appr0val",
        "(?i)sourc[e\\s]*appro[vw]al",
        "(?i)source\\s*appro[uv]al",
        "(?i)sourc[e\\s]*appro\\.al",
        "(?i)sourc[e\\s]*appro\\-val",
        "(?i)sourc[e\\s]*appro\\s*val",
        "(?i)saurce\\s*approval",
        "(?i)scurce\\s*approval",
        "(?i)sourcc\\s*approval"
      ],
      "exact_phrases": [],
      "partial_triggers": [
        "sourc eapproval",
        "sourceapprova1",
        "s0urce appr0val",
        "sourcapproval",
        "saurce approval",
        "scurce approval"
      ],
      "context_patterns": [],
      "agency_specific": {},
      "negative_patterns": [],
      "code_triggers": {},
      "compound_patterns": [],
      "scoring_weights": {
        "regex_match": 0.85,
        "partial_match": 0.75
      }
    },
    {
      "group_name": "html_scraping_artifacts",
      "regex_patterns": [
        "(?i)&nbsp;sourc[e\\s]*approv[a-z]*&nbsp;",
        "(?i)<[^>]*>sourc[e\\s]*approv[a-z]*<[^>]*>",
        "(?i)\\&quot;sourc[e\\s]*approv[a-z]*\\&quot;",
        "(?i)&#\\d+;sourc[e\\s]*approv[a-z]*",
        "(?i)sourc[e\\s]*approv[a-z]*\\s*<br\\s*/?>",
        "(?i)sourc[e\\s]*approv[a-z]*\\s*\\n\\s*requir[a-z]*"
      ],
      "exact_phrases": [],
      "partial_triggers": [],
      "context_patterns": [],
      "agency_specific": {},
      "negative_patterns": [],
      "code_triggers": {},
      "compound_patterns": [],
      "scoring_weights": {
        "regex_match": 0.8
      }
    },
    {
      "group_name": "government_typos_misspellings",
      "regex_patterns": [
        "(?i)sorce\\s*apporval",
        "(?i)souce\\s*aproval",
        "(?i)sourece\\s*approvel",
        "(?i)sourch\\s*approal",
        "(?i)sourse\\s*apprval",
        "(?i)sourde\\s*appoval",
        "(?i)sourc\\s*approvel",
        "(?i)source\\s*appoval",
        "(?i)source\\s*aproval",
        "(?i)source\\s*appproval",
        "(?i)source\\s*approuval",
        "(?i)source\\s*approvall",
        "(?i)source\\s*aprroval",
        "(?i)surce\\s*approval",
        "(?i)soure\\s*approval"
      ],
      "exact_phrases": [
        "sorce apporval required",
        "souce aproval required",
        "sourece approvel required",
        "sourse apprval required"
      ],
      "partial_triggers": [],
      "context_patterns": [],
      "agency_specific": {},
      "negative_patterns": [],
      "code_triggers": {},
      "compound_patterns": [],
      "scoring_weights": {
        "regex_match": 0.85,
        "exact_match": 0.9
      }
    },
    {
      "group_name": "extreme_abbreviations",
      "regex_patterns": [
        "(?i)src\\s*appr\\s*req",
        "(?i)SA\\s*req",
        "(?i)SAR\\s*req'd",
        "(?i)s/a\\s*req",
        "(?i)s\\.a\\.\\s*req",
        "(?i)src\\s*app\\s*rqd",
        "(?i)sc\\s*apvl\\s*req",
        "(?i)src\\s*aprvl\\s*rqrd",
        "(?i)s\\.\\s*appr\\.\\s*req\\.",
        "(?i)sourc\\.\\s*app\\.\\s*req\\.",
        "(?i)govt\\.?\\s*src\\s*appr",
        "(?i)gov't\\s*src\\s*appr",
        "(?i)GOV\\s*SA\\s*REQ"
      ],
      "exact_phrases": [
        "SA REQ",
        "SAR REQ'D",
        "SRC APPR REQ",
        "S/A REQ",
        "GOV SA REQ"
      ],
      "partial_triggers": [],
      "context_patterns": [],
      "agency_specific": {},
      "negative_patterns": [],
      "code_triggers": {},
      "compound_patterns": [],
      "scoring_weights": {
        "regex_match": 0.8,
        "exact_match": 0.85
      }
    },
    {
      "group_name": "boilerplate_templates",
      "regex_patterns": [
        "(?i)\\[?source\\s*approval\\s*required\\]?",
        "(?i)\\{source\\s*approval\\s*required\\}",
        "(?i)\\(source\\s*approval\\s*required\\)",
        "(?i)\\*+\\s*source\\s*approval\\s*required\\s*\\*+",
        "(?i)_+source\\s*approval\\s*required_+",
        "(?i)\\-+\\s*source\\s*approval\\s*required\\s*\\-+",
        "(?i)NOTE:\\s*source\\s*approval\\s*required",
        "(?i)NOTICE:\\s*source\\s*approval\\s*required",
        "(?i)IMPORTANT:\\s*source\\s*approval\\s*required",
        "(?i)WARNING:\\s*source\\s*approval\\s*required",
        "(?i)ATTENTION:\\s*source\\s*approval\\s*required",
        "(?i)\\*\\*\\*\\s*source\\s*approval\\s*required\\s*\\*\\*\\*"
      ],
      "exact_phrases": [
        "[SOURCE APPROVAL REQUIRED]",
        "{SOURCE APPROVAL REQUIRED}",
        "(SOURCE APPROVAL REQUIRED)",
        "***SOURCE APPROVAL REQUIRED***",
        "NOTE: Source approval required",
        "IMPORTANT: Source approval required"
      ],
      "partial_triggers": [],
      "context_patterns": [],
      "agency_specific": {},
      "negative_patterns": [],
      "code_triggers": {},
      "compound_patterns": [],
      "scoring_weights": {
        "regex_match": 0.9,
        "exact_match": 0.95
      }
    },
    {
      "group_name": "nsn_with_sar_requirements",
      "regex_patterns": [
        "(?i)NSN\\s*(?:\\d{2}|7R)[-\\s]?\\d{4}[-\\s]?\\d{2}[-\\s]?\\d{3}[-\\s]?\\d{4}[-\\s]?[A-Z0-9]{2}\\s*(?:.*)?(?:SAR|source\\s*approval)",
        "(?i)NSN:?\\s*(?:\\d{2}|7R)[-\\s]?\\d{4}[-\\s]?\\d{2}[-\\s]?\\d{7}\\s*(?:.*)?approv[a-z]*",
        "(?i)(?:\\d{4}[-\\s]?\\d{2}[-\\s]?\\d{3}[-\\s]?\\d{4})\\s*(?:.*)?source\\s*control",
        "(?i)P/N\\s*[A-Z0-9\\-]+\\s*(?:.*)?approv[a-z]*\\s*source",
        "(?i)PN:\\s*[A-Z0-9\\-]+\\s*(?:.*)?SAR"
      ],
      "exact_phrases": [],
      "partial_triggers": [
        "NSN 7R",
        "NSN: 7R",
        "P/N",
        "PN:"
      ],
      "context_patterns": [],
      "agency_specific": {},
      "negative_patterns": [],
      "code_triggers": {},
      "compound_patterns": [],
      "scoring_weights": {
        "regex_match": 0.75
      }
    },
    {
      "group_name": "dfars_far_clause_patterns",
      "regex_patterns": [
        "(?i)DFARS\\s*(?:clause\\s*)?252\\.209[-\\.]?7010",
        "(?i)DFARS\\s*252\\.246[-\\.]?70[0-9]{2}",
        "(?i)FAR\\s*(?:clause\\s*)?52\\.209[-\\.]?[0-9]+",
        "(?i)FAR\\s*52\\.246[-\\.]?[0-9]+",
        "(?i)(?:clause|provision)\\s*252\\.209",
        "(?i)(?:clause|provision)\\s*52\\.209",
        "(?i)Critical\\s*Safety\\s*Item.*DFARS",
        "(?i)CSI.*252\\.209"
      ],
      "exact_phrases": [
        "DFARS 252.209-7010",
        "DFARS clause 252.209-7010",
        "FAR 52.209",
        "FAR 52.246"
      ],
      "partial_triggers": [
        "252.209",
        "52.209",
        "52.246"
      ],
      "context_patterns": [],
      "agency_specific": {},
      "negative_patterns": [],
      "code_triggers": {},
      "compound_patterns": [],
      "scoring_weights": {
        "regex_match": 0.8,
        "exact_match": 0.85
      }
    },
    {
      "group_name": "urgency_timeline_restrictions",
      "regex_patterns": [
        "(?i)(?:immediate|urgent|expedited)\\s*(?:.*)?(?:no\\s*time|insufficient\\s*time)\\s*(?:for\\s*)?(?:new\\s*)?source",
        "(?i)(?:critical|emergency)\\s*(?:requirement|need)\\s*(?:.*)?(?:existing|current)\\s*sources\\s*only",
        "(?i)(?:AOG|aircraft\\s*on\\s*ground)\\s*(?:.*)?approved\\s*sources",
        "(?i)(?:mission|operational)\\s*(?:critical|essential)\\s*(?:.*)?no\\s*(?:new\\s*)?sources",
        "(?i)(?:deployment|readiness)\\s*(?:requirement|deadline)\\s*(?:.*)?approved\\s*only",
        "(?i)time\\s*(?:constraint|sensitive)\\s*(?:.*)?existing\\s*sources"
      ],
      "exact_phrases": [
        "AOG requirement",
        "Aircraft on Ground",
        "mission critical requirement",
        "urgent requirement",
        "emergency procurement",
        "immediate need"
      ],
      "partial_triggers": [
        "AOG",
        "urgent",
        "emergency",
        "immediate"
      ],
      "context_patterns": [],
      "agency_specific": {},
      "negative_patterns": [],
      "code_triggers": {},
      "compound_patterns": [],
      "scoring_weights": {
        "regex_match": 0.85,
        "exact_match": 0.9
      }
    },
    {
      "group_name": "distributor_specific_restrictions",
      "regex_patterns": [
        "(?i)(?:dealer|distributor|reseller|supplier)\\s*(?:must|shall)\\s*(?:be\\s*)?(?:authorized|approved)",
        "(?i)authorized\\s*(?:dealer|distributor|reseller)\\s*(?:letter|certification|documentation)",
        "(?i)(?:proof|evidence|documentation)\\s*of\\s*(?:dealer|distributor)\\s*(?:authorization|approval)",
        "(?i)(?:manufacturer|OEM)\\s*(?:authorized|approved)\\s*(?:dealer|distributor)",
        "(?i)(?:valid|current)\\s*(?:dealer|distributor)\\s*(?:agreement|authorization)",
        "(?i)(?:dealer|distributor)\\s*(?:.*)?(?:technically\\s*)?unacceptable\\s*(?:unless|without)"
      ],
      "exact_phrases": [
        "authorized distributor letter required",
        "dealer authorization required",
        "distributor must be approved",
        "OEM authorized distributor",
        "manufacturer approved dealer"
      ],
      "partial_triggers": [
        "distributor letter",
        "dealer authorization",
        "authorized distributor"
      ],
      "context_patterns": [],
      "agency_specific": {},
      "negative_patterns": [],
      "code_triggers": {},
      "compound_patterns": [],
      "scoring_weights": {
        "regex_match": 0.85,
        "exact_match": 0.9
      }
    },
    {
      "group_name": "multi_language_variations",
      "regex_patterns": [
        "(?i)sourc[e\\s]*(?:approval|aproval|approvel|approvl|apprval|apprvl)",
        "(?i)(?:approval|aproval|approvel|approvl|apprval|apprvl)\\s*(?:of\\s*)?sourc[e\\s]*",
        "(?i)sourc[e\\s]*(?:qualification|qualif|qual|qualific)",
        "(?i)sourc[e\\s]*(?:verification|verif|verf|verify)",
        "(?i)sourc[e\\s]*(?:validation|valid|vldt|validate)",
        "(?i)sourc[e\\s]*(?:certification|cert|certif|certificate)"
      ],
      "exact_phrases": [],
      "partial_triggers": [],
      "context_patterns": [],
      "agency_specific": {},
      "negative_patterns": [],
      "code_triggers": {},
      "compound_patterns": [],
      "scoring_weights": {
        "regex_match": 0.8
      }
    },
    {
      "group_name": "conditional_logic_patterns",
      "regex_patterns": [
        "(?i)if\\s*(?:not\\s*)?(?:from\\s*)?approved\\s*sourc[e\\s]*(?:then\\s*)?(?:.*)?(?:reject|unaccept)",
        "(?i)unless\\s*(?:from\\s*)?approved\\s*sourc[e\\s]*(?:.*)?(?:reject|unaccept)",
        "(?i)only\\s*if\\s*(?:from\\s*)?approved\\s*sourc[e\\s]*",
        "(?i)must\\s*be\\s*(?:from\\s*)?(?:an\\s*)?approved\\s*sourc[e\\s]*(?:or|otherwise)",
        "(?i)when\\s*(?:not\\s*)?(?:from\\s*)?approved\\s*sourc[e\\s]*"
      ],
      "exact_phrases": [
        "if not from approved source",
        "unless from approved source",
        "only if approved source",
        "must be from approved source"
      ],
      "partial_triggers": [],
      "context_patterns": [],
      "agency_specific": {},
      "negative_patterns": [],
      "code_triggers": {},
      "compound_patterns": [],
      "scoring_weights": {
        "regex_match": 0.85,
        "exact_match": 0.9
      }
    },
    {
      "group_name": "reference_document_patterns",
      "regex_patterns": [
        "(?i)see\\s*(?:attachment|attach|att|atch)\\s*(?:.*)?sourc[e\\s]*approv",
        "(?i)refer\\s*to\\s*(?:attachment|section|para|paragraph)\\s*(?:.*)?sourc[e\\s]*approv",
        "(?i)(?:attachment|section|para)\\s*[A-Z0-9]+\\s*(?:.*)?sourc[e\\s]*approv",
        "(?i)(?:per|iaw|in\\s*accordance\\s*with)\\s*(?:.*)?sourc[e\\s]*approv",
        "(?i)as\\s*(?:stated|specified|defined)\\s*(?:in\\s*)?(?:.*)?sourc[e\\s]*approv"
      ],
      "exact_phrases": [
        "see attachment for source approval",
        "refer to section",
        "per attachment",
        "IAW source approval"
      ],
      "partial_triggers": [],
      "context_patterns": [],
      "agency_specific": {},
      "negative_patterns": [],
      "code_triggers": {},
      "compound_patterns": [],
      "scoring_weights": {
        "regex_match": 0.75
      }
    },
    {
      "group_name": "combined_amsc_amc_variations",
      "regex_patterns": [
        "(?i)AMC\\s*[:/\\-\\s]+\\s*[345]",
        "(?i)AMSC\\s*[:/\\-\\s]+\\s*[BCDHKLMNPQRSTUVY]",
        "(?i)AMC\\s*[345]\\s*[,/\\-\\s]+\\s*AMSC\\s*[BCDHKLMNPQRSTUVY]",
        "(?i)Acq\\.?\\s*Method\\s*[:/\\-\\s]+\\s*[345]",
        "(?i)Acq\\.?\\s*Method\\s*Suffix\\s*[:/\\-\\s]+\\s*[BCDHKLMNPQRSTUVY]",
        "(?i)Method\\s*Code\\s*[:/\\-\\s]+\\s*[345]",
        "(?i)Suffix\\s*Code\\s*[:/\\-\\s]+\\s*[BCDHKLMNPQRSTUVY]"
      ],
      "exact_phrases": [
        "AMC: 3",
        "AMC: 4",
        "AMC: 5",
        "AMSC: B",
        "AMSC: C",
        "AMSC: D"
      ],
      "partial_triggers": [],
      "context_patterns": [],
      "agency_specific": {},
      "negative_patterns": [],
      "code_triggers": {},
      "compound_patterns": [],
      "scoring_weights": {
        "regex_match": 0.85,
        "exact_match": 0.9
      }
    },
    {
      "group_name": "cage_code_format_variations",
      "regex_patterns": [
        "(?i)CAGE\\s*(?:Code\\s*)?[0-9A-Z]{5}",
        "(?i)CAGE\\s*#\\s*[0-9A-Z]{5}",
        "(?i)CAGE:\\s*[0-9A-Z]{5}",
        "(?i)\\[CAGE\\s*[0-9A-Z]{5}\\]",
        "(?i)\\(CAGE\\s*[0-9A-Z]{5}\\)",
        "(?i)Cage\\s*[0-9A-Z]{5}",
        "(?i)cage\\s*[0-9A-Z]{5}",
        "(?i)NCAGE\\s*[0-9A-Z]{5}",
        "(?i)NATO\\s*CAGE\\s*[0-9A-Z]{5}"
      ],
      "exact_phrases": [],
      "partial_triggers": [
        "CAGE",
        "cage",
        "NCAGE"
      ],
      "context_patterns": [],
      "agency_specific": {},
      "negative_patterns": [],
      "code_triggers": {},
      "compound_patterns": [],
      "scoring_weights": {
        "regex_match": 0.75
      }
    },
    {
      "group_name": "weapon_system_variations",
      "regex_patterns": [
        "(?i)(?:F|f)[-\\s]?(?:15|16|18|22|35)[A-Z]?\\s*(?:.*)?approv",
        "(?i)(?:A|a)[-\\s]?10[A-Z]?\\s*(?:.*)?approv",
        "(?i)(?:B|b)[-\\s]?(?:1|2|52)[A-Z]?\\s*(?:.*)?approv",
        "(?i)(?:C|c)[-\\s]?(?:5|17|130)[A-Z]?\\s*(?:.*)?approv",
        "(?i)(?:UH|uh|AH|ah|CH|ch|MH|mh)[-\\s]?(?:1|47|53|60|64)[A-Z]?\\s*(?:.*)?approv",
        "(?i)(?:V|v)[-\\s]?22\\s*(?:osprey)?\\s*(?:.*)?approv",
        "(?i)(?:KC|kc)[-\\s]?(?:10|46|135)[A-Z]?\\s*(?:.*)?approv",
        "(?i)(?:E|e)[-\\s]?(?:2|3|4|6|8)[A-Z]?\\s*(?:.*)?approv",
        "(?i)(?:P|p)[-\\s]?(?:3|8)[A-Z]?\\s*(?:.*)?approv",
        "(?i)(?:T|t)[-\\s]?(?:6|38|45)[A-Z]?\\s*(?:.*)?approv"
      ],
      "exact_phrases": [],
      "partial_triggers": [],
      "context_patterns": [],
      "agency_specific": {},
      "negative_patterns": [],
      "code_triggers": {},
      "compound_patterns": [],
      "scoring_weights": {
        "regex_match": 0.7
      }
    },
    {
      "group_name": "quality_system_patterns",
      "regex_patterns": [
        "(?i)AS9100[A-Z]?\\s*(?:certified|certification|required)",
        "(?i)AS9120[A-Z]?\\s*(?:certified|certification|required)",
        "(?i)ISO\\s*9001\\s*(?:.*)?sourc[e\\s]*approv",
        "(?i)NADCAP\\s*(?:certified|certification|accredited)",
        "(?i)MIL[-\\s]?(?:STD|SPEC|PRF)[-\\s]?[0-9]+\\s*(?:.*)?approv",
        "(?i)MIL[-\\s]?Q[-\\s]?9858[A]?\\s*(?:.*)?approv",
        "(?i)MIL[-\\s]?I[-\\s]?45208[A]?\\s*(?:.*)?approv"
      ],
      "exact_phrases": [
        "AS9100 certified",
        "AS9120 certified",
        "NADCAP accredited",
        "MIL-STD",
        "MIL-SPEC"
      ],
      "partial_triggers": [],
      "context_patterns": [],
      "agency_specific": {},
      "negative_patterns": [],
      "code_triggers": {},
      "compound_patterns": [],
      "scoring_weights": {
        "regex_match": 0.75,
        "exact_match": 0.8
      }
    },
    {
      "group_name": "negation_exception_patterns",
      "regex_patterns": [
        "(?i)except\\s*(?:for\\s*)?sourc[e\\s]*approv",
        "(?i)other\\s*than\\s*sourc[e\\s]*approv",
        "(?i)aside\\s*from\\s*sourc[e\\s]*approv",
        "(?i)excluding\\s*sourc[e\\s]*approv",
        "(?i)without\\s*regard\\s*to\\s*sourc[e\\s]*approv",
        "(?i)regardless\\s*of\\s*sourc[e\\s]*approv"
      ],
      "exact_phrases": [],
      "partial_triggers": [],
      "context_patterns": [],
      "agency_specific": {},
      "negative_patterns": [],
      "code_triggers": {},
      "compound_patterns": [],
      "scoring_weights": {
        "regex_match": 0.6
      }
    },
    {
      "group_name": "complex_nested_patterns",
      "regex_patterns": [
        "(?i)(?:if|when|unless|until)\\s*(?:.*)?sourc[e\\s]*approv[a-z]*\\s*(?:.*)?(?:then|shall|must|will)",
        "(?i)(?:prior\\s*to|before|in\\s*advance\\s*of)\\s*(?:.*)?(?:award|contract)\\s*(?:.*)?sourc[e\\s]*approv",
        "(?i)sourc[e\\s]*approv[a-z]*\\s*(?:.*)?(?:prior\\s*to|before|in\\s*advance\\s*of)\\s*(?:.*)?(?:award|contract)",
        "(?i)(?:for|regarding|concerning)\\s*(?:.*)?(?:CSI|CAI|critical)\\s*(?:.*)?sourc[e\\s]*approv"
      ],
      "exact_phrases": [],
      "partial_triggers": [],
      "context_patterns": [],
      "agency_specific": {},
      "negative_patterns": [],
      "code_triggers": {},
      "compound_patterns": [],
      "scoring_weights": {
        "regex_match": 0.8
      }
    },
    {
      "group_name": "solicitation_section_headers",
      "regex_patterns": [
        "(?i)^\\s*(?:section|sect|sec)\\s*[A-Z0-9]+\\s*[-:]?\\s*sourc[e\\s]*approv",
        "(?i)^\\s*(?:paragraph|para|par)\\s*[A-Z0-9]+\\s*[-:]?\\s*sourc[e\\s]*approv",
        "(?i)^\\s*(?:clause|provision)\\s*[A-Z0-9]+\\s*[-:]?\\s*sourc[e\\s]*approv",
        "(?i)^\\s*[A-Z0-9]+\\.\\s*sourc[e\\s]*approv",
        "(?i)^\\s*\\([A-Z0-9]+\\)\\s*sourc[e\\s]*approv"
      ],
      "exact_phrases": [],
      "partial_triggers": [],
      "context_patterns": [],
      "agency_specific": {},
      "negative_patterns": [],
      "code_triggers": {},
      "compound_patterns": [],
      "scoring_weights": {
        "regex_match": 0.85
      }
    },
    {
      "group_name": "final_catch_all_patterns",
      "regex_patterns": [
        "(?i).{0,10}sourc.{0,3}appr.{0,10}req.{0,10}",
        "(?i).{0,10}eng.{0,5}sourc.{0,10}",
        "(?i).{0,10}approv.{0,3}sourc.{0,10}",
        "(?i).{0,10}SAR.{0,10}req.{0,10}",
        "(?i).{0,10}sourc.{0,3}control.{0,10}",
        "(?i).{0,10}technical.{0,3}unaccept.{0,10}",
        "(?i).{0,10}CSI.{0,10}approv.{0,10}",
        "(?i).{0,10}flight.{0,3}critical.{0,10}"
      ],
      "exact_phrases": [],
      "partial_triggers": [],
      "context_patterns": [],
      "agency_specific": {},
      "negative_patterns": [],
      "code_triggers": {},
      "compound_patterns": [],
      "scoring_weights": {
        "regex_match": 0.5
      }
    }
  ]
}