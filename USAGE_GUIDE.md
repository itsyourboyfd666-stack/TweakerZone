# Grok-Blackbox Integration - Usage Guide

## 🚀 Quick Start

### Option 1: Interactive CLI (Recommended)
```bash
./quickstart.sh
```

### Option 2: Manual Setup
```bash
# Install dependencies
python3 -m pip install requests python-dotenv

# Run interactive CLI
python3 grok_cli.py
```

### Option 3: Direct Script Usage
```bash
# Setup API keys
python3 grok_cli.py --setup

# Test Grok
python3 grok_cli.py --test-grok

# Check status
python3 grok_cli.py --status
```

---

## 🔑 Getting API Keys

### Grok API Key (X.AI)
1. Visit: https://console.x.ai/
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key

### Blackbox API Key
1. Visit: https://www.blackbox.ai/
2. Sign up or log in
3. Go to Settings → API
4. Generate an API key
5. Copy the key

---

## 📝 Configuration Methods

### Method 1: Environment Variables
```bash
export XAI_API_KEY='your-grok-api-key-here'
export BLACKBOX_API_KEY='your-blackbox-api-key-here'
```

### Method 2: .env File
```bash
# Copy template
cp .env.example .env

# Edit .env file
nano .env

# Add your keys:
XAI_API_KEY=your-grok-api-key-here
BLACKBOX_API_KEY=your-blackbox-api-key-here
```

### Method 3: Interactive CLI
```bash
python3 grok_cli.py
# Select option 1: Setup API Keys
# Follow the prompts
```

---

## 💻 Programming Usage

### Basic Grok Query
```python
from grok_blackbox_integration import GrokBlackboxConnector

connector = GrokBlackboxConnector()

# Simple chat
response = connector.grok_chat([
    {"role": "user", "content": "What is quantum computing?"}
])

print(response['choices'][0]['message']['content'])
```

### Blackbox Code Query
```python
from grok_blackbox_integration import GrokBlackboxConnector

connector = GrokBlackboxConnector()

# Code assistance
result = connector.blackbox_query(
    "Write a Python function to find prime numbers",
    mode="code",
    language="python"
)

print(result)
```

### Hybrid Query (Both APIs)
```python
from grok_blackbox_integration import GrokBlackboxConnector

connector = GrokBlackboxConnector()

# Use both Grok and Blackbox
result = connector.hybrid_query(
    "How do I implement a binary search tree?",
    use_grok=True,
    use_blackbox=True,
    context="I'm using Python 3.9"
)

print(result['combined_analysis'])
```

---

## 🎨 Customization Examples

### Custom System Prompt
```python
connector = GrokBlackboxConnector()

messages = [
    {
        "role": "system", 
        "content": "You are a cybersecurity expert specializing in penetration testing."
    },
    {
        "role": "user", 
        "content": "Explain SQL injection vulnerabilities"
    }
]

response = connector.grok_chat(messages)
```

### Adjust Temperature (Creativity)
```python
# More creative (0.0 - 2.0)
response = connector.grok_chat(
    messages=[{"role": "user", "content": "Write a poem about AI"}],
    temperature=1.5,  # Higher = more creative
    max_tokens=500
)
```

### Different Grok Models
```python
# Use vision model
response = connector.grok_chat(
    messages=[{"role": "user", "content": "Describe this image"}],
    model="grok-vision-beta"
)
```

---

## 🔧 Advanced Customization

### Modify Base Integration
Edit `grok_blackbox_integration.py` to:

1. **Add Custom Methods**
```python
def custom_security_scan(self, code: str) -> Dict:
    """Custom security analysis"""
    messages = [
        {"role": "system", "content": "You are a security auditor"},
        {"role": "user", "content": f"Analyze this code for vulnerabilities:\n{code}"}
    ]
    return self.grok_chat(messages)
```

2. **Add Response Caching**
```python
import hashlib
import json

def _cache_key(self, query: str) -> str:
    return hashlib.md5(query.encode()).hexdigest()

def cached_query(self, query: str):
    cache_file = f".cache/{self._cache_key(query)}.json"
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return json.load(f)
    
    result = self.grok_chat([{"role": "user", "content": query}])
    
    os.makedirs('.cache', exist_ok=True)
    with open(cache_file, 'w') as f:
        json.dump(result, f)
    
    return result
```

3. **Add Streaming Support**
```python
def grok_chat_stream(self, messages: List[Dict]):
    """Stream responses from Grok"""
    response = self.grok_chat(messages, stream=True)
    
    for chunk in response.iter_lines():
        if chunk:
            yield json.loads(chunk)
```

---

## 🧪 Testing

### Test Grok Connection
```bash
python3 grok_cli.py --test-grok
```

### Test Blackbox Connection
```bash
python3 grok_cli.py --test-blackbox
```

### Run All Tests
```python
# Create test_integration.py
from grok_blackbox_integration import GrokBlackboxConnector

def test_all():
    connector = GrokBlackboxConnector()
    
    # Test 1: Grok
    print("Testing Grok...")
    grok_result = connector.grok_chat([
        {"role": "user", "content": "Say hello"}
    ])
    assert 'choices' in grok_result
    print("✅ Grok test passed")
    
    # Test 2: Blackbox
    print("Testing Blackbox...")
    bb_result = connector.blackbox_query("print hello world in python")
    print("✅ Blackbox test passed")
    
    # Test 3: Hybrid
    print("Testing Hybrid...")
    hybrid_result = connector.hybrid_query("What is Python?")
    assert hybrid_result['query'] == "What is Python?"
    print("✅ Hybrid test passed")

if __name__ == "__main__":
    test_all()
```

---

## 🛠️ Troubleshooting

### Issue: "API key not found"
**Solution:** Set environment variables or use the CLI setup:
```bash
export XAI_API_KEY='your-key'
# or
python3 grok_cli.py --setup
```

### Issue: "Module not found: requests"
**Solution:** Install dependencies:
```bash
python3 -m pip install requests python-dotenv
```

### Issue: "Connection refused"
**Solution:** Check your internet connection and API endpoints:
```python
connector = GrokBlackboxConnector()
print(connector.grok_base_url)  # Should be https://api.x.ai/v1
```

### Issue: "401 Unauthorized"
**Solution:** Verify your API key is correct and active:
```bash
python3 grok_cli.py --status
```

---

## 📚 Examples

### Example 1: Code Review Assistant
```python
connector = GrokBlackboxConnector()

code = """
def login(username, password):
    query = f"SELECT * FROM users WHERE user='{username}' AND pass='{password}'"
    return db.execute(query)
"""

result = connector.hybrid_query(
    f"Review this code for security issues:\n{code}",
    context="Focus on SQL injection vulnerabilities"
)

print(result['combined_analysis'])
```

### Example 2: Learning Assistant
```python
connector = GrokBlackboxConnector()

topic = "async/await in Python"

result = connector.hybrid_query(
    f"Explain {topic} with examples",
    use_grok=True,
    use_blackbox=True
)

# Grok provides explanation
print("Explanation:", result['grok_response'])

# Blackbox provides code examples
print("Code:", result['blackbox_response'])
```

### Example 3: Debugging Helper
```python
connector = GrokBlackboxConnector()

error = """
Traceback (most recent call last):
  File "app.py", line 42, in process_data
    result = data['key']
KeyError: 'key'
"""

solution = connector.grok_chat([
    {"role": "user", "content": f"Help me fix this error:\n{error}"}
])

print(solution['choices'][0]['message']['content'])
```

---

## 🔐 Security Best Practices

1. **Never commit API keys to git**
   ```bash
   echo ".env" >> .gitignore
   echo "grok_blackbox_config.json" >> .gitignore
   ```

2. **Use environment variables in production**
   ```bash
   # In production
   export XAI_API_KEY=$(cat /secure/path/grok_key)
   ```

3. **Rotate keys regularly**
   - Change API keys every 90 days
   - Revoke old keys immediately

4. **Monitor API usage**
   - Check usage dashboards regularly
   - Set up billing alerts

---

## 📞 Support

- **Grok API Docs**: https://docs.x.ai/
- **Blackbox Docs**: https://www.blackbox.ai/docs
- **Issues**: Check README.md for troubleshooting

---

## 🎯 Next Steps

1. ✅ Install dependencies
2. ✅ Get API keys
3. ✅ Configure keys
4. ✅ Test connection
5. ✅ Start building!

Happy coding! 🚀
