#!/usr/bin/env python
import sys
import warnings
import os
import agentops
from datetime import datetime, timedelta
from crew import Marketing

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

agentops.init()

def get_dynamic_campaign_dates():
    """Generate dynamic campaign dates based on current date"""
    today = datetime.now()
    
    # Campaign starts next month or immediately if it's end of month
    if today.day > 25:  # If late in month, start next month
        campaign_start = today.replace(day=1) + timedelta(days=32)
        campaign_start = campaign_start.replace(day=1)
    else:  # Start from next week
        campaign_start = today + timedelta(days=7)
    
    # Campaign runs for 3 months
    campaign_end = campaign_start + timedelta(days=90)
    
    # Generate campaign name based on quarter
    quarter = (campaign_start.month - 1) // 3 + 1
    campaign_name = f"Q{quarter} {campaign_start.year} AI Marketing Campaign"
    
    return {
        'current_year': str(today.year),
        'current_date': today.strftime('%Y-%m-%d'),
        'campaign_name': campaign_name,
        'start_date': campaign_start.strftime('%Y-%m-%d'),
        'end_date': campaign_end.strftime('%Y-%m-%d')
    }

def run():
    """
    Run the crew with dynamic date handling.
    """
    # Get dynamic dates
    date_info = get_dynamic_campaign_dates()
    
    inputs = {
        **date_info,  # Spread dynamic date info
        'budget': 5000,
        'channels': ['email', 'social', 'web'],
        'target_audience': 'young professionals',
        'topic': 'AI-powered marketing automation',
        'brand_voice': 'professional yet conversational'
    }
    
    print(f"🗓️  Campaign Info:")
    print(f"   Current Date: {date_info['current_date']}")
    print(f"   Campaign: {date_info['campaign_name']}")
    print(f"   Duration: {date_info['start_date']} → {date_info['end_date']}")
    print(f"   Target: {inputs['target_audience']}")
    print(f"   Topic: {inputs['topic']}\n")
    
    try:
        Marketing().crew().kickoff(inputs=inputs)
        print("✅ Workflow completed successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🔧 To fix this:")
        print("1. Get a Google Gemini API key from https://aistudio.google.com/app/apikey")
        print("2. Set it as environment variable: GOOGLE_API_KEY=your-actual-key")
        print("3. Get a Serper API key from https://serper.dev/ for web search")
        print("4. Set it as environment variable: SERPER_API_KEY=your-serper-key")
        print("5. Install dependencies: uv sync")
        raise Exception(f"An error occurred while running the crew: {e}")


if __name__ == "__main__":
    run()