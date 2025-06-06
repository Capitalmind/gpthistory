# GPTHistory - OpenAI API v1+ Compatible Fork

A Python command line tool to help you search your ChatGPT conversation history with semantic search using OpenAI embeddings.

## 🆕 What's New in This Fork

This fork updates the original gpthistory tool to work with modern OpenAI API:

- ✅ **OpenAI API v1+ Compatible** - Works with latest OpenAI library
- ✅ **Flexible API Key Loading** - Supports `~/.bin/.env` or standard `.env` files
- ✅ **Latest Embedding Model** - Uses `text-embedding-3-small` for better performance
- ✅ **Better Error Handling** - Graceful failures and detailed logging
- ✅ **Backward Compatible** - Same CLI interface as original

## Installation

### Install this updated fork (recommended)

```bash
pipx install git+https://github.com/Capitalmind/gpthistory.git@updated-openai-api
```

### Install from source

```bash
git clone https://github.com/Capitalmind/gpthistory.git
cd gpthistory
git checkout updated-openai-api
pipx install .
```

## Setup

### 1. Export your ChatGPT conversations

1. Go to [ChatGPT Settings](https://chat.openai.com/settings) → Data controls → Export data
2. Download and extract the ZIP file
3. Locate the `conversations.json` file

### 2. Set up your OpenAI API key

**Option 1: Create `~/.bin/.env` (recommended for centralized key storage)**
```bash
mkdir -p ~/.bin
echo "OPENAI_API_KEY=your_api_key_here" >> ~/.bin/.env
```

**Option 2: Use standard `.env` in your project directory**
```bash
echo "OPENAI_API_KEY=your_api_key_here" >> .env
```

Get your API key from: https://platform.openai.com/api-keys

## Usage

### Build the search index

```bash
cd /path/to/your/chatgpt/export
gpthistory build-index --file conversations.json
```

This creates a searchable index with embeddings stored at `~/.gpthistory/chatindex.csv`

### Search your conversations

```bash
gpthistory search "python coding tips"
gpthistory search "machine learning algorithms"
gpthistory search "debugging techniques"
```

Results include:
- Matching conversation excerpts
- Similarity scores
- Direct ChatGPT conversation links

## What This Fork Fixes

### ❌ Original Issues
- `APIRemovedInV1` errors with OpenAI v1+
- Hardcoded API key setup requirements
- Outdated embedding models
- Poor error handling for API failures

### ✅ Fork Improvements
- Full OpenAI API v1+ compatibility
- Flexible API key loading from multiple sources
- Updated to `text-embedding-3-small` model
- Comprehensive error handling and logging
- Maintained CLI interface compatibility

## API Changes

**Original (broken with OpenAI v1+):**
```python
import openai
openai.api_key = "your-key"
response = openai.Embedding.create(...)
```

**This fork (v1+ compatible):**
```python
from openai import OpenAI
client = OpenAI(api_key="your-key")
response = client.embeddings.create(...)
```

## Cost Considerations

- Uses OpenAI's `text-embedding-3-small` model (~$0.02 per 1M tokens)
- Large conversation histories may cost a few dollars to index
- Incremental indexing only processes new conversations on subsequent runs

## Requirements

- Python 3.8+
- OpenAI API key with billing enabled
- ChatGPT conversation export file

## Troubleshooting

### "APIRemovedInV1" Error
You're using the original version. Install this fork:
```bash
pipx install git+https://github.com/Capitalmind/gpthistory.git@updated-openai-api
```

### "API Key not found"
Set up your API key in `~/.bin/.env`:
```bash
echo "OPENAI_API_KEY=sk-your-key-here" >> ~/.bin/.env
```

### Command not found
Ensure pipx is installed and in your PATH:
```bash
sudo apt install pipx
pipx ensurepath
```

## Example Usage

```bash
# Build index from your ChatGPT export
gpthistory build-index --file conversations.json

# Search for conversations about specific topics
gpthistory search "machine learning"
gpthistory search "code optimization"
gpthistory search "debugging python"
```

## Contributing

This is a community-maintained fork of [sarchak/gpthistory](https://github.com/sarchak/gpthistory).

Found a bug or want to contribute? Open an issue or submit a pull request!

## License

MIT License - same as the original project.

## Credits

- Original project: [sarchak/gpthistory](https://github.com/sarchak/gpthistory) by [@shrikar84](https://x.com/shrikar84)
- OpenAI v1+ compatibility updates: [@Capitalmind](https://github.com/Capitalmind)