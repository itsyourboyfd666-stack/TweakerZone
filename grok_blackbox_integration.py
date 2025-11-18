#!/usr/bin/env python3
"""
Grok-Blackbox Integration
Connects Grok (X.AI) API with Blackbox for enhanced AI capabilities
"""

import os
import json
import requests
from typing import Optional, Dict, List, Any


class GrokBlackboxConnector:
    """Main connector class for Grok-Blackbox integration"""
    
    def __init__(self, grok_api_key: Optional[str] = None, blackbox_api_key: Optional[str] = None):
        """
        Initialize the connector with API keys
        
        Args:
            grok_api_key: X.AI Grok API key (or set XAI_API_KEY env var)
            blackbox_api_key: Blackbox API key (or set BLACKBOX_API_KEY env var)
        """
        self.grok_api_key = grok_api_key or os.getenv('XAI_API_KEY')
        self.blackbox_api_key = blackbox_api_key or os.getenv('BLACKBOX_API_KEY')
        
        self.grok_base_url = "https://api.x.ai/v1"
        self.blackbox_base_url = "https://api.blackbox.ai/v1"
        
        self.session = requests.Session()
        
    def set_grok_key(self, api_key: str):
        """Set Grok API key"""
        self.grok_api_key = api_key
        
    def set_blackbox_key(self, api_key: str):
        """Set Blackbox API key"""
        self.blackbox_api_key = api_key
    
    def grok_chat(self, 
                  messages: List[Dict[str, str]], 
                  model: str = "grok-beta",
                  temperature: float = 0.7,
                  max_tokens: int = 2048,
                  stream: bool = False) -> Dict[str, Any]:
        """
        Send chat request to Grok API
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Grok model to use (grok-beta, grok-vision-beta)
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens in response
            stream: Whether to stream the response
            
        Returns:
            API response as dict
        """
        if not self.grok_api_key:
            raise ValueError("Grok API key not set. Use set_grok_key() or XAI_API_KEY env var")
        
        headers = {
            "Authorization": f"Bearer {self.grok_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messages": messages,
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream
        }
        
        response = self.session.post(
            f"{self.grok_base_url}/chat/completions",
            headers=headers,
            json=payload
        )
        
        response.raise_for_status()
        return response.json()
    
    def blackbox_query(self, 
                       query: str,
                       mode: str = "code",
                       language: Optional[str] = None) -> Dict[str, Any]:
        """
        Send query to Blackbox API
        
        Args:
            query: The query/prompt to send
            mode: Query mode (code, chat, search)
            language: Programming language context
            
        Returns:
            API response as dict
        """
        if not self.blackbox_api_key:
            raise ValueError("Blackbox API key not set. Use set_blackbox_key() or BLACKBOX_API_KEY env var")
        
        headers = {
            "Authorization": f"Bearer {self.blackbox_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "query": query,
            "mode": mode
        }
        
        if language:
            payload["language"] = language
        
        response = self.session.post(
            f"{self.blackbox_base_url}/query",
            headers=headers,
            json=payload
        )
        
        response.raise_for_status()
        return response.json()
    
    def hybrid_query(self, 
                     user_query: str,
                     use_grok: bool = True,
                     use_blackbox: bool = True,
                     context: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute a hybrid query using both Grok and Blackbox
        
        Args:
            user_query: The user's query
            use_grok: Whether to use Grok
            use_blackbox: Whether to use Blackbox
            context: Additional context for the query
            
        Returns:
            Combined results from both APIs
        """
        results = {
            "query": user_query,
            "grok_response": None,
            "blackbox_response": None,
            "combined_analysis": None
        }
        
        # Get Grok response
        if use_grok and self.grok_api_key:
            messages = [
                {"role": "system", "content": "You are Grok, a helpful AI assistant with a rebellious streak."}
            ]
            
            if context:
                messages.append({"role": "system", "content": f"Context: {context}"})
            
            messages.append({"role": "user", "content": user_query})
            
            try:
                grok_result = self.grok_chat(messages)
                results["grok_response"] = grok_result.get("choices", [{}])[0].get("message", {}).get("content")
            except Exception as e:
                results["grok_response"] = f"Error: {str(e)}"
        
        # Get Blackbox response
        if use_blackbox and self.blackbox_api_key:
            try:
                blackbox_result = self.blackbox_query(user_query)
                results["blackbox_response"] = blackbox_result
            except Exception as e:
                results["blackbox_response"] = f"Error: {str(e)}"
        
        # Combine insights
        if results["grok_response"] and results["blackbox_response"]:
            results["combined_analysis"] = self._combine_responses(
                results["grok_response"],
                results["blackbox_response"]
            )
        
        return results
    
    def _combine_responses(self, grok_resp: str, blackbox_resp: Any) -> str:
        """Combine responses from both APIs into a unified analysis"""
        combined = f"""
=== GROK ANALYSIS ===
{grok_resp}

=== BLACKBOX ANALYSIS ===
{json.dumps(blackbox_resp, indent=2)}

=== SYNTHESIS ===
Combined insights from both Grok and Blackbox AI systems.
"""
        return combined
    
    def save_config(self, filepath: str = "grok_blackbox_config.json"):
        """Save current configuration to file"""
        config = {
            "grok_api_key": self.grok_api_key[:10] + "..." if self.grok_api_key else None,
            "blackbox_api_key": self.blackbox_api_key[:10] + "..." if self.blackbox_api_key else None,
            "grok_base_url": self.grok_base_url,
            "blackbox_base_url": self.blackbox_base_url
        }
        
        with open(filepath, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"Configuration saved to {filepath}")


def main():
    """Example usage"""
    print("=== Grok-Blackbox Integration ===\n")
    
    # Initialize connector
    connector = GrokBlackboxConnector()
    
    # Check for API keys
    if not connector.grok_api_key:
        print("⚠️  Grok API key not found. Set XAI_API_KEY environment variable.")
        print("   Get your key from: https://console.x.ai/")
    
    if not connector.blackbox_api_key:
        print("⚠️  Blackbox API key not found. Set BLACKBOX_API_KEY environment variable.")
        print("   Get your key from: https://www.blackbox.ai/")
    
    print("\n--- Example Usage ---\n")
    
    # Example 1: Grok chat
    if connector.grok_api_key:
        print("1. Grok Chat Example:")
        try:
            response = connector.grok_chat([
                {"role": "user", "content": "What is the meaning of life in 20 words?"}
            ])
            print(f"   Response: {response['choices'][0]['message']['content']}\n")
        except Exception as e:
            print(f"   Error: {e}\n")
    
    # Example 2: Hybrid query
    print("2. Hybrid Query Example:")
    print("   (Requires both API keys to be set)\n")
    
    # Save configuration
    connector.save_config()
    
    print("\n✅ Setup complete!")
    print("\nTo use this integration:")
    print("1. Set your API keys:")
    print("   export XAI_API_KEY='your-grok-api-key'")
    print("   export BLACKBOX_API_KEY='your-blackbox-api-key'")
    print("\n2. Import and use:")
    print("   from grok_blackbox_integration import GrokBlackboxConnector")
    print("   connector = GrokBlackboxConnector()")
    print("   result = connector.hybrid_query('Your question here')")


if __name__ == "__main__":
    main()
