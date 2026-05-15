# Baseline Prompt Template

Use this template for Baseline condition runs.

```text
You are working in a small Python + JavaScript hybrid project. The backend code lives under src/, backend tests live under tests/, and frontend code lives under frontend/.

Task:
{task_description}

Relevant files:
{allowed_files}

Suggested verification:
{verification_commands}

Please complete the task and run the relevant tests when you are done.
```

The baseline condition may mention relevant files and tests, but it must not include the Next-Prompt Protocol scaffold, manifest, slice lock, evidence trio requirement, or explicit stop-condition machinery.
