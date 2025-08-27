# File: soteria_sdk/__init__.py

from .client import configure
from .exceptions import SoteriaValidationError
from .decorators import guard_prompt

# -- Redaction Guards --
guard_pii = guard_prompt(guard_name="pii-redactor", prompt_arg="prompt")
guard_secrets = guard_prompt(guard_name="secrets-masker", prompt_arg="prompt")


# -- Blocking Guards --
guard_profanity = guard_prompt(guard_name="profanity-blocker", prompt_arg="prompt")
guard_jailbreak = guard_prompt(guard_name="jailbreak-detector", prompt_arg="prompt")
guard_unusual_prompt = guard_prompt(guard_name="unusual-prompt-detector", prompt_arg="prompt")
guard_database_injection = guard_prompt(guard_name="database-injection-detector", prompt_arg="prompt")

# -- Combined Pipeline Guards --
guard_standard_security = guard_prompt(guard_name="standard-security-pipeline", prompt_arg="prompt")

# -- Formatting Guards --
guard_two_words = guard_prompt(guard_name="two-words-only", prompt_arg="prompt")
guard_short_length = guard_prompt(guard_name="length-checker-short", prompt_arg="prompt")


__all__ = [
    "configure",
    "guard_prompt",
    "SoteriaValidationError",
    # Pre-configured decorators (The "menu")
    "guard_pii",
    "guard_secrets",
    "guard_profanity",
    "guard_jailbreak",
    "guard_unusual_prompt",
    "guard_standard_security",
    "guard_two_words",
    "guard_short_length",
    "guard_database_injection"
]