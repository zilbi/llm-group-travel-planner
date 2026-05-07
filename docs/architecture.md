# Architecture

This project is structured as a Telegram-based group travel planning system.

## Main Components

- `commands/` — handles bot commands and user interaction flow
- `ml/` — contains LLM-based itinerary generation and AI-related components
- `db/` — stores user, trip, and preference-related data
- `main.py` — application entry point
- `Dockerfile` — container setup for deployment
  
## Workflow

1. Users provide travel preferences and constraints through chat
2. The system parses chat input and extracts trip parameters
3. The extracted parameters are passed to the itinerary generation module
4. The system generates shared travel options for the group
5. The bot returns itinerary suggestions and relevant booking or flight links
