#!/usr/bin/env python
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

# Add the marketing directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "marketing"))

# Now import the Marketing class
from src.marketing.crew import Marketing

# Load environment variables
load_dotenv()

def main():
    """
    Main function to run the marketing workflow.
    """
    print("Starting marketing workflow...")
    
    # Define inputs for the marketing workflow
    inputs = {
        'topic': 'AI-powered marketing automation',
        'current_year': str(datetime.now().year),
        'brand_voice': 'professional yet conversational'
    }
    
    try:
        # Create and kickoff the marketing crew
        result = Marketing().crew().kickoff(inputs=inputs)
        print("\nWorkflow completed successfully!")
        print(f"Result: {result}")
        
    except Exception as e:
        print(f"An error occurred while running the marketing workflow: {e}")

if __name__ == "__main__":
    main()
