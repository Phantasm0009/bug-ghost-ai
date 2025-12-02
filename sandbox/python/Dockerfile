# Bug Ghost AI - Python Sandbox
# Minimal Python environment for safe code execution
FROM python:3.11-slim

# Create non-root user
RUN useradd -m -u 1000 -s /bin/bash sandbox

# Create workspace
RUN mkdir /workspace && chown sandbox:sandbox /workspace

# Set working directory
WORKDIR /workspace

# Install common packages (can be extended)
RUN pip install --no-cache-dir pytest requests

# Switch to non-root user
USER sandbox

# Default command (will be overridden)
CMD ["python", "--version"]
