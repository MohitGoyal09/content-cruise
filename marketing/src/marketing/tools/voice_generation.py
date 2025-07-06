import os
import base64
import time
from sarvamai import SarvamAI
from pydantic import BaseModel
from crewai.tools import BaseTool
from typing import Type
from dotenv import load_dotenv

load_dotenv()


SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
if SARVAM_API_KEY:
    client = SarvamAI(api_subscription_key=SARVAM_API_KEY)
else:
    client = None

class VoiceGenerationToolInput(BaseModel):
    """Input for the voice generation tool."""
    text: str 
    language_code: str = "en-IN"  
    speaker: str = "anushka"  

class VoiceGenerationTool(BaseTool):
    name: str = "Voice Generation Tool"
    description: str = """Generate voice audio for text content. Use sparingly due to API costs.
    
    Valid language codes: 'bn-IN', 'en-IN', 'gu-IN', 'hi-IN', 'kn-IN', 'ml-IN', 'mr-IN', 'od-IN', 'pa-IN', 'ta-IN', 'te-IN'
    Valid speakers: 'meera', 'pavithra', 'maitreyi', 'arvind', 'amol', 'amartya', 'diya', 'neel', 'misha', 'vian', 'arjun', 'maya', 'anushka', 'abhilash', 'manisha', 'vidya', 'arya', 'karun', 'hitesh'
    """
    args_schema: Type[BaseModel] = VoiceGenerationToolInput

    def _run(self, text: str, language_code: str = "hi-IN", speaker: str = "amol") -> str:
        """Generate a voice for the given text with simple rate limiting."""
        
        print(f"🎵 Voice Generation Request: '{text}' in {language_code} with speaker {speaker}")
        
        # Force Hindi language for slogans
        if language_code != "hi-IN":
            language_code = "hi-IN"
            print(f"⚠️ Forcing Hindi language for audio generation: {language_code}")
            
        valid_language_codes = ['bn-IN', 'en-IN', 'gu-IN', 'hi-IN', 'kn-IN', 'ml-IN', 'mr-IN', 'od-IN', 'pa-IN', 'ta-IN', 'te-IN']
        valid_speakers = ['meera', 'pavithra', 'maitreyi', 'arvind', 'amol', 'amartya', 'diya', 'neel', 'misha', 'vian', 'arjun', 'maya', 'anushka', 'abhilash', 'manisha', 'vidya', 'arya', 'karun', 'hitesh']
        
        if language_code not in valid_language_codes:
            language_code = "hi-IN"  
            print(f"Warning: Invalid language_code provided. Using default: {language_code}")
            
        if speaker not in valid_speakers:
            speaker = "anushka"  
            print(f"Warning: Invalid speaker provided. Using default: {speaker}")
        
        print(f"🎵 Final audio settings: Language={language_code}, Speaker={speaker}")
        
        time.sleep(5)
        
        #
        if not SARVAM_API_KEY:
            return f"""
ERROR: Voice generation failed - SARVAM_API_KEY not found.

Get your API key at: https://sarvam.ai/
Set it as: export SARVAM_API_KEY=your_key_here

Text for manual processing: "{text}"
"""
        
        if not client:
            return f"Voice generation unavailable. Text: '{text}'"
        
        # Limit text length
        if len(text) > 200:
            text = text[:200] + "..."
            
        try:
            print(f"🎵 Generating voice for: '{text[:50]}...'")
            
            # Updated API call for SARVAM - correct method signature
            resp = client.text_to_speech.convert(
                text=text,
                target_language_code=language_code,
                speaker=speaker,
                model="bulbul:v2",
                enable_preprocessing=True
            )
            
            # API response is working correctly
            
            # Access response attributes properly for SARVAM API
            audio_data = None
            if hasattr(resp, 'audios') and resp.audios:
                audio_data = resp.audios[0]
            elif hasattr(resp, 'audio') and resp.audio:
                audio_data = resp.audio
            elif hasattr(resp, 'data') and resp.data:
                audio_data = resp.data
            
            if not audio_data:
                return f"Voice generation failed - no audio data found. Response type: {type(resp)}. Text: '{text}'"
            
            # Decode the audio data
            decoded_audio = base64.b64decode(audio_data)
            
          
            safe_text = "".join(c for c in text[:20] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_text = safe_text.replace(' ', '_')
            filename = f"audio_{safe_text}.wav"
            
          
            # Get campaign name with validation
            campaign_name = os.getenv("CAMPAIGN_NAME")
            if not campaign_name or campaign_name.strip() in ["", "None", "null"]:
                from datetime import datetime
                current_year = datetime.now().year
                campaign_name = f"auto-voice-campaign-{current_year}-{int(time.time())}"
                os.environ["CAMPAIGN_NAME"] = campaign_name
                print(f"⚠️ Fixed invalid campaign name for audio, using: {campaign_name}")
            
            audio_dir = f"content/{campaign_name}/audio"
            os.makedirs(audio_dir, exist_ok=True)
            
            filepath = os.path.join(audio_dir, filename)
            
            with open(filepath, "wb") as f:
                f.write(decoded_audio)
                
            return f"✅ Voice audio generated: {filepath}\nText: '{text}'"
            
        except Exception as e:
            error_msg = str(e)
            
            if any(term in error_msg.lower() for term in ['rate limit', 'quota', '429']):
                return f"⚠️ Rate limit error - wait 10 minutes and try again. Text: '{text}'"
            else:
                return f"❌ Voice generation failed: {error_msg}. Text: '{text}'"
    