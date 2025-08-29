# Soteria SDK Documentation

This document provides an in-depth guide to using the Soteria SDK for Python, focusing on its capabilities for input processing, sanitization, and validation of prompts before they are sent to Large Language Models (LLMs).

## 1. Introduction to Soteria SDK

The Soteria SDK is designed to act as a robust firewall and pre-processor for your LLM inputs. It allows developers to define and apply a series of "guards" (validators) to incoming prompts, ensuring they meet specific criteria, are free from sensitive information, or do not attempt to circumvent LLM safety measures.

The SDK operates on a client-server architecture:
- **Client-side (SDK)**: Your application integrates with the Soteria SDK, which provides convenient decorators and functions to apply guards to your prompts. The SDK sends prompts to a Soteria AI server for processing.

```bash
uv add soteria-sdk
```

## 2. Configuration

Before using the Soteria SDK, you need to configure it with your API key and the base URL of the Soteria AI service.

### Using `soteria_sdk.configure()`

The primary way to configure the SDK is by calling the `soteria_sdk.configure()` function:

```python

import soteria_sdk

# Configure with your API key and optionally a custom API base URL
soteria_sdk.configure(api_key="YOUR_API_KEY_HERE", api_base="https://api.soteriainfra.com")
```

- `api_key` (required): Your unique API key obtained from the Soteria web application. This authenticates your requests to the Soteria AI server.
- `api_base` (required): The base URL of the Soteria AI service.

### Using Environment Variables

Alternatively, you can configure the API key using the `SOTERIA_API_KEY` environment variable. This is particularly useful for deployment environments where you don't want to hardcode credentials in your code.

```bash
export SOTERIA_API_KEY="YOUR_API_KEY_HERE"
```

If both `soteria_sdk.configure()` and the environment variable are set, the value provided to `configure()` will take precedence.

## 3. Basic Setup and Usage

The Soteria SDK provides a convenient `@guard_prompt` decorator to easily integrate prompt validation into your Python functions.

### The `@guard_prompt` Decorator

The Soteria SDK provides ready-to-use decorators for common validation scenarios. These decorators are pre-configured with specific guard names and expect your function to have a parameter named `@prompt`.

When a function decorated with a pre-configured guard is called, the SDK automatically:

- Intercepts the prompt argument
- Sends it to the Soteria server for processing by the specified guard
- Either allows the (potentially modified) prompt to proceed or raises a `SoteriaValidationError`

### Example Usage

Here's a basic example of how to use a pre-configured guard:

```python

import soteria_sdk

# 1. Configure Soteria (replace with your actual API key)
soteria_sdk.configure(api_key="YOUR_API_KEY_HERE", api_base="https://api.soteriainfra.com")


# 2. Define a function that sends a prompt to an LLM
#    Apply the guard_pii decorator to the 'user_prompt' argument
@soteria_sdk.guard_pii
def send_to_llm(prompt: str):
    """
    Simulates sending a prompt to an LLM.
    The 'guard_pii' guard will redact PII from 'user_prompt' before this function runs.
    """
    print(f"Sending to LLM: {prompt}")
    # In a real application, you would call your LLM API here
    return f"LLM response to: {prompt}"


# Example calls
try:
    # This prompt contains PII (email address)
    response1 = send_to_llm(prompt="My email is john.doe@example.com. What's the weather like?")
    print(f"Response 1: {response1}")

    # This prompt is clean
    response2 = send_to_llm(prompt="Tell me a joke.")
    print(f"Response 2: {response2}")

except soteria_sdk.SoteriaValidationError as e:
    print(f"Validation Error: {e}")
    print(f"Validation Summary: {e.validation_summaries}")
except ConnectionError as e:
    print(f"Connection Error: {e}")
```

## 4. Pre-configured Features (Firewall)

The Soteria SDK comes with several pre-configured decorators for common use cases. These decorators correspond to specific guard pipelines that are expected to be available on the Soteria AI server.

### Redaction Firewall

These firewalls are designed to identify and remove or mask sensitive information from prompts. If a redaction guard fails, it typically modifies the `processed_prompt` and allows the execution to continue.

- `guard_pii`: Redacts Personally Identifiable Information (PII) from the prompt.
- `guard_secrets`: Masks sensitive secrets (e.g., API keys, credentials) from the prompt.

### Blocking Firewall

These firewalls are designed to prevent prompts from proceeding if they violate certain safety or content policies. If a blocking guard fails, it typically raises a `SoteriaValidationError`.

- `guard_profanity`: Blocks prompts containing profane language.
- `guard_jailbreak`: Detects and blocks prompts attempting to circumvent LLM safety mechanisms or extract sensitive information.
- `guard_unusual_prompt`: Identifies and blocks prompts that are statistically unusual or out of distribution compared to expected inputs.
- `guard_database_injection`: Detects and blocks prompts attempting to add malicious data into the database by unauthorized users.

### Combined Pipeline Firewall

These firewalls represent a combination of multiple validators, forming a comprehensive security or content policy pipeline.

- `guard_standard_security`: A pre-defined pipeline that combines common security-focused guards (e.g., PII, secrets, jailbreak, profanity).

### Formatting Firewall

These firewalls enforce specific formatting or structural constraints on the prompt.

- `guard_two_words`: Ensures the prompt consists of exactly two words.
- `guard_short_length`: Ensures the prompt's length is below a certain threshold.

## 5. Error Handling

Effective error handling is crucial when integrating Soteria into your application. The SDK provides a specific exception for validation failures.

### Catching `SoteriaValidationError`

When a prompt fails validation due to a `BLOCK` or `EXCEPTION` `on_fail` action configured for a validator on the server, the `@guard_prompt` decorator raises a `soteria.SoteriaValidationError`. You should wrap your guarded function calls in `try...except` blocks to gracefully handle these scenarios.

```python

import soteria_sdk

soteria_sdk.configure(api_key="YOUR_API_KEY_HERE", api_base="https://api.soteriainfra.com")


@soteria_sdk.guard_profanity
def send_message(prompt: str):
    print(f"Sending message: {prompt}")


try:
    send_message(prompt="Hello, world!")
    send_message(prompt="This is a bad word.")  # This will trigger the error
except soteria_sdk.SoteriaValidationError as e:
    print("\n--- Soteria Validation Error Caught ---")
    print(f"Error Message: {e}")
    print(f"Detailed Summaries: {e.validation_summaries}")
    print("The prompt was blocked or caused an exception on the server.")
except ConnectionError as e:
    print(f"Failed to connect to Soteria server: {e}")
```