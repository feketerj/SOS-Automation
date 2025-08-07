import os
import json
import logging
from dotenv import load_dotenv

# Import our custom modules
# Make sure these files are in the correct subdirectories (api_clients/ and filters/)
from api_clients.highergov_client_enhanced import EnhancedHigherGovClient
from filters.initial_checklist_v2 import InitialChecklistFilterV2, Decision

# --- Configuration ---
# Set up basic logging to see the script's progress
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file (for the API key)
load_dotenv()

# Get configuration from environment variables
SAVED_SEARCH_ID = os.getenv('SAVED_SEARCH_ID', 'g6eFIE5ftdvpSvP-u1UJ-')
OUTPUT_DIR = 'output'


def main():
    """
    Main function to run the SOS opportunity assessment pipeline.
    """
    logging.info("--- Starting SourceOne Spares Automation Pipeline ---")

    # Create the output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    logging.info(f"Output will be saved to the '{OUTPUT_DIR}' directory.")

    try:
        # --- Step 1: Initialize Clients ---
        api_client = EnhancedHigherGovClient()
        filter_logic = InitialChecklistFilterV2()
        logging.info("API Client and V2 Filter Logic initialized successfully.")

        # --- Step 2: Fetch Opportunities ---
        logging.info(f"Fetching opportunities from saved search ID: {SAVED_SEARCH_ID}")
        # Use the correct HigherGov API endpoint structure
        search_params = {
            'api_key': api_client.api_key,
            'search_id': SAVED_SEARCH_ID,
            'page_size': 100,  # Get 100 at a time
            'source_type': 'sam'  # Federal opportunities
        }
        # Use the correct endpoint path
        response_data = api_client._get('opportunity/', params=search_params)
        
        opportunities = response_data.get('results', [])
        if not opportunities:
            logging.warning("No opportunities found for the given saved search. Exiting.")
            return

        logging.info(f"Found {len(opportunities)} opportunities to process.")

        # --- Step 3: Process Each Opportunity ---
        for i, opp in enumerate(opportunities, 1):
            opp_id = opp.get('source_id', 'UnknownID')
            opp_title = opp.get('title', 'Unknown Title')
            
            print("\n" + "="*80)
            logging.info(f"Processing Opportunity {i}/{len(opportunities)}: {opp_title} ({opp_id})")
            
            # This would be the place to fetch full document text if not already in the opp object
            # For now, we rely on the text extracted by the filter's method.
            
            # --- Step 4: Assess with V2 Filter ---
            final_decision, detailed_results = filter_logic.assess_opportunity(opp)
            
            # --- Step 5: Report Results ---
            print(f"\nFINAL DECISION: [{final_decision.value}]")
            print("-"*20)
            print("Detailed Assessment Breakdown:")
            for result in detailed_results:
                # Only print checks that were not a simple PASS
                if result.decision != Decision.PASS:
                    print(f"  - Check: {result.check_name}")
                    print(f"    - Decision: {result.decision.value}")
                    print(f"    - Reason: {result.reason}")
                    if result.quote:
                        print(f"    - Quote: '{result.quote[:150]}...'") # Truncate long quotes

            # --- Step 6: Save Detailed Output ---
            output_data = {
                'opportunity_id': opp_id,
                'opportunity_title': opp_title,
                'final_decision': final_decision.value,
                'assessment_details': [res.__dict__ for res in detailed_results],
                'original_opportunity': opp # Save the original data for reference
            }

            file_path = os.path.join(OUTPUT_DIR, f"{opp_id}.json")
            with open(file_path, 'w') as f:
                json.dump(output_data, f, indent=4, default=str) # Use default=str for datetime objects
            logging.info(f"Detailed results saved to {file_path}")

    except Exception as e:
        logging.error(f"An unexpected error occurred in the main pipeline: {e}", exc_info=True)

    finally:
        logging.info("--- Pipeline execution finished. ---")


if __name__ == "__main__":
    main()
