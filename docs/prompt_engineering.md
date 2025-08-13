# Prompt Engineering Documentation

## Overview

This document outlines the prompt engineering strategy used in the AI-powered Menu Intelligence Widget for generating menu descriptions and upsell suggestions.

## Core Prompt Structure

### System Role
```
You are a professional restaurant menu writer and marketing expert.
```

### Main Task Prompt
```
Task: Create content for a food item called "{item_name}"

Requirements:
1. Generate a compelling menu description (maximum 30 words) that:
   - Highlights key ingredients and flavors
   - Uses appetizing language
   - Appeals to customer emotions
   - Is concise and scannable

2. Suggest ONE upsell combo item that:
   - Complements the main item
   - Is realistic for a restaurant setting
   - Has clear value proposition
   - Uses persuasive language

Format your response as JSON:
{
    "description": "Your menu description here (max 30 words)",
    "upsell_suggestion": "Your upsell combo suggestion here"
}
```

## Prompt Engineering Principles

### 1. Clarity
- **Clear Role Definition**: Establishes the AI as a "professional restaurant menu writer and marketing expert"
- **Specific Task**: Clearly defines what needs to be generated
- **Structured Requirements**: Breaks down requirements into specific, actionable points

### 2. Control
- **Word Limit**: Enforces 30-word maximum for descriptions
- **Format Specification**: Requires JSON response format
- **Single Upsell**: Limits to one suggestion to avoid overwhelming users
- **Realistic Constraints**: Ensures suggestions are practical for restaurant settings

### 3. Context
- **Restaurant Context**: Emphasizes restaurant-specific language and constraints
- **Customer Focus**: Directs attention to customer appeal and emotions
- **Marketing Perspective**: Incorporates persuasive language and value propositions

## Prompt Optimization Strategies

### 1. Example-Based Learning
```
Example for "Margherita Pizza":
{
    "description": "Fresh mozzarella, basil, and tomato sauce on crispy crust",
    "upsell_suggestion": "Pair it with a refreshing Italian soda for the perfect meal!"
}
```

**Benefits:**
- Provides clear format expectations
- Demonstrates appropriate tone and style
- Shows realistic word count and content

### 2. Constraint Specification
- **Word Limits**: Prevents overly verbose responses
- **Format Requirements**: Ensures consistent, parseable output
- **Content Guidelines**: Directs focus on key elements

### 3. Contextual Framing
- **Professional Role**: Establishes expertise and authority
- **Business Context**: Ensures practical, actionable suggestions
- **Customer Perspective**: Focuses on appeal and persuasion

## Model-Specific Considerations

### GPT-3.5-turbo
- **Temperature**: 0.7 (balanced creativity and consistency)
- **Max Tokens**: 200 (sufficient for concise responses)
- **System Message**: Reinforces professional role

### GPT-4
- **Enhanced Creativity**: Better understanding of nuanced requirements
- **Improved Formatting**: More reliable JSON output
- **Context Awareness**: Better grasp of restaurant industry specifics

## Error Handling and Fallbacks

### JSON Parsing Failures
If the AI response cannot be parsed as JSON, the system falls back to:
```python
{
    "description": f"Delicious {item_name} made with fresh ingredients and authentic flavors.",
    "upsell_suggestion": f"Pair your {item_name} with a refreshing beverage for the perfect dining experience!"
}
```

### API Failures
- **Simulation Mode**: Pre-defined responses for common food items
- **Graceful Degradation**: Maintains functionality even without API access
- **User Feedback**: Clear error messages and retry mechanisms

## Prompt Evaluation Metrics

### Success Criteria
1. **Format Compliance**: Response is valid JSON
2. **Word Count**: Description within 30-word limit
3. **Relevance**: Content matches food item type
4. **Appeal**: Language is appetizing and persuasive
5. **Practicality**: Upsell suggestions are realistic

### Quality Indicators
- **Consistency**: Similar items produce similar quality output
- **Creativity**: Varied language while maintaining professionalism
- **Accuracy**: Descriptions match expected food characteristics
- **Effectiveness**: Upsell suggestions are compelling

## Integration Considerations

### POS System Integration
The prompt is designed to generate content that can be directly used in:
- **Menu Management Systems**: Descriptions fit standard menu layouts
- **Order Systems**: Upsell suggestions can trigger combo offers
- **Marketing Materials**: Content is ready for promotional use

### Scalability
- **Template-Based**: Easy to modify for different restaurant types
- **Localization-Ready**: Can be adapted for different cuisines and cultures
- **Customizable**: Parameters can be adjusted for specific business needs

## Future Enhancements

### Potential Improvements
1. **Cuisine-Specific Prompts**: Tailored prompts for different food types
2. **Seasonal Context**: Incorporate seasonal ingredients and themes
3. **Price Integration**: Include pricing considerations in upsell suggestions
4. **Dietary Restrictions**: Account for vegetarian, vegan, gluten-free options
5. **Cultural Sensitivity**: Adapt language for different cultural contexts

### Advanced Features
- **A/B Testing**: Compare different prompt variations
- **Performance Analytics**: Track which prompts generate better results
- **Dynamic Prompting**: Adjust prompts based on user feedback
- **Multi-Language Support**: Extend to different languages
