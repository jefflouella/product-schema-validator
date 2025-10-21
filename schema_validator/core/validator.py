"""
Product Schema Validator with Anti-Bot Bypass and State Management.
Validates schema.org Product markup with pause/resume support and progress callbacks.
"""

import asyncio
import json
import random
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Callable
from urllib.parse import urlparse

import jsonschema
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
import validators

from .schemas import PRODUCT_SCHEMA, REQUIRED_FIELDS, RECOMMENDED_FIELDS


class ValidationState:
    """Manages validation state for pause/resume functionality."""
    
    def __init__(self):
        self.is_running = False
        self.is_paused = False
        self.should_stop = False
    
    def start(self):
        """Start validation."""
        self.is_running = True
        self.is_paused = False
        self.should_stop = False
    
    def pause(self):
        """Pause validation."""
        self.is_paused = True
    
    def resume(self):
        """Resume validation."""
        self.is_paused = False
    
    def stop(self):
        """Stop validation."""
        self.should_stop = True
        self.is_paused = False
    
    def reset(self):
        """Reset state."""
        self.is_running = False
        self.is_paused = False
        self.should_stop = False


class SchemaValidator:
    """Validates Product schema markup with anti-bot bypass capabilities and state management."""
    
    def __init__(self, 
                 headless: bool = True,
                 timeout: int = 30000,
                 delay_range: Tuple[int, int] = (2, 5),
                 max_retries: int = 1,
                 concurrent_limit: int = 3,
                 user_agents: Optional[List[str]] = None,
                 progress_callback: Optional[Callable] = None):
        self.headless = headless
        self.timeout = timeout
        self.delay_range = delay_range
        self.max_retries = max_retries
        self.concurrent_limit = concurrent_limit
        self.progress_callback = progress_callback
        
        # Validation state
        self.state = ValidationState()
        
        # User agents for rotation
        self.user_agents = user_agents or [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"
        ]
        
        self.product_schema = PRODUCT_SCHEMA
        self.required_fields = REQUIRED_FIELDS
        self.recommended_fields = RECOMMENDED_FIELDS
    
    async def create_browser_context(self, playwright) -> Tuple[Browser, BrowserContext]:
        """Create browser with stealth settings."""
        browser = await playwright.chromium.launch(
            headless=self.headless,
            args=[
                '--no-sandbox',
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor',
                '--disable-background-timer-throttling',
                '--disable-backgrounding-occluded-windows',
                '--disable-renderer-backgrounding',
                '--disable-extensions',
                '--disable-plugins',
                '--disable-images'
            ]
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent=random.choice(self.user_agents),
            extra_http_headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
        )
        
        # Block unnecessary resources to speed up loading
        await context.route("**/*", lambda route: (
            route.abort() if route.request.resource_type in ["image", "media", "font", "stylesheet"] 
            else route.continue_()
        ))
        
        # Add stealth scripts
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });
        """)
        
        return browser, context
    
    async def extract_schema(self, page: Page, url: str) -> Optional[Dict]:
        """Extract Product schema from page."""
        try:
            # Wait for page to load completely - use 'domcontentloaded' instead of 'networkidle'
            # 'networkidle' waits for no network activity for 500ms, which is too slow for modern sites
            await page.wait_for_load_state('domcontentloaded', timeout=self.timeout)
            
            # Give a small additional wait for dynamic content
            await page.wait_for_timeout(2000)
            
            # Get page content
            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            # Look for JSON-LD scripts
            json_ld_scripts = soup.find_all('script', type='application/ld+json')
            
            for script in json_ld_scripts:
                try:
                    data = json.loads(script.string)
                    
                    # Handle arrays of schemas
                    if isinstance(data, list):
                        for item in data:
                            if item.get('@type') == 'Product':
                                return item
                    elif isinstance(data, dict) and data.get('@type') == 'Product':
                        return data
                        
                except (json.JSONDecodeError, AttributeError):
                    continue
            
            # Fallback: look for microdata
            product_elements = soup.find_all(attrs={'itemtype': 'http://schema.org/Product'})
            if product_elements:
                # Basic microdata extraction (simplified)
                product_data = {'@type': 'Product'}
                
                name_elem = soup.find(attrs={'itemprop': 'name'})
                if name_elem:
                    product_data['name'] = name_elem.get_text(strip=True)
                
                image_elem = soup.find(attrs={'itemprop': 'image'})
                if image_elem:
                    product_data['image'] = image_elem.get('content') or image_elem.get('src')
                
                return product_data
            
            return None
            
        except Exception as e:
            print(f"Error extracting schema from {url}: {e}")
            return None
    
    def validate_schema(self, schema_data: Dict) -> Dict:
        """Validate schema against schema.org Product specification."""
        if not schema_data:
            return {
                'valid': False,
                'errors': ['No schema data found'],
                'warnings': [],
                'score': 0
            }
        
        errors = []
        warnings = []
        score = 0
        
        # Validate against JSON schema
        try:
            jsonschema.validate(schema_data, self.product_schema)
        except jsonschema.ValidationError as e:
            errors.append(f"Schema validation error: {e.message}")
        except jsonschema.SchemaError as e:
            errors.append(f"Schema definition error: {e.message}")
        
        # Check required fields
        for field in self.required_fields:
            if field not in schema_data:
                errors.append(f"Missing required field: {field}")
            else:
                score += 20  # 20 points per required field
        
        # Check recommended fields
        for field in self.recommended_fields:
            if field not in schema_data:
                warnings.append(f"Missing recommended field: {field}")
            else:
                score += 5  # 5 points per recommended field
        
        # Validate offers structure
        if 'offers' in schema_data:
            offers = schema_data['offers']
            if not isinstance(offers, dict):
                errors.append("Offers must be an object")
            else:
                required_offer_fields = ['price', 'priceCurrency', 'availability']
                for field in required_offer_fields:
                    if field not in offers:
                        errors.append(f"Missing required offer field: {field}")
        
        # Calculate final score
        max_score = len(self.required_fields) * 20 + len(self.recommended_fields) * 5
        final_score = min(100, (score / max_score) * 100) if max_score > 0 else 0
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'score': round(final_score, 1)
        }
    
    async def process_url(self, page: Page, url: str) -> Dict:
        """Process a single URL and return validation results."""
        result = {
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'status': 'error',
            'schema_found': False,
            'validation': None,
            'error': None,
            'response_time': 0
        }
        
        start_time = time.time()
        
        try:
            # Navigate to URL
            response = await page.goto(url, timeout=self.timeout, wait_until='networkidle')
            
            if response and response.status >= 400:
                result['error'] = f"HTTP {response.status}"
                return result
            
            # Extract schema
            schema_data = await self.extract_schema(page, url)
            
            if schema_data:
                result['schema_found'] = True
                result['schema_data'] = schema_data
                
                # Validate schema
                validation = self.validate_schema(schema_data)
                result['validation'] = validation
                result['status'] = 'success' if validation['valid'] else 'warning'
            else:
                result['status'] = 'error'
                result['error'] = 'No Product schema found'
            
        except Exception as e:
            result['error'] = str(e)
            result['status'] = 'error'
        
        result['response_time'] = round(time.time() - start_time, 2)
        return result
    
    async def validate_urls_async(self, urls: List[str]) -> List[Dict]:
        """Process URLs with pause/resume support and progress callbacks."""
        results = []
        self.state.start()
        semaphore = asyncio.Semaphore(self.concurrent_limit)
        
        total_urls = len(urls)
        processed = 0
        
        async def process_with_semaphore(url):
            nonlocal processed
            
            # Check for pause/stop
            while self.state.is_paused and not self.state.should_stop:
                await asyncio.sleep(0.5)
            
            if self.state.should_stop:
                return None
            
            async with semaphore:
                async with async_playwright() as p:
                    browser, context = await self.create_browser_context(p)
                    page = await context.new_page()
                    
                    try:
                        result = await self.process_url(page, url)
                        processed += 1
                        
                        # Emit progress callback
                        if self.progress_callback:
                            await self.progress_callback({
                                'url': url,
                                'result': result,
                                'progress': processed / total_urls * 100,
                                'processed': processed,
                                'total': total_urls
                            })
                        
                        return result
                    finally:
                        await browser.close()
        
        # Process URLs
        tasks = [process_with_semaphore(url) for url in urls]
        
        for coro in asyncio.as_completed(tasks):
            if self.state.should_stop:
                break
            
            result = await coro
            if result:
                results.append(result)
                
                # Rate limiting
                delay = random.uniform(*self.delay_range)
                await asyncio.sleep(delay)
        
        self.state.reset()
        return results
    
    def start(self):
        """Start validation."""
        self.state.start()
    
    def pause(self):
        """Pause validation."""
        self.state.pause()
    
    def resume(self):
        """Resume validation."""
        self.state.resume()
    
    def stop(self):
        """Stop validation."""
        self.state.stop()
    
    def get_state(self) -> Dict:
        """Get current validation state."""
        return {
            'is_running': self.state.is_running,
            'is_paused': self.state.is_paused,
            'should_stop': self.state.should_stop
        }

