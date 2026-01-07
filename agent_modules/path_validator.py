"""
Path validation utility for ensuring file access stays within allowed directories.
"""

import os
from typing import Tuple, Optional
from .exceptions import PathValidationError


class PathValidator:
    """Validates file paths to prevent path traversal attacks."""
    
    def __init__(self, allowed_directory: str):
        """
        Initialize path validator.
        
        Args:
            allowed_directory: The directory that all paths must be within
        """
        self.allowed_directory = os.path.realpath(allowed_directory)
        
        # Validate that allowed directory exists
        if not os.path.exists(self.allowed_directory):
            raise PathValidationError(f"Allowed directory does not exist: {self.allowed_directory}")
        if not os.path.isdir(self.allowed_directory):
            raise PathValidationError(f"Allowed directory is not a directory: {self.allowed_directory}")
    
    def validate(self, filepath: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Validate that a filepath is within the allowed directory.
        
        Args:
            filepath: The path to validate (can be relative or absolute)
            
        Returns:
            tuple: (is_valid: bool, normalized_path: str or None, error_message: str or None)
        """
        try:
            abs_allowed_dir = os.path.realpath(self.allowed_directory)
            
            # If filepath is relative, join it with allowed directory first
            if not os.path.isabs(filepath):
                filepath = os.path.join(self.allowed_directory, filepath)
            
            abs_filepath = os.path.realpath(filepath)
            
            # Check if the filepath is within the allowed directory
            try:
                common_path = os.path.commonpath([abs_allowed_dir, abs_filepath])
            except ValueError:
                # Different drives on Windows
                return False, None, f"Access denied: Path is outside allowed directory"
            
            if common_path != abs_allowed_dir:
                return False, None, f"Access denied: Path '{filepath}' is outside allowed directory '{self.allowed_directory}'"
            
            return True, abs_filepath, None
            
        except Exception as error:
            return False, None, f"Path validation error: {str(error)}"
    
    def validate_and_raise(self, filepath: str) -> str:
        """
        Validate path and raise exception if invalid.
        
        Args:
            filepath: The path to validate
            
        Returns:
            str: Normalized absolute path
            
        Raises:
            PathValidationError: If path is invalid
        """
        is_valid, normalized_path, error_msg = self.validate(filepath)
        if not is_valid:
            raise PathValidationError(error_msg or "Path validation failed")
        return normalized_path
