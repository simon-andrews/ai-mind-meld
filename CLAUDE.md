# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AI Mind Meld game where two AI players attempt to converge on the same word through iterative rounds. The game simulates the improv game "Mind Meld" using OpenAI-compatible API calls through OpenRouter.

## Development Commands

- **Run the game**: `uv run python main.py`
- **See all configuration options**: `uv run python main.py --help`
- **Install dependencies**: `uv sync`
- **Format code**: `uv run ruff format`
- **Lint code**: `uv run ruff check`
- **Fix linting issues**: `uv run ruff check --fix`
- **Install pre-commit hooks**: `uv run pre-commit install`
- **Python version**: Requires Python >=3.12

## Environment Setup

- Set `OPENROUTER_API_KEY` environment variable before running
- Dictionary file (`dictionary.txt`) required for fallback words

## Architecture

- `GameState`: Dataclass tracking game progress (rounds, words, convergence status)
- `MindMeldAI`: AI player class that generates words based on game history and context
- `MindMeldGame`: Main game controller managing two AI players and game flow
- Game flow: streaming AI responses → word extraction → convergence checking → game summary

## Key Implementation Details

- **Streaming responses**: AI responses are streamed in real-time with visual thinking process display
- **Word extraction**: Uses regex pattern `FINAL WORD:\s*([A-Za-z]+)` with multiple fallback methods
- **Word cleaning**: Removes non-alphabetic characters, handles multi-word responses
- **Fallback system**: Uses random words from `dictionary.txt` when extraction fails
- **Context management**: Only previous round words shown to AIs (not full history)
- **Default model**: `anthropic/claude-sonnet-4`
- **Error handling**: Graceful handling of API key validation, interrupts, and network errors