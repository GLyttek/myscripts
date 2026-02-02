# Agent Patterns

Early experiments with LLM agent patterns using a coffee shop simulation.

## Files

- **main.py** - Main orchestrator
- **barista2.py** - Barista agent with tool use
- **coffee.py** / **coffee2.py** - Coffee-related utilities

## Pattern: Tool-Using Agent

The barista agent demonstrates:
1. **Intent Recognition** - Understanding customer orders
2. **Tool Selection** - Choosing appropriate actions
3. **State Management** - Tracking order progress
4. **Response Generation** - Natural conversation

## Architecture

```
Customer Input → Intent Parser → Tool Router → Action Executor → Response Generator
```

## Learning Value

Simple but complete example of:
- ReAct pattern (Reason + Act)
- Tool calling
- Conversation state
- Domain-specific agents

## Original Source

Learning experiments from August 2024.
