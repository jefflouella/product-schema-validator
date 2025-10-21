#!/usr/bin/env python3
"""
HTML Report Generator for Schema Validation Results
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
    
    def __init__(self, results_file: str = "results/validation_results.json"):
        self.results_file = Path(results_file)
        self.results = self.load_results()
    
    def load_results(self) -> List[Dict]:
        """Load validation results from JSON file."""
        if not self.results_file.exists():
            raise FileNotFoundError(f"Results file not found: {self.results_file}")
        
        with open(self.results_file, 'r') as f:
            return json.load(f)
    
    def generate_summary_stats(self) -> Dict:
        """Generate summary statistics from results."""
        total = len(self.results)
        success = sum(1 for r in self.results if r['status'] == 'success')
        warning = sum(1 for r in self.results if r['status'] == 'warning')
        error = sum(1 for r in self.results if r['status'] == 'error')
        no_schema = sum(1 for r in self.results if r['status'] == 'no_schema')
        blocked = sum(1 for r in self.results if r['status'] == 'blocked')
        
        schema_found = sum(1 for r in self.results if r.get('schema_found', False))
        avg_score = 0
        
        if schema_found > 0:
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
            'no_schema': no_schema,
            'blocked': blocked,
            'schema_found': schema_found,
            'success_rate': round((success / total) * 100, 1) if total > 0 else 0,
            'schema_rate': round((schema_found / total) * 100, 1) if total > 0 else 0,
            'avg_score': round(avg_score, 1)
        }
    
    def generate_csv_export(self, output_file: str = "results/validation_results.csv"):
        """Generate CSV export of results."""
        output_path = Path(output_file)
        output_path.parent.mkdir(exist_ok=True)
        
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
                    'url': result['url'],
                    'status': result['status'],
                    'schema_found': result.get('schema_found', False),
                    'score': validation.get('score', 0) if validation else 0,
                    'errors': '; '.join(validation.get('errors', [])) if validation else '',
                    'warnings': '; '.join(validation.get('warnings', [])) if validation else '',
                    'response_time': result.get('response_time', 0),
                    'timestamp': result.get('timestamp', '')
                }
                writer.writerow(row)
    
    def generate_html_report(self, output_file: str = "results/validation_report.html"):
        """Generate interactive HTML report."""
        output_path = Path(output_file)
        output_path.parent.mkdir(exist_ok=True)
        
        # Load HTML template
        template_path = Path("templates/report_template.html")
        if not template_path.exists():
            self.create_default_template()
        
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        template = Template(template_content)
        
        # Prepare data for template
        summary = self.generate_summary_stats()
        
        # Prepare results data for JavaScript
        results_data = []
        for result in self.results:
            validation = result.get('validation') or {}
            result_data = {
                'url': result['url'],
                'status': result['status'],
                'schema_found': result.get('schema_found', False),
                'validation': result.get('validation'),  # Include full validation object for modal
                'score': validation.get('score', 0) if validation else 0,
                'errors': validation.get('errors', []) if validation else [],
                'warnings': validation.get('warnings', []) if validation else [],
                'response_time': result.get('response_time', 0),
                'timestamp': result.get('timestamp', ''),
                'schema_data': result.get('schema_data', {}),
                'error': result.get('error')  # Include error message for no-schema cases
            }
            results_data.append(result_data)
        
        # Add progress information
        progress_info = {
            'total_processed': len(self.results),
            'is_complete': True,  # This will be updated in real-time
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Render template
        html_content = template.render(
            summary=summary,
            results=results_data,
            generation_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            progress=progress_info,
            report_title="Product Schema Validation Report"
        )
        
        # Write HTML file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path
    
    def create_default_template(self):
        """Create default HTML template if it doesn't exist."""
        template_path = Path("templates/report_template.html")
        template_path.parent.mkdir(exist_ok=True)
        
        template_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ report_title or "Product Schema Validation Report" }}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        .status-success { color: #28a745; }
        .status-warning { color: #ffc107; }
        .status-error { color: #dc3545; }
        .status-blocked { color: #6c757d; }
        .table-responsive { max-height: 600px; overflow-y: auto; }
        .score-badge { font-size: 0.8em; }
        .filter-section { background: #f8f9fa; padding: 1rem; border-radius: 0.375rem; margin-bottom: 1rem; }
        
        /* Modal overlay styles */
        .modal-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            z-index: 1000;
        }
        
        .modal-content {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            max-width: 90%;
            max-height: 90%;
            overflow-y: auto;
            padding: 0;
        }
        
        .modal-header {
            background: #f8f9fa;
            padding: 1rem;
            border-bottom: 1px solid #dee2e6;
            border-radius: 8px 8px 0 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .modal-body {
            padding: 1.5rem;
        }
        
        .close-btn {
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: #6c757d;
        }
        
        .close-btn:hover {
            color: #000;
        }
        
        /* Error and warning highlighting */
        .error-highlight {
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            border-radius: 4px;
            padding: 0.5rem;
            margin: 0.5rem 0;
        }
        
        .warning-highlight {
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 4px;
            padding: 0.5rem;
            margin: 0.5rem 0;
        }
        
        .path-display {
            font-family: monospace;
            background-color: #f8f9fa;
            padding: 0.25rem 0.5rem;
            border-radius: 3px;
            font-size: 0.9em;
            margin: 0.25rem 0;
        }
        
        .copy-path-btn {
            background: #007bff;
            color: white;
            border: none;
            padding: 0.25rem 0.5rem;
            border-radius: 3px;
            font-size: 0.8em;
            cursor: pointer;
            margin-left: 0.5rem;
        }
        
        .copy-path-btn:hover {
            background: #0056b3;
        }
        
        .explanation-text {
            font-style: italic;
            color: #6c757d;
            margin-top: 0.25rem;
        }
    </style>
</head>
<body>
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">
                <h1 class="my-4">
                    <i class="fas fa-search"></i> {{ report_title or "Product Schema Validation Report" }}
                    <small class="text-muted">Generated: {{ generation_time }}</small>
                </h1>
                
                <!-- Summary Cards -->
                <div class="row mb-4">
                    <div class="col-md-2">
                        <div class="card text-center">
                            <div class="card-body">
                                <h5 class="card-title text-primary">{{ summary.total }}</h5>
                                <p class="card-text">Total URLs</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-2">
                        <div class="card text-center">
                            <div class="card-body">
                                <h5 class="card-title text-success">{{ summary.success }}</h5>
                                <p class="card-text">Success</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-2">
                        <div class="card text-center">
                            <div class="card-body">
                                <h5 class="card-title text-warning">{{ summary.warning }}</h5>
                                <p class="card-text">Warnings</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-2">
                        <div class="card text-center">
                            <div class="card-body">
                                <h5 class="card-title text-danger">{{ summary.error }}</h5>
                                <p class="card-text">Errors</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-2">
                        <div class="card text-center">
                            <div class="card-body">
                                <h5 class="card-title text-secondary">{{ summary.blocked }}</h5>
                                <p class="card-text">Blocked</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-2">
                        <div class="card text-center">
                            <div class="card-body">
                                <h5 class="card-title text-info">{{ summary.schema_found }}</h5>
                                <p class="card-text">Schema Found</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Charts -->
                <div class="row mb-4">
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header">
                                <h5>Status Distribution</h5>
                            </div>
                            <div class="card-body">
                                <canvas id="statusChart" width="400" height="200"></canvas>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header">
                                <h5>Schema Coverage</h5>
                            </div>
                            <div class="card-body">
                                <canvas id="schemaChart" width="400" height="200"></canvas>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Filters -->
                <div class="filter-section">
                    <div class="row">
                        <div class="col-md-3">
                            <label for="statusFilter" class="form-label">Status Filter:</label>
                            <select id="statusFilter" class="form-select">
                                <option value="">All</option>
                                <option value="success">Success</option>
                                <option value="warning">Warning</option>
                                <option value="error">Error</option>
                            </select>
                        </div>
                        <div class="col-md-3">
                            <label for="schemaFilter" class="form-label">Schema Found:</label>
                            <select id="schemaFilter" class="form-select">
                                <option value="">All</option>
                                <option value="true">Yes</option>
                                <option value="false">No</option>
                            </select>
                        </div>
                        <div class="col-md-3">
                            <label for="searchInput" class="form-label">Search URL:</label>
                            <input type="text" id="searchInput" class="form-control" placeholder="Search URLs...">
                        </div>
                        <div class="col-md-3">
                            <label class="form-label">&nbsp;</label>
                            <div>
                                <button id="exportCsv" class="btn btn-outline-primary">
                                    <i class="fas fa-download"></i> Export CSV
                                </button>
                                <button id="clearFilters" class="btn btn-outline-secondary">
                                    <i class="fas fa-times"></i> Clear
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Results Table -->
                <div class="card">
                    <div class="card-header">
                        <h5>Validation Results</h5>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-striped table-hover" id="resultsTable">
                                <thead class="table-dark">
                                    <tr>
                                        <th>URL</th>
                                        <th>Status</th>
                                        <th>Schema</th>
                                        <th>Score</th>
                                        <th>Response Time</th>
                                        <th>Issues</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for result in results %}
                                    <tr data-status="{{ result.status }}" data-schema="{{ result.schema_found|lower }}">
                                        <td>
                                            <a href="{{ result.url }}" target="_blank" class="text-decoration-none">
                                                {{ result.url[:50] }}{% if result.url|length > 50 %}...{% endif %}
                                            </a>
                                        </td>
                                        <td>
                                            <span class="badge status-{{ result.status }}">
                                                {% if result.status == 'success' %}
                                                    <i class="fas fa-check"></i> Success
                                                {% elif result.status == 'warning' %}
                                                    <i class="fas fa-exclamation-triangle"></i> Warning
                                                {% elif result.status == 'blocked' %}
                                                    <i class="fas fa-shield-alt"></i> Blocked
                                                {% else %}
                                                    <i class="fas fa-times"></i> Error
                                                {% endif %}
                                            </span>
                                        </td>
                                        <td>
                                            {% if result.schema_found %}
                                                <span class="badge bg-success"><i class="fas fa-check"></i> Found</span>
                                            {% else %}
                                                <span class="badge bg-danger"><i class="fas fa-times"></i> Not Found</span>
                                            {% endif %}
                                        </td>
                                        <td>
                                            {% if result.score > 0 %}
                                                <span class="badge score-badge {% if result.score >= 80 %}bg-success{% elif result.score >= 60 %}bg-warning{% else %}bg-danger{% endif %}">
                                                    {{ result.score }}%
                                                </span>
                                            {% else %}
                                                <span class="text-muted">N/A</span>
                                            {% endif %}
                                        </td>
                                        <td>{{ result.response_time }}s</td>
                                        <td>
                                            {% if result.errors %}
                                                <span class="text-danger" title="{{ result.errors|join('; ') }}">
                                                    <i class="fas fa-exclamation-circle"></i> {{ result.errors|length }} errors
                                                </span>
                                            {% endif %}
                                            {% if result.warnings %}
                                                <span class="text-warning" title="{{ result.warnings|join('; ') }}">
                                                    <i class="fas fa-exclamation-triangle"></i> {{ result.warnings|length }} warnings
                                                </span>
                                            {% endif %}
                                        </td>
                                        <td>
                                            <button class="btn btn-sm btn-outline-info" onclick="showDetails({{ loop.index }})">
                                                <i class="fas fa-eye"></i> Details
                                            </button>
                                        </td>
                                    </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Modal Overlay -->
    <div id="detailsModal" class="modal-overlay" onclick="closeModal()">
        <div class="modal-content" onclick="event.stopPropagation()">
            <div class="modal-header">
                <h5 class="modal-title">Schema Details</h5>
                <button class="close-btn" onclick="closeModal()">&times;</button>
            </div>
            <div class="modal-body" id="modalBody">
                <!-- Content will be populated by JavaScript -->
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Chart.js configuration
        const statusCtx = document.getElementById('statusChart').getContext('2d');
        new Chart(statusCtx, {
            type: 'doughnut',
            data: {
                labels: ['Success', 'Warning', 'Error'],
                datasets: [{
                    data: [{{ summary.success }}, {{ summary.warning }}, {{ summary.error }}],
                    backgroundColor: ['#28a745', '#ffc107', '#dc3545']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
        
        const schemaCtx = document.getElementById('schemaChart').getContext('2d');
        new Chart(schemaCtx, {
            type: 'doughnut',
            data: {
                labels: ['Schema Found', 'No Schema'],
                datasets: [{
                    data: [{{ summary.schema_found }}, {{ summary.total - summary.schema_found }}],
                    backgroundColor: ['#28a745', '#dc3545']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
        
        // Filter functionality
        function filterTable() {
            const statusFilter = document.getElementById('statusFilter').value;
            const schemaFilter = document.getElementById('schemaFilter').value;
            const searchInput = document.getElementById('searchInput').value.toLowerCase();
            
            const rows = document.querySelectorAll('#resultsTable tbody tr');
            rows.forEach(row => {
                if (row.id.startsWith('details-')) return; // Skip detail rows
                
                const status = row.dataset.status;
                const schema = row.dataset.schema;
                const url = row.querySelector('td a').textContent.toLowerCase();
                
                const statusMatch = !statusFilter || status === statusFilter;
                const schemaMatch = !schemaFilter || schema === schemaFilter;
                const searchMatch = !searchInput || url.includes(searchInput);
                
                row.style.display = (statusMatch && schemaMatch && searchMatch) ? '' : 'none';
            });
        }
        
        // Event listeners
        document.getElementById('statusFilter').addEventListener('change', filterTable);
        document.getElementById('schemaFilter').addEventListener('change', filterTable);
        document.getElementById('searchInput').addEventListener('input', filterTable);
        
        document.getElementById('clearFilters').addEventListener('click', () => {
            document.getElementById('statusFilter').value = '';
            document.getElementById('schemaFilter').value = '';
            document.getElementById('searchInput').value = '';
            filterTable();
        });
        
        document.getElementById('exportCsv').addEventListener('click', () => {
            window.open('validation_results.csv', '_blank');
        });
        
    </script>
    
    <!-- Results data -->
    <script type="application/json" id="results-data">{{ results|tojson }}</script>
    
    <script>
        // Global results data
        let resultsData = null;
        
        // Load results data safely
        function loadResultsData() {
            if (!resultsData) {
                try {
                    const dataScript = document.getElementById('results-data');
                    resultsData = JSON.parse(dataScript.textContent);
                } catch (e) {
                    console.error('Error loading results data:', e);
                    resultsData = [];
                }
            }
            return resultsData;
        }
        
        // Show details in modal overlay
        function showDetails(index) {
            const modal = document.getElementById('detailsModal');
            const modalBody = document.getElementById('modalBody');
            
            // Get the result data for this index
            const results = loadResultsData();
            const result = results[index - 1]; // Convert to 0-based index
            
            if (!result) {
                console.error('Result not found for index:', index);
                return;
            }
            
            // Build modal content
            let content = '<div class="mb-3">';
            content += '<h6><strong>URL:</strong></h6>';
            content += '<p><a href="' + result.url + '" target="_blank">' + result.url + '</a></p>';
            content += '</div>';
            
            content += '<div class="mb-3">';
            content += '<h6><strong>Status:</strong></h6>';
            content += '<p><span class="badge status-' + result.status + '">' + result.status + '</span></p>';
            content += '</div>';
            
            if (result.schema_found) {
                // Show validation score first
                if (result.validation) {
                    content += '<div class="mb-3">';
                    content += '<h6><strong>Validation Score:</strong></h6>';
                    content += '<p class="h4">' + (result.validation.score || 0) + '%</p>';
                    content += '</div>';
                }
                
                // Show errors FIRST (most important)
                if (result.validation && result.validation.errors && result.validation.errors.length > 0) {
                    content += '<div class="mb-3">';
                    content += '<h6 class="text-danger"><strong>Errors:</strong></h6>';
                    result.validation.errors.forEach(error => {
                        content += '<div class="error-highlight">';
                        
                        // Handle both old format (string) and new format (object)
                        if (typeof error === 'string') {
                            content += '<div class="text-danger"><strong>' + error + '</strong></div>';
                            // Add specific explanations for common errors
                            if (error.includes('price') && error.includes('required')) {
                                content += '<div class="explanation-text">The product price is missing from the offers section. This is required for proper e-commerce functionality.</div>';
                            } else if (error.includes('Missing required offer field')) {
                                content += '<div class="explanation-text">This offer field is required for proper pricing information display.</div>';
                            } else {
                                content += '<div class="explanation-text">This is a validation error that needs to be fixed.</div>';
                            }
                        } else {
                            content += '<div class="text-danger"><strong>' + error.message + '</strong></div>';
                            if (error.path) {
                                content += '<div class="path-display">Path: ' + error.path + 
                                         '<button class="copy-path-btn" data-path="' + error.path + '">Copy Path</button></div>';
                            }
                            if (error.explanation) {
                                content += '<div class="explanation-text">' + error.explanation + '</div>';
                            }
                        }
                        content += '</div>';
                    });
                    content += '</div>';
                }
                
                // Show warnings SECOND
                if (result.validation && result.validation.warnings && result.validation.warnings.length > 0) {
                    content += '<div class="mb-3">';
                    content += '<h6 class="text-warning"><strong>Warnings:</strong></h6>';
                    result.validation.warnings.forEach(warning => {
                        content += '<div class="warning-highlight">';
                        
                        // Handle both old format (string) and new format (object)
                        if (typeof warning === 'string') {
                            content += '<div class="text-warning"><strong>' + warning + '</strong></div>';
                            // Add specific explanations for common warnings
                            if (warning.includes('gtin')) {
                                content += '<div class="explanation-text">GTIN (Global Trade Item Number) is recommended for better product identification and search engine optimization.</div>';
                            } else if (warning.includes('aggregateRating')) {
                                content += '<div class="explanation-text">Product ratings and reviews help with SEO and customer trust.</div>';
                            } else if (warning.includes('review')) {
                                content += '<div class="explanation-text">Customer reviews improve product credibility and search rankings.</div>';
                            } else {
                                content += '<div class="explanation-text">This is a recommended field that would improve SEO.</div>';
                            }
                        } else {
                            content += '<div class="text-warning"><strong>' + warning.message + '</strong></div>';
                            if (warning.path) {
                                content += '<div class="path-display">Path: ' + warning.path + 
                                         '<button class="copy-path-btn" data-path="' + warning.path + '">Copy Path</button></div>';
                            }
                            if (warning.explanation) {
                                content += '<div class="explanation-text">' + warning.explanation + '</div>';
                            }
                        }
                        content += '</div>';
                    });
                    content += '</div>';
                }
                
                // Show schema data LAST (for reference)
                content += '<div class="mb-3">';
                content += '<h6><strong>Schema Data:</strong></h6>';
                if (result.schema_data) {
                    // Highlight problematic fields in the schema data
                    let schemaJson = JSON.stringify(result.schema_data, null, 2);
                    
                    // Highlight missing required fields - check if validation exists first
                    if (result.validation && result.validation.errors) {
                        result.validation.errors.forEach(error => {
                            if (typeof error === 'string' && error.includes('Missing required field')) {
                                const field = error.replace('Missing required field: ', '');
                                schemaJson = schemaJson.replace(new RegExp('"' + field + '"', 'g'), '<span class="text-danger bg-danger bg-opacity-10 fw-bold">"' + field + '"</span>');
                            }
                        });
                    }
                    
                    // Highlight missing recommended fields - check if validation exists first
                    if (result.validation && result.validation.warnings) {
                        result.validation.warnings.forEach(warning => {
                            if (typeof warning === 'string' && warning.includes('Missing recommended field')) {
                                const field = warning.replace('Missing recommended field: ', '');
                                schemaJson = schemaJson.replace(new RegExp('"' + field + '"', 'g'), '<span class="text-warning bg-warning bg-opacity-10 fw-bold">"' + field + '"</span>');
                            }
                        });
                    }
                    
                    content += '<pre class="bg-light p-3"><code>' + schemaJson + '</code></pre>';
                } else {
                    content += '<p class="text-muted">No schema data available</p>';
                }
                content += '</div>';
            } else {
                content += '<div class="mb-3">';
                content += '<h6><strong>No Schema Found</strong></h6>';
                if (result.error) {
                    content += '<p class="text-danger">Error: ' + result.error + '</p>';
                }
                content += '</div>';
            }
            
            // Set content and show modal
            modalBody.innerHTML = content;
            modal.style.display = 'block';
        }
        
        // Close modal
        function closeModal() {
            const modal = document.getElementById('detailsModal');
            modal.style.display = 'none';
        }
        
        // Close modal on Escape key
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape') {
                closeModal();
            }
        });
        
        // Copy path to clipboard
        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(function() {
                // Show a brief success message
                const btn = event.target;
                const originalText = btn.textContent;
                btn.textContent = 'Copied!';
                btn.style.background = '#28a745';
                setTimeout(() => {
                    btn.textContent = originalText;
                    btn.style.background = '#007bff';
                }, 1000);
            }).catch(function(err) {
                console.error('Could not copy text: ', err);
            });
        }
        
        // Handle copy button clicks using event delegation
        document.addEventListener('click', function(event) {
            if (event.target.classList.contains('copy-path-btn')) {
                const path = event.target.getAttribute('data-path');
                if (path) {
                    copyToClipboard(path);
                }
            }
        });
    </script>
</body>
</html>'''
        
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(template_content)
    
    def generate_all_reports(self):
        """Generate all report formats."""
        print("Generating reports...")
        
        # Generate CSV export
        csv_path = self.generate_csv_export()
        print(f"CSV export: {csv_path}")
        
        # Generate HTML report
        html_path = self.generate_html_report()
        print(f"HTML report: {html_path}")
        
        return {
            'csv': csv_path,
            'html': html_path
        }


def main():
    """Main entry point for report generation."""
    try:
        generator = ReportGenerator()
        reports = generator.generate_all_reports()
        
        print("\nReport generation complete!")
        print(f"Files created:")
        for report_type, path in reports.items():
            print(f"  {report_type.upper()}: {path}")
            
    except Exception as e:
        print(f"Error generating reports: {e}")


if __name__ == "__main__":
    main()
