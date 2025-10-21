"""
Web routes for Schema Validator application.
"""

import json
import asyncio
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename

from .app import get_db, socketio
from .socketio_events import start_validation_task
from ..core.validator import SchemaValidator
from ..core.report import ReportGenerator
from ..config import Config

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Dashboard page."""
    db = get_db()
    projects = db.get_projects()
    
    # Get URL count per project
    for project in projects:
        urls = db.get_urls(project_id=project['id'], status='active')
        project['url_count'] = len(urls)
    
    # Get recent validation runs
    recent_runs = db.get_validation_runs(limit=5)
    
    return render_template('index.html', 
                         projects=projects,
                         recent_runs=recent_runs,
                         config=Config)


@bp.route('/projects')
def projects():
    """Projects management page."""
    db = get_db()
    all_projects = db.get_projects()
    
    # Get URL count per project
    for project in all_projects:
        urls = db.get_urls(project_id=project['id'])
        project['url_count'] = len(urls)
    
    return render_template('projects.html', projects=all_projects)


@bp.route('/urls')
def urls():
    """URLs management page."""
    db = get_db()
    project_id = request.args.get('project_id', type=int)
    
    projects = db.get_projects()
    urls_list = db.get_urls(project_id=project_id)
    
    return render_template('urls.html', 
                         urls=urls_list,
                         projects=projects,
                         selected_project_id=project_id)


@bp.route('/results')
def results():
    """Results viewer page."""
    db = get_db()
    run_id = request.args.get('run_id', type=int)
    
    runs = db.get_validation_runs(limit=20)
    
    results_data = None
    selected_run = None
    
    if run_id:
        selected_run = db.get_validation_run(run_id)
        results_data = db.get_validation_results(run_id)
    
    return render_template('results.html',
                         runs=runs,
                         selected_run=selected_run,
                         results=results_data)


@bp.route('/settings')
def settings():
    """Settings page."""
    return render_template('settings.html', config=Config)


# API Endpoints

@bp.route('/api/projects', methods=['GET'])
def api_get_projects():
    """Get all projects."""
    db = get_db()
    projects = db.get_projects()
    return jsonify(projects)


@bp.route('/api/projects', methods=['POST'])
def api_create_project():
    """Create a new project."""
    data = request.json
    db = get_db()
    
    project_id = db.create_project(
        name=data.get('name'),
        description=data.get('description', ''),
        settings=data.get('settings')
    )
    
    return jsonify({'id': project_id, 'message': 'Project created successfully'})


@bp.route('/api/projects/<int:project_id>', methods=['PUT'])
def api_update_project(project_id):
    """Update a project."""
    data = request.json
    db = get_db()
    
    db.update_project(
        project_id=project_id,
        name=data.get('name'),
        description=data.get('description'),
        settings=data.get('settings')
    )
    
    return jsonify({'message': 'Project updated successfully'})


@bp.route('/api/projects/<int:project_id>', methods=['DELETE'])
def api_delete_project(project_id):
    """Delete a project."""
    db = get_db()
    db.delete_project(project_id)
    return jsonify({'message': 'Project deleted successfully'})


@bp.route('/api/urls', methods=['GET'])
def api_get_urls():
    """Get all URLs."""
    db = get_db()
    project_id = request.args.get('project_id', type=int)
    status = request.args.get('status')
    
    urls = db.get_urls(project_id=project_id, status=status)
    return jsonify(urls)


@bp.route('/api/urls', methods=['POST'])
def api_add_url():
    """Add a new URL."""
    data = request.json
    db = get_db()
    
    url_id = db.add_url(
        url=data.get('url'),
        project_id=data.get('project_id'),
        tags=data.get('tags', ''),
        notes=data.get('notes', '')
    )
    
    return jsonify({'id': url_id, 'message': 'URL added successfully'})


@bp.route('/api/urls/bulk', methods=['POST'])
def api_add_urls_bulk():
    """Add multiple URLs."""
    data = request.json
    db = get_db()
    
    urls = data.get('urls', [])
    project_id = data.get('project_id')
    
    url_ids = []
    for url in urls:
        if url.strip():
            url_id = db.add_url(url.strip(), project_id=project_id)
            url_ids.append(url_id)
    
    return jsonify({'count': len(url_ids), 'message': f'{len(url_ids)} URLs added successfully'})


@bp.route('/api/urls/<int:url_id>', methods=['PUT'])
def api_update_url(url_id):
    """Update a URL."""
    data = request.json
    db = get_db()
    
    db.update_url(
        url_id=url_id,
        url=data.get('url'),
        status=data.get('status'),
        tags=data.get('tags'),
        notes=data.get('notes')
    )
    
    return jsonify({'message': 'URL updated successfully'})


@bp.route('/api/urls/<int:url_id>', methods=['DELETE'])
def api_delete_url(url_id):
    """Delete a URL."""
    db = get_db()
    db.delete_url(url_id)
    return jsonify({'message': 'URL deleted successfully'})


@bp.route('/api/urls/bulk-delete', methods=['POST'])
def api_bulk_delete_urls():
    """Delete multiple URLs."""
    data = request.json
    url_ids = data.get('url_ids', [])
    
    db = get_db()
    db.bulk_delete_urls(url_ids)
    
    return jsonify({'count': len(url_ids), 'message': f'{len(url_ids)} URLs deleted'})


@bp.route('/api/validation/start', methods=['POST'])
def api_start_validation():
    """Start a validation run."""
    data = request.json
    project_id = data.get('project_id')
    settings = data.get('settings', {})
    
    db = get_db()
    
    # Get active URLs for the project
    urls = db.get_urls(project_id=project_id, status='active')
    
    if not urls:
        return jsonify({'error': 'No active URLs found for validation'}), 400
    
    # Create validation run
    run_id = db.create_validation_run(
        project_id=project_id,
        total_urls=len(urls),
        settings=settings
    )
    
    # Start validation in background
    socketio.start_background_task(start_validation_task, run_id, urls, settings)
    
    return jsonify({'run_id': run_id, 'message': 'Validation started', 'total_urls': len(urls)})


@bp.route('/api/validation/runs', methods=['GET'])
def api_get_validation_runs():
    """Get validation runs."""
    db = get_db()
    project_id = request.args.get('project_id', type=int)
    limit = request.args.get('limit', 50, type=int)
    
    runs = db.get_validation_runs(project_id=project_id, limit=limit)
    return jsonify(runs)


@bp.route('/api/validation/runs/<int:run_id>', methods=['GET'])
def api_get_validation_run(run_id):
    """Get a specific validation run."""
    db = get_db()
    run = db.get_validation_run(run_id)
    
    if not run:
        return jsonify({'error': 'Validation run not found'}), 404
    
    return jsonify(run)


@bp.route('/api/validation/results/<int:run_id>', methods=['GET'])
def api_get_validation_results(run_id):
    """Get results for a validation run."""
    db = get_db()
    results = db.get_validation_results(run_id)
    return jsonify(results)


@bp.route('/api/validation/results/<int:run_id>/download/<format>', methods=['GET'])
def api_download_results(run_id, format):
    """Download validation results in specified format."""
    db = get_db()
    results = db.get_validation_results(run_id)
    
    if not results:
        return jsonify({'error': 'No results found'}), 404
    
    generator = ReportGenerator(results)
    
    if format == 'csv':
        output_path = Config.RESULTS_DIR / f'validation_run_{run_id}.csv'
        generator.generate_csv(output_path)
        return send_file(output_path, as_attachment=True)
    
    elif format == 'json':
        output_path = Config.RESULTS_DIR / f'validation_run_{run_id}.json'
        generator.generate_json(output_path)
        return send_file(output_path, as_attachment=True)
    
    else:
        return jsonify({'error': 'Invalid format. Use csv or json'}), 400


@bp.route('/api/settings', methods=['GET'])
def api_get_settings():
    """Get current settings."""
    return jsonify({
        'headless': Config.DEFAULT_HEADLESS,
        'timeout': Config.DEFAULT_TIMEOUT,
        'delay_min': Config.DEFAULT_DELAY_MIN,
        'delay_max': Config.DEFAULT_DELAY_MAX,
        'max_retries': Config.DEFAULT_MAX_RETRIES,
        'concurrent_limit': Config.DEFAULT_CONCURRENT_LIMIT
    })

