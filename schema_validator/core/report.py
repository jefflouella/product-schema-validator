"""
HTML Report Generator for Schema Validation Results.
Creates interactive HTML reports with filtering, sorting, and export capabilities.
"""

import json
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from jinja2 import Template


class ReportGenerator:
    """Generates interactive HTML reports from validation results."""
    
    def __init__(self, results: List[Dict]):
        self.results = results
    
    def generate_summary_stats(self) -> Dict:
        """Generate summary statistics from results."""
        total = len(self.results)
        if total == 0:
            return {
                'total': 0,
                'success': 0,
                'warning': 0,
                'error': 0,
                'schema_found': 0,
                'success_rate': 0,
                'schema_rate': 0,
                'avg_score': 0
            }
        
        success = sum(1 for r in self.results if r.get('status') == 'success')
        warning = sum(1 for r in self.results if r.get('status') == 'warning')
        error = sum(1 for r in self.results if r.get('status') == 'error')
        schema_found = sum(1 for r in self.results if r.get('schema_found', False))
        
        # Calculate average score
        scores = []
        for r in self.results:
            validation = r.get('validation')
            if validation and isinstance(validation, dict) and 'score' in validation:
                scores.append(validation['score'])
        avg_score = sum(scores) / len(scores) if scores else 0
        
        return {
            'total': total,
            'success': success,
            'warning': warning,
            'error': error,
            'schema_found': schema_found,
            'success_rate': round((success / total) * 100, 1) if total > 0 else 0,
            'schema_rate': round((schema_found / total) * 100, 1) if total > 0 else 0,
            'avg_score': round(avg_score, 1)
        }
    
    def generate_csv(self, output_path: Path) -> Path:
        """Generate CSV export of results."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'url', 'status', 'schema_found', 'score', 'errors', 'warnings', 
                'response_time', 'timestamp'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for result in self.results:
                validation = result.get('validation') or {}
                row = {
                    'url': result.get('url', ''),
                    'status': result.get('status', ''),
                    'schema_found': result.get('schema_found', False),
                    'score': validation.get('score', 0) if validation else 0,
                    'errors': '; '.join(validation.get('errors', [])) if validation else '',
                    'warnings': '; '.join(validation.get('warnings', [])) if validation else '',
                    'response_time': result.get('response_time', 0),
                    'timestamp': result.get('timestamp', '')
                }
                writer.writerow(row)
        
        return output_path
    
    def generate_json(self, output_path: Path) -> Path:
        """Generate JSON export of results."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2)
        
        return output_path

