

# **Framework for an Automated Decision Filter: Military Source Approval Requirements for Aviation Spares Distribution**

## **Section 1: The Source Approval Mandate: Foundational Analysis**

The United States government's procurement system for military aviation components is fundamentally shaped by stringent requirements for source approval. This system is not arbitrary; it is a deliberate and deeply entrenched framework designed to mitigate catastrophic risk and ensure the operational readiness of critical defense assets. For an aviation aftermarket parts distributor such as Source One Spares (SOS), understanding the bedrock principles of this system is paramount to developing an effective automated filter for contracting opportunities. The logic for accepting or rejecting a solicitation must be grounded in the government's core motivations. These motivations consistently trace back to two distinct but often overlapping pillars: the doctrine of airworthiness and safety, and the challenge of incomplete or proprietary technical data. The presence of language related to either of these pillars in a solicitation is a powerful indicator that significant restrictions on competition are in place.

### **1.1 The Doctrine of Airworthiness and Safety**

The highest priority in military aviation procurement is ensuring the safety of personnel and the successful execution of missions. This priority is codified through the designation of certain components as being essential to the function and safety of a weapon system. These designations are not mere classifications; they are triggers that fundamentally alter procurement rules, shifting them from open competition to a highly restricted environment.

Solicitations frequently contain explicit terminology identifying these high-risk components. The most common designations are **Flight Critical Items**, **Critical Safety Items (CSI)**, and **Critical Application Items (CAI)**.1 An item is designated as a CSI or CAI if its failure could lead to a catastrophic event, such as the loss of an aircraft or serious injury or death to the crew.3 For example, a solicitation may state that an item requires government source approval specifically because "the item is flight critical" 1 or because it is a designated CSI.5

This system establishes a clear and rigid chain of authority. The Department of Defense (DoD) delegates the responsibility for identifying these critical items and qualifying potential sources of supply to the Engineering Support Activity (ESA) within each military service branch (e.g., Army, Navy, Air Force).4 This is a crucial structural element of the procurement landscape. The procuring agency, such as the Defense Logistics Agency (DLA), is typically not the engineering authority. Therefore, DLA does not have the authority to approve new sources for critical items; it is bound to procure them exclusively from the Approved Source List (ASL) maintained by the responsible service's ESA.7 This separation of duties explains why a contractor cannot simply prove its capability to the DLA buyer; the qualification must be granted by a separate, technical branch of the military. For the purposes of an automated filter, the appearance of terms like "CSI," "CAI," or "flight critical" must be treated as a primary trigger for a "NO-GO" decision, pending the presence of specific, overriding exceptions.

### **1.2 The Technical Data Package (TDP) Problem**

The second pillar supporting source restrictions is the availability and completeness of the Technical Data Package (TDP). A TDP contains all the drawings, specifications, manufacturing processes, and materials information necessary to produce a part that is identical in form, fit, and function to the original. When the government possesses a complete and unrestricted TDP, it can conduct a full and open competition, allowing any capable manufacturer to produce the item.9 However, this is often not the case.

Many solicitations are restricted because the government lacks a sufficient TDP. This can be for several reasons: the data may never have been purchased from the Original Equipment Manufacturer (OEM), the rights to use the data for competitive procurement may be restricted, or the cost to acquire the data may be deemed uneconomical.11 Solicitations will explicitly state this reality with phrases such as "Drawings and technical data are not available" 13 or "the technical data available has not been determined adequate to support acquisition via full and open competition".1

For a distributor like SOS, the absence of a TDP is a formidable barrier. SOS relies on a competitive marketplace of manufacturers to source its products. If the government itself does not have the necessary data to enable a new company to manufacture the part, it has no choice but to restrict the procurement to the entity that holds that proprietary knowledge—typically the OEM or a source formally licensed by the OEM.14 This situation is a definitive "NO-GO" for any supplier not already on the short list of approved sources. The filter's logic must be programmed to recognize any mention of unavailable, inadequate, or proprietary technical data as a strong trigger for rejection. The two pillars of restriction—item criticality and data unavailability—are frequently cited together. A solicitation might justify its restrictions by stating an item is "flight critical

**and/or** the technical data available has not been determined adequate".1 The use of "and/or" is significant, as it indicates that either condition alone is sufficient to enforce source approval requirements. One opportunity may be restricted purely due to its criticality, even with a full TDP, while another may be restricted purely due to a lack of data, even if the part is non-critical. The automated filter must be designed to act on either trigger independently; it does not need to find both to classify a solicitation as restricted.

## **Section 2: Decoding Solicitation Language: Primary Trigger Phrases (The "Hard NO-GO")**

While the underlying principles of safety and data rights explain *why* procurements are restricted, the automated filter must operate on the specific language used in the solicitations themselves. Government contracting documents contain highly standardized phrases that serve as clear, unambiguous signals about the competitive landscape of an opportunity. These phrases function as "Hard NO-GO" triggers, indicating that unless a specific and explicit exception is also present, the solicitation is closed to any company not already on the approved source list.

### **2.1 Explicit Requirement for Prior Approval**

The most direct and common set of trigger phrases are those that explicitly state that source approval is a prerequisite for contract award. This language makes it clear that the qualification process is separate from and must be completed before the procurement action. For a distributor like SOS, if they or their manufacturing partner are not already approved for the specific National Stock Number (NSN) in question, these phrases signal that the opportunity is not viable.

Key trigger phrases in this category include:

* "Source approval required prior to award" 1  
* "requires Government source approval" 13  
* "requires engineering source approval" 15  
* "This part requires engineering source approval by the design control activity" 17

The consistency of this language across different buying commands (Navy, DLA, etc.) makes it a reliable input for the filter's logic. It indicates that the procuring officer has no discretion to consider offers from unapproved sources.

### **2.2 Solicitation Limited to Existing Sources**

A second category of phrases goes a step further by stating that the government has already limited the solicitation to the pre-vetted list of suppliers. This language reveals a procurement process that is effectively "pre-selected," where the competitive field was determined before the solicitation was ever made public. These are among the most definitive "Hard NO-GO" triggers.

Key trigger phrases indicating a pre-selected competition include:

* "Only the source(s) previously approved by the Government for this item have been solicited." 1  
* "Quotes/proposals received from sources which are not Government-approved sources of supply will be deemed technically unacceptable" 13  
* "This is a source controlled drawing item. Approved sources are \[CAGE Code\]\[Part Number\]..." 18  
* "Review the NSN and the approved source list below." 20

This language confirms that even if a solicitation appears on a public portal like SAM.gov, it may be a targeted release intended only for the named or previously identified sources. Any quote submitted by an unapproved source will be summarily rejected as non-responsive or technically unacceptable.13 For a distributor, this means that even possessing the exact part from the OEM is insufficient if SOS or that OEM is not on the specific ASL for that NSN. The critical factor is not possessing the item, but possessing the

*approved status*.

### **2.3 Prohibitive Timelines for New Source Approval**

The final category of "Hard NO-GO" language addresses the practical impossibility of becoming a new source within the timeframe of a specific procurement. The government recognizes that the Source Approval Request (SAR) process is lengthy and resource-intensive. To avoid delays in acquiring needed parts, solicitations for urgent requirements will often include language that preemptively dismisses any attempt by a new source to qualify.

The most potent trigger phrase in this category is:

* "The time required for approval of a new source is normally such that award cannot be delayed pending approval of a new source." 1

This single sentence is a clear instruction to the market: do not submit a SAR package for this particular buy, as it will not be considered. The procurement timeline is fixed and will not accommodate the 60- to 180-day (or longer) evaluation period required for a new source to be approved.21 When the filter detects this phrase, it should immediately classify the opportunity as a "NO-GO," as there is no path to participation for an unapproved source in that instance.

## **Section 3: The Gatekeepers: Agency-Specific Terminology and Approved Source Lists (ASLs)**

A sophisticated automated filter must recognize that the Department of Defense is not a monolithic entity. The responsibility for source approval is decentralized, with each military service maintaining its own engineering authorities and, consequently, its own Approved Source Lists. While the DLA is the largest buyer of spare parts, it often acts as a procurement agent for the services, which retain the ultimate technical authority. Understanding this structure and the specific terminology used by each branch is essential for correctly interpreting a solicitation's restrictions.

### **3.1 The Defense Logistics Agency (DLA): The Central Purchaser**

The DLA, through its major subordinate commands like DLA Aviation and DLA Land and Maritime, is the primary purchasing body for a vast number of NSNs.10 However, a critical dynamic to understand is that for many of the parts it buys, particularly critical ones, the DLA is not the engineering authority. A DLA solicitation for an F-16 part, for example, is governed by the source approval decisions of the U.S. Air Force.7 Similarly, a DLA solicitation for an Apache helicopter part is controlled by the U.S. Army's approval authority.8

The DLA itself acknowledges this structure, with solicitations stating "Engineering source approval required" 16 or noting that DLA must use the service-managed ASL.4 The filter's logic must, therefore, be designed to parse DLA solicitations for keywords indicating the end-user service (e.g., "Air Force," "Army," "Navy," or a specific weapon system like "F-16" or "UH-60"). This allows the filter to apply the correct set of agency-specific rules and terminology, preventing the misinterpretation of who the ultimate gatekeeper is.

### **3.2 The U.S. Navy: NAVSUP and NAVAIR**

The Navy's aviation procurement is primarily managed by two key commands: the Naval Supply Systems Command (NAVSUP) and the Naval Air Systems Command (NAVAIR).1 NAVSUP, and specifically its Weapon Systems Support (WSS) division, typically handles the contracting and logistics, including the management of the SAR process.21 However, the technical authority for the aircraft and its components—including configuration management and the approval of any engineering changes or variances—resides with NAVAIR.1

Navy solicitations often use specific boilerplate language, such as "WSS TERM H Z 07 GOVERNMENT SOURCE APPROVAL REQUIRED PRIOR TO AWARD".25 The reference to these "Term Local Text" codes is a unique feature of NAVSUP solicitations that the filter should be programmed to recognize as a definitive source approval requirement.

### **3.3 The U.S. Air Force: AFMC and Tinker AFB**

The U.S. Air Force's engineering authority for aviation components is its Engineering Support Activity (ESA), which falls under the Air Force Materiel Command (AFMC).5 For certain systems, this authority is further delegated to a "Designated Air Force Single Manager for a Weapon System".5 The Air Force also publishes its own detailed qualification requirement documents, such as RQR-PSD-1 for propulsion items managed at Tinker Air Force Base, which outlines the specific technical requirements a potential new source must meet.3 Language in a solicitation referring to the "Air Force ESA" or a specific AFMC center as the approval authority is a clear indicator of a restricted procurement.

### **3.4 The U.S. Army: AMCOM and TACOM**

For Army aviation, the key entity is the U.S. Army Aviation and Missile Command (AMCOM).5 Court documents and solicitations make it clear that AMCOM is the "sole authority to determine all approved sources" for the parts it manages, such as spares for the Apache helicopter.8 Solicitations for these items will often state that "All prospective manufacturers...are required to be an AMCOM approved source".8

A crucial lesson from AMCOM's management is the perishable nature of "approved" status. A company can be an approved source for years, having delivered hundreds of parts, only to be removed from the ASL when the government updates the governing TDP.8 In one documented case, a company named Rotair was an approved source for an Apache assembly since 2011, but was no longer listed on the ASL for a 2022 solicitation because the TDP had been updated earlier that year without including them.26 The DLA contracting officer correctly deferred to the AMCOM-controlled TDP, rejecting the company's bid. This highlights a critical business process requirement for SOS: it is not enough to know that a supplier

*was* approved. Verification of *current* approval status at the time of a bid is essential. While the filter cannot perform this verification, its logic underscores the need for SOS to maintain a dynamic internal system for tracking supplier qualifications.

## **Section 4: The Code Breaker's Guide: Acquisition Method & Suffix Codes (AMC/AMSC)**

Beyond the free-text language of a solicitation, the most reliable and machine-readable indicators of procurement restrictions are the Acquisition Method Code (AMC) and Acquisition Method Suffix Code (AMSC). This two-character code provides a concise and structured summary of an item's competitive status and the reasoning behind it. For an automated filter, these codes are the ideal input for making rapid and accurate GO/NO-GO decisions.

### **4.1 Understanding the Codes**

The AMC/AMSC system is used across the DoD to provide standardized guidance to contracting officers.27

* **Acquisition Method Code (AMC):** This is a single digit from 0 to 5 that describes *who* is eligible to supply the part. For example, AMC 1 or 2 indicates a competitive procurement, while AMC 3, 4, or 5 indicates a restricted procurement limited to the manufacturer or a specific prime contractor.28  
* **Acquisition Method Suffix Code (AMSC):** This is a single letter (A through Y) that provides the engineering or technical *reason* for the AMC restriction. It typically relates to the status of the TDP, data rights, or the need for special qualifications.12

A solicitation will present this as a two-part code, such as "AMC 1 / AMSC G" or "AMC 3 / AMSC C".17 The combination of the two provides a complete picture of the procurement landscape for that NSN.

### **4.2 The AMC/AMSC "NO-GO" Matrix for Distributors**

For SOS, as a distributor, the implication of an AMC/AMSC code is nuanced. A code that is a "NO-GO" for a direct bid from SOS might still represent an opportunity to supply the part if sourced from an approved manufacturer. The following matrix is designed to translate these codes into clear, actionable rules for the automated filter, tailored specifically to the distributor business model. The filter should be programmed to parse solicitations for these codes and apply the corresponding rule.

| Code (AMC/AMSC) | Official Definition | Implication for SOS (as a Distributor) | Filter Rule |
| :---- | :---- | :---- | :---- |
| **1/G or 2/G** | Competitive acquisition; Government has unlimited rights to the complete technical data package.12 | **Ideal Scenario.** This is a fully competitive procurement. SOS can source the part from any capable manufacturer that can produce to the government-provided TDP. | **GO** |
| **1/T or 2/T** | Competitive acquisition; but the item is subject to a Qualified Products List (QPL).27 | **Conditional GO.** SOS can only participate if its intended manufacturing source is already on the QPL for that item at the time of award. | **FLAG FOR REVIEW.** System must check internal supplier data to verify the manufacturer is on the specified QPL. If yes, GO. If no, NO-GO. |
| **3/C or 4/C** | Acquire directly from the actual manufacturer only (AMC 3/4); requires engineering source approval by the design control activity (AMSC C).12 | **Distributor Opportunity.** SOS cannot be the prime awardee. The part must be acquired from a specific, pre-approved manufacturer. SOS can only participate if they are an authorized distributor for that *exact* approved manufacturer and can provide the required documentation. | **FLAG FOR REVIEW.** System must parse the solicitation for the CAGE code(s) of the approved manufacturer(s) and check if SOS is an authorized distributor. If yes, GO. If no, NO-GO. |
| **3/D or 4/D** | Acquire directly from the actual manufacturer only (AMC 3/4); the data needed to acquire this part competitively is not available and cannot be obtained economically (AMSC D).12 | **Highly Restricted.** Similar to 3/C, but the restriction is due to a lack of data. SOS can only participate as an authorized distributor for the named, approved manufacturer who possesses the proprietary data. | **FLAG FOR REVIEW.** System must parse the solicitation for the CAGE code(s) of the approved manufacturer(s) and check if SOS is an authorized distributor. If yes, GO. If no, NO-GO. |
| **5/D** | Acquire directly from a sole source prime contractor which is not the actual manufacturer (AMC 5); data is not available (AMSC D).12 | **Subcontracting Opportunity Only.** This is a "sole source" procurement directed to a specific prime contractor. SOS cannot bid directly. The only potential path to participation is as a subcontractor to the named prime. | **NO-GO (Direct Bid) / FLAG (Subcontracting).** The system should parse the solicitation for the Prime Contractor's name and CAGE code and flag it for the business development team to explore a subcontracting relationship. |
| **Any AMC with Suffix B** | The part must be acquired from a manufacturing source specified on a source control drawing.12 | **Highly Restricted.** This is a "source controlled" item. SOS can only participate if it is an authorized distributor for one of the specific sources listed on the drawing. | **FLAG FOR REVIEW.** System must parse the solicitation for the approved CAGE code(s) and check if SOS is an authorized distributor. If yes, GO. If no, NO-GO. |

## **Section 5: Identifying Opportunity: Exception Phrases and Pathways to Approval**

A filter that only identifies "NO-GO" conditions is only half-built. To provide a true competitive advantage, the system must also be able to identify the exceptions and pathways that can transform a seemingly restricted opportunity into a viable one. The government, particularly the DLA, is often actively seeking to increase competition and break sole-source dependencies to reduce costs.10 Language indicating this intent can override the restrictive triggers detailed in previous sections. These opportunities fall into two categories: tactical (can be bid now) and strategic (require investment to bid in the future).

### **5.1 Explicit Calls for New Sources**

The most powerful exception is an explicit invitation from the government for new suppliers to come forward. This language signals that the agency is conducting market research and is willing to consider new sources, even for items that are currently restricted.

Key exception phrases include:

* "Please provide any sources that may be able to manufacture this item." 20  
* "The government is so interested in finding more suppliers for this item that they are making samples available for companies to reverse engineer." 10  
* "DLA looking for competition for..." 10  
* "If you wish to be evaluated for addition to the approved source list..." 32

When a solicitation is identified as a "Sources Sought" notice, it serves the same purpose.13 These are not typically requests for quotes to fulfill an immediate need, but rather requests for information to gauge market capability for future procurements. The presence of any of these phrases should cause the filter to override a "NO-GO" trigger and flag the opportunity for strategic review.

### **5.2 The Source Approval Request (SAR) Pathway**

The formal mechanism for a new manufacturer to become an approved source is the Source Approval Request (SAR).34 A SAR is a comprehensive package of technical data submitted by a prospective supplier to demonstrate their ability to produce a part that meets or exceeds the quality of the OEM.35 An "Alternate Offer" (AO) is essentially a SAR that is submitted in response to an active solicitation.30

The filter must be able to distinguish between solicitations that prohibit the submission of a SAR for that specific buy (e.g., "award cannot be delayed") and those that are open to it. An opportunity becomes a potential "GO" if it explicitly invites SARs or AOs and the procurement timeline is not prohibitive. The SAR process is complex and requires the prospective supplier to provide a detailed data package categorized by their experience with the part (e.g., Category I for a supplier who has made the exact item for the OEM, Category II for a supplier who has made a similar item).21 While this is a long and arduous process, it is the primary path to breaking into restricted markets.

### **5.3 The Reverse Engineering Opportunity**

For parts that are sole-sourced and for which the government does not have a TDP, the DLA has established a specific program to foster competition: the Replenishment Parts Purchase or Borrow (RPPOB) program.22 This program allows interested companies to purchase or borrow a sample of a sole-source part for the express purpose of reverse engineering it. After successfully reverse engineering the part, the company can then submit a SAR package for approval.22

This represents a significant strategic opportunity. Solicitations that mention the availability of samples for reverse engineering 10 or NSNs that are known to be part of the RPPOB program are not immediate tactical sales. They are long-term investments in developing a new capability that can lead to lucrative contracts in the future. The filter should be programmed to identify these opportunities and flag them for the strategic business development team.

The existence of these exception pathways reveals that opportunities are not simply binary. A restrictive AMC code like 5/D ("Sole Source, No Data") would normally be a "Hard NO-GO." However, if that same solicitation includes the phrase "DLA looking for competition for this item," the nature of the opportunity changes completely. It transforms from a closed door into a strategic invitation. This requires the filter to move beyond a simple GO/NO-GO logic to a more nuanced, three-tiered system that can distinguish between immediate tactical sales and long-term strategic investments.

## **Section 6: The Distributor's Role: Specific Rules and Requirements for Intermediaries**

Even when an opportunity is deemed a "GO" or a viable "FLAG FOR REVIEW," a distributor like SOS has an additional layer of rules and obligations to satisfy. The government places specific responsibilities on intermediaries to ensure the integrity of the supply chain. The filter's logic must account for these distributor-specific requirements, which primarily revolve around documentation, traceability, and the limits of commercial equivalency standards.

### **6.1 The Authorized Distributor Letter**

For many procurements of source-controlled or restricted items, it is not enough for a distributor to simply offer a part from an approved manufacturer. The distributor must prove its formal relationship with that manufacturer. Solicitations frequently include a non-negotiable requirement for this proof.

The key requirement is stated as: "Quotes/proposals from dealers/distributors for government approved source(s) MUST submit a copy of their authorized distributor letter (on the actual manufacturer’s letterhead)".13

This is a critical documentation requirement that must be fulfilled at the time the quote is submitted. Failure to provide this letter will result in the quote being deemed technically unacceptable and ineligible for award. While the automated filter cannot check for the existence of this letter, its logic must be tied to this business process. Any opportunity flagged as a potential "GO" for a source-controlled part must trigger a secondary, internal check within SOS's systems to verify that a valid, current authorized distributor letter is on file for the required manufacturer.

### **6.2 Traceability and Counterfeit Part Prevention**

The government is intensely focused on preventing non-conforming, unapproved, or counterfeit parts from entering the military supply chain, and it views the distribution channel as a potential point of weakness.4 A 2017 DoD Inspector General report identified lapses in DLA's ability to validate that parts purchased from distributors were, in fact, manufactured by the approved source.4

This focus has led to stricter enforcement and the inclusion of specific clauses in contracts. Distributors must be able to provide clear traceability and a documented chain of custody for their parts, proving they originated from the approved source.5 Clauses requiring suppliers to maintain a "Counterfeit Parts and Material Prevention Control Plan" are becoming more common.36 Furthermore, the rules explicitly state that a distributor's approval can be revoked if they change their proposed source of supply after being added to an approved list.5 This underscores the principle that approval is tied not just to the distributor, but to the specific distributor-manufacturer pairing for a given part.

### **6.3 The Limits of Commercial Equivalency (FAA PMA)**

In the commercial aviation world, the Federal Aviation Administration (FAA) grants Parts Manufacturer Approval (PMA) to companies to produce replacement parts. While there is some overlap between the military and civilian aviation sectors, holding an FAA PMA is not a substitute for DoD source approval.

A company that holds a PMA for a part identical to a military NSN may have a stronger case when submitting a SAR package, particularly under "SAR Category I" (which is for suppliers who have previously manufactured the exact item).34 Some solicitations, especially from the U.S. Coast Guard which operates many commercial derivative aircraft, may even explicitly require FAA-approved repair facilities or adherence to FAA standards.37

However, for core DoD weapon systems procured by DLA, the Army, the Navy, and the Air Force, the military's own ESA is the paramount authority.7 An FAA PMA part is not automatically acceptable. The manufacturer must still undergo the full military SAR process to be added to the ASL. Therefore, the automated filter should not treat the presence of "FAA Approved" or "PMA" as a reliable "GO" signal for DoD solicitations. It is a potentially positive factor for a strategic SAR assessment but does not override a "NO-GO" trigger based on military source control requirements.

## **Section 7: Recommendations for Filter Implementation and Opportunity Triage**

The preceding analysis provides the detailed components required to construct an intelligent and effective automated decision filter. To translate this analysis into a functional software system, the logic must be synthesized into a clear, prioritized structure. The most effective implementation is not a simple binary filter but a three-tiered triage system that accurately reflects the different types of opportunities present in the government marketplace. This approach will allow SOS to not only eliminate non-viable solicitations but also to identify and categorize strategic opportunities for future growth.

### **7.1 The Three-Tiered Triage System**

A binary GO/NO-GO filter is insufficient because it fails to distinguish between immediately actionable bids and long-term strategic plays. A more valuable system will categorize solicitations into three distinct tiers, each triggering a different workflow within SOS.

* **Tier 1: GO (Green Light):** This category is for solicitations that are fully competitive and immediately actionable. These are primarily opportunities with an AMC/AMSC code of 1/G or 2/G, indicating an open competition with a complete technical data package available.12 These solicitations should be routed directly to the quoting and procurement teams for immediate action.  
* **Tier 2: NO-GO (Red Light):** This category is for solicitations that are definitively closed to SOS. These are restricted opportunities (e.g., AMC 3, 4, or 5\) that also contain prohibitive language, such as "award cannot be delayed pending approval of a new source".1 These solicitations should be automatically archived by the system with no further action required.  
* **Tier 3: FLAG FOR REVIEW (Yellow Light):** This is the most critical category for competitive advantage. It captures solicitations that are restricted but contain an exception or a potential pathway to participation. This includes "Sources Sought" notices, invitations to submit a SAR, opportunities for reverse engineering under the RPPOB program, or any source-controlled item where SOS may be an authorized distributor for the named manufacturer.10 These solicitations should be routed to a specialized strategic sourcing manager or business development team for manual investigation and long-term planning.

### **7.2 Master Filter Logic Table**

The following table provides the master logic for the development team. It consolidates all trigger phrases, codes, and exceptions into a single, prioritized structure. The filter should process these rules in order of priority. For example, a "Sources Sought" notice (Priority 1\) should be flagged for strategic review even if it contains a restrictive AMC code (a lower priority rule).

| Priority | Condition / Trigger (Defaults to NO-GO) | Exception / Overriding Condition (Potential GO) | Required Internal Verification | Final Filter Output |
| :---- | :---- | :---- | :---- | :---- |
| 1 | Solicitation type is "Sources Sought" OR text contains "seeking new sources," "looking for competition," "provide any sources that may".10 | N/A (This is a top-level exception). | Confirm product category is relevant to SOS. | **FLAG FOR STRATEGIC REVIEW** |
| 2 | Solicitation mentions "reverse engineer," "sample available for reverse engineering," or the RPPOB program.10 | N/A (This is a top-level strategic exception). | Assess internal/partner capability for reverse engineering the item. | **FLAG FOR RPPOB PROGRAM** |
| 3 | Solicitation contains a restrictive AMC (3, 4, 5\) or AMSC (B, C, D, H, K, L, M, N, P, Q, R, S, T, U, V, Y).12 | Text explicitly invites "Source Approval Request," "SAR," or "Alternate Offer" submissions.30 | Review solicitation for SAR submission deadlines and requirements. | **FLAG FOR SAR PROCESS** |
| 4 | Solicitation contains a restrictive AMC (3, 4, 5\) or AMSC (B, C, D, H, K, L, M, N, P, Q, R, S, T, U, V, Y) and lists approved CAGE codes.18 | N/A | Check internal database to see if SOS is an authorized distributor for any of the listed CAGE codes. | **GO** (if authorized distributor) / **NO-GO** (if not) |
| 5 | Solicitation text contains "Source approval required," "engineering source approval," "only previously approved sources," or "deemed technically unacceptable".1 | Text contains prohibitive language like "award cannot be delayed".1 | None. | **NO-GO** |
| 6 | Solicitation has an AMC of 1 or 2\.28 | AMSC is 'G'.12 | None. | **GO** |
| 7 | Solicitation has an AMC of 1 or 2\.28 | AMSC is 'T' (QPL item).27 | Check internal database for a supplier on the specified QPL. | **GO** (if QPL supplier exists) / **NO-GO** (if not) |
| 8 | All other solicitations. | N/A | Default case. | **FLAG FOR MANUAL REVIEW** |

### **7.3 Recommendations for Continuous Improvement**

The government procurement landscape is dynamic. To ensure the long-term effectiveness of this automated filter, SOS should implement the following processes:

1. **Quarterly Logic Review:** The logic, trigger phrases, and codes used by the filter should be reviewed on a quarterly basis against new solicitation language to identify any emerging patterns or changes in government terminology.  
2. **Establish a Feedback Loop:** The strategic sourcing managers who review the "FLAGGED" opportunities should have a formal process for reporting new phrases, unique agency requirements, or rule exceptions back to the software development team. This will allow for iterative refinement of the filter's accuracy.  
3. **Develop an Internal Supplier Qualification Database:** The analysis repeatedly shows that success in the restricted market depends on knowing the current approval status of manufacturing partners. SOS should invest in building and maintaining a dynamic internal database that tracks its suppliers' approval statuses for specific NSNs, weapon systems, and military engineering authorities. This database would be a critical tool for validating the "FLAGGED" opportunities and making informed bid decisions.

#### **Works cited**

1. NAVSUP WSS Term Local Text (April 28, 2025), accessed August 8, 2025, [https://www.navsup.navy.mil/Portals/65/NAVSUP%20ENTERPRISE/NAVSUP%20Weapon%20Systems%20Support/Documents/NAVSUP%20WSS%20Term%20Local%20Text%20(28APR2025).docx?ver=M0Byyq3wuw1boxtal\_900A%3D%3D](https://www.navsup.navy.mil/Portals/65/NAVSUP%20ENTERPRISE/NAVSUP%20Weapon%20Systems%20Support/Documents/NAVSUP%20WSS%20Term%20Local%20Text%20\(28APR2025\).docx?ver=M0Byyq3wuw1boxtal_900A%3D%3D)  
2. 61--POWER SUPPLY, IN REPAIR/MODIFICATION OF | Bid Banana, accessed August 8, 2025, [https://bidbanana.thebidlab.com/bid/aFvpJXcPXP7awE201GsT](https://bidbanana.thebidlab.com/bid/aFvpJXcPXP7awE201GsT)  
3. REPAIR QUALIFICATION REQUIREMENTS (RQR) FOR PROPULSION CRITICAL SAFETY ITEMS (CSI) & CRITICAL APPLICATION ITEMS (CAI), accessed August 8, 2025, [https://www.tinker.af.mil/Portals/106/RQR-PSD-1%2028-January-2020.pdf](https://www.tinker.af.mil/Portals/106/RQR-PSD-1%2028-January-2020.pdf)  
4. Audit of the Defense Logistics Agency's Purchases of Aviation Critical Safety Items \- Oversight.gov, accessed August 8, 2025, [https://www.oversight.gov/sites/default/files/documents/reports/2019-12/DODIG-2020-037.pdf](https://www.oversight.gov/sites/default/files/documents/reports/2019-12/DODIG-2020-037.pdf)  
5. Aviation Source Approval and Management Handbook \- DLA, accessed August 8, 2025, [https://www.dla.mil/portals/104/documents/aviation/source%20approval%20handbook.pdf](https://www.dla.mil/portals/104/documents/aviation/source%20approval%20handbook.pdf)  
6. afmci23-113.pdf \- Air Force, accessed August 8, 2025, [https://static.e-publishing.af.mil/production/1/afmc/publication/afmci23-113/afmci23-113.pdf](https://static.e-publishing.af.mil/production/1/afmc/publication/afmci23-113/afmci23-113.pdf)  
7. B-421411, Chase Defense Partners \- GAO, accessed August 8, 2025, [https://www.gao.gov/assets/820/819375.pdf](https://www.gao.gov/assets/820/819375.pdf)  
8. In the United States Court of Federal Claims \- CM/ECF, accessed August 8, 2025, [https://ecf.cofc.uscourts.gov/cgi-bin/show\_public\_doc?2023cv0688-97-0](https://ecf.cofc.uscourts.gov/cgi-bin/show_public_doc?2023cv0688-97-0)  
9. Defense Contracting Bootcamp: Know the FLIS \- BidLink, accessed August 8, 2025, [https://www.bidlink.net/news/2023/09/defense-contracting-bootcamp-flis/](https://www.bidlink.net/news/2023/09/defense-contracting-bootcamp-flis/)  
10. Archives for September 2023 | BidLink Defense Industry News, accessed August 8, 2025, [https://www.bidlink.net/news/2023/09/](https://www.bidlink.net/news/2023/09/)  
11. Contracting Activity: Aviation AUC Solicitation Number: SPE4A5-20-R-0070 \- AWS, accessed August 8, 2025, [https://imlive.s3.amazonaws.com/Federal%20Government/ID104888615710135509742480110571535421031/SPE4A522F4865%20REDACTED.pdf](https://imlive.s3.amazonaws.com/Federal%20Government/ID104888615710135509742480110571535421031/SPE4A522F4865%20REDACTED.pdf)  
12. AMSC Codes \- Bidspeed, accessed August 8, 2025, [https://www.fedbidspeed.com/amsc](https://www.fedbidspeed.com/amsc)  
13. Coupling, Shaft, Rigi SPRPA125QEF44 \- HigherGov, accessed August 8, 2025, [https://www.highergov.com/contract-opportunity/coupling-shaft-rigi-sprpa125qef44-o-8c33b/](https://www.highergov.com/contract-opportunity/coupling-shaft-rigi-sprpa125qef44-o-8c33b/)  
14. FOR EASE OF PROCESSING, PLEASE RETURN THIS SHEET WHEN MAILING YOUR QUOTE. FMS \- AWS, accessed August 8, 2025, [https://imlive.s3.amazonaws.com/Federal%20Government/ID298140030860472715200029552900884933371/ZAPPPED.N0010420.QAC69.PDF](https://imlive.s3.amazonaws.com/Federal%20Government/ID298140030860472715200029552900884933371/ZAPPPED.N0010420.QAC69.PDF)  
15. SAM.gov, accessed August 8, 2025, [https://sam.gov/opp/85ead84068694f6cae85e31ae2f1cedb/view](https://sam.gov/opp/85ead84068694f6cae85e31ae2f1cedb/view)  
16. FBODaily.com | FedBizOpps: PRESOL | 29 | Body, Valve Assembly, accessed August 8, 2025, [https://ftp.fbodaily.com/archive/2015/10-October/17-Oct-2015/FBO-03923026.htm](https://ftp.fbodaily.com/archive/2015/10-October/17-Oct-2015/FBO-03923026.htm)  
17. SAM.gov, accessed August 8, 2025, [https://sam.gov/opp/fe4af0155a9044f6bfbba8d57f11e16b/view](https://sam.gov/opp/fe4af0155a9044f6bfbba8d57f11e16b/view)  
18. SAM.gov, accessed August 8, 2025, [https://sam.gov/workspace/contract/opp/fa71318cc603418d88ce630669157d85/view](https://sam.gov/workspace/contract/opp/fa71318cc603418d88ce630669157d85/view)  
19. 16--"source control item" \- SAM.gov, accessed August 8, 2025, [https://sam.gov/opp/5241f89565bd21636d433527f741e0dd/view](https://sam.gov/opp/5241f89565bd21636d433527f741e0dd/view)  
20. SAM.gov, accessed August 8, 2025, [https://sam.gov/opp/f1b2c996fdae436ab158db1a5d7f6968/view](https://sam.gov/opp/f1b2c996fdae436ab158db1a5d7f6968/view)  
21. NAVSUP Weapon Systems Support \- NAVSEA, accessed August 8, 2025, [https://www.navsea.navy.mil/Portals/103/Documents/NAVSSES/Small%20Business%20with%20Naval%20Supply%20NAVSUP.pdf](https://www.navsea.navy.mil/Portals/103/Documents/NAVSSES/Small%20Business%20with%20Naval%20Supply%20NAVSUP.pdf)  
22. New Source Contract Step-by-Step \- DLA, accessed August 8, 2025, [https://www.dla.mil/Aviation/Offers/Engineering/RPPOB/New-Source-Contract-Step-by-Step/](https://www.dla.mil/Aviation/Offers/Engineering/RPPOB/New-Source-Contract-Step-by-Step/)  
23. Development of a Naval Supply Systems Command Acquisition Supplement \- A Business Practice Improvement \- DTIC, accessed August 8, 2025, [https://apps.dtic.mil/sti/tr/pdf/AD1009341.pdf](https://apps.dtic.mil/sti/tr/pdf/AD1009341.pdf)  
24. 53--MOTOR AND BRAKE,AIR, IN REPAIR/MODIFICATION OF | Bid Banana, accessed August 8, 2025, [https://bidbanana.thebidlab.com/bid/AIPDrL3VrnQLRjAr29nj](https://bidbanana.thebidlab.com/bid/AIPDrL3VrnQLRjAr29nj)  
25. NAVSUP WSS Term Local Text (01FEB2023).docx \- Naval Supply Systems Command, accessed August 8, 2025, [https://www.navsup.navy.mil/Portals/65/NAVSUP%20ENTERPRISE/NAVSUP%20Weapon%20Systems%20Support/Documents/NAVSUP%20WSS%20Term%20Local%20Text%20(01FEB2023).docx?ver=MmLvlnC4PiLZeEAIRLQNdg%3D%3D](https://www.navsup.navy.mil/Portals/65/NAVSUP%20ENTERPRISE/NAVSUP%20Weapon%20Systems%20Support/Documents/NAVSUP%20WSS%20Term%20Local%20Text%20\(01FEB2023\).docx?ver=MmLvlnC4PiLZeEAIRLQNdg%3D%3D)  
26. In the United States Court of Federal Claims \- CM/ECF, accessed August 8, 2025, [https://ecf.cofc.uscourts.gov/cgi-bin/show\_public\_doc?2023cv0688-41-0](https://ecf.cofc.uscourts.gov/cgi-bin/show_public_doc?2023cv0688-41-0)  
27. NAICS | BidLink Defense Industry News, accessed August 8, 2025, [https://www.bidlink.net/news/tag/naics/](https://www.bidlink.net/news/tag/naics/)  
28. AMSC\_RMSC Codes Defined, accessed August 8, 2025, [https://www.tinker.af.mil/Portals/106/RSC%20Codes%20Defined.docx?ver=2017-06-27-115450-837](https://www.tinker.af.mil/Portals/106/RSC%20Codes%20Defined.docx?ver=2017-06-27-115450-837)  
29. DoD Procurement; Acquisition Method Codes (Part 1\) | BidLink Defense Industry News, accessed August 8, 2025, [https://www.bidlink.net/news/2019/01/dod-procurement-acquisition-method-codes-part-1/](https://www.bidlink.net/news/2019/01/dod-procurement-acquisition-method-codes-part-1/)  
30. Value Engineering \> Defense Logistics Agency \> Details \- DLA, accessed August 8, 2025, [https://www.dla.mil/Small-Business/Resources/Training/Details/Article/4163628/value-engineering/](https://www.dla.mil/Small-Business/Resources/Training/Details/Article/4163628/value-engineering/)  
31. cooler, lubricating \- SAM.gov, accessed August 8, 2025, [https://sam.gov/opp/dcfba46246c34ec2b5dbb0e25c79bf3d/view](https://sam.gov/opp/dcfba46246c34ec2b5dbb0e25c79bf3d/view)  
32. NSN: 5895-01-587-8342, PARTS KIT,ELECTRONI ... \- SAM.gov, accessed August 8, 2025, [https://sam.gov/opp/2357ba9c05364f49afff15c416cae645/view](https://sam.gov/opp/2357ba9c05364f49afff15c416cae645/view)  
33. Mount, Viewer SPE4A6-16-X-0627 \- HigherGov, accessed August 8, 2025, [https://www.highergov.com/contract-opportunity/mount-viewer-spe4a6-16-x-0627-j-5b6df/](https://www.highergov.com/contract-opportunity/mount-viewer-spe4a6-16-x-0627-j-5b6df/)  
34. DEFENSE LOGISTICS AGENCY DLA Aviation Source Approval Request Process, accessed August 8, 2025, [https://www.dla.mil/Portals/104/Documents/Aviation/IndustryDays/2019/Source%20Approval.pdf?ver=2019-05-28-095351-617](https://www.dla.mil/Portals/104/Documents/Aviation/IndustryDays/2019/Source%20Approval.pdf?ver=2019-05-28-095351-617)  
35. dla land and maritime \- alternate offer & source approval request (ao & sar) guidance, accessed August 8, 2025, [https://www.dla.mil/portals/104/documents/landandmaritime/v/ve/vendorinfo.pdf](https://www.dla.mil/portals/104/documents/landandmaritime/v/ve/vendorinfo.pdf)  
36. Procurement Quality Requirements | Reinhold Industries, accessed August 8, 2025, [https://reinhold-ind.com/wp-content/uploads/2023/10/F-7.4.2-QC-Rev-I-Procurement-Quality-Requirements.pdf](https://reinhold-ind.com/wp-content/uploads/2023/10/F-7.4.2-QC-Rev-I-Procurement-Quality-Requirements.pdf)  
37. Repair of APU Electronic Controls and ATF3 Bleed Solenoid Packs. \- SAM.gov, accessed August 8, 2025, [https://sam.gov/opp/a2328f7b05f891925f32e477ac4d5e11/view](https://sam.gov/opp/a2328f7b05f891925f32e477ac4d5e11/view)  
38. CBCA 2119 TKC AEROSPACE, INC., Appellant, v. DEPARTMENT OF HOMELAND SECURITY, Respondent., accessed August 8, 2025, [https://www.cbca.gov/files/decisions/2012/MCCANN\_01-31-12\_2119\_\_TKC\_AEROSPACE\_INC\_508.pdf](https://www.cbca.gov/files/decisions/2012/MCCANN_01-31-12_2119__TKC_AEROSPACE_INC_508.pdf)