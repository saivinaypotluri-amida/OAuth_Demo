from openai import AzureOpenAI
from typing import Dict, List, Optional
import logging
import time

logger = logging.getLogger(__name__)


class AzureAIService:
    def __init__(self, endpoint: str, api_key: str, deployment: str, api_version: str = "2023-05-15"):
        """Initialize Azure OpenAI service"""
        self.endpoint = endpoint
        self.api_key = api_key
        self.deployment = deployment
        self.api_version = api_version
        
        self.client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version=api_version
        )
    
    async def test_connection(self) -> Dict[str, any]:
        """Test Azure OpenAI connection"""
        try:
            # Test with a simple completion
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=10
            )
            
            return {
                "status": "success",
                "message": "Successfully connected to Azure OpenAI",
                "details": {
                    "deployment": self.deployment,
                    "model": response.model
                }
            }
        except Exception as e:
            logger.error(f"Azure OpenAI connection test failed: {e}")
            return {
                "status": "failed",
                "message": f"Connection failed: {str(e)}",
                "details": None
            }
    
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> Dict:
        """Generate AI response"""
        start_time = time.time()
        
        try:
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            end_time = time.time()
            execution_time_ms = (end_time - start_time) * 1000
            
            return {
                "success": True,
                "response": response.choices[0].message.content,
                "tokens_used": response.usage.total_tokens,
                "execution_time_ms": execution_time_ms,
                "model": response.model
            }
        except Exception as e:
            logger.error(f"Failed to generate AI response: {e}")
            end_time = time.time()
            return {
                "success": False,
                "error": str(e),
                "execution_time_ms": (end_time - start_time) * 1000
            }
    
    async def generate_summary(
        self,
        content: str,
        max_tokens: int = 500
    ) -> Dict:
        """Generate a summary of the given content"""
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that creates concise and informative summaries. "
                          "Create a well-structured summary with key points and important details."
            },
            {
                "role": "user",
                "content": f"Please create a comprehensive summary of the following content:\n\n{content}"
            }
        ]
        
        return await self.generate_response(messages, max_tokens=max_tokens, temperature=0.5)
    
    async def answer_question(
        self,
        question: str,
        context: Optional[str] = None
    ) -> Dict:
        """Answer a question, optionally with context"""
        messages = [
            {
                "role": "system",
                "content": "You are a helpful AI assistant integrated with Slack. "
                          "Provide clear, concise, and accurate responses to user questions."
            }
        ]
        
        if context:
            messages.append({
                "role": "system",
                "content": f"Context: {context}"
            })
        
        messages.append({
            "role": "user",
            "content": question
        })
        
        return await self.generate_response(messages)
