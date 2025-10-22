"""
FlareSolverr-based Product Schema Validator.
Implements proven Cloudflare bypass techniques from FlareSolverr.
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


class FlareValidationState:
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


class FlareSchemaValidator:
    """
    FlareSolverr-inspired Product Schema Validator with advanced Cloudflare bypass.
    Implements proven techniques from FlareSolverr for reliable bypass.
    """
    
    def __init__(
        self,
        concurrent_limit: int = 3,
        timeout: int = 30,
        delay_min: float = 1.0,
        delay_max: float = 3.0,
        max_retries: int = 2,
        headless: bool = True,
        user_agent: str = "random",
        custom_user_agent: str = "",
        stealth_mode: bool = True,
        block_resources: bool = True,
        progress_callback: Optional[Callable] = None
    ):
        self.concurrent_limit = concurrent_limit
        self.timeout = timeout * 1000  # Convert to milliseconds
        self.delay_min = delay_min
        self.delay_max = delay_max
        self.max_retries = max_retries
        self.headless = headless
        self.user_agent = user_agent
        self.custom_user_agent = custom_user_agent
        self.stealth_mode = stealth_mode
        self.block_resources = block_resources
        self.progress_callback = progress_callback
        
        # FlareSolverr-inspired user agents
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0"
        ]
        
        self.state = FlareValidationState()
    
    async def create_browser_context(self, playwright) -> Tuple[Browser, BrowserContext]:
        """Create browser with FlareSolverr-inspired stealth settings."""
        
        # FlareSolverr uses undetected-chromedriver approach
        browser = await playwright.chromium.launch(
            headless=self.headless,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-zygote',
                '--disable-gpu',
                '--disable-background-timer-throttling',
                '--disable-backgrounding-occluded-windows',
                '--disable-renderer-backgrounding',
                '--disable-features=TranslateUI',
                '--disable-ipc-flooding-protection',
                '--disable-extensions',
                '--disable-plugins',
                '--disable-images' if self.block_resources else '',
                '--disable-javascript' if not self.stealth_mode else '',
                '--disable-css' if not self.stealth_mode else '',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor',
                '--disable-blink-features=AutomationControlled',
                '--disable-automation',
                '--disable-infobars',
                '--disable-extensions-file-access-check',
                '--disable-extensions-http-throttling',
                '--disable-client-side-phishing-detection',
                '--disable-component-update',
                '--disable-domain-reliability',
                '--disable-hang-monitor',
                '--disable-prompt-on-repost',
                '--disable-sync',
                '--disable-translate',
                '--hide-scrollbars',
                '--mute-audio',
                '--no-default-browser-check',
                '--no-first-run',
                '--safebrowsing-disable-auto-update',
                '--enable-automation',
                '--password-store=basic',
                '--use-mock-keychain'
            ]
        )
        
        # Select user agent
        if self.custom_user_agent:
            user_agent = self.custom_user_agent
        elif self.user_agent == "random":
            user_agent = random.choice(self.user_agents)
        else:
            user_agent = self.user_agents[0]
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent=user_agent,
            extra_http_headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Cache-Control': 'max-age=0',
                'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                'Sec-Ch-Ua-Mobile': '?0',
                'Sec-Ch-Ua-Platform': '"Windows"',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1',
                'DNT': '1',
                'Connection': 'keep-alive',
            }
        )
        
        # Block unnecessary resources for speed
        if self.block_resources:
            await context.route("**/*", lambda route: (
                route.abort() if route.request.resource_type in ["image", "media", "font", "stylesheet"] 
                else route.continue_()
            ))
        
        # FlareSolverr-inspired stealth scripts
        if self.stealth_mode:
            await context.add_init_script("""
                // Remove webdriver property
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                
                // Mock plugins like FlareSolverr does
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [
                        {
                            0: {type: "application/x-google-chrome-pdf", suffixes: "pdf", description: "Portable Document Format", enabledPlugin: Plugin},
                            description: "Portable Document Format",
                            filename: "internal-pdf-viewer",
                            length: 1,
                            name: "Chrome PDF Plugin"
                        },
                        {
                            0: {type: "application/pdf", suffixes: "pdf", description: "", enabledPlugin: Plugin},
                            description: "",
                            filename: "mhjfbmdgcfjbbpaeojofohoefgiehjai",
                            length: 1,
                            name: "Chrome PDF Viewer"
                        }
                    ],
                });
                
                // Mock languages
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en'],
                });
                
                // Mock permissions
                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                        Promise.resolve({ state: Notification.permission }) :
                        originalQuery(parameters)
                );
                
                // Mock chrome runtime
                window.chrome = {
                    runtime: {},
                    loadTimes: function() {},
                    csi: function() {},
                    app: {}
                };
                
                // Mock screen properties
                Object.defineProperty(screen, 'colorDepth', {
                    get: () => 24,
                });
                
                Object.defineProperty(screen, 'pixelDepth', {
                    get: () => 24,
                });
                
                // Mock timezone
                Object.defineProperty(Intl.DateTimeFormat.prototype, 'resolvedOptions', {
                    value: function() {
                        return {
                            calendar: 'gregory',
                            locale: 'en-US',
                            numberingSystem: 'latn',
                            timeZone: 'America/New_York'
                        };
                    }
                });
                
                // Remove automation indicators
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
                
                // Override automation detection
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                
                // Mock getParameter
                const originalGetParameter = URLSearchParams.prototype.get;
                URLSearchParams.prototype.get = function(name) {
                    if (name === 'webdriver') return null;
                    return originalGetParameter.call(this, name);
                };
            """)
        
        return browser, context
    
    async def extract_schema(self, page: Page, url: str) -> Optional[Dict]:
        """Extract Product schema from page using FlareSolverr approach."""
        try:
            # FlareSolverr waits for Cloudflare challenge to be solved
            # We'll use a more aggressive approach for faster loading
            await page.wait_for_load_state('domcontentloaded', timeout=self.timeout)
            
            # Add small delay to let any dynamic content load
            await page.wait_for_timeout(1000)
            
            # Get page content
            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            # Look for JSON-LD structured data
            json_ld_scripts = soup.find_all('script', type='application/ld+json')
            for script in json_ld_scripts:
                try:
                    data = json.loads(script.string)
                    if isinstance(data, dict) and data.get('@type') == 'Product':
                        return data
                    elif isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict) and item.get('@type') == 'Product':
                                return item
                except (json.JSONDecodeError, AttributeError):
                    continue
            
            # Look for microdata
            microdata_items = soup.find_all(attrs={'itemtype': 'http://schema.org/Product'})
            if microdata_items:
                product_data = {}
                for item in microdata_items:
                    for prop in item.find_all(attrs={'itemprop': True}):
                        key = prop.get('itemprop')
                        value = prop.get('content') or prop.get_text(strip=True)
                        if key and value:
                            product_data[key] = value
                if product_data:
                    return product_data
            
            # Look for RDFa
            rdfa_items = soup.find_all(attrs={'typeof': 'schema:Product'})
            if rdfa_items:
                product_data = {}
                for item in rdfa_items:
                    for prop in item.find_all(attrs={'property': True}):
                        key = prop.get('property', '').replace('schema:', '')
                        value = prop.get('content') or prop.get_text(strip=True)
                        if key and value:
                            product_data[key] = value
                if product_data:
                    return product_data
            
            return None
            
        except Exception as e:
            print(f"Error extracting schema from {url}: {e}")
            return None
    
    async def validate_url(self, url: str) -> Dict:
        """Validate a single URL using FlareSolverr approach."""
        start_time = time.time()
        
        try:
            async with async_playwright() as p:
                browser, context = await self.create_browser_context(p)
                
                try:
                    page = await context.new_page()
                    
                    # Navigate to URL with retries
                    for attempt in range(self.max_retries + 1):
                        try:
                            await page.goto(url, timeout=self.timeout, wait_until='domcontentloaded')
                            break
                        except Exception as e:
                            if attempt == self.max_retries:
                                raise e
                            await asyncio.sleep(random.uniform(1, 3))
                    
                    # Extract schema
                    schema_data = await self.extract_schema(page, url)
                    
                    # Validate schema
                    if schema_data:
                        try:
                            jsonschema.validate(schema_data, PRODUCT_SCHEMA)
                            status = "success"
                            score = self.calculate_score(schema_data)
                            errors = []
                            warnings = self.get_warnings(schema_data)
                        except jsonschema.ValidationError as e:
                            status = "error"
                            score = 0
                            errors = [str(e)]
                            warnings = []
                    else:
                        status = "error"
                        score = 0
                        errors = ["No Product schema found"]
                        warnings = []
                    
                    response_time = time.time() - start_time
                    
                    return {
                        'url': url,
                        'status': status,
                        'schema_data': schema_data or {},
                        'response_time': response_time,
                        'score': score,
                        'errors': errors,
                        'warnings': warnings
                    }
                    
                finally:
                    await browser.close()
                    
        except Exception as e:
            response_time = time.time() - start_time
            return {
                'url': url,
                'status': 'error',
                'schema_data': {},
                'response_time': response_time,
                'score': 0,
                'errors': [str(e)],
                'warnings': []
            }
    
    def calculate_score(self, schema_data: Dict) -> int:
        """Calculate validation score based on schema completeness."""
        score = 0
        
        # Required fields (40 points)
        required_count = sum(1 for field in REQUIRED_FIELDS if field in schema_data)
        score += (required_count / len(REQUIRED_FIELDS)) * 40
        
        # Recommended fields (30 points)
        recommended_count = sum(1 for field in RECOMMENDED_FIELDS if field in schema_data)
        score += (recommended_count / len(RECOMMENDED_FIELDS)) * 30
        
        # Additional fields (30 points)
        total_fields = len(schema_data)
        if total_fields > len(REQUIRED_FIELDS) + len(RECOMMENDED_FIELDS):
            score += min(30, (total_fields - len(REQUIRED_FIELDS) - len(RECOMMENDED_FIELDS)) * 2)
        
        return min(100, int(score))
    
    def get_warnings(self, schema_data: Dict) -> List[str]:
        """Get validation warnings."""
        warnings = []
        
        for field in RECOMMENDED_FIELDS:
            if field not in schema_data:
                warnings.append(f"Missing recommended field: {field}")
        
        return warnings
    
    async def validate_urls(self, urls: List[str]) -> List[Dict]:
        """Validate multiple URLs with concurrency control."""
        self.state.start()
        results = []
        
        # Process URLs in batches
        for i in range(0, len(urls), self.concurrent_limit):
            if self.state.should_stop:
                break
                
            # Wait if paused
            while self.state.is_paused and not self.state.should_stop:
                await asyncio.sleep(0.1)
            
            if self.state.should_stop:
                break
            
            # Process batch
            batch = urls[i:i + self.concurrent_limit]
            tasks = [self.validate_url(url) for url in batch]
            
            try:
                batch_results = await asyncio.gather(*tasks, return_exceptions=True)
                
                for result in batch_results:
                    if isinstance(result, Exception):
                        results.append({
                            'url': 'unknown',
                            'status': 'error',
                            'schema_data': {},
                            'response_time': 0,
                            'score': 0,
                            'errors': [str(result)],
                            'warnings': []
                        })
                    else:
                        results.append(result)
                        
                        # Call progress callback
                        if self.progress_callback:
                            try:
                                self.progress_callback({
                                    'url': result['url'],
                                    'result': result,
                                    'progress': len(results),
                                    'total': len(urls)
                                })
                            except Exception as e:
                                print(f"Error in progress callback: {e}")
                
                # Add delay between batches
                if i + self.concurrent_limit < len(urls):
                    delay = random.uniform(self.delay_min, self.delay_max)
                    await asyncio.sleep(delay)
                    
            except Exception as e:
                print(f"Error processing batch: {e}")
                continue
        
        self.state.reset()
        return results
