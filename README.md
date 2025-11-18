# Grok-Blackbox Integration

Connect Grok (X.AI) with Blackbox for enhanced AI capabilities.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API keys:**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

   Or export them directly:
   ```bash
   export XAI_API_KEY='your-grok-api-key'
   export BLACKBOX_API_KEY='your-blackbox-api-key'
   ```

3. **Get API Keys:**
   - **Grok API**: https://console.x.ai/
   - **Blackbox API**: https://www.blackbox.ai/

## Usage

### Basic Example

```python
from grok_blackbox_integration import GrokBlackboxConnector

# Initialize
connector = GrokBlackboxConnector()

# Use Grok
response = connector.grok_chat([
    {"role": "user", "content": "Explain quantum computing"}
])
print(response['choices'][0]['message']['content'])

# Use Blackbox
result = connector.blackbox_query("Write a Python function to sort a list")
print(result)

# Hybrid query (uses both)
combined = connector.hybrid_query("How do I optimize database queries?")
print(combined['combined_analysis'])
```

### Run the example

```bash
python3 grok_blackbox_integration.py
```

## Features

- ✅ Grok API integration (chat completions)
- ✅ Blackbox API integration (code assistance)
- ✅ Hybrid queries (combine both AI systems)
- ✅ Configurable models and parameters
- ✅ Session management
- ✅ Error handling

## API Methods

### `grok_chat(messages, model='grok-beta', temperature=0.7, max_tokens=2048)`
Send chat requests to Grok API.

### `blackbox_query(query, mode='code', language=None)`
Query Blackbox for code assistance.

### `hybrid_query(user_query, use_grok=True, use_blackbox=True, context=None)`
Execute queries using both APIs and combine results.

## Customization

Edit `grok_blackbox_integration.py` to:
- Add custom prompts
- Modify response processing
- Implement streaming responses
- Add caching mechanisms
- Integrate with other tools

## Security

- Never commit `.env` file with real API keys
- Use environment variables for production
- Rotate API keys regularly
- Monitor API usage and costs

## License

See LICENSE file for details.
