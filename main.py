import argparse
import os
import random
import re
import time
from dataclasses import dataclass, field
from typing import List, Optional
from openai import OpenAI

# Game constants
FINAL_WORD_PATTERN = r"FINAL WORD:\s*([A-Za-z]+)"


def _extract_word_from_response(content: str) -> str:
    """Extract and clean the final word from AI response content."""
    lines = content.strip().split("\n")
    last_line = lines[-1] if lines else ""

    # Try regex pattern first
    match = re.search(FINAL_WORD_PATTERN, content, re.IGNORECASE)
    if match:
        word = match.group(1).upper()
    elif "FINAL WORD:" in last_line.upper():
        word = last_line.split(":")[-1].strip().upper()
    else:
        word = last_line.strip().upper()

    return _clean_word(word)


def _get_random_fallback_word() -> str:
    """Get a random word from dictionary.txt as fallback."""
    with open("dictionary.txt", "r") as f:
        words = [line.strip().upper() for line in f if line.strip()]
    return random.choice(words)


def _clean_word(word: str) -> str:
    """Clean and validate a word, returning a fallback if invalid."""
    # Remove non-alphabetic characters
    cleaned = "".join(c for c in word if c.isalpha())

    # Take only first word if multiple
    if " " in cleaned:
        cleaned = cleaned.split()[0]

    # Return fallback if no valid word
    if not cleaned:
        return _get_random_fallback_word()

    return cleaned


def _validate_api_key(api_key: Optional[str]) -> None:
    """Validate that API key is provided."""
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable not set")


@dataclass
class GameState:
    """Tracks the current state of the Mind Meld game."""

    round_number: int = 1
    player1_words: List[str] = field(default_factory=list)
    player2_words: List[str] = field(default_factory=list)
    convergence_achieved: bool = False


class MindMeldAI:
    """AI player for the Mind Meld game."""

    def __init__(
        self,
        name: str,
        model: str,
        client: OpenAI,
        max_tokens: int = 2048,
        temperature: float = 1.0,
    ) -> None:
        """Initialize AI player with name, model, OpenAI client, and generation parameters."""
        self.name = name
        self.model = model
        self.client = client
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.word_history: List[str] = []

    def generate_word(
        self, game_state: GameState, use_predefined_word: bool = False
    ) -> str:
        """Generate a word based on the current game state."""
        # For first round without predefined words, use dictionary
        if game_state.round_number == 1 and not use_predefined_word:
            word = _get_random_fallback_word()
            self.word_history.append(word)
            return word

        context = self._build_context(game_state)
        self._display_thinking_header()

        response_content = self._get_ai_response(context)
        word = _extract_word_from_response(response_content)

        self.word_history.append(word)
        return word

    def _build_context(self, game_state: GameState) -> str:
        """Build the context prompt for the AI based on game state."""
        context_parts: List[str] = []

        if game_state.round_number == 1:
            context_parts.append(
                "This is the first round. Pick a completely random word."
            )
        else:
            context_parts.append(f"This is round {game_state.round_number}.")

            if game_state.player1_words and game_state.player2_words:
                prev_round_idx = len(game_state.player1_words) - 1
                p1_word = game_state.player1_words[prev_round_idx]
                p2_word = game_state.player2_words[prev_round_idx]
                context_parts.append(
                    f"Previous round: Player 1 said '{p1_word}', Player 2 said '{p2_word}'"
                )

            context_parts.extend(
                [
                    "Try to think of a word that might lead to convergence with your opponent's thinking.",
                    "Remember: The goal is to eventually say the same word as your opponent.",
                    "Think about word associations, common concepts, or themes that might emerge.",
                    "Remember that repeating words that have already been said by either player is not allowed.",
                ]
            )

        context_parts.extend(
            [
                "Think through your reasoning step by step, then put your final word choice on the very last line.",
                "Format: Show your thinking process, then end with 'FINAL WORD: [your_word]'",
            ]
        )

        return "\n".join(context_parts)

    def _display_thinking_header(self) -> None:
        """Display the thinking process header."""
        print(f"\n💭 {self.name}'s thinking process:")
        print("-" * 40)

    def _get_ai_response(self, context: str) -> str:
        """Get streaming AI response and display it."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are playing Mind Meld, an improv game where two players try to converge on the same word. Think through your reasoning process, then put your final word choice on the last line in the format 'FINAL WORD: [word]'. Show your thinking process before the final word.",
                },
                {"role": "user", "content": context},
            ],
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            stream=True,
        )

        content = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                token = chunk.choices[0].delta.content
                content += token
                print(token, end="", flush=True)

        print("\n" + "-" * 40)
        return content


class MindMeldGame:
    """Main game controller for Mind Meld."""

    def __init__(
        self,
        openrouter_api_key: str,
        model: str = "anthropic/claude-sonnet-4",
        player1_word: Optional[str] = None,
        player2_word: Optional[str] = None,
        max_tokens: int = 2048,
        temperature: float = 1.0,
        max_rounds: int = 10,
        round_pause_seconds: float = 2.0,
    ) -> None:
        # Initialize OpenAI client with OpenRouter
        self.client = OpenAI(
            api_key=openrouter_api_key, base_url="https://openrouter.ai/api/v1"
        )

        # Create two AI players with specified model and parameters
        self.player1 = MindMeldAI(
            "AI Player 1", model, self.client, max_tokens, temperature
        )
        self.player2 = MindMeldAI(
            "AI Player 2", model, self.client, max_tokens, temperature
        )

        # Store predefined first words if provided
        self.player1_first_word = player1_word.upper() if player1_word else None
        self.player2_first_word = player2_word.upper() if player2_word else None

        # Store game parameters
        self.max_rounds = max_rounds
        self.round_pause_seconds = round_pause_seconds

        self.game_state = GameState()

    def play_round(self) -> bool:
        """Play one round of Mind Meld. Returns True if convergence achieved."""

        print(f"\n=== ROUND {self.game_state.round_number} ===")

        # Player 1 generates word (use predefined word for first round if provided)
        if self.game_state.round_number == 1 and self.player1_first_word:
            word1 = self.player1_first_word
            print(f"\n🎯 {self.player1.name} uses predefined word: '{word1}'")
            self.player1.word_history.append(word1)
        else:
            use_predefined = self.game_state.round_number == 1 and bool(
                self.player1_first_word
            )
            word1 = self.player1.generate_word(self.game_state, use_predefined)
            print(f"\n🎯 {self.player1.name} chooses: '{word1}'")

        # Player 2 generates word (use predefined word for first round if provided)
        if self.game_state.round_number == 1 and self.player2_first_word:
            word2 = self.player2_first_word
            print(f"\n🎯 {self.player2.name} uses predefined word: '{word2}'")
            self.player2.word_history.append(word2)
        else:
            use_predefined = self.game_state.round_number == 1 and bool(
                self.player2_first_word
            )
            word2 = self.player2.generate_word(self.game_state, use_predefined)
            print(f"\n🎯 {self.player2.name} chooses: '{word2}'")

        # Update game state
        self.game_state.player1_words.append(word1)
        self.game_state.player2_words.append(word2)

        # Check for convergence
        if word1 == word2:
            print(f"\n🎉 MIND MELD ACHIEVED! Both players said '{word1}'!")
            self.game_state.convergence_achieved = True
            return True
        else:
            print(f"\n❌ No match this round. ({word1} ≠ {word2})")
            return False

    def play_game(self) -> None:
        """Play a complete game of Mind Meld."""

        print("🧠 MIND MELD GAME STARTING 🧠")
        print("=" * 50)
        print(
            f"{self.player1.name} ({self.player1.model}) vs {self.player2.name} ({self.player2.model})"
        )
        print("Goal: Both AIs must say the same word to achieve Mind Meld!")
        print("=" * 50)

        while (
            not self.game_state.convergence_achieved
            and self.game_state.round_number <= self.max_rounds
        ):
            converged = self.play_round()

            if converged:
                print(f"\n🏆 Game completed in {self.game_state.round_number} rounds!")
                break

            self.game_state.round_number += 1
            time.sleep(self.round_pause_seconds)

        self.print_game_summary()

    def print_game_summary(self) -> None:
        """Print a summary of the completed game."""

        print("\n" + "=" * 50)
        print("GAME SUMMARY")
        print("=" * 50)

        for i, (word1, word2) in enumerate(
            zip(self.game_state.player1_words, self.game_state.player2_words)
        ):
            status = "✅ MATCH!" if word1 == word2 else "❌ No match"
            print(f"Round {i + 1}: {word1} | {word2} - {status}")

        if self.game_state.convergence_achieved:
            print(f"\n🎉 Mind Meld achieved in {self.game_state.round_number} rounds!")
        else:
            print(
                f"\n💭 Game ended after {self.max_rounds} rounds without convergence."
            )

        print("=" * 50)


def main() -> None:
    """Main entry point for the Mind Meld game."""

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="AI Mind Meld Game")
    parser.add_argument(
        "--player-1-word", type=str, help="Predefined first word for Player 1"
    )
    parser.add_argument(
        "--player-2-word", type=str, help="Predefined first word for Player 2"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="anthropic/claude-sonnet-4",
        help="Model to use for both AI players (default: anthropic/claude-sonnet-4)",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=2048,
        help="Maximum tokens for AI responses (default: 2048)",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=1.0,
        help="Temperature for AI responses (default: 1.0)",
    )
    parser.add_argument(
        "--max-rounds",
        type=int,
        default=10,
        help="Maximum number of rounds per game (default: 10)",
    )
    parser.add_argument(
        "--round-pause-seconds",
        type=float,
        default=2.0,
        help="Pause between rounds in seconds (default: 2.0)",
    )
    args = parser.parse_args()

    # Get OpenRouter API key
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

    try:
        _validate_api_key(openrouter_api_key)
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("Please set your OpenRouter API key:")
        print("export OPENROUTER_API_KEY='your-api-key-here'")
        return

    try:
        # Create and run the game with command line arguments
        assert openrouter_api_key is not None  # Already validated above
        game = MindMeldGame(
            openrouter_api_key,
            args.model,
            args.player_1_word,
            args.player_2_word,
            args.max_tokens,
            args.temperature,
            args.max_rounds,
            args.round_pause_seconds,
        )
        game.play_game()

    except KeyboardInterrupt:
        print("\n\nGame interrupted by user. Thanks for playing!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please check your API key and internet connection.")


if __name__ == "__main__":
    main()
