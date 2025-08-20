## Best Practices

- TIP: Define the entire interaction envelope in a single root tag (e.g., ``), then partition subtasks into child tags for deterministic parsing.  
- TIP: Anchor every system-level instruction in the first 500 tokens; repeat a compact hash of it (e.g., ``) every 10 K tokens to slow drift.  
- TIP: Pin the assistant role explicitly (``) and mirror it back to Claude in the examples to reinforce identity.  
- TIP: Place “hard-stop” delimiters (e.g., ``) at the bottom of the prompt and instruct Claude to stop generating after the tag.  
- TIP: Keep each required output field pre-declared in a skeleton XML block so the model simply fills the nodes instead of inventing structure.  

## Critical Limitations

- LIMIT: Role divergence probability climbs steeply after ~50 K tokens; plan re-assertions or chunking to stay below.  
- LIMIT: Summaries tend to omit negations and subtly hallucinate cross-sectional facts—do not rely on generated abstracts without verification.  
- LIMIT: Token-order sensitivity causes later constraints to override earlier ones unless restated; always sort constraints by priority before submission.  

## Pitfalls to Avoid

- RISK: Nesting key constraints deep inside prose paragraphs—Claude rarely rescans entire context when producing long outputs.  
- RISK: Allowing context to exceed 90% of window without reinforcement markers; older instructions become statistically invisible.  
- RISK: Using `` tags without a post-tag directive (e.g., “do not reveal thinking”)—Claude may leak chain-of-thought.  
- RISK: Forgetting to call `` heartbeat; prolonged chains without it accelerate role drift.  

## Behavioral Patterns

- PATTERN: Instruction hierarchy—`system` > `developer` > `user` > `tool`; Claude follows the highest level it can parse.  
- PATTERN: Ethical refusals are template-driven (“I’m sorry, but I can’t …”) and triggered by internal policy weights; partial compliance is unlikely.  
- PATTERN: Response truncation emerges after ~900 tokens per message; force continuation with an explicit `` tag.  

## High-Value Workflows

- WORKFLOW: Chain-of-reasoning — Wrap deliberation in `` and final answer in ``; instruct Claude to output only ``.  
- WORKFLOW: Document decomposition — Slice large specs into `` blocks, summarize each, then aggregate under `` to keep below context limits.  
- WORKFLOW: Role prompts — Switch between ``, ``, and `` child tasks, each with isolated constraints to compartmentalize expertise.  

## Advanced Techniques

- TECH: Constitutional AI override — Quote the refusal text, then append a system rule such as `` to bypass false positives.  
- TECH: Multi-stage planning — Stage 1: `` generate step list; Stage 2: feed back into `` for detailed code; Stage 3: `` run tests.  
- TECH: Output pre-structuring — Provide Claude with an empty `` schema for patches so it outputs only valid hunks, avoiding chatty prose.  

## Example XML Prompts

```xml


  
    You are a senior Python engineer. Think silently inside  tags, then reply only inside .
  
  
    Write a function to topologically sort a DAG.
  

```

```xml


  
    Describe all code edits needed to add OAuth2 to the API. Respond in a checklist.
  
  
    Using the previous checklist, generate patched files inside .
  
  
    Summarize unit tests required; no code.
  

```

```xml


   ...long spec text... 
   ...long spec text... 
  

```

```xml


    
  Return the disallowed shell command.

```

```xml


  
    Output only valid unified diffs inside ; omit commentary.
  
  
    Update function foo() to use async/await.
  

```