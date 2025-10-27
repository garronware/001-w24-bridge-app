# Overview

This is a Flask-based web application that integrates with the Werk24 API to analyze technical drawings. The application provides both a web interface and a REST API endpoint for processing engineering drawings and extracting metadata, features, and insights from them. It's designed to work with n8n automation workflows through CORS-enabled API endpoints.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Web Framework
- **Flask** - Chosen as the lightweight web framework for handling HTTP requests
- Provides both API endpoints and a simple web UI for manual testing
- Rationale: Flask's simplicity makes it ideal for microservices and API-first applications

## API Design
- **RESTful endpoint** (`/process-drawing`) - Accepts POST requests with drawing files
- **CORS enabled** - Configured with `origins="*"` to allow integration with n8n and other automation tools
- Returns JSON-formatted analysis results from Werk24
- Rationale: REST architecture provides a simple, stateless interface that integrates easily with automation platforms

## Asynchronous Processing
- **Async/await pattern** - Used for Werk24 API communication to handle I/O-bound operations efficiently
- `analyze_drawing()` function implements async context managers and comprehensions
- Rationale: Technical drawing analysis can be time-intensive; async operations prevent blocking

## Drawing Analysis Pipeline
- **Werk24 SDK integration** - Uses official Python client for technical drawing interpretation
- **Multi-aspect extraction** - Configured to extract three types of data:
  - Metadata (drawing information)
  - Features (geometric elements)
  - Insights (derived intelligence)
- **Stream processing** - Filters messages by type (`TechreadMessageType.ASK`) and processes only valid payloads
- Rationale: Comprehensive extraction provides maximum value from each drawing analysis

## Frontend Architecture
- **Server-side rendering** - Uses Flask's template engine (Jinja2) to serve HTML
- Simple single-page interface for manual testing and demonstration
- Gradient-styled UI with modern CSS for better user experience
- Rationale: Minimal frontend keeps the application focused on API functionality while still providing testing capabilities

# External Dependencies

## Third-Party Services
- **Werk24 API** - Cloud-based technical drawing analysis service
  - Requires authentication (credentials expected via environment or SDK configuration)
  - Provides AI-powered interpretation of engineering drawings
  - Handles various drawing formats and standards

## Python Packages
- **Flask** - Web framework (v2.x+)
- **flask-cors** - Cross-origin resource sharing middleware
- **werk24** - Official Werk24 Python SDK
  - Includes async client (`Werk24Client`)
  - Provides structured data models and message types

## Infrastructure Requirements
- **Python 3.7+** - Required for async/await syntax
- **Environment variables** - Werk24 API credentials (authentication method to be configured)
- No database currently configured (stateless application)

## Integration Points
- **n8n compatibility** - CORS configuration specifically mentions n8n automation platform
- File upload handling via HTTP multipart/form-data
- JSON response format for easy consumption by automation tools