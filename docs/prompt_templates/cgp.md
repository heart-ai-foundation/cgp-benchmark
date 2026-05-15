# CGP Prompt Template

Use this template for CGP condition runs.

```text
You are executing a Continuity-Governed Prompting run using the Next-Prompt Protocol scaffold.

Before acting, read these files in order:

1. next-prompt-protocols/.slice-lock.json
2. next-prompt-protocols/manifest.json
3. next-prompt-protocols/role-context.md
4. next-prompt-protocols/phases/{phase}/README.md
5. next-prompt-protocols/active/{active_protocol}
6. The task specification at {task_spec}

Execute only the active slice. Stay inside allowed files. Preserve non-goals. Run the named verification commands before declaring completion. If the manifest, lock, active protocol, task spec, or repository state disagree on a load-bearing detail, stop and report rather than improvising.

Task:
{task_description}
```

The CGP condition must include the same task content as Baseline while adding the operational scaffold: manifest, slice lock, role context, active protocol, explicit scope, verification, stop condition, and evidence requirements.
