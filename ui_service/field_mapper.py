#!/usr/bin/env python3
"""
Field mapper for UI to handle different field naming conventions
Maps between CSV/JSON field names and UI display requirements
"""

import pandas as pd
from typing import Dict, Any, Optional


class FieldMapper:
    """Handles field mapping between backend output and UI display"""

    # Field aliases - UI will check these in order
    FIELD_MAPPINGS = {
        'title': ['announcement_title', 'solicitation_title', 'title', 'sos_pipeline_title'],
        'id': ['announcement_number', 'solicitation_id', 'opportunity_id', 'id'],
        'agency': ['agency', 'agency_name', 'contracting_office'],
        'result': ['result', 'final_decision', 'decision', 'classification'],
        'stage': ['pipeline_stage', 'assessment_type', 'processing_method'],
        'url': ['highergov_url', 'sam_url', 'url', 'source_url'],
        'description': ['brief_description', 'description', 'summary'],
        'rationale': ['analysis_notes', 'rationale', 'reasoning', 'recommendation'],
        'knockout': ['knockout_category', 'knock_pattern', 'knockout_reason'],
        'due_date': ['due_date', 'response_due_date', 'deadline'],
        'posted_date': ['posted_date', 'publish_date', 'post_date'],
        'special_action': ['special_action', 'co_contact_reason', 'action_required']
    }

    @staticmethod
    def get_field(row: pd.Series, field_type: str, default: str = 'N/A') -> str:
        """
        Get a field value from a row, checking multiple possible field names

        Args:
            row: Pandas Series containing the data
            field_type: The type of field to get (e.g., 'title', 'id')
            default: Default value if field not found

        Returns:
            The field value or default if not found
        """
        # Get list of possible field names
        possible_fields = FieldMapper.FIELD_MAPPINGS.get(field_type, [field_type])

        # Try each possible field name
        for field_name in possible_fields:
            if field_name in row.index:
                value = row[field_name]
                # Check for valid value
                if not pd.isna(value) and str(value).strip() not in ['', 'nan', 'None']:
                    return str(value)

        return default

    @staticmethod
    def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize a dataframe to have consistent column names

        Args:
            df: Input dataframe with various column names

        Returns:
            DataFrame with normalized column names
        """
        # Create a copy to avoid modifying original
        normalized = df.copy()

        # Add normalized columns if they don't exist
        for standard_name, possible_names in FieldMapper.FIELD_MAPPINGS.items():
            if standard_name not in normalized.columns:
                for possible_name in possible_names:
                    if possible_name in normalized.columns:
                        normalized[standard_name] = normalized[possible_name]
                        break

        return normalized

    @staticmethod
    def format_result_color(result: str) -> str:
        """
        Get the color/style for a result value

        Args:
            result: The decision result (GO, NO-GO, INDETERMINATE)

        Returns:
            Color code for streamlit
        """
        result_upper = str(result).upper()
        if 'GO' in result_upper and 'NO' not in result_upper:
            return '🟢'  # Green for GO
        elif 'NO' in result_upper or 'NO-GO' in result_upper:
            return '🔴'  # Red for NO-GO
        elif 'INDETERMINATE' in result_upper:
            return '🟡'  # Yellow for INDETERMINATE
        else:
            return '⚪'  # White for unknown

    @staticmethod
    def get_stage_description(stage: str) -> str:
        """
        Get human-readable description for pipeline stage

        Args:
            stage: Pipeline stage code

        Returns:
            Human-readable description
        """
        stage_map = {
            'APP': 'Regex Filter',
            'BATCH': 'Batch AI Assessment',
            'AGENT': 'Agent Verification',
            'REGEX': 'Regex Filter',
            'REGEX_KNOCKOUT': 'Filtered by Regex',
            'MISTRAL_BATCH_ASSESSMENT': 'Batch AI Assessment',
            'MISTRAL_ASSESSMENT': 'Real-time AI Assessment'
        }

        # Check for exact match first
        if stage in stage_map:
            return stage_map[stage]

        # Check if stage contains any known patterns
        stage_upper = str(stage).upper()
        for key, value in stage_map.items():
            if key in stage_upper:
                return value

        return stage  # Return as-is if no match