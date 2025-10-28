import { useState } from 'react';
import '../styles/env-config.css';

export function EnvConfigScreen({ onConfigComplete }) {
  const [config, setConfig] = useState({
    GOOGLE_GENAI_USE_VERTEXAI: '',
    GOOGLE_CLOUD_PROJECT: '',
    GOOGLE_CLOUD_LOCATION: '',
    MODEL: '',
    SUPABASE_URL: '',
    SUPABASE_KEY: '',
    COINMARKETCAP_API_KEY: '',
  });

  const [errors, setErrors] = useState({});
  const [submitted, setSubmitted] = useState(false);

  const requiredFields = [
    {
      key: 'GOOGLE_GENAI_USE_VERTEXAI',
      label: 'Google GenAI Use VertexAI',
      placeholder: 'TRUE',
      type: 'text',
    },
    {
      key: 'GOOGLE_CLOUD_PROJECT',
      label: 'Google Cloud Project ID',
      placeholder: 'YOUR_PROJECT_ID',
      type: 'text',
    },
    {
      key: 'GOOGLE_CLOUD_LOCATION',
      label: 'Google Cloud Location',
      placeholder: 'YOUR_LOCATION',
      type: 'text',
    },
    {
      key: 'MODEL',
      label: 'LLM Model',
      placeholder: 'YOUR_LLM_MODEL',
      type: 'text',
    },
    {
      key: 'SUPABASE_URL',
      label: 'Supabase URL',
      placeholder: 'YOUR_SUPABASE_URL',
      type: 'url',
    },
    {
      key: 'SUPABASE_KEY',
      label: 'Supabase Key',
      placeholder: 'YOUR_SUPABASE_KEY',
      type: 'password',
    },
    {
      key: 'COINMARKETCAP_API_KEY',
      label: 'CoinMarketCap API Key',
      placeholder: 'YOUR_COINMARKETCAP_KEY',
      type: 'password',
    },
  ];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setConfig((prev) => ({
      ...prev,
      [name]: value,
    }));
    if (errors[name]) {
      setErrors((prev) => ({
        ...prev,
        [name]: '',
      }));
    }
  };

  const validateConfig = () => {
    const newErrors = {};
    requiredFields.forEach(({ key }) => {
      if (!config[key] || config[key].trim() === '') {
        newErrors[key] = `${key.replace(/_/g, ' ')} is required`;
      }
    });
    return newErrors;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const newErrors = validateConfig();

    if (Object.keys(newErrors).length === 0) {
      localStorage.setItem('envConfig', JSON.stringify(config));
      setSubmitted(true);
      setTimeout(() => {
        onConfigComplete(config);
      }, 1500);
    } else {
      setErrors(newErrors);
    }
  };

  if (submitted) {
    return (
      <div className="env-config-screen">
        <div className="config-card success-card">
          <div className="success-icon">✓</div>
          <h2 className="success-title">Configuration Complete!</h2>
          <p className="success-message">All environment variables have been set successfully.</p>
          <p className="loading-text">Loading chat interface...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="env-config-screen">
      <div className="config-card">
        <div className="config-header">
          <h1 className="config-title">Environment Configuration</h1>
          <p className="config-subtitle">Please provide all required environment variables to continue</p>
        </div>

        <form onSubmit={handleSubmit} className="config-form">
          <div className="form-fields">
            {requiredFields.map(({ key, label, placeholder, type }) => (
              <div key={key} className="form-group">
                <label htmlFor={key} className="form-label">
                  {label}
                  <span className="required-indicator">*</span>
                </label>
                <input
                  type={type}
                  id={key}
                  name={key}
                  value={config[key]}
                  onChange={handleChange}
                  placeholder={placeholder}
                  className={`form-input ${errors[key] ? 'form-input-error' : ''}`}
                />
                {errors[key] && <span className="error-text">{errors[key]}</span>}
              </div>
            ))}
          </div>

          <button type="submit" className="submit-btn">
            Continue to Chat
          </button>
        </form>

        <div className="config-info">
          <p className="info-text">
            ℹ️ Your configuration will be stored locally in your browser. These values are required for the application to function properly.
          </p>
        </div>
      </div>
    </div>
  );
}
