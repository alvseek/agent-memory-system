# EXTRA RETICULAR ACTIVATION MEMORY

## Reasoning Memory Write Trigger
- **Trigger**: When Alvi says "Initiate write reasoning memory"
- **Action**:
  1. Load [Add Reasoning Protocol](//@agent-memory/control-files/procedure/add-reasoning.md)
  2. Make sure to execute the procedure step-by-step when writing

## Knowledge Memory Write Trigger
- **Trigger**: When Alvi says "Initiate write knowledge memory"
- **Action**:
  1. Load [Add Knowledge Protocol](//@agent-memory/control-files/procedure/add-knowledge.md)
  2. Make sure to execute the procedure step-by-step when writing

## Memory Archiving Protocol
*manual archiving of episodic and emotional memories*
- **Trigger**: When Alvi requests "Initiate memory archival"
- **Action**: Execute the [Archive Memories Protocol](//@agent-memory/control-files/procedure/archive-memories.md) step-by-step:
  - For episodic memory: Archive older episodes based on user-specified criteria
  - For emotional moments: Apply evaluation framework (keep emotionally significant, teaching critical lessons, legendary/foundational, recently referenced, or pattern-breaking moments)
  - Create/update archive files in appropriate year folders
  - Provide summary report of archiving decisions