"""
Schema.org Product schema definitions and validation rules.
"""

# Schema.org Product schema definition
PRODUCT_SCHEMA = {
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
REQUIRED_FIELDS = ["name", "image", "offers"]

# Recommended fields for better SEO
RECOMMENDED_FIELDS = ["description", "brand", "sku", "gtin", "aggregateRating", "review"]

