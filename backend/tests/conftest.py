"""Pytest configuration."""
import pytest
import os

# Set test environment variables
os.environ["DATABASE_URL"] = "postgresql://postgres:postgres@localhost:5432/bug_ghost_test"
os.environ["LLM_API_KEY"] = "test-key"
os.environ["LLM_MODEL"] = "gpt-4"
os.environ["LLM_PROVIDER"] = "openai"
