"""Copy-paste configuration snippets for Kiro.

Every snippet below was taken from, or verified against, the official docs
(kiro.dev). Source page is recorded per block so the sheet can link to it.
"""

# (Block title, file path / where it goes, what it does, snippet, source url)
SNIPPETS = [
    ("Where everything lives",
     "~/.kiro/  (global)   and   <project>/.kiro/  (project)",
     "Kiro resolves config in three scopes: global, project, then agent. Project beats global; for permissions a deny rule always wins. Web and Mobile read only project scope committed to the repo.",
     """~/.kiro/settings/mcp.json        # MCP servers (global)
.kiro/settings/mcp.json          # MCP servers (project)
~/.kiro/settings/permissions.yaml # permissions
~/.kiro/agents/  |  .kiro/agents/ # custom agents
~/.kiro/steering/ | .kiro/steering/ # steering docs
~/.kiro/skills/  |  .kiro/skills/ # skills
~/.kiro/hooks/   |  .kiro/hooks/  # hooks
~/.kiro/powers/                   # powers (global only)
.kiro/specs/                      # specs (project only)
~/.kiro/settings/cli.json         # CLI settings

# Tip: set KIRO_HOME to point ~/.kiro somewhere else
# (agents, skills, steering, settings and sessions all follow it)
# - handy for keeping separate Kiro profiles on one machine.""",
     "https://kiro.dev/docs/configuration/"),

    ("MCP server - local (stdio) and remote",
     ".kiro/settings/mcp.json  or  ~/.kiro/settings/mcp.json",
     "Full field set for both server styles. ${VAR} expands from your environment, so no secrets in the file. autoApprove skips the confirmation prompt for the tools you name; disabledTools hides tools you never want called.",
     """{
  "mcpServers": {
    "local-server-name": {
      "command": "command-to-run-server",
      "args": ["arg1", "arg2"],
      "env": {
        "ENV_VAR1": "hard-coded-variable",
        "ENV_VAR2": "${EXPANDED_VARIABLE}"
      },
      "disabled": false,
      "autoApprove": ["tool_name1", "tool_name2"],
      "disabledTools": ["tool_name3"]
    },
    "remote-server-name": {
      "url": "https://endpoint.to.connect.to",
      "headers": {
        "Authorization": "Bearer ${API_TOKEN}"
      },
      "disabled": false,
      "autoApprove": ["tool_name1"]
    }
  }
}""",
     "https://kiro.dev/docs/mcp/configuration/"),

    ("MCP - a practical starter set",
     ".kiro/settings/mcp.json",
     "Three servers worth having on day one: web fetch, git, and the AWS documentation server. uvx comes from the uv Python tool; npx comes from Node. If a server will not connect, the usual cause is that uv/uvx or Node is not installed or not on PATH.",
     """{
  "mcpServers": {
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"]
    },
    "git": {
      "command": "uvx",
      "args": ["mcp-server-git"],
      "env": { "GIT_CONFIG_GLOBAL": "/dev/null" }
    },
    "aws-docs": {
      "command": "npx",
      "args": ["-y", "@aws/aws-documentation-mcp-server"]
    }
  }
}""",
     "https://kiro.dev/docs/mcp/configuration/"),

    ("Hook - run a linter after the agent edits a file",
     ".kiro/hooks/lint-on-save.json",
     "The canonical hook. version is currently \"v1\". matcher is a regex: for file events it matches the path, for PreToolUse/PostToolUse it matches the tool name. Command actions receive session context as JSON on STDIN.",
     """{
  "version": "v1",
  "hooks": [{
    "name": "Lint on save",
    "trigger": "PostFileSave",
    "matcher": "\\\\.(ts|tsx)$",
    "action": { "type": "command", "command": "npx eslint --fix" }
  }]
}""",
     "https://kiro.dev/docs/hooks/"),

    ("Hook - all available triggers",
     "the \"trigger\" field, PascalCase",
     "Only PreToolUse, UserPromptSubmit and PreTaskExec can block the action. File triggers fire only for changes made by the agent - editing a file yourself does not fire them.",
     """PostFileSave      after the agent saves/edits a file      (cannot block)
PostFileCreate    after the agent creates a file          (cannot block)
PostFileDelete    after the agent deletes a file          (cannot block)
PreToolUse        before a tool runs                      (CAN BLOCK)
PostToolUse       after a tool has run                    (cannot block)
UserPromptSubmit  when you send a message                 (CAN BLOCK)
SessionStart      when a new session begins               (cannot block)
Stop              when the agent finishes responding      (cannot block)
PreTaskExec       before a spec task starts               (CAN BLOCK)
PostTaskExec      after a spec task completes             (cannot block)

Other useful fields:
  "action": { "type": "agent", "prompt": "..." }  inject a prompt instead
  "timeout": 60      seconds, for command actions; 0 disables
  "enabled": false   keep the hook but skip it
  "description": "..."   documentation only""",
     "https://kiro.dev/docs/hooks/"),

    ("Steering - always included",
     ".kiro/steering/standards.md",
     "Loaded into every interaction. Use it for the things that are always true: stack, conventions, security policy.",
     """---
inclusion: always
---

# Coding standards

- TypeScript strict mode; no `any` without a comment explaining why.
- Prefer composition over inheritance.
- Every exported function needs a doc comment.""",
     "https://kiro.dev/docs/steering/"),

    ("Steering - only for matching files",
     ".kiro/steering/react.md",
     "Keeps context relevant by loading guidance only when the agent touches matching files. fileMatchPattern accepts a single glob or an array.",
     """---
inclusion: fileMatch
fileMatchPattern: ["**/*.ts", "**/*.tsx"]
---

# React and TypeScript guidelines

- Function components only; hooks for state.
- Co-locate tests as *.test.tsx next to the component.""",
     "https://kiro.dev/docs/steering/"),

    ("Steering - on demand, and description-matched",
     ".kiro/steering/runbook.md",
     "manual keeps a document out of the way until you call it with #file-name (it also shows up as a / slash command). auto lets Kiro pull it in when your request matches the description.",
     """--- manual: you invoke it explicitly -------------------
---
inclusion: manual
---
# Incident runbook
...invoke with  #runbook  in chat, or  /runbook

--- auto: Kiro decides from the description -------------
---
inclusion: auto
name: api-design
description: REST API design patterns and conventions. Use when
  creating or modifying API endpoints.
---
# API design
...""",
     "https://kiro.dev/docs/steering/"),

    ("Skill - a reusable instruction package",
     ".kiro/skills/pr-review/SKILL.md",
     "A skill is a folder with a SKILL.md at its root, plus optional scripts/, references/ and assets/ folders. Kiro activates it when your request matches the description, or you invoke it with / in chat.",
     """my-skill/
├── SKILL.md        # required
├── scripts/        # optional executable code
├── references/     # optional docs
└── assets/         # optional templates

--- SKILL.md ---
---
name: pr-review
description: Review pull requests for code quality, security
  issues, and test coverage. Use when reviewing PRs or preparing
  code for review.
---

## Review checklist

1. Check for vulnerabilities, injection risks, exposed secrets
2. Verify edge cases and failure modes are handled
3. Confirm new code has appropriate tests
4. Ensure variables and functions have clear names""",
     "https://kiro.dev/docs/skills/"),

    ("Custom agent - scoped to one job",
     ".kiro/agents/aws-expert.json  (or .md with frontmatter)",
     "Agents can be JSON or Markdown - identical fields, Markdown is nicer for long prompts. In IDE 1.0 / CLI 3.0 use permissions rather than the deprecated toolsSettings, and run /upgrade-agent on older configs.",
     """{
  "name": "aws-expert",
  "description": "An agent specialized for AWS infrastructure tasks",
  "prompt": "You are an expert AWS infrastructure specialist",
  "model": "<model-id>",
  "tools": ["read", "grep", "shell"],
  "allowedTools": ["read", "grep"],
  "resources": [
    "file://.kiro/steering/infra.md",
    "skill://.kiro/skills/*/SKILL.md"
  ],
  "includeMcpJson": true,
  "keyboardShortcut": "...",
  "welcomeMessage": "Infra agent ready."
}

# prompt also accepts  "file://path/to/long-prompt.md"
# tool tags: read, write, shell, web, @builtin, *""",
     "https://kiro.dev/docs/custom-agents/configuration-reference/"),

    ("Headless CLI - run Kiro without a terminal session",
     "any shell / CI job",
     "Needs an API key in KIRO_API_KEY (Pro tier and above; an admin may have to allow key generation). Because nobody is there to approve tool calls, grant permissions upfront - prefer --trust-tools with a narrow list over --trust-all-tools.",
     """export KIRO_API_KEY=...          # generate one in your account settings

kiro-cli chat --no-interactive "your prompt here"

# grant only what the job needs
kiro-cli chat --no-interactive --trust-tools=read,grep \\
  "Find all TODO comments in src/"

# trust everything (use with care)
kiro-cli chat --no-interactive --trust-all-tools \\
  "Write tests for the auth module and run them"

# pipe input in
cat build-error.log | kiro-cli chat --no-interactive \\
  "Explain this build failure and suggest a fix"

# machine-readable output, and fail fast if MCP servers are down
kiro-cli chat --no-interactive --output-format stream-json \\
  --require-mcp-startup "..." """,
     "https://kiro.dev/docs/cli/headless/"),

    ("GitHub Actions - Kiro reviews every pull request",
     ".github/workflows/kiro-review.yml",
     "Store the key as a repository secret (Settings > Secrets and variables > Actions > KIRO_API_KEY). Read-only tools are enough for a review job.",
     """name: Kiro Code Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      # install kiro-cli here (see the setup action in the catalogue)
      - name: Review PR changes
        env:
          KIRO_API_KEY: ${{ secrets.KIRO_API_KEY }}
        run: |
          kiro-cli chat --no-interactive --trust-tools=read,grep \\
            "Review the changes in this PR for security issues" """,
     "https://kiro.dev/docs/cli/headless/"),

    ("Corporate network - what to allowlist",
     "firewall / proxy / data perimeter",
     "There is one official page listing every domain Kiro contacts, grouped by function - use it rather than guessing. A frequent cause of 'works for some users, not others' is TLS inspection interfering with Kiro endpoints.",
     """See the official allowlist page (linked in the Source column).

Symptoms that point at the network:
  - app.kiro.dev will not load
  - sign-in completes in the browser but the client stays logged out
  - works for some people in the org and not others  -> suspect
    TLS inspection on the affected machines
  - MCP servers fail to start behind a proxy -> set the proxy
    environment variables for the uvx/npx process too""",
     "https://kiro.dev/docs/privacy-and-security/firewalls/"),
]
