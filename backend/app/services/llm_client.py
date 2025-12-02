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
        # Fallback to dummy client if no API key provided (local dev/testing)
        if not api_key:
            return DummyLLMClient()
        if provider.lower() == "openai":
            return OpenAIClient(api_key, model)
        if provider.lower() == "anthropic":
            return AnthropicClient(api_key, model)
        # Unknown provider -> dummy
        return DummyLLMClient()


class DummyLLMClient(BaseLLMClient):
    """Deterministic offline LLM fallback for local development.

    Generates a minimal JSON response so the UI can function without real LLM keys.
    """

    async def generate_completion(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        # Very small heuristic: detect language mentioned in prompt to tailor reproduction
        language = "python"
        lowered = prompt.lower()
        if "javascript" in lowered or "node" in lowered or "typescript" in lowered:
            language = "javascript"
        elif "java" in lowered:
            language = "java"

        if language == "python":
            repro = "def buggy(x):\n    return x['missing']\n\nprint(buggy({}))  # KeyError"
            test = "import pytest\n\ndef buggy(x):\n    return x['missing']\n\ndef test_buggy():\n    with pytest.raises(KeyError):\n        buggy({})"
            explanation = "Accessing a non-existent key raises KeyError. The reproduction shows direct dict indexing without presence check."
            fix = "Use x.get('missing') or check 'missing' in x before access."
        elif language == "javascript":
            repro = "function buggy(obj){ return obj.missing.toLowerCase(); }\nconsole.log(buggy({})); // TypeError"
            test = "test('buggy throws', () => { expect(() => buggy({})).toThrow(TypeError); });"
            explanation = "Calling toLowerCase() on undefined causes a TypeError. Missing property access isn't guarded."
            fix = "Add optional chaining (obj.missing?.toLowerCase()) or validate input before use."
        else:  # java
            repro = "public class Main { public static void main(String[] a){ String s = null; System.out.println(s.toLowerCase()); } }"
            test = "// JUnit test would assert NullPointerException when invoking toLowerCase on null"
            explanation = "Dereferencing null String leads to NullPointerException."
            fix = "Initialize the variable or guard against null before calling methods."

        return json.dumps({
            "repro_code": repro,
            "test_code": test,
            "explanation": explanation,
            "fix_suggestion": fix
        })
