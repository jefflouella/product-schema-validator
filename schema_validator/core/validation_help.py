"""
Validation help content for errors and warnings.
Comprehensive help system based on schema.org Product specification and common validation issues.
"""

VALIDATION_HELP = {
    # Schema validation errors (from JSON Schema validation)
    "Schema validation error": {
        "title": "Schema Validation Error",
        "description": "The structured data on this page doesn't conform to the schema.org Product specification.",
        "fix": "Ensure your JSON-LD, microdata, or RDFa markup follows the correct schema.org Product format. Check for typos, missing quotes, or incorrect nesting.",
        "example": "Make sure your markup looks like: {\"@type\": \"Product\", \"name\": \"Product Name\", \"image\": \"image.jpg\", \"offers\": {\"@type\": \"Offer\", \"price\": \"29.99\"}}",
        "resources": [
            "https://schema.org/Product",
            "https://developers.google.com/search/docs/appearance/structured-data/product"
        ]
    },
    
    "Schema definition error": {
        "title": "Schema Definition Error", 
        "description": "There's a fundamental issue with how the schema is structured or defined.",
        "fix": "Check that your schema markup is valid JSON and properly formatted. Ensure all brackets, braces, and quotes are properly closed.",
        "example": "Use a JSON validator to check your markup syntax before implementing on your site.",
        "resources": [
            "https://jsonlint.com/",
            "https://validator.schema.org/"
        ]
    },
    
    # Required field errors
    "Missing required field: name": {
        "title": "Missing Product Name",
        "description": "The product name is required for all Product schema markup. This is the most important field as it identifies the product.",
        "fix": "Add a 'name' property to your Product schema with the product's name. This should be the exact product name as it appears on your site.",
        "example": '"name": "iPhone 15 Pro Max 256GB - Natural Titanium"',
        "resources": [
            "https://schema.org/Product#name"
        ]
    },
    
    "Missing required field: image": {
        "title": "Missing Product Image",
        "description": "Product images are required to help users identify the product in search results and rich snippets.",
        "fix": "Add an 'image' property with the URL of your product image. You can provide a single image or an array of images.",
        "example": '"image": "https://example.com/product.jpg" or "image": ["https://example.com/product1.jpg", "https://example.com/product2.jpg"]',
        "resources": [
            "https://schema.org/Product#image"
        ]
    },
    
    "Missing required field: offers": {
        "title": "Missing Product Offers",
        "description": "Product pricing and availability information is required for e-commerce products to appear in rich results.",
        "fix": "Add an 'offers' property with Offer schema containing price, currency, and availability information.",
        "example": '"offers": {"@type": "Offer", "price": "29.99", "priceCurrency": "USD", "availability": "InStock"}',
        "resources": [
            "https://schema.org/Product#offers",
            "https://schema.org/Offer"
        ]
    },
    
    # Offer field errors
    "Missing required offer field: price": {
        "title": "Missing Price Information",
        "description": "The price is required within the offers object to enable price display in search results.",
        "fix": "Add a 'price' property inside your offers object with the product price as a string.",
        "example": '"offers": {"@type": "Offer", "price": "29.99", "priceCurrency": "USD", "availability": "InStock"}',
        "resources": [
            "https://schema.org/Offer#price"
        ]
    },
    
    "Missing required offer field: priceCurrency": {
        "title": "Missing Price Currency",
        "description": "The currency code is required to specify what currency the price is in.",
        "fix": "Add a 'priceCurrency' property with a valid 3-letter ISO currency code (e.g., USD, EUR, GBP, CAD).",
        "example": '"priceCurrency": "USD"',
        "resources": [
            "https://schema.org/Offer#priceCurrency",
            "https://en.wikipedia.org/wiki/ISO_4217"
        ]
    },
    
    "Missing required offer field: availability": {
        "title": "Missing Availability Information",
        "description": "Product availability status is required for proper inventory management and search result display.",
        "fix": "Add an 'availability' property with one of these values: InStock, OutOfStock, PreOrder, or LimitedAvailability.",
        "example": '"availability": "InStock"',
        "resources": [
            "https://schema.org/ItemAvailability",
            "https://schema.org/Offer#availability"
        ]
    },
    
    "Offers must be an object": {
        "title": "Invalid Offers Format",
        "description": "The offers property must be an object, not a string or array.",
        "fix": "Ensure your offers property is structured as an object with Offer schema properties.",
        "example": '"offers": {"@type": "Offer", "price": "29.99", "priceCurrency": "USD", "availability": "InStock"}',
        "resources": [
            "https://schema.org/Offer"
        ]
    },
    
    # Price format errors
    "Price format invalid": {
        "title": "Invalid Price Format",
        "description": "The price should be formatted as a decimal number with up to 2 decimal places.",
        "fix": "Format your price as a string with numbers and optional decimal point (e.g., '29.99', '100', '15.50').",
        "example": '"price": "29.99" (not 29.99 or $29.99)',
        "resources": [
            "https://schema.org/Offer#price"
        ]
    },
    
    "Invalid currency code": {
        "title": "Invalid Currency Code",
        "description": "The currency code must be a valid 3-letter ISO 4217 currency code.",
        "fix": "Use a valid ISO currency code like USD, EUR, GBP, CAD, AUD, etc.",
        "example": '"priceCurrency": "USD" (not $ or US$)',
        "resources": [
            "https://en.wikipedia.org/wiki/ISO_4217"
        ]
    },
    
    "Invalid availability value": {
        "title": "Invalid Availability Value",
        "description": "The availability value must be one of the predefined schema.org values.",
        "fix": "Use one of these exact values: InStock, OutOfStock, PreOrder, LimitedAvailability.",
        "example": '"availability": "InStock" (not "in stock" or "available")',
        "resources": [
            "https://schema.org/ItemAvailability"
        ]
    },
    
    # Image format errors
    "Invalid image URL": {
        "title": "Invalid Image URL",
        "description": "The image URL must be a valid, accessible URL pointing to an image file.",
        "fix": "Ensure your image URLs are absolute URLs (starting with http:// or https://) and point to accessible image files.",
        "example": '"image": "https://example.com/images/product.jpg"',
        "resources": [
            "https://schema.org/Product#image"
        ]
    },
    
    "Image not accessible": {
        "title": "Image Not Accessible",
        "description": "The image URL returns an error or is not accessible.",
        "fix": "Check that the image URL is correct and the image file exists and is publicly accessible.",
        "example": "Test the image URL in your browser to ensure it loads properly.",
        "resources": [
            "https://schema.org/Product#image"
        ]
    },
    
    # Recommended field warnings
    "Missing recommended field: description": {
        "title": "Missing Product Description",
        "description": "While not required, a product description helps search engines and users understand what the product is and can improve click-through rates.",
        "fix": "Add a 'description' property with a detailed description of your product (typically 150-300 characters).",
        "example": '"description": "High-quality wireless headphones with active noise cancellation and 30-hour battery life."',
        "resources": [
            "https://schema.org/Product#description"
        ]
    },
    
    "Missing recommended field: brand": {
        "title": "Missing Brand Information",
        "description": "Brand information helps users identify and trust your product, and can improve search result appearance.",
        "fix": "Add a 'brand' property with the manufacturer or brand name.",
        "example": '"brand": "Apple" or "brand": {"@type": "Brand", "name": "Apple"}',
        "resources": [
            "https://schema.org/Product#brand",
            "https://schema.org/Brand"
        ]
    },
    
    "Missing recommended field: sku": {
        "title": "Required SKU",
        "description": "A Stock Keeping Unit (SKU) is required to help with inventory management and product identification.",
        "fix": "Add a 'sku' property with your product's unique identifier.",
        "example": '"sku": "IPHONE-15-PRO-256-NATURAL"',
        "resources": [
            "https://schema.org/Product#sku"
        ]
    },
    
    "Missing recommended field: gtin": {
        "title": "Missing GTIN",
        "description": "Global Trade Item Numbers (GTIN) help with product identification across different systems and platforms.",
        "fix": "Add a 'gtin' property with the product's barcode number (UPC, EAN, ISBN, etc.).",
        "example": '"gtin": "123456789012" or "gtin": ["123456789012", "987654321098"]',
        "resources": [
            "https://schema.org/Product#gtin"
        ]
    },
    
    "Missing recommended field: aggregateRating": {
        "title": "Missing Product Ratings",
        "description": "Product ratings help build trust and can improve click-through rates in search results.",
        "fix": "Add an 'aggregateRating' property with overall rating information from customer reviews.",
        "example": '"aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.5", "reviewCount": "127"}',
        "resources": [
            "https://schema.org/Product#aggregateRating",
            "https://schema.org/AggregateRating"
        ]
    },
    
    "Missing recommended field: review": {
        "title": "Missing Product Reviews",
        "description": "Customer reviews provide social proof and detailed feedback about your product.",
        "fix": "Add a 'review' property with customer review information.",
        "example": '"review": [{"@type": "Review", "author": "John Doe", "reviewRating": {"@type": "Rating", "ratingValue": "5"}}]',
        "resources": [
            "https://schema.org/Product#review",
            "https://schema.org/Review"
        ]
    },
    
    # Rating validation errors
    "Invalid rating value": {
        "title": "Invalid Rating Value",
        "description": "Rating values must be numbers between 1 and 5 (or the maximum value for your rating scale).",
        "fix": "Ensure rating values are numeric and within the valid range for your rating system.",
        "example": '"ratingValue": "4.5" (not "4.5 stars" or "excellent")',
        "resources": [
            "https://schema.org/Rating#ratingValue"
        ]
    },
    
    "Invalid review count": {
        "title": "Invalid Review Count",
        "description": "Review count must be a non-negative integer.",
        "fix": "Ensure review count is a whole number (integer) that's 0 or greater.",
        "example": '"reviewCount": "127" (not "127 reviews" or "127.5")',
        "resources": [
            "https://schema.org/AggregateRating#reviewCount"
        ]
    },
    
    # General errors
    "No schema data found": {
        "title": "No Product Schema Found",
        "description": "No structured data markup was found on this page.",
        "fix": "Add schema.org Product markup to your page using JSON-LD, microdata, or RDFa format.",
        "example": "Include JSON-LD script tag with Product schema in your page's <head> section.",
        "resources": [
            "https://schema.org/Product",
            "https://developers.google.com/search/docs/appearance/structured-data/product"
        ]
    },
    
    "No Product schema found": {
        "title": "No Product Schema Detected",
        "description": "The page loaded successfully but no Product schema markup was found.",
        "fix": "Implement schema.org Product markup on your product pages to help search engines understand your content.",
        "example": "Add structured data markup using tools like Google's Structured Data Markup Helper.",
        "resources": [
            "https://developers.google.com/search/docs/appearance/structured-data/product",
            "https://search.google.com/test/rich-results"
        ]
    },
    
    # HTTP errors
    "HTTP 404": {
        "title": "Page Not Found (404)",
        "description": "The URL returned a 404 error, meaning the page was not found.",
        "fix": "Check that the URL is correct and the page exists. Update any broken links.",
        "example": "Verify the URL is accessible by visiting it directly in your browser.",
        "resources": [
            "https://support.google.com/webmasters/answer/9370220"
        ]
    },
    
    "HTTP 500": {
        "title": "Server Error (500)",
        "description": "The server encountered an internal error when trying to load the page.",
        "fix": "This is a server-side issue. Check your website's server logs and ensure the page is working properly.",
        "example": "Contact your web developer or hosting provider to resolve server issues.",
        "resources": [
            "https://support.google.com/webmasters/answer/9370220"
        ]
    },
    
    # Network/timeout errors
    "Timeout": {
        "title": "Page Load Timeout",
        "description": "The page took too long to load and timed out.",
        "fix": "Optimize your page loading speed or increase the timeout setting in your validation configuration.",
        "example": "Check your page's loading performance using tools like Google PageSpeed Insights.",
        "resources": [
            "https://developers.google.com/speed/pagespeed/insights/"
        ]
    },
    
    "Blocked": {
        "title": "Crawler Blocked",
        "description": "The crawler was blocked from accessing the page, possibly due to bot protection or rate limiting.",
        "fix": "Check if your site has bot protection that might be blocking automated crawlers. Consider whitelisting the crawler's user agent.",
        "example": "Review your site's robots.txt file and bot protection settings.",
        "resources": [
            "https://developers.google.com/search/docs/crawling-indexing/robots/intro"
        ]
    }
}