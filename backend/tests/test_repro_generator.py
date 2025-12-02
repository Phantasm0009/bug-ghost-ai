"""Tests for the reproduction generator service."""
import pytest
from unittest.mock import Mock, AsyncMock
from app.services.repro_generator import ReproductionGenerator
from app.schemas.debug_session import DebugSessionCreate


@pytest.mark.asyncio
async def test_generate_reproduction_success():
    """Test successful reproduction generation."""
    
    # Mock LLM client
    mock_llm = Mock()
    mock_llm.generate_completion = AsyncMock(return_value="""
    {
        "repro_code": "console.log('test');",
        "test_code": "test('should work', () => {});",
        "explanation": "The error occurs because...",
        "fix_suggestion": "Fix by doing X"
    }
    """)
    
    # Create generator
    generator = ReproductionGenerator(mock_llm)
    
    # Test data
    session_data = DebugSessionCreate(
        language="javascript",
        runtime_info="Node 18",
        error_text="TypeError: Cannot read property 'x' of undefined",
        code_snippet="const obj = {}; console.log(obj.x.y);",
        context_description="Happens on form submit"
    )
    
    # Generate
    result = await generator.generate_reproduction(session_data)
    
    # Assertions
    assert result.repro_code == "console.log('test');"
    assert result.test_code == "test('should work', () => {});"
    assert "error occurs" in result.explanation.lower()
    assert "Fix by doing X" in result.fix_suggestion


@pytest.mark.asyncio
async def test_generate_reproduction_handles_malformed_json():
    """Test handling of malformed JSON response."""
    
    # Mock LLM client returning invalid JSON
    mock_llm = Mock()
    mock_llm.generate_completion = AsyncMock(return_value="This is not JSON")
    
    generator = ReproductionGenerator(mock_llm)
    
    session_data = DebugSessionCreate(
        language="python",
        error_text="NameError: name 'x' is not defined"
    )
    
    result = await generator.generate_reproduction(session_data)
    
    # Should return error message in explanation
    assert "Failed to parse" in result.explanation
    assert "Could not parse" in result.repro_code
