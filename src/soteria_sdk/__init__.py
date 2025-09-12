# File: soteria_sdk/__init__.py

from soteria_sdk.client import configure
from soteria_sdk.exceptions import SoteriaValidationError
from soteria_sdk.decorators import guard_prompt

# -- Redaction Guards --
guard_pii_redactor = guard_prompt(guard_name="pii-redactor", prompt_arg="prompt")
guard_secrets_redactor = guard_prompt(guard_name="secrets-redactor", prompt_arg="prompt")


# -- Blocking Guards --
guard_jailbreak = guard_prompt(guard_name="jailbreak-detector", prompt_arg="prompt")
guard_prompt_injection = guard_prompt(guard_name="prompt-injection-detector", prompt_arg="prompt")


__all__ = [
    "configure",
    "guard_prompt",
    "SoteriaValidationError",
    # Pre-configured decorators (The "menu")
    "guard_pii_redactor",
    "guard_secrets_redactor",
    "guard_jailbreak",
    "guard_prompt_injection"
]