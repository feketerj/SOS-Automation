"""
Quick URL Update Script
Use this to easily update the daily endpoint URL
"""

import os
from pathlib import Path

def update_daily_url():
    """Update the daily endpoint URL in .env file"""
    print("SOS Daily Endpoint URL Updater")
    print("=" * 40)
    print("Current .env file content:")
    
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            content = f.read()
            print(content)
    else:
        print("No .env file found")
        return
    
    print("\nPaste the new daily URL here:")
    print("(Example: https://www.highergov.com/api-external/opportunity/?saved_search=ABC123XYZ)")
    new_url = input("New URL: ").strip()
    
    if not new_url:
        print("No URL provided. Exiting.")
        return
    
    # Read current content
    lines = []
    with open(env_file, 'r') as f:
        lines = f.readlines()
    
    # Update or add the URL line
    updated = False
    for i, line in enumerate(lines):
        if line.startswith('DAILY_ENDPOINT_URL='):
            lines[i] = f'DAILY_ENDPOINT_URL={new_url}\n'
            updated = True
            break
    
    if not updated:
        lines.append(f'DAILY_ENDPOINT_URL={new_url}\n')
    
    # Write back to file
    with open(env_file, 'w') as f:
        f.writelines(lines)
    
    print(f"\n✅ Updated .env file with new URL:")
    print(f"DAILY_ENDPOINT_URL={new_url}")
    print("\nYou can now run the main pipeline!")

if __name__ == "__main__":
    update_daily_url()
