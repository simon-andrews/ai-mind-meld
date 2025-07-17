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

🎯 AI Player 1 chooses: 'ICICLE'

🎯 AI Player 2 chooses: 'YOGURT'

❌ No match this round. (ICICLE ≠ YOGURT)

=== ROUND 2 ===

💭 AI Player 1's thinking process:
----------------------------------------
Let me think through this step by step.

In round 1, I said "ICICLE" and my opponent said "YOGURT". These seem quite different at first glance, but I need to find potential connections or middle ground.

Possible connections between ICICLE and YOGURT:
- Both are cold/frozen items (icicles are frozen water, yogurt is often refrigerated)
- Both have a somewhat similar shape when you think about it - elongated/cylindrical
- Both are consumable in some sense (people sometimes lick/suck on icicles)
- Both are white/pale in color typically

Common themes that might emerge:
- COLD/FROZEN - this seems like the strongest connection
- FOOD/EDIBLE items
- WHITE/PALE colored things
- SMOOTH textures

Given that we're trying to converge, I should pick something that bridges these concepts. My opponent might be thinking along similar lines about the "cold" connection.

Some possibilities:
- ICE CREAM (combines cold like icicle, creamy like yogurt, food item)
- MILK (white, cold when refrigerated, base for yogurt)
- POPSICLE (frozen like icicle, sweet/edible like yogurt)
- CREAM (white, cold, related to yogurt)

I think ICE CREAM is the strongest choice because:
1. It's cold/frozen (connecting to icicle)
2. It's a dairy-based food product (connecting to yogurt)
3. It's something both players would likely think of when bridging "cold" and "food"
4. It's a very common, obvious connection point

FINAL WORD: ICE CREAM
----------------------------------------

🎯 AI Player 1 chooses: 'ICE'

💭 AI Player 2's thinking process:
----------------------------------------
Let me think through this step by step.

In round 1, I said "ICICLE" and my opponent said "YOGURT". These seem quite different at first glance, but I need to find connections or think about what might bridge these concepts.

Possible connections between ICICLE and YOGURT:
- Both are cold (icicles are frozen, yogurt is often refrigerated/cold)
- Both have a white/pale appearance
- Both can be smooth or have interesting textures
- Both are consumable in some sense (people sometimes suck on icicles)

Common themes that might emerge:
- COLD/FROZEN - This seems like the strongest connection
- WHITE/PALE colors
- SMOOTH textures
- Things found in refrigerators/freezers

Since we're trying to converge, I should think about what word my opponent might choose based on the same ICICLE-YOGURT pairing. They might also notice the "cold" connection.

Words that bridge cold concepts:
- FREEZE/FROZEN
- ICE
- CHILL
- SNOW
- FROST

But I also want to consider food-related cold things since yogurt is food:
- POPSICLE (frozen treat)
- ICE CREAM
- SORBET
- GELATO

Given that my opponent chose a food item (yogurt) and I chose something ice-related (icicle), they might be thinking of frozen desserts or cold foods. ICE CREAM seems like a natural bridge - it's cold like an icicle, and it's a creamy dairy product like yogurt.

FINAL WORD: ICE CREAM
----------------------------------------

🎯 AI Player 2 chooses: 'ICE'

🎉 MIND MELD ACHIEVED! Both players said 'ICE'!

🏆 Game completed in 2 rounds!

==================================================
GAME SUMMARY
==================================================
Round 1: ICICLE | YOGURT - ❌ No match
Round 2: ICE | ICE - ✅ MATCH!

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
- `--model`: Model to use for both AI players (default: anthropic/claude-sonnet-4)
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