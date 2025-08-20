{
  "category": "sar_patterns",
  "pattern_groups": [
    {
      "group_name": "explicit_sar_language",
      "regex_patterns": [
        "sourc[e|es?]?\\s*approv[a|e][l|d]\\s*requir[e|ed|ing|ement]",
        "government\\s*sourc[e|es?]?\\s*approv[a|e][l|d]\\s*requir",
        "engineering\\s*sourc[e|es?]?\\s*approv[a|e][l|d]",
        "sourc[e|es?]?\\s*qualificat[i|e]on\\s*requir",
        "requir[e|es|ed|ing]\\s*[a-z\\s]{0,20}?sourc[e|es?]?\\s*approv",
        "militar[y|ies]\\s*sourc[e|es?]?\\s*approv",
        "sourc[e|es?]?\\s*approv[a|e][l|d]\\s*prior\\s*to\\s*award",
        "must\\s*be\\s*[a-z\\s]{0,30}?approv[e|ed]\\s*sourc",
        "approv[e|ed]\\s*sourc[e|es?]?\\s*prior\\s*to"
      ],
      "exact_phrases": [
        "source approval required",
        "Government source approval required",
        "engineering source approval required",
        "Source approval required prior to award",
        "military source approval required",
        "requires engineering source approval",
        "source qualification required",
        "ESA source approval required",
        "AMCOM source approval required",
        "NAVAIR source approval required"
      ],
      "partial_triggers": [
        "source approv",
        "sourc approv",
        "src approval",
        "source aproval",
        "source approva",
        "souce approval",
        "soruce approval",
        "source apprval"
      ],
      "context_patterns": [
        {
          "before": ["requires", "must have", "need", "mandatory"],
          "trigger": "source approval",
          "after": ["prior", "before", "for award", "to bid"]
        }
      ],
      "agency_specific": {
        "DLA": [
          "DLA source approval required",
          "Defense Logistics Agency source approval",
          "DLA Aviation source approval"
        ],
        "NAVSUP": [
          "WSS TERM H Z 07 GOVERNMENT SOURCE APPROVAL REQUIRED PRIOR TO AWARD",
          "NAVSUP WSS source approval",
          "Naval source approval required"
        ],
        "NAVAIR": [
          "NAVAIR engineering source approval",
          "Naval Air Systems Command approval"
        ],
        "AMCOM": [
          "AMCOM approved source",
          "Army Aviation and Missile Command source approval",
          "All prospective manufacturers are required to be an AMCOM approved source"
        ],
        "AFMC": [
          "Air Force ESA approval",
          "AFMC source approval",
          "Tinker AFB source approval"
        ]
      },
      "negative_patterns": [
        "FAA source approval",
        "FAA approved",
        "ISO source approval",
        "commercial source approval",
        "civilian source approval",
        "no source approval required",
        "source approval not required",
        "source approval waived"
      ],
      "code_triggers": {
        "AMC_codes": ["AMC 3", "AMC 4", "AMC 5", "AMC3", "AMC4", "AMC5"],
        "AMSC_codes": ["AMSC C", "AMSC D", "AMSC P", "AMSC R", "AMSC B", "AMSC H", "AMSC K", "AMSC L", "AMSC M", "AMSC N", "AMSC Q", "AMSC S", "AMSC T", "AMSC U", "AMSC V", "AMSC Y"]
      },
      "compound_patterns": [
        ["military", "AND", "source approval"],
        ["AMC", "AND", "AMSC"],
        ["engineering", "AND", "approval", "AND", "required"],
        ["source", "AND", "qualification", "AND", "prior"]
      ],
      "scoring_weights": {
        "explicit_match": 10,
        "regex_match": 8,
        "partial_match": 5,
        "context_match": 7,
        "code_match": 9,
        "compound_match": 8
      }
    },
    {
      "group_name": "approved_source_list",
      "regex_patterns": [
        "approv[e|ed]\\s*sourc[e|es?]?\\s*list",
        "ASL\\s*\\(?approv[e|ed]\\s*sourc",
        "qualifi[e|ed]\\s*suppli[e|ers?]?\\s*list",
        "QPL\\s*\\(?qualifi[e|ed]\\s*product",
        "QML\\s*\\(?qualifi[e|ed]\\s*manufactur",
        "qualifi[e|ed]\\s*bidders?\\s*list",
        "pre[\\-\\s]?approv[e|ed]\\s*vendor",
        "pre[\\-\\s]?qualifi[e|ed]\\s*suppli"
      ],
      "exact_phrases": [
        "approved source list",
        "Approved Source List",
        "qualified suppliers list",
        "Qualified Products List",
        "QPL",
        "QML",
        "qualified manufacturers list",
        "approved manufacturers list",
        "pre-approved vendors list",
        "service-managed ASL"
      ],
      "partial_triggers": [
        "approved sourc",
        "aproved source",
        "approved src",
        "qualified suppl",
        "qualifed supplier",
        "QPL list",
        "QML list"
      ],
      "context_patterns": [
        {
          "before": ["must be on", "listed on", "included in", "part of"],
          "trigger": "approved source",
          "after": ["list", "listing", "database", "system"]
        }
      ],
      "agency_specific": {
        "DLA": ["DLA ASL", "DLA-managed approved source list"],
        "Navy": ["Navy ASL", "NAVSUP approved source list"],
        "Army": ["Army ASL", "AMCOM-controlled ASL"],
        "AirForce": ["Air Force QPL", "AFMC qualified products list"]
      },
      "negative_patterns": [
        "not on approved source list",
        "removed from ASL",
        "seeking additions to ASL",
        "open to new sources"
      ],
      "code_triggers": {},
      "compound_patterns": [
        ["qualified", "OR", "approved", "AND", "list"],
        ["QPL", "OR", "QML", "OR", "ASL"]
      ],
      "scoring_weights": {
        "explicit_match": 9,
        "regex_match": 7,
        "partial_match": 4,
        "context_match": 6
      }
    },
    {
      "group_name": "military_specification_sar",
      "regex_patterns": [
        "militar[y|ies]\\s*spec[s|ification|ified]",
        "MIL[\\-\\s]?SPEC",
        "MIL[\\-\\s]?STD",
        "militar[y|ies]\\s*standard",
        "defense\\s*spec[s|ification]",
        "DOD[\\-\\s]?spec",
        "weapon\\s*system\\s*spec"
      ],
      "exact_phrases": [
        "military specification",
        "military spec",
        "MIL-SPEC",
        "MIL-STD",
        "military standard",
        "defense specification",
        "DOD specification",
        "weapon system specification"
      ],
      "partial_triggers": [
        "mil spec",
        "milspec",
        "mil-spec",
        "military sp",
        "mil std"
      ],
      "context_patterns": [
        {
          "before": ["per", "according to", "IAW", "complies with"],
          "trigger": "military",
          "after": ["specification", "spec", "standard"]
        }
      ],
      "agency_specific": {},
      "negative_patterns": [
        "commercial specification",
        "FAA specification",
        "civilian specification",
        "industry standard"
      ],
      "code_triggers": {},
      "compound_patterns": [
        ["military", "AND", "specification", "AND", "required"],
        ["MIL", "AND", "SPEC", "AND", "compliance"]
      ],
      "scoring_weights": {
        "explicit_match": 7,
        "regex_match": 6,
        "context_match": 5
      }
    },
    {
      "group_name": "technical_approval_authority",
      "regex_patterns": [
        "design\\s*control\\s*activit[y|ies]",
        "DCA\\s*approv",
        "engineer[ing]?\\s*support\\s*activit[y|ies]",
        "ESA\\s*approv",
        "technical\\s*authorit[y|ies]",
        "configuration\\s*control\\s*authorit",
        "single\\s*manager\\s*for\\s*[a-z\\s]*weapon"
      ],
      "exact_phrases": [
        "design control activity",
        "DCA approval required",
        "engineering support activity",
        "ESA approval",
        "technical authority approval",
        "configuration control authority",
        "Designated Air Force Single Manager",
        "weapon system manager approval"
      ],
      "partial_triggers": [
        "DCA approv",
        "ESA approv",
        "tech authority",
        "config control"
      ],
      "context_patterns": [
        {
          "before": ["requires", "must have", "approved by"],
          "trigger": "DCA",
          "after": ["approval", "authorization", "concurrence"]
        }
      ],
      "agency_specific": {
        "AirForce": ["Air Force ESA", "AFMC technical authority"],
        "Navy": ["NAVAIR technical authority", "NAVSEA engineering"],
        "Army": ["AMCOM technical authority", "TACOM engineering"]
      },
      "negative_patterns": [],
      "code_triggers": {},
      "compound_patterns": [
        ["design", "AND", "control", "AND", "activity"],
        ["engineering", "AND", "support", "AND", "activity"]
      ],
      "scoring_weights": {
        "explicit_match": 8,
        "regex_match": 7,
        "context_match": 6
      }
    },
    {
      "group_name": "cage_code_restrictions",
      "regex_patterns": [
        "CAGE\\s*code[s]?\\s*[0-9A-Z]{5}",
        "only\\s*CAGE\\s*[0-9A-Z]{5}",
        "restricted\\s*to\\s*CAGE",
        "limited\\s*to\\s*CAGE",
        "approved\\s*CAGE[s]?\\s*code"
      ],
      "exact_phrases": [
        "restricted to CAGE",
        "limited to CAGE code",
        "only approved CAGE",
        "CAGE codes listed",
        "approved CAGE codes only"
      ],
      "partial_triggers": [
        "CAGE code",
        "CAGE only",
        "restricted CAGE"
      ],
      "context_patterns": [
        {
          "before": ["limited to", "restricted to", "only"],
          "trigger": "CAGE",
          "after": ["code", "codes", "listed below"]
        }
      ],
      "agency_specific": {},
      "negative_patterns": [
        "any CAGE code",
        "all CAGE codes acceptable",
        "CAGE code not restricted"
      ],
      "code_triggers": {
        "cage_pattern": "[0-9A-Z]{5}"
      },
      "compound_patterns": [
        ["CAGE", "AND", "restricted"],
        ["CAGE", "AND", "only", "AND", "approved"]
      ],
      "scoring_weights": {
        "explicit_match": 8,
        "cage_code_present": 7
      }
    },
    {
      "group_name": "prohibitive_language",
      "regex_patterns": [
        "award\\s*cannot\\s*be\\s*delay[ed]?",
        "no\\s*time\\s*for\\s*[a-z\\s]*approv",
        "immediate\\s*award\\s*requir",
        "urgent\\s*requir[e|ement]",
        "cannot\\s*wait\\s*for\\s*approv",
        "previously\\s*approv[e|ed]\\s*sourc[e|es]?\\s*only"
      ],
      "exact_phrases": [
        "award cannot be delayed",
        "no time for source approval",
        "immediate award required",
        "urgent requirement",
        "cannot wait for approval",
        "previously approved sources only",
        "existing approved sources only"
      ],
      "partial_triggers": [
        "cannot delay",
        "no time for",
        "urgent requir",
        "immediate award"
      ],
      "context_patterns": [
        {
          "before": ["award", "contract", "delivery"],
          "trigger": "cannot be delayed",
          "after": ["for approval", "for SAR", "for qualification"]
        }
      ],
      "agency_specific": {},
      "negative_patterns": [
        "can be delayed",
        "time available for approval",
        "SAR submissions welcome"
      ],
      "code_triggers": {},
      "compound_patterns": [
        ["urgent", "AND", "no time", "AND", "approval"],
        ["award", "AND", "cannot", "AND", "delay"]
      ],
      "scoring_weights": {
        "explicit_match": 9,
        "urgency_indicator": 8
      }
    },
    {
      "group_name": "specific_platform_sar",
      "regex_patterns": [
        "F[\\-\\s]?[0-9]{1,3}[A-Z]?\\s*sourc[e|es]?\\s*approv",
        "C[\\-\\s]?[0-9]{1,3}[A-Z]?\\s*sourc[e|es]?\\s*approv",
        "AH[\\-\\s]?[0-9]{1,3}[A-Z]?\\s*sourc[e|es]?\\s*approv",
        "UH[\\-\\s]?[0-9]{1,3}[A-Z]?\\s*sourc[e|es]?\\s*approv",
        "Apache\\s*sourc[e|es]?\\s*approv",
        "Blackhawk\\s*sourc[e|es]?\\s*approv"
      ],
      "exact_phrases": [
        "F-15 source approval",
        "F-16 source approval", 
        "F-22 source approval",
        "F-35 source approval",
        "C-17 source approval",
        "C-130 source approval",
        "AH-64 Apache source approval",
        "UH-60 Blackhawk source approval"
      ],
      "partial_triggers": [],
      "context_patterns": [
        {
          "before": ["for", "requires"],
          "trigger": "F-",
          "after": ["source approval", "approved sources"]
        }
      ],
      "agency_specific": {},
      "negative_patterns": [
        "Boeing 737",
        "KC-46",
        "commercial aircraft"
      ],
      "code_triggers": {},
      "compound_patterns": [
        ["military aircraft", "AND", "source approval"]
      ],
      "scoring_weights": {
        "platform_match": 9
      }
    }
  ]
}