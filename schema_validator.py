#!/usr/bin/env python3
"""
Product Schema Validator with Anti-Bot Bypass
Validates schema.org Product markup across URLs while handling Cloudflare protection.
"""

import asyncio
import json
import random
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

import jsonschema
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from tqdm import tqdm
import validators


class SchemaValidator:
    """Validates Product schema markup with anti-bot bypass capabilities."""
    
    def __init__(self, 
                 headless: bool = True,
                 timeout: int = 30000,
                 delay_range: Tuple[int, int] = (2, 5),
                 max_retries: int = 1,
                 concurrent_limit: int = 3):
        self.headless = headless
        self.timeout = timeout
        self.delay_range = delay_range
        self.max_retries = max_retries
        self.concurrent_limit = concurrent_limit
        
        # User agents for rotation
        self.user_agents = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"
        ]
        
        # Schema.org Product schema definition
        self.product_schema = {
            "type": "object",
            "properties": {
                "@type": {"const": "Product"},
                "name": {"type": "string", "minLength": 1},
                "description": {"type": "string", "minLength": 1},
                "image": {
                    "oneOf": [
                        {"type": "string", "format": "uri"},
                        {"type": "array", "items": {"type": "string", "format": "uri"}}
                    ]
                },
                "offers": {
                    "type": "object",
                    "properties": {
                        "@type": {"const": "Offer"},
                        "price": {"type": "string", "pattern": r"^\d+(\.\d{2})?$"},
                        "priceCurrency": {"type": "string", "pattern": r"^[A-Z]{3}$"},
                        "availability": {
                            "type": "string",
                            "enum": ["InStock", "OutOfStock", "PreOrder", "LimitedAvailability"]
                        }
                    },
                    "required": ["price", "priceCurrency", "availability"]
                },
                "brand": {"type": "string"},
                "sku": {"type": "string"},
                "gtin": {"type": "string"},
                "aggregateRating": {
                    "type": "object",
                    "properties": {
                        "@type": {"const": "AggregateRating"},
                        "ratingValue": {"type": "number", "minimum": 1, "maximum": 5},
                        "reviewCount": {"type": "integer", "minimum": 0}
                    }
                },
                "review": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "@type": {"const": "Review"},
                            "author": {"type": "string"},
                            "reviewRating": {
                                "type": "object",
                                "properties": {
                                    "@type": {"const": "Rating"},
                                    "ratingValue": {"type": "number", "minimum": 1, "maximum": 5}
                                }
                            }
                        }
                    }
                }
            },
            "required": ["@type", "name", "image", "offers"]
        }
        
        # Required fields for minimum validation
        self.required_fields = ["name", "image", "offers"]
        self.recommended_fields = ["description", "brand", "sku", "gtin", "aggregateRating", "review"]

    async def create_browser_context(self, playwright) -> Tuple[Browser, BrowserContext]:
        """Create browser with stealth settings."""
        browser = await playwright.chromium.launch(
            headless=self.headless,
            args=[
                '--no-sandbox',
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor'
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
            # Wait for page to load completely
            await page.wait_for_load_state('networkidle', timeout=self.timeout)
            
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

    async def process_urls(self, urls: List[str]) -> List[Dict]:
        """Process all URLs with rate limiting and concurrency control."""
        results = []
        semaphore = asyncio.Semaphore(self.concurrent_limit)
        
        async def process_with_semaphore(url):
            async with semaphore:
                async with async_playwright() as p:
                    browser, context = await self.create_browser_context(p)
                    page = await context.new_page()
                    
                    try:
                        result = await self.process_url(page, url)
                        return result
                    finally:
                        await browser.close()
        
        # Process URLs with progress bar
        tasks = [process_with_semaphore(url) for url in urls]
        
        with tqdm(total=len(urls), desc="Processing URLs") as pbar:
            for coro in asyncio.as_completed(tasks):
                result = await coro
                results.append(result)
                pbar.update(1)
                
                # Rate limiting
                delay = random.uniform(*self.delay_range)
                await asyncio.sleep(delay)
        
        return results

    async def validate_urls(self, urls_file: str = "urls.txt") -> List[Dict]:
        """Main method to validate URLs from file."""
        urls_path = Path(urls_file)
        if not urls_path.exists():
            raise FileNotFoundError(f"URLs file not found: {urls_file}")
        
        # Read URLs
        with open(urls_path, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
        
        print(f"Found {len(urls)} URLs to validate")
        
        # Validate URLs format
        valid_urls = []
        for url in urls:
            if validators.url(url):
                valid_urls.append(url)
            else:
                print(f"Invalid URL skipped: {url}")
        
        print(f"Processing {len(valid_urls)} valid URLs...")
        
        # Process URLs
        results = await self.process_urls(valid_urls)
        
        # Save results
        results_path = Path("results/validation_results.json")
        results_path.parent.mkdir(exist_ok=True)
        
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Print summary
        success_count = sum(1 for r in results if r['status'] == 'success')
        warning_count = sum(1 for r in results if r['status'] == 'warning')
        error_count = sum(1 for r in results if r['status'] == 'error')
        
        print(f"\nValidation Summary:")
        print(f"Total URLs: {len(results)}")
        print(f"Success: {success_count}")
        print(f"Warnings: {warning_count}")
        print(f"Errors: {error_count}")
        print(f"Success Rate: {(success_count / len(results) * 100):.1f}%")
        
        return results


async def main():
    """Main entry point."""
    validator = SchemaValidator(
        headless=True,
        timeout=30000,
        delay_range=(2, 5),
        max_retries=1,
        concurrent_limit=3
    )
    
    try:
        results = await validator.validate_urls()
        print(f"\nResults saved to: results/validation_results.json")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
