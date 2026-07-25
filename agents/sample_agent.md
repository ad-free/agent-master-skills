---
name: Sample Agent
description: A sample agent persona used for CI smoke tests
mode: subagent
version: 0.1.0
owner: noname.spyware@gmail.com
allowedTools: [none]
samplePrompts:
  - "You are Sample Agent. Show me an example of how you'd respond to 'write a unit test for function X'."
---

# Sample Agent

This is a small example agent used to validate the `tools/validate_agents.py` script in CI.

Use it as a template for adding new agents.
