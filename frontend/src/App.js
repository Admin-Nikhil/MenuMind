import React, { useState } from 'react';
import axios from 'axios';
import { Sparkles, Zap, AlertCircle, CheckCircle } from 'lucide-react';
import './App.css';

function App() {
  const [itemName, setItemName] = useState('');
  const [model, setModel] = useState('gpt-3.5-turbo');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!itemName.trim()) {
      setError('Please enter a food item name');
      return;
    }

    setLoading(true);
    setError(null);
    setSuccess(null);
    setResult(null);

    try {
      const response = await axios.post('/generate-item-details', {
        item_name: itemName.trim(),
        model: model
      });

      setResult(response.data);
      setSuccess('Content generated successfully!');
    } catch (err) {
      console.error('Error generating content:', err);
      
      if (err.response?.data?.error) {
        setError(err.response.data.error);
      } else if (err.response?.status === 429) {
        setError('Rate limit exceeded. Please wait a moment before trying again.');
      } else if (err.response?.status === 500) {
        setError('Server error. Please try again later.');
      } else {
        setError('Failed to generate content. Please check your connection and try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleModelToggle = () => {
    setModel(prev => prev === 'gpt-3.5-turbo' ? 'gpt-4' : 'gpt-3.5-turbo');
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    setSuccess('Copied to clipboard!');
    setTimeout(() => setSuccess(null), 2000);
  };

  return (
    <div className="container">
      <div className="card">
        <div className="header">
          <h1>
            <Sparkles size={40} style={{ marginRight: '10px', verticalAlign: 'middle' }} />
            Menu Intelligence Widget
          </h1>
          <p>AI-powered menu description and upsell suggestions for your POS system</p>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="itemName">Food Item Name</label>
            <input
              type="text"
              id="itemName"
              value={itemName}
              onChange={(e) => setItemName(e.target.value)}
              placeholder="e.g., Paneer Tikka Pizza, Margherita Pizza, Chicken Burger..."
              disabled={loading}
            />
          </div>

          <div className="model-toggle">
            <label>AI Model:</label>
            <span>GPT-3.5</span>
            <label className="toggle-switch">
              <input
                type="checkbox"
                checked={model === 'gpt-4'}
                onChange={handleModelToggle}
                disabled={loading}
              />
              <span className="slider"></span>
            </label>
            <span>GPT-4</span>
          </div>

          <button 
            type="submit" 
            className="btn" 
            disabled={loading || !itemName.trim()}
          >
            {loading ? (
              <div className="loading">
                <div className="spinner"></div>
                Generating Content...
              </div>
            ) : (
              <>
                <Zap size={20} />
                Generate Menu Content
              </>
            )}
          </button>
        </form>

        {error && (
          <div className="error">
            <AlertCircle size={20} style={{ marginRight: '8px', verticalAlign: 'middle' }} />
            {error}
          </div>
        )}

        {success && (
          <div className="success">
            <CheckCircle size={20} style={{ marginRight: '8px', verticalAlign: 'middle' }} />
            {success}
          </div>
        )}

        {result && (
          <div className="result">
            <h3>Generated Content for "{result.item_name}"</h3>
            
            <div className="result-item">
              <h4>Menu Description</h4>
              <p>{result.description}</p>
              <button 
                onClick={() => copyToClipboard(result.description)}
                style={{
                  marginTop: '8px',
                  padding: '4px 8px',
                  fontSize: '0.8rem',
                  background: '#667eea',
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer'
                }}
              >
                Copy
              </button>
            </div>

            <div className="result-item">
              <h4>Upsell Suggestion</h4>
              <p>{result.upsell_suggestion}</p>
              <button 
                onClick={() => copyToClipboard(result.upsell_suggestion)}
                style={{
                  marginTop: '8px',
                  padding: '4px 8px',
                  fontSize: '0.8rem',
                  background: '#667eea',
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer'
                }}
              >
                Copy
              </button>
            </div>

            <div style={{ fontSize: '0.8rem', color: '#718096', marginTop: '1rem' }}>
              <strong>Model used:</strong> {result.model_used} | 
              <strong> Generated at:</strong> {new Date(result.generated_at).toLocaleString()}
            </div>
          </div>
        )}

        <div className="footer">
          <p>
            Built for Grafterr POS System Integration | 
            <a href="#" onClick={(e) => e.preventDefault()}> View Integration Guide</a>
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;
