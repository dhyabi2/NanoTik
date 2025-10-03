# NanoTik - AI Video Generator

## Overview

NanoTik is an AI-powered video generation platform that creates professional videos from text prompts, integrated with Nano cryptocurrency payments. The application combines multiple AI services (LLM for script generation, Azure Speech for voiceovers, Pexels for video clips) with a cryptocurrency payment system to deliver a complete video production solution. Built with Python and Streamlit, it offers a multi-language web interface supporting English, Chinese, and Arabic.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application with responsive design
- **UI Components**: Wide layout with expandable sidebar for navigation and payment controls
- **State Management**: Streamlit session state for user sessions, credits, language preferences, and transaction history
- **Internationalization**: Custom i18n utility supporting 3 languages (English, Chinese, Arabic) with translation dictionaries

**Rationale**: Streamlit provides rapid development of data-driven applications with minimal frontend code. The session state approach keeps user data persistent across interactions without requiring complex state management libraries.

### Backend Architecture
- **Application Structure**: Modular service-oriented architecture with separated concerns:
  - `services/`: Business logic (LLM, Payment, Video services)
  - `models/`: Data models (UserSession)
  - `utils/`: Helper functions (i18n)
- **Configuration**: TOML-based config with environment variable overrides (priority: env vars > config.toml > config.example.toml)
- **Video Processing Pipeline**: Multi-stage workflow:
  1. Script generation via LLM
  2. Voiceover synthesis with Azure Speech
  3. Video clip sourcing from Pexels
  4. Final composition with MoviePy

**Rationale**: Service-oriented design allows independent scaling and testing of components. The pipeline architecture enables monitoring and failure recovery at each stage of video generation.

### Data Storage
- **Database**: PostgreSQL with psycopg2 driver
- **Schema Design**:
  - `users`: Tracks user sessions, credits, and activity timestamps
  - `videos`: Stores generated video metadata with foreign key to users
- **Connection Pattern**: Context manager pattern for automatic connection cleanup
- **Initialization**: Automatic table creation on first database connection

**Rationale**: PostgreSQL provides ACID compliance for payment and credit transactions. The foreign key relationship ensures referential integrity between users and their videos.

### Authentication & Authorization
- **Session Management**: UUID-based session IDs stored in Streamlit session state
- **User Tracking**: Anonymous sessions linked to database users via session_id
- **Credit System**: Integer-based credits stored in database, checked before video generation

**Rationale**: Anonymous session approach eliminates registration friction while maintaining user state. Database-backed credits ensure consistency even if session state is lost.

### AI/LLM Integration
- **Multi-Provider Support**: Pluggable LLM architecture supporting:
  - OpenAI (GPT-4)
  - DeepSeek
  - Moonshot AI
- **Provider Selection**: Configuration-driven provider switching via environment variables
- **Client Initialization**: Unified OpenAI client interface with provider-specific base URLs

**Rationale**: Multi-provider approach prevents vendor lock-in and allows cost optimization by switching between providers based on pricing and availability.

### Video Generation Architecture
- **Script Generation**: LLM service creates structured scripts based on topic and duration
- **Voiceover Synthesis**: Azure Cognitive Services Speech SDK for text-to-speech
- **Video Sourcing**: Pexels API integration for stock video clips
- **Composition**: MoviePy for video editing, effects, and final rendering
- **Quality Tiers**: Three-tier system (Basic/HD/Premium) with different credit costs

**Rationale**: Azure Speech provides high-quality multilingual voices. Pexels offers free stock footage. MoviePy enables programmatic video editing without external dependencies.

### Payment System
- **Cryptocurrency**: Nano cryptocurrency for instant, fee-less transactions
- **Payment Flow**: UUID-based payment requests with address generation
- **Credit Conversion**: Direct mapping of NANO amounts to credit values
- **Transaction Tracking**: Payment IDs linked to user sessions for audit trail

**Rationale**: Nano eliminates transaction fees and provides instant settlement, crucial for micropayments. The simulated payment flow structure allows easy integration with actual Nano MCP server.

## External Dependencies

### Third-Party APIs
- **OpenAI API**: LLM for script generation (supports custom base URLs for compatible providers)
- **DeepSeek API**: Alternative LLM provider (base URL: https://api.deepseek.com/v1)
- **Moonshot API**: Alternative LLM provider (base URL: https://api.moonshot.cn/v1)
- **Azure Cognitive Services**: Speech synthesis API (configurable region)
- **Pexels API**: Stock video footage (supports multiple API keys for rate limiting)
- **Nano MCP Server**: Cryptocurrency payment processing (environment: NANO_MCP_URL)

### Python Libraries
- **streamlit**: Web application framework
- **psycopg2**: PostgreSQL database driver with RealDictCursor support
- **openai**: Unified client for multiple LLM providers
- **azure-cognitiveservices-speech**: Azure Speech SDK
- **pexels-api**: Pexels video search client
- **moviepy**: Video editing and composition
- **toml**: Configuration file parsing

### Database
- **PostgreSQL**: Primary data store accessed via DATABASE_URL environment variable
- **Schema**: Auto-created tables for users and videos with timestamp tracking
- **Connection Pooling**: Not implemented (uses direct connections with context managers)

### Environment Configuration
- Required environment variables:
  - `DATABASE_URL`: PostgreSQL connection string
  - `OPENAI_API_KEY`, `DEEPSEEK_API_KEY`, `MOONSHOT_API_KEY`: LLM provider keys
  - `AZURE_SPEECH_KEY`, `AZURE_SPEECH_REGION`: Azure Speech credentials
  - `PEXELS_API_KEYS`: Comma-separated list of Pexels API keys
  - `NANO_MCP_URL`, `NANO_WALLET_ADDRESS`: Nano payment configuration
  - `LLM_PROVIDER`: Provider selection (openai/deepseek/moonshot)

### File System Dependencies
- **Output Directories**: Configurable paths for generated videos and temporary files
- **Video Storage**: Local filesystem storage with path references in database
- **Temp Files**: Automatic cleanup not implemented (manual temp directory management)