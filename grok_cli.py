#!/usr/bin/env python3
"""
Interactive CLI for Grok-Blackbox Integration
Provides easy customization and testing interface
"""

import os
import sys
import json
from grok_blackbox_integration import GrokBlackboxConnector


class GrokCLI:
    """Interactive CLI for Grok-Blackbox"""
    
    def __init__(self):
        self.connector = GrokBlackboxConnector()
        self.config_file = "grok_blackbox_config.json"
        self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    print(f"✅ Loaded configuration from {self.config_file}")
            except Exception as e:
                print(f"⚠️  Error loading config: {e}")
    
    def save_config(self):
        """Save current configuration"""
        self.connector.save_config(self.config_file)
    
    def setup_keys(self):
        """Interactive API key setup"""
        print("\n=== API Key Setup ===\n")
        
        # Grok API Key
        current_grok = "Set" if self.connector.grok_api_key else "Not set"
        print(f"Grok API Key: {current_grok}")
        grok_key = input("Enter Grok API key (or press Enter to skip): ").strip()
        if grok_key:
            self.connector.set_grok_key(grok_key)
            os.environ['XAI_API_KEY'] = grok_key
            print("✅ Grok API key updated")
        
        # Blackbox API Key
        current_bb = "Set" if self.connector.blackbox_api_key else "Not set"
        print(f"\nBlackbox API Key: {current_bb}")
        bb_key = input("Enter Blackbox API key (or press Enter to skip): ").strip()
        if bb_key:
            self.connector.set_blackbox_key(bb_key)
            os.environ['BLACKBOX_API_KEY'] = bb_key
            print("✅ Blackbox API key updated")
        
        self.save_config()
        print("\n✅ Configuration saved!\n")
    
    def test_grok(self):
        """Test Grok API connection"""
        if not self.connector.grok_api_key:
            print("❌ Grok API key not set. Run setup first.")
            return
        
        print("\n=== Testing Grok API ===\n")
        query = input("Enter your question (or press Enter for default): ").strip()
        if not query:
            query = "Say hello in a witty way"
        
        print(f"\n🤖 Asking Grok: {query}\n")
        
        try:
            response = self.connector.grok_chat([
                {"role": "user", "content": query}
            ])
            
            answer = response['choices'][0]['message']['content']
            print(f"💬 Grok says:\n{answer}\n")
            
            # Show metadata
            print(f"📊 Metadata:")
            print(f"   Model: {response.get('model', 'N/A')}")
            print(f"   Tokens: {response.get('usage', {}).get('total_tokens', 'N/A')}")
            
        except Exception as e:
            print(f"❌ Error: {e}\n")
    
    def test_blackbox(self):
        """Test Blackbox API connection"""
        if not self.connector.blackbox_api_key:
            print("❌ Blackbox API key not set. Run setup first.")
            return
        
        print("\n=== Testing Blackbox API ===\n")
        query = input("Enter your code question: ").strip()
        if not query:
            query = "Write a Python function to reverse a string"
        
        print(f"\n🤖 Asking Blackbox: {query}\n")
        
        try:
            response = self.connector.blackbox_query(query)
            print(f"💬 Blackbox response:\n{json.dumps(response, indent=2)}\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")
    
    def hybrid_test(self):
        """Test hybrid query"""
        if not self.connector.grok_api_key and not self.connector.blackbox_api_key:
            print("❌ No API keys set. Run setup first.")
            return
        
        print("\n=== Hybrid Query Test ===\n")
        query = input("Enter your question: ").strip()
        if not query:
            query = "Explain async/await in Python"
        
        print(f"\n🤖 Processing hybrid query: {query}\n")
        
        try:
            result = self.connector.hybrid_query(query)
            
            if result['grok_response']:
                print("=== GROK RESPONSE ===")
                print(result['grok_response'])
                print()
            
            if result['blackbox_response']:
                print("=== BLACKBOX RESPONSE ===")
                print(json.dumps(result['blackbox_response'], indent=2))
                print()
            
            if result['combined_analysis']:
                print("=== COMBINED ANALYSIS ===")
                print(result['combined_analysis'])
        
        except Exception as e:
            print(f"❌ Error: {e}\n")
    
    def customize_prompts(self):
        """Customize system prompts"""
        print("\n=== Customize System Prompts ===\n")
        print("Current Grok system prompt:")
        print("'You are Grok, a helpful AI assistant with a rebellious streak.'\n")
        
        new_prompt = input("Enter new system prompt (or press Enter to keep current): ").strip()
        if new_prompt:
            print(f"✅ New prompt set: {new_prompt}")
            print("Note: Modify grok_blackbox_integration.py to persist this change")
    
    def show_status(self):
        """Show current configuration status"""
        print("\n=== Configuration Status ===\n")
        print(f"Grok API Key: {'✅ Set' if self.connector.grok_api_key else '❌ Not set'}")
        print(f"Blackbox API Key: {'✅ Set' if self.connector.blackbox_api_key else '❌ Not set'}")
        print(f"Grok Base URL: {self.connector.grok_base_url}")
        print(f"Blackbox Base URL: {self.connector.blackbox_base_url}")
        print()
    
    def show_menu(self):
        """Display main menu"""
        print("\n" + "="*50)
        print("   GROK-BLACKBOX INTEGRATION CLI")
        print("="*50)
        print("\n1. Setup API Keys")
        print("2. Test Grok API")
        print("3. Test Blackbox API")
        print("4. Hybrid Query Test")
        print("5. Customize Prompts")
        print("6. Show Status")
        print("7. Exit")
        print()
    
    def run(self):
        """Main CLI loop"""
        print("\n🚀 Welcome to Grok-Blackbox Integration CLI\n")
        
        while True:
            self.show_menu()
            choice = input("Select option (1-7): ").strip()
            
            if choice == '1':
                self.setup_keys()
            elif choice == '2':
                self.test_grok()
            elif choice == '3':
                self.test_blackbox()
            elif choice == '4':
                self.hybrid_test()
            elif choice == '5':
                self.customize_prompts()
            elif choice == '6':
                self.show_status()
            elif choice == '7':
                print("\n👋 Goodbye!\n")
                break
            else:
                print("\n❌ Invalid option. Please try again.\n")


def main():
    """Entry point"""
    cli = GrokCLI()
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--setup':
            cli.setup_keys()
        elif sys.argv[1] == '--test-grok':
            cli.test_grok()
        elif sys.argv[1] == '--test-blackbox':
            cli.test_blackbox()
        elif sys.argv[1] == '--status':
            cli.show_status()
        else:
            print(f"Unknown argument: {sys.argv[1]}")
            print("Usage: python3 grok_cli.py [--setup|--test-grok|--test-blackbox|--status]")
    else:
        cli.run()


if __name__ == "__main__":
    main()
