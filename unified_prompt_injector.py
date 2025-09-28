#!/usr/bin/env python3
"""
Unified Prompt Injector - Ensures all stages use consistent assessment logic.
"""

import os
from pathlib import Path

class UnifiedPromptInjector:
    """Manages unified prompts across batch processor and agent."""

    def __init__(self):
        self.base_path = Path(__file__).parent
        # Load prompts first
        self.prompts = {
            'minimal': self._load_prompt('BATCH_SYSTEM_PROMPT_MINIMAL.md'),
            'full': self._load_prompt('UNIFIED_SYSTEM_PROMPT.md')
        }
        # Then parse sections from the full prompt
        self.prompts['sections'] = self._load_sections()

    def _load_prompt(self, filename):
        """Load a prompt file."""
        filepath = self.base_path / filename
        if filepath.exists():
            return filepath.read_text(encoding='utf-8')
        return None

    def _load_sections(self):
        """Parse the full prompt into sections."""
        full_prompt = self.prompts.get('full', '')
        if not full_prompt:
            return {}

        sections = {}
        current_section = None
        current_content = []

        for line in full_prompt.split('\n'):
            if line.startswith('## SECTION'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content)
                current_section = line.split(':')[1].split('(')[0].strip() if ':' in line else 'UNKNOWN'
                current_content = [line]
            elif current_section:
                current_content.append(line)

        if current_section:
            sections[current_section] = '\n'.join(current_content)

        return sections

    def get_batch_prompt(self, token_limit=1000):
        """Get appropriate prompt for batch processor based on token limit."""
        if token_limit < 1000:
            return self.prompts.get('minimal', '')
        else:
            # Return sections 1-3 for medium token limit
            sections = []
            for section_name in ['CORE MISSION', 'CRITICAL OVERRIDES', 'KNOCKOUT CATEGORIES - QUICK REFERENCE']:
                if section_name in self.prompts.get('sections', {}):
                    sections.append(self.prompts['sections'][section_name])
            return '\n\n'.join(sections)

    def get_agent_prompt(self):
        """Get full prompt for agent."""
        return self.prompts.get('full', '')

    def get_few_shot_examples(self):
        """Extract just the examples section."""
        sections = self.prompts.get('sections', {})
        return sections.get('FEW-SHOT EXAMPLES', '')

    def format_for_batch_api(self, prompt, user_message):
        """Format prompt and user message for Mistral batch API."""
        return {
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_message}
            ]
        }

    def format_for_agent_api(self, user_message):
        """Format for agent API with full prompt."""
        return {
            "messages": [
                {"role": "system", "content": self.get_agent_prompt()},
                {"role": "user", "content": user_message}
            ]
        }

    def get_override_rules(self):
        """Extract just the override rules for quick reference."""
        sections = self.prompts.get('sections', {})
        return sections.get('CRITICAL OVERRIDES', '')

# Usage example
if __name__ == "__main__":
    injector = UnifiedPromptInjector()

    print("=== MINIMAL PROMPT (Batch) ===")
    print(injector.get_batch_prompt(token_limit=500)[:500] + "...")

    print("\n=== OVERRIDE RULES ===")
    print(injector.get_override_rules()[:500] + "...")

    print("\n=== FEW-SHOT EXAMPLES ===")
    print(injector.get_few_shot_examples()[:500] + "...")

    # Example batch API formatting
    test_opportunity = "F-16 parts with AMSC Code Z"
    batch_formatted = injector.format_for_batch_api(
        injector.get_batch_prompt(token_limit=1000),
        test_opportunity
    )
    print("\n=== BATCH API FORMAT ===")
    print(f"System: {batch_formatted['messages'][0]['content'][:100]}...")
    print(f"User: {batch_formatted['messages'][1]['content']}")