# Bug Ghost AI - Java Sandbox
# Minimal Java environment for code execution
FROM eclipse-temurin:17-jdk-alpine

# Create non-root user (remove existing user if UID conflicts)
RUN deluser $(getent passwd 1000 | cut -d: -f1) 2>/dev/null || true && \
    adduser -D -u 1000 sandbox

# Create workspace
RUN mkdir /workspace && chown sandbox:sandbox /workspace

# Set working directory
WORKDIR /workspace

# Switch to non-root user
USER sandbox

# Default command
CMD ["java", "--version"]
