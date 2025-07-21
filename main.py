#!/usr/bin/env python3
"""
Universal AI Assistant Framework
A versatile framework for building AI assistants with multiple capabilities.
"""

import os
import json
import openai
from typing import Dict, List, Any, Optional
from datetime import datetime

class UniversalAssistant:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the universal AI assistant."""
        self.client = openai.OpenAI(
            api_key=api_key or os.getenv("OPENAI_API_KEY")
        )
        self.skills = {}
        self.conversation_history = []
        
    def register_skill(self, name: str, skill_function):
        """Register a new skill with the assistant."""
        self.skills[name] = skill_function
        print(f"Skill '{name}' registered successfully.")
    
    def list_skills(self) -> List[str]:
        """List all available skills."""
        return list(self.skills.keys())
    
    def process_request(self, user_input: str) -> str:
        """
        Process user request and determine appropriate response.
        
        Args:
            user_input: User's natural language request
            
        Returns:
            Assistant's response
        """
        # Add to conversation history
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "user": user_input
        })
        
        # Determine intent and execute appropriate skill
        intent = self._analyze_intent(user_input)
        response = self._execute_skill(intent, user_input)
        
        # Add response to history
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "assistant": response
        })
        
        return response
    
    def _analyze_intent(self, user_input: str) -> Dict[str, Any]:
        """Analyze user intent to determine which skill to use."""
        system_prompt = f"""
        You are an intent classifier for a universal AI assistant.
        Available skills: {', '.join(self.skills.keys())}
        
        Analyze the user's request and return a JSON object with:
        - "skill": the most appropriate skill name (or "general" if no specific skill needed)
        - "confidence": confidence score (0-1)
        - "parameters": any parameters needed for the skill
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.1
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            return {"skill": "general", "confidence": 0.5, "parameters": {}}
    
    def _execute_skill(self, intent: Dict[str, Any], user_input: str) -> str:
        """Execute the appropriate skill based on intent analysis."""
        skill_name = intent.get("skill", "general")
        
        if skill_name in self.skills:
            try:
                return self.skills[skill_name](user_input, intent.get("parameters", {}))
            except Exception as e:
                return f"Error executing skill '{skill_name}': {str(e)}"
        else:
            # Default general conversation
            return self._general_conversation(user_input)
    
    def _general_conversation(self, user_input: str) -> str:
        """Handle general conversation when no specific skill is needed."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"I'm sorry, I encountered an error: {str(e)}"

# Example skill functions
def web_search_skill(user_input: str, parameters: Dict[str, Any]) -> str:
    """Example web search skill."""
    query = parameters.get("query", user_input)
    return f"Searching the web for: {query}\n(This is a placeholder - implement actual web search)"

def calculation_skill(user_input: str, parameters: Dict[str, Any]) -> str:
    """Example calculation skill."""
    expression = parameters.get("expression", "")
    return f"Calculating: {expression}\n(This is a placeholder - implement actual calculation)"

def main():
    """Main function to run the universal assistant."""
    assistant = UniversalAssistant()
    
    # Register example skills
    assistant.register_skill("web_search", web_search_skill)
    assistant.register_skill("calculation", calculation_skill)
    
    print("Universal AI Assistant Framework")
    print("=" * 40)
    print(f"Available skills: {', '.join(assistant.list_skills())}")
    print("Type 'quit' to exit\n")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == 'quit':
            break
            
        response = assistant.process_request(user_input)
        print(f"Assistant: {response}\n")

if __name__ == "__main__":
    main()

