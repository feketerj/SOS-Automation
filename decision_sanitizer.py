#!/usr/bin/env python3
"""
Decision Sanitizer - Ensures consistent AGENT SCHEMA formatting across all pipeline stages
Transforms any pipeline output to match the unified Agent schema format
"""

class DecisionSanitizer:
    """
    Transforms pipeline data to unified Agent schema format.
    Ensures all stages (App/Batch/Agent) output identical structure.
    """

    # Assessment type translation mapping
    ASSESSMENT_TYPE_MAP = {
        # Legacy names -> Canonical names
        'REGEX_KNOCKOUT': 'APP_KNOCKOUT',
        'REGEX_ONLY': 'APP_KNOCKOUT',
        'APP_ONLY': 'APP_KNOCKOUT',
        'AGENT_VERIFIED': 'MISTRAL_ASSESSMENT',
        'AGENT_AI': 'MISTRAL_ASSESSMENT',
        'BATCH_AI': 'MISTRAL_BATCH_ASSESSMENT',
        # Already canonical (map to themselves)
        'APP_KNOCKOUT': 'APP_KNOCKOUT',
        'MISTRAL_ASSESSMENT': 'MISTRAL_ASSESSMENT',
        'MISTRAL_BATCH_ASSESSMENT': 'MISTRAL_BATCH_ASSESSMENT'
    }

    @staticmethod
    def _normalize_assessment_type(assessment_type):
        """
        Normalize assessment type to canonical name.

        Args:
            assessment_type: Raw assessment type string or None

        Returns:
            Canonical assessment type string
        """
        if not assessment_type:
            return ''

        # Ensure it's a string before calling upper()
        assessment_type_str = str(assessment_type) if assessment_type is not None else ''
        if not assessment_type_str:
            return ''

        # Check mapping
        normalized = DecisionSanitizer.ASSESSMENT_TYPE_MAP.get(
            assessment_type_str.upper(),
            assessment_type_str  # Return original if not in map
        )

        # Optional: Log translation for monitoring (can be enabled/disabled)
        if hasattr(DecisionSanitizer, '_log_translation') and DecisionSanitizer._log_translation:
            if normalized != assessment_type:
                print(f"[TRANSLATION] Assessment type: '{assessment_type}' -> '{normalized}'")

        return normalized

    @staticmethod
    def is_already_sanitized(data):
        """
        Check if data has already been sanitized.

        Args:
            data: Dictionary to check

        Returns:
            bool: True if already sanitized, False otherwise
        """
        if not isinstance(data, dict):
            return False

        # Primary check: explicit _sanitized marker
        if data.get('_sanitized') == True:
            # If explicitly marked, trust it
            return True

        # Secondary check: has unified schema structure
        # Require result field and at least one tracking field
        has_normalized_result = data.get('result') in ['GO', 'NO-GO', 'INDETERMINATE']
        has_pipeline_stage = 'pipeline_stage' in data and data['pipeline_stage']
        has_assessment_type = 'assessment_type' in data and data['assessment_type']

        # Consider sanitized if has result and at least one tracking field
        return has_normalized_result and (has_pipeline_stage or has_assessment_type)

    @staticmethod
    def sanitize(data, _recursion_guard=False):
        """
        Transform data to unified Agent schema format.

        Args:
            data: Dictionary containing assessment data from any pipeline stage
            _recursion_guard: Internal flag to prevent infinite recursion

        Returns:
            Dictionary in unified Agent schema format with these fields:
            - solicitation_id, solicitation_title, summary
            - result (GO/NO-GO/INDETERMINATE)
            - knock_out_reasons, exceptions, special_action
            - rationale, recommendation, sos_pipeline_title
            - sam_url, hg_url, pipeline_stage, assessment_type
        """
        if not isinstance(data, dict):
            return data

        # Skip if already sanitized to prevent double processing
        # But if called with recursion guard, force sanitization
        if not _recursion_guard and DecisionSanitizer.is_already_sanitized(data):
            return data

        # Prevent infinite recursion
        if _recursion_guard and data.get('_recursion_blocked'):
            # Data has been through sanitization twice, return as-is
            return data

        # Map various decision field names to 'result'
        result = None

        # Check top-level fields first
        for field in ['result', 'decision', 'final_decision', 'recommendation']:
            if field in data:
                result = DecisionSanitizer._normalize(data[field])
                break

        # If not found, check nested 'assessment' dictionary (legacy format)
        if result is None and 'assessment' in data and isinstance(data['assessment'], dict):
            assessment_data = data['assessment']
            for field in ['decision', 'result', 'final_decision', 'recommendation']:
                if field in assessment_data:
                    result = DecisionSanitizer._normalize(assessment_data[field])
                    break

        if result is None:
            result = 'INDETERMINATE'

        # Determine pipeline stage and assessment type
        pipeline_stage = data.get('pipeline_stage', '')
        assessment_type = data.get('assessment_type', '')

        # Normalize assessment type if it exists
        if assessment_type:
            assessment_type = DecisionSanitizer._normalize_assessment_type(assessment_type)

        # Auto-detect if not specified
        if not pipeline_stage or not assessment_type:
            # Check processing method field first (most reliable)
            processing_method = data.get('processing_method', '')
            if processing_method == 'APP_ONLY' or processing_method == 'REGEX_ONLY':
                if not pipeline_stage:
                    pipeline_stage = 'APP'
                if not assessment_type:
                    assessment_type = 'APP_KNOCKOUT'
            elif processing_method == 'BATCH_AI':
                if not pipeline_stage:
                    pipeline_stage = 'BATCH'
                if not assessment_type:
                    assessment_type = 'MISTRAL_BATCH_ASSESSMENT'
            elif processing_method == 'AGENT_AI' or processing_method == 'AGENT_VERIFIED':
                # Handle both AGENT_AI and AGENT_VERIFIED as agent assessments
                if not pipeline_stage:
                    pipeline_stage = 'AGENT'
                if not assessment_type:
                    assessment_type = 'MISTRAL_ASSESSMENT'
            # Check for specific field patterns
            elif 'result' in data and 'knock_out_reasons' in data and 'exceptions' in data:
                # Agent output has these specific fields
                if not pipeline_stage:
                    pipeline_stage = 'AGENT'
                if not assessment_type:
                    assessment_type = 'MISTRAL_ASSESSMENT'
            elif 'batch' in str(data.get('source', '')).lower() or 'BATCH_AI' in str(data.get('processing_method', '')):
                if not pipeline_stage:
                    pipeline_stage = 'BATCH'
                if not assessment_type:
                    assessment_type = 'MISTRAL_BATCH_ASSESSMENT'
            elif 'regex_knockout' in data or ('knock_pattern' in data and not 'result' in data):
                if not pipeline_stage:
                    pipeline_stage = 'APP'
                if not assessment_type:
                    assessment_type = 'APP_KNOCKOUT'
            else:
                # Default based on presence of certain fields
                if data.get('model_id') or data.get('agent_id'):
                    if not pipeline_stage:
                        pipeline_stage = 'AGENT'
                    if not assessment_type:
                        assessment_type = 'MISTRAL_ASSESSMENT'
                elif data.get('assessment') and isinstance(data.get('assessment'), dict):
                    # Legacy nested format, likely from batch
                    if not pipeline_stage:
                        pipeline_stage = 'BATCH'
                    if not assessment_type:
                        assessment_type = 'MISTRAL_BATCH_ASSESSMENT'
                else:
                    # Only set defaults if nothing is already set
                    if not pipeline_stage and not assessment_type:
                        pipeline_stage = 'APP'
                        assessment_type = 'APP_KNOCKOUT'

        # Final normalization of assessment_type after all detection logic
        assessment_type = DecisionSanitizer._normalize_assessment_type(assessment_type)

        # Build unified schema output
        unified = {
            # Core Agent schema fields (10 required)
            'solicitation_id': data.get('solicitation_id', data.get('source_id', data.get('announcement_number', ''))),
            'solicitation_title': data.get('solicitation_title', data.get('title', data.get('announcement_title', ''))),
            'summary': data.get('summary', data.get('ai_summary', data.get('description_text', '')))[:500] if data.get('summary', data.get('ai_summary', data.get('description_text', ''))) else '',
            'result': result,
            'final_decision': result,  # Keep for backward compatibility with output manager
            'knock_out_reasons': data.get('knock_out_reasons', [data.get('knock_pattern')] if data.get('knock_pattern') else []),
            'exceptions': data.get('exceptions', []),
            'special_action': data.get('special_action', ''),
            'rationale': data.get('rationale', data.get('reasoning',
                        data.get('assessment', {}).get('reasoning', data.get('primary_blocker', '')))),
            'recommendation': data.get('recommendation', ''),
            'sos_pipeline_title': data.get('sos_pipeline_title', ''),

            # Extended fields for tracking
            'sam_url': data.get('sam_url', data.get('sam_gov_url', data.get('source_path', ''))),
            'hg_url': data.get('hg_url', data.get('highergov_url', data.get('path', data.get('url', '')))),
            'pipeline_stage': pipeline_stage,
            'assessment_type': assessment_type,

            # Mark as sanitized to prevent double processing
            '_sanitized': True,

            # Add recursion blocker if we're in a recursive call
            '_recursion_blocked': _recursion_guard
        }

        # Remove the recursion blocker if not needed
        if not _recursion_guard:
            unified.pop('_recursion_blocked', None)

        # Preserve any additional metadata
        for key in ['agency', 'due_date', 'posted_date', 'naics', 'psc', 'set_aside',
                    'value_low', 'value_high', 'place_of_performance', 'doc_length',
                    'announcement_number', 'announcement_title', 'opportunity_id',
                    'brief_description', 'analysis_notes', 'knock_pattern',
                    'knockout_category', 'highergov_url', 'assessment_timestamp']:
            if key in data:
                unified[key] = data[key]

        return unified

    @staticmethod
    def _normalize(decision):
        """
        Normalize decision to exact format expected by output manager.
        Must return exactly 'GO', 'NO-GO', or 'INDETERMINATE'.

        Args:
            decision: Raw decision string

        Returns:
            Normalized decision string
        """
        if decision is None:
            return 'INDETERMINATE'

        # Convert to uppercase string and strip whitespace
        decision_upper = str(decision).upper().strip()

        # Check for GO (must be exact match or contain GO without NO)
        if decision_upper == 'GO':
            return 'GO'
        elif 'GO' in decision_upper and 'NO' not in decision_upper:
            return 'GO'

        # Check for NO-GO variants
        elif 'NO-GO' in decision_upper:
            return 'NO-GO'
        elif 'NO_GO' in decision_upper:
            return 'NO-GO'
        elif decision_upper == 'NO GO':
            return 'NO-GO'
        elif decision_upper.startswith('NO') and 'GO' in decision_upper:
            return 'NO-GO'

        # Check for INDETERMINATE or unknown
        elif 'INDETERMINATE' in decision_upper:
            return 'INDETERMINATE'
        elif 'UNKNOWN' in decision_upper:
            return 'INDETERMINATE'
        elif 'FURTHER' in decision_upper:
            return 'INDETERMINATE'
        elif 'CONTACT' in decision_upper and 'CO' in decision_upper:
            return 'INDETERMINATE'

        # Default to INDETERMINATE for any unrecognized format
        else:
            return 'INDETERMINATE'

    @staticmethod
    def sanitize_batch(data_list):
        """
        Sanitize a list of assessment dictionaries.

        Args:
            data_list: List of assessment dictionaries

        Returns:
            List of sanitized assessment dictionaries
        """
        if not isinstance(data_list, list):
            return data_list

        return [DecisionSanitizer.sanitize(item) for item in data_list]