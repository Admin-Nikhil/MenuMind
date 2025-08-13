# Grafterr POS Integration Guide

## Overview

This document provides detailed instructions for integrating the AI-powered Menu Intelligence Widget into Grafterr's POS item management system.

## Integration Architecture

### Frontend Integration
```javascript
// Example: Embedding the widget in Grafterr's item creation form
import MenuIntelligenceWidget from './components/MenuIntelligenceWidget';

function ItemCreationForm() {
  const [itemName, setItemName] = useState('');
  const [generatedDescription, setGeneratedDescription] = useState('');
  const [upsellSuggestion, setUpsellSuggestion] = useState('');

  const handleAIGeneration = async (itemName) => {
    try {
      const response = await fetch('/api/generate-item-details', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ item_name: itemName })
      });
      
      const data = await response.json();
      setGeneratedDescription(data.description);
      setUpsellSuggestion(data.upsell_suggestion);
    } catch (error) {
      console.error('AI generation failed:', error);
    }
  };

  return (
    <div className="item-creation-form">
      <input 
        value={itemName}
        onChange={(e) => setItemName(e.target.value)}
        placeholder="Enter item name"
      />
      
      {/* AI Widget Integration */}
      <MenuIntelligenceWidget
        itemName={itemName}
        onGenerate={handleAIGeneration}
        onDescriptionGenerated={setGeneratedDescription}
        onUpsellGenerated={setUpsellSuggestion}
      />
      
      <textarea 
        value={generatedDescription}
        onChange={(e) => setGeneratedDescription(e.target.value)}
        placeholder="Menu description"
      />
      
      <textarea 
        value={upsellSuggestion}
        onChange={(e) => setUpsellSuggestion(e.target.value)}
        placeholder="Upsell suggestion"
      />
    </div>
  );
}
```

### Backend Integration
```python
# Example: Grafterr backend API integration
from flask import Blueprint, request, jsonify
from .menu_intelligence import generate_menu_content

menu_intelligence_bp = Blueprint('menu_intelligence', __name__)

@menu_intelligence_bp.route('/api/generate-item-details', methods=['POST'])
def generate_item_details():
    """Generate AI-powered menu content for Grafterr items"""
    try:
        data = request.get_json()
        item_name = data.get('item_name')
        
        # Generate content using our AI service
        result = generate_menu_content(item_name)
        
        # Store in Grafterr's database
        item = Item(
            name=item_name,
            description=result['description'],
            upsell_suggestion=result['upsell_suggestion'],
            ai_generated=True,
            generated_at=datetime.now()
        )
        
        db.session.add(item)
        db.session.commit()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

## Database Schema Integration

### Item Table Extensions
```sql
-- Add AI-generated content fields to existing items table
ALTER TABLE items ADD COLUMN ai_description TEXT;
ALTER TABLE items ADD COLUMN upsell_suggestion TEXT;
ALTER TABLE items ADD COLUMN ai_generated BOOLEAN DEFAULT FALSE;
ALTER TABLE items ADD COLUMN ai_model_used VARCHAR(50);
ALTER TABLE items ADD COLUMN ai_generated_at TIMESTAMP;
```

### Upsell Combinations Table
```sql
-- New table for managing upsell combinations
CREATE TABLE upsell_combinations (
    id SERIAL PRIMARY KEY,
    main_item_id INTEGER REFERENCES items(id),
    suggested_item_id INTEGER REFERENCES items(id),
    suggestion_text TEXT,
    ai_generated BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);
```

## User Interface Integration

### 1. Item Creation/Editing Screen
```jsx
// Enhanced item form with AI widget
function ItemForm({ item, onSave }) {
  const [showAIWidget, setShowAIWidget] = useState(false);
  
  return (
    <div className="item-form">
      <div className="form-section">
        <label>Item Name</label>
        <input value={item.name} onChange={handleNameChange} />
        
        {/* AI Generation Button */}
        <button 
          type="button" 
          onClick={() => setShowAIWidget(true)}
          className="ai-generate-btn"
        >
          <SparklesIcon /> Generate AI Content
        </button>
      </div>
      
      {/* AI Widget Modal */}
      {showAIWidget && (
        <AIModal
          itemName={item.name}
          onGenerate={handleAIGeneration}
          onClose={() => setShowAIWidget(false)}
        />
      )}
      
      <div className="form-section">
        <label>Description</label>
        <textarea 
          value={item.description} 
          onChange={handleDescriptionChange}
          placeholder="Enter item description or use AI to generate"
        />
      </div>
      
      <div className="form-section">
        <label>Upsell Suggestion</label>
        <textarea 
          value={item.upsell_suggestion} 
          onChange={handleUpsellChange}
          placeholder="Enter upsell suggestion or use AI to generate"
        />
      </div>
    </div>
  );
}
```

### 2. Menu Management Dashboard
```jsx
// AI-powered menu management dashboard
function MenuManagementDashboard() {
  const [items, setItems] = useState([]);
  const [selectedItems, setSelectedItems] = useState([]);
  
  const handleBulkAIGeneration = async () => {
    for (const item of selectedItems) {
      if (!item.description || !item.upsell_suggestion) {
        await generateAIContent(item.id, item.name);
      }
    }
  };
  
  return (
    <div className="menu-dashboard">
      <div className="dashboard-header">
        <h2>Menu Management</h2>
        <button onClick={handleBulkAIGeneration}>
          Generate AI Content for Selected
        </button>
      </div>
      
      <div className="items-grid">
        {items.map(item => (
          <ItemCard 
            key={item.id}
            item={item}
            onSelect={() => handleItemSelect(item.id)}
            showAIIndicator={item.ai_generated}
          />
        ))}
      </div>
    </div>
  );
}
```

## API Endpoints for Grafterr

### 1. Menu Intelligence API
```python
# Grafterr API endpoints
@api.route('/menu-intelligence/generate', methods=['POST'])
@require_auth
def generate_menu_content():
    """Generate AI content for menu items"""
    pass

@api.route('/menu-intelligence/bulk-generate', methods=['POST'])
@require_auth
def bulk_generate_content():
    """Generate AI content for multiple items"""
    pass

@api.route('/menu-intelligence/suggestions', methods=['GET'])
@require_auth
def get_upsell_suggestions():
    """Get upsell suggestions for an item"""
    pass

@api.route('/menu-intelligence/analytics', methods=['GET'])
@require_auth
def get_ai_analytics():
    """Get analytics on AI-generated content performance"""
    pass
```

### 2. Configuration Management
```python
# AI configuration management
@api.route('/menu-intelligence/config', methods=['GET', 'PUT'])
@require_auth
def manage_ai_config():
    """Manage AI model preferences and settings"""
    pass
```

## Security Considerations

### 1. Authentication & Authorization
```python
# Ensure only authorized users can access AI features
@require_auth
@require_permission('menu_management')
def generate_menu_content():
    # Implementation
    pass
```

### 2. Rate Limiting
```python
# Apply rate limiting to prevent abuse
@limiter.limit("10 per minute")
def generate_menu_content():
    # Implementation
    pass
```

### 3. Input Validation
```python
# Validate all inputs before processing
def validate_item_name(item_name):
    if not item_name or len(item_name) > 100:
        raise ValueError("Invalid item name")
    return sanitize_input(item_name)
```

## Performance Optimization

### 1. Caching Strategy
```python
# Cache AI responses to reduce API calls
@cache.memoize(timeout=3600)  # Cache for 1 hour
def get_cached_ai_response(item_name, model):
    return generate_ai_response(item_name, model)
```

### 2. Batch Processing
```python
# Process multiple items in batches
def bulk_generate_content(item_names):
    results = []
    for batch in chunk_items(item_names, batch_size=5):
        batch_results = process_batch(batch)
        results.extend(batch_results)
    return results
```

## Monitoring & Analytics

### 1. Usage Tracking
```python
# Track AI feature usage
def track_ai_usage(user_id, action, item_name, model_used):
    analytics.track('ai_menu_generation', {
        'user_id': user_id,
        'action': action,
        'item_name': item_name,
        'model_used': model_used,
        'timestamp': datetime.now()
    })
```

### 2. Performance Metrics
```python
# Monitor AI response times and success rates
def monitor_ai_performance():
    metrics = {
        'response_time': measure_response_time(),
        'success_rate': calculate_success_rate(),
        'error_rate': calculate_error_rate(),
        'user_satisfaction': get_user_feedback()
    }
    return metrics
```

## Deployment Considerations

### 1. Environment Configuration
```bash
# Production environment variables
OPENAI_API_KEY=your_production_key
AI_MODEL_PREFERENCE=gpt-4
RATE_LIMIT_PER_MINUTE=20
CACHE_ENABLED=true
ANALYTICS_ENABLED=true
```

### 2. Scaling Strategy
- **Horizontal Scaling**: Deploy multiple AI service instances
- **Load Balancing**: Distribute requests across instances
- **Database Optimization**: Index AI-related fields
- **CDN Integration**: Cache static assets

## Testing Strategy

### 1. Unit Tests
```python
def test_ai_content_generation():
    result = generate_menu_content("Margherita Pizza")
    assert result['description']
    assert result['upsell_suggestion']
    assert len(result['description']) <= 30
```

### 2. Integration Tests
```python
def test_grafterr_integration():
    # Test full integration with Grafterr's item management
    pass
```

### 3. User Acceptance Testing
- Test AI content quality
- Validate user experience
- Measure performance impact
- Gather user feedback

## Future Enhancements

### 1. Advanced Features
- **Multi-language Support**: Generate content in different languages
- **Cuisine-specific Prompts**: Tailored prompts for different restaurant types
- **Seasonal Content**: Dynamic content based on seasons and holidays
- **A/B Testing**: Compare different AI-generated content versions

### 2. Machine Learning Integration
- **User Preference Learning**: Adapt to user's content preferences
- **Performance Optimization**: Learn from successful content patterns
- **Automated Quality Assessment**: Evaluate content quality automatically

### 3. Business Intelligence
- **Content Performance Analytics**: Track which descriptions perform better
- **Upsell Effectiveness**: Measure upsell suggestion conversion rates
- **ROI Analysis**: Calculate return on investment for AI features
