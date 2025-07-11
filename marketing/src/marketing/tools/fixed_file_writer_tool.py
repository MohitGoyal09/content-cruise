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

    def _validate_file_placement(self, file_path: str) -> None:
        """Validate file placement to prevent common path errors."""
        # Common error patterns to catch and prevent
        critical_errors = []
        
        # Error 1: posts_v1.md in blogs folder instead of social-media
        if "posts_v1.md" in file_path and "/blogs/" in file_path:
            critical_errors.append("ERROR: posts_v1.md MUST be in social-media folder, NOT blogs folder!")
        
        # Error 2: posts_final.md in blogs folder instead of social-media
        if "posts_final.md" in file_path and "/blogs/" in file_path:
            critical_errors.append("ERROR: posts_final.md MUST be in social-media folder, NOT blogs folder!")
        
        # Error 3: Final files in root campaign directory instead of subfolders
        if ("posts_final.md" in file_path or "email-sequence_final.md" in file_path):
            # Check if file is in root directory (has campaign name but no subfolder)
            if file_path.count("/") == 2 and file_path.endswith((".md", ".txt")):
                critical_errors.append("ERROR: Final files MUST be in subfolders (social-media/, emails/), NOT root directory!")
        
        # Error 4: email files in wrong folder
        if "email-sequence" in file_path and not "/emails/" in file_path:
            critical_errors.append("ERROR: Email sequence files MUST be in emails folder!")
        
        # Error 5: Social media files in wrong folder
        if ("posts_v1.md" in file_path or "posts_final.md" in file_path) and not "/social-media/" in file_path:
            critical_errors.append("ERROR: Social media posts MUST be in social-media folder!")
        
        # If any critical errors found, log but don't raise exception (allow with warning)
        if critical_errors:
            error_message = "\n".join(critical_errors)
            print(f"⚠️ FILE PLACEMENT WARNING:\n{error_message}")
            print(f"⚠️ Attempting to fix path automatically...")
            # Don't raise exception, let the path fixing logic handle it
        else:
            print(f"✅ File placement validation passed for: {file_path}")

    def _validate_and_fix_campaign_name(self, file_path: str) -> str:
        """Validate and fix campaign name in file path."""
        print(f"📝 Original file_path: {file_path}")
        
        # CRITICAL: Validate file placement to prevent common errors
        self._validate_file_placement(file_path)
        
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
            elif "analysis" in file_path.lower() or "feedback" in file_path.lower() or "optimization" in file_path.lower():
                subdir = "analysis"
            elif "posts_v1" in file_path.lower() or "posts_final" in file_path.lower() or "social" in file_path.lower():
                subdir = "social-media"
            elif "email-sequence" in file_path.lower() or "email" in file_path.lower():
                subdir = "emails"
            elif ("blog" in file_path.lower() or "guide" in file_path.lower() or "ai-marketing-guide" in file_path.lower()) and "social" not in file_path.lower():
                subdir = "blogs"
            elif "audio" in file_path.lower() or "slogan" in file_path.lower():
                subdir = "audio"
            else:
                subdir = "misc"
                
            original_filename = os.path.basename(file_path)
            
            # Special handling for incorrect blog post names
            if "blog_post.md" in file_path.lower():
                print(f"⚠️ WARNING: Incorrect blog filename detected: {file_path}")
                print(f"⚠️ Converting 'blog_post.md' to 'ai-marketing-guide.md' in blogs folder")
                original_filename = "ai-marketing-guide.md"
                subdir = "blogs"
            file_path = f"content/{campaign_name}/{subdir}/{original_filename}"
            print(f"⚠️ Reconstructed path from simple filename: {file_path}")
        
        # Additional fix: Handle special characters in campaign names that cause path issues
        # Only apply character cleaning to the campaign name part, not the entire path
        path_parts = file_path.split('/')
        
        # Clean only non-path parts (avoid breaking Windows drive letters and path separators)
        if len(path_parts) > 2:  # Only clean campaign names and filenames, not full paths
            for i, part in enumerate(path_parts):
                if i > 0 and part and not part.endswith(':'):  # Skip drive letters and first part
                    # Replace problematic characters only in campaign/folder names
                    part = part.replace("(", "").replace(")", "")
                    part = re.sub(r"[<>\"|?*]", "", part)  # Remove invalid filename characters (keep : for Windows drives)
                    part = re.sub(r"\s+", "-", part)  # Replace spaces with hyphens
                    part = re.sub(r"-+", "-", part)  # Replace multiple hyphens with single
                    path_parts[i] = part
            
            file_path = '/'.join(path_parts)
        
        file_path = re.sub(r"/+", "/", file_path)  # Fix double slashes
        
        print(f"📝 Final file_path: {file_path}")
        return file_path

    def _run(self, file_path: str, content: str, overwrite: bool = True) -> str:
        """Write content to file with campaign name validation."""
        try:
            # Fix campaign name in file path
            original_path = file_path
            file_path = self._validate_and_fix_campaign_name(file_path)
            
            print(f"🔧 Path transformation: '{original_path}' -> '{file_path}'")
            
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
            
            print(f"📍 Final absolute path: {file_path}")
            
            # Create directory structure if it doesn't exist
            directory = os.path.dirname(file_path)
            print(f"📂 Creating directory: {directory}")
            
            try:
                Path(directory).mkdir(parents=True, exist_ok=True)
                print(f"✅ Directory created successfully: {directory}")
            except Exception as dir_error:
                print(f"❌ Error creating directory {directory}: {str(dir_error)}")
                return f"❌ Error creating directory '{directory}': {str(dir_error)}"
            
            # Check if file exists and handle overwrite
            if os.path.exists(file_path) and not overwrite:
                return f"File '{file_path}' already exists and overwrite is disabled."
            
            # Validate content
            if not content or content.strip() == "":
                print(f"⚠️ Warning: Empty content for file '{file_path}'")
                content = "# Content not available\n\nThis file was created but no content was provided."
            
            # Write content to file
            print(f"📝 Writing {len(content)} characters to file...")
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            
            # Verify file was created successfully
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                print(f"✅ File verification passed: {file_path} ({file_size} bytes)")
                return f"✅ Successfully wrote {file_size} bytes to '{file_path}'"
            else:
                print(f"❌ File verification failed: {file_path}")
                return f"❌ Failed to create file '{file_path}'"
                
        except PermissionError as e:
            error_msg = f"❌ Permission denied writing to '{file_path}': {str(e)}"
            print(error_msg)
            return error_msg
        except FileNotFoundError as e:
            error_msg = f"❌ Directory path invalid for '{file_path}': {str(e)}"
            print(error_msg)
            return error_msg
        except Exception as e:
            error_msg = f"❌ Error writing file '{file_path}': {str(e)}"
            print(error_msg)
            return error_msg 