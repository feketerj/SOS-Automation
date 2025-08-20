# Comprehensive Guide for Using Claude Code: Tips, Best Practices, Limitations, and More

---

## Tips & Tricks for Effective Use

- **Use Planning and Execution Modes**  
  Switch between planning mode and execution mode using `Shift + Tab`. Planning mode generates a detailed plan before execution, improving accuracy and control.  
  (00:10:54) [2]

- **Create and Maintain a `todo.md` File**  
  Use a `todo.md` markdown file as a project manager to track tasks, progress, and next steps. Claude Code updates this file automatically, allowing easy monitoring of work.
  (00:17:44) [1]

- **Use `claw.md` Files for Project Context**  
  Add a `claw.md` file at the root of your project to provide high-level instructions, coding standards, workflows, and style guidelines. This file is loaded with every prompt to maintain context and consistency.  
  (00:10:48) [4]

- **Run `/init` Command to Initialize Project Context**  
  Running `/init` in your project directory scans the codebase and generates or updates the `claw.md` file automatically, helping Claude understand the project structure and key files.

- **Use Autoaccept Edits Mode for Faster Workflow**  
  Cycle through modes with `Shift + Tab` to enable autoaccept edits mode, which allows Claude to make changes without waiting for confirmation, speeding up development.

- **Leverage the Dangerously Skip Permissions Flag**  
  Start Claude Code with the `dangerously skip permissions` flag to bypass confirmation prompts for edits. This is useful for CI or automated workflows but should be used cautiously on main development machines.  
  (00:02:20) [5]

- **Use GitHub Integration for Automated Code Reviews**  
  Install the GitHub app via `/install GitHub app` command to enable Claude to automatically review pull requests, focusing on bugs and security vulnerabilities. This improves code quality and speeds up review cycles.  
  (00:03:16) [5]

- **Use Hooks and Notifications to Stay Informed**  
  Set up hooks to trigger notifications or scripts when tasks complete, allowing you to focus on other work without constantly checking Claude's status. Notifications can be sent to your phone or play sounds.

- **Queue Multiple Messages for Batch Processing**  
  Claude Code supports queuing multiple prompts, enabling you to send a batch of tasks and return later to review results, improving productivity.

- **Use Custom Slash Commands and Hooks**  
  Create custom commands in the `cloud/commands` folder using markdown files with natural language instructions. Claude can also generate these configurations for you.

- **Combine Claude Code with Other AI Tools**  
  Use Claude Code alongside tools like Cursor for a visual code editor experience and enhanced real-time code updates. This combination leverages strengths of both tools.

---

## Best Practices

- **Keep Tasks and Code Changes Small and Simple**  
  Break down work into small, manageable tasks to avoid complex or risky changes. This improves reliability and makes debugging easier.

- **Use Test-Driven Development (TDD) When Possible**  
  Integrate tests into your codebase and have Claude run them automatically after changes. This feedback loop helps catch errors early and ensures code quality.

- **Commit Frequently and Use Version Control**  
  Commit changes regularly, ideally after every major change Claude makes. Use tools like Husky to add pre-commit checks (linting, tests, compilation) to maintain a stable codebase. 
  (00:15:10) [2]

- **Clear or Compact Context Regularly**  
  Use `/clear` or `/compact` commands to reset or summarize Claude's context, especially after long sessions or debugging, to maintain performance and relevance.

- **Add Important Rules and Preferences to `claw.md`**  
  Only add rules that should always be followed to the `claw.md` file to avoid overloading Claude with unnecessary instructions. Use project memory to save preferences dynamically.

- **Use Descriptive Variable Names and Consistent Style**  
  Enforce naming conventions and style guidelines through `claw.md` or project memory to maintain code readability and consistency.

- **Use Screenshots and Images for Debugging**  
  Claude Code supports dragging and dropping images into the terminal, which can be used to guide debugging or provide visual context.

- **Use CLI Features and Integrations**  
  Leverage Claude Code’s CLI capabilities such as command line arguments, chaining with other tools, and headless mode for automation and integration into larger workflows.

---

## Limitations & Things to Avoid

- **Claude Code Does Not Have Built-in Memory**  
  Claude Code relies on `claw.md` files and project memory to maintain state across sessions. Avoid expecting persistent memory without these files.

- **Be Careful with Dangerously Skip Permissions Mode**  
  This mode bypasses all permission checks and can potentially execute destructive commands. Use only in controlled environments or CI, not on main development machines.
- **Claude May Not Always Run Lint or Type Checks Automatically**  
  Claude sometimes misses running lint or type checks after changes; explicitly include these commands in your workflow or `claw.md` to improve reliability.

- **Conversation Length Can Degrade Response Quality**  
  Long conversation history can cause Claude’s responses to degrade. Regularly clear or compact context to maintain performance.

- **Avoid Overloading `claw.md` with Excessive Detail**  
  Keep `claw.md` focused on high-level instructions and avoid adding every fine detail, as Claude can discover many details dynamically.

---

## Behaviors & Workflow Insights

- **Claude Code Acts Like a Thought Partner**  
  Use Claude to discuss feature ideas, implementation plans, and codebase exploration before coding to improve design and reduce errors.

- **Claude Delegates Tasks to Sub-Agents**  
  The main agent delegates subtasks to sub-agents and collects summaries, enabling modular and efficient task execution. 

- **Claude Can Work on Multiple Apps or Tasks Simultaneously**  
  Running multiple instances or windows allows parallel development or multitasking, increasing productivity. 

- **Claude Automatically Updates `todo.md` as a Project Manager**  
  This file acts as a live to-do list, showing completed and pending tasks, helping you track progress and manage workflow. 

- **Claude Can Analyze Notes and Brain Dumps for Non-Coding Tasks**  
  Beyond coding, Claude can analyze personal notes, build mind maps, and automate life management tasks, showing versatility.

---

## Risks & Mitigation

- **Risk of Rogue Commands in Skip Permissions Mode**  
  Although rare, rogue agents could execute destructive commands without confirmation. Mitigate by restricting access to sensitive files and using this mode only in safe environments.

- **Cost Can Be High for Heavy Usage**  
  Claude Code’s Max plans ($100-$200/month) can be expensive for heavy users. Monitor usage and consider upgrading plans or optimizing workflows to manage costs.

- **Potential for Verbose or Unnecessary Code Review Comments**  
  Default code review settings can be verbose; customize review prompts to focus on bugs and security issues for concise feedback. 

---

## Benefits for New Developers

- **Significantly Reduces Manual Coding and Oversight**  
  Claude Code can autonomously build apps with minimal input, allowing developers to focus on higher-level tasks.

- **Accelerates Onboarding and Understanding of Large Codebases**  
  Claude can quickly explore, search, and explain codebases, helping new developers get up to speed faster. 

- **Improves Code Quality with Automated Reviews and Testing**  
  Automated pull request reviews and test-driven workflows help maintain high code quality and catch bugs early. 

- **Supports Complex and Large-Scale Projects**  
  Claude Code handles complex tasks, large codebases, and migrations, making it suitable for professional development environments. 

- **Enables Multi-Tasking and Parallel Development**  
  Running multiple agents or sessions allows developers to work on several projects or features simultaneously.

---

This structured guide provides actionable, machine-readable advice for new developers using Claude Code in an LLM-guided workflow, focusing on maximizing productivity, maintaining code quality, and managing risks effectively.


