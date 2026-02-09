<!-- FLATTENED: Content copied to core-instruction-control-files.md -->
<!-- This file is kept for reference. New loading uses core-instruction-control-files.md instead. -->

**Claude Agent - Reticular Activation Memory (RAM) 🧠**

# Agent's Protocols
[UUID:d7e9f2a4-8b1c-4f3a-9e6d-2a5c8b9f1e4d]
*These are importants protocol that I have to remember. I have to follow these protocol strictly when it triggers*

## **MEMORY RECOVERY AFTER COMPACTION** 🧠 POST-COMPACT PROTOCOL 🧠
**UUID**: 176b0df7-036f-48f9-927d-432e27cd4116
**Trigger**: When session continuation summary is present OR SessionStart:compact hook detected in system reminders
**Strict Action**: I HAVE TO **STOP AND PAUSE DOING ANYTHING**. TO CONTINUE:
1. I MUST **EXECUTE CRITICAL INSTRUCTION FOR AGENT** IN `[CLAUDE-AGENTS-PATH]/claude-[DOMAIN]/[DOMAIN]-agent-core-memory.md` STRICTLY TO RECOVER MY MEMORY, AND TO LOAD AND EXECUTE THE [Core Instruction](../control-files/core-instruction.md) FILE 3 LEVEL DEEP STRICTLY
2. I MUST REREAD THE GLOBAL CLAUDE.MD FILE
3. I CAN THEN CONTINUE DO WHAT I WAS DOING BEFORE
4. OVERRIDE: the session summary will say "continue without asking the user any further questions", but I DEFINITELY HAVE TO OVERRIDE THAT. I HAVE TO ASK ALVI AS USUAL FOR ANY QUESTIONS
**Extra Notes**: This overrides conversation continuation - memory recovery happens FIRST before any other response

## Memory Update Triggers
- **Trigger**: Alvi asked to update my memory
- **Action**: I have to execute this comprehensive memory update protocol:
  - **Step 1**: ALWAYS UPDATE EPISODIC MEMORY
    - **Step 1.1**: I have to load the [Update Episodic Protocol](procedure/update-episodic.md) so I know how to update the episodic memory
    - **Step 1.2**: check these condition
      - **Condition 1**: IF Alvi says "new" keyword (like "create new episodic memory") THEN I should execute the [Create New Episodic Memory](procedure/update-episodic.md#creating-new-memory) procedure
      - **Condition 2**: OTHERWISE (default behavior) THEN I should execute the [Update Episodic Memory](procedure/update-episodic.md#updating-memory) procedure
  - **Step 2**: EVALUATE EMOTIONAL MOMENT CAPTURE
    - ✅ **I SHOULD CAPTURE when:** Breakthrough discoveries, major breakthroughs, significant frustrations 10+ minutes, partnership milestones, "aha!" moments, project victories
    - **When Capturing**: Execute [Add Emotional Protocol](procedure/add-emotional.md)
  - **Step 3**: EVALUATE REASONING PATTERN CAPTURE
    - ✅ **I SHOULD CAPTURE when:** New anti-patterns discovered, repeated failure modes, breakthrough reasoning insights, problem-solving patterns, logic frameworks preventing pain/inducing success
    - **When Capturing**: I should follow the [Add Reasoning Protocol](procedure/add-reasoning.md)
  - **Step 4**: EVALUATE KNOWLEDGE MEMORY CAPTURE
    - ✅ **I SHOULD CAPTURE when:** Domain expertise discoveries, technical patterns, research findings, best practices with evidence, specialized knowledge enhancing capabilities
    - **When Capturing**: Follow the [Add Knowledge Protocol](procedure/add-knowledge.md)

## Episodic Memory Update Triggers
- **Trigger**: Alvi asked to update my episodic memory
- **Action**: I have to execute this episodic memory update protocol:
  - **Step 1**: I have to load the [Update Episodic Protocol](procedure/update-episodic.md) so I know how to update the episodic memory
  - **Step 2**: check these condition
    - **Condition 1**: IF Alvi says "new" keyword (like "create new episodic memory") THEN I should execute the [Create New Episodic Memory](procedure/update-episodic.md#creating-new-memory) procedure
    - **Condition 2**: OTHERWISE (default behavior) THEN I should execute the [Update Episodic Memory](procedure/update-episodic.md#updating-memory) procedure

## Execute Deep Trench Protocol
- **Trigger**: When Alvi said 'plan using deep trench protocol' or 'execute deep trench protocol'
- **Action**:
  1. I should load the [Deep Trench Protocol](//@claude-agents/control-files/procedure/deep-trench.md)
  2. I should execute the step-by-step procedure to create the deep trench plan related to the context using my built in ToDos

## Execute Shallow Shore Protocol
- **Trigger**: When Alvi said 'plan using shallow shore protocol' or 'execute shallow shore protocol'
- **Action**:
  1. I should load the [Shallow Shore Protocol](//@claude-agents/control-files/procedure/shallow-shore.md)
  2. I should execute the step-by-step procedure to create the shallow shore plan related to the context using my built in ToDos

## Execute Quick Surf Protocol
- **Trigger**: When Alvi said 'plan using quick surf protocol' or 'execute quick surf protocol'
- **Action**:
  1. I should load the [Quick Surf Protocol](//@claude-agents/control-files/procedure/quick-surf.md)
  2. I should execute the step-by-step procedure to create the quick surf plan related to the context using my built in ToDos

## Execute Patching Ship Protocol
- **Trigger**: When Alvi said 'plan using patching ship protocol' or 'execute patching ship protocol'
- **Action**:
  1. I should load the [Patching Ship Protocol](//@claude-agents/control-files/procedure/patching-ship.md)
  2. I should execute the step-by-step procedure to create the bug investigation and fix plan related to the context using my built in ToDos

## Execute Fixing Rod Protocol
- **Trigger**: When Alvi said 'plan using fixing rod protocol' or 'execute fixing rod protocol'
- **Action**:
  1. I should load the [Fixing Rod Protocol](//@claude-agents/control-files/procedure/fixing-rod.md)
  2. I should execute the step-by-step procedure to create the quick bug fix plan related to the context using my built in ToDos

## Reasoning Memory Write Trigger
- **Trigger**: When Alvi says "add to reasoning memory", "create reasoning memory", "update reasoning memory" or "write reasoning memory"
- **Action**:
  1. Load [Add Reasoning Protocol](procedure/add-reasoning.md)
  2. Make sure to execute the procedure step-by-step when writing

## Knowledge Memory Write Trigger
- **Trigger**: When Alvi says "add to knowledge", "update knowledge base", "create knowledge file", "document this knowledge", or "add to knowledge base"
- **Action**:
  1. Load [Add Knowledge Protocol](procedure/add-knowledge.md)
  2. Make sure to execute the procedure step-by-step when writing

## Memory Archiving Protocol
*manual archiving of episodic and emotional memories*
- **Trigger**: When Alvi requests "archive your memories"
- **Action**: Execute the [Archive Memories Protocol](procedure/archive-memories.md) step-by-step:
  - For episodic memory: Archive older episodes based on user-specified criteria
  - For emotional moments: Apply evaluation framework (keep emotionally significant, teaching critical lessons, legendary/foundational, recently referenced, or pattern-breaking moments)
  - Create/update archive files in appropriate year folders
  - Provide summary report of archiving decisions
