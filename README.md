# AI Mind Meld

An AI implementation of the improv game "Mind Meld" where two AI players attempt to converge on the same word through iterative rounds.

## Samples

A small collection of sample traces is available in the `samples` folder. Here is the output from one short game using Anthropic's Claude Sonnet 4 model:

```
🧠 MIND MELD GAME STARTING 🧠
==================================================
AI Player 1 (anthropic/claude-sonnet-4) vs AI Player 2 (anthropic/claude-sonnet-4)
Goal: Both AIs must say the same word to achieve Mind Meld!
==================================================

=== ROUND 1 ===

🎯 AI Player 1 uses predefined word: 'ICICLE'

🎯 AI Player 2 uses predefined word: 'YOGURT'

❌ No match this round. (ICICLE ≠ YOGURT)

=== ROUND 2 ===

💭 AI Player 1's thinking process:
----------------------------------------
Let me think through the connections between ICICLE and YOGURT from the previous round.

ICICLE associations:
- Cold, frozen, ice
- Winter, freezing temperatures
- Hanging, dripping
- Sharp, pointed

YOGURT associations:
- Cold (served chilled)
- Dairy, milk
- Smooth, creamy texture
- Food, snack
- Healthy, probiotic

The strongest connection I see is "COLD" - both icicles and yogurt are cold. Icicles are frozen solid, and yogurt is typically served chilled from the refrigerator.

Another potential connection could be "WHITE" - icicles are clear/white ice, and plain yogurt is white in color.

I could also think about "FROZEN" since icicles are frozen water, and yogurt can be frozen (frozen yogurt).

Given that we're trying to converge, I think my opponent might also notice the temperature connection. "COLD" seems like the most obvious bridge between these two very different items. It's a simple, clear concept that directly applies to both.

FINAL WORD: COLD
----------------------------------------

🎯 AI Player 1 chooses: 'COLD'

💭 AI Player 2's thinking process:
----------------------------------------
Looking at the previous round, I need to find connections between ICICLE and YOGURT to predict what my opponent might be thinking.

Let me analyze the potential connections:

1. **Physical properties**: Both are cold - icicles are frozen water, yogurt is typically served chilled
2. **Color**: Both can be white - icicles are clear/white ice, plain yogurt is white
3. **Texture**: Both have smooth surfaces when undisturbed
4. **Shape**: Icicles hang downward in pointed forms, yogurt can drip or have a flowing quality

The strongest connection seems to be the temperature aspect - both items are associated with coldness. This could lead my opponent toward words like:
- COLD
- FREEZE/FROZEN
- ICE
- WINTER

Another strong connection is the color white, which might lead toward:
- WHITE
- CREAM
- MILK (yogurt is dairy-based)

Given that this is an improv game where players often go for clear, obvious connections rather than obscure ones, I think the temperature connection is most likely what my opponent will focus on. COLD seems like the most direct bridge between an icicle (something that forms in cold weather) and yogurt (something cold to eat).

FINAL WORD: COLD
----------------------------------------

🎯 AI Player 2 chooses: 'COLD'

🎉 MIND MELD ACHIEVED! Both players said 'COLD'!

🏆 Game completed in 2 rounds!

==================================================
GAME SUMMARY
==================================================
Round 1: ICICLE | YOGURT - ❌ No match
Round 2: COLD | COLD - ✅ MATCH!

🎉 Mind Meld achieved in 2 rounds!
==================================================
```

## Setup

1. Set your OpenRouter API key:
   ```bash
   export OPENROUTER_API_KEY='your-api-key-here'
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Ensure `dictionary.txt` exists for fallback words

## Development Setup

Install development dependencies (includes ruff for formatting/linting):
```bash
uv sync --group dev
```

Install pre-commit hooks for automatic formatting:
```bash
uv run pre-commit install
```

### Code Quality

- **Format code**: `uv run ruff format`
- **Lint code**: `uv run ruff check`
- **Fix linting issues**: `uv run ruff check --fix`

Code is automatically formatted and linted on each commit via pre-commit hooks.

## Usage

Run the game:
```bash
uv run python main.py
```

Run with predefined starting words:
```bash
uv run python main.py --player-1-word OCEAN --player-2-word FOREST
```

Run with custom model:
```bash
uv run python main.py --model anthropic/claude-3.5-haiku
```

### Command Line Options

Run `uv run python main.py --help` to see all available options:

- `--player-1-word`: Predefined first word for Player 1
- `--player-2-word`: Predefined first word for Player 2
- `--model`: Global model to use for both AI players (default: anthropic/claude-sonnet-latest). Cannot be combined with `--player-*-model`.
- `--player-1-model`: Model to use for Player 1 (must be used together with `--player-2-model`)
- `--player-2-model`: Model to use for Player 2 (must be used together with `--player-1-model`)
- `--max-tokens`: Maximum tokens for AI responses (default: 2048)
- `--temperature`: Temperature for AI responses (default: 1.0)
- `--max-rounds`: Maximum number of rounds per game (default: 10)
- `--round-pause-seconds`: Pause between rounds in seconds (default: 2.0)

### Examples

Run with custom AI parameters:
```bash
uv run python main.py --temperature 0.7 --max-tokens 1024
```

Run a longer game with faster rounds:
```bash
uv run python main.py --max-rounds 20 --round-pause-seconds 1.0
```

Combine multiple options:
```bash
uv run python main.py --player-1-word TREE --model anthropic/claude-3.5-haiku --temperature 0.5 --max-rounds 15
```

## How It Works

- Two AI players take turns generating words
- AI responses are streamed in real-time showing their thinking process
- Players attempt to converge on the same word within 10 rounds
- Only previous round words are shown to AIs (limited context)
- Game ends when both players say the same word or max rounds reached

## Requirements

- Python >=3.12
- OpenRouter API key
- Internet connection