# Validation Help Content Style Guide

This style guide ensures consistency and quality across all validation help content in the Product Schema Validator.

## Content Structure

Each help entry must follow this exact structure:

```json
{
    "title": "Brief, Clear Title",
    "description": "Detailed explanation of what the error/warning means",
    "fix": "Specific, actionable steps to resolve the issue",
    "example": "Concrete example showing the correct implementation",
    "resources": [
        "URL to relevant documentation",
        "Additional helpful resources"
    ]
}
```

## Writing Guidelines

### Title
- **Format**: Clear, concise, and descriptive
- **Length**: 2-8 words maximum
- **Style**: Use title case, no ending punctuation
- **Examples**:
  - ✅ "Missing Product Name"
  - ✅ "Invalid Price Format"
  - ❌ "This is an error about the product name being missing"
  - ❌ "missing product name"

### Description
- **Purpose**: Explain what the error/warning means and why it matters
- **Length**: 1-3 sentences, 20-60 words
- **Tone**: Professional, informative, non-alarmist
- **Focus**: User impact and SEO implications
- **Examples**:
  - ✅ "The product name is required for all Product schema markup. This is the most important field as it identifies the product."
  - ❌ "You need to add a name field because it's required."

### Fix
- **Purpose**: Provide specific, actionable steps to resolve the issue
- **Length**: 1-3 sentences, 15-50 words
- **Tone**: Direct, instructional
- **Format**: Start with action verb when possible
- **Examples**:
  - ✅ "Add a 'name' property to your Product schema with the product's name. This should be the exact product name as it appears on your site."
  - ❌ "You should probably add a name field to your schema."

### Example
- **Purpose**: Show concrete, copy-pasteable code examples
- **Format**: Always show the correct implementation
- **Style**: Use actual schema markup, not pseudo-code
- **Context**: Include enough context to be helpful
- **Examples**:
  - ✅ `"name": "iPhone 15 Pro Max 256GB - Natural Titanium"`
  - ✅ `"offers": {"@type": "Offer", "price": "29.99", "priceCurrency": "USD", "availability": "InStock"}`
  - ❌ "Add a name field with your product name"
  - ❌ `"name": "Your Product Name"`

### Resources
- **Purpose**: Link to authoritative documentation and tools
- **Count**: 1-3 resources per entry
- **Priority**: Official schema.org docs first, then Google docs, then tools
- **Format**: Full URLs, no shortened links
- **Validation**: All links must be tested and working

## Content Categories

### Error Types (Priority Order)
1. **Schema Validation Errors** - JSON schema compliance issues
2. **Required Field Errors** - Missing mandatory fields
3. **Offer Field Errors** - Issues with pricing/availability data
4. **Format Validation Errors** - Invalid data formats
5. **Image Errors** - Image URL and accessibility issues
6. **HTTP Errors** - Server response errors
7. **Network Errors** - Timeout and blocking issues

### Warning Types (Priority Order)
1. **Missing Recommended Fields** - Optional but beneficial fields
2. **Rating/Review Issues** - Problems with rating data
3. **Brand/SKU Issues** - Product identification problems

## Naming Conventions

### Error Message Keys
- Use exact error message text as the key
- Include full context (e.g., "Missing required field: name" not just "name")
- Maintain case sensitivity
- Use colons and spaces as they appear in actual errors

### File Organization
- All help content goes in `validation_help.py`
- Use clear section comments to group related entries
- Maintain alphabetical order within each category
- Keep entries under 100 lines each

## Quality Standards

### Technical Accuracy
- All examples must be valid schema.org markup
- Currency codes must be valid ISO 4217 codes
- Availability values must match schema.org enum values
- All URLs must be current and working

### User Experience
- Help content should reduce user confusion, not increase it
- Avoid technical jargon when possible
- Focus on practical solutions, not theoretical explanations
- Always provide actionable next steps

### Consistency
- Use consistent terminology throughout
- Maintain consistent formatting and structure
- Use the same tone and voice across all entries
- Follow the established example patterns

## Review Checklist

Before adding new help content, verify:

- [ ] Title follows naming conventions
- [ ] Description explains the "why" not just the "what"
- [ ] Fix provides specific, actionable steps
- [ ] Example is copy-pasteable and correct
- [ ] Resources are current and authoritative
- [ ] Content matches the established tone and style
- [ ] Technical details are accurate
- [ ] Entry fits logically into the existing structure

## Common Patterns

### Missing Field Pattern
```json
{
    "title": "Missing [Field Name]",
    "description": "The [field] is required for [reason]. [Additional context about importance].",
    "fix": "Add a '[field]' property to your Product schema with [specific requirements].",
    "example": "\"[field]\": \"[realistic example value]\"",
    "resources": ["https://schema.org/Product#[field]"]
}
```

### Invalid Format Pattern
```json
{
    "title": "Invalid [Field] Format",
    "description": "The [field] must be formatted according to schema.org requirements.",
    "fix": "Format your [field] as [specific requirements].",
    "example": "\"[field]\": \"[correct format]\" (not [incorrect format])",
    "resources": ["https://schema.org/Offer#[field]"]
}
```

### HTTP Error Pattern
```json
{
    "title": "[Error Name] ([Code])",
    "description": "The URL returned a [code] error, meaning [explanation].",
    "fix": "[Specific steps to resolve the issue].",
    "example": "[Practical example of what to check].",
    "resources": ["https://support.google.com/webmasters/answer/9370220"]
}
```

## Maintenance

### Regular Updates
- Review and update help content quarterly
- Check all resource links monthly
- Update examples when schema.org specifications change
- Add new entries as validation logic expands

### Version Control
- Track changes to help content in git commits
- Document why content was added or modified
- Maintain backward compatibility for existing help keys
- Test all new content with actual validation scenarios

This style guide ensures that all validation help content is consistent, accurate, and helpful to users working with schema.org Product markup.
