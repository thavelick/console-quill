# Console Quill

A development tool to capture console.log, console.warn, and console.error messages from web pages and log them to a file.

## Installation

Install directly from GitHub using uv:

```bash
uv tool install git+https://github.com/thavelick/console-quill
```

## Usage

### Start the server

```bash
console-quill --logfile /path/to/your/logfile.log --port 9876
```

Options:
- `--logfile` (required): Path to the log file where console messages will be written
- `--port` (optional): Port to run the server on (default: 9876)

### Include in your web page

Add this script tag to your HTML page:

```html
<script src="http://localhost:9876/console-quill.js"></script>
```

### Log format

Console messages are logged in a Unix-style format:

```
2025-07-08 21:44:36 [LOG] Page loaded successfully
2025-07-08 21:44:36 [WARN] This is a startup warning
2025-07-08 21:44:36 [ERROR] This is a startup error
2025-07-08 21:44:37 [LOG] Testing with multiple arguments {"key":"value"} [1,2,3]
```

## How it works

1. The Python server serves a JavaScript file that overrides the browser's console methods
2. The JavaScript preserves the original console behavior (messages still appear in browser console)
3. Additionally, it sends console messages to the `/log` endpoint via HTTP POST
4. The server writes these messages to your specified log file in Unix-style format
5. Network errors are silently ignored to avoid cluttering the browser console

## License

This project is licensed under the AGPL-3.0 License - see the LICENSE file for details.

## Development

The project uses uv for dependency management and is structured as a standard Python package.

```bash
# Clone the repository
git clone https://github.com/thavelick/console-quill.git
cd console-quill

# Install in development mode
uv tool install -e .

# Run the server
console-quill --logfile test.log
```