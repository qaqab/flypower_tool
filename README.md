# Flypower Tool

Dify plugin containing Flypower company tools.

It provides image generation through an OpenAI-compatible endpoint and the
`set_next_step` tool for passing the next objective and reasoning effort to a
subsequent model call.

## Configuration

- Use an HTTPS API base URL, such as `https://litellm.flyfus.com` or `https://litellm.flyfus.com/v1`.
- Image generation verifies credentials with `GET /v1/models`; the response must include at least one supported image model.
- `set_next_step` does not require image credentials.
