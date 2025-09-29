"""Unit tests for individual stage processors"""
import unittest
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stage_processors.stage_01_timing import TimingStage
from stage_processors.stage_02_set_asides import SetAsidesStage
from stage_processors.stage_03_security import SecurityStage


class TestTimingStage(unittest.TestCase):
    """Test cases for timing stage"""

    def setUp(self):
        self.stage = TimingStage()

    def test_past_deadline_detection(self):
        """Test detection of past deadlines"""
        past_date = (datetime.now() - timedelta(days=5)).strftime("%B %d, %Y")
        text = f"Proposals were due by {past_date}"
        result = self.stage.check_timing(text)
        self.assertEqual(result['decision'], 'NO-GO')
        self.assertLess(result['days_remaining'], 0)

    def test_future_deadline_detection(self):
        """Test detection of future deadlines"""
        future_date = (datetime.now() + timedelta(days=30)).strftime("%B %d, %Y")
        text = f"Responses due by {future_date}"
        result = self.stage.check_timing(text)
        self.assertEqual(result['decision'], 'GO')
        self.assertGreater(result['days_remaining'], 0)

    def test_today_deadline_detection(self):
        """Test detection of today's deadline"""
        today = datetime.now().strftime("%B %d, %Y")
        text = f"Deadline: {today}"
        result = self.stage.check_timing(text)
        # Should be NO-GO or INDETERMINATE depending on time
        self.assertIn(result['decision'], ['NO-GO', 'INDETERMINATE'])

    def test_no_deadline_detection(self):
        """Test handling when no deadline is found"""
        text = "This opportunity has no specific deadline mentioned"
        result = self.stage.check_timing(text)
        self.assertEqual(result['decision'], 'GO')
        self.assertEqual(result.get('flag'), 'NO_DEADLINE_FOUND')
        self.assertIsNone(result['deadline_found'])

    def test_various_deadline_formats(self):
        """Test various deadline format patterns"""
        patterns = [
            ("Closing date: December 31, 2025", "2025-12-31"),
            ("Must be received by 12/31/2025", "2025-12-31"),
            ("No later than December 31, 2025", "2025-12-31"),
            ("Expires on 31 Dec 2025", "2025-12-31"),
        ]
        for text, expected_date in patterns:
            result = self.stage.check_timing(text)
            self.assertIsNotNone(result['deadline_found'])
            # Check the date portion matches
            self.assertIn(expected_date, result['deadline_found'])


class TestSetAsidesStage(unittest.TestCase):
    """Test cases for set-asides stage"""

    def setUp(self):
        self.stage = SetAsidesStage()

    def test_8a_detection(self):
        """Test 8(a) set-aside detection"""
        text = "This is an 8(a) set-aside procurement"
        result = self.stage.check_set_asides(text)
        self.assertEqual(result['decision'], 'NO-GO')
        self.assertIn('8(a)', result['set_aside_types'])

    def test_sdvosb_detection(self):
        """Test SDVOSB detection"""
        text = "Service-Disabled Veteran-Owned Small Business set-aside"
        result = self.stage.check_set_asides(text)
        self.assertEqual(result['decision'], 'NO-GO')
        self.assertIn('SDVOSB', result['set_aside_types'])

    def test_multiple_set_asides(self):
        """Test detection of multiple set-aside types"""
        text = "This procurement is set aside for 8(a) or WOSB businesses"
        result = self.stage.check_set_asides(text)
        self.assertEqual(result['decision'], 'NO-GO')
        self.assertEqual(len(result['set_aside_types']), 2)

    def test_unrestricted_detection(self):
        """Test unrestricted/full and open detection"""
        text = "This is an unrestricted, full and open competition"
        result = self.stage.check_set_asides(text)
        self.assertEqual(result['decision'], 'GO')
        self.assertEqual(result['set_aside_count'], 0)

    def test_naics_without_set_aside(self):
        """Test NAICS code without explicit set-aside"""
        text = "NAICS Code: 541330, Size Standard: $16.5 million"
        result = self.stage.check_set_asides(text)
        self.assertEqual(result['decision'], 'INDETERMINATE')
        self.assertIsNotNone(result['naics_info'])

    def test_no_set_aside(self):
        """Test when no set-aside is found"""
        text = "Commercial item procurement with no restrictions"
        result = self.stage.check_set_asides(text)
        self.assertEqual(result['decision'], 'GO')
        self.assertEqual(result['set_aside_count'], 0)


class TestSecurityStage(unittest.TestCase):
    """Test cases for security stage"""

    def setUp(self):
        self.stage = SecurityStage()

    def test_secret_clearance_detection(self):
        """Test Secret clearance detection"""
        text = "Contractor must possess a Secret clearance"
        result = self.stage.check_security(text)
        self.assertEqual(result['decision'], 'NO-GO')
        self.assertEqual(result['clearance_level'], 'SECRET')

    def test_top_secret_sci_detection(self):
        """Test Top Secret/SCI detection"""
        text = "Requires TS/SCI clearance for all personnel"
        result = self.stage.check_security(text)
        self.assertEqual(result['decision'], 'NO-GO')
        self.assertEqual(result['clearance_level'], 'TOP SECRET/SCI')

    def test_facility_clearance_detection(self):
        """Test facility clearance detection"""
        text = "Must have facility clearance and DD-254"
        result = self.stage.check_security(text)
        self.assertEqual(result['decision'], 'NO-GO')
        self.assertTrue(result['has_facility_requirement'])

    def test_sap_detection(self):
        """Test Special Access Program detection"""
        text = "Work involves Special Access Program (SAP)"
        result = self.stage.check_security(text)
        self.assertEqual(result['decision'], 'NO-GO')
        self.assertTrue(result['has_sap_requirement'])

    def test_false_positive_sap(self):
        """Test SAP software is not flagged as security requirement"""
        text = "Must have experience with SAP software and ERP systems"
        result = self.stage.check_security(text)
        self.assertEqual(result['decision'], 'GO')
        self.assertFalse(result['has_sap_requirement'])

    def test_no_clearance_required(self):
        """Test when no clearance is required"""
        text = "Commercial procurement with no special requirements"
        result = self.stage.check_security(text)
        self.assertEqual(result['decision'], 'GO')
        self.assertIsNone(result['clearance_level'])

    def test_classification_without_clearance(self):
        """Test classification markings without explicit clearance requirement"""
        text = "Contains ITAR-controlled technical data"
        result = self.stage.check_security(text)
        self.assertEqual(result['decision'], 'INDETERMINATE')
        self.assertEqual(result.get('flag'), 'CLASSIFICATION_WITHOUT_CLEARANCE')


if __name__ == '__main__':
    unittest.main()