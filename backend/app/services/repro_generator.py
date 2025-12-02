"""Service for generating bug reproductions using LLM."""
import json
from typing import Optional
from app.schemas.debug_session import DebugSessionCreate, ReproductionResult
from app.services.llm_client import BaseLLMClient


class ReproductionGenerator:
    """Generates bug reproductions using an LLM."""
    
    def __init__(self, llm_client: BaseLLMClient):
        self.llm_client = llm_client
    
    def _build_prompt(self, session_data: DebugSessionCreate) -> tuple[str, str]:
        """Build the prompt for LLM."""
        
        system_prompt = """You are an expert debugging assistant. Your task is to analyze errors and generate:
1. A minimal reproduction script
2. A unit test that triggers the bug
3. A clear explanation of the root cause
4. A suggested fix

You must respond with ONLY valid JSON in this exact format:
{
  "repro_code": "// minimal reproduction code here",
  "test_code": "// unit test code here",
  "explanation": "Clear explanation of the root cause",
  "fix_suggestion": "How to fix the issue, potentially with code"
}

Make the reproduction as minimal as possible while still triggering the error.
The test should use appropriate testing frameworks (Jest for JS/TS, pytest for Python, etc.)."""

        user_prompt = f"""Please analyze this error and generate a reproduction:

**Language:** {session_data.language}
**Runtime:** {session_data.runtime_info or 'Not specified'}

**Error:**
```
{session_data.error_text}
```

**Code Snippet:**
```
{session_data.code_snippet or 'Not provided'}
```

**Context:**
{session_data.context_description or 'No additional context'}

Generate a minimal reproduction, test, explanation, and fix suggestion.
Respond with ONLY the JSON object, no markdown formatting."""

        return system_prompt, user_prompt
    
    async def generate_reproduction(self, session_data: DebugSessionCreate) -> ReproductionResult:
        """Generate a reproduction using the LLM."""
        
        system_prompt, user_prompt = self._build_prompt(session_data)
        
        try:
            # Get response from LLM
            response = await self.llm_client.generate_completion(user_prompt, system_prompt)
            
            # Clean response (remove markdown code blocks if present)
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            
            # Parse JSON
            result_dict = json.loads(response)
            
            # Validate and create result
            return ReproductionResult(
                repro_code=result_dict.get("repro_code", ""),
                test_code=result_dict.get("test_code", ""),
                explanation=result_dict.get("explanation", ""),
                fix_suggestion=result_dict.get("fix_suggestion", "")
            )
            
        except json.JSONDecodeError as e:
            # Fallback: try to extract information manually
            return ReproductionResult(
                repro_code="// Error: Could not parse LLM response",
                test_code="// Error: Could not parse LLM response",
                explanation=f"Failed to parse LLM response: {str(e)}\n\nRaw response:\n{response[:500]}",
                fix_suggestion="Please try again or provide more context."
            )
        except Exception as e:
            raise Exception(f"Error generating reproduction: {str(e)}")
