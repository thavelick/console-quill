# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Console Quill is a development tool that captures console.log, console.warn, and console.error messages from web pages and logs them to a file. It consists of:

1. A Python HTTP server that serves JavaScript and receives log data
2. A JavaScript client that overrides console methods
3. A command-line interface for easy usage

## Development Environment Setup

Before making changes:
1. Run `make install` to install in development mode
2. Run `make dev` to start the development server
3. The server will be available at http://localhost:9876

## Development Workflow

### Before committing changes:
1. Run `make lint` to format code and fix style issues
2. Test functionality manually using test.html
3. Verify both browser console and log file output work correctly

### Making changes:
- Follow existing code patterns and conventions
- Test with various console message types (log, warn, error)
- Update documentation when needed

### Common development commands:
- `make dev` - Start development server with test.log
- `make lint` - Format and fix code style with ruff
- `make install` - Install in development mode
- `make clean` - Clean up test files
- `make update` - Update dependencies
- `make help` - Show all available commands

## Project Structure

- `console_quill/server.py` - Main HTTP server implementation
- `console_quill/static/console-quill.js` - JavaScript client for console override
- `console_quill/__init__.py` - Package initialization
- `pyproject.toml` - Project configuration with entry point
- `test.html` - Test file for manual testing

## Testing

Manual testing workflow:
1. Run `make dev` to start the server
2. Open `test.html` in a browser
3. Check browser console and `test.log` file for output
4. Click the "Test Console Logs" button to generate more test messages
5. Verify server connection errors are handled silently

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