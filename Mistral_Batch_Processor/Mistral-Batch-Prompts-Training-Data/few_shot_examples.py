"""
Few-shot examples for batch processing
Selected to show diverse decision patterns - clear GOs, clear NO-GOs, and edge cases
"""

FEW_SHOT_EXAMPLES = [
    {
        "type": "CLEAR GO - Simple Commercial Parts",
        "user": "Request for Quote: 500 EA bolts, screws, and washers, various NSNs. Commercial items, surplus acceptable. FAA 8130-3 required. Open competition.",
        "assistant": "GO - Standard commercial hardware perfectly aligned with SOS capabilities. Open competition with no restrictions. Surplus explicitly acceptable matches our inventory model. FAA 8130-3 is our standard certification. No platform restrictions, no set-asides, no security requirements. These are commodity parts we stock regularly. Pipeline title: PN: Various | Qty: 500 | Condition: Surplus | Commercial hardware purchase."
    },
    {
        "type": "CLEAR GO - Boeing 737 Refurbished",
        "user": "Boeing 737-800 brake assemblies needed. 25 units, refurbished acceptable with FAA Form 8130-3. Small business set-aside. 45 days delivery.",
        "assistant": "GO - Boeing 737 is our core commercial platform. Refurbished parts are our specialty with FAA 8130-3 standard documentation. Small business set-aside favors SOS. No technical data restrictions or source approval requirements. Commercial aircraft with reasonable delivery timeline. Pipeline title: PN: Various | Qty: 25 | Condition: Refurb | Boeing 737 | Purchase brake assemblies."
    },
    {
        "type": "CLEAR NO-GO - Military Fighter",
        "user": "F-16 Block 50 fighter jet components. New manufacture required. Secret clearance mandatory. Drawings not available.",
        "assistant": "NO-GO - F-16 is pure military fighter platform. Secret clearance requirement is automatic disqualifier for SOS. New manufacture without drawings impossible for parts distributor. Military-only platform with no civilian equivalent. Multiple hard knock-outs with no exceptions available."
    },
    {
        "type": "CLEAR NO-GO - Wrong Set-Aside",
        "user": "8(a) set-aside for hydraulic pumps. Must be certified 8(a) minority-owned business. Refurbished acceptable.",
        "assistant": "NO-GO - 8(a) set-aside immediately disqualifies SOS. We don't have 8(a) certification which is reserved for socially/economically disadvantaged businesses. Set-aside restrictions are hard knock-outs regardless of technical capability. Cannot pursue."
    },
    {
        "type": "EDGE CASE - Contact CO",
        "user": "P-8 Poseidon (Boeing 737 variant) spare parts. Approved sources list applies but FAA 8130-3 acceptable for commercial equivalents. Navy program.",
        "assistant": "CONTACT CO - P-8 is military variant of Boeing 737 which SOS supports. Approved sources list typically requires SAR, but FAA 8130-3 acceptance for commercial equivalents suggests opening. Recommend contacting Contracting Officer to clarify if our 737 inventory qualifies. This matches exception for Navy commercial platforms."
    }
]

def get_few_shot_messages():
    """
    Returns few-shot examples formatted as messages for batch processing
    """
    messages = []
    for example in FEW_SHOT_EXAMPLES:
        messages.append({"role": "user", "content": example["user"]})
        messages.append({"role": "assistant", "content": example["assistant"]})
    return messages