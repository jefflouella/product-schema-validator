"""
SocketIO event handlers for real-time validation updates.
"""

import asyncio
from datetime import datetime
from flask_socketio import emit

from .app import socketio, get_db
from ..core.validator import SchemaValidator


# Global validator instance for state management
current_validator = None


def start_validation_task(run_id, urls, settings):
    """Background task to run validation with real-time updates."""
    global current_validator
    
    db = get_db()
    
    # Extract URLs from url objects
    url_list = [url_obj['url'] for url_obj in urls]
    url_id_map = {url_obj['url']: url_obj['id'] for url_obj in urls}
    
    # Create validator with progress callback
    def progress_callback(data):
        """Emit progress updates via SocketIO."""
        try:
            # Update database
            processed = data['processed']  # Use processed count, not progress percentage
            db.update_validation_run(run_id, processed_urls=processed)
            
            # Save result to database
            url = data['url']
            url_id = url_id_map.get(url)
            if url_id and data['result'] is not None:
                db.add_validation_result(run_id, url_id, data['result'])
            elif url_id and data['result'] is None:
                # Handle failed validation
                db.add_validation_result(run_id, url_id, {
                    'status': 'error',
                    'error': 'Failed to validate URL',
                    'score': 0.0
                })
            
            # Emit to clients
            socketio.emit('validation_progress', {
                'run_id': run_id,
                'url': url,
                'result': data['result'],
                'progress': data['progress'],
                'processed': processed,
                'total': data['total']
            })
        except Exception as e:
            print(f"Error in progress callback: {e}")
            # Emit error to clients
            socketio.emit('validation_error', {
                'run_id': run_id,
                'error': f'Progress callback error: {str(e)}'
            })
    
    # Create original working validator
    current_validator = SchemaValidator(
        headless=settings.get('headless', True),
        timeout=settings.get('timeout', 30000),
        delay_range=(settings.get('delay_min', 2), settings.get('delay_max', 5)),
        max_retries=settings.get('max_retries', 1),
        concurrent_limit=settings.get('concurrent_limit', 3),
        progress_callback=progress_callback
    )
    
    # Run validation
    try:
        # Create event loop for async execution
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        results = loop.run_until_complete(current_validator.validate_urls_async(url_list))
        
        # Update run status
        db.update_validation_run(
            run_id,
            status='completed',
            end_time=datetime.now().isoformat()
        )
        
        # Emit completion
        socketio.emit('validation_complete', {
            'run_id': run_id,
            'total_results': len(results),
            'message': 'Validation completed successfully'
        })
        
    except Exception as e:
        # Update run status to failed
        db.update_validation_run(
            run_id,
            status='failed',
            end_time=datetime.now().isoformat()
        )
        
        # Emit error
        socketio.emit('validation_error', {
            'run_id': run_id,
            'error': str(e)
        })
    
    finally:
        current_validator = None


@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    print('Client connected')
    emit('connected', {'message': 'Connected to validation server'})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    print('Client disconnected')


@socketio.on('pause_validation')
def handle_pause_validation():
    """Handle pause validation request."""
    global current_validator
    if current_validator:
        current_validator.state.pause()
        emit('validation_paused', {'message': 'Validation paused'})
    else:
        emit('error', {'message': 'No active validation to pause'})


@socketio.on('resume_validation')
def handle_resume_validation():
    """Handle resume validation request."""
    global current_validator
    if current_validator:
        current_validator.state.resume()
        emit('validation_resumed', {'message': 'Validation resumed'})
    else:
        emit('error', {'message': 'No active validation to resume'})


@socketio.on('stop_validation')
def handle_stop_validation():
    """Handle stop validation request."""
    global current_validator
    if current_validator:
        current_validator.stop()
        
        # Update run status in database
        db = get_db()
        # Note: We'd need to track the current run_id, but for now we'll let the task handle cleanup
        
        emit('validation_stopped', {'message': 'Validation stopped'})
    else:
        emit('error', {'message': 'No active validation to stop'})


@socketio.on('get_validation_state')
def handle_get_validation_state():
    """Get current validation state."""
    global current_validator
    if current_validator:
        state = current_validator.get_state()
        emit('validation_state', state)
    else:
        emit('validation_state', {
            'is_running': False,
            'is_paused': False,
            'should_stop': False
        })

