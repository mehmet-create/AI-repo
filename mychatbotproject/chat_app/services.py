# chat_app/services.py
import os
from google import genai 

class MiceInfoAgent:
    """Core logic for the Mus Musculus Bot, powered by Gemini."""
    
    SYSTEM_PROMPT = (
        "You are an expert zoologist specializing in the common house mouse (*Mus musculus*). "
        "Provide factual, accurate, and concise answers to questions about their biology, "
        "behavior, lifespan, and diet. **LIMIT YOUR RESPONSE to a maximum of 3 sentences.** "
        "If the question is not about mice, politely state that your expertise is limited to Mus musculus."
    )

    def __init__(self):
        # 🚨 Client will automatically pick up the GEMINI_API_KEY environment variable.
        try:
            self.client = genai.Client()
            self.model_name = "gemini-2.5-flash"
        except Exception as e:
            # Handle case where key might be missing
            print(f"Failed to initialize Gemini Client: {e}")
            self.client = None

    def get_mouse_info(self, user_query: str) -> str:
        """Sends the user query and system prompt to Gemini."""
        if not self.client:
            return "Agent service is unavailable. Please check the API key configuration."
            
        try:
            # Structure the prompt for the best results
            full_prompt = self.SYSTEM_PROMPT + "\n\nUser Question: " + user_query
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[
                    {"role": "user", "parts": [{"text": full_prompt}]}
                ],
                # Optional safety setting to ensure a quick response
                config={"max_output_tokens": 250} 
            )
            return response.text.strip()
            
        except Exception as e:
            print(f"Gemini API Error: {e}")
            return "I apologize, but I encountered an error while processing your request."