from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import openai
import os
import re
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Development mode flag (set to True to disable rate limiting for testing)
DEV_MODE = os.getenv('DEV_MODE', 'False').lower() == 'true'

app = Flask(__name__)
CORS(app)

# Rate limiting setup
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour", "30 per minute"]  # More lenient for testing
)

# OpenAI configuration (you'll need to set OPENAI_API_KEY in .env)
openai.api_key = os.getenv('OPENAI_API_KEY', 'dummy-key-for-simulation')

# In-memory storage for rate limiting (in production, use Redis)
request_history = {}

def sanitize_input(text):
    """Sanitize and validate user input"""
    if not text or not isinstance(text, str):
        return None
    
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\']', '', text.strip())
    
    # Limit length
    if len(sanitized) > 100:
        return None
    
    return sanitized

def validate_food_item(item_name):
    """Validate food item name"""
    if not item_name:
        return False, "Food item name is required"
    
    # Check for common food-related keywords
    food_keywords = ['pizza', 'burger', 'pasta', 'salad', 'soup', 'rice', 'bread', 
                    'chicken', 'beef', 'fish', 'vegetarian', 'vegan', 'dessert',
                    'drink', 'beverage', 'appetizer', 'main', 'side', 'tikka',
                    'curry', 'noodles', 'sandwich', 'wrap', 'taco', 'sushi']
    
    item_lower = item_name.lower()
    if not any(keyword in item_lower for keyword in food_keywords):
        return False, "Please provide a valid food item name"
    
    return True, "Valid"

def check_rate_limit(client_ip):
    """Simple rate limiting check"""
    if DEV_MODE:
        return True  # Skip rate limiting in development mode
    
    now = datetime.now()
    if client_ip in request_history:
        last_request = request_history[client_ip]
        if now - last_request < timedelta(seconds=1):  # 1 second between requests (more lenient for testing)
            return False
    request_history[client_ip] = now
    return True

def generate_ai_response(item_name, model="gpt-3.5-turbo"):
    """
    Generate AI response using OpenAI API or simulation
    """
    
    # Prompt engineering for menu description and upsell
    prompt = f"""
    You are a professional restaurant menu writer and marketing expert. 
    
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
    {{
        "description": "Your menu description here (max 30 words)",
        "upsell_suggestion": "Your upsell combo suggestion here"
    }}
    
    Example for "Margherita Pizza":
    {{
        "description": "Fresh mozzarella, basil, and tomato sauce on crispy crust",
        "upsell_suggestion": "Pair it with a refreshing Italian soda for the perfect meal!"
    }}
    """
    
    try:
        # Try real OpenAI API if key is available
        if os.getenv('OPENAI_API_KEY') and os.getenv('OPENAI_API_KEY') != 'dummy-key-for-simulation':
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a professional restaurant menu writer."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            ai_response = response.choices[0].message.content
        else:
            # Simulation mode for demo purposes
            ai_response = simulate_ai_response(item_name, model)
        
        # Parse JSON response
        try:
            result = json.loads(ai_response)
            return result
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return {
                "description": f"Delicious {item_name} made with fresh ingredients and authentic flavors.",
                "upsell_suggestion": f"Pair your {item_name} with a refreshing beverage for the perfect dining experience!"
            }
            
    except Exception as e:
        # Fallback response
        return {
            "description": f"Delicious {item_name} made with fresh ingredients and authentic flavors.",
            "upsell_suggestion": f"Pair your {item_name} with a refreshing beverage for the perfect dining experience!"
        }

def simulate_ai_response(item_name, model):
    """Simulate AI responses for demo purposes"""
    
    # Pre-defined responses for common food items
    responses = {
        "pizza": {
            "description": "Fresh-baked pizza with premium toppings and crispy crust",
            "upsell_suggestion": "Add a garlic bread and soft drink combo for just $3 more!"
        },
        "burger": {
            "description": "Juicy beef patty with fresh lettuce, tomato, and special sauce",
            "upsell_suggestion": "Upgrade to a meal with fries and drink for complete satisfaction!"
        },
        "pasta": {
            "description": "Al dente pasta tossed in rich, flavorful sauce with herbs",
            "upsell_suggestion": "Complete your meal with a fresh garden salad and garlic bread!"
        },
        "salad": {
            "description": "Crisp mixed greens with fresh vegetables and house dressing",
            "upsell_suggestion": "Add grilled chicken or shrimp for a protein-packed meal!"
        },
        "curry": {
            "description": "Aromatic spices blend with tender meat and rich gravy",
            "upsell_suggestion": "Pair with fluffy basmati rice and naan bread for authentic taste!"
        }
    }
    
    # Find matching response
    item_lower = item_name.lower()
    for key, response in responses.items():
        if key in item_lower:
            return json.dumps(response)
    
    # Default response
    default_response = {
        "description": f"Delicious {item_name} prepared with fresh ingredients and authentic flavors",
        "upsell_suggestion": f"Enhance your {item_name} experience with a complementary side dish!"
    }
    
    # Simulate different responses for different models
    if "gpt-4" in model.lower():
        default_response["description"] = f"Artisanal {item_name} crafted with premium ingredients and expert culinary techniques"
        default_response["upsell_suggestion"] = f"Elevate your dining experience with our signature {item_name} paired with a curated beverage selection!"
    
    return json.dumps(default_response)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/generate-item-details', methods=['POST'])
@limiter.limit("30 per minute" if not DEV_MODE else "1000 per minute")  # Disable rate limiting in dev mode
def generate_item_details():
    """
    Generate menu description and upsell suggestion for a food item
    """
    try:
        # Get client IP for rate limiting
        client_ip = get_remote_address()
        
        # Check rate limit
        if not check_rate_limit(client_ip):
            return jsonify({
                "error": "Rate limit exceeded. Please wait a moment before trying again."
            }), 429
        
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        item_name = data.get('item_name', '').strip()
        model = data.get('model', 'gpt-3.5-turbo')
        
        # Validate and sanitize input
        sanitized_item = sanitize_input(item_name)
        if not sanitized_item:
            return jsonify({"error": "Invalid or missing food item name"}), 400
        
        # Validate food item
        is_valid, message = validate_food_item(sanitized_item)
        if not is_valid:
            return jsonify({"error": message}), 400
        
        # Generate AI response
        ai_response = generate_ai_response(sanitized_item, model)
        
        # Add metadata
        response_data = {
            "item_name": sanitized_item,
            "model_used": model,
            "generated_at": datetime.now().isoformat(),
            **ai_response
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        app.logger.error(f"Error generating item details: {str(e)}")
        return jsonify({
            "error": "An error occurred while generating content. Please try again."
        }), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limit errors"""
    return jsonify({
        "error": "Rate limit exceeded. Please wait before making another request."
    }), 429

if __name__ == '__main__':
    print("🚀 Starting AI-Powered Menu Intelligence Widget Backend")
    print("📝 API Endpoints:")
    print("   - POST /generate-item-details - Generate menu content")
    print("   - GET  /health - Health check")
    print("🔧 To use real OpenAI API, set OPENAI_API_KEY in .env file")
    print("🎭 Currently running in simulation mode")
    if DEV_MODE:
        print("🔧 Development mode enabled - Rate limiting disabled")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
