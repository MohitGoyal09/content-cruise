import os
from typing import Type, Optional, Union
from pydantic import BaseModel, Field, field_validator
from crewai.tools import BaseTool

class FixedFileReadToolInput(BaseModel):
    """Input for the fixed file read tool with proper parameter handling."""
    file_path: str = Field(..., description="Full path to the file to read")
    start_line: Optional[int] = Field(default=None, description="Line number to start reading from (1-indexed)")
    line_count: Optional[int] = Field(default=None, description="Number of lines to read. If None, reads entire file")
    
    @field_validator('start_line', mode='before')
    @classmethod
    def validate_start_line(cls, v):
        if v is None or v == "None" or v == "null":
            return None
        try:
            return int(v) if v is not None else None
        except (ValueError, TypeError):
            return None
    
    @field_validator('line_count', mode='before') 
    @classmethod
    def validate_line_count(cls, v):
        if v is None or v == "None" or v == "null":
            return None
        try:
            return int(v) if v is not None else None
        except (ValueError, TypeError):
            return None

class FixedFileReadTool(BaseTool):
    name: str = "Read a file's content"
    description: str = """
    Read the content of a file. Provide 'file_path' parameter with the path to the file.
    Optionally provide 'start_line' to start from a specific line and 'line_count' to limit lines read.
    If line_count is not provided or None, reads the entire file.
    """
    args_schema: Type[BaseModel] = FixedFileReadToolInput

    def _run(self, file_path: str, start_line: Optional[int] = None, line_count: Optional[int] = None) -> str:
        """Read file content with proper parameter handling."""
        try:
            # Resolve relative paths
            if not os.path.isabs(file_path):
                file_path = os.path.join(os.getcwd(), file_path)
            
            if not os.path.exists(file_path):
                return f"Error: File '{file_path}' not found."
            
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            # Handle start_line (convert to 0-based indexing)
            start_idx = (start_line - 1) if start_line is not None and start_line > 0 else 0
            start_idx = max(0, start_idx)  # Ensure non-negative
            
            # Handle line_count
            if line_count is not None and line_count > 0:
                end_idx = start_idx + line_count
                selected_lines = lines[start_idx:end_idx]
            else:
                # Read from start_idx to end of file
                selected_lines = lines[start_idx:]
            
            content = ''.join(selected_lines)
            
            # Provide informative response
            total_lines = len(lines)
            lines_read = len(selected_lines)
            
            if not content.strip():
                return f"File '{file_path}' is empty or selected range contains no content.\nTotal file lines: {total_lines}"
            
            return f"Content from '{file_path}' (lines {start_idx + 1}-{start_idx + lines_read} of {total_lines}):\n\n{content}"
            
        except UnicodeDecodeError:
            return f"Error: Could not read file '{file_path}' - file appears to be binary or uses unsupported encoding."
        except PermissionError:
            return f"Error: Permission denied reading file '{file_path}'."
        except Exception as e:
            return f"Error reading file '{file_path}': {str(e)}" 