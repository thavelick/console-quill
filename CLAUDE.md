# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Console Quill is a development tool that captures console.log, console.warn, and console.error messages from web pages and logs them to a file. It consists of:

1. A Python HTTP server that serves JavaScript and receives log data
2. A JavaScript client that overrides console methods
3. A command-line interface for easy usage

## Development Commands

### Installation and Setup
```bash
# Install in development mode
uv tool install -e .

# Run the server for testing
console-quill --logfile test.log --port 9876
```

### Project Structure
- `console_quill/server.py` - Main HTTP server implementation
- `console_quill/static/console-quill.js` - JavaScript client for console override
- `console_quill/__init__.py` - Package initialization
- `pyproject.toml` - Project configuration with entry point

### Testing
Test the functionality by:
1. Running the server: `console-quill --logfile test.log`
2. Creating a test HTML file with `<script src="http://localhost:9876/console-quill.js"></script>`
3. Opening the HTML file and checking both browser console and log file

## Architecture

The system uses Python's built-in `http.server` module to create a lightweight HTTP server that:
- Serves the JavaScript file at `/console-quill.js`
- Accepts POST requests at `/log` endpoint
- Writes log entries as JSON lines to the specified file

The JavaScript client preserves original console behavior while additionally sending messages to the server via fetch() requests.

## Key Design Decisions

- Uses only Python standard library (no external dependencies)
- Default port 9876 to avoid conflicts with common development servers
- JSON Lines format for log file (one JSON object per line)
- CORS headers to allow cross-origin requests
- Fire-and-forget approach for network requests to avoid blocking console output