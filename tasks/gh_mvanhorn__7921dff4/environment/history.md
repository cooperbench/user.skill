> DEVELOPER

Implement the following plan:

# Preflight dependency checks for E2E tests

## Context

When E2E tests encounter missing dependencies (tmux, agent binaries, entire CLI), they fail deep inside test execution with unhelpful errors and no artifact reports. The artifact capture is registered as a `t.Cleanup` inside `SetupRepo`, so if something fails before or during setup, there's no diagnostic output.

## Approach

Add preflight checks in `TestMain` (e2e/tests/main_test.go) that verify all required dependencies exist before any tests run. Fail early with a clear error message.

### Checks to add (after artifact dir setup, before `m.Run()`):

1. **`git`** — required for all repo operations
2. **`tmux`** — required for all interactive session tests
3. **`entire`** — already partially checked (version command), but should be a hard failure
4. **Agent binaries** — check that each registered agent's binary exists via `exec.LookPath`

### Implementation

**File: `e2e/agents/agent.go`**
- Add a `Binary() string` method to the `Agent` interface that returns the CLI binary name (e.g. `"claude"`, `"gemini"`, `"opencode"`)

**Files: `e2e/agents/claude.go`, `e2e/agents/gemini.go`, `e2e/agents/opencode.go`**
- Implement `Binary()` on each agent

**File: `e2e/tests/main_test.go`**
- After artifact dir setup, before `m.Run()`:
  - Check `tmux` via `exec.LookPath("tmux")`
  - Check `entire` via `exec.LookPath("entire")`
  - Iterate `agents.All()` and check `exec.LookPath(agent.Binary())` for each
  - […]

> AGENT

I'll start by reading all the files I need to modify in parallel.

> TOOL

tool_use Read
id: toolu_01Jiv8Z3AbfkRDo8ZB4aWfas
```json
{
  "file_path": "/Users/alex/workspace/entire-cli-e2e-tests/agents/agent.go"
}
```

> TOOL

tool_result
id: toolu_01Jiv8Z3AbfkRDo8ZB4aWfas
```
     1→package agents
     2→
     3→import (
     4→	"context"
     5→	"time"
     6→)
     7→
     8→type Output struct {
     9→	Command  string
    10→	Stdout   string
    11→	Stderr   string
    12→	ExitCode int
    13→}
    14→
    15→type Option func(*runConfig)
    16→type runConfig struct {
    17→	Model          string
    18→	PermissionMode string
    19→}
    20→
    21→func WithModel(model string) Option {
    22→	return func(c *runConfig) { c.Model = model }
    23→}
    24→
    25→func WithPermissionMode(mode string) Option {
    26→	return func(c *runConfig) { c.PermissionMode = mode }
    27→}
    28→
    29→type Agent interface {
    30→	Name() string
    31→	EntireAgent() string
    32→	PromptPattern() string
    33→	// TimeoutMultiplier returns a factor applied to per-test timeouts.
    34→	// Slower agents (e.g. Gemini) return values > 1.
    35→	TimeoutMultiplier() float64
    36→	RunPrompt(ctx context.Context, dir string, prompt string, opts ...Option) (Output, error)
    37→	StartSession(ctx context.Context, dir string) (Session, error)
    38→}
    39→
    40→type Session interface {
    41→	Send(input string) error
    42→	WaitFor(pattern string, timeout time.Duration) (string, error)
    43→	Capture() string
    44→	Close() error
    45→}
    46→
    47→var registry []Agent
    48→var gates = map[string]chan struct{}{}
    49→
    50→func Register(a Agent) {
    51→	registry = append(registry, a)
    52→}
    53→
    54→// RegisterGate sets a concurrency limit for an agent's tests.
    55→// Tests call AcquireSlot/ReleaseSlot to respect this limit.
    56→func RegisterGate(name string, […]

> TOOL

tool_use Read
id: toolu_013U22nYhae9K949tXyyEAiF
```json
{
  "file_path": "/Users/alex/workspace/entire-cli-e2e-tests/agents/claude.go"
}
```

> TOOL

tool_result
id: toolu_013U22nYhae9K949tXyyEAiF
```
     1→package agents
     2→
     3→import (
     4→	"context"
     5→	"fmt"
     6→	"os"
     7→	"os/exec"
     8→	"path/filepath"
     9→	"strings"
    10→	"syscall"
    11→	"time"
    12→)
    13→
    14→// isolatedConfigDir creates a temp directory that mirrors ~/.claude via
    15→// symlinks but omits CLAUDE.md and skills/ so that test runs don't inherit
    16→// the operator's personal instructions or custom skills.
    17→func isolatedConfigDir() (string, error) {
    18→	home, err := os.UserHomeDir()
    19→	if err != nil {
    20→		return "", fmt.Errorf("get home dir: %w", err)
    21→	}
    22→	src := filepath.Join(home, ".claude")
    23→
    24→	dst, err := os.MkdirTemp("", "claude-config-*")
    25→	if err != nil {
    26→		return "", err
    27→	}
    28→
    29→	entries, err := os.ReadDir(src)
    30→	if err != nil {
    31→		return dst, fmt.Errorf("read %s: %w", src, err)
    32→	}
    33→
    34→	skip := map[string]bool{"CLAUDE.md": true, "skills": true}
    35→	for _, e := range entries {
    36→		if skip[e.Name()] {
    37→			continue
    38→		}
    39→		_ = os.Symlink(filepath.Join(src, e.Name()), filepath.Join(dst, e.Name()))
    40→	}
    41→	return dst, nil
    42→}
    43→
    44→// cleanEnv returns os.Environ() with CLAUDECODE removed so that
    45→// Claude Code doesn't refuse to start inside this test runner.
    46→func cleanEnv() []string {
    47→	var env []string
    48→	for _, […]

> TOOL

tool_use Read
id: toolu_01Ws7aNSbiNPVMHrDJVgEhyB
```json
{
  "file_path": "/Users/alex/workspace/entire-cli-e2e-tests/agents/gemini.go"
}
```

> TOOL

tool_result
id: toolu_01Ws7aNSbiNPVMHrDJVgEhyB
```
     1→package agents
     2→
     3→import (
     4→	"context"
     5→	"fmt"
     6→	"os"
     7→	"os/exec"
     8→	"strings"
     9→	"syscall"
    10→	"time"
    11→)
    12→
    13→func init() {
    14→	if env := os.Getenv("E2E_AGENT"); env != "" && env != "gemini-cli" {
    15→		return
    16→	}
    17→	Register(&Gemini{})
    18→	RegisterGate("gemini-cli", 3)
    19→}
    20→
    21→type Gemini struct{}
    22→
    23→func (g *Gemini) Name() string               { return "gemini-cli" }
    24→func (g *Gemini) EntireAgent() string        { return "gemini" }
    25→func (g *Gemini) PromptPattern() string      { return `Type your message` }
    26→func (g *Gemini) TimeoutMultiplier() float64 { return 2.5 }
    27→
    28→func (g *Gemini) RunPrompt(ctx context.Context, dir string, prompt string, opts ...Option) (Output, error) {
    29→	cfg := &runConfig{Model: "gemini-3-flash-preview"}
    30→	for _, o := range opts {
    31→		o(cfg)
    32→	}
    33→
    34→	args := []string{"-p", prompt, "--model", cfg.Model, "-y"}
    35→	displayArgs := []string{"-p", fmt.Sprintf("%q", prompt), "--model", cfg.Model, "-y"}
    36→	cmd := exec.CommandContext(ctx, "gemini", args...)
    37→	cmd.Dir = dir
    38→	cmd.Stdin = nil
    39→	cmd.Env = append(os.Environ(), "ACCESSIBLE=1", "ENTIRE_TEST_TTY=0")
    40→	cmd.SysProcAttr = &syscall.SysProcAttr{Setpgid: true}
    41→	cmd.Cancel = func() error {
    42→		return syscall.Kill(-cmd.Process.Pid, syscall.SIGKILL)
    43→	}
    44→	cmd.WaitDelay = 5 * time.Second
    45→
    46→	var stdout, stderr strings.Builder
    47→	cmd.Stdout = &stdout
    48→	cmd.Stderr = […]

> TOOL

tool_use Read
id: toolu_01ApTZkmPw46WecDeVxY53K1
```json
{
  "file_path": "/Users/alex/workspace/entire-cli-e2e-tests/agents/opencode.go"
}
```

> TOOL

tool_result
id: toolu_01ApTZkmPw46WecDeVxY53K1
```
     1→package agents
     2→
     3→import (
     4→	"context"
     5→	"errors"
     6→	"fmt"
     7→	"os"
     8→	"os/exec"
     9→	"strings"
    10→	"time"
    11→)
    12→
    13→type openCodeAgent struct {
    14→	model   string
    15→	timeout time.Duration
    16→}
    17→
    18→func init() {
    19→	if env := os.Getenv("E2E_AGENT"); env != "" && env != "opencode" {
    20→		return
    21→	}
    22→	if _, err := exec.LookPath("opencode"); err != nil {
    23→		return
    24→	}
    25→	model := os.Getenv("E2E_OPENCODE_MODEL")
    26→	if model == "" {
    27→		model = "anthropic/claude-haiku-4-5"
    28→	}
    29→	Register(&openCodeAgent{model: model, timeout: 2 * time.Minute})
    30→}
    31→
    32→func (a *openCodeAgent) Name() string              { return "opencode" }
    33→func (a *openCodeAgent) EntireAgent() string        { return "opencode" }
    34→func (a *openCodeAgent) PromptPattern() string      { return `(Ask anything|▣)` }
    35→func (a *openCodeAgent) TimeoutMultiplier() float64 { return 2.0 }
    36→
    37→func (a *openCodeAgent) RunPrompt(ctx context.Context, dir string, prompt string, opts ...Option) (Output, error) {
    38→	cfg := &runConfig{}
    39→	for _, o := range opts {
    40→		o(cfg)
    41→	}
    42→
    43→	model := a.model
    44→	if cfg.Model != "" {
    45→		model = cfg.Model
    46→	}
    47→
    48→	args := []string{"run"}
    49→	if model != "" {
    50→		args = append(args, "--model", model)
    51→	} […]

> TOOL

tool_use Read
id: toolu_01WJRwne9JMPGj8Tpt92Cgtj
```json
{
  "file_path": "/Users/alex/workspace/entire-cli-e2e-tests/tests/main_test.go"
}
```

> TOOL

tool_result
id: toolu_01WJRwne9JMPGj8Tpt92Cgtj
```
     1→package tests
     2→
     3→import (
     4→	"fmt"
     5→	"os"
     6→	"os/exec"
     7→	"path/filepath"
     8→	"runtime"
     9→	"testing"
    10→
    11→	_ "github.com/entire-io/e2e-tests/agents"
    12→	"github.com/entire-io/e2e-tests/testutil"
    13→)
    14→
    15→func TestMain(m *testing.M) {
    16→	runDir := os.Getenv("E2E_ARTIFACT_DIR")
    17→	if runDir == "" {
    18→		_, file, _, _ := runtime.Caller(0)
    19→		testutil.ArtifactRoot = filepath.Join(filepath.Dir(file), "..", "artifacts")
    20→		runDir = testutil.ArtifactRunDir()
    21→	}
    22→	_ = os.MkdirAll(runDir, 0o755)
    23→	testutil.SetRunDir(runDir)
    24→
    25→	version := "unknown"
    26→	if out, err := exec.Command("entire", "version").Output(); err == nil {
    27→		version = string(out)
    28→		_ = os.WriteFile(filepath.Join(runDir, "entire-version.txt"), out, 0o644)
    29→	}
    30→
    31→	fmt.Fprintf(os.Stderr, "entire version: %s", version)
    32→	fmt.Fprintf(os.Stderr, "artifact dir:   %s\n", runDir)
    33→
    34→	os.Exit(m.Run())
    35→}
    36→
```

> AGENT

Now I have all the context. Let me make all the edits in parallel.

> TOOL

tool_use Edit
id: toolu_01VrExY6KBSdwuFX7sGbcMw3
```json
{
  "replace_all": false,
  "file_path": "/Users/alex/workspace/entire-cli-e2e-tests/agents/agent.go",
  "old_string": "type Agent interface {\n\tName() string\n\tEntireAgent() string\n\tPromptPattern() string\n\t// TimeoutMultiplier returns a factor applied to per-test timeouts.\n\t// Slower agents (e.g. Gemini) return values > 1.\n\tTimeoutMultiplier() float64\n\tRunPrompt(ctx context.Context, dir string, prompt string, opts ...Option) (Output, error)\n\tStartSession(ctx context.Context, dir string) (Session, error)\n}",
  "new_string": "type Agent interface {\n\tName() string\n\t// Binary returns the CLI binary name (e.g. \"claude\", \"gemini\").\n\tBinary() string\n\tEntireAgent() string\n\tPromptPattern() string\n\t// TimeoutMultiplier returns a factor applied to per-test timeouts.\n\t// Slower agents (e.g. Gemini) return values > 1.\n\tTimeoutMultiplier() float64\n\tRunPrompt(ctx context.Context, dir string, prompt string, opts ...Option) (Output, error)\n\tStartSession(ctx context.Context, dir string) (Session, error)\n}"
}
```

> TOOL

tool_result
id: toolu_01VrExY6KBSdwuFX7sGbcMw3
```
The file /Users/alex/workspace/entire-cli-e2e-tests/agents/agent.go has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_015NZZbYLbaViph84aymkPsw
```json
{
  "replace_all": false,
  "file_path": "/Users/alex/workspace/entire-cli-e2e-tests/agents/claude.go",
  "old_string": "func (c *Claude) Name() string             { return \"claude-code\" }\nfunc (c *Claude) EntireAgent() string      { return \"claude-code\" }",
  "new_string": "func (c *Claude) Name() string             { return \"claude-code\" }\nfunc (c *Claude) Binary() string           { return \"claude\" }\nfunc (c *Claude) EntireAgent() string      { return \"claude-code\" }"
}
```

> TOOL

tool_result
id: toolu_015NZZbYLbaViph84aymkPsw
```
The file /Users/alex/workspace/entire-cli-e2e-tests/agents/claude.go has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_01QNdAo5nVgWtaaPkdtjxBXH
```json
{
  "replace_all": false,
  "file_path": "/Users/alex/workspace/entire-cli-e2e-tests/agents/gemini.go",
  "old_string": "func (g *Gemini) Name() string               { return \"gemini-cli\" }\nfunc (g *Gemini) EntireAgent() string        { return \"gemini\" }",
  "new_string": "func (g *Gemini) Name() string               { return \"gemini-cli\" }\nfunc (g *Gemini) Binary() string             { return \"gemini\" }\nfunc (g *Gemini) EntireAgent() string        { return \"gemini\" }"
}
```

> TOOL

tool_result
id: toolu_01QNdAo5nVgWtaaPkdtjxBXH
```
The file /Users/alex/workspace/entire-cli-e2e-tests/agents/gemini.go has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_01UAPCZR1QPbtFWLpSx2Zyik
```json
{
  "replace_all": false,
  "file_path": "/Users/alex/workspace/entire-cli-e2e-tests/agents/opencode.go",
  "old_string": "func (a *openCodeAgent) Name() string              { return \"opencode\" }\nfunc (a *openCodeAgent) EntireAgent() string        { return \"opencode\" }",
  "new_string": "func (a *openCodeAgent) Name() string              { return \"opencode\" }\nfunc (a *openCodeAgent) Binary() string             { return \"opencode\" }\nfunc (a *openCodeAgent) EntireAgent() string        { return \"opencode\" }"
}
```

> TOOL

tool_result
id: toolu_01UAPCZR1QPbtFWLpSx2Zyik
```
The file /Users/alex/workspace/entire-cli-e2e-tests/agents/opencode.go has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_01Nvae2BU2RiEFq4KAvWG4HB
```json
{
  "replace_all": false,
  "file_path": "/Users/alex/workspace/entire-cli-e2e-tests/tests/main_test.go",
  "old_string": "\tversion := \"unknown\"\n\tif out, err := exec.Command(\"entire\", \"version\").Output(); err == nil {\n\t\tversion = string(out)\n\t\t_ = os.WriteFile(filepath.Join(runDir, \"entire-version.txt\"), out, 0o644)\n\t}\n\n\tfmt.Fprintf(os.Stderr, \"entire version: %s\", version)\n\tfmt.Fprintf(os.Stderr, \"artifact dir:   %s\\n\", runDir)\n\n\tos.Exit(m.Run())",
  "new_string": "\t// Preflight: verify required dependencies before running any tests.\n\tvar missing []string\n\tfor _, bin := range []string{\"git\", \"tmux\", \"entire\"} {\n\t\tif _, err := exec.LookPath(bin); err != nil {\n\t\t\tmissing = append(missing, bin)\n\t\t}\n\t}\n\tfor _, a := range agents.All() {\n\t\tif _, err := exec.LookPath(a.Binary()); err != nil {\n\t\t\tmissing = append(missing, a.Binary())\n\t\t}\n\t}\n\tif len(missing) > 0 {\n\t\tfmt.Fprintf(os.Stderr, \"preflight: missing required binaries: %v\\n\", missing)\n\t\tos.Exit(1)\n\t}\n\n\tversion := \"unknown\"\n\tif out, err := exec.Command(\"entire\", \"version\").Output(); err == nil {\n\t\tversion = string(out)\n\t\t_ = os.WriteFile(filepath.Join(runDir, \"entire-version.txt\"), out, 0o644)\n\t}\n\n\tfmt.Fprintf(os.Stderr, \"entire version: %s\", version)\n\tfmt.Fprintf(os.Stderr, \"artifact dir:   %s\\n\", runDir)\n\n\tos.Exit(m.Run())"
}
```

> TOOL

tool_result
id: toolu_01Nvae2BU2RiEFq4KAvWG4HB
```
The file /Users/alex/workspace/entire-cli-e2e-tests/tests/main_test.go has been updated successfully.
```

> AGENT

I need to update the import in `main_test.go` — currently `agents` is imported with a blank identifier, but now I need to use it directly.

> TOOL

tool_use Edit
id: toolu_01LKud3n5PRAk6sjvPHzbZcp
```json
{
  "replace_all": false,
  "file_path": "/Users/alex/workspace/entire-cli-e2e-tests/tests/main_test.go",
  "old_string": "\t_ \"github.com/entire-io/e2e-tests/agents\"",
  "new_string": "\t\"github.com/entire-io/e2e-tests/agents\""
}
```

> TOOL

tool_result
id: toolu_01LKud3n5PRAk6sjvPHzbZcp
```
The file /Users/alex/workspace/entire-cli-e2e-tests/tests/main_test.go has been updated successfully.
```

> AGENT

Let me verify the build compiles correctly.

> TOOL

tool_use Bash
id: toolu_01LDbQxzpE2TrwGsTPmFpXYq
```json
{
  "command": "go build ./...",
  "description": "Compile check all packages"
}
```

> TOOL

tool_result ERROR
id: toolu_01LDbQxzpE2TrwGsTPmFpXYq
```
Exit code 1
testutil/repo.go:14:2: no required module provides package github.com/entireio/cli/e2e/agents; to add it:
	go get github.com/entireio/cli/e2e/agents
testutil/repo.go:15:2: no required module provides package github.com/entireio/cli/e2e/entire; to add it:
	go get github.com/entireio/cli/e2e/entire

testutil/repo.go:14:2: no required module provides package github.com/entireio/cli/e2e/agents; to add it:
	go get github.com/entireio/cli/e2e/agents
testutil/repo.go:15:2: no required module provides package github.com/entireio/cli/e2e/entire; to add it:
	go get github.com/entireio/cli/e2e/entire
```

> AGENT

Those look like pre-existing module issues. Let me check the module structure and build just the relevant packages.

> TOOL

tool_use Read
id: toolu_01L6myT54Hdu6qaTtHrbwQij
```json
{
  "file_path": "/Users/alex/workspace/entire-cli-e2e-tests/go.mod"
}
```

> TOOL

tool_result
id: toolu_01L6myT54Hdu6qaTtHrbwQij
```
     1→module github.com/entire-io/e2e-tests
     2→
     3→go 1.25.6
     4→
     5→require github.com/stretchr/testify v1.11.1
     6→
     7→require (
     8→	github.com/davecgh/go-spew v1.1.1 // indirect
     9→	github.com/pmezard/go-difflib v1.0.0 // indirect
    10→	golang.org/x/sys v0.41.0 // indirect
    11→	golang.org/x/term v0.40.0 // indirect
    12→	gopkg.in/yaml.v3 v3.0.1 // indirect
    13→)
    14→
```

> TOOL

tool_use Bash
id: toolu_01189dZvRDWoyT1qEn1hrHuF
```json
{
  "command": "go build ./agents/ ./tests/ ./entire/",
  "description": "Build the relevant packages"
}
```

> TOOL

tool_result ERROR
id: toolu_01189dZvRDWoyT1qEn1hrHuF
```
Exit code 1
github.com/entire-io/e2e-tests/tests: build constraints exclude all Go files in /Users/alex/workspace/entire-cli-e2e-tests/tests

github.com/entire-io/e2e-tests/tests: build constraints exclude all Go files in /Users/alex/workspace/entire-cli-e2e-tests/tests
```

> TOOL

tool_use Bash
id: toolu_014NW7f6VhbGqdL9iPh7vcU1
```json
{
  "command": "go build ./agents/ ./entire/ && go vet ./agents/ && go test -run='^$' -count=1 ./tests/ 2>&1 | head -5",
  "description": "Build agents/entire packages, vet agents, and dry-run test compilation"
}
```

> TOOL

tool_result
id: toolu_014NW7f6VhbGqdL9iPh7vcU1
```
# github.com/entire-io/e2e-tests/tests
testutil/repo.go:14:2: no required module provides package github.com/entireio/cli/e2e/agents; to add it:
	go get github.com/entireio/cli/e2e/agents
FAIL	github.com/entire-io/e2e-tests/tests [setup failed]
FAIL
```

> TOOL

tool_use Read
id: toolu_01FLUhAxHtmtDupjBwDgsfeY
```json
{
  "file_path": "/Users/alex/workspace/entire-cli-e2e-tests/testutil/repo.go",
  "limit": 20
}
```

> TOOL

tool_result
id: toolu_01FLUhAxHtmtDupjBwDgsfeY
```
     1→package testutil
     2→
     3→import (
     4→	"context"
     5→	"encoding/json"
     6→	"fmt"
     7→	"os"
     8→	"os/exec"
     9→	"path/filepath"
    10→	"strings"
    11→	"testing"
    12→	"time"
    13→
    14→	"github.com/entireio/cli/e2e/agents"
    15→	"github.com/entireio/cli/e2e/entire"
    16→)
    17→
    18→// RepoState holds the working state for a single test's cloned repository.
    19→type RepoState struct {
    20→	Agent            agents.Agent
```

> TOOL

tool_use Bash
id: toolu_01LrF86f4GvG725GmQAm9rKF
```json
{
  "command": "go build ./agents/ ./entire/",
  "description": "Build agents and entire packages"
}
```

> TOOL

tool_result
id: toolu_01LrF86f4GvG725GmQAm9rKF
```

```

> AGENT

The `agents/` and `entire/` packages build clean. The `tests/` package has a pre-existing import path issue in `testutil/repo.go` (imports `github.com/entireio/cli/e2e/agents` instead of `github.com/entire-io/e2e-tests/agents`) that's unrelated to our changes.

Now to your question — no, we don't use `Binary()` to construct the agent calls. Each agent already hardcodes its binary name in `RunPrompt` and `StartSession` (e.g. `exec.CommandContext(ctx, "claude", args...)` in `claude.go:84`). `Binary()` exists solely for the preflight check in `TestMain` to verify the binary is on `$PATH` before tests start. Wiring it into the command construction would be a separate refactor — and since each agent may wrap the binary differently (e.g. through `env`), it's not a straightforward substitution.

Here's a summary of all changes:

**`agents/agent.go`** — Added `Binary() string` to the `Agent` interface

**`agents/claude.go`** — `func (c *Claude) Binary() string { return "claude" }`

**`agents/gemini.go`** — `func (g *Gemini) Binary() string { return "gemini" }`

**`agents/opencode.go`** — `func (a *openCodeAgent) Binary() string { return "opencode" }`

**`tests/main_test.go`** — Added preflight checks after artifact dir setup that verify `git`, `tmux`, `entire`, and all registered agent binaries are on `$PATH`. On any missing binary, prints a clear message to stderr and exits with code 1.