import sys
import os
import time
import logging
from pathlib import Path
from datetime import datetime, timedelta


sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from crew import Marketing


logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                   handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)

def simple_rate_limit_delay():
    """Simple delay to prevent rate limiting"""
    time.sleep(5)  

def generate_campaign_name(topic, target_audience):
    """Generate a clean campaign name from topic and audience"""
    # Create URL-friendly campaign name
    topic_clean = topic.lower().replace(" ", "-").replace("'", "")
    audience_clean = target_audience.split()[0].lower()  
    current_year = datetime.now().year
    
    campaign_name = f"{topic_clean}-{audience_clean}-{current_year}"
    return campaign_name

def create_directories(campaign_name):
    """Create output directories with dynamic campaign name"""
   
    os.chdir(Path(__file__).parent.parent.parent)
    
    base_dir = Path(f"content/{campaign_name}")
    base_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ Created campaign directory: {base_dir}")
    
   
    subdirs = [
        "market_research",  
        "blogs",          
        "analysis",       
        "social-media",    
        "emails",         
        "audio"            
    ]
    for subdir in subdirs:
        (base_dir / subdir).mkdir(exist_ok=True)
    print(f"✅ Created subdirectories: {', '.join(subdirs)}")
    
    # Create placeholder files for market research to ensure they exist
    market_research_dir = base_dir / "market_research"
    expected_files = ["competitors.md", "keywords.md", "audience.md"]
    
    for file in expected_files:
        file_path = market_research_dir / file
        if not file_path.exists():
            with open(file_path, "w") as f:
                f.write(f"# {file.replace('.md', '').title()} Research\n\n")
                f.write("This file will be populated by the market research task.\n")
            print(f"✅ Created placeholder file: {file_path}")
    
    return campaign_name

def verify_content_generation(campaign_name):
    """Verify that all required content was generated"""
    base_dir = Path(f"content/{campaign_name}")
    
    # Define expected files for each directory
    expected_files = {
        "market_research": ["competitors.md", "keywords.md", "audience.md"],
        "blogs": ["ai-marketing-guide.md"],
        "analysis": ["quick-improvements.md"],
        "social-media": ["posts.md"],
        "emails": ["email-sequence.md"],
        "audio": ["slogans.md"]
    }
    
    missing_files = []
    
    # Check each directory for expected files
    for subdir, files in expected_files.items():
        dir_path = base_dir / subdir
        if not dir_path.exists():
            dir_path.mkdir(exist_ok=True)
            print(f"⚠️ Created missing directory: {dir_path}")
        
        for file in files:
            file_path = dir_path / file
            if not file_path.exists() or os.path.getsize(file_path) == 0:
                missing_files.append(f"{subdir}/{file}")
                
                # Create placeholder for missing file
                with open(file_path, "w") as f:
                    f.write(f"# {file.replace('.md', '').title()}\n\n")
                    f.write("This file needs to be regenerated.\n")
                print(f"⚠️ Created placeholder for missing file: {file_path}")
    
    if missing_files:
        print(f"⚠️ Warning: The following files were missing or empty and replaced with placeholders:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    else:
        print("✅ All expected content files were generated successfully!")
        return True

def get_campaign_inputs():
    """Get predefined example campaign inputs for testing"""
    print("\n🎯 Campaign Configuration (Example Values)")
    print("=" * 40)
    
  
    topic = "AI-powered marketing automation"
    target_audience = "small business owners aged 30-45"
    brand_voice = "professional yet approachable, data-driven and actionable"
    budget = "75000"
    duration_days = 45  
    
    start_date = datetime.now()
    end_date = start_date + timedelta(days=duration_days)
    
    campaign_name = generate_campaign_name(topic, target_audience)
    
    print(f"\n✅ Using Example Campaign Configuration:")
    print(f"   📝 Topic: {topic}")
    print(f"   👥 Audience: {target_audience}")
    print(f"   🎨 Brand Voice: {brand_voice}")
    print(f"   💰 Budget: ${budget}")
    print(f"   📅 Start Date: {start_date.strftime('%B %d, %Y')}")
    print(f"   📅 End Date: {end_date.strftime('%B %d, %Y')}")
    print(f"   📁 Campaign Name: {campaign_name}")
    
    return {
        'topic': topic,
        'campaign_name': campaign_name,
        'target_audience': target_audience,
        'brand_voice': brand_voice,
        'budget': budget,
        'start_date': start_date.strftime('%B %d, %Y'),
        'end_date': end_date.strftime('%B %d, %Y')
    }

def main():
    """SPEED-OPTIMIZED workflow with minimal thinking overhead"""
    print("⚡ AI Marketing Content Creation - SPEED-OPTIMIZED WORKFLOW")
    print("🚀 Direct Execution → 📊 Research → 📝 Create → 🔍 Analyze → 📱 Social → 🎵 Audio")
    print("⚡ Zero Thinking Overhead | 🎯 Target: <$0.75, ~8 min | 🧠 Mistral + Gemini")
    print("=" * 80)
    
    # Get campaign inputs from user
    inputs = get_campaign_inputs()
    
    # Create directories with dynamic campaign name
    create_directories(inputs['campaign_name'])
    
    # Set campaign name as environment variable for tools to use
    os.environ["CAMPAIGN_NAME"] = inputs['campaign_name']
    
    try:
        print("\n🚀 Starting SPEED-OPTIMIZED campaign...")
        
        # Minimal delay for speed
        print("⏳ Quick initialization...")
        time.sleep(1)  # Reduced from 5 seconds to 1 second
        
        # Initialize crew
        crew_instance = Marketing()
        
        # Run campaign
        result = crew_instance.crew().kickoff(inputs=inputs)
        
        # Verify all content was generated
        all_content_generated = verify_content_generation(inputs['campaign_name'])
        
        if all_content_generated:
            print("🎉 Campaign completed successfully with ALL required content!")
        else:
            print("⚠️ Campaign completed but some content may be missing or incomplete.")
            print("   Please check the placeholder files and consider regenerating.")
        
        print(f"Check the 'content/{inputs['campaign_name']}/' directory for results.")
        
       
        content_dir = Path(f"content/{inputs['campaign_name']}")
        if content_dir.exists():
            print(f"\n📁 Created files in {content_dir}:")
            for file_path in content_dir.rglob("*"):
                if file_path.is_file():
                    print(f"  - {file_path}")
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Campaign failed: {error_msg}", exc_info=True)
        print(f"❌ Campaign failed: {e}")
        
        if 'timeout' in error_msg.lower() or 'timed out' in error_msg.lower():
            print("🔧 TIMEOUT ERROR: API request timed out")
            print("💡 Solutions:")
            print("   1. Check your internet connection")
            print("   2. Try running again (network issues are often temporary)")
            print("   3. Check API service status at status pages")
            print("   4. Reduce max_tokens if the issue persists")
        elif 'rate limit' in error_msg.lower() or '429' in error_msg:
            print("🔧 Solution: Wait 10 minutes and try again")
        elif 'api key' in error_msg.lower() or 'credentials' in error_msg.lower():
            print("🔧 Solution: Check your API keys (GOOGLE_API_KEY, MISTRAL_API_KEY)")
        elif 'quota' in error_msg.lower():
            print("🔧 Solution: Check your API quotas and billing")
        else:
            print("🔧 Solution: Check your configuration")
            print(f"   Full error: {error_msg}")
            
        # Show any partial results and create placeholders for missing content
        print("\n⚠️ Attempting to recover and create placeholders for missing content...")
        verify_content_generation(inputs['campaign_name'])
        
        # Show partial results
        content_dir = Path(f"content/{inputs['campaign_name']}")
        if content_dir.exists():
            print(f"\n📁 Partial results saved in {content_dir}:")
            for file_path in content_dir.rglob("*"):
                if file_path.is_file():
                    print(f"  - {file_path}")

if __name__ == "__main__":
    main()