# Bug Ghost AI - Node.js Sandbox
# Minimal Node.js environment for JavaScript/TypeScript execution
FROM node:20-alpine

# Create non-root user (remove existing user if UID conflicts)
RUN deluser node 2>/dev/null || true && \
    adduser -D -u 1000 sandbox

# Create workspace
RUN mkdir /workspace && chown sandbox:sandbox /workspace

# Set working directory
WORKDIR /workspace

# Install global packages
RUN npm install -g typescript ts-node jest

# Switch to non-root user
USER sandbox

# Default command
CMD ["node", "--version"]
