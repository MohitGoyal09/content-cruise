# 🚀 AI Marketing Automation - Streamlit Dashboard

A modern, polished web interface for your AI-powered marketing automation system. Built with **Streamlit** for rapid development and beautiful UX.

## ✨ Features

### 🎯 Campaign Creation
- **Interactive Form**: Easy-to-use sidebar form for campaign parameters
- **Real-time Validation**: Input validation and helpful tooltips
- **Smart Defaults**: Pre-filled with example values for quick testing

### 📊 Progress Tracking
- **Live Progress Bar**: Real-time updates during campaign generation
- **Status Messages**: Clear feedback on what's happening
- **Visual Spinner**: Beautiful loading animations

### 📁 Content Management
- **Campaign Library**: Browse all previous campaigns
- **Organized Tabs**: Content organized by type (research, blogs, social media, etc.)
- **File Downloads**: One-click download for all generated content
- **Audio Playback**: Built-in audio player for voice slogans

### 🎨 Modern UI
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Beautiful Icons**: Intuitive visual indicators
- **Clean Layout**: Professional, easy-to-navigate interface
- **Real-time Updates**: Automatic refresh when campaigns complete

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd marketing
pip install -r requirements.txt
```

### 2. Start the Dashboard
```bash
# Option 1: Use the launcher script
python run_streamlit.py

# Option 2: Direct streamlit command
streamlit run streamlit_dashboard.py --server.port 8501
```

### 3. Open in Browser
Navigate to: **http://localhost:8501**

## 📱 How to Use

### Creating a New Campaign

1. **Fill in the form** in the left sidebar:
   - **Campaign Topic**: What your campaign is about
   - **Target Audience**: Who you're targeting
   - **Budget**: Campaign budget in USD
   - **Duration**: How long the campaign will run
   - **Brand Voice**: Your brand's tone and personality

2. **Click "🚀 Generate Campaign"**

3. **Watch the progress** as AI agents create your content:
   - Market research
   - Blog posts
   - Social media content
   - Email sequences
   - Audio slogans

### Viewing Campaign Content

1. **Select a campaign** from the dropdown in the right column
2. **Click "🔍 View Campaign"**
3. **Browse content** using the organized tabs:
   - 📊 **Market Research**: Competitor analysis, keywords, audience insights
   - ✍️ **Blog Posts**: Full articles ready for publishing
   - 📈 **Analysis**: Performance recommendations
   - 💬 **Social Media**: Posts for LinkedIn, Twitter, Instagram
   - 💌 **Email Marketing**: Complete email sequences
   - 🔊 **Audio Slogans**: Voice-generated marketing slogans

### Downloading Content

- **Individual Files**: Click "📥 Download" button next to any file
- **Audio Files**: Play directly in browser or download
- **Text Files**: Preview with markdown formatting, then download

## 🔊 Audio Features

The dashboard includes built-in audio playback for voice slogans:
- **Play Button**: Click to play audio directly in browser
- **Download**: Save audio files to your computer
- **Format**: High-quality WAV files

## ⚡ Why Streamlit?

**Streamlit was chosen over Flask for rapid development:**

| Feature | Streamlit | Flask |
|---------|-----------|-------|
| **Development Speed** | ⚡ 10x faster | ⏱️ Slower |
| **Built-in Components** | ✅ Forms, file downloads, audio players | ❌ Manual HTML/CSS/JS |
| **Responsive Design** | ✅ Automatic | ❌ Manual |
| **State Management** | ✅ Built-in | ❌ Manual sessions |
| **Real-time Updates** | ✅ Automatic | ❌ Manual JavaScript |

## 🛠️ Technical Details

### Architecture
```
marketing/
├── streamlit_dashboard.py     # Main Streamlit app
├── run_streamlit.py          # Quick launcher
├── requirements.txt          # Dependencies
├── src/marketing/            # CrewAI backend
│   ├── crew.py              # AI agents and tasks
│   ├── config/              # Agent and task configurations
│   └── tools/               # Custom tools
└── content/                 # Generated campaign content
    └── {campaign-name}/     # Individual campaign folders
        ├── market_research/
        ├── blogs/
        ├── social-media/
        ├── emails/
        └── audio/
```

### Key Functions
- **`run_campaign()`**: Executes the CrewAI workflow with progress tracking
- **`load_campaign_content()`**: Reads and displays generated content
- **`display_content_section()`**: Renders content with download buttons
- **`get_campaigns()`**: Lists all available campaigns

## 🎨 UI Components

### Sidebar Form
- Text inputs for campaign parameters
- Number inputs with validation
- Text area for brand voice
- Submit button with full-width styling

### Main Content Area
- **Two-column layout**: Content display + Campaign selector
- **Tabbed interface**: Organized by content type
- **Expandable sections**: Click to view file contents
- **Download buttons**: One-click file downloads

### Progress Tracking
- **Progress bar**: Visual completion indicator
- **Status text**: Current operation description
- **Spinner**: Loading animation during generation

## 🚀 Next Steps

The dashboard is ready to use! You can:

1. **Test with existing campaigns** in the `content/` folder
2. **Generate new campaigns** using the form
3. **Customize the UI** by modifying `streamlit_dashboard.py`
4. **Add new features** like campaign comparison or analytics

---

**Built with ❤️ using Streamlit and CrewAI** 