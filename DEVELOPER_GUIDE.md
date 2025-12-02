# Bug Ghost AI - Developer Guide

## Project Structure

```
bug-ghost-ai/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   │   └── routes_debug.py
│   │   ├── models/         # SQLAlchemy models
│   │   │   └── debug_session.py
│   │   ├── schemas/        # Pydantic schemas
│   │   │   └── debug_session.py
│   │   ├── services/       # Business logic
│   │   │   ├── llm_client.py       # LLM abstraction
│   │   │   ├── repro_generator.py  # Reproduction generation
│   │   │   └── sandbox_runner.py   # Future: Docker execution
│   │   ├── db/             # Database config
│   │   │   └── session.py
│   │   ├── config.py       # Application settings
│   │   └── main.py         # FastAPI app entry point
│   ├── tests/              # Backend tests
│   ├── requirements.txt    # Python dependencies
│   ├── pyproject.toml      # Poetry config
│   └── Dockerfile
│
├── frontend/               # Next.js 14 frontend
│   ├── app/               # App Router pages
│   │   ├── page.tsx       # Landing page
│   │   ├── layout.tsx     # Root layout
│   │   ├── sessions/
│   │   │   ├── page.tsx   # Sessions list
│   │   │   └── [id]/page.tsx  # Session detail
│   │   └── globals.css
│   ├── components/        # React components
│   │   ├── Navbar.tsx
│   │   ├── ErrorForm.tsx
│   │   ├── SessionResult.tsx
│   │   └── CodeBlock.tsx
│   ├── lib/              # Utilities
│   │   ├── api.ts        # API client
│   │   └── types.ts      # TypeScript types
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   └── Dockerfile
│
├── docker-compose.yml     # Full stack orchestration
├── README.md             # Project documentation
├── CONTRIBUTING.md       # Contribution guidelines
├── LICENSE               # MIT License
└── .gitignore
```

## Architecture Overview

### Backend Architecture

**FastAPI Application:**
- RESTful API design
- Async/await for LLM calls
- SQLAlchemy ORM for database
- Pydantic for validation
- Dependency injection pattern

**Key Components:**

1. **API Layer** (`app/api/`)
   - REST endpoints
   - Request validation
   - Response serialization

2. **Service Layer** (`app/services/`)
   - `LLMClient`: Abstract LLM provider (OpenAI/Anthropic)
   - `ReproductionGenerator`: Core AI logic for generating reproductions
   - `SandboxRunner`: Future Docker execution (Phase 2)

3. **Data Layer** (`app/models/`, `app/schemas/`)
   - SQLAlchemy models for DB
   - Pydantic schemas for API

### Frontend Architecture

**Next.js 14 App Router:**
- Server and client components
- File-based routing
- TypeScript for type safety
- Tailwind CSS for styling

**Key Components:**

1. **Pages**
   - `/`: Landing page with error form
   - `/sessions`: List of all sessions
   - `/sessions/[id]`: Individual session view

2. **Components**
   - `ErrorForm`: Multi-step error submission
   - `SessionResult`: Tabbed result view
   - `CodeBlock`: Syntax-highlighted code display
   - `Navbar`: Navigation

3. **API Integration**
   - Axios client in `lib/api.ts`
   - TypeScript types in `lib/types.ts`

### Database Schema

**DebugSession Table:**
```sql
CREATE TABLE debug_sessions (
    id UUID PRIMARY KEY,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    
    -- Input
    language VARCHAR(50) NOT NULL,
    runtime_info VARCHAR(200),
    error_text TEXT NOT NULL,
    code_snippet TEXT,
    context_description TEXT,
    
    -- Status
    status VARCHAR(20) NOT NULL,  -- processing, completed, failed
    
    -- Output
    repro_code TEXT,
    test_code TEXT,
    explanation TEXT,
    fix_suggestion TEXT,
    
    -- Metadata
    llm_model VARCHAR(100),
    error_message TEXT
);
```

## Development Workflow

### Backend Development

1. **Start development server:**
   ```bash
   cd backend
   source venv/bin/activate  # Windows: venv\Scripts\activate
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Run tests:**
   ```bash
   pytest
   pytest --cov=app  # With coverage
   ```

3. **Add new endpoint:**
   - Create route in `app/api/routes_*.py`
   - Add schema in `app/schemas/`
   - Implement logic in `app/services/`
   - Write tests in `tests/`

### Frontend Development

1. **Start development server:**
   ```bash
   cd frontend
   npm run dev
   ```

2. **Type checking:**
   ```bash
   npm run type-check
   ```

3. **Build for production:**
   ```bash
   npm run build
   npm start
   ```

4. **Add new page:**
   - Create file in `app/` directory
   - Add components in `components/`
   - Update types in `lib/types.ts`

## API Integration

### LLM Client Design

The `LLMClient` is provider-agnostic:

```python
class BaseLLMClient(ABC):
    @abstractmethod
    async def generate_completion(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None
    ) -> str:
        pass

class OpenAIClient(BaseLLMClient):
    # Implementation for OpenAI
    
class AnthropicClient(BaseLLMClient):
    # Implementation for Anthropic
```

**Adding a new provider:**

1. Create new class inheriting from `BaseLLMClient`
2. Implement `generate_completion` method
3. Add to factory in `LLMClient.create()`
4. Update config and documentation

### Prompt Engineering

The reproduction prompt is in `ReproductionGenerator._build_prompt()`:

**Structure:**
- System prompt: Defines AI role and output format
- User prompt: Includes error, code, context
- Output: JSON with `repro_code`, `test_code`, `explanation`, `fix_suggestion`

**Improving prompts:**
- Test with various error types
- Adjust temperature for creativity vs. precision
- Add examples for few-shot learning
- Validate output structure

## Testing Strategy

### Backend Tests

**Unit Tests:**
- Service layer logic (mocked dependencies)
- Validation schemas
- Utility functions

**Integration Tests:**
- API endpoints (with test DB)
- Database operations
- LLM integration (mocked)

**Example:**
```python
@pytest.mark.asyncio
async def test_generate_reproduction():
    mock_llm = Mock()
    mock_llm.generate_completion = AsyncMock(return_value="{...}")
    
    generator = ReproductionGenerator(mock_llm)
    result = await generator.generate_reproduction(session_data)
    
    assert result.repro_code is not None
```

### Frontend Tests

**Type Safety:**
- TypeScript strict mode
- Proper typing for props and state
- API response types

**Component Tests** (future):
- React Testing Library
- User interactions
- Error states

## Performance Considerations

### Backend Optimizations

1. **Database:**
   - Connection pooling (SQLAlchemy)
   - Indexes on frequently queried fields
   - Pagination for list endpoints

2. **LLM Calls:**
   - Async/await for non-blocking
   - Timeout handling
   - Rate limiting

3. **Caching** (future):
   - Redis for session caching
   - Memoize common error patterns

### Frontend Optimizations

1. **Code Splitting:**
   - Next.js automatic code splitting
   - Dynamic imports for heavy components

2. **State Management:**
   - Local state for forms
   - Server state via API calls
   - No unnecessary re-renders

3. **Assets:**
   - Optimized images (Next.js Image)
   - CSS purging (Tailwind)
   - Font optimization

## Security Considerations

### API Security

1. **Input Validation:**
   - Pydantic schemas validate all input
   - Max length limits on text fields
   - Sanitize user input

2. **Rate Limiting:**
   - Prevent API abuse
   - Protect LLM API costs

3. **CORS:**
   - Whitelist frontend domains
   - No wildcard in production

### Data Privacy

1. **User Data:**
   - No PII collected in MVP
   - Sessions stored but not linked to users (yet)

2. **API Keys:**
   - Never expose LLM keys to frontend
   - Use environment variables
   - Rotate keys regularly

## Deployment

### Production Checklist

**Backend:**
- [ ] Set production DATABASE_URL
- [ ] Configure LLM_API_KEY
- [ ] Update CORS_ORIGINS
- [ ] Enable HTTPS
- [ ] Set up monitoring (Sentry)
- [ ] Database backups
- [ ] Rate limiting
- [ ] Health check endpoint

**Frontend:**
- [ ] Set NEXT_PUBLIC_API_URL
- [ ] Build optimization
- [ ] Enable analytics (optional)
- [ ] Error tracking
- [ ] CDN for assets

### Monitoring

**Metrics to track:**
- API response times
- LLM call success rate
- Database query performance
- Error rates
- Session creation rate

**Tools:**
- Backend: Prometheus + Grafana
- Frontend: Vercel Analytics
- Logs: CloudWatch / Datadog
- Errors: Sentry

## Troubleshooting

### Common Issues

**Backend won't start:**
- Check DATABASE_URL is correct
- Ensure PostgreSQL is running
- Verify LLM_API_KEY is set

**Frontend can't reach API:**
- Check NEXT_PUBLIC_API_URL
- Verify CORS settings
- Check network/firewall

**LLM errors:**
- Verify API key is valid
- Check rate limits
- Review prompt length

**Database migrations:**
- Tables auto-create on startup
- For changes, use Alembic migrations

## Future Enhancements

### Phase 2: Sandbox Execution

**Docker Integration:**
1. Implement `SandboxRunner.run_in_sandbox()`
2. Create language-specific Docker images
3. File I/O for code execution
4. Capture stdout/stderr
5. Security: network isolation, resource limits

**UI Updates:**
- Add "Run in Sandbox" button
- Display execution logs
- Show exit codes
- Execution timeline

### Phase 3: Advanced Features

- Team collaboration
- GitHub integration
- VS Code extension
- Browser extension
- Custom LLM models
- Analytics dashboard

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Questions?

Open an issue or discussion on GitHub!
