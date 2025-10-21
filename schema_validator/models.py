"""
Database models for Schema Validator.
"""

from datetime import datetime
from typing import Dict, List, Optional


class Project:
    """Project model for organizing URLs."""
    
    def __init__(self, id: Optional[int] = None, name: str = "", description: str = "",
                 created_date: Optional[datetime] = None, settings_json: Optional[str] = None):
        self.id = id
        self.name = name
        self.description = description
        self.created_date = created_date or datetime.now()
        self.settings_json = settings_json or "{}"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_date': self.created_date.isoformat() if isinstance(self.created_date, datetime) else self.created_date,
            'settings_json': self.settings_json
        }


class URL:
    """URL model for validation targets."""
    
    def __init__(self, id: Optional[int] = None, project_id: Optional[int] = None,
                 url: str = "", added_date: Optional[datetime] = None,
                 status: str = "active", tags: str = "", notes: str = ""):
        self.id = id
        self.project_id = project_id
        self.url = url
        self.added_date = added_date or datetime.now()
        self.status = status
        self.tags = tags
        self.notes = notes
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'project_id': self.project_id,
            'url': self.url,
            'added_date': self.added_date.isoformat() if isinstance(self.added_date, datetime) else self.added_date,
            'status': self.status,
            'tags': self.tags,
            'notes': self.notes
        }


class ValidationRun:
    """Validation run model for tracking validation sessions."""
    
    def __init__(self, id: Optional[int] = None, project_id: Optional[int] = None,
                 start_time: Optional[datetime] = None, end_time: Optional[datetime] = None,
                 status: str = "pending", total_urls: int = 0, processed_urls: int = 0,
                 settings_snapshot: Optional[str] = None):
        self.id = id
        self.project_id = project_id
        self.start_time = start_time or datetime.now()
        self.end_time = end_time
        self.status = status
        self.total_urls = total_urls
        self.processed_urls = processed_urls
        self.settings_snapshot = settings_snapshot or "{}"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'project_id': self.project_id,
            'start_time': self.start_time.isoformat() if isinstance(self.start_time, datetime) else self.start_time,
            'end_time': self.end_time.isoformat() if isinstance(self.end_time, datetime) and self.end_time else None,
            'status': self.status,
            'total_urls': self.total_urls,
            'processed_urls': self.processed_urls,
            'settings_snapshot': self.settings_snapshot
        }


class ValidationResult:
    """Validation result model for individual URL results."""
    
    def __init__(self, id: Optional[int] = None, run_id: Optional[int] = None,
                 url_id: Optional[int] = None, status: str = "pending",
                 schema_data: Optional[str] = None, errors: Optional[str] = None,
                 score: float = 0.0, validated_at: Optional[datetime] = None,
                 response_time: float = 0.0):
        self.id = id
        self.run_id = run_id
        self.url_id = url_id
        self.status = status
        self.schema_data = schema_data
        self.errors = errors
        self.score = score
        self.validated_at = validated_at or datetime.now()
        self.response_time = response_time
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'run_id': self.run_id,
            'url_id': self.url_id,
            'status': self.status,
            'schema_data': self.schema_data,
            'errors': self.errors,
            'score': self.score,
            'validated_at': self.validated_at.isoformat() if isinstance(self.validated_at, datetime) else self.validated_at,
            'response_time': self.response_time
        }

