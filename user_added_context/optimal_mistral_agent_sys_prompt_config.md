<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Optimal Mistral Agent System Prompt Configuration for API Use on LePlatform

## Configuration Parameters Table

![Optimal Mistral Agent Configuration Parameters for API Use via LePlatform](https://ppl-ai-code-interpreter-files.s3.amazonaws.com/web/direct-files/6ce35e846e398a15fce960b701e8525e/b19e1518-6eda-411b-b191-a61ea0a671b6/33198c72.png)

Optimal Mistral Agent Configuration Parameters for API Use via LePlatform

## **Recommended Configuration Just Below Threshold**

Based on the research from official Mistral documentation, respected forums, and power user experiences, here's the optimal configuration for production API agents:[^1][^2][^3][^4][^5][^6][^7][^8][^9][^10][^11][^12]

### **Core System Prompt Specifications**

**Optimal System Prompt Size**: **6,000-7,500 tokens**

- This represents approximately 4,500-5,600 words[^13][^14]
- Stays comfortably below the 8,000 token upper threshold while allowing comprehensive instructions
- Production agents from major companies use thousands of words for precise control[^11]

**Context Window Allocation**:

- **Input**: 25% (8,000 tokens for system prompt + user input)
- **Few-shot examples**: 15% (4,800 tokens)
- **Output buffer**: 60% (19,200 tokens)
- Total: 32,000 tokens for standard models


### **Few-Shot Example Configuration**

**Optimal Number**: **4-5 examples**[^15][^16][^17][^18]

- Performance improvements saturate around 6 examples
- 4-5 examples provide 90% of the benefit with 50% less latency
- Each example should be 200-400 tokens (150-300 words)


### **System Prompt Optimal Characteristics**

**Structure Components** (in priority order):[^7][^19]

1. **Role and Identity** (10-15% of prompt)
2. **Primary Purpose** (15-20% of prompt)
3. **Specific Constraints** (20-25% of prompt)
4. **Output Formatting** (10-15% of prompt)
5. **Edge Case Handling** (15-20% of prompt)
6. **Security Instructions** (10-15% of prompt)
7. **Example References** (5-10% of prompt)

### **Best Practices Including Security**

#### **Prompt Injection Defense**[^20][^21][^22][^23][^24][^25]

1. **Input Pre-processing**:
    - Implement paraphrasing or retokenization for external inputs
    - Use content classification to detect malicious instructions
    - Apply markdown sanitization
2. **Structural Defense**:
    - Separate system instructions from user content using control tokens[^1][^26][^27]
    - Use explicit instruction boundaries: `[INST]` and `[/INST]`
    - Never allow system prompt modification via user input
3. **Output Validation**:
    - Implement human-in-the-loop for sensitive operations
    - Use confidence thresholds (Top-P: 0.5) to filter uncertain outputs[^28]
    - Apply rate limiting per organization/workspace[^29][^10]

#### **Technical Reminders**

**Token Management**:[^30][^13][^31][^14]

- Monitor token usage through API metrics
- Input + output tokens cannot exceed model limits
- Use smaller models for simple tasks to optimize costs

**Model Selection for Agents**:[^32][^33][^13]

- **Mistral Small**: Fast responses, 128k context
- **Mistral Large 2**: Complex reasoning, 128k context
- **Codestral**: Technical tasks, 256k context
- **Magistral**: Step-by-step reasoning, 40k context

**Temperature Configuration**:[^34][^11][^28]

- **0.1-0.3**: Factual, deterministic tasks
- **0.3-0.5**: Balanced technical responses
- Avoid > 0.5 for production API use


#### **Implementation Checklist**

1. ✅ Keep system prompt between 6,000-7,500 tokens
2. ✅ Include 4-5 diverse, well-structured examples
3. ✅ Implement 3-layer security (input filtering, isolation, validation)
4. ✅ Use single-purpose agent design
5. ✅ Set temperature to 0.2-0.4 for consistency
6. ✅ Reserve 20% context buffer for unexpected inputs
7. ✅ Test with adversarial prompts before deployment
8. ✅ Monitor token usage and adjust tiers as needed[^10][^29]

### **Platform-Specific Considerations**

For LePlatform agents specifically:[^4][^6][^35][^36][^9]

- Agents are created at the workspace level with organizational rate limits
- Free tier is limited; production requires Tier 2+ (\$20+ billing)[^10]
- System prompts persist invisibly throughout conversations
- Use the Agent configuration UI for testing before API deployment
- Leverage the built-in Memories feature for persistent context when needed[^13]

This configuration balances performance, reliability, and security while staying within optimal token limits for efficient API operations on Mistral's LePlatform.