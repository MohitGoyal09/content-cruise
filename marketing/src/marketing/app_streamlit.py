import streamlit as st
import os
import sys
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path
import base64
import logging

# Add the parent directory to the path to import the crew
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from crew import Marketing

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Streamlit page
st.set_page_config(
    page_title="AI Marketing Automation",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

def generate_campaign_name(topic, target_audience):
    """Generate a clean campaign name from topic and audience"""
    try:
        # Validate inputs
        if not topic or not topic.strip():
            topic = "marketing-campaign"
        if not target_audience or not target_audience.strip():
            target_audience = "general-audience"
        
        topic_clean = topic.strip().lower().replace(" ", "-").replace("'", "").replace("/", "-").replace("\\", "-")
        audience_words = target_audience.strip().split()
        audience_clean = audience_words[0].lower() if audience_words else "general"
        current_year = datetime.now().year
        campaign_name = f"{topic_clean}-{audience_clean}-{current_year}"
        
        #
        if not campaign_name or campaign_name in ["-", "--", "---"]:
            campaign_name = f"campaign-{current_year}-{int(time.time())}"
        
        return campaign_name
    except Exception as e:
        logger.error(f"Error generating campaign name: {str(e)}")
        # Fallback to timestamp-based name
        current_year = datetime.now().year
        return f"campaign-{current_year}-{int(time.time())}"

def create_directories(campaign_name):
    """Create output directories with dynamic campaign name"""
    try:
        # Validate campaign name
        if not campaign_name or campaign_name.strip() in ["", "None", "null"]:
            current_year = datetime.now().year
            campaign_name = f"fallback-campaign-{current_year}-{int(time.time())}"
            logger.warning(f"Invalid campaign name provided, using fallback: {campaign_name}")

        # Change to the marketing directory
        os.chdir(Path(__file__).parent.parent.parent)
        # Clean campaign name to avoid path issues
        clean_name = str(campaign_name).strip().replace("None", "fallback").replace("null", "fallback")
        base_dir = Path(f"content/{clean_name}")
        base_dir.mkdir(parents=True, exist_ok=True)
        # Create subdirectories
        subdirs = ["market_research", "blogs", "analysis", "social-media", "emails", "audio"]
        for subdir in subdirs:
            (base_dir / subdir).mkdir(exist_ok=True)

        logger.info(f"Created directories for campaign: {clean_name}")
        return clean_name
    except Exception as e:
        logger.error(f"Error creating directories: {str(e)}")
        # Fallback directory creation
        current_year = datetime.now().year
        fallback_name = f"error-recovery-{current_year}-{int(time.time())}"
        base_dir = Path(f"content/{fallback_name}")
        base_dir.mkdir(parents=True, exist_ok=True)
        return fallback_name

def run_campaign_thread(inputs, progress_bar, status_text, agent_text, task_text, progress_text, time_text):
    """Run the campaign in a separate thread to avoid blocking the UI"""
    try:
        # Validate and create directories
        validated_campaign_name = create_directories(inputs['campaign_name'])
        inputs['campaign_name'] = validated_campaign_name  # Update with validated name
        os.environ["CAMPAIGN_NAME"] = validated_campaign_name
        
        # Initialize crew
        crew_instance = Marketing()
        
        # Run the crew in a separate thread
        result = crew_instance.crew().kickoff(inputs=inputs)
        
        # Update UI when complete
        status_text.text("✅ Campaign completed successfully!")
        progress_bar.progress(100)
        
        return True, inputs['campaign_name']
        
    except Exception as e:
        logger.error(f"Campaign failed: {str(e)}", exc_info=True)
        status_text.error(f"❌ Campaign failed: {str(e)}")
        return False, None


    """Update the UI with progress information"""
    try:
        while True:
          
            
            # Update progress bar
            progress_bar.progress(progress)
            
            # Update status text
            if task_status == "completed":
                status_text.text(f"✅ Completed: {current_task}")
            elif task_status == "in_progress":
                status_text.text(f"🔄 In Progress: {current_task}")
            else:
                status_text.text(f"⏳ Pending: {current_task}")
                
            # Update agent text
            agent_text.text(f"👤 Current Agent: {current_agent}")
            
            # Update task text
            task_text.text(f"📋 Current Task: {current_task}")
            
            
            
            # Sleep for a short time before updating again
            time.sleep(1)
            
            # Exit if campaign is complete
            if progress >= 100:
                break
    except Exception as e:
        logger.error(f"Error updating progress UI: {str(e)}", exc_info=True)

def run_campaign(inputs):
    """Run the campaign and update progress"""
    try:
        # Initialize progress UI elements
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("🚀 Initializing campaign...")
        progress_bar.progress(10)
        
        validated_campaign_name = create_directories(inputs['campaign_name'])
        inputs['campaign_name'] = validated_campaign_name  # Update with validated name
        os.environ["CAMPAIGN_NAME"] = validated_campaign_name
        
        status_text.text("📊 Starting market research...")
        progress_bar.progress(20)
        
        # Initialize and run crew
        crew_instance = Marketing()
        
        status_text.text("✍️ Generating content...")
        progress_bar.progress(40)
        
        # Run the crew in a separate thread to avoid blocking
        with st.spinner("🤖 AI agents are working on your campaign..."):
            result = crew_instance.crew().kickoff(inputs=inputs)
        
        status_text.text("🎨 Finalizing content...")
        progress_bar.progress(90)
        
        time.sleep(1)  # Small delay for completion effect
        
        status_text.text("✅ Campaign completed successfully!")
        progress_bar.progress(100)
        
        return True, inputs['campaign_name']
        
        
    except Exception as e:
        logger.error(f"Campaign failed: {str(e)}", exc_info=True)
        st.error(f"❌ Campaign failed: {str(e)}")
        return False, None

def get_campaigns():
    """Get list of existing campaigns"""
    content_dir = Path('content')
    campaigns = []
    
    if content_dir.exists():
        for campaign_dir in content_dir.iterdir():
            if campaign_dir.is_dir():
                campaigns.append({
                    'name': campaign_dir.name,
                    'created': datetime.fromtimestamp(campaign_dir.stat().st_mtime).strftime('%Y-%m-%d %H:%M'),
                    'path': campaign_dir
                })
    
    return sorted(campaigns, key=lambda x: x['created'], reverse=True)

def load_campaign_content(campaign_name):
    """Load content from a campaign directory"""
    campaign_dir = Path(f'content/{campaign_name}')
    
    if not campaign_dir.exists():
        return None
    
    content = {}
    
    # Read all content files
    for subdir in ['market_research', 'blogs', 'analysis', 'social-media', 'emails', 'audio']:
        subdir_path = campaign_dir / subdir
        if subdir_path.exists():
            content[subdir] = {}
            for file_path in subdir_path.glob('*'):
                if file_path.is_file():
                    if file_path.suffix == '.md':
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content[subdir][file_path.name] = f.read()
                        except Exception as e:
                            content[subdir][file_path.name] = f"Error reading file: {str(e)}"
                    elif file_path.suffix == '.wav':
                        content[subdir][file_path.name] = file_path
    
    return content

def display_content_section(title, icon, content_dict, campaign_name, section_key):
    """Display a content section with files"""
    if not content_dict:
        return
    
    st.subheader(f"{icon} {title}")
    
    for filename, file_content in content_dict.items():
        with st.expander(f"📄 {filename}", expanded=False):
            if filename.endswith('.wav'):
                # Audio file
                st.audio(str(file_content))
                
                # Download button for audio
                with open(file_content, 'rb') as audio_file:
                    st.download_button(
                        label=f"📥 Download {filename}",
                        data=audio_file.read(),
                        file_name=filename,
                        mime="audio/wav",
                        key=f"download_{section_key}_{filename}"
                    )
            else:
                # Text content
                if isinstance(file_content, str) and len(file_content.strip()) > 0:
                    # Display content with markdown rendering
                    if file_content.strip() != "This file needs to be regenerated.":
                        st.markdown(file_content)
                    else:
                        st.warning("This file needs to be regenerated.")
                    
                    # Download button for text files
                    st.download_button(
                        label=f"📥 Download {filename}",
                        data=file_content,
                        file_name=filename,
                        mime="text/markdown",
                        key=f"download_{section_key}_{filename}"
                    )
                else:
                    st.warning("File is empty or could not be read.")

def main():
    """Main Streamlit application"""
    
    # Change to the marketing directory
    os.chdir(Path(__file__).parent.parent.parent)
    
    # Header
    st.title("🚀 AI Marketing Automation Dashboard")
    st.markdown("### Create comprehensive marketing campaigns with AI-powered content generation")
    st.divider()
    
    # Sidebar for campaign creation
    with st.sidebar:
        st.header("🎯 New Campaign")
        
        with st.form("campaign_form"):
            topic = st.text_input(
                "Campaign Topic",
                value="AI-powered marketing automation",
                help="What is your campaign about?"
            )
            
            target_audience = st.text_input(
                "Target Audience",
                value="small business owners aged 30-45",
                help="Who are you targeting?"
            )
            
            budget = st.number_input(
                "Budget ($)",
                value=75000,
                min_value=1000,
                step=1000,
                help="Campaign budget in USD"
            )
            
            duration_days = st.number_input(
                "Duration (Days)",
                value=45,
                min_value=7,
                max_value=365,
                help="Campaign duration"
            )
            
            brand_voice = st.text_area(
                "Brand Voice",
                value="professional yet approachable, data-driven and actionable",
                help="Describe your brand's tone and personality"
            )
            
            submitted = st.form_submit_button("🚀 Generate Campaign", use_container_width=True)
            
            if submitted:
                # Generate campaign
                start_date = datetime.now()
                end_date = start_date + timedelta(days=duration_days)
                campaign_name = generate_campaign_name(topic, target_audience)
                
                inputs = {
                    'topic': topic,
                    'campaign_name': campaign_name,
                    'target_audience': target_audience,
                    'brand_voice': brand_voice,
                    'budget': str(budget),
                    'start_date': start_date.strftime('%B %d, %Y'),
                    'end_date': end_date.strftime('%B %d, %Y')
                }
                
                st.session_state.generating = True
                st.session_state.current_campaign = campaign_name
                
                # Run campaign
                success, campaign_name = run_campaign(inputs)
                
                if success:
                    st.success(f"✅ Campaign '{campaign_name}' completed!")
                    st.session_state.generating = False
                    st.rerun()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.header("📁 Previous Campaigns")
        campaigns = get_campaigns()
        
        if campaigns:
            selected_campaign = st.selectbox(
                "Select a campaign to view:",
                options=[c['name'] for c in campaigns],
                format_func=lambda x: f"{x} ({next(c['created'] for c in campaigns if c['name'] == x)})",
                index=0 if 'current_campaign' not in st.session_state else 
                      ([c['name'] for c in campaigns].index(st.session_state.current_campaign) 
                       if st.session_state.current_campaign in [c['name'] for c in campaigns] else 0)
            )
            
            if st.button("🔍 View Campaign", use_container_width=True):
                st.session_state.selected_campaign = selected_campaign
        else:
            st.info("No campaigns yet. Create your first campaign!")
    
    with col1:
        st.header("📊 Campaign Content")
        
        # Display selected campaign content
        campaign_to_show = None
        if 'selected_campaign' in st.session_state:
            campaign_to_show = st.session_state.selected_campaign
        elif 'current_campaign' in st.session_state:
            campaign_to_show = st.session_state.current_campaign
        
        if campaign_to_show:
            content = load_campaign_content(campaign_to_show)
            
            if content:
                st.success(f"📂 Showing content for: **{campaign_to_show}**")
                
                # Content sections with icons and organization
                sections = {
                    'market_research': ('📈 Market Research', '📊'),
                    'blogs': ('📝 Blog Posts', '✍️'),
                    'analysis': ('🔍 Analysis', '📈'),
                    'social-media': ('📱 Social Media', '💬'),
                    'emails': ('📧 Email Marketing', '💌'),
                    'audio': ('🎵 Audio Slogans', '🔊')
                }
                
                # Create tabs for different content types
                tab_names = [sections[key][0] for key in sections.keys() if key in content and content[key]]
                
                if tab_names:
                    tabs = st.tabs(tab_names)
                    
                    tab_index = 0
                    for section_key, (title, icon) in sections.items():
                        if section_key in content and content[section_key]:
                            with tabs[tab_index]:
                                display_content_section(
                                    title, icon, content[section_key], 
                                    campaign_to_show, section_key
                                )
                            tab_index += 1
                else:
                    st.warning("No content found in this campaign. The campaign may still be generating or failed to complete.")
            else:
                st.error("Campaign not found or has no content.")
        else:
            st.info("👈 Select a campaign from the sidebar or create a new one to get started!")
    
    # Footer
    st.divider()
    st.markdown("*Built with ❤️ by Mohit*")

if __name__ == "__main__":
    main() 