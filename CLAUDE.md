# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastAPI-based medical service server with LLM integration. The project consists of:
- Multiple FastAPI microservices for different domains (chatbot, category, clinic, drug, emergency support)
- React frontend application
- Template-based architecture for extensibility
- LangChain integration for LLM capabilities with OpenAI

## Commands

### Backend Development

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run chatbot server (main server)
python application/chatbot_server/main.py

# Run with uvicorn (with reload for development)
uvicorn application.chatbot_server.main:app --host 0.0.0.0 --port 8000 --reload

# Run other microservices
python application/category_server/main.py
python application/clinic_server/main.py
python application/drug_server/main.py
python application/emergency_support_server/main.py
```

### Frontend Development

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test
```

## Architecture

### Template System
The application uses a template-based architecture centered around `BaseTemplate`:
- All domain-specific logic extends `BaseTemplate` (template/base/base_template.py)
- Templates are registered in `TemplateContext` during application startup
- Each domain (account, chatbot, category, clinic, drug, emergency_support, internal_external) has its own template implementation
- Templates handle initialization, data loading, and client lifecycle events

### Service Layer Structure
- **cache/**: Redis-based caching and session management
- **db/**: Database connectivity (MySQL pools for global and sharded databases)
- **http/**: HTTP client pool for inter-service communication
- **lang_chain/**: LLM integration modules for each domain using LangChain and OpenAI
- **net/**: Network protocol base classes

### Microservices
Each microservice follows the same pattern:
- `main.py`: FastAPI application setup with lifespan management
- `routers/`: API endpoint definitions
- Connects to specific template implementations

### Configuration
- Uses `config.json` for production and `config_debug.json` for development
- Environment variables loaded via `.env` file
- Configuration includes database, cache, message queue, and service URLs

### Key Dependencies
- **FastAPI**: Web framework
- **LangChain**: LLM orchestration
- **OpenAI**: LLM provider
- **Redis**: Caching and session management
- **MySQL**: Database (via aiomysql)
- **FAISS**: Vector database for RAG
- **Sentence Transformers**: Text embeddings

## Adding New Features

### To add a new template/domain:
1. Create template implementation in `template/[domain]/[domain]_template_impl.py`
2. Extend `BaseTemplate` class
3. Add template type to `template/base/template_type.py`
4. Register in the appropriate server's `main.py` during startup

### To add a new microservice:
1. Create directory structure under `application/[service_name]_server/`
2. Implement `main.py` with FastAPI app and lifespan management
3. Add routers in `routers/` subdirectory
4. Configure service URL in config files