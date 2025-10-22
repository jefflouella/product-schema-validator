"""
Database operations for Schema Validator using SQLite.
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from ..config import Config
from ..models import Project, URL, ValidationRun, ValidationResult


class Database:
    """SQLite database handler for Schema Validator."""
    
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or Config.DATABASE_PATH
        self.init_database()
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection."""
        conn = sqlite3.Connection(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database schema."""
        Config.init_app()  # Ensure directories exist
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create projects table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                created_date TEXT NOT NULL,
                settings_json TEXT DEFAULT '{}'
            )
        ''')
        
        # Create urls table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                url TEXT NOT NULL,
                added_date TEXT NOT NULL,
                status TEXT DEFAULT 'active',
                tags TEXT DEFAULT '',
                notes TEXT DEFAULT '',
                FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
            )
        ''')
        
        # Create validation_runs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS validation_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                start_time TEXT NOT NULL,
                end_time TEXT,
                status TEXT DEFAULT 'pending',
                total_urls INTEGER DEFAULT 0,
                processed_urls INTEGER DEFAULT 0,
                settings_snapshot TEXT DEFAULT '{}',
                FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
            )
        ''')
        
        # Create validation_results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS validation_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id INTEGER NOT NULL,
                url_id INTEGER NOT NULL,
                status TEXT DEFAULT 'pending',
                schema_data TEXT,
                errors TEXT,
                warnings TEXT,
                score REAL DEFAULT 0.0,
                validated_at TEXT NOT NULL,
                response_time REAL DEFAULT 0.0,
                has_warnings BOOLEAN DEFAULT 0,
                FOREIGN KEY (run_id) REFERENCES validation_runs (id) ON DELETE CASCADE,
                FOREIGN KEY (url_id) REFERENCES urls (id) ON DELETE CASCADE
            )
        ''')
        
        # Add new fields to existing validation_results table if they don't exist
        try:
            cursor.execute('ALTER TABLE validation_results ADD COLUMN warnings TEXT')
        except sqlite3.OperationalError:
            pass  # Column already exists
        
        try:
            cursor.execute('ALTER TABLE validation_results ADD COLUMN has_warnings BOOLEAN DEFAULT 0')
        except sqlite3.OperationalError:
            pass  # Column already exists
        
        # Create indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_urls_project ON urls(project_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_runs_project ON validation_runs(project_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_results_run ON validation_results(run_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_results_url ON validation_results(url_id)')
        
        conn.commit()
        conn.close()
        
        # Don't create default project - let users start fresh
    
    # Project operations
    def create_project(self, name: str, description: str = "", settings: Dict = None) -> int:
        """Create a new project."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO projects (name, description, created_date, settings_json)
            VALUES (?, ?, ?, ?)
        ''', (name, description, datetime.now().isoformat(), json.dumps(settings or {})))
        
        project_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return project_id
    
    def get_projects(self) -> List[Dict]:
        """Get all projects."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM projects ORDER BY created_date DESC')
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_project(self, project_id: int) -> Optional[Dict]:
        """Get project by ID."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def update_project(self, project_id: int, name: str = None, description: str = None, settings: Dict = None):
        """Update project."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        updates = []
        values = []
        
        if name is not None:
            updates.append('name = ?')
            values.append(name)
        if description is not None:
            updates.append('description = ?')
            values.append(description)
        if settings is not None:
            updates.append('settings_json = ?')
            values.append(json.dumps(settings))
        
        if updates:
            values.append(project_id)
            cursor.execute(f'UPDATE projects SET {", ".join(updates)} WHERE id = ?', values)
            conn.commit()
        
        conn.close()
    
    def delete_project(self, project_id: int):
        """Delete project and all associated data."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # First delete all URLs for this project
        cursor.execute('DELETE FROM urls WHERE project_id = ?', (project_id,))
        
        # Delete all validation runs for this project (this will cascade to results)
        cursor.execute('DELETE FROM validation_runs WHERE project_id = ?', (project_id,))
        
        # Finally delete the project
        cursor.execute('DELETE FROM projects WHERE id = ?', (project_id,))
        
        conn.commit()
        conn.close()
    
    # URL operations
    def add_url(self, url: str, project_id: int = None, tags: str = "", notes: str = "", status: str = "active") -> int:
        """Add a new URL."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Use first project if none specified
        if project_id is None:
            projects = self.get_projects()
            project_id = projects[0]['id'] if projects else None
        
        cursor.execute('''
            INSERT INTO urls (project_id, url, added_date, status, tags, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (project_id, url, datetime.now().isoformat(), status, tags, notes))
        
        url_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return url_id
    
    def get_urls(self, project_id: int = None, status: str = None) -> List[Dict]:
        """Get URLs, optionally filtered by project and status."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM urls'
        conditions = []
        values = []
        
        if project_id is not None:
            conditions.append('project_id = ?')
            values.append(project_id)
        if status is not None:
            conditions.append('status = ?')
            values.append(status)
        
        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)
        
        query += ' ORDER BY added_date DESC'
        
        cursor.execute(query, values)
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_url(self, url_id: int) -> Optional[Dict]:
        """Get URL by ID."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM urls WHERE id = ?', (url_id,))
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def update_url(self, url_id: int, url: str = None, status: str = None, tags: str = None, notes: str = None):
        """Update URL."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        updates = []
        values = []
        
        if url is not None:
            updates.append('url = ?')
            values.append(url)
        if status is not None:
            updates.append('status = ?')
            values.append(status)
        if tags is not None:
            updates.append('tags = ?')
            values.append(tags)
        if notes is not None:
            updates.append('notes = ?')
            values.append(notes)
        
        if updates:
            values.append(url_id)
            cursor.execute(f'UPDATE urls SET {", ".join(updates)} WHERE id = ?', values)
            conn.commit()
        
        conn.close()
    
    def delete_url(self, url_id: int):
        """Delete URL."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM urls WHERE id = ?', (url_id,))
        conn.commit()
        conn.close()
    
    def bulk_delete_urls(self, url_ids: List[int]):
        """Delete multiple URLs."""
        if not url_ids:
            return
        
        conn = self.get_connection()
        cursor = conn.cursor()
        placeholders = ','.join('?' * len(url_ids))
        cursor.execute(f'DELETE FROM urls WHERE id IN ({placeholders})', url_ids)
        conn.commit()
        conn.close()
    
    # Validation run operations
    def create_validation_run(self, project_id: int = None, total_urls: int = 0, settings: Dict = None) -> int:
        """Create a new validation run."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO validation_runs (project_id, start_time, status, total_urls, settings_snapshot)
            VALUES (?, ?, 'running', ?, ?)
        ''', (project_id, datetime.now().isoformat(), total_urls, json.dumps(settings or {})))
        
        run_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return run_id
    
    def get_validation_runs(self, project_id: int = None, limit: int = 50) -> List[Dict]:
        """Get validation runs."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM validation_runs'
        values = []
        
        if project_id is not None:
            query += ' WHERE project_id = ?'
            values.append(project_id)
        
        query += ' ORDER BY start_time DESC LIMIT ?'
        values.append(limit)
        
        cursor.execute(query, values)
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_validation_run(self, run_id: int) -> Optional[Dict]:
        """Get validation run by ID."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM validation_runs WHERE id = ?', (run_id,))
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def update_validation_run(self, run_id: int, status: str = None, processed_urls: int = None, end_time: str = None):
        """Update validation run."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        updates = []
        values = []
        
        if status is not None:
            updates.append('status = ?')
            values.append(status)
        if processed_urls is not None:
            updates.append('processed_urls = ?')
            values.append(processed_urls)
        if end_time is not None:
            updates.append('end_time = ?')
            values.append(end_time)
        
        if updates:
            values.append(run_id)
            cursor.execute(f'UPDATE validation_runs SET {", ".join(updates)} WHERE id = ?', values)
            conn.commit()
        
        conn.close()
    
    # Validation result operations
    def add_validation_result(self, run_id: int, url_id: int, result: Dict) -> int:
        """Add a validation result."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Handle different result structures
        status = result.get('status', 'error')
        schema_data = result.get('schema_data', {})
        response_time = result.get('response_time', 0.0)
        
        # Extract validation data safely
        validation = result.get('validation', {})
        if isinstance(validation, dict):
            score = validation.get('score', 0.0)
            errors = validation.get('errors', [])
            warnings = validation.get('warnings', [])
        else:
            score = 0.0
            errors = []
            warnings = []
        
        # Handle error case
        if result.get('error'):
            errors.append(result['error'])
        
        # Check if result has warnings
        has_warnings = result.get('has_warnings', False) or (len(warnings) > 0)
        
        cursor.execute('''
            INSERT INTO validation_results 
            (run_id, url_id, status, schema_data, errors, warnings, score, validated_at, response_time, has_warnings)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            run_id,
            url_id,
            status,
            json.dumps(schema_data),
            json.dumps(errors),
            json.dumps(warnings),
            score,
            datetime.now().isoformat(),
            response_time,
            has_warnings
        ))
        
        result_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return result_id
    
    def delete_validation_run(self, run_id: int):
        """Delete a validation run and all its results."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Delete validation results first (foreign key constraint)
        cursor.execute('DELETE FROM validation_results WHERE run_id = ?', (run_id,))
        
        # Delete the validation run
        cursor.execute('DELETE FROM validation_runs WHERE id = ?', (run_id,))
        
        conn.commit()
        conn.close()
    
    def get_validation_results(self, run_id: int) -> List[Dict]:
        """Get validation results for a run."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT vr.*, u.url, u.project_id
            FROM validation_results vr
            JOIN urls u ON vr.url_id = u.id
            WHERE vr.run_id = ?
            ORDER BY vr.validated_at DESC
        ''', (run_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        results = []
        for row in rows:
            result_dict = dict(row)
            # Parse JSON fields
            if result_dict.get('schema_data'):
                result_dict['schema_data'] = json.loads(result_dict['schema_data'])
            
            # Handle errors and warnings
            errors = []
            warnings = []
            
            if result_dict.get('errors'):
                try:
                    errors = json.loads(result_dict['errors'])
                except (json.JSONDecodeError, TypeError):
                    # Handle old format where errors was a dict with errors and warnings
                    try:
                        error_data = json.loads(result_dict['errors'])
                        if isinstance(error_data, dict):
                            errors = error_data.get('errors', [])
                            warnings = error_data.get('warnings', [])
                        else:
                            errors = error_data
                    except (json.JSONDecodeError, TypeError):
                        errors = []
            
            if result_dict.get('warnings'):
                try:
                    warnings = json.loads(result_dict['warnings'])
                except (json.JSONDecodeError, TypeError):
                    warnings = []
            
            result_dict['validation'] = {
                'errors': errors,
                'warnings': warnings,
                'score': result_dict.get('score', 0.0)
            }
            
            # Ensure has_warnings is a boolean
            result_dict['has_warnings'] = bool(result_dict.get('has_warnings', False))
            
            results.append(result_dict)
        
        return results

