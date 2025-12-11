# Agentic Coding Tips & Tricks


## Stop! Think before you leap!
- Don’t rush into prompting/asking
- Often it’s better to spend a few minutes to think about what you really want (outcome). And what you don’t want.
- This can save you time and frustration down the line

## A picture says more than 1000 words
- Screenshots provide 10x more context than text. Drag directly into terminal
- BUT! They can quickly overload the context if you use too many/too large

## Branch useful conversations
- You can branch off (resume) useful conversations
- Possibility to run multiple parallel conversation, using a shared root conversation

## Single task per conversation 
- Don’t do too much at the same time!
- Break down your problem and focus on one thing at  a time 
- Consider using multiple parallel conversations, each focusing on single aspect
- If your task is complex, create a plan first

## Multitasking
- Use multiple terminals, with multiple parallel conversations in same branch, but working on different problems (requires discipline and focus…)
- Use git worktrees (if needed), to more effectively work in multiple branches in parallel

## Priming
- Instead of putting too much information into common memory files (CLAUDE.md / AGENTS.md), start each new conversation with priming
- Work type specific priming - i.e. priming specific to a certain “role” or type or work (i.e. testing, visual validation, architecture…)
- Tasks specific priming - i.e. what is the nature of the current feature/fix being implemented

## Test-first approach
- Adopt a TDD-based approach
- Or simply instruct the agent to write test before implementing a feature or fix

## Validation loops
- Visual validation loops, using for instance PlayWright
- Code/security review
- Unit/integration testing 
- Architectural fitness functions

## Beware of /compact (where available)
- Whenever you compact the conversation, there is a risk you loose important context/instructions
- Keep regular check on your context window
- If over 50%, it may be better to ask the agent to summarise the status of the implementation in a document or existing plan/spec

## Tools and MCPs
- Existing CLI commands etc are often preferred over MCPs
- Select your MCPs with care - they can consume a lot of context (in just metadata)
- Consider loading MCPs only when you need them