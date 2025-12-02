"""Generic LLM client supporting multiple providers."""
import json
from abc import ABC, abstractmethod
from typing import Optional
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic


class BaseLLMClient(ABC):
    """Abstract base class for LLM clients."""
    
    @abstractmethod
    async def generate_completion(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate a completion from the LLM."""
        pass


class OpenAIClient(BaseLLMClient):
    """OpenAI client implementation."""
    
    def __init__(self, api_key: str, model: str):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
    
    async def generate_completion(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate completion using OpenAI."""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=4000
        )
        
        return response.choices[0].message.content


class AnthropicClient(BaseLLMClient):
    """Anthropic Claude client implementation."""
    
    def __init__(self, api_key: str, model: str):
        self.client = AsyncAnthropic(api_key=api_key)
        self.model = model
    
    async def generate_completion(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate completion using Anthropic."""
        message = await self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            system=system_prompt or "",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return message.content[0].text


class LLMClient:
    """Factory for creating LLM clients."""
    
    @staticmethod
    def create(provider: str, api_key: str, model: str) -> BaseLLMClient:
        """Create an LLM client based on provider."""
        if provider.lower() == "openai":
            return OpenAIClient(api_key, model)
        elif provider.lower() == "anthropic":
            return AnthropicClient(api_key, model)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
