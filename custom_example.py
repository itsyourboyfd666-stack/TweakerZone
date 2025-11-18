#!/usr/bin/env python3
"""
Custom Grok-Blackbox Integration Examples
Demonstrates how to customize the integration for specific use cases
"""

from grok_blackbox_integration import GrokBlackboxConnector
import json


class CustomGrokBlackbox(GrokBlackboxConnector):
    """Extended connector with custom methods"""
    
    def security_audit(self, code: str, language: str = "python") -> dict:
        """
        Perform security audit on code using both Grok and Blackbox
        
        Args:
            code: Source code to audit
            language: Programming language
            
        Returns:
            Security audit report
        """
        print(f"🔒 Running security audit on {language} code...\n")
        
        # Use Grok for security analysis
        grok_analysis = None
        if self.grok_api_key:
            messages = [
                {
                    "role": "system",
                    "content": "You are a cybersecurity expert. Analyze code for vulnerabilities including SQL injection, XSS, CSRF, insecure deserialization, and other OWASP Top 10 issues."
                },
                {
                    "role": "user",
                    "content": f"Analyze this {language} code for security vulnerabilities:\n\n```{language}\n{code}\n```"
                }
            ]
            
            try:
                response = self.grok_chat(messages, temperature=0.3)
                grok_analysis = response['choices'][0]['message']['content']
            except Exception as e:
                grok_analysis = f"Error: {e}"
        
        # Use Blackbox for code quality
        blackbox_analysis = None
        if self.blackbox_api_key:
            try:
                blackbox_analysis = self.blackbox_query(
                    f"Review this {language} code for security issues and best practices:\n{code}",
                    mode="code",
                    language=language
                )
            except Exception as e:
                blackbox_analysis = f"Error: {e}"
        
        return {
            "code": code,
            "language": language,
            "grok_security_analysis": grok_analysis,
            "blackbox_analysis": blackbox_analysis,
            "timestamp": __import__('datetime').datetime.now().isoformat()
        }
    
    def explain_like_im_five(self, topic: str) -> str:
        """
        Get simple explanation of complex topics
        
        Args:
            topic: Topic to explain
            
        Returns:
            Simple explanation
        """
        if not self.grok_api_key:
            return "Grok API key required"
        
        messages = [
            {
                "role": "system",
                "content": "You are a teacher who explains complex topics in simple terms that a 5-year-old could understand. Use analogies and simple language."
            },
            {
                "role": "user",
                "content": f"Explain {topic} like I'm five years old"
            }
        ]
        
        response = self.grok_chat(messages, temperature=0.8)
        return response['choices'][0]['message']['content']
    
    def code_generator(self, description: str, language: str = "python") -> dict:
        """
        Generate code from description using both APIs
        
        Args:
            description: What the code should do
            language: Target programming language
            
        Returns:
            Generated code and explanations
        """
        print(f"💻 Generating {language} code...\n")
        
        results = {
            "description": description,
            "language": language,
            "grok_code": None,
            "blackbox_code": None
        }
        
        # Grok generation
        if self.grok_api_key:
            messages = [
                {
                    "role": "system",
                    "content": f"You are an expert {language} programmer. Generate clean, well-documented code."
                },
                {
                    "role": "user",
                    "content": f"Write {language} code that: {description}\n\nInclude comments and error handling."
                }
            ]
            
            try:
                response = self.grok_chat(messages, temperature=0.5)
                results["grok_code"] = response['choices'][0]['message']['content']
            except Exception as e:
                results["grok_code"] = f"Error: {e}"
        
        # Blackbox generation
        if self.blackbox_api_key:
            try:
                results["blackbox_code"] = self.blackbox_query(
                    description,
                    mode="code",
                    language=language
                )
            except Exception as e:
                results["blackbox_code"] = f"Error: {e}"
        
        return results
    
    def debug_helper(self, error_message: str, code_context: str = "") -> str:
        """
        Get debugging help for errors
        
        Args:
            error_message: The error message
            code_context: Optional code that caused the error
            
        Returns:
            Debugging suggestions
        """
        if not self.grok_api_key:
            return "Grok API key required"
        
        context = f"\n\nCode context:\n```\n{code_context}\n```" if code_context else ""
        
        messages = [
            {
                "role": "system",
                "content": "You are a debugging expert. Analyze errors and provide clear, actionable solutions."
            },
            {
                "role": "user",
                "content": f"Help me debug this error:\n\n{error_message}{context}\n\nProvide:\n1. What caused the error\n2. How to fix it\n3. How to prevent it"
            }
        ]
        
        response = self.grok_chat(messages, temperature=0.3)
        return response['choices'][0]['message']['content']
    
    def learning_path(self, skill: str, current_level: str = "beginner") -> str:
        """
        Generate personalized learning path
        
        Args:
            skill: Skill to learn
            current_level: Current skill level (beginner/intermediate/advanced)
            
        Returns:
            Learning path recommendations
        """
        if not self.grok_api_key:
            return "Grok API key required"
        
        messages = [
            {
                "role": "system",
                "content": "You are a learning advisor. Create structured, practical learning paths."
            },
            {
                "role": "user",
                "content": f"Create a learning path for {skill}. Current level: {current_level}.\n\nInclude:\n1. Prerequisites\n2. Step-by-step topics\n3. Practical projects\n4. Resources\n5. Timeline estimate"
            }
        ]
        
        response = self.grok_chat(messages, temperature=0.7)
        return response['choices'][0]['message']['content']


def demo_security_audit():
    """Demo: Security audit"""
    print("\n" + "="*60)
    print("DEMO 1: Security Audit")
    print("="*60 + "\n")
    
    connector = CustomGrokBlackbox()
    
    vulnerable_code = """
def login(username, password):
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    result = db.execute(query)
    return result
"""
    
    audit = connector.security_audit(vulnerable_code, "python")
    
    if audit['grok_security_analysis']:
        print("🔒 Security Analysis:")
        print(audit['grok_security_analysis'])
    else:
        print("⚠️  Set XAI_API_KEY to run security audit")


def demo_explain_simple():
    """Demo: Simple explanations"""
    print("\n" + "="*60)
    print("DEMO 2: Explain Like I'm Five")
    print("="*60 + "\n")
    
    connector = CustomGrokBlackbox()
    
    if connector.grok_api_key:
        explanation = connector.explain_like_im_five("blockchain technology")
        print(f"📚 Simple Explanation:\n{explanation}")
    else:
        print("⚠️  Set XAI_API_KEY to run this demo")


def demo_code_generation():
    """Demo: Code generation"""
    print("\n" + "="*60)
    print("DEMO 3: Code Generation")
    print("="*60 + "\n")
    
    connector = CustomGrokBlackbox()
    
    result = connector.code_generator(
        "Create a function that validates email addresses using regex",
        "python"
    )
    
    if result['grok_code']:
        print("💻 Generated Code (Grok):")
        print(result['grok_code'])
    else:
        print("⚠️  Set XAI_API_KEY to generate code")


def demo_debugging():
    """Demo: Debugging helper"""
    print("\n" + "="*60)
    print("DEMO 4: Debug Helper")
    print("="*60 + "\n")
    
    connector = CustomGrokBlackbox()
    
    error = "TypeError: 'NoneType' object is not subscriptable"
    code = """
def get_user_data(user_id):
    user = database.find_user(user_id)
    return user['name']  # Error happens here
"""
    
    if connector.grok_api_key:
        solution = connector.debug_helper(error, code)
        print(f"🐛 Debug Solution:\n{solution}")
    else:
        print("⚠️  Set XAI_API_KEY to run debugging demo")


def demo_learning_path():
    """Demo: Learning path generator"""
    print("\n" + "="*60)
    print("DEMO 5: Learning Path Generator")
    print("="*60 + "\n")
    
    connector = CustomGrokBlackbox()
    
    if connector.grok_api_key:
        path = connector.learning_path("penetration testing", "beginner")
        print(f"📖 Learning Path:\n{path}")
    else:
        print("⚠️  Set XAI_API_KEY to generate learning path")


def main():
    """Run all demos"""
    print("\n🎨 Custom Grok-Blackbox Integration Examples\n")
    print("These demos show how to customize the integration for specific use cases.\n")
    
    # Check API keys
    connector = CustomGrokBlackbox()
    if not connector.grok_api_key:
        print("⚠️  Note: Set XAI_API_KEY environment variable to run all demos")
        print("   export XAI_API_KEY='your-key-here'\n")
    
    # Run demos
    demos = [
        demo_security_audit,
        demo_explain_simple,
        demo_code_generation,
        demo_debugging,
        demo_learning_path
    ]
    
    for demo in demos:
        try:
            demo()
            input("\nPress Enter to continue to next demo...")
        except KeyboardInterrupt:
            print("\n\n👋 Demos interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error in demo: {e}")
            input("\nPress Enter to continue...")
    
    print("\n✅ All demos complete!")
    print("\nTo create your own customizations:")
    print("1. Extend the CustomGrokBlackbox class")
    print("2. Add your custom methods")
    print("3. Use the existing grok_chat() and blackbox_query() methods")
    print("\nSee custom_example.py for implementation details.\n")


if __name__ == "__main__":
    main()
