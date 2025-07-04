import os
import re
from datetime import datetime
from typing import Type, Optional
from pathlib import Path
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class FixedFileWriterToolInput(BaseModel):
    """Input for the fixed file writer tool with campaign name validation."""
    file_path: str = Field(..., description="Path to the file to write")
    content: str = Field(..., description="Content to write to the file")
    overwrite: bool = Field(default=True, description="Whether to overwrite if file exists")

class FixedFileWriterTool(BaseTool):
    name: str = "File Writer Tool"
    description: str = """
    Write content to a file with automatic campaign name validation and correction.
    Automatically fixes 'None' campaign names and ensures proper directory structure.
    """
    args_schema: Type[BaseModel] = FixedFileWriterToolInput

    def _validate_and_fix_campaign_name(self, file_path: str) -> str:
        """Validate and fix campaign name in file path."""
        print(f"📝 Original file_path: {file_path}")
        
        # Check if path contains None, null, or empty campaign name
        if "/None/" in file_path or "/null/" in file_path or "//" in file_path:
            # Get campaign name from environment or generate fallback
            campaign_name = os.getenv("CAMPAIGN_NAME")
            
            if not campaign_name or campaign_name.strip() in ["", "None", "null"]:
                # Generate fallback campaign name
                current_year = datetime.now().year
                timestamp = int(datetime.now().timestamp())
                campaign_name = f"auto-campaign-{current_year}-{timestamp}"
                
                # Update environment variable
                os.environ["CAMPAIGN_NAME"] = campaign_name
                print(f"⚠️ Fixed invalid campaign name, using: {campaign_name}")
            
            # Replace problematic parts in path
            file_path = file_path.replace("/None/", f"/{campaign_name}/")
            file_path = file_path.replace("/null/", f"/{campaign_name}/")
            file_path = re.sub(r"/+", "/", file_path)  # Fix double slashes
            
            print(f"📝 Fixed file_path: {file_path}")
        
        # Additional validation: ensure path starts with content/ structure
        if not file_path.startswith("content/") and "content/" not in file_path:
            # This might be a simple filename without proper structure
            campaign_name = os.getenv("CAMPAIGN_NAME")
            if not campaign_name or campaign_name.strip() in ["", "None", "null"]:
                current_year = datetime.now().year
                timestamp = int(datetime.now().timestamp())
                campaign_name = f"auto-campaign-{current_year}-{timestamp}"
                os.environ["CAMPAIGN_NAME"] = campaign_name
            
            # Determine appropriate subdirectory based on filename
            if "competitors" in file_path.lower() or "keywords" in file_path.lower() or "audience" in file_path.lower():
                subdir = "market_research"
            elif "blog" in file_path.lower() or "post" in file_path.lower():
                subdir = "blogs"
            elif "social" in file_path.lower() or "posts" in file_path.lower():
                subdir = "social-media"
            elif "email" in file_path.lower():
                subdir = "emails"
            elif "audio" in file_path.lower() or "slogan" in file_path.lower():
                subdir = "audio"
            elif "analysis" in file_path.lower():
                subdir = "analysis"
            else:
                subdir = "misc"
            
            original_filename = os.path.basename(file_path)
            file_path = f"content/{campaign_name}/{subdir}/{original_filename}"
            print(f"⚠️ Reconstructed path from simple filename: {file_path}")
        
        print(f"📝 Final file_path: {file_path}")
        return file_path

    def _run(self, file_path: str, content: str, overwrite: bool = True) -> str:
        """Write content to file with campaign name validation."""
        try:
            # Fix campaign name in file path
            file_path = self._validate_and_fix_campaign_name(file_path)
            
            # Ensure we're in the marketing directory
            current_dir = os.getcwd()
            if not current_dir.endswith("marketing"):
                # Find marketing directory
                marketing_path = None
                for root, dirs, files in os.walk("."):
                    if "marketing" in dirs and "src" in os.listdir(os.path.join(root, "marketing")):
                        marketing_path = os.path.join(root, "marketing")
                        break
                
                if marketing_path:
                    os.chdir(marketing_path)
                    print(f"📁 Changed to marketing directory: {os.getcwd()}")
            
            # Convert relative path to absolute
            if not os.path.isabs(file_path):
                file_path = os.path.join(os.getcwd(), file_path)
            
            # Create directory structure if it doesn't exist
            directory = os.path.dirname(file_path)
            Path(directory).mkdir(parents=True, exist_ok=True)
            
            # Check if file exists and handle overwrite
            if os.path.exists(file_path) and not overwrite:
                return f"File '{file_path}' already exists and overwrite is disabled."
            
            # Write content to file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            
            # Verify file was created successfully
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                return f"✅ Successfully wrote {file_size} bytes to '{file_path}'"
            else:
                return f"❌ Failed to create file '{file_path}'"
                
        except PermissionError:
            return f"❌ Permission denied writing to '{file_path}'"
        except FileNotFoundError:
            return f"❌ Directory path invalid for '{file_path}'"
        except Exception as e:
            return f"❌ Error writing file '{file_path}': {str(e)}" 