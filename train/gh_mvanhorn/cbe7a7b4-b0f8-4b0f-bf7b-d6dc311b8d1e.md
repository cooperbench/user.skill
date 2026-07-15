> DEVELOPER

Implement the following plan:

# Test: Skip transcript flush wait for idle/ended sessions

## Context

We fixed a performance bug where `waitForTranscriptFlush` (3s timeout) was called during prepare-commit-msg and post-commit hooks for sessions that had already flushed their transcript (IDLE/ENDED phase). The fix guards `PrepareTranscript` calls with `state.Phase.IsActive()`.

We need a test that verifies: when a session is IDLE or ENDED and PostCommit runs, it completes quickly without hitting the 3s sentinel timeout.

## Approach

Add a timing-based test to `phase_postcommit_test.go` that:

1. Sets up a session with a checkpoint and a `TranscriptPath` pointing to a real transcript file (important — without `TranscriptPath` set, the `PrepareTranscript` code path is never reached)
2. Sets the session `AgentType` to `claude-code` (triggers the sentinel wait in `PrepareTranscript`)
3. Sets phase to IDLE
4. Runs `PostCommit()`
5. Asserts it completes in **under 2 seconds** (well under the 3s sentinel timeout)

This is a regression test: before the fix, this test would take ~3s+ per session due to sentinel timeouts. After the fix, it completes in milliseconds.

Also add a parallel test for ENDED phase to cover both non-active states.

### Why timing assertion works here

The sentinel timeout is 3s. Normal PostCommit for these tests runs in <500ms (git operations only). A 2s threshold gives generous headroom while still catching the 3s timeout regression. This is not a flaky pattern because the difference is 10-50x (milliseconds vs seconds).

## Files to modify

- `cmd/entire/cli/strategy/phase_postcommit_test.go` — add new test

## Test structure

```go
func TestPostCommit_IdleSession_SkipsSentinelWait(t *testing.T) {
    // Setup: git repo, session with checkpoint, transcript file, AgentType=claude-code
    // Set phase to IDLE, set TranscriptPath to transcript file
    // Time PostCommit() — assert < 2s
    // Also verify condensation still happened correctly
}

func TestPostCommit_EndedSession_SkipsSentinelWait(t *testing.T) {
    // Same but with phase=ENDED and FilesTouched set
}
```

Key setup details:
- Must set `state.TranscriptPath` to a real file (otherwise PrepareTranscript short-circuits on empty path)
- Must set `state.AgentType = agent.AgentTypeClaudeCode` (only Claude Code has the sentinel wait)
- Use existing `setupSessionWithCheckpoint` + `commitWithCheckpointTrailer` helpers
- Follow existing test patterns in `phase_postcommit_test.go`

## Verification

```bash
mise run test        # All unit tests pass
mise run test:ci     # Unit + integration tests pass
mise run lint        # No lint issues
```


If you need specific details from before exiting plan mode (like exact code snippets, error messages, or content you generated), read the full transcript at: /Users/soph/.claude/projects/-Users-soph-Work-entire-devenv-cli-experiments/0678bc4f-2fc6-46a8-be5f-bc8938d51a06.jsonl

> AGENT

Let me read the existing test file and related source files to understand the patterns.

> TOOL

tool_use Read
id: toolu_012CUEFmjUyqXUC3HNSafzCc
```json
{
  "file_path": "/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/strategy/phase_postcommit_test.go"
}
```

> TOOL

tool_result
id: toolu_012CUEFmjUyqXUC3HNSafzCc
```
     1→package strategy
     2→
     3→import (
     4→	"context"
     5→	"os"
     6→	"path/filepath"
     7→	"testing"
     8→	"time"
     9→
    10→	"github.com/entireio/cli/cmd/entire/cli/checkpoint"
    11→	"github.com/entireio/cli/cmd/entire/cli/checkpoint/id"
    12→	"github.com/entireio/cli/cmd/entire/cli/paths"
    13→	"github.com/entireio/cli/cmd/entire/cli/session"
    14→	"github.com/entireio/cli/cmd/entire/cli/trailers"
    15→
    16→	"github.com/go-git/go-git/v5"
    17→	"github.com/go-git/go-git/v5/plumbing"
    18→	"github.com/go-git/go-git/v5/plumbing/object"
    19→	"github.com/stretchr/testify/assert"
    20→	"github.com/stretchr/testify/require"
    21→)
    22→
    23→const testNewActiveSessionID = "new-active-session"
    24→
    25→// TestPostCommit_ActiveSession_CondensesImmediately verifies that PostCommit on
    26→// an ACTIVE session condenses immediately and stays ACTIVE.
    27→// With the 1:1 checkpoint model, each commit gets its own checkpoint right away.
    28→func TestPostCommit_ActiveSession_CondensesImmediately(t *testing.T) {
    29→	dir := setupGitRepo(t)
    30→	t.Chdir(dir)
    31→
    32→	repo, err := git.PlainOpen(dir)
    33→	require.NoError(t, err)
    34→
    35→	s := &ManualCommitStrategy{}
    36→	sessionID := "test-postcommit-active"
    37→
    38→	// Initialize session and save a checkpoint so there is shadow branch content
    39→	setupSessionWithCheckpoint(t, s, repo, dir, sessionID)
    40→
    41→	// Set phase to ACTIVE (simulating agent mid-turn)
    42→	state, err := s.loadSessionState(sessionID)
    43→	require.NoError(t, err)
    44→	state.Phase = session.PhaseActive
    45→	require.NoError(t, s.saveSessionState(state))
    46→
    47→	// Create a commit WITH the Entire-Checkpoint trailer on the main branch
    48→	commitWithCheckpointTrailer(t, repo, dir, "a1b2c3d4e5f6")
    49→
    50→	// Run PostCommit
    51→	err = s.PostCommit()
    52→	require.NoError(t, err)
    53→
    54→	// Verify phase stays ACTIVE (immediate condensation, no deferred phase)
    55→	state, err = s.loadSessionState(sessionID)
    56→	require.NoError(t, err)
    57→	require.NotNil(t, state)
    58→	assert.Equal(t, session.PhaseActive, state.Phase,
    59→		"ACTIVE session should stay ACTIVE after immediate condensation on GitCommit")
    60→
    61→	// Verify condensation happened: the entire/checkpoints/v1 branch should exist
    62→	sessionsRef, err := repo.Reference(plumbing.NewBranchReferenceName(paths.MetadataBranchName), true)
    63→	require.NoError(t, err, "entire/checkpoints/v1 branch should exist after immediate condensation")
    64→	assert.NotNil(t, sessionsRef)
    65→
    66→	// Verify StepCount was reset to 0 by condensation
    67→	assert.Equal(t, 0, state.StepCount,
    68→		"StepCount should be reset after immediate condensation")
    69→}
    70→
    71→// TestPostCommit_IdleSession_Condenses verifies that PostCommit on an IDLE
    72→// session condenses session data and cleans up the shadow branch.
    73→func TestPostCommit_IdleSession_Condenses(t *testing.T) {
    74→	dir := setupGitRepo(t)
    75→	t.Chdir(dir)
    76→
    77→	repo, err := git.PlainOpen(dir)
    78→	require.NoError(t, err)
    79→
    80→	s := &ManualCommitStrategy{}
    81→	sessionID := "test-postcommit-idle"
    82→
    83→	// Initialize session and save a checkpoint so there is shadow branch content
    84→	setupSessionWithCheckpoint(t, s, repo, dir, sessionID)
    85→
    86→	// Set phase to IDLE (agent turn finished, waiting for user)
    87→	state, err := s.loadSessionState(sessionID)
    88→	require.NoError(t, err)
    89→	state.Phase = session.PhaseIdle
    90→	state.LastInteractionTime = nil
    91→	state.FilesTouched = []string{"test.txt"}
    92→	require.NoError(t, s.saveSessionState(state))
    93→
    94→	// Record shadow branch name before PostCommit
    95→	shadowBranch := getShadowBranchNameForCommit(state.BaseCommit, state.WorktreeID)
    96→
    97→	// Create a commit WITH the Entire-Checkpoint trailer
    98→	commitWithCheckpointTrailer(t, repo, dir, "b2c3d4e5f6a1")
    99→
   100→	// Run PostCommit
   101→	err = s.PostCommit()
   102→	require.NoError(t, err)
   103→
   104→	// Verify condensation happened: the entire/checkpoints/v1 branch should exist
   105→	sessionsRef, err := repo.Reference(plumbing.NewBranchReferenceName(paths.MetadataBranchName), true)
   106→	require.NoError(t, err, "entire/checkpoints/v1 branch should exist after condensation")
   107→	assert.NotNil(t, sessionsRef)
   108→
   109→	// Verify shadow branch IS deleted after condensation
   110→	refName := plumbing.NewBranchReferenceName(shadowBranch)
   111→	_, err = repo.Reference(refName, true)
   112→	assert.Error(t, err,
   113→		"shadow branch should be deleted after condensation for IDLE session")
   114→}
   115→
   116→// TestPostCommit_RebaseDuringActive_SkipsTransition verifies that PostCommit
   117→// is a no-op during rebase operations, leaving the session phase unchanged.
   118→func TestPostCommit_RebaseDuringActive_SkipsTransition(t *testing.T) {
   119→	dir := setupGitRepo(t)
   120→	t.Chdir(dir)
   121→
   122→	repo, err := git.PlainOpen(dir)
   123→	require.NoError(t, err)
   124→
   125→	s := &ManualCommitStrategy{}
   126→	sessionID := "test-postcommit-rebase"
   127→
   128→	// Initialize session and save a checkpoint
   129→	setupSessionWithCheckpoint(t, s, repo, dir, sessionID)
   130→
   131→	// Set phase to ACTIVE
   132→	state, err := s.loadSessionState(sessionID)
   133→	require.NoError(t, err)
   134→	state.Phase = session.PhaseActive
   135→	require.NoError(t, s.saveSessionState(state))
   136→
   137→	// Capture shadow branch name BEFORE any state changes
   138→	shadowBranch := getShadowBranchNameForCommit(state.BaseCommit, state.WorktreeID)
   139→	originalStepCount := state.StepCount
   140→
   141→	// Simulate rebase in progress by creating .git/rebase-merge/ directory
   142→	gitDir := filepath.Join(dir, ".git")
   143→	rebaseMergeDir := filepath.Join(gitDir, "rebase-merge")
   144→	require.NoError(t, os.MkdirAll(rebaseMergeDir, 0o755))
   145→	defer os.RemoveAll(rebaseMergeDir)
   146→
   147→	// Create a commit WITH the checkpoint trailer
   148→	commitWithCheckpointTrailer(t, repo, dir, "c3d4e5f6a1b2")
   149→
   150→	// Run PostCommit
   151→	err = s.PostCommit()
   152→	require.NoError(t, err)
   153→
   154→	// Verify phase stayed ACTIVE (no transition during rebase)
   155→	state, err = s.loadSessionState(sessionID)
   156→	require.NoError(t, err)
   157→	require.NotNil(t, state)
   158→	assert.Equal(t, session.PhaseActive, state.Phase,
   159→		"session should stay ACTIVE during rebase (no transition)")
   160→
   161→	// Verify StepCount was NOT reset (no condensation happened)
   162→	assert.Equal(t, originalStepCount, state.StepCount,
   163→		"StepCount should be unchanged - no condensation during rebase")
   164→
   165→	// Verify NO condensation happened (entire/checkpoints/v1 branch should not exist)
   166→	_, err = repo.Reference(plumbing.NewBranchReferenceName(paths.MetadataBranchName), true)
   167→	require.Error(t, err,
   168→		"entire/checkpoints/v1 branch should NOT exist - no condensation during rebase")
   169→
   170→	// Verify shadow branch still exists (not cleaned up during rebase)
   171→	refName := plumbing.NewBranchReferenceName(shadowBranch)
   172→	_, err = repo.Reference(refName, true)
   173→	assert.NoError(t, err,
   174→		"shadow branch should be preserved during rebase")
   175→}
   176→
   177→// TestPostCommit_ActiveSessionAlwaysCondenses verifies that an ACTIVE session
   178→// is always condensed on GitCommit, even when it has no checkpoints or tracked files.
   179→// This is because PrepareCommitMsg already validated the trailer, so PostCommit
   180→// trusts that decision rather than re-validating via transcript analysis (which is
   181→// unreliable when subagents are still running).
   182→func TestPostCommit_ActiveSessionAlwaysCondenses(t *testing.T) {
   183→	dir := setupGitRepo(t)
   184→	t.Chdir(dir)
   185→
   186→	repo, err := git.PlainOpen(dir)
   187→	require.NoError(t, err)
   188→
   189→	s := &ManualCommitStrategy{}
   190→	idleSessionID := "test-postcommit-idle-multi"
   191→	activeSessionID := "test-postcommit-active-multi"
   192→
   193→	// Initialize the idle session with a checkpoint
   194→	setupSessionWithCheckpoint(t, s, repo, dir, idleSessionID)
   195→
   196→	// Get worktree path and base commit from the idle session
   197→	idleState, err := s.loadSessionState(idleSessionID)
   198→	require.NoError(t, err)
   199→	worktreePath := idleState.WorktreePath
   200→	baseCommit := idleState.BaseCommit
   201→	worktreeID := idleState.WorktreeID
   202→
   203→	// Set idle session to IDLE phase
   204→	idleState.Phase = session.PhaseIdle
   205→	idleState.LastInteractionTime = nil
   206→	idleState.FilesTouched = []string{"test.txt"}
   207→	require.NoError(t, s.saveSessionState(idleState))
   208→
   209→	// Create a second session with the SAME base commit and worktree (concurrent session).
   210→	// This session is ACTIVE but has NO checkpoints (StepCount=0, no shadow branch content).
   211→	// Despite having no content, it WILL be condensed because ACTIVE sessions always
   212→	// condense — PrepareCommitMsg already validated the trailer.
   213→	now := time.Now()
   214→	activeState := &SessionState{
   215→		SessionID:           activeSessionID,
   216→		BaseCommit:          baseCommit,
   217→		WorktreePath:        worktreePath,
   218→		WorktreeID:          worktreeID,
   219→		StartedAt:           now,
   220→		Phase:               session.PhaseActive,
   221→		LastInteractionTime: &now,
   222→		StepCount:           0,
   223→	}
   224→	require.NoError(t, s.saveSessionState(activeState))
   225→
   226→	// Record shadow branch name before PostCommit
   227→	shadowBranch := getShadowBranchNameForCommit(baseCommit, worktreeID)
   228→
   229→	// Create a commit WITH the checkpoint trailer
   230→	commitWithCheckpointTrailer(t, repo, dir, "d4e5f6a1b2c3")
   231→
   232→	// Run PostCommit
   233→	err = s.PostCommit()
   234→	require.NoError(t, err)
   235→
   236→	// Verify the ACTIVE session stays ACTIVE (immediate condensation model)
   237→	activeState, err = s.loadSessionState(activeSessionID)
   238→	require.NoError(t, err)
   239→	assert.Equal(t, session.PhaseActive, activeState.Phase,
   240→		"ACTIVE session should stay ACTIVE after GitCommit")
   241→
   242→	// Verify both sessions condensed (entire/checkpoints/v1 branch should exist)
   243→	idleState, err = s.loadSessionState(idleSessionID)
   244→	require.NoError(t, err)
   245→	sessionsRef, err := repo.Reference(plumbing.NewBranchReferenceName(paths.MetadataBranchName), true)
   246→	require.NoError(t, err, "entire/checkpoints/v1 branch should exist after condensation")
   247→	require.NotNil(t, sessionsRef)
   248→
   249→	// Verify IDLE session's StepCount was reset by condensation
   250→	assert.Equal(t, 0, idleState.StepCount,
   251→		"IDLE session StepCount should be reset after condensation")
   252→
   253→	// Verify shadow branch is cleaned up because ALL sessions condensed
   254→	// (both IDLE and ACTIVE were condensed on this commit)
   255→	refName := plumbing.NewBranchReferenceName(shadowBranch)
   256→	_, err = repo.Reference(refName, true)
   257→	assert.Error(t, err,
   258→		"shadow branch should be deleted when all sessions have been condensed")
   259→}
   260→
   261→// TestPostCommit_CondensationFailure_PreservesShadowBranch verifies that when
   262→// condensation fails (corrupted shadow branch), BaseCommit is NOT updated.
   263→func TestPostCommit_CondensationFailure_PreservesShadowBranch(t *testing.T) {
   264→	dir := setupGitRepo(t)
   265→	t.Chdir(dir)
   266→
   267→	repo, err := git.PlainOpen(dir)
   268→	require.NoError(t, err)
   269→
   270→	s := &ManualCommitStrategy{}
   271→	sessionID := "test-postcommit-condense-fail-idle"
   272→
   273→	// Initialize session and save a checkpoint
   274→	setupSessionWithCheckpoint(t, s, repo, dir, sessionID)
   275→
   276→	// Set phase to IDLE
   277→	state, err := s.loadSessionState(sessionID)
   278→	require.NoError(t, err)
   279→	state.Phase = session.PhaseIdle
   280→	state.LastInteractionTime = nil
   281→	state.FilesTouched = []string{"test.txt"}
   282→	require.NoError(t, s.saveSessionState(state))
   283→
   284→	// Record original BaseCommit and StepCount before corruption
   285→	originalBaseCommit := state.BaseCommit
   286→	originalStepCount := state.StepCount
   287→
   288→	// Corrupt shadow branch by pointing it at ZeroHash
   289→	shadowBranch := getShadowBranchNameForCommit(state.BaseCommit, state.WorktreeID)
   290→	corruptRef := plumbing.NewHashReference(plumbing.NewBranchReferenceName(shadowBranch), plumbing.ZeroHash)
   291→	require.NoError(t, repo.Storer.SetReference(corruptRef))
   292→
   293→	// Create a commit with the checkpoint trailer
   294→	commitWithCheckpointTrailer(t, repo, dir, "e5f6a1b2c3d4")
   295→
   296→	// Run PostCommit
   297→	err = s.PostCommit()
   298→	require.NoError(t, err, "PostCommit should not return error even when condensation fails")
   299→
   300→	// Verify BaseCommit was NOT updated (condensation failed)
   301→	state, err = s.loadSessionState(sessionID)
   302→	require.NoError(t, err)
   303→	assert.Equal(t, originalBaseCommit, state.BaseCommit,
   304→		"BaseCommit should NOT be updated when condensation fails")
   305→	assert.Equal(t, originalStepCount, state.StepCount,
   306→		"StepCount should NOT be reset when condensation fails")
   307→
   308→	// Verify entire/checkpoints/v1 branch does NOT exist (condensation failed)
   309→	_, err = repo.Reference(plumbing.NewBranchReferenceName(paths.MetadataBranchName), true)
   310→	require.Error(t, err,
   311→		"entire/checkpoints/v1 branch should NOT exist when condensation fails")
   312→
   313→	// Phase transition still applies even when condensation fails
   314→	assert.Equal(t, session.PhaseIdle, state.Phase,
   315→		"phase should remain IDLE when condensation fails")
   316→}
   317→
   318→// TestPostCommit_IdleSession_NoNewContent_PreservesBaseCommit verifies that when
   319→// an IDLE session has no new transcript content since last condensation,
   320→// PostCommit skips condensation and does NOT update BaseCommit.
   321→//
   322→// This prevents the bug where old IDLE sessions would have their BaseCommit
   323→// incorrectly updated, causing them to be condensed on future commits.
   324→func TestPostCommit_IdleSession_NoNewContent_PreservesBaseCommit(t *testing.T) {
   325→	dir := setupGitRepo(t)
   326→	t.Chdir(dir)
   327→
   328→	repo, err := git.PlainOpen(dir)
   329→	require.NoError(t, err)
   330→
   331→	s := &ManualCommitStrategy{}
   332→	sessionID := "test-postcommit-idle-no-content"
   333→
   334→	// Initialize session and save a checkpoint
   335→	setupSessionWithCheckpoint(t, s, repo, dir, sessionID)
   336→
   337→	// Set phase to IDLE with CheckpointTranscriptStart matching transcript length (2 lines)
   338→	state, err := s.loadSessionState(sessionID)
   339→	require.NoError(t, err)
   340→	state.Phase = session.PhaseIdle
   341→	state.LastInteractionTime = nil
   342→	state.CheckpointTranscriptStart = 2 // Transcript has exactly 2 lines
   343→	require.NoError(t, s.saveSessionState(state))
   344→
   345→	// Record shadow branch name and original BaseCommit
   346→	shadowBranch := getShadowBranchNameForCommit(state.BaseCommit, state.WorktreeID)
   347→	originalBaseCommit := state.BaseCommit
   348→	originalStepCount := state.StepCount
   349→
   350→	// Create a commit with the checkpoint trailer
   351→	commitWithCheckpointTrailer(t, repo, dir, "f6a1b2c3d4e5")
   352→
   353→	// Run PostCommit
   354→	err = s.PostCommit()
   355→	require.NoError(t, err)
   356→
   357→	// Verify BaseCommit was NOT updated (IDLE sessions don't get BaseCommit updated)
   358→	state, err = s.loadSessionState(sessionID)
   359→	require.NoError(t, err)
   360→	assert.Equal(t, originalBaseCommit, state.BaseCommit,
   361→		"BaseCommit should NOT be updated for IDLE session with no new content")
   362→
   363→	// Shadow branch should still exist (not deleted, no condensation)
   364→	refName := plumbing.NewBranchReferenceName(shadowBranch)
   365→	_, err = repo.Reference(refName, true)
   366→	require.NoError(t, err,
   367→		"shadow branch should still exist when no condensation happened")
   368→
   369→	// entire/checkpoints/v1 branch should NOT exist (no condensation)
   370→	_, err = repo.Reference(plumbing.NewBranchReferenceName(paths.MetadataBranchName), true)
   371→	require.Error(t, err,
   372→		"entire/checkpoints/v1 branch should NOT exist when no condensation happened")
   373→
   374→	// StepCount should be unchanged
   375→	assert.Equal(t, originalStepCount, state.StepCount,
   376→		"StepCount should be unchanged when no condensation happened")
   377→}
   378→
   379→// TestPostCommit_EndedSession_FilesTouched_Condenses verifies that an ENDED
   380→// session with files touched and new content condenses on commit.
   381→func TestPostCommit_EndedSession_FilesTouched_Condenses(t *testing.T) {
   382→	dir := setupGitRepo(t)
   383→	t.Chdir(dir)
   384→
   385→	repo, err := git.PlainOpen(dir)
   386→	require.NoError(t, err)
   387→
   388→	s := &ManualCommitStrategy{}
   389→	sessionID := "test-postcommit-ended-condenses"
   390→
   391→	// Initialize session and save a checkpoint
   392→	setupSessionWithCheckpoint(t, s, repo, dir, sessionID)
   393→
   394→	// Set phase to ENDED with files touched
   395→	state, err := s.loadSessionState(sessionID)
   396→	require.NoError(t, err)
   397→	now := time.Now()
   398→	state.Phase = session.PhaseEnded
   399→	state.EndedAt = &now
   400→	state.FilesTouched = []string{"test.txt"}
   401→	require.NoError(t, s.saveSessionState(state))
   402→
   403→	// Record shadow branch name
   404→	shadowBranch := getShadowBranchNameForCommit(state.BaseCommit, state.WorktreeID)
   405→
   406→	// Create a commit with the checkpoint trailer
   407→	commitWithCheckpointTrailer(t, repo, dir, "a1b2c3d4e5f7")
   408→
   409→	// Run PostCommit
   410→	err = s.PostCommit()
   411→	require.NoError(t, err)
   412→
   413→	// Verify entire/checkpoints/v1 branch exists (condensation happened)
   414→	sessionsRef, err := repo.Reference(plumbing.NewBranchReferenceName(paths.MetadataBranchName), true)
   415→	require.NoError(t, err, "entire/checkpoints/v1 branch should exist after condensation")
   416→	assert.NotNil(t, sessionsRef)
   417→
   418→	// Verify old shadow branch is deleted after condensation
   419→	refName := plumbing.NewBranchReferenceName(shadowBranch)
   420→	_, err = repo.Reference(refName, true)
   421→	require.Error(t, err,
   422→		"shadow branch should be deleted after condensation for ENDED session")
   423→
   424→	// Verify StepCount was reset by condensation
   425→	state, err = s.loadSessionState(sessionID)
   426→	require.NoError(t, err)
   427→	assert.Equal(t, 0, state.StepCount,
   428→		"StepCount should be reset after condensation")
   429→
   430→	// Phase stays ENDED
   431→	assert.Equal(t, session.PhaseEnded, state.Phase,
   432→		"ENDED session should stay ENDED after condensation")
   433→}
   434→
   435→// TestPostCommit_EndedSession_FilesTouched_NoNewContent verifies that an ENDED
   436→// session with files touched but no new transcript content skips condensation
   437→// and does NOT update BaseCommit.
   438→//
   439→// This prevents the bug where old ENDED sessions would have their BaseCommit
   440→// incorrectly updated, causing them to be condensed on future commits.
   441→func TestPostCommit_EndedSession_FilesTouched_NoNewContent(t *testing.T) {
   442→	dir := setupGitRepo(t)
   443→	t.Chdir(dir)
   444→
   445→	repo, err := git.PlainOpen(dir)
   446→	require.NoError(t, err)
   447→
   448→	s := &ManualCommitStrategy{}
   449→	sessionID := "test-postcommit-ended-no-content"
   450→
   451→	// Initialize session and save a checkpoint
   452→	setupSessionWithCheckpoint(t, s, repo, dir, sessionID)
   453→
   454→	// Set phase to ENDED with files touched but no new content
   455→	state, err := s.loadSessionState(sessionID)
   456→	require.NoError(t, err)
   457→	now := time.Now()
   458→	state.Phase = session.PhaseEnded
   459→	state.EndedAt = &now
   460→	state.FilesTouched = []string{"test.txt"}
   461→	state.CheckpointTranscriptStart = 2 // Transcript has exactly 2 lines
   462→	require.NoError(t, s.saveSessionState(state))
   463→
   464→	// Record shadow branch name, original BaseCommit, and StepCount
   465→	shadowBranch := getShadowBranchNameForCommit(state.BaseCommit, state.WorktreeID)
   466→	originalBaseCommit := state.BaseCommit
   467→	originalStepCount := state.StepCount
   468→
   469→	// Create a commit with the checkpoint trailer
   470→	commitWithCheckpointTrailer(t, repo, dir, "b2c3d4e5f6a2")
   471→
   472→	// Run PostCommit
   473→	err = s.PostCommit()
   474→	require.NoError(t, err)
   475→
   476→	// Verify entire/checkpoints/v1 branch does NOT exist (no condensation)
   477→	_, err = repo.Reference(plumbing.NewBranchReferenceName(paths.MetadataBranchName), true)
   478→	require.Error(t, err,
   479→		"entire/checkpoints/v1 branch should NOT exist when no new content")
   480→
   481→	// Shadow branch should still exist
   482→	refName := plumbing.NewBranchReferenceName(shadowBranch)
   483→	_, err = repo.Reference(refName, true)
   484→	require.NoError(t, err,
   485→		"shadow branch should still exist when no condensation happened")
   486→
   487→	// BaseCommit should NOT be updated (ENDED sessions don't get BaseCommit updated)
   488→	state, err = s.loadSessionState(sessionID)
   489→	require.NoError(t, err)
   490→	assert.Equal(t, originalBaseCommit, state.BaseCommit,
   491→		"BaseCommit should NOT be updated for ENDED session with no new content")
   492→
   493→	// StepCount unchanged
   494→	assert.Equal(t, originalStepCount, state.StepCount,
   495→		"StepCount should be unchanged when no condensation happened")
   496→}
   497→
   498→// TestPostCommit_EndedSession_NoFilesTouched_Discards verifies that an ENDED
   499→// session with no files touched takes the discard path and does NOT update BaseCommit.
   500→//
   501→// This prevents the bug where old ENDED sessions would have their BaseCommit
   502→// incorrectly updated, causing them to be condensed on future commits.
   503→func TestPostCommit_EndedSession_NoFilesTouched_Discards(t *testing.T) {
   504→	dir := setupGitRepo(t)
   505→	t.Chdir(dir)
   506→
   507→	repo, err := git.PlainOpen(dir)
   508→	require.NoError(t, err)
   509→
   510→	s := &ManualCommitStrategy{}
   511→	sessionID := "test-postcommit-ended-discard"
   512→
   513→	// Initialize session and save a checkpoint
   514→	setupSessionWithCheckpoint(t, s, repo, dir, sessionID)
   515→
   516→	// Set phase to ENDED with no files touched
   517→	state, err := s.loadSessionState(sessionID)
   518→	require.NoError(t, err)
   519→	now := time.Now()
   520→	state.Phase = session.PhaseEnded
   521→	state.EndedAt = &now
   522→	state.FilesTouched = nil // No files touched
   523→	require.NoError(t, s.saveSessionState(state))
   524→
   525→	// Record original BaseCommit and StepCount
   526→	originalBaseCommit := state.BaseCommit
   527→	originalStepCount := state.StepCount
   528→
   529→	// Create a commit with the checkpoint trailer
   530→	commitWithCheckpointTrailer(t, repo, dir, "c3d4e5f6a1b3")
   531→
   532→	// Run PostCommit
   533→	err = s.PostCommit()
   534→	require.NoError(t, err)
   535→
   536→	// Verify entire/checkpoints/v1 branch does NOT exist (no condensation for discard path)
   537→	_, err = repo.Reference(plumbing.NewBranchReferenceName(paths.MetadataBranchName), true)
   538→	require.Error(t, err,
   539→		"entire/checkpoints/v1 branch should NOT exist for discard path")
   540→
   541→	// BaseCommit should NOT be updated (ENDED sessions don't get BaseCommit updated)
   542→	state, err = s.loadSessionState(sessionID)
   543→	require.NoError(t, err)
   544→	assert.Equal(t, originalBaseCommit, state.BaseCommit,
   545→		"BaseCommit should NOT be updated for ENDED session on discard path")
   546→
   547→	// StepCount unchanged
   548→	assert.Equal(t, originalStepCount, state.StepCount,
   549→		"StepCount should be unchanged on discard path")
   550→
   551→	// Phase stays ENDED
   552→	assert.Equal(t, session.PhaseEnded, state.Phase,
   553→		"ENDED session should stay ENDED on discard path")
   554→}
   555→
   556→// TestPostCommit_CondensationFailure_EndedSession_PreservesShadowBranch verifies
   557→// that when condensation fails for an ENDED session with files touched,
   558→// BaseCommit is preserved (not updated).
   559→func TestPostCommit_CondensationFailure_EndedSession_PreservesShadowBranch(t *testing.T) {
   560→	dir := setupGitRepo(t)
   561→	t.Chdir(dir)
   562→
   563→	repo, err := git.PlainOpen(dir)
   564→	require.NoError(t, err)
   565→
   566→	s := &ManualCommitStrategy{}
   567→	sessionID := "test-postcommit-condense-fail-ended"
   568→
   569→	// Initialize session and save a checkpoint
   570→	setupSessionWithCheckpoint(t, s, repo, dir, sessionID)
   571→
   572→	// Set phase to ENDED with files touched
   573→	state, err := s.loadSessionState(sessionID)
   574→	require.NoError(t, err)
   575→	now := time.Now()
   576→	state.Phase = session.PhaseEnded
   577→	state.EndedAt = &now
   578→	state.FilesTouched = []string{"test.txt"}
   579→	require.NoError(t, s.saveSessionState(state))
   580→
   581→	// Record original BaseCommit and StepCount
   582→	originalBaseCommit := state.BaseCommit
   583→	originalStepCount := state.StepCount
   584→
   585→	// Corrupt shadow branch by pointing it at ZeroHash
   586→	shadowBranch := getShadowBranchNameForCommit(state.BaseCommit, state.WorktreeID)
   587→	corruptRef := plumbing.NewHashReference(plumbing.NewBranchReferenceName(shadowBranch), plumbing.ZeroHash)
   588→	require.NoError(t, repo.Storer.SetReference(corruptRef))
   589→
   590→	// Create a commit with the checkpoint trailer
   591→	commitWithCheckpointTrailer(t, repo, dir, "e5f6a1b2c3d5")
   592→
   593→	// Run PostCommit
   594→	err = s.PostCommit()
   595→	require.NoError(t, err, "PostCommit should not return error even when condensation fails")
   596→
   597→	// Verify BaseCommit was NOT updated (condensation failed)
   598→	state, err = s.loadSessionState(sessionID)
   599→	require.NoError(t, err)
   600→	assert.Equal(t, originalBaseCommit, state.BaseCommit,
   601→		"BaseCommit should NOT be updated when condensation fails for ENDED session")
   602→	assert.Equal(t, originalStepCount, state.StepCount,
   603→		"StepCount should NOT be reset when condensation fails for ENDED session")
   604→
   605→	// Verify entire/checkpoints/v1 branch does NOT exist (condensation failed)
   606→	_, err = repo.Reference(plumbing.NewBranchReferenceName(paths.MetadataBranchName), true)
   607→	require.Error(t, err,
   608→		"entire/checkpoints/v1 branch should NOT exist when condensation fails")
   609→
   610→	// Phase stays ENDED
   611→	assert.Equal(t, session.PhaseEnded, state.Phase,
   612→		"ENDED session should stay ENDED when condensation fails")
   613→}
   614→
   615→// TestTurnEnd_Active_NoActions verifies that HandleTurnEnd with no actions
   616→// is a no-op (normal ACTIVE → IDLE transition has no strategy-specific actions).
   617→func TestTurnEnd_Active_NoActions(t *testing.T) {
   618→	dir := setupGitRepo(t)
   619→	t.Chdir(dir)
   620→
   621→	repo, err := git.PlainOpen(dir)
   622→	require.NoError(t, err)
   623→
   624→	s := &ManualCommitStrategy{}
   625→	sessionID := "test-turnend-no-actions"
   626→
   627→	// Initialize session and save a checkpoint
   628→	setupSessionWithCheckpoint(t, s, repo, dir, sessionID)
   629→
   630→	// Set phase to ACTIVE (normal turn, no commit during turn)
   631→	state, err := s.loadSessionState(sessionID)
   632→	require.NoError(t, err)
   633→	state.Phase = session.PhaseActive
   634→	require.NoError(t, s.saveSessionState(state))
   635→
   636→	originalBaseCommit := state.BaseCommit
   637→	originalStepCount := state.StepCount
   638→
   639→	// ACTIVE + TurnEnd → IDLE with no strategy-specific actions
   640→	result := session.Transition(state.Phase, session.EventTurnEnd, session.TransitionContext{})
   641→
   642→	// Apply transition with no-op handler (no strategy actions for ACTIVE → IDLE)
   643→	err = session.ApplyTransition(state, result, session.NoOpActionHandler{})
   644→	require.NoError(t, err)
   645→
   646→	// Call HandleTurnEnd — should be a no-op (no TurnCheckpointIDs)
   647→	err = s.HandleTurnEnd(state)
   648→	require.NoError(t, err)
   649→
   650→	// Verify state is unchanged
   651→	assert.Equal(t, originalBaseCommit, state.BaseCommit,
   652→		"BaseCommit should be unchanged for no-op turn end")
   653→	assert.Equal(t, originalStepCount, state.StepCount,
   654→		"StepCount should be unchanged for no-op turn end")
   655→
   656→	// Shadow branch should still exist (not cleaned up)
   657→	shadowBranch := getShadowBranchNameForCommit(originalBaseCommit, state.WorktreeID)
   658→	refName := plumbing.NewBranchReferenceName(shadowBranch)
   659→	_, err = repo.Reference(refName, true)
   660→	assert.NoError(t, err,
   661→		"shadow branch should still exist after no-op turn end")
   662→}
   663→
   664→// TestPostCommit_FilesTouched_ResetsAfterCondensation verifies that FilesTouched
   665→// is reset after condensation, so subsequent condensations only contain the files
   666→// touched since the last commit — not the accumulated history.
   667→func TestPostCommit_FilesTouched_ResetsAfterCondensation(t *testing.T) {
   668→	dir := setupGitRepo(t)
   669→	t.Chdir(dir)
   670→
   671→	repo, err := git.PlainOpen(dir)
   672→	require.NoError(t, err)
   673→
   674→	s := &ManualCommitStrategy{}
   675→	sessionID := "test-filestouched-reset"
   676→
   677→	// --- Round 1: Save checkpoint touching files A.txt and B.txt ---
   678→
   679→	metadataDir := ".entire/metadata/" + sessionID
   680→	metadataDirAbs := filepath.Join(dir, metadataDir)
   681→	require.NoError(t, os.MkdirAll(metadataDirAbs, 0o755))
   682→
   683→	transcript := `{"type":"human","message":{"content":"round 1 prompt"}}
   684→{"type":"assistant","message":{"content":"round 1 response"}}
   685→`
   686→	require.NoError(t, os.WriteFile(
   687→		filepath.Join(metadataDirAbs, paths.TranscriptFileName),
   688→		[]byte(transcript), 0o644))
   689→
   690→	// Create files A.txt and B.txt
   691→	require.NoError(t, os.WriteFile(filepath.Join(dir, "A.txt"), []byte("file A"), 0o644))
   692→	require.NoError(t, os.WriteFile(filepath.Join(dir, "B.txt"), []byte("file B"), 0o644))
   693→
   694→	err = s.SaveStep(StepContext{
   695→		SessionID:      sessionID,
   696→		ModifiedFiles:  []string{},
   697→		NewFiles:       []string{"A.txt", "B.txt"},
   698→		DeletedFiles:   []string{},
   699→		MetadataDir:    metadataDir,
   700→		MetadataDirAbs: metadataDirAbs,
   701→		CommitMessage:  "Checkpoint 1: files A and B",
   702→		AuthorName:     "Test",
   703→		AuthorEmail:    "test@test.com",
   704→	})
   705→	require.NoError(t, err)
   706→
   707→	// Set phase to IDLE so PostCommit triggers immediate condensation
   708→	state, err := s.loadSessionState(sessionID)
   709→	require.NoError(t, err)
   710→	state.Phase = session.PhaseIdle
   711→	require.NoError(t, s.saveSessionState(state))
   712→
   713→	// Verify FilesTouched has A.txt and B.txt before condensation
   714→	assert.ElementsMatch(t, []string{"A.txt", "B.txt"}, state.FilesTouched,
   715→		"FilesTouched should contain A.txt and B.txt before first condensation")
   716→
   717→	// --- Commit A.txt, B.txt and condense (round 1) ---
   718→	checkpointID1 := "a1a2a3a4a5a6"
   719→	commitFilesWithTrailer(t, repo, dir, checkpointID1, "A.txt", "B.txt")
   720→
   721→	err = s.PostCommit()
   722→	require.NoError(t, err)
   723→
   724→	// Verify condensation happened
   725→	_, err = repo.Reference(plumbing.NewBranchReferenceName(paths.MetadataBranchName), true)
   726→	require.NoError(t, err, "entire/checkpoints/v1 should exist after first condensation")
   727→
   728→	// Verify first condensation contains A.txt and B.txt
   729→	store := checkpoint.NewGitStore(repo)
   730→	cpID1 := id.MustCheckpointID(checkpointID1)
   731→	summary1, err := store.ReadCommitted(context.Background(), cpID1)
   732→	require.NoError(t, err)
   733→	require.NotNil(t, summary1)
   734→	assert.ElementsMatch(t, []string{"A.txt", "B.txt"}, summary1.FilesTouched,
   735→		"First condensation should contain A.txt and B.txt")
   736→
   737→	// Verify FilesTouched was reset after condensation
   738→	state, err = s.loadSessionState(sessionID)
   739→	require.NoError(t, err)
   740→	assert.Nil(t, state.FilesTouched,
   741→		"FilesTouched should be nil after condensation (all files were committed)")
   742→
   743→	// --- Round 2: Save checkpoint touching files C.txt and D.txt ---
   744→
   745→	// Append to transcript for round 2
   746→	transcript2 := `{"type":"human","message":{"content":"round 2 prompt"}}
   747→{"type":"assistant","message":{"content":"round 2 response"}}
   748→`
   749→	f, err := os.OpenFile(
   750→		filepath.Join(metadataDirAbs, paths.TranscriptFileName),
   751→		os.O_APPEND|os.O_WRONLY, 0o644)
   752→	require.NoError(t, err)
   753→	_, err = f.WriteString(transcript2)
   754→	require.NoError(t, err)
   755→	require.NoError(t, f.Close())
   756→
   757→	// Create files C.txt and D.txt
   758→	require.NoError(t, os.WriteFile(filepath.Join(dir, "C.txt"), []byte("file C"), 0o644))
   759→	require.NoError(t, os.WriteFile(filepath.Join(dir, "D.txt"), []byte("file D"), 0o644))
   760→
   761→	err = s.SaveStep(StepContext{
   762→		SessionID:      sessionID,
   763→		ModifiedFiles:  []string{},
   764→		NewFiles:       []string{"C.txt", "D.txt"},
   765→		DeletedFiles:   []string{},
   766→		MetadataDir:    metadataDir,
   767→		MetadataDirAbs: metadataDirAbs,
   768→		CommitMessage:  "Checkpoint 2: files C and D",
   769→		AuthorName:     "Test",
   770→		AuthorEmail:    "test@test.com",
   771→	})
   772→	require.NoError(t, err)
   773→
   774→	// Set phase to IDLE for immediate condensation
   775→	state, err = s.loadSessionState(sessionID)
   776→	require.NoError(t, err)
   777→	state.Phase = session.PhaseIdle
   778→	require.NoError(t, s.saveSessionState(state))
   779→
   780→	// Verify FilesTouched only has C.txt and D.txt (NOT A.txt, B.txt)
   781→	assert.ElementsMatch(t, []string{"C.txt", "D.txt"}, state.FilesTouched,
   782→		"FilesTouched should only contain C.txt and D.txt after reset")
   783→
   784→	// --- Commit C.txt, D.txt and condense (round 2) ---
   785→	checkpointID2 := "b1b2b3b4b5b6"
   786→	commitFilesWithTrailer(t, repo, dir, checkpointID2, "C.txt", "D.txt")
   787→
   788→	err = s.PostCommit()
   789→	require.NoError(t, err)
   790→
   791→	// Verify second condensation contains ONLY C.txt and D.txt
   792→	cpID2 := id.MustCheckpointID(checkpointID2)
   793→	summary2, err := store.ReadCommitted(context.Background(), cpID2)
   794→	require.NoError(t, err)
   795→	require.NotNil(t, summary2, "Second condensation should exist")
   796→	assert.ElementsMatch(t, []string{"C.txt", "D.txt"}, summary2.FilesTouched,
   797→		"Second condensation should only contain C.txt and D.txt, not accumulated files from first condensation")
   798→}
   799→
   800→// TestSubtractFiles verifies that subtractFiles correctly removes files present
   801→// in the exclude set and preserves files not in it.
   802→func TestSubtractFiles(t *testing.T) {
   803→	t.Parallel()
   804→
   805→	tests := []struct {
   806→		name     string
   807→		files    []string
   808→		exclude  map[string]struct{}
   809→		expected []string
   810→	}{
   811→		{
   812→			name:     "no overlap",
   813→			files:    []string{"a.txt", "b.txt"},
   814→			exclude:  map[string]struct{}{"c.txt": {}},
   815→			expected: []string{"a.txt", "b.txt"},
   816→		},
   817→		{
   818→			name:     "full overlap",
   819→			files:    []string{"a.txt", "b.txt"},
   820→			exclude:  map[string]struct{}{"a.txt": {}, "b.txt": {}},
   821→			expected: nil,
   822→		},
   823→		{
   824→			name:     "partial overlap",
   825→			files:    []string{"a.txt", "b.txt", "c.txt"},
   826→			exclude:  map[string]struct{}{"b.txt": {}},
   827→			expected: []string{"a.txt", "c.txt"},
   828→		},
   829→		{
   830→			name:     "empty files",
   831→			files:    []string{},
   832→			exclude:  map[string]struct{}{"a.txt": {}},
   833→			expected: nil,
   834→		},
   835→		{
   836→			name:     "empty exclude",
   837→			files:    []string{"a.txt", "b.txt"},
   838→			exclude:  map[string]struct{}{},
   839→			expected: []string{"a.txt", "b.txt"},
   840→		},
   841→	}
   842→
   843→	for _, tt := range tests {
   844→		t.Run(tt.name, func(t *testing.T) {
   845→			t.Parallel()
   846→			result := subtractFiles(tt.files, tt.exclude)
   847→			assert.Equal(t, tt.expected, result)
   848→		})
   849→	}
   850→}
   851→
   852→// TestFilesChangedInCommit verifies that filesChangedInCommit correctly extracts
   853→// the set of files changed in a commit by diffing against its parent.
   854→func TestFilesChangedInCommit(t *testing.T) {
   855→	dir := setupGitRepo(t)
   856→	t.Chdir(dir)
   857→
   858→	repo, err := git.PlainOpen(dir)
   859→	require.NoError(t, err)
   860→
   861→	wt, err := repo.Worktree()
   862→	require.NoError(t, err)
   863→
   864→	// Create files and commit them
   865→	require.NoError(t, os.WriteFile(filepath.Join(dir, "file1.txt"), []byte("content1"), 0o644))
   866→	require.NoError(t, os.WriteFile(filepath.Join(dir, "file2.txt"), []byte("content2"), 0o644))
   867→	_, err = wt.Add("file1.txt")
   868→	require.NoError(t, err)
   869→	_, err = wt.Add("file2.txt")
   870→	require.NoError(t, err)
   871→
   872→	commitHash, err := wt.Commit("add files", &git.CommitOptions{
   873→		Author: &object.Signature{Name: "Test", Email: "test@test.com", When: time.Now()},
   874→	})
   875→	require.NoError(t, err)
   876→
   877→	commit, err := repo.CommitObject(commitHash)
   878→	require.NoError(t, err)
   879→
   880→	changed := filesChangedInCommit(commit)
   881→	assert.Contains(t, changed, "file1.txt")
   882→	assert.Contains(t, changed, "file2.txt")
   883→	// test.txt was in the initial commit, not this one
   884→	assert.NotContains(t, changed, "test.txt")
   885→}
   886→
   887→// TestFilesChangedInCommit_InitialCommit verifies that filesChangedInCommit
   888→// handles the initial commit (no parent) by listing all files.
   889→func TestFilesChangedInCommit_InitialCommit(t *testing.T) {
   890→	dir := t.TempDir()
   891→	t.Chdir(dir)
   892→
   893→	repo, err := git.PlainInit(dir, false)
   894→	require.NoError(t, err)
   895→
   896→	cfg, err := repo.Config()
   897→	require.NoError(t, err)
   898→	cfg.User.Name = "Test"
   899→	cfg.User.Email = "test@test.com"
   900→	require.NoError(t, repo.SetConfig(cfg))
   901→
   902→	wt, err := repo.Worktree()
   903→	require.NoError(t, err)
   904→
   905→	require.NoError(t, os.WriteFile(filepath.Join(dir, "init.txt"), []byte("initial"), 0o644))
   906→	_, err = wt.Add("init.txt")
   907→	require.NoError(t, err)
   908→
   909→	commitHash, err := wt.Commit("initial", &git.CommitOptions{
   910→		Author: &object.Signature{Name: "Test", Email: "test@test.com", When: time.Now()},
   911→	})
   912→	require.NoError(t, err)
   913→
   914→	commit, err := repo.CommitObject(commitHash)
   915→	require.NoError(t, err)
   916→
   917→	changed := filesChangedInCommit(commit)
   918→	assert.Contains(t, changed, "init.txt")
   919→	assert.Len(t, changed, 1)
   920→}
   921→
   922→// TestPostCommit_ActiveSession_CarryForward_PartialCommit verifies that when an
   923→// ACTIVE session has touched files A, B, C but only A and B are committed, the
   924→// remaining file C is carried forward to a new shadow branch.
   925→func TestPostCommit_ActiveSession_CarryForward_PartialCommit(t *testing.T) {
   926→	dir := setupGitRepo(t)
   927→	t.Chdir(dir)
   928→
   929→	repo, err := git.PlainOpen(dir)
   930→	require.NoError(t, err)
   931→
   932→	s := &ManualCommitStrategy{}
   933→	sessionID := "test-carry-forward-partial"
   934→
   935→	// Create metadata directory with transcript
   936→	metadataDir := ".entire/metadata/" + sessionID
   937→	metadataDirAbs := filepath.Join(dir, metadataDir)
   938→	require.NoError(t, os.MkdirAll(metadataDirAbs, 0o755))
   939→
   940→	transcript := `{"type":"human","message":{"content":"create files A B C"}}
   941→{"type":"assistant","message":{"content":"creating files"}}
   942→`
   943→	require.NoError(t, os.WriteFile(
   944→		filepath.Join(metadataDirAbs, paths.TranscriptFileName),
   945→		[]byte(transcript), 0o644))
   946→
   947→	// Create all three files
   948→	require.NoError(t, os.WriteFile(filepath.Join(dir, "A.txt"), []byte("file A"), 0o644))
   949→	require.NoError(t, os.WriteFile(filepath.Join(dir, "B.txt"), []byte("file B"), 0o644))
   950→	require.NoError(t, os.WriteFile(filepath.Join(dir, "C.txt"), []byte("file C"), 0o644))
   951→
   952→	// Save checkpoint with all three files
   953→	err = s.SaveStep(StepContext{
   954→		SessionID:      sessionID,
   955→		ModifiedFiles:  []string{},
   956→		NewFiles:       []string{"A.txt", "B.txt", "C.txt"},
   957→		DeletedFiles:   []string{},
   958→		MetadataDir:    metadataDir,
   959→		MetadataDirAbs: metadataDirAbs,
   960→		CommitMessage:  "Checkpoint: files A, B, C",
   961→		AuthorName:     "Test",
   962→		AuthorEmail:    "test@test.com",
   963→	})
   964→	require.NoError(t, err)
   965→
   966→	// Set phase to ACTIVE (agent mid-turn)
   967→	state, err := s.loadSessionState(sessionID)
   968→	require.NoError(t, err)
   969→	state.Phase = session.PhaseActive
   970→	require.NoError(t, s.saveSessionState(state))
   971→
   972→	// Verify FilesTouched contains all three files
   973→	assert.ElementsMatch(t, []string{"A.txt", "B.txt", "C.txt"}, state.FilesTouched)
   974→
   975→	// Commit ONLY A.txt and B.txt (not C.txt) with checkpoint trailer
   976→	wt, err := repo.Worktree()
   977→	require.NoError(t, err)
   978→	_, err = wt.Add("A.txt")
   979→	require.NoError(t, err)
   980→	_, err = wt.Add("B.txt")
   981→	require.NoError(t, err)
   982→
   983→	cpID := "cf1cf2cf3cf4"
   984→	commitMsg := "commit A and B\n\n" + trailers.CheckpointTrailerKey + ": " + cpID + "\n"
   985→	_, err = wt.Commit(commitMsg, &git.CommitOptions{
   986→		Author: &object.Signature{Name: "Test", Email: "test@test.com", When: time.Now()},
   987→	})
   988→	require.NoError(t, err)
   989→
   990→	// Run PostCommit
   991→	err = s.PostCommit()
   992→	require.NoError(t, err)
   993→
   994→	// Verify session stayed ACTIVE
   995→	state, err = s.loadSessionState(sessionID)
   996→	require.NoError(t, err)
   997→	assert.Equal(t, session.PhaseActive, state.Phase)
   998→
   999→	// Verify carry-forward: FilesTouched should now only contain C.txt
  1000→	assert.Equal(t, []string{"C.txt"}, state.FilesTouched,
  1001→		"carry-forward should preserve only the uncommitted file C.txt")
  1002→
  1003→	// Verify StepCount was set to 1 (carry-forward creates a new checkpoint)
  1004→	assert.Equal(t, 1, state.StepCount,
  1005→		"carry-forward should set StepCount to 1")
  1006→
  1007→	// Verify CheckpointTranscriptStart was reset to 0 (prompt-level carry-forward)
  1008→	assert.Equal(t, 0, state.CheckpointTranscriptStart,
  1009→		"carry-forward should reset CheckpointTranscriptStart to 0 for full transcript reprocessing")
  1010→
  1011→	// Verify LastCheckpointID was cleared (next commit generates fresh ID)
  1012→	assert.Empty(t, state.LastCheckpointID,
  1013→		"carry-forward should clear LastCheckpointID")
  1014→
  1015→	// Verify a new shadow branch exists at the new HEAD
  1016→	newShadowBranch := getShadowBranchNameForCommit(state.BaseCommit, state.WorktreeID)
  1017→	_, err = repo.Reference(plumbing.NewBranchReferenceName(newShadowBranch), true)
  1018→	assert.NoError(t, err,
  1019→		"carry-forward should create a new shadow branch at the new HEAD")
  1020→}
  1021→
  1022→// TestPostCommit_ActiveSession_CarryForward_AllCommitted verifies that when an
  1023→// ACTIVE session's files are ALL included in the commit, no carry-forward occurs.
  1024→func TestPostCommit_ActiveSession_CarryForward_AllCommitted(t *testing.T) {
  1025→	dir := setupGitRepo(t)
  1026→	t.Chdir(dir)
  1027→
  1028→	repo, err := git.PlainOpen(dir)
  1029→	require.NoError(t, err)
  1030→
  1031→	s := &ManualCommitStrategy{}
  1032→	sessionID := "test-carry-forward-all"
  1033→
  1034→	// Initialize session and save a checkpoint with files A and B
  1035→	metadataDir := ".entire/metadata/" + sessionID
  1036→	metadataDirAbs := filepath.Join(dir, metadataDir)
  1037→	require.NoError(t, os.MkdirAll(metadataDirAbs, 0o755))
  1038→
  1039→	transcript := `{"type":"human","message":{"content":"create files A B"}}
  1040→{"type":"assistant","message":{"content":"creating files"}}
  1041→`
  1042→	require.NoError(t, os.WriteFile(
  1043→		filepath.Join(metadataDirAbs, paths.TranscriptFileName),
  1044→		[]byte(transcript), 0o644))
  1045→
  1046→	require.NoError(t, os.WriteFile(filepath.Join(dir, "A.txt"), []byte("file A"), 0o644))
  1047→	require.NoError(t, os.WriteFile(filepath.Join(dir, "B.txt"), []byte("file B"), 0o644))
  1048→
  1049→	err = s.SaveStep(StepContext{
  1050→		SessionID:      sessionID,
  1051→		ModifiedFiles:  []string{},
  1052→		NewFiles:       []string{"A.txt", "B.txt"},
  1053→		DeletedFiles:   []string{},
  1054→		MetadataDir:    metadataDir,
  1055→		MetadataDirAbs: metadataDirAbs,
  1056→		CommitMessage:  "Checkpoint: files A, B",
  1057→		AuthorName:     "Test",
  1058→		AuthorEmail:    "test@test.com",
  1059→	})
  1060→	require.NoError(t, err)
  1061→
  1062→	// Set phase to ACTIVE
  1063→	state, err := s.loadSessionState(sessionID)
  1064→	require.NoError(t, err)
  1065→	state.Phase = session.PhaseActive
  1066→	require.NoError(t, s.saveSessionState(state))
  1067→
  1068→	// Commit ALL files (A.txt and B.txt) with checkpoint trailer
  1069→	wt, err := repo.Worktree()
  1070→	require.NoError(t, err)
  1071→	_, err = wt.Add("A.txt")
  1072→	require.NoError(t, err)
  1073→	_, err = wt.Add("B.txt")
  1074→	require.NoError(t, err)
  1075→
  1076→	cpID := "cf5cf6cf7cf8"
  1077→	commitMsg := "commit A and B\n\n" + trailers.CheckpointTrailerKey + ": " + cpID + "\n"
  1078→	_, err = wt.Commit(commitMsg, &git.CommitOptions{
  1079→		Author: &object.Signature{Name: "Test", Email: "test@test.com", When: time.Now()},
  1080→	})
  1081→	require.NoError(t, err)
  1082→
  1083→	// Run PostCommit
  1084→	err = s.PostCommit()
  1085→	require.NoError(t, err)
  1086→
  1087→	// Verify session stayed ACTIVE
  1088→	state, err = s.loadSessionState(sessionID)
  1089→	require.NoError(t, err)
  1090→	assert.Equal(t, session.PhaseActive, state.Phase)
  1091→
  1092→	// Verify NO carry-forward: FilesTouched should be nil (all condensed, nothing remaining)
  1093→	assert.Nil(t, state.FilesTouched,
  1094→		"when all files are committed, no carry-forward should occur (FilesTouched cleared by condensation)")
  1095→
  1096→	// Verify StepCount was reset to 0 by condensation (not 1 from carry-forward)
  1097→	assert.Equal(t, 0, state.StepCount,
  1098→		"without carry-forward, StepCount should be reset to 0 by condensation")
  1099→}
  1100→
  1101→// TestPostCommit_ActiveSession_RecordsTurnCheckpointIDs verifies that PostCommit
  1102→// records the checkpoint ID in TurnCheckpointIDs for ACTIVE sessions.
  1103→// This enables HandleTurnEnd to finalize all checkpoints with the full transcript.
  1104→func TestPostCommit_ActiveSession_RecordsTurnCheckpointIDs(t *testing.T) {
  1105→	dir := setupGitRepo(t)
  1106→	t.Chdir(dir)
  1107→
  1108→	repo, err := git.PlainOpen(dir)
  1109→	require.NoError(t, err)
  1110→
  1111→	s := &ManualCommitStrategy{}
  1112→	sessionID := "test-turn-checkpoint-ids"
  1113→
  1114→	setupSessionWithCheckpoint(t, s, repo, dir, sessionID)
  1115→
  1116→	// Set phase to ACTIVE (simulating agent mid-turn)
  1117→	state, err := s.loadSessionState(sessionID)
  1118→	require.NoError(t, err)
  1119→	state.Phase = session.PhaseActive
  1120→	state.TurnCheckpointIDs = nil // Start clean
  1121→	require.NoError(t, s.saveSessionState(state))
  1122→
  1123→	// Create first commit with checkpoint trailer
  1124→	commitWithCheckpointTrailer(t, repo, dir, "a1b2c3d4e5f6")
  1125→
  1126→	err = s.PostCommit()
  1127→	require.NoError(t, err)
  1128→
  1129→	// Verify TurnCheckpointIDs was populated
  1130→	state, err = s.loadSessionState(sessionID)
  1131→	require.NoError(t, err)
  1132→	assert.Equal(t, []string{"a1b2c3d4e5f6"}, state.TurnCheckpointIDs,
  1133→		"TurnCheckpointIDs should contain the checkpoint ID after condensation")
  1134→}
  1135→
  1136→// TestPostCommit_IdleSession_DoesNotRecordTurnCheckpointIDs verifies that PostCommit
  1137→// does NOT record TurnCheckpointIDs for IDLE sessions.
  1138→func TestPostCommit_IdleSession_DoesNotRecordTurnCheckpointIDs(t *testing.T) {
  1139→	dir := setupGitRepo(t)
  1140→	t.Chdir(dir)
  1141→
  1142→	repo, err := git.PlainOpen(dir)
  1143→	require.NoError(t, err)
  1144→
  1145→	s := &ManualCommitStrategy{}
  1146→	sessionID := "test-idle-no-turn-ids"
  1147→
  1148→	setupSessionWithCheckpoint(t, s, repo, dir, sessionID)
  1149→
  1150→	// Set phase to IDLE with files touched so overlap check passes
  1151→	state, err := s.loadSessionState(sessionID)
  1152→	require.NoError(t, err)
  1153→	state.Phase = session.PhaseIdle
  1154→	state.FilesTouched = []string{"test.txt"}
  1155→	require.NoError(t, s.saveSessionState(state))
  1156→
  1157→	commitWithCheckpointTrailer(t, repo, dir, "c3d4e5f6a1b2")
  1158→
  1159→	err = s.PostCommit()
  1160→	require.NoError(t, err)
  1161→
  1162→	// Verify TurnCheckpointIDs was NOT set (IDLE sessions don't need finalization)
  1163→	state, err = s.loadSessionState(sessionID)
  1164→	require.NoError(t, err)
  1165→	assert.Empty(t, state.TurnCheckpointIDs,
  1166→		"TurnCheckpointIDs should not be populated for IDLE sessions")
  1167→}
  1168→
  1169→// TestHandleTurnEnd_PartialFailure verifies that HandleTurnEnd continues
  1170→// processing remaining checkpoints when one UpdateCommitted call fails.
  1171→// This locks the best-effort behavior: valid checkpoints get finalized even
  1172→// when one checkpoint ID is invalid or missing from entire/checkpoints/v1.
  1173→func TestHandleTurnEnd_PartialFailure(t *testing.T) {
  1174→	dir := setupGitRepo(t)
  1175→	t.Chdir(dir)
  1176→
  1177→	repo, err := git.PlainOpen(dir)
  1178→	require.NoError(t, err)
  1179→
  1180→	s := &ManualCommitStrategy{}
  1181→	sessionID := "test-partial-failure"
  1182→
  1183→	setupSessionWithCheckpoint(t, s, repo, dir, sessionID)
  1184→
  1185→	// Set phase to ACTIVE and create a transcript file with updated content
  1186→	state, err := s.loadSessionState(sessionID)
  1187→	require.NoError(t, err)
  1188→	state.Phase = session.PhaseActive
  1189→	state.TurnCheckpointIDs = nil
  1190→	require.NoError(t, s.saveSessionState(state))
  1191→
  1192→	// First commit → creates real checkpoint on entire/checkpoints/v1
  1193→	commitWithCheckpointTrailer(t, repo, dir, "a1b2c3d4e5f6")
  1194→	require.NoError(t, s.PostCommit())
  1195→
  1196→	// Write new content and create a second checkpoint on the shadow branch.
  1197→	// Use SaveStep directly (instead of setupSessionWithCheckpoint) so that
  1198→	// second.txt is included in FilesTouched — the overlap check needs it.
  1199→	require.NoError(t, os.WriteFile(filepath.Join(dir, "second.txt"), []byte("second file"), 0o644))
  1200→	metadataDir := ".entire/metadata/" + sessionID
  1201→	metadataDirAbs := filepath.Join(dir, metadataDir)
  1202→	err = s.SaveStep(StepContext{
  1203→		SessionID:      sessionID,
  1204→		ModifiedFiles:  []string{"test.txt"},
  1205→		NewFiles:       []string{"second.txt"},
  1206→		DeletedFiles:   []string{},
  1207→		MetadataDir:    metadataDir,
  1208→		MetadataDirAbs: metadataDirAbs,
  1209→		CommitMessage:  "Checkpoint 2",
  1210→		AuthorName:     "Test",
  1211→		AuthorEmail:    "test@test.com",
  1212→	})
  1213→	require.NoError(t, err, "SaveStep should succeed for second checkpoint")
  1214→	state, err = s.loadSessionState(sessionID)
  1215→	require.NoError(t, err)
  1216→	state.Phase = session.PhaseActive
  1217→	// Preserve TurnCheckpointIDs from the first commit
  1218→	state.TurnCheckpointIDs = []string{"a1b2c3d4e5f6"}
  1219→	require.NoError(t, s.saveSessionState(state))
  1220→
  1221→	commitFilesWithTrailer(t, repo, dir, "b2c3d4e5f6a1", "second.txt")
  1222→	require.NoError(t, s.PostCommit())
  1223→
  1224→	// Verify we now have 2 real checkpoint IDs
  1225→	state, err = s.loadSessionState(sessionID)
  1226→	require.NoError(t, err)
  1227→	require.Len(t, state.TurnCheckpointIDs, 2,
  1228→		"Should have 2 real checkpoint IDs after 2 mid-turn commits")
  1229→
  1230→	// Inject a fake 3rd checkpoint ID that doesn't exist on entire/checkpoints/v1
  1231→	state.TurnCheckpointIDs = append(state.TurnCheckpointIDs, "ffffffffffff")
  1232→
  1233→	// Write a full transcript file for HandleTurnEnd to read
  1234→	fullTranscript := `{"type":"human","message":{"content":"build something"}}
  1235→{"type":"assistant","message":{"content":"done building"}}
  1236→{"type":"human","message":{"content":"now test it"}}
  1237→{"type":"assistant","message":{"content":"tests pass"}}
  1238→`
  1239→	transcriptPath := filepath.Join(dir, ".entire", "metadata", sessionID, "full_transcript.jsonl")
  1240→	require.NoError(t, os.MkdirAll(filepath.Dir(transcriptPath), 0o755))
  1241→	require.NoError(t, os.WriteFile(transcriptPath, []byte(fullTranscript), 0o644))
  1242→	state.TranscriptPath = transcriptPath
  1243→	require.NoError(t, s.saveSessionState(state))
  1244→
  1245→	// Call HandleTurnEnd — should NOT return error (best-effort)
  1246→	err = s.HandleTurnEnd(state)
  1247→	require.NoError(t, err,
  1248→		"HandleTurnEnd should return nil even with partial failures (best-effort)")
  1249→
  1250→	// TurnCheckpointIDs should be cleared regardless of partial failure
  1251→	assert.Empty(t, state.TurnCheckpointIDs,
  1252→		"TurnCheckpointIDs should be cleared after HandleTurnEnd, even with errors")
  1253→
  1254→	// Verify the 2 valid checkpoints were finalized with the full transcript
  1255→	store := checkpoint.NewGitStore(repo)
  1256→	for _, cpIDStr := range []string{"a1b2c3d4e5f6", "b2c3d4e5f6a1"} {
  1257→		cpID := id.MustCheckpointID(cpIDStr)
  1258→		content, readErr := store.ReadSessionContent(context.Background(), cpID, 0)
  1259→		require.NoError(t, readErr,
  1260→			"Should be able to read finalized checkpoint %s", cpIDStr)
  1261→		assert.Contains(t, string(content.Transcript), "now test it",
  1262→			"Checkpoint %s should contain the full transcript (including later messages)", cpIDStr)
  1263→	}
  1264→}
  1265→
  1266→// setupSessionWithCheckpoint initializes a session and creates one checkpoint
  1267→// on the shadow branch so there is content available for condensation.
  1268→// Also modifies test.txt to "agent modified content" and includes it in the checkpoint,
  1269→// so content-aware carry-forward comparisons work correctly when commitFilesWithTrailer
  1270→// commits the same content.
  1271→func setupSessionWithCheckpoint(t *testing.T, s *ManualCommitStrategy, _ *git.Repository, dir, sessionID string) {
  1272→	t.Helper()
  1273→
  1274→	// Modify test.txt with agent content (same content that commitFilesWithTrailer will commit)
  1275→	testFile := filepath.Join(dir, "test.txt")
  1276→	require.NoError(t, os.WriteFile(testFile, []byte("agent modified content"), 0o644))
  1277→
  1278→	// Create metadata directory with a transcript file
  1279→	metadataDir := ".entire/metadata/" + sessionID
  1280→	metadataDirAbs := filepath.Join(dir, metadataDir)
  1281→	require.NoError(t, os.MkdirAll(metadataDirAbs, 0o755))
  1282→
  1283→	transcript := `{"type":"human","message":{"content":"test prompt"}}
  1284→{"type":"assistant","message":{"content":"test response"}}
  1285→`
  1286→	require.NoError(t, os.WriteFile(
  1287→		filepath.Join(metadataDirAbs, paths.TranscriptFileName),
  1288→		[]byte(transcript), 0o644))
  1289→
  1290→	// SaveStep creates the shadow branch and checkpoint
  1291→	// Include test.txt as a modified file so it's saved to the shadow branch
  1292→	err := s.SaveStep(StepContext{
  1293→		SessionID:      sessionID,
  1294→		ModifiedFiles:  []string{"test.txt"},
  1295→		NewFiles:       []string{},
  1296→		DeletedFiles:   []string{},
  1297→		MetadataDir:    metadataDir,
  1298→		MetadataDirAbs: metadataDirAbs,
  1299→		CommitMessage:  "Checkpoint 1",
  1300→		AuthorName:     "Test",
  1301→		AuthorEmail:    "test@test.com",
  1302→	})
  1303→	require.NoError(t, err, "SaveStep should succeed to create shadow branch content")
  1304→}
  1305→
  1306→// commitWithCheckpointTrailer creates a commit on the current branch with the
  1307→// Entire-Checkpoint trailer in the commit message. This simulates what happens
  1308→// after PrepareCommitMsg adds the trailer and the user completes the commit.
  1309→func commitWithCheckpointTrailer(t *testing.T, repo *git.Repository, dir, checkpointIDStr string) {
  1310→	t.Helper()
  1311→	commitFilesWithTrailer(t, repo, dir, checkpointIDStr, "test.txt")
  1312→}
  1313→
  1314→// commitFilesWithTrailer stages the given files and commits with a checkpoint trailer.
  1315→// Files must already exist on disk. The test.txt file is modified to ensure there's always something to commit.
  1316→// Important: For tests using content-aware carry-forward, call setupSessionWithCheckpointAndFile first
  1317→// so the shadow branch has the same content that will be committed.
  1318→func commitFilesWithTrailer(t *testing.T, repo *git.Repository, dir, checkpointIDStr string, files ...string) {
  1319→	t.Helper()
  1320→
  1321→	cpID := id.MustCheckpointID(checkpointIDStr)
  1322→
  1323→	// Modify test.txt with agent-like content that matches what setupSessionWithCheckpointAndFile saves
  1324→	testFile := filepath.Join(dir, "test.txt")
  1325→	content := "agent modified content"
  1326→	require.NoError(t, os.WriteFile(testFile, []byte(content), 0o644))
  1327→
  1328→	wt, err := repo.Worktree()
  1329→	require.NoError(t, err)
  1330→
  1331→	_, err = wt.Add("test.txt")
  1332→	require.NoError(t, err)
  1333→	for _, f := range files {
  1334→		_, err = wt.Add(f)
  1335→		require.NoError(t, err)
  1336→	}
  1337→
  1338→	commitMsg := "test commit\n\n" + trailers.CheckpointTrailerKey + ": " + cpID.String() + "\n"
  1339→	_, err = wt.Commit(commitMsg, &git.CommitOptions{
  1340→		Author: &object.Signature{
  1341→			Name:  "Test",
  1342→			Email: "test@test.com",
  1343→			When:  time.Now(),
  1344→		},
  1345→	})
  1346→	require.NoError(t, err, "commit with checkpoint trailer should succeed")
  1347→}
  1348→
  1349→// TestPostCommit_OldIdleSession_BaseCommitNotUpdated verifies that when an IDLE
  1350→// session from a previous commit exists, and a NEW session makes a commit, the
  1351→// old IDLE session's BaseCommit is NOT updated to the new HEAD.
  1352→//
  1353→// This is a regression test for the bug where old sessions (IDLE/ENDED) would
  1354→// have their BaseCommit updated, causing them to be incorrectly condensed on
  1355→// future commits because their BaseCommit matched the new shadow branch.
  1356→func TestPostCommit_OldIdleSession_BaseCommitNotUpdated(t *testing.T) {
  1357→	dir := setupGitRepo(t)
  1358→	t.Chdir(dir)
  1359→
  1360→	repo, err := git.PlainOpen(dir)
  1361→	require.NoError(t, err)
  1362→
  1363→	s := &ManualCommitStrategy{}
  1364→
  1365→	// --- Create an old IDLE session from a previous commit ---
  1366→	oldSessionID := "old-idle-session"
  1367→	setupSessionWithCheckpoint(t, s, repo, dir, oldSessionID)
  1368→
  1369→	oldState, err := s.loadSessionState(oldSessionID)
  1370→	require.NoError(t, err)
  1371→	oldState.Phase = session.PhaseIdle
  1372→	oldState.FilesTouched = []string{"old-file.txt"} // Has files touched (important for bug)
  1373→	require.NoError(t, s.saveSessionState(oldState))
  1374→
  1375→	// Record the old session's BaseCommit BEFORE the new commit
  1376→	oldSessionOriginalBaseCommit := oldState.BaseCommit
  1377→
  1378→	// Create a commit to move HEAD forward (simulating old session was condensed)
  1379→	wt, err := repo.Worktree()
  1380→	require.NoError(t, err)
  1381→	require.NoError(t, os.WriteFile(filepath.Join(dir, "unrelated.txt"), []byte("unrelated"), 0o644))
  1382→	_, err = wt.Add("unrelated.txt")
  1383→	require.NoError(t, err)
  1384→	_, err = wt.Commit("unrelated commit without trailer", &git.CommitOptions{
  1385→		Author: &object.Signature{Name: "Test", Email: "test@test.com", When: time.Now()},
  1386→	})
  1387→	require.NoError(t, err)
  1388→
  1389→	// --- Create a NEW ACTIVE session at the new HEAD ---
  1390→	newSessionID := testNewActiveSessionID
  1391→	setupSessionWithCheckpoint(t, s, repo, dir, newSessionID)
  1392→
  1393→	newState, err := s.loadSessionState(newSessionID)
  1394→	require.NoError(t, err)
  1395→	newState.Phase = session.PhaseActive
  1396→	require.NoError(t, s.saveSessionState(newState))
  1397→
  1398→	// --- Commit from the new session ---
  1399→	commitWithCheckpointTrailer(t, repo, dir, "a1b2c3d4e5f6")
  1400→
  1401→	// Get new HEAD for comparison
  1402→	head, err := repo.Head()
  1403→	require.NoError(t, err)
  1404→	newHead := head.Hash().String()
  1405→
  1406→	// Run PostCommit
  1407→	err = s.PostCommit()
  1408→	require.NoError(t, err)
  1409→
  1410→	// --- Verify: old IDLE session's BaseCommit should NOT be updated ---
  1411→	oldState, err = s.loadSessionState(oldSessionID)
  1412→	require.NoError(t, err)
  1413→	assert.Equal(t, oldSessionOriginalBaseCommit, oldState.BaseCommit,
  1414→		"OLD IDLE session's BaseCommit should NOT be updated when a different session commits")
  1415→	assert.NotEqual(t, newHead, oldState.BaseCommit,
  1416→		"OLD IDLE session's BaseCommit should NOT match new HEAD")
  1417→
  1418→	// New ACTIVE session's BaseCommit SHOULD be updated (it was condensed)
  1419→	newState, err = s.loadSessionState(newSessionID)
  1420→	require.NoError(t, err)
  1421→	assert.Equal(t, newHead, newState.BaseCommit,
  1422→		"NEW ACTIVE session's BaseCommit should be updated after condensation")
  1423→}
  1424→
  1425→// TestPostCommit_OldEndedSession_BaseCommitNotUpdated verifies that when an ENDED
  1426→// session from a previous commit exists (with no new content to condense), and a
  1427→// NEW session makes a commit, the old ENDED session's BaseCommit is NOT updated.
  1428→//
  1429→// This simulates the scenario where:
  1430→// 1. Old session ran and was already condensed (no new transcript content)
  1431→// 2. Old session is now ENDED
  1432→// 3. New session commits
  1433→// 4. Old ENDED session should NOT have BaseCommit updated
  1434→func TestPostCommit_OldEndedSession_BaseCommitNotUpdated(t *testing.T) {
  1435→	dir := setupGitRepo(t)
  1436→	t.Chdir(dir)
  1437→
  1438→	repo, err := git.PlainOpen(dir)
  1439→	require.NoError(t, err)
  1440→
  1441→	s := &ManualCommitStrategy{}
  1442→
  1443→	// --- Create an old ENDED session that has NO new content to condense ---
  1444→	oldSessionID := "old-ended-session"
  1445→	setupSessionWithCheckpoint(t, s, repo, dir, oldSessionID)
  1446→
  1447→	oldState, err := s.loadSessionState(oldSessionID)
  1448→	require.NoError(t, err)
  1449→	now := time.Now()
  1450→	oldState.Phase = session.PhaseEnded
  1451→	oldState.EndedAt = &now
  1452→	oldState.FilesTouched = []string{"old-file.txt"} // Has files touched
  1453→	// Mark transcript as fully condensed (no new content since last checkpoint)
  1454→	// The transcript has 2 lines, so CheckpointTranscriptStart=2 means no new content
  1455→	oldState.CheckpointTranscriptStart = 2
  1456→	require.NoError(t, s.saveSessionState(oldState))
  1457→
  1458→	// Record the old session's BaseCommit BEFORE the new commit
  1459→	oldSessionOriginalBaseCommit := oldState.BaseCommit
  1460→
  1461→	// Create a commit to move HEAD forward
  1462→	wt, err := repo.Worktree()
  1463→	require.NoError(t, err)
  1464→	require.NoError(t, os.WriteFile(filepath.Join(dir, "unrelated.txt"), []byte("unrelated"), 0o644))
  1465→	_, err = wt.Add("unrelated.txt")
  1466→	require.NoError(t, err)
  1467→	_, err = wt.Commit("unrelated commit without trailer", &git.CommitOptions{
  1468→		Author: &object.Signature{Name: "Test", Email: "test@test.com", When: time.Now()},
  1469→	})
  1470→	require.NoError(t, err)
  1471→
  1472→	// --- Create a NEW ACTIVE session at the new HEAD ---
  1473→	newSessionID := testNewActiveSessionID
  1474→	setupSessionWithCheckpoint(t, s, repo, dir, newSessionID)
  1475→
  1476→	newState, err := s.loadSessionState(newSessionID)
  1477→	require.NoError(t, err)
  1478→	newState.Phase = session.PhaseActive
  1479→	require.NoError(t, s.saveSessionState(newState))
  1480→
  1481→	// --- Commit from the new session ---
  1482→	commitWithCheckpointTrailer(t, repo, dir, "b1c2d3e4f5a6")
  1483→
  1484→	// Get new HEAD for comparison
  1485→	head, err := repo.Head()
  1486→	require.NoError(t, err)
  1487→	newHead := head.Hash().String()
  1488→
  1489→	// Run PostCommit
  1490→	err = s.PostCommit()
  1491→	require.NoError(t, err)
  1492→
  1493→	// --- Verify: old ENDED session's BaseCommit should NOT be updated ---
  1494→	oldState, err = s.loadSessionState(oldSessionID)
  1495→	require.NoError(t, err)
  1496→	assert.Equal(t, oldSessionOriginalBaseCommit, oldState.BaseCommit,
  1497→		"OLD ENDED session's BaseCommit should NOT be updated when a different session commits")
  1498→	assert.NotEqual(t, newHead, oldState.BaseCommit,
  1499→		"OLD ENDED session's BaseCommit should NOT match new HEAD")
  1500→
  1501→	// New ACTIVE session's BaseCommit SHOULD be updated
  1502→	newState, err = s.loadSessionState(newSessionID)
  1503→	require.NoError(t, err)
  1504→	assert.Equal(t, newHead, newState.BaseCommit,
  1505→		"NEW ACTIVE session's BaseCommit should be updated after condensation")
  1506→}
  1507→
  1508→// TestPostCommit_EndedSessionCarryForward_NotCondensedIntoUnrelatedCommit verifies
  1509→// that an ENDED session with carry-forward files is NOT condensed into a commit
  1510→// that doesn't touch any of those files.
  1511→//
  1512→// This is the primary bug scenario: ENDED sessions go through HandleCondenseIfFilesTouched,
  1513→// which previously only checked len(FilesTouched) > 0 && hasNew — no overlap check.
  1514→// Carry-forward would set FilesTouched with remaining uncommitted files, and
  1515→// sessionHasNewContent returned true because the shadow branch had content. This
  1516→// caused ENDED sessions to be re-condensed into every subsequent commit indefinitely.
  1517→func TestPostCommit_EndedSessionCarryForward_NotCondensedIntoUnrelatedCommit(t *testing.T) {
  1518→	dir := setupGitRepo(t)
  1519→	t.Chdir(dir)
  1520→
  1521→	repo, err := git.PlainOpen(dir)
  1522→	require.NoError(t, err)
  1523→
  1524→	s := &ManualCommitStrategy{}
  1525→
  1526→	// --- Create an ENDED session with carry-forward files ---
  1527→	endedSessionID := "ended-carry-forward"
  1528→	setupSessionWithCheckpoint(t, s, repo, dir, endedSessionID)
  1529→
  1530→	endedState, err := s.loadSessionState(endedSessionID)
  1531→	require.NoError(t, err)
  1532→	now := time.Now()
  1533→	endedState.Phase = session.PhaseEnded
  1534→	endedState.EndedAt = &now
  1535→	// Simulate carry-forward: session touched test.txt but it wasn't fully committed yet.
  1536→	// CheckpointTranscriptStart=0 so sessionHasNewContent returns true (transcript grew).
  1537→	endedState.FilesTouched = []string{"test.txt"}
  1538→	endedState.CheckpointTranscriptStart = 0
  1539→	require.NoError(t, s.saveSessionState(endedState))
  1540→
  1541→	endedOriginalBaseCommit := endedState.BaseCommit
  1542→	endedOriginalStepCount := endedState.StepCount
  1543→
  1544→	// Move HEAD forward with an unrelated commit (no trailer)
  1545→	wt, err := repo.Worktree()
  1546→	require.NoError(t, err)
  1547→	require.NoError(t, os.WriteFile(filepath.Join(dir, "unrelated.txt"), []byte("unrelated work"), 0o644))
  1548→	_, err = wt.Add("unrelated.txt")
  1549→	require.NoError(t, err)
  1550→	_, err = wt.Commit("unrelated commit", &git.CommitOptions{
  1551→		Author: &object.Signature{Name: "Test", Email: "test@test.com", When: time.Now()},
  1552→	})
  1553→	require.NoError(t, err)
  1554→
  1555→	// --- Create a NEW ACTIVE session at the new HEAD ---
  1556→	newSessionID := testNewActiveSessionID
  1557→	require.NoError(t, os.WriteFile(filepath.Join(dir, "new-feature.txt"), []byte("new feature content"), 0o644))
  1558→
  1559→	metadataDir := ".entire/metadata/" + newSessionID
  1560→	metadataDirAbs := filepath.Join(dir, metadataDir)
  1561→	require.NoError(t, os.MkdirAll(metadataDirAbs, 0o755))
  1562→
  1563→	transcript := `{"type":"human","message":{"content":"add new feature"}}
  1564→{"type":"assistant","message":{"content":"adding new feature"}}
  1565→`
  1566→	require.NoError(t, os.WriteFile(
  1567→		filepath.Join(metadataDirAbs, paths.TranscriptFileName),
  1568→		[]byte(transcript), 0o644))
  1569→
  1570→	err = s.SaveStep(StepContext{
  1571→		SessionID:      newSessionID,
  1572→		ModifiedFiles:  []string{},
  1573→		NewFiles:       []string{"new-feature.txt"},
  1574→		DeletedFiles:   []string{},
  1575→		MetadataDir:    metadataDir,
  1576→		MetadataDirAbs: metadataDirAbs,
  1577→		CommitMessage:  "Checkpoint: new feature",
  1578→		AuthorName:     "Test",
  1579→		AuthorEmail:    "test@test.com",
  1580→	})
  1581→	require.NoError(t, err)
  1582→
  1583→	newState, err := s.loadSessionState(newSessionID)
  1584→	require.NoError(t, err)
  1585→	newState.Phase = session.PhaseActive
  1586→	require.NoError(t, s.saveSessionState(newState))
  1587→
  1588→	// --- Commit ONLY new-feature.txt (not test.txt) with checkpoint trailer ---
  1589→	wt, err = repo.Worktree()
  1590→	require.NoError(t, err)
  1591→	_, err = wt.Add("new-feature.txt")
  1592→	require.NoError(t, err)
  1593→
  1594→	cpID := "ae1ae2ae3ae4"
  1595→	commitMsg := "add new feature\n\n" + trailers.CheckpointTrailerKey + ": " + cpID + "\n"
  1596→	_, err = wt.Commit(commitMsg, &git.CommitOptions{
  1597→		Author: &object.Signature{Name: "Test", Email: "test@test.com", When: time.Now()},
  1598→	})
  1599→	require.NoError(t, err)
  1600→
  1601→	head, err := repo.Head()
  1602→	require.NoError(t, err)
  1603→	newHead := head.Hash().String()
  1604→
  1605→	// Run PostCommit
  1606→	err = s.PostCommit()
  1607→	require.NoError(t, err)
  1608→
  1609→	// --- Verify: ENDED session was NOT condensed ---
  1610→	endedState, err = s.loadSessionState(endedSessionID)
  1611→	require.NoError(t, err)
  1612→
  1613→	// StepCount should be unchanged (not reset by condensation)
  1614→	assert.Equal(t, endedOriginalStepCount, endedState.StepCount,
  1615→		"ENDED session StepCount should NOT be reset (no condensation)")
  1616→
  1617→	// BaseCommit should NOT be updated for ENDED sessions (PR #359)
  1618→	assert.Equal(t, endedOriginalBaseCommit, endedState.BaseCommit,
  1619→		"ENDED session BaseCommit should NOT be updated")
  1620→
  1621→	// FilesTouched should still have the carry-forward files (not cleared by condensation)
  1622→	assert.Equal(t, []string{"test.txt"}, endedState.FilesTouched,
  1623→		"ENDED session FilesTouched should be preserved (carry-forward files not consumed)")
  1624→
  1625→	// Phase stays ENDED
  1626→	assert.Equal(t, session.PhaseEnded, endedState.Phase,
  1627→		"ENDED session should remain ENDED")
  1628→
  1629→	// --- Verify: new ACTIVE session WAS condensed ---
  1630→	newState, err = s.loadSessionState(newSessionID)
  1631→	require.NoError(t, err)
  1632→	assert.Equal(t, 0, newState.StepCount,
  1633→		"New ACTIVE session StepCount should be reset by condensation")
  1634→	assert.Equal(t, newHead, newState.BaseCommit,
  1635→		"New ACTIVE session BaseCommit should be updated after condensation")
  1636→}
  1637→
  1638→// TestPostCommit_StaleActiveSession_NotCondensed verifies that a stale ACTIVE
  1639→// session (agent killed without Stop hook) is NOT condensed into an unrelated
  1640→// commit from a different session.
  1641→//
  1642→// Root cause: when an agent is killed without the Stop hook firing, its session
  1643→// remains in ACTIVE phase permanently. Previously, PostCommit unconditionally
  1644→// set hasNew=true for ACTIVE sessions and skipped the filesOverlapWithContent
  1645→// check, so stale ACTIVE sessions got condensed into every commit.
  1646→//
  1647→// The fix applies the overlap check to ALL sessions (including ACTIVE) using
  1648→// filesTouchedBefore, so stale sessions with unrelated files are filtered out.
  1649→func TestPostCommit_StaleActiveSession_NotCondensed(t *testing.T) {
  1650→	dir := setupGitRepo(t)
  1651→	t.Chdir(dir)
  1652→
  1653→	repo, err := git.PlainOpen(dir)
  1654→	require.NoError(t, err)
  1655→
  1656→	s := &ManualCommitStrategy{}
  1657→
  1658→	// --- Create a stale ACTIVE session from an old commit ---
  1659→	// This simulates an agent that was killed without the Stop hook firing.
  1660→	staleSessionID := "stale-active-session"
  1661→	setupSessionWithCheckpoint(t, s, repo, dir, staleSessionID)
  1662→
  1663→	staleState, err := s.loadSessionState(staleSessionID)
  1664→	require.NoError(t, err)
  1665→	staleState.Phase = session.PhaseActive
  1666→	// The stale session touched "test.txt" (set by setupSessionWithCheckpoint)
  1667→	// but the new commit will modify a different file.
  1668→	staleState.FilesTouched = []string{"test.txt"}
  1669→	require.NoError(t, s.saveSessionState(staleState))
  1670→
  1671→	staleOriginalBaseCommit := staleState.BaseCommit
  1672→	staleOriginalStepCount := staleState.StepCount
  1673→
  1674→	// Move HEAD forward with an unrelated commit (no trailer)
  1675→	wt, err := repo.Worktree()
  1676→	require.NoError(t, err)
  1677→	require.NoError(t, os.WriteFile(filepath.Join(dir, "unrelated.txt"), []byte("unrelated work"), 0o644))
  1678→	_, err = wt.Add("unrelated.txt")
  1679→	require.NoError(t, err)
  1680→	_, err = wt.Commit("unrelated commit", &git.CommitOptions{
  1681→		Author: &object.Signature{Name: "Test", Email: "test@test.com", When: time.Now()},
  1682→	})
  1683→	require.NoError(t, err)
  1684→
  1685→	// --- Create a NEW ACTIVE session at the new HEAD ---
  1686→	newSessionID := testNewActiveSessionID
  1687→
  1688→	// Create a new file for the new session (different from stale session's test.txt)
  1689→	require.NoError(t, os.WriteFile(filepath.Join(dir, "new-feature.txt"), []byte("new feature content"), 0o644))
  1690→
  1691→	metadataDir := ".entire/metadata/" + newSessionID
  1692→	metadataDirAbs := filepath.Join(dir, metadataDir)
  1693→	require.NoError(t, os.MkdirAll(metadataDirAbs, 0o755))
  1694→
  1695→	transcript := `{"type":"human","message":{"content":"add new feature"}}
  1696→{"type":"assistant","message":{"content":"adding new feature"}}
  1697→`
  1698→	require.NoError(t, os.WriteFile(
  1699→		filepath.Join(metadataDirAbs, paths.TranscriptFileName),
  1700→		[]byte(transcript), 0o644))
  1701→
  1702→	err = s.SaveStep(StepContext{
  1703→		SessionID:      newSessionID,
  1704→		ModifiedFiles:  []string{},
  1705→		NewFiles:       []string{"new-feature.txt"},
  1706→		DeletedFiles:   []string{},
  1707→		MetadataDir:    metadataDir,
  1708→		MetadataDirAbs: metadataDirAbs,
  1709→		CommitMessage:  "Checkpoint: new feature",
  1710→		AuthorName:     "Test",
  1711→		AuthorEmail:    "test@test.com",
  1712→	})
  1713→	require.NoError(t, err)
  1714→
  1715→	newState, err := s.loadSessionState(newSessionID)
  1716→	require.NoError(t, err)
  1717→	newState.Phase = session.PhaseActive
  1718→	require.NoError(t, s.saveSessionState(newState))
  1719→
  1720→	// --- Commit ONLY new-feature.txt (not test.txt) with checkpoint trailer ---
  1721→	wt, err = repo.Worktree()
  1722→	require.NoError(t, err)
  1723→	_, err = wt.Add("new-feature.txt")
  1724→	require.NoError(t, err)
  1725→
  1726→	cpID := "de1de2de3de4"
  1727→	commitMsg := "add new feature\n\n" + trailers.CheckpointTrailerKey + ": " + cpID + "\n"
  1728→	_, err = wt.Commit(commitMsg, &git.CommitOptions{
  1729→		Author: &object.Signature{Name: "Test", Email: "test@test.com", When: time.Now()},
  1730→	})
  1731→	require.NoError(t, err)
  1732→
  1733→	head, err := repo.Head()
  1734→	require.NoError(t, err)
  1735→	newHead := head.Hash().String()
  1736→
  1737→	// Run PostCommit
  1738→	err = s.PostCommit()
  1739→	require.NoError(t, err)
  1740→
  1741→	// --- Verify: stale ACTIVE session was NOT condensed ---
  1742→	staleState, err = s.loadSessionState(staleSessionID)
  1743→	require.NoError(t, err)
  1744→
  1745→	// StepCount should be unchanged (not reset by condensation)
  1746→	assert.Equal(t, staleOriginalStepCount, staleState.StepCount,
  1747→		"Stale ACTIVE session StepCount should NOT be reset (no condensation)")
  1748→
  1749→	// BaseCommit IS updated for ACTIVE sessions (updateBaseCommitIfChanged)
  1750→	assert.Equal(t, newHead, staleState.BaseCommit,
  1751→		"Stale ACTIVE session BaseCommit should be updated (ACTIVE sessions always get BaseCommit updated)")
  1752→	assert.NotEqual(t, staleOriginalBaseCommit, staleState.BaseCommit,
  1753→		"Stale ACTIVE session BaseCommit should have changed")
  1754→
  1755→	// Phase stays ACTIVE
  1756→	assert.Equal(t, session.PhaseActive, staleState.Phase,
  1757→		"Stale ACTIVE session should remain ACTIVE")
  1758→
  1759→	// --- Verify: new ACTIVE session WAS condensed ---
  1760→	newState, err = s.loadSessionState(newSessionID)
  1761→	require.NoError(t, err)
  1762→
  1763→	// StepCount reset to 0 by condensation
  1764→	assert.Equal(t, 0, newState.StepCount,
  1765→		"New ACTIVE session StepCount should be reset by condensation")
  1766→
  1767→	// BaseCommit updated to new HEAD
  1768→	assert.Equal(t, newHead, newState.BaseCommit,
  1769→		"New ACTIVE session BaseCommit should be updated after condensation")
  1770→
  1771→	// Verify entire/checkpoints/v1 exists (new session was condensed)
  1772→	_, err = repo.Reference(plumbing.NewBranchReferenceName(paths.MetadataBranchName), true)
  1773→	require.NoError(t, err,
  1774→		"entire/checkpoints/v1 should exist (new session was condensed)")
  1775→}
  1776→
  1777→// TestPostCommit_IdleSessionEmptyFilesTouched_NotCondensed verifies that an IDLE
  1778→// session with hasNew=true but empty FilesTouched is NOT condensed into a commit.
  1779→//
  1780→// This can happen for conversation-only sessions where the transcript grew but no
  1781→// files were modified. Previously, filesOverlapWithContent was called with an empty
  1782→// list and returned false. The shouldCondenseWithOverlapCheck method must also
  1783→// return false when filesTouchedBefore is empty.
  1784→func TestPostCommit_IdleSessionEmptyFilesTouched_NotCondensed(t *testing.T) {
  1785→	dir := setupGitRepo(t)
  1786→	t.Chdir(dir)
  1787→
  1788→	repo, err := git.PlainOpen(dir)
  1789→	require.NoError(t, err)
  1790→
  1791→	s := &ManualCommitStrategy{}
  1792→
  1793→	// --- Create an IDLE session with a checkpoint but no files touched ---
  1794→	idleSessionID := "idle-no-files-session"
  1795→	setupSessionWithCheckpoint(t, s, repo, dir, idleSessionID)
  1796→
  1797→	idleState, err := s.loadSessionState(idleSessionID)
  1798→	require.NoError(t, err)
  1799→	idleState.Phase = session.PhaseIdle
  1800→	// Clear FilesTouched to simulate a conversation-only session
  1801→	idleState.FilesTouched = nil
  1802→	// CheckpointTranscriptStart=0 so sessionHasNewContent returns true
  1803→	idleState.CheckpointTranscriptStart = 0
  1804→	require.NoError(t, s.saveSessionState(idleState))
  1805→
  1806→	idleOriginalStepCount := idleState.StepCount
  1807→
  1808→	// --- Make a commit with an unrelated file ---
  1809→	wt, err := repo.Worktree()
  1810→	require.NoError(t, err)
  1811→	require.NoError(t, os.WriteFile(filepath.Join(dir, "other-work.txt"), []byte("other work"), 0o644))
  1812→	_, err = wt.Add("other-work.txt")
  1813→	require.NoError(t, err)
  1814→
  1815→	cpID := "f1f2f3f4f5f6"
  1816→	commitMsg := "other work\n\n" + trailers.CheckpointTrailerKey + ": " + cpID + "\n"
  1817→	_, err = wt.Commit(commitMsg, &git.CommitOptions{
  1818→		Author: &object.Signature{Name: "Test", Email: "test@test.com", When: time.Now()},
  1819→	})
  1820→	require.NoError(t, err)
  1821→
  1822→	// Run PostCommit
  1823→	err = s.PostCommit()
  1824→	require.NoError(t, err)
  1825→
  1826→	// --- Verify: IDLE session with no files was NOT condensed ---
  1827→	idleState, err = s.loadSessionState(idleSessionID)
  1828→	require.NoError(t, err)
  1829→
  1830→	assert.Equal(t, idleOriginalStepCount, idleState.StepCount,
  1831→		"IDLE session with empty FilesTouched should NOT be condensed")
  1832→	assert.Equal(t, session.PhaseIdle, idleState.Phase,
  1833→		"IDLE session should remain IDLE")
  1834→	// BaseCommit is NOT updated for non-ACTIVE sessions (updateBaseCommitIfChanged skips them)
  1835→}
  1836→
```

> TOOL

tool_use Read
id: toolu_01XBqGxQ82YhWeLRx33Vtk5y
```json
{
  "file_path": "/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/strategy/manual_commit_hooks.go"
}
```

> TOOL

tool_result
id: toolu_01XBqGxQ82YhWeLRx33Vtk5y
```
     1→package strategy
     2→
     3→import (
     4→	"bufio"
     5→	"bytes"
     6→	"context"
     7→	"fmt"
     8→	"log/slog"
     9→	"os"
    10→	"path/filepath"
    11→	"strings"
    12→
    13→	"github.com/entireio/cli/cmd/entire/cli/agent"
    14→	"github.com/entireio/cli/cmd/entire/cli/agent/claudecode"
    15→
    16→	"github.com/entireio/cli/cmd/entire/cli/checkpoint"
    17→	"github.com/entireio/cli/cmd/entire/cli/checkpoint/id"
    18→	"github.com/entireio/cli/cmd/entire/cli/logging"
    19→	"github.com/entireio/cli/cmd/entire/cli/paths"
    20→	"github.com/entireio/cli/cmd/entire/cli/session"
    21→	"github.com/entireio/cli/cmd/entire/cli/stringutil"
    22→	"github.com/entireio/cli/cmd/entire/cli/trailers"
    23→	"github.com/entireio/cli/redact"
    24→
    25→	"github.com/go-git/go-git/v5"
    26→	"github.com/go-git/go-git/v5/plumbing"
    27→	"github.com/go-git/go-git/v5/plumbing/object"
    28→	"github.com/go-git/go-git/v5/utils/binary"
    29→)
    30→
    31→// hasTTY checks if /dev/tty is available for interactive prompts.
    32→// Returns false when running as an agent subprocess (no controlling terminal).
    33→//
    34→// In test environments, ENTIRE_TEST_TTY overrides the real check:
    35→//   - ENTIRE_TEST_TTY=1 → simulate human (TTY available)
    36→//   - ENTIRE_TEST_TTY=0 → simulate agent (no TTY)
    37→func hasTTY() bool {
    38→	if v := os.Getenv("ENTIRE_TEST_TTY"); v != "" {
    39→		return v == "1"
    40→	}
    41→
    42→	// Gemini CLI sets GEMINI_CLI=1 when running shell commands.
    43→	// Gemini subprocesses may have access to the user's TTY, but they can't
    44→	// actually respond to interactive prompts. Treat them as non-TTY.
    45→	// See: https://geminicli.com/docs/tools/shell/
    46→	if os.Getenv("GEMINI_CLI") != "" {
    47→		return false
    48→	}
    49→
    50→	tty, err := os.OpenFile("/dev/tty", os.O_RDWR, 0)
    51→	if err != nil {
    52→		return false
    53→	}
    54→	_ = tty.Close()
    55→	return true
    56→}
    57→
    58→// askConfirmTTY prompts the user for a yes/no confirmation via /dev/tty.
    59→// This works even when stdin is redirected (e.g., git commit -m).
    60→// Returns true for yes, false for no. If TTY is unavailable, returns the default.
    61→// If context is non-empty, it is displayed on a separate line before the prompt.
    62→func askConfirmTTY(prompt string, context string, defaultYes bool) bool {
    63→	// In test mode, don't try to interact with the real TTY — just use the default.
    64→	// ENTIRE_TEST_TTY=1 simulates "a human is present" for the hasTTY() check
    65→	// but we can't actually read from the TTY in tests.
    66→	if os.Getenv("ENTIRE_TEST_TTY") != "" {
    67→		return defaultYes
    68→	}
    69→
    70→	// Gemini CLI sets GEMINI_CLI=1 when running shell commands (including git commit).
    71→	// The agent can't respond to TTY prompts, so use the default to avoid hanging.
    72→	// See: https://geminicli.com/docs/tools/shell/
    73→	if os.Getenv("GEMINI_CLI") != "" {
    74→		return defaultYes
    75→	}
    76→
    77→	// Open /dev/tty for both reading and writing
    78→	// This is the controlling terminal, which works even when stdin/stderr are redirected
    79→	tty, err := os.OpenFile("/dev/tty", os.O_RDWR, 0)
    80→	if err != nil {
    81→		// Can't open TTY (e.g., running in CI), use default
    82→		return defaultYes
    83→	}
    84→	defer tty.Close()
    85→
    86→	// Show context if provided
    87→	if context != "" {
    88→		fmt.Fprintf(tty, "%s\n", context)
    89→	}
    90→
    91→	// Show prompt with default indicator
    92→	// Write to tty directly, not stderr, since git hooks may redirect stderr to /dev/null
    93→	var hint string
    94→	if defaultYes {
    95→		hint = "[Y/n]"
    96→	} else {
    97→		hint = "[y/N]"
    98→	}
    99→	fmt.Fprintf(tty, "%s %s ", prompt, hint)
   100→
   101→	// Read response
   102→	reader := bufio.NewReader(tty)
   103→	response, err := reader.ReadString('\n')
   104→	if err != nil {
   105→		return defaultYes
   106→	}
   107→
   108→	response = strings.TrimSpace(strings.ToLower(response))
   109→	switch response {
   110→	case "y", "yes":
   111→		return true
   112→	case "n", "no":
   113→		return false
   114→	default:
   115→		// Empty or invalid input - use default
   116→		return defaultYes
   117→	}
   118→}
   119→
   120→// CommitMsg is called by the git commit-msg hook after the user edits the message.
   121→// If the message contains only our trailer (no actual user content), strip it
   122→// so git will abort the commit due to empty message.
   123→//
   124→//nolint:unparam // error return required by interface but hooks must return nil
   125→func (s *ManualCommitStrategy) CommitMsg(commitMsgFile string) error {
   126→	content, err := os.ReadFile(commitMsgFile) //nolint:gosec // Path comes from git hook
   127→	if err != nil {
   128→		return nil //nolint:nilerr // Hook must be silent on failure
   129→	}
   130→
   131→	message := string(content)
   132→
   133→	// Check if our trailer is present (ParseCheckpoint validates format, so found==true means valid)
   134→	if _, found := trailers.ParseCheckpoint(message); !found {
   135→		// No trailer, nothing to do
   136→		return nil
   137→	}
   138→
   139→	// Check if there's any user content (non-comment, non-trailer lines)
   140→	if !hasUserContent(message) {
   141→		// No user content - strip the trailer so git aborts
   142→		message = stripCheckpointTrailer(message)
   143→		if err := os.WriteFile(commitMsgFile, []byte(message), 0o600); err != nil {
   144→			return nil //nolint:nilerr // Hook must be silent on failure
   145→		}
   146→	}
   147→
   148→	return nil
   149→}
   150→
   151→// hasUserContent checks if the message has any content besides comments and our trailer.
   152→func hasUserContent(message string) bool {
   153→	trailerPrefix := trailers.CheckpointTrailerKey + ":"
   154→	for _, line := range strings.Split(message, "\n") {
   155→		trimmed := strings.TrimSpace(line)
   156→		// Skip empty lines
   157→		if trimmed == "" {
   158→			continue
   159→		}
   160→		// Skip comment lines
   161→		if strings.HasPrefix(trimmed, "#") {
   162→			continue
   163→		}
   164→		// Skip our trailer line
   165→		if strings.HasPrefix(trimmed, trailerPrefix) {
   166→			continue
   167→		}
   168→		// Found user content
   169→		return true
   170→	}
   171→	return false
   172→}
   173→
   174→// stripCheckpointTrailer removes the Entire-Checkpoint trailer line from the message.
   175→func stripCheckpointTrailer(message string) string {
   176→	trailerPrefix := trailers.CheckpointTrailerKey + ":"
   177→	var result []string
   178→	for _, line := range strings.Split(message, "\n") {
   179→		if !strings.HasPrefix(strings.TrimSpace(line), trailerPrefix) {
   180→			result = append(result, line)
   181→		}
   182→	}
   183→	return strings.Join(result, "\n")
   184→}
   185→
   186→// isGitSequenceOperation checks if git is currently in the middle of a rebase,
   187→// cherry-pick, or revert operation. During these operations, commits are being
   188→// replayed and should not be linked to agent sessions.
   189→//
   190→// Detects:
   191→//   - rebase: .git/rebase-merge/ or .git/rebase-apply/ directories
   192→//   - cherry-pick: .git/CHERRY_PICK_HEAD file
   193→//   - revert: .git/REVERT_HEAD file
   194→func isGitSequenceOperation() bool {
   195→	// Get git directory (handles worktrees and relative paths correctly)
   196→	gitDir, err := GetGitDir()
   197→	if err != nil {
   198→		return false // Can't determine, assume not in sequence operation
   199→	}
   200→
   201→	// Check for rebase state directories
   202→	if _, err := os.Stat(filepath.Join(gitDir, "rebase-merge")); err == nil {
   203→		return true
   204→	}
   205→	if _, err := os.Stat(filepath.Join(gitDir, "rebase-apply")); err == nil {
   206→		return true
   207→	}
   208→
   209→	// Check for cherry-pick and revert state files
   210→	if _, err := os.Stat(filepath.Join(gitDir, "CHERRY_PICK_HEAD")); err == nil {
   211→		return true
   212→	}
   213→	if _, err := os.Stat(filepath.Join(gitDir, "REVERT_HEAD")); err == nil {
   214→		return true
   215→	}
   216→
   217→	return false
   218→}
   219→
   220→// PrepareCommitMsg is called by the git prepare-commit-msg hook.
   221→// Adds an Entire-Checkpoint trailer to the commit message with a stable checkpoint ID.
   222→// Only adds a trailer if there's actually new session content to condense.
   223→// The actual condensation happens in PostCommit - if the user removes the trailer,
   224→// the commit will not be linked to the session (useful for "manual" commits).
   225→// For amended commits, preserves the existing checkpoint ID.
   226→//
   227→// The source parameter indicates how the commit was initiated:
   228→//   - "" or "template": normal editor flow - adds trailer with explanatory comment
   229→//   - "message": using -m or -F flag - prompts user interactively via /dev/tty
   230→//   - "merge", "squash": skip trailer entirely (auto-generated messages)
   231→//   - "commit": amend operation - preserves existing trailer or restores from LastCheckpointID
   232→//
   233→
   234→func (s *ManualCommitStrategy) PrepareCommitMsg(commitMsgFile string, source string) error {
   235→	logCtx := logging.WithComponent(context.Background(), "checkpoint")
   236→
   237→	// Skip during rebase, cherry-pick, or revert operations
   238→	// These are replaying existing commits and should not be linked to agent sessions
   239→	if isGitSequenceOperation() {
   240→		logging.Debug(logCtx, "prepare-commit-msg: skipped during git sequence operation",
   241→			slog.String("strategy", "manual-commit"),
   242→			slog.String("source", source),
   243→		)
   244→		return nil
   245→	}
   246→
   247→	// Skip for merge and squash sources
   248→	// These are auto-generated messages - not from Claude sessions
   249→	switch source {
   250→	case "merge", "squash":
   251→		logging.Debug(logCtx, "prepare-commit-msg: skipped for source",
   252→			slog.String("strategy", "manual-commit"),
   253→			slog.String("source", source),
   254→		)
   255→		return nil
   256→	}
   257→
   258→	// Handle amend (source="commit") separately: preserve or restore trailer
   259→	if source == "commit" {
   260→		return s.handleAmendCommitMsg(logCtx, commitMsgFile)
   261→	}
   262→
   263→	repo, err := OpenRepository()
   264→	if err != nil {
   265→		return nil //nolint:nilerr // Hook must be silent on failure
   266→	}
   267→
   268→	worktreePath, err := GetWorktreePath()
   269→	if err != nil {
   270→		return nil //nolint:nilerr // Hook must be silent on failure
   271→	}
   272→
   273→	// Find all active sessions for this worktree
   274→	// We match by worktree (not BaseCommit) because the user may have made
   275→	// intermediate commits without entering new prompts, causing HEAD to diverge
   276→	sessions, err := s.findSessionsForWorktree(worktreePath)
   277→	if err != nil || len(sessions) == 0 {
   278→		// No active sessions or error listing - silently skip (hooks must be resilient)
   279→		logging.Debug(logCtx, "prepare-commit-msg: no active sessions",
   280→			slog.String("strategy", "manual-commit"),
   281→			slog.String("source", source),
   282→		)
   283→		return nil //nolint:nilerr // Intentional: hooks must be silent on failure
   284→	}
   285→
   286→	// Fast path: when an agent is committing (ACTIVE session + no TTY), skip
   287→	// content detection and interactive prompts. The agent can't respond to TTY
   288→	// prompts and the content detection can miss mid-session work (no shadow
   289→	// branch yet, transcript analysis may fail). Generate a checkpoint ID and
   290→	// add the trailer directly.
   291→	if !hasTTY() {
   292→		for _, state := range sessions {
   293→			if state.Phase.IsActive() {
   294→				return s.addTrailerForAgentCommit(logCtx, commitMsgFile, state, source)
   295→			}
   296→		}
   297→	}
   298→
   299→	// Check if any session has new content to condense
   300→	sessionsWithContent := s.filterSessionsWithNewContent(repo, sessions)
   301→
   302→	if len(sessionsWithContent) == 0 {
   303→		// No new content — no trailer needed
   304→		logging.Debug(logCtx, "prepare-commit-msg: no content to link",
   305→			slog.String("strategy", "manual-commit"),
   306→			slog.String("source", source),
   307→			slog.Int("sessions_found", len(sessions)),
   308→		)
   309→		return nil
   310→	}
   311→
   312→	// Read current commit message
   313→	content, err := os.ReadFile(commitMsgFile) //nolint:gosec // commitMsgFile is provided by git hook
   314→	if err != nil {
   315→		return nil //nolint:nilerr // Hook must be silent on failure
   316→	}
   317→
   318→	message := string(content)
   319→
   320→	// Check if trailer already exists (ParseCheckpoint validates format, so found==true means valid)
   321→	if existingCpID, found := trailers.ParseCheckpoint(message); found {
   322→		// Trailer already exists (e.g., amend) - keep it
   323→		logging.Debug(logCtx, "prepare-commit-msg: trailer already exists",
   324→			slog.String("strategy", "manual-commit"),
   325→			slog.String("source", source),
   326→			slog.String("existing_checkpoint_id", existingCpID.String()),
   327→		)
   328→		return nil
   329→	}
   330→
   331→	// Generate a fresh checkpoint ID
   332→	checkpointID, err := id.Generate()
   333→	if err != nil {
   334→		return fmt.Errorf("failed to generate checkpoint ID: %w", err)
   335→	}
   336→
   337→	// Determine agent type and last prompt from session
   338→	agentType := DefaultAgentType // default for backward compatibility
   339→	var lastPrompt string
   340→	if len(sessionsWithContent) > 0 {
   341→		firstSession := sessionsWithContent[0]
   342→		if firstSession.AgentType != "" {
   343→			agentType = firstSession.AgentType
   344→		}
   345→		lastPrompt = s.getLastPrompt(repo, firstSession)
   346→	}
   347→
   348→	// Prepare prompt for display: collapse newlines/whitespace, then truncate (rune-safe)
   349→	displayPrompt := stringutil.TruncateRunes(stringutil.CollapseWhitespace(lastPrompt), 80, "...")
   350→
   351→	// Add trailer differently based on commit source
   352→	switch source {
   353→	case "message":
   354→		// Using -m or -F: ask user interactively whether to add trailer
   355→		// (comments won't be stripped by git in this mode)
   356→
   357→		// Build context string for interactive prompt
   358→		var promptContext string
   359→		if displayPrompt != "" {
   360→			promptContext = "You have an active " + string(agentType) + " session.\nLast Prompt: " + displayPrompt
   361→		}
   362→
   363→		if !askConfirmTTY("Link this commit to "+string(agentType)+" session context?", promptContext, true) {
   364→			// User declined - don't add trailer
   365→			logging.Debug(logCtx, "prepare-commit-msg: user declined trailer",
   366→				slog.String("strategy", "manual-commit"),
   367→				slog.String("source", source),
   368→			)
   369→			return nil
   370→		}
   371→		message = addCheckpointTrailer(message, checkpointID)
   372→	default:
   373→		// Normal editor flow: add trailer with explanatory comment (will be stripped by git)
   374→		message = addCheckpointTrailerWithComment(message, checkpointID, string(agentType), displayPrompt)
   375→	}
   376→
   377→	logging.Info(logCtx, "prepare-commit-msg: trailer added",
   378→		slog.String("strategy", "manual-commit"),
   379→		slog.String("source", source),
   380→		slog.String("checkpoint_id", checkpointID.String()),
   381→	)
   382→
   383→	// Write updated message back
   384→	if err := os.WriteFile(commitMsgFile, []byte(message), 0o600); err != nil {
   385→		return nil //nolint:nilerr // Hook must be silent on failure
   386→	}
   387→
   388→	return nil
   389→}
   390→
   391→// handleAmendCommitMsg handles the prepare-commit-msg hook for amend operations
   392→// (source="commit"). It preserves existing trailers or restores from LastCheckpointID.
   393→func (s *ManualCommitStrategy) handleAmendCommitMsg(logCtx context.Context, commitMsgFile string) error {
   394→	// Read current commit message
   395→	content, err := os.ReadFile(commitMsgFile) //nolint:gosec // commitMsgFile is provided by git hook
   396→	if err != nil {
   397→		return nil //nolint:nilerr // Hook must be silent on failure
   398→	}
   399→
   400→	message := string(content)
   401→
   402→	// If message already has a trailer, keep it unchanged
   403→	if existingCpID, found := trailers.ParseCheckpoint(message); found {
   404→		logging.Debug(logCtx, "prepare-commit-msg: amend preserves existing trailer",
   405→			slog.String("strategy", "manual-commit"),
   406→			slog.String("checkpoint_id", existingCpID.String()),
   407→		)
   408→		return nil
   409→	}
   410→
   411→	// No trailer in message — check if any session has LastCheckpointID to restore
   412→	worktreePath, err := GetWorktreePath()
   413→	if err != nil {
   414→		return nil //nolint:nilerr // Hook must be silent on failure
   415→	}
   416→
   417→	sessions, err := s.findSessionsForWorktree(worktreePath)
   418→	if err != nil || len(sessions) == 0 {
   419→		return nil //nolint:nilerr // No sessions - nothing to restore
   420→	}
   421→
   422→	// For amend, HEAD^ is the commit being amended, and HEAD is where we are now.
   423→	// We need to match sessions whose BaseCommit equals HEAD (the commit being amended
   424→	// was created from this base). This prevents stale sessions from injecting
   425→	// unrelated checkpoint IDs.
   426→	repo, repoErr := OpenRepository()
   427→	if repoErr != nil {
   428→		return nil //nolint:nilerr // Hook must be silent on failure
   429→	}
   430→	head, headErr := repo.Head()
   431→	if headErr != nil {
   432→		return nil //nolint:nilerr // Hook must be silent on failure
   433→	}
   434→	currentHead := head.Hash().String()
   435→
   436→	// Find first matching session with LastCheckpointID to restore.
   437→	// LastCheckpointID is set after condensation completes.
   438→	for _, state := range sessions {
   439→		if state.BaseCommit != currentHead {
   440→			continue
   441→		}
   442→		if state.LastCheckpointID.IsEmpty() {
   443→			continue
   444→		}
   445→		cpID := state.LastCheckpointID
   446→		source := "LastCheckpointID"
   447→
   448→		// Restore the trailer
   449→		message = addCheckpointTrailer(message, cpID)
   450→		if writeErr := os.WriteFile(commitMsgFile, []byte(message), 0o600); writeErr != nil {
   451→			return nil //nolint:nilerr // Hook must be silent on failure
   452→		}
   453→
   454→		logging.Info(logCtx, "prepare-commit-msg: restored trailer on amend",
   455→			slog.String("strategy", "manual-commit"),
   456→			slog.String("checkpoint_id", cpID.String()),
   457→			slog.String("session_id", state.SessionID),
   458→			slog.String("source", source),
   459→		)
   460→		return nil
   461→	}
   462→
   463→	// No checkpoint ID found - leave message unchanged
   464→	logging.Debug(logCtx, "prepare-commit-msg: amend with no checkpoint to restore",
   465→		slog.String("strategy", "manual-commit"),
   466→	)
   467→	return nil
   468→}
   469→
   470→// PostCommit is called by the git post-commit hook after a commit is created.
   471→// Uses the session state machine to determine what action to take per session:
   472→//   - ACTIVE → condense immediately (each commit gets its own checkpoint)
   473→//   - IDLE → condense immediately
   474→//   - ENDED → condense if files touched, discard if empty
   475→//
   476→// After condensation for ACTIVE sessions, remaining uncommitted files are
   477→// carried forward to a new shadow branch so the next commit gets its own checkpoint.
   478→//
   479→// Shadow branches are only deleted when ALL sessions sharing the branch are non-active
   480→// and were condensed during this PostCommit.
   481→
   482→// postCommitActionHandler implements session.ActionHandler for PostCommit.
   483→// Each session in the loop gets its own handler with per-session context.
   484→// Handler methods use the *State parameter from ApplyTransition (same pointer
   485→// as the state being transitioned) rather than capturing state separately.
   486→type postCommitActionHandler struct {
   487→	s                      *ManualCommitStrategy
   488→	logCtx                 context.Context
   489→	repo                   *git.Repository
   490→	checkpointID           id.CheckpointID
   491→	head                   *plumbing.Reference
   492→	commit                 *object.Commit
   493→	newHead                string
   494→	shadowBranchName       string
   495→	shadowBranchesToDelete map[string]struct{}
   496→	committedFileSet       map[string]struct{}
   497→	hasNew                 bool
   498→	filesTouchedBefore     []string
   499→
   500→	// Output: set by handler methods, read by caller after TransitionAndLog.
   501→	condensed bool
   502→}
   503→
   504→func (h *postCommitActionHandler) HandleCondense(state *session.State) error {
   505→	shouldCondense := h.shouldCondenseWithOverlapCheck(state.Phase.IsActive())
   506→
   507→	logging.Debug(h.logCtx, "post-commit: HandleCondense decision",
   508→		slog.String("session_id", state.SessionID),
   509→		slog.String("phase", string(state.Phase)),
   510→		slog.Bool("has_new", h.hasNew),
   511→		slog.Bool("should_condense", shouldCondense),
   512→		slog.String("shadow_branch", h.shadowBranchName),
   513→	)
   514→
   515→	if shouldCondense {
   516→		h.condensed = h.s.condenseAndUpdateState(h.logCtx, h.repo, h.checkpointID, state, h.head, h.shadowBranchName, h.shadowBranchesToDelete, h.committedFileSet)
   517→	} else {
   518→		h.s.updateBaseCommitIfChanged(h.logCtx, state, h.newHead)
   519→	}
   520→	return nil
   521→}
   522→
   523→func (h *postCommitActionHandler) HandleCondenseIfFilesTouched(state *session.State) error {
   524→	shouldCondense := len(state.FilesTouched) > 0 && h.shouldCondenseWithOverlapCheck(state.Phase.IsActive())
   525→
   526→	logging.Debug(h.logCtx, "post-commit: HandleCondenseIfFilesTouched decision",
   527→		slog.String("session_id", state.SessionID),
   528→		slog.String("phase", string(state.Phase)),
   529→		slog.Bool("has_new", h.hasNew),
   530→		slog.Int("files_touched", len(state.FilesTouched)),
   531→		slog.Bool("should_condense", shouldCondense),
   532→		slog.String("shadow_branch", h.shadowBranchName),
   533→	)
   534→
   535→	if shouldCondense {
   536→		h.condensed = h.s.condenseAndUpdateState(h.logCtx, h.repo, h.checkpointID, state, h.head, h.shadowBranchName, h.shadowBranchesToDelete, h.committedFileSet)
   537→	} else {
   538→		h.s.updateBaseCommitIfChanged(h.logCtx, state, h.newHead)
   539→	}
   540→	return nil
   541→}
   542→
   543→// shouldCondenseWithOverlapCheck returns true if the session should be condensed
   544→// into this commit. Requires both that hasNew is true AND that the session's files
   545→// overlap with the committed files with matching content.
   546→//
   547→// This prevents stale sessions (ACTIVE sessions where the agent was killed, or
   548→// ENDED/IDLE sessions with carry-forward files) from being condensed into every
   549→// unrelated commit.
   550→//
   551→// filesTouchedBefore is populated from:
   552→//   - state.FilesTouched for IDLE/ENDED sessions (set via SaveStep/SaveTaskStep -> mergeFilesTouched)
   553→//   - transcript extraction for ACTIVE sessions when FilesTouched is empty
   554→//
   555→// When filesTouchedBefore is empty:
   556→//   - For ACTIVE sessions: fail-open (trust hasNew) because the agent may be
   557→//     mid-turn before any files are saved to state.
   558→//   - For IDLE/ENDED sessions: return false because there are no files to
   559→//     overlap with the commit.
   560→func (h *postCommitActionHandler) shouldCondenseWithOverlapCheck(isActive bool) bool {
   561→	if !h.hasNew {
   562→		return false
   563→	}
   564→	if len(h.filesTouchedBefore) == 0 {
   565→		return isActive // ACTIVE: fail-open; IDLE/ENDED: no files = no overlap
   566→	}
   567→	// Only check files that were actually changed in this commit.
   568→	// Without this, files that exist in the tree but weren't changed
   569→	// would pass the "modified file" check in filesOverlapWithContent
   570→	// (because the file exists in the parent tree), causing stale
   571→	// sessions to be incorrectly condensed.
   572→	var committedTouchedFiles []string
   573→	for _, f := range h.filesTouchedBefore {
   574→		if _, ok := h.committedFileSet[f]; ok {
   575→			committedTouchedFiles = append(committedTouchedFiles, f)
   576→		}
   577→	}
   578→	if len(committedTouchedFiles) == 0 {
   579→		return false
   580→	}
   581→	return filesOverlapWithContent(h.repo, h.shadowBranchName, h.commit, committedTouchedFiles)
   582→}
   583→
   584→func (h *postCommitActionHandler) HandleDiscardIfNoFiles(state *session.State) error {
   585→	if len(state.FilesTouched) == 0 {
   586→		logging.Debug(h.logCtx, "post-commit: skipping empty ended session (no files to condense)",
   587→			slog.String("session_id", state.SessionID),
   588→		)
   589→	}
   590→	h.s.updateBaseCommitIfChanged(h.logCtx, state, h.newHead)
   591→	return nil
   592→}
   593→
   594→func (h *postCommitActionHandler) HandleWarnStaleSession(_ *session.State) error {
   595→	// Not produced by EventGitCommit; no-op for exhaustiveness.
   596→	return nil
   597→}
   598→
   599→// During rebase/cherry-pick/revert operations, phase transitions are skipped entirely.
   600→//
   601→//nolint:unparam // error return required by interface but hooks must return nil
   602→func (s *ManualCommitStrategy) PostCommit() error {
   603→	logCtx := logging.WithComponent(context.Background(), "checkpoint")
   604→
   605→	repo, err := OpenRepository()
   606→	if err != nil {
   607→		return nil //nolint:nilerr // Hook must be silent on failure
   608→	}
   609→
   610→	// Get HEAD commit to check for trailer
   611→	head, err := repo.Head()
   612→	if err != nil {
   613→		return nil //nolint:nilerr // Hook must be silent on failure
   614→	}
   615→
   616→	commit, err := repo.CommitObject(head.Hash())
   617→	if err != nil {
   618→		return nil //nolint:nilerr // Hook must be silent on failure
   619→	}
   620→
   621→	// Check if commit has checkpoint trailer (ParseCheckpoint validates format)
   622→	checkpointID, found := trailers.ParseCheckpoint(commit.Message)
   623→	if !found {
   624→		// No trailer — user removed it or it was never added (mid-turn commit).
   625→		// Still update BaseCommit for active sessions so future commits can match.
   626→		s.postCommitUpdateBaseCommitOnly(logCtx, head)
   627→		return nil
   628→	}
   629→
   630→	worktreePath, err := GetWorktreePath()
   631→	if err != nil {
   632→		return nil //nolint:nilerr // Hook must be silent on failure
   633→	}
   634→
   635→	// Find all active sessions for this worktree
   636→	sessions, err := s.findSessionsForWorktree(worktreePath)
   637→	if err != nil || len(sessions) == 0 {
   638→		logging.Warn(logCtx, "post-commit: no active sessions despite trailer",
   639→			slog.String("strategy", "manual-commit"),
   640→			slog.String("checkpoint_id", checkpointID.String()),
   641→		)
   642→		return nil //nolint:nilerr // Intentional: hooks must be silent on failure
   643→	}
   644→
   645→	// Build transition context
   646→	isRebase := isGitSequenceOperation()
   647→	transitionCtx := session.TransitionContext{
   648→		IsRebaseInProgress: isRebase,
   649→	}
   650→
   651→	if isRebase {
   652→		logging.Debug(logCtx, "post-commit: rebase/sequence in progress, skipping phase transitions",
   653→			slog.String("strategy", "manual-commit"),
   654→		)
   655→	}
   656→
   657→	// Track shadow branch names and whether they can be deleted
   658→	shadowBranchesToDelete := make(map[string]struct{})
   659→	// Track active sessions that were NOT condensed — their shadow branches must be preserved
   660→	uncondensedActiveOnBranch := make(map[string]bool)
   661→
   662→	newHead := head.Hash().String()
   663→	committedFileSet := filesChangedInCommit(commit)
   664→
   665→	for _, state := range sessions {
   666→		shadowBranchName := getShadowBranchNameForCommit(state.BaseCommit, state.WorktreeID)
   667→
   668→		// Check for new content (needed for TransitionContext and condensation).
   669→		// Fail-open: if content check errors, assume new content exists so we
   670→		// don't silently skip data that should have been condensed.
   671→		//
   672→		// For ACTIVE sessions: the commit has a checkpoint trailer (verified above),
   673→		// meaning PrepareCommitMsg already determined this commit is session-related.
   674→		// The trailer is only added when either:
   675→		//   - No TTY (agent/subagent committing) — added unconditionally
   676→		//   - TTY (human committing) — added after content detection confirmed agent work
   677→		// In both cases, PrepareCommitMsg already validated this commit. We trust
   678→		// that decision here. Transcript-based re-validation is unreliable because
   679→		// subagent transcripts may not be available yet (subagent still running).
   680→		var hasNew bool
   681→		if state.Phase.IsActive() {
   682→			hasNew = true
   683→		} else {
   684→			var contentErr error
   685→			hasNew, contentErr = s.sessionHasNewContent(repo, state)
   686→			if contentErr != nil {
   687→				hasNew = true
   688→				logging.Debug(logCtx, "post-commit: error checking session content, assuming new content",
   689→					slog.String("session_id", state.SessionID),
   690→					slog.String("error", contentErr.Error()),
   691→				)
   692→			}
   693→		}
   694→		transitionCtx.HasFilesTouched = len(state.FilesTouched) > 0
   695→
   696→		// Save FilesTouched BEFORE TransitionAndLog — the handler's condensation
   697→		// clears it, but we need the original list for carry-forward computation.
   698→		// For mid-session commits (ACTIVE, no shadow branch), state.FilesTouched may be empty
   699→		// because no SaveStep/Stop has been called yet. Extract files from transcript.
   700→		filesTouchedBefore := make([]string, len(state.FilesTouched))
   701→		copy(filesTouchedBefore, state.FilesTouched)
   702→		if len(filesTouchedBefore) == 0 && state.Phase.IsActive() && state.TranscriptPath != "" {
   703→			filesTouchedBefore = s.extractFilesFromLiveTranscript(state)
   704→		}
   705→
   706→		logging.Debug(logCtx, "post-commit: carry-forward prep",
   707→			slog.String("session_id", state.SessionID),
   708→			slog.Bool("is_active", state.Phase.IsActive()),
   709→			slog.String("transcript_path", state.TranscriptPath),
   710→			slog.Int("files_touched_before", len(filesTouchedBefore)),
   711→			slog.Any("files", filesTouchedBefore),
   712→		)
   713→
   714→		// Run the state machine transition with handler for strategy-specific actions.
   715→		handler := &postCommitActionHandler{
   716→			s:                      s,
   717→			logCtx:                 logCtx,
   718→			repo:                   repo,
   719→			checkpointID:           checkpointID,
   720→			head:                   head,
   721→			commit:                 commit,
   722→			newHead:                newHead,
   723→			shadowBranchName:       shadowBranchName,
   724→			shadowBranchesToDelete: shadowBranchesToDelete,
   725→			committedFileSet:       committedFileSet,
   726→			hasNew:                 hasNew,
   727→			filesTouchedBefore:     filesTouchedBefore,
   728→		}
   729→
   730→		if err := TransitionAndLog(state, session.EventGitCommit, transitionCtx, handler); err != nil {
   731→			fmt.Fprintf(os.Stderr, "[entire] Warning: post-commit action handler error: %v\n", err)
   732→		}
   733→
   734→		// Record checkpoint ID for ACTIVE sessions so HandleTurnEnd can finalize
   735→		// with full transcript. IDLE/ENDED sessions already have complete transcripts.
   736→		// NOTE: This check runs AFTER TransitionAndLog updated the phase. It relies on
   737→		// ACTIVE + GitCommit → ACTIVE (phase stays ACTIVE). If that state machine
   738→		// transition ever changed, this guard would silently stop recording IDs.
   739→		if handler.condensed && state.Phase.IsActive() {
   740→			state.TurnCheckpointIDs = append(state.TurnCheckpointIDs, checkpointID.String())
   741→		}
   742→
   743→		// Carry forward remaining uncommitted files so the next commit gets its
   744→		// own checkpoint ID. This applies to ALL phases — if a user splits their
   745→		// commit across two `git commit` invocations, each gets a 1:1 checkpoint.
   746→		// Uses content-aware comparison: if user did `git add -p` and committed
   747→		// partial changes, the file still has remaining agent changes to carry forward.
   748→		if handler.condensed {
   749→			remainingFiles := filesWithRemainingAgentChanges(repo, shadowBranchName, commit, filesTouchedBefore, committedFileSet)
   750→			state.FilesTouched = remainingFiles
   751→			logging.Debug(logCtx, "post-commit: carry-forward decision (content-aware)",
   752→				slog.String("session_id", state.SessionID),
   753→				slog.Int("files_touched_before", len(filesTouchedBefore)),
   754→				slog.Int("committed_files", len(committedFileSet)),
   755→				slog.Int("remaining_files", len(remainingFiles)),
   756→				slog.Any("remaining", remainingFiles),
   757→				slog.Any("committed_files", committedFileSet),
   758→			)
   759→			if len(remainingFiles) > 0 {
   760→				s.carryForwardToNewShadowBranch(logCtx, repo, state, remainingFiles)
   761→			}
   762→		}
   763→
   764→		// Save the updated state
   765→		if err := s.saveSessionState(state); err != nil {
   766→			fmt.Fprintf(os.Stderr, "[entire] Warning: failed to update session state: %v\n", err)
   767→		}
   768→
   769→		// Only preserve shadow branch for active sessions that were NOT condensed.
   770→		// Condensed sessions already have their data on entire/checkpoints/v1.
   771→		if state.Phase.IsActive() && !handler.condensed {
   772→			uncondensedActiveOnBranch[shadowBranchName] = true
   773→		}
   774→	}
   775→
   776→	// Clean up shadow branches — only delete when ALL sessions on the branch are non-active
   777→	// or were condensed during this PostCommit.
   778→	for shadowBranchName := range shadowBranchesToDelete {
   779→		if uncondensedActiveOnBranch[shadowBranchName] {
   780→			logging.Debug(logCtx, "post-commit: preserving shadow branch (active session exists)",
   781→				slog.String("shadow_branch", shadowBranchName),
   782→			)
   783→			continue
   784→		}
   785→		if err := deleteShadowBranch(repo, shadowBranchName); err != nil {
   786→			fmt.Fprintf(os.Stderr, "[entire] Warning: failed to clean up %s: %v\n", shadowBranchName, err)
   787→		} else {
   788→			fmt.Fprintf(os.Stderr, "[entire] Cleaned up shadow branch: %s\n", shadowBranchName)
   789→			logging.Info(logCtx, "shadow branch deleted",
   790→				slog.String("strategy", "manual-commit"),
   791→				slog.String("shadow_branch", shadowBranchName),
   792→			)
   793→		}
   794→	}
   795→
   796→	return nil
   797→}
   798→
   799→// condenseAndUpdateState runs condensation for a session and updates state afterward.
   800→// Returns true if condensation succeeded.
   801→func (s *ManualCommitStrategy) condenseAndUpdateState(
   802→	logCtx context.Context,
   803→	repo *git.Repository,
   804→	checkpointID id.CheckpointID,
   805→	state *SessionState,
   806→	head *plumbing.Reference,
   807→	shadowBranchName string,
   808→	shadowBranchesToDelete map[string]struct{},
   809→	committedFiles map[string]struct{},
   810→) bool {
   811→	result, err := s.CondenseSession(repo, checkpointID, state, committedFiles)
   812→	if err != nil {
   813→		fmt.Fprintf(os.Stderr, "[entire] Warning: condensation failed for session %s: %v\n",
   814→			state.SessionID, err)
   815→		logging.Warn(logCtx, "post-commit: condensation failed",
   816→			slog.String("session_id", state.SessionID),
   817→			slog.String("error", err.Error()),
   818→		)
   819→		return false
   820→	}
   821→
   822→	// Track this shadow branch for cleanup
   823→	shadowBranchesToDelete[shadowBranchName] = struct{}{}
   824→
   825→	// Update session state for the new base commit
   826→	newHead := head.Hash().String()
   827→	state.BaseCommit = newHead
   828→	state.AttributionBaseCommit = newHead
   829→	state.StepCount = 0
   830→	state.CheckpointTranscriptStart = result.TotalTranscriptLines
   831→
   832→	// Clear attribution tracking — condensation already used these values
   833→	state.PromptAttributions = nil
   834→	state.PendingPromptAttribution = nil
   835→	state.FilesTouched = nil
   836→
   837→	// Save checkpoint ID so subsequent commits can reuse it (e.g., amend restores trailer)
   838→	state.LastCheckpointID = checkpointID
   839→
   840→	shortID := state.SessionID
   841→	if len(shortID) > 8 {
   842→		shortID = shortID[:8]
   843→	}
   844→	fmt.Fprintf(os.Stderr, "[entire] Condensed session %s: %s (%d checkpoints)\n",
   845→		shortID, result.CheckpointID, result.CheckpointsCount)
   846→
   847→	logging.Info(logCtx, "session condensed",
   848→		slog.String("strategy", "manual-commit"),
   849→		slog.String("checkpoint_id", result.CheckpointID.String()),
   850→		slog.Int("checkpoints_condensed", result.CheckpointsCount),
   851→		slog.Int("transcript_lines", result.TotalTranscriptLines),
   852→	)
   853→
   854→	return true
   855→}
   856→
   857→// updateBaseCommitIfChanged updates BaseCommit to newHead if it changed.
   858→// Only updates ACTIVE sessions. IDLE/ENDED sessions should NOT have their
   859→// BaseCommit updated, as this would cause them to be incorrectly associated
   860→// with a new shadow branch and potentially condensed on future commits.
   861→func (s *ManualCommitStrategy) updateBaseCommitIfChanged(logCtx context.Context, state *SessionState, newHead string) {
   862→	// Only update ACTIVE sessions. IDLE/ENDED sessions are kept around for
   863→	// LastCheckpointID reuse and should not be advanced to HEAD.
   864→	if !state.Phase.IsActive() {
   865→		logging.Debug(logCtx, "post-commit: updateBaseCommitIfChanged skipped non-active session",
   866→			slog.String("session_id", state.SessionID),
   867→			slog.String("phase", string(state.Phase)),
   868→		)
   869→		return
   870→	}
   871→	if state.BaseCommit != newHead {
   872→		state.BaseCommit = newHead
   873→		logging.Debug(logCtx, "post-commit: updated BaseCommit",
   874→			slog.String("session_id", state.SessionID),
   875→			slog.String("new_head", truncateHash(newHead)),
   876→		)
   877→	}
   878→}
   879→
   880→// postCommitUpdateBaseCommitOnly updates BaseCommit for all sessions on the current
   881→// worktree when a commit has no Entire-Checkpoint trailer. This prevents BaseCommit
   882→// from going stale, which would cause future PrepareCommitMsg calls to skip the
   883→// session (BaseCommit != currentHeadHash filter).
   884→//
   885→// Unlike the full PostCommit flow, this does NOT fire EventGitCommit or trigger
   886→// condensation — it only keeps BaseCommit in sync with HEAD.
   887→func (s *ManualCommitStrategy) postCommitUpdateBaseCommitOnly(logCtx context.Context, head *plumbing.Reference) {
   888→	worktreePath, err := GetWorktreePath()
   889→	if err != nil {
   890→		return // Silent failure — hooks must be resilient
   891→	}
   892→
   893→	sessions, err := s.findSessionsForWorktree(worktreePath)
   894→	if err != nil || len(sessions) == 0 {
   895→		return
   896→	}
   897→
   898→	newHead := head.Hash().String()
   899→	for _, state := range sessions {
   900→		// Only update active sessions. Idle/ended sessions are kept around for
   901→		// LastCheckpointID reuse and should not be advanced to HEAD.
   902→		if !state.Phase.IsActive() {
   903→			continue
   904→		}
   905→		if state.BaseCommit != newHead {
   906→			logging.Debug(logCtx, "post-commit (no trailer): updating BaseCommit",
   907→				slog.String("session_id", state.SessionID),
   908→				slog.String("old_base", truncateHash(state.BaseCommit)),
   909→				slog.String("new_head", truncateHash(newHead)),
   910→			)
   911→			state.BaseCommit = newHead
   912→			if err := s.saveSessionState(state); err != nil {
   913→				fmt.Fprintf(os.Stderr, "[entire] Warning: failed to update session state: %v\n", err)
   914→			}
   915→		}
   916→	}
   917→}
   918→
   919→// truncateHash safely truncates a git hash to 7 chars for logging.
   920→func truncateHash(h string) string {
   921→	if len(h) > 7 {
   922→		return h[:7]
   923→	}
   924→	return h
   925→}
   926→
   927→// filterSessionsWithNewContent returns sessions that have new transcript content
   928→// beyond what was already condensed.
   929→func (s *ManualCommitStrategy) filterSessionsWithNewContent(repo *git.Repository, sessions []*SessionState) []*SessionState {
   930→	var result []*SessionState
   931→
   932→	for _, state := range sessions {
   933→		hasNew, err := s.sessionHasNewContent(repo, state)
   934→		if err != nil {
   935→			// On error, include the session (fail open for hooks)
   936→			result = append(result, state)
   937→			continue
   938→		}
   939→		if hasNew {
   940→			result = append(result, state)
   941→		}
   942→	}
   943→
   944→	return result
   945→}
   946→
   947→// sessionHasNewContent checks if a session has new transcript content
   948→// beyond what was already condensed.
   949→func (s *ManualCommitStrategy) sessionHasNewContent(repo *git.Repository, state *SessionState) (bool, error) {
   950→	logCtx := logging.WithComponent(context.Background(), "manual-commit")
   951→
   952→	// Get shadow branch
   953→	shadowBranchName := getShadowBranchNameForCommit(state.BaseCommit, state.WorktreeID)
   954→	refName := plumbing.NewBranchReferenceName(shadowBranchName)
   955→	ref, err := repo.Reference(refName, true)
   956→	if err != nil {
   957→		// No shadow branch means no Stop has happened since the last condensation.
   958→		// However, the agent may have done work (including commits) without a Stop.
   959→		// Check the live transcript to detect this scenario.
   960→		logging.Debug(logCtx, "sessionHasNewContent: no shadow branch, checking live transcript",
   961→			slog.String("session_id", state.SessionID),
   962→			slog.String("shadow_branch", shadowBranchName),
   963→		)
   964→		return s.sessionHasNewContentFromLiveTranscript(repo, state)
   965→	}
   966→
   967→	commit, err := repo.CommitObject(ref.Hash())
   968→	if err != nil {
   969→		return false, fmt.Errorf("failed to get commit object: %w", err)
   970→	}
   971→
   972→	tree, err := commit.Tree()
   973→	if err != nil {
   974→		return false, fmt.Errorf("failed to get commit tree: %w", err)
   975→	}
   976→
   977→	// Look for transcript file
   978→	metadataDir := paths.EntireMetadataDir + "/" + state.SessionID
   979→	var transcriptLines int
   980→	var hasTranscriptFile bool
   981→
   982→	if file, fileErr := tree.File(metadataDir + "/" + paths.TranscriptFileName); fileErr == nil {
   983→		hasTranscriptFile = true
   984→		if content, contentErr := file.Contents(); contentErr == nil {
   985→			transcriptLines = countTranscriptItems(state.AgentType, content)
   986→		}
   987→	} else if file, fileErr := tree.File(metadataDir + "/" + paths.TranscriptFileNameLegacy); fileErr == nil {
   988→		hasTranscriptFile = true
   989→		if content, contentErr := file.Contents(); contentErr == nil {
   990→			transcriptLines = countTranscriptItems(state.AgentType, content)
   991→		}
   992→	}
   993→
   994→	// If shadow branch exists but has no transcript (e.g., carry-forward from mid-session commit),
   995→	// check if the session has FilesTouched. Carry-forward sets FilesTouched with remaining files.
   996→	if !hasTranscriptFile {
   997→		if len(state.FilesTouched) > 0 {
   998→			// Shadow branch has files from carry-forward - check if staged files overlap
   999→			// AND have matching content (content-aware check).
  1000→			stagedFiles := getStagedFiles(repo)
  1001→			if len(stagedFiles) > 0 {
  1002→				// PrepareCommitMsg context: check staged files overlap with content
  1003→				result := stagedFilesOverlapWithContent(repo, tree, stagedFiles, state.FilesTouched)
  1004→				logging.Debug(logCtx, "sessionHasNewContent: no transcript, carry-forward with staged files",
  1005→					slog.String("session_id", state.SessionID),
  1006→					slog.Int("files_touched", len(state.FilesTouched)),
  1007→					slog.Int("staged_files", len(stagedFiles)),
  1008→					slog.Bool("result", result),
  1009→				)
  1010→				return result, nil
  1011→			}
  1012→			// PostCommit context: no staged files, but we have carry-forward files.
  1013→			// Return true and let the caller do the overlap check with committed files.
  1014→			logging.Debug(logCtx, "sessionHasNewContent: no transcript, carry-forward without staged files (post-commit context)",
  1015→				slog.String("session_id", state.SessionID),
  1016→				slog.Int("files_touched", len(state.FilesTouched)),
  1017→			)
  1018→			return true, nil
  1019→		}
  1020→		// No transcript and no FilesTouched - fall back to live transcript check
  1021→		logging.Debug(logCtx, "sessionHasNewContent: no transcript and no files touched, checking live transcript",
  1022→			slog.String("session_id", state.SessionID),
  1023→		)
  1024→		return s.sessionHasNewContentFromLiveTranscript(repo, state)
  1025→	}
  1026→
  1027→	// Check if there's new content to condense. Two cases:
  1028→	// 1. Transcript has grown since last condensation (new prompts/responses)
  1029→	// 2. FilesTouched has files not yet committed (carry-forward scenario)
  1030→	//
  1031→	// For PrepareCommitMsg context, we verify staged files overlap with session's files
  1032→	// using content-aware matching to detect reverted files.
  1033→	// For PostCommit context, getStagedFiles() is empty (files already committed),
  1034→	// so we return true and let the caller do the overlap check via filesOverlapWithContent.
  1035→
  1036→	hasTranscriptGrowth := transcriptLines > state.CheckpointTranscriptStart
  1037→	hasUncommittedFiles := len(state.FilesTouched) > 0
  1038→
  1039→	logging.Debug(logCtx, "sessionHasNewContent: transcript check",
  1040→		slog.String("session_id", state.SessionID),
  1041→		slog.Int("transcript_lines", transcriptLines),
  1042→		slog.Int("checkpoint_transcript_start", state.CheckpointTranscriptStart),
  1043→		slog.Bool("has_transcript_growth", hasTranscriptGrowth),
  1044→		slog.Bool("has_uncommitted_files", hasUncommittedFiles),
  1045→	)
  1046→
  1047→	if !hasTranscriptGrowth && !hasUncommittedFiles {
  1048→		return false, nil // No new content and no carry-forward files
  1049→	}
  1050→
  1051→	// Check if staged files overlap with session's files with content-aware matching.
  1052→	// This is primarily for PrepareCommitMsg; in PostCommit, stagedFiles is empty.
  1053→	stagedFiles := getStagedFiles(repo)
  1054→	if len(stagedFiles) > 0 {
  1055→		result := stagedFilesOverlapWithContent(repo, tree, stagedFiles, state.FilesTouched)
  1056→		logging.Debug(logCtx, "sessionHasNewContent: staged files overlap check",
  1057→			slog.String("session_id", state.SessionID),
  1058→			slog.Int("staged_files", len(stagedFiles)),
  1059→			slog.Bool("result", result),
  1060→		)
  1061→		return result, nil
  1062→	}
  1063→
  1064→	// No staged files - either PostCommit context or edge case.
  1065→	// Return transcript growth status. For PostCommit with hasTranscriptFile=true,
  1066→	// if there's no transcript growth, the session hasn't done new work since last checkpoint.
  1067→	// (Carry-forward creates a shadow branch WITHOUT transcript, handled in the block above.)
  1068→	logging.Debug(logCtx, "sessionHasNewContent: no staged files, returning transcript growth",
  1069→		slog.String("session_id", state.SessionID),
  1070→		slog.Bool("has_transcript_growth", hasTranscriptGrowth),
  1071→		slog.Bool("has_uncommitted_files", hasUncommittedFiles),
  1072→	)
  1073→	return hasTranscriptGrowth, nil
  1074→}
  1075→
  1076→// sessionHasNewContentFromLiveTranscript checks if a session has new content
  1077→// by examining the live transcript file. This is used when no shadow branch exists
  1078→// (i.e., no Stop has happened yet) but the agent may have done work.
  1079→//
  1080→// Returns true if:
  1081→//  1. The transcript has grown since the last condensation, AND
  1082→//  2. The new transcript portion contains file modifications, AND
  1083→//  3. At least one modified file overlaps with the currently staged files
  1084→//
  1085→// The overlap check ensures we don't add checkpoint trailers to commits that are
  1086→// unrelated to the agent's recent changes.
  1087→//
  1088→// This handles the scenario where the agent commits mid-session before Stop.
  1089→func (s *ManualCommitStrategy) sessionHasNewContentFromLiveTranscript(repo *git.Repository, state *SessionState) (bool, error) {
  1090→	logCtx := logging.WithComponent(context.Background(), "checkpoint")
  1091→
  1092→	modifiedFiles, ok := s.extractNewModifiedFilesFromLiveTranscript(state)
  1093→	if !ok || len(modifiedFiles) == 0 {
  1094→		return false, nil
  1095→	}
  1096→
  1097→	logging.Debug(logCtx, "live transcript check: found file modifications",
  1098→		slog.String("session_id", state.SessionID),
  1099→		slog.Int("modified_files", len(modifiedFiles)),
  1100→	)
  1101→
  1102→	// Check if any modified files overlap with currently staged files
  1103→	// This ensures we only add checkpoint trailers to commits that include
  1104→	// files the agent actually modified
  1105→	stagedFiles := getStagedFiles(repo)
  1106→
  1107→	logging.Debug(logCtx, "live transcript check: comparing staged vs modified",
  1108→		slog.String("session_id", state.SessionID),
  1109→		slog.Int("staged_files", len(stagedFiles)),
  1110→		slog.Int("modified_files", len(modifiedFiles)),
  1111→	)
  1112→
  1113→	if !hasOverlappingFiles(stagedFiles, modifiedFiles) {
  1114→		logging.Debug(logCtx, "live transcript check: no overlap between staged and modified files",
  1115→			slog.String("session_id", state.SessionID),
  1116→		)
  1117→		return false, nil // No overlap - staged files are unrelated to agent's work
  1118→	}
  1119→
  1120→	return true, nil
  1121→}
  1122→
  1123→// extractFilesFromLiveTranscript extracts modified file paths from the live transcript.
  1124→// Returns empty slice if extraction fails (fail-open behavior for hooks).
  1125→// Extracts files from the transcript starting at CheckpointTranscriptStart, which gives
  1126→// files touched since the last condensation — used for carry-forward computation.
  1127→func (s *ManualCommitStrategy) extractFilesFromLiveTranscript(state *SessionState) []string {
  1128→	return s.extractModifiedFilesFromLiveTranscript(state, state.CheckpointTranscriptStart)
  1129→}
  1130→
  1131→// extractNewModifiedFilesFromLiveTranscript extracts modified files from the live
  1132→// transcript that are NEW since the last condensation. Returns the normalized file list
  1133→// and whether the extraction succeeded. Used by sessionHasNewContentFromLiveTranscript
  1134→// to detect agent work.
  1135→func (s *ManualCommitStrategy) extractNewModifiedFilesFromLiveTranscript(state *SessionState) ([]string, bool) {
  1136→	logCtx := logging.WithComponent(context.Background(), "checkpoint")
  1137→
  1138→	if state.TranscriptPath == "" || state.AgentType == "" {
  1139→		return nil, false
  1140→	}
  1141→
  1142→	ag, err := agent.GetByAgentType(state.AgentType)
  1143→	if err != nil {
  1144→		return nil, false
  1145→	}
  1146→
  1147→	// Ensure transcript file is up-to-date (OpenCode creates/refreshes it via `opencode export`).
  1148→	// Only wait for flush when the session is active — for idle/ended sessions the
  1149→	// transcript is already fully flushed (the Stop hook completed the flush).
  1150→	// Skipping the wait avoids a 3s timeout per session in prepare-commit-msg/post-commit hooks.
  1151→	if state.Phase.IsActive() {
  1152→		if preparer, ok := ag.(agent.TranscriptPreparer); ok {
  1153→			if prepErr := preparer.PrepareTranscript(state.TranscriptPath); prepErr != nil {
  1154→				logging.Debug(logCtx, "prepare transcript failed",
  1155→					slog.String("session_id", state.SessionID),
  1156→					slog.String("agent_type", string(state.AgentType)),
  1157→					slog.String("transcript_path", state.TranscriptPath),
  1158→					slog.Any("error", prepErr),
  1159→				)
  1160→			}
  1161→		}
  1162→	}
  1163→
  1164→	analyzer, ok := ag.(agent.TranscriptAnalyzer)
  1165→	if !ok {
  1166→		return nil, false
  1167→	}
  1168→
  1169→	// Check if transcript has grown since last condensation
  1170→	currentPos, err := analyzer.GetTranscriptPosition(state.TranscriptPath)
  1171→	if err != nil {
  1172→		return nil, false
  1173→	}
  1174→	if currentPos <= state.CheckpointTranscriptStart {
  1175→		logging.Debug(logCtx, "live transcript check: no new content",
  1176→			slog.String("session_id", state.SessionID),
  1177→			slog.Int("current_pos", currentPos),
  1178→			slog.Int("start_offset", state.CheckpointTranscriptStart),
  1179→		)
  1180→		return nil, true // No new content, but extraction succeeded
  1181→	}
  1182→
  1183→	return s.extractModifiedFilesFromLiveTranscript(state, state.CheckpointTranscriptStart), true
  1184→}
  1185→
  1186→// extractModifiedFilesFromLiveTranscript extracts modified files from the live transcript
  1187→// (including subagent transcripts) starting from the given offset, and normalizes them
  1188→// to repo-relative paths. Returns the normalized file list.
  1189→func (s *ManualCommitStrategy) extractModifiedFilesFromLiveTranscript(state *SessionState, offset int) []string {
  1190→	logCtx := logging.WithComponent(context.Background(), "checkpoint")
  1191→
  1192→	if state.TranscriptPath == "" || state.AgentType == "" {
  1193→		return nil
  1194→	}
  1195→
  1196→	ag, err := agent.GetByAgentType(state.AgentType)
  1197→	if err != nil {
  1198→		return nil
  1199→	}
  1200→
  1201→	// Ensure transcript file is up-to-date (OpenCode creates/refreshes it via `opencode export`).
  1202→	// Only wait for flush when the session is active — for idle/ended sessions the
  1203→	// transcript is already fully flushed (the Stop hook completed the flush).
  1204→	if state.Phase.IsActive() {
  1205→		if preparer, ok := ag.(agent.TranscriptPreparer); ok {
  1206→			if prepErr := preparer.PrepareTranscript(state.TranscriptPath); prepErr != nil {
  1207→				logging.Debug(logCtx, "prepare transcript failed",
  1208→					slog.String("session_id", state.SessionID),
  1209→					slog.String("agent_type", string(state.AgentType)),
  1210→					slog.String("transcript_path", state.TranscriptPath),
  1211→					slog.Any("error", prepErr),
  1212→				)
  1213→			}
  1214→		}
  1215→	}
  1216→
  1217→	analyzer, ok := ag.(agent.TranscriptAnalyzer)
  1218→	if !ok {
  1219→		return nil
  1220→	}
  1221→
  1222→	var modifiedFiles []string
  1223→
  1224→	// For Claude Code, use ExtractAllModifiedFiles which parses the main transcript
  1225→	// AND subagent transcripts in a single pass, avoiding redundant parsing.
  1226→	if state.AgentType == agent.AgentTypeClaudeCode {
  1227→		subagentsDir := filepath.Join(filepath.Dir(state.TranscriptPath), state.SessionID, "subagents")
  1228→		allFiles, extractErr := claudecode.ExtractAllModifiedFiles(state.TranscriptPath, offset, subagentsDir)
  1229→		if extractErr != nil {
  1230→			logging.Debug(logCtx, "extractModifiedFilesFromLiveTranscript: extraction failed",
  1231→				slog.String("session_id", state.SessionID),
  1232→				slog.String("error", extractErr.Error()),
  1233→			)
  1234→		} else {
  1235→			modifiedFiles = allFiles
  1236→		}
  1237→	} else {
  1238→		files, _, err := analyzer.ExtractModifiedFilesFromOffset(state.TranscriptPath, offset)
  1239→		if err != nil {
  1240→			logging.Debug(logCtx, "extractModifiedFilesFromLiveTranscript: main transcript extraction failed",
  1241→				slog.String("transcript_path", state.TranscriptPath),
  1242→				slog.Any("error", err),
  1243→			)
  1244→		} else {
  1245→			modifiedFiles = files
  1246→		}
  1247→	}
  1248→
  1249→	if len(modifiedFiles) == 0 {
  1250→		return nil
  1251→	}
  1252→
  1253→	// Normalize to repo-relative paths.
  1254→	// Transcript tool_use entries contain absolute paths (e.g., /Users/alex/project/src/main.go)
  1255→	// but getStagedFiles/committedFiles use repo-relative paths (e.g., src/main.go).
  1256→	basePath := state.WorktreePath
  1257→	if basePath == "" {
  1258→		if wp, wpErr := GetWorktreePath(); wpErr == nil {
  1259→			basePath = wp
  1260→		}
  1261→	}
  1262→	if basePath != "" {
  1263→		normalized := make([]string, 0, len(modifiedFiles))
  1264→		for _, f := range modifiedFiles {
  1265→			if rel := paths.ToRelativePath(f, basePath); rel != "" {
  1266→				normalized = append(normalized, rel)
  1267→			} else {
  1268→				normalized = append(normalized, f)
  1269→			}
  1270→		}
  1271→		modifiedFiles = normalized
  1272→	}
  1273→
  1274→	return modifiedFiles
  1275→}
  1276→
  1277→// addTrailerForAgentCommit handles the fast path when an agent is committing
  1278→// (ACTIVE session + no TTY). Generates a checkpoint ID and adds the trailer
  1279→// directly, bypassing content detection and interactive prompts.
  1280→func (s *ManualCommitStrategy) addTrailerForAgentCommit(logCtx context.Context, commitMsgFile string, state *SessionState, source string) error {
  1281→	cpID, err := id.Generate()
  1282→	if err != nil {
  1283→		return nil //nolint:nilerr // Hook must be silent on failure
  1284→	}
  1285→
  1286→	content, err := os.ReadFile(commitMsgFile) //nolint:gosec // commitMsgFile is provided by git hook
  1287→	if err != nil {
  1288→		return nil //nolint:nilerr // Hook must be silent on failure
  1289→	}
  1290→
  1291→	message := string(content)
  1292→
  1293→	// Don't add if trailer already exists
  1294→	if _, found := trailers.ParseCheckpoint(message); found {
  1295→		return nil
  1296→	}
  1297→
  1298→	message = addCheckpointTrailer(message, cpID)
  1299→
  1300→	logging.Info(logCtx, "prepare-commit-msg: agent commit trailer added",
  1301→		slog.String("strategy", "manual-commit"),
  1302→		slog.String("source", source),
  1303→		slog.String("checkpoint_id", cpID.String()),
  1304→		slog.String("session_id", state.SessionID),
  1305→	)
  1306→
  1307→	if err := os.WriteFile(commitMsgFile, []byte(message), 0o600); err != nil {
  1308→		return nil //nolint:nilerr // Hook must be silent on failure
  1309→	}
  1310→	return nil
  1311→}
  1312→
  1313→// addCheckpointTrailer adds the Entire-Checkpoint trailer to a commit message.
  1314→// Handles proper trailer formatting (blank line before trailers if needed).
  1315→func addCheckpointTrailer(message string, checkpointID id.CheckpointID) string {
  1316→	trailer := trailers.CheckpointTrailerKey + ": " + checkpointID.String()
  1317→
  1318→	// If message already ends with trailers (lines starting with key:), just append
  1319→	// Otherwise, add a blank line first
  1320→	lines := strings.Split(strings.TrimRight(message, "\n"), "\n")
  1321→
  1322→	// Check if the message already ends with a trailer paragraph.
  1323→	// Git trailers must be in a separate paragraph (preceded by a blank line).
  1324→	// A single-paragraph message (e.g., just a subject line) cannot have trailers,
  1325→	// even if the subject contains ": " (like conventional commits: "docs: Add foo").
  1326→	//
  1327→	// Scan from the bottom: find the last paragraph of non-comment content,
  1328→	// then check if it looks like trailers AND has a blank line above it.
  1329→	hasTrailers := false
  1330→	i := len(lines) - 1
  1331→
  1332→	// Skip trailing comment lines
  1333→	for i >= 0 && strings.HasPrefix(strings.TrimSpace(lines[i]), "#") {
  1334→		i--
  1335→	}
  1336→
  1337→	// Check if the last non-comment line looks like a trailer
  1338→	if i >= 0 {
  1339→		line := strings.TrimSpace(lines[i])
  1340→		if line != "" && strings.Contains(line, ": ") {
  1341→			// Found a trailer-like line. Now scan upward past the trailer block
  1342→			// to verify there's a blank line (paragraph separator) above it.
  1343→			for i > 0 {
  1344→				i--
  1345→				above := strings.TrimSpace(lines[i])
  1346→				if strings.HasPrefix(above, "#") {
  1347→					continue
  1348→				}
  1349→				if above == "" {
  1350→					// Blank line found above trailer block — real trailers
  1351→					hasTrailers = true
  1352→					break
  1353→				}
  1354→				if !strings.Contains(above, ": ") {
  1355→					// Non-trailer, non-blank line — this is message body, not trailers
  1356→					break
  1357→				}
  1358→				// Another trailer-like line, keep scanning upward
  1359→			}
  1360→		}
  1361→	}
  1362→
  1363→	if hasTrailers {
  1364→		// Append trailer directly
  1365→		return strings.TrimRight(message, "\n") + "\n" + trailer + "\n"
  1366→	}
  1367→
  1368→	// Add blank line before trailer
  1369→	return strings.TrimRight(message, "\n") + "\n\n" + trailer + "\n"
  1370→}
  1371→
  1372→// addCheckpointTrailerWithComment adds the Entire-Checkpoint trailer with an explanatory comment.
  1373→// The trailer is placed above the git comment block but below the user's message area,
  1374→// with a comment explaining that the user can remove it if they don't want to link the commit
  1375→// to the agent session. If prompt is non-empty, it's shown as context.
  1376→func addCheckpointTrailerWithComment(message string, checkpointID id.CheckpointID, agentName, prompt string) string {
  1377→	trailer := trailers.CheckpointTrailerKey + ": " + checkpointID.String()
  1378→	commentLines := []string{
  1379→		"# Remove the Entire-Checkpoint trailer above if you don't want to link this commit to " + agentName + " session context.",
  1380→	}
  1381→	if prompt != "" {
  1382→		commentLines = append(commentLines, "# Last Prompt: "+prompt)
  1383→	}
  1384→	commentLines = append(commentLines, "# The trailer will be added to your next commit based on this branch.")
  1385→	comment := strings.Join(commentLines, "\n")
  1386→
  1387→	lines := strings.Split(message, "\n")
  1388→
  1389→	// Find where the git comment block starts (first # line)
  1390→	commentStart := -1
  1391→	for i, line := range lines {
  1392→		if strings.HasPrefix(line, "#") {
  1393→			commentStart = i
  1394→			break
  1395→		}
  1396→	}
  1397→
  1398→	if commentStart == -1 {
  1399→		// No git comments, append trailer at the end
  1400→		return strings.TrimRight(message, "\n") + "\n\n" + trailer + "\n" + comment + "\n"
  1401→	}
  1402→
  1403→	// Split into user content and git comments
  1404→	userContent := strings.Join(lines[:commentStart], "\n")
  1405→	gitComments := strings.Join(lines[commentStart:], "\n")
  1406→
  1407→	// Build result: user content, blank line, trailer, comment, blank line, git comments
  1408→	userContent = strings.TrimRight(userContent, "\n")
  1409→	if userContent == "" {
  1410→		// No user content yet - leave space for them to type, then trailer
  1411→		// Two newlines: first for user's message line, second for blank separator
  1412→		return "\n\n" + trailer + "\n" + comment + "\n\n" + gitComments
  1413→	}
  1414→	return userContent + "\n\n" + trailer + "\n" + comment + "\n\n" + gitComments
  1415→}
  1416→
  1417→// InitializeSession creates session state for a new session or updates an existing one.
  1418→// This implements the optional SessionInitializer interface.
  1419→// Called during UserPromptSubmit to allow git hooks to detect active sessions.
  1420→//
  1421→// If the session already exists and HEAD has moved (e.g., user committed), updates
  1422→// BaseCommit to the new HEAD so future checkpoints go to the correct shadow branch.
  1423→//
  1424→// If there's an existing shadow branch with commits from a different session ID,
  1425→// returns a SessionIDConflictError to prevent orphaning existing session work.
  1426→//
  1427→// agentType is the human-readable name of the agent (e.g., "Claude Code").
  1428→// transcriptPath is the path to the live transcript file (for mid-session commit detection).
  1429→// userPrompt is the user's prompt text (stored truncated as FirstPrompt for display).
  1430→func (s *ManualCommitStrategy) InitializeSession(sessionID string, agentType agent.AgentType, transcriptPath string, userPrompt string) error {
  1431→	repo, err := OpenRepository()
  1432→	if err != nil {
  1433→		return fmt.Errorf("failed to open git repository: %w", err)
  1434→	}
  1435→
  1436→	// Check if session already exists
  1437→	state, err := s.loadSessionState(sessionID)
  1438→	if err != nil {
  1439→		return fmt.Errorf("failed to check session state: %w", err)
  1440→	}
  1441→
  1442→	if state != nil && state.BaseCommit != "" {
  1443→		// Session is fully initialized — apply phase transition for TurnStart.
  1444→		if transErr := TransitionAndLog(state, session.EventTurnStart, session.TransitionContext{}, session.NoOpActionHandler{}); transErr != nil {
  1445→			fmt.Fprintf(os.Stderr, "[entire] Warning: turn start transition failed: %v\n", transErr)
  1446→		}
  1447→
  1448→		// Generate a new TurnID for each turn (correlates carry-forward checkpoints)
  1449→		turnID, err := id.Generate()
  1450→		if err != nil {
  1451→			return fmt.Errorf("failed to generate turn ID: %w", err)
  1452→		}
  1453→		state.TurnID = turnID.String()
  1454→
  1455→		// Backfill AgentType if empty or set to the generic default "Agent"
  1456→		if !isSpecificAgentType(state.AgentType) && agentType != "" {
  1457→			state.AgentType = agentType
  1458→		}
  1459→
  1460→		// Backfill FirstPrompt if empty (for sessions created before the first_prompt field was added)
  1461→		if state.FirstPrompt == "" && userPrompt != "" {
  1462→			state.FirstPrompt = truncatePromptForStorage(userPrompt)
  1463→		}
  1464→
  1465→		// Update transcript path if provided (may change on session resume)
  1466→		if transcriptPath != "" && state.TranscriptPath != transcriptPath {
  1467→			state.TranscriptPath = transcriptPath
  1468→		}
  1469→
  1470→		// Clear checkpoint IDs on every new prompt.
  1471→		// LastCheckpointID is set during PostCommit, cleared at new prompt.
  1472→		// TurnCheckpointIDs tracks mid-turn checkpoints for stop-time finalization.
  1473→		state.LastCheckpointID = ""
  1474→		state.TurnCheckpointIDs = nil
  1475→
  1476→		// Calculate attribution at prompt start (BEFORE agent makes any changes)
  1477→		// This captures user edits since the last checkpoint (or base commit for first prompt).
  1478→		// IMPORTANT: Always calculate attribution, even for the first checkpoint, to capture
  1479→		// user edits made before the first prompt. The inner CalculatePromptAttribution handles
  1480→		// nil lastCheckpointTree by falling back to baseTree.
  1481→		promptAttr := s.calculatePromptAttributionAtStart(repo, state)
  1482→		state.PendingPromptAttribution = &promptAttr
  1483→
  1484→		// Check if HEAD has moved (user pulled/rebased or committed)
  1485→		// migrateShadowBranchIfNeeded handles renaming the shadow branch and updating state.BaseCommit
  1486→		if _, err := s.migrateShadowBranchIfNeeded(repo, state); err != nil {
  1487→			return fmt.Errorf("failed to check/migrate shadow branch: %w", err)
  1488→		}
  1489→
  1490→		if err := s.saveSessionState(state); err != nil {
  1491→			return fmt.Errorf("failed to update session state: %w", err)
  1492→		}
  1493→		return nil
  1494→	}
  1495→	// If state exists but BaseCommit is empty, it's a partial state from concurrent warning
  1496→	// Continue below to properly initialize it
  1497→
  1498→	// Initialize new session
  1499→	state, err = s.initializeSession(repo, sessionID, agentType, transcriptPath, userPrompt)
  1500→	if err != nil {
  1501→		return fmt.Errorf("failed to initialize session: %w", err)
  1502→	}
  1503→
  1504→	// Apply phase transition: new session starts as ACTIVE.
  1505→	if transErr := TransitionAndLog(state, session.EventTurnStart, session.TransitionContext{}, session.NoOpActionHandler{}); transErr != nil {
  1506→		fmt.Fprintf(os.Stderr, "[entire] Warning: turn start transition failed: %v\n", transErr)
  1507→	}
  1508→
  1509→	// Calculate attribution for pre-prompt edits
  1510→	// This captures any user edits made before the first prompt
  1511→	promptAttr := s.calculatePromptAttributionAtStart(repo, state)
  1512→	state.PendingPromptAttribution = &promptAttr
  1513→	if err = s.saveSessionState(state); err != nil {
  1514→		return fmt.Errorf("failed to save attribution: %w", err)
  1515→	}
  1516→
  1517→	fmt.Fprintf(os.Stderr, "Initialized shadow session: %s\n", sessionID)
  1518→	return nil
  1519→}
  1520→
  1521→// calculatePromptAttributionAtStart calculates attribution at prompt start (before agent runs).
  1522→// This captures user changes since the last checkpoint - no filtering needed since
  1523→// the agent hasn't made any changes yet.
  1524→//
  1525→// IMPORTANT: This reads from the worktree (not staging area) to match what WriteTemporary
  1526→// captures in checkpoints. If we read staged content but checkpoints capture worktree content,
  1527→// unstaged changes would be in the checkpoint but not counted in PromptAttribution, causing
  1528→// them to be incorrectly attributed to the agent later.
  1529→func (s *ManualCommitStrategy) calculatePromptAttributionAtStart(
  1530→	repo *git.Repository,
  1531→	state *SessionState,
  1532→) PromptAttribution {
  1533→	logCtx := logging.WithComponent(context.Background(), "attribution")
  1534→	nextCheckpointNum := state.StepCount + 1
  1535→	result := PromptAttribution{CheckpointNumber: nextCheckpointNum}
  1536→
  1537→	// Get last checkpoint tree from shadow branch (if it exists)
  1538→	// For the first checkpoint, no shadow branch exists yet - this is fine,
  1539→	// CalculatePromptAttribution will use baseTree as the reference instead.
  1540→	var lastCheckpointTree *object.Tree
  1541→	shadowBranchName := checkpoint.ShadowBranchNameForCommit(state.BaseCommit, state.WorktreeID)
  1542→	refName := plumbing.NewBranchReferenceName(shadowBranchName)
  1543→	ref, err := repo.Reference(refName, true)
  1544→	if err != nil {
  1545→		logging.Debug(logCtx, "prompt attribution: no shadow branch yet (first checkpoint)",
  1546→			slog.String("shadow_branch", shadowBranchName))
  1547→		// Continue with lastCheckpointTree = nil
  1548→	} else {
  1549→		shadowCommit, err := repo.CommitObject(ref.Hash())
  1550→		if err != nil {
  1551→			logging.Debug(logCtx, "prompt attribution: failed to get shadow commit",
  1552→				slog.String("shadow_ref", ref.Hash().String()),
  1553→				slog.String("error", err.Error()))
  1554→			// Continue with lastCheckpointTree = nil
  1555→		} else {
  1556→			lastCheckpointTree, err = shadowCommit.Tree()
  1557→			if err != nil {
  1558→				logging.Debug(logCtx, "prompt attribution: failed to get shadow tree",
  1559→					slog.String("error", err.Error()))
  1560→				// Continue with lastCheckpointTree = nil
  1561→			}
  1562→		}
  1563→	}
  1564→
  1565→	// Get base tree for agent lines calculation
  1566→	var baseTree *object.Tree
  1567→	if baseCommit, err := repo.CommitObject(plumbing.NewHash(state.BaseCommit)); err == nil {
  1568→		if tree, treeErr := baseCommit.Tree(); treeErr == nil {
  1569→			baseTree = tree
  1570→		} else {
  1571→			logging.Debug(logCtx, "prompt attribution: base tree unavailable",
  1572→				slog.String("error", treeErr.Error()))
  1573→		}
  1574→	} else {
  1575→		logging.Debug(logCtx, "prompt attribution: base commit unavailable",
  1576→			slog.String("base_commit", state.BaseCommit),
  1577→			slog.String("error", err.Error()))
  1578→	}
  1579→
  1580→	worktree, err := repo.Worktree()
  1581→	if err != nil {
  1582→		logging.Debug(logCtx, "prompt attribution skipped: failed to get worktree",
  1583→			slog.String("error", err.Error()))
  1584→		return result
  1585→	}
  1586→
  1587→	// Get worktree status to find ALL changed files
  1588→	status, err := worktree.Status()
  1589→	if err != nil {
  1590→		logging.Debug(logCtx, "prompt attribution skipped: failed to get worktree status",
  1591→			slog.String("error", err.Error()))
  1592→		return result
  1593→	}
  1594→
  1595→	worktreeRoot := worktree.Filesystem.Root()
  1596→
  1597→	// Build map of changed files with their worktree content
  1598→	// IMPORTANT: We read from worktree (not staging area) to match what WriteTemporary
  1599→	// captures in checkpoints. This ensures attribution is consistent.
  1600→	changedFiles := make(map[string]string)
  1601→	for filePath, fileStatus := range status {
  1602→		// Skip unmodified files
  1603→		if fileStatus.Worktree == git.Unmodified && fileStatus.Staging == git.Unmodified {
  1604→			continue
  1605→		}
  1606→		// Skip .entire metadata directory (session data, not user code)
  1607→		if strings.HasPrefix(filePath, paths.EntireMetadataDir+"/") || strings.HasPrefix(filePath, ".entire/") {
  1608→			continue
  1609→		}
  1610→
  1611→		// Always read from worktree to match checkpoint behavior
  1612→		fullPath := filepath.Join(worktreeRoot, filePath)
  1613→		var content string
  1614→		if data, err := os.ReadFile(fullPath); err == nil { //nolint:gosec // filePath is from git worktree status
  1615→			// Use git's binary detection algorithm (matches getFileContent behavior).
  1616→			// Binary files are excluded from line-based attribution calculations.
  1617→			isBinary, binErr := binary.IsBinary(bytes.NewReader(data))
  1618→			if binErr == nil && !isBinary {
  1619→				content = string(data)
  1620→			}
  1621→		}
  1622→		// else: file deleted, unreadable, or binary - content remains empty string
  1623→
  1624→		changedFiles[filePath] = content
  1625→	}
  1626→
  1627→	// Use CalculatePromptAttribution from manual_commit_attribution.go
  1628→	result = CalculatePromptAttribution(baseTree, lastCheckpointTree, changedFiles, nextCheckpointNum)
  1629→
  1630→	return result
  1631→}
  1632→
  1633→// getStagedFiles returns a list of files staged for commit.
  1634→func getStagedFiles(repo *git.Repository) []string {
  1635→	worktree, err := repo.Worktree()
  1636→	if err != nil {
  1637→		return nil
  1638→	}
  1639→
  1640→	status, err := worktree.Status()
  1641→	if err != nil {
  1642→		return nil
  1643→	}
  1644→
  1645→	var staged []string
  1646→	for path, fileStatus := range status {
  1647→		// Check if file is staged (in index)
  1648→		if fileStatus.Staging != git.Unmodified && fileStatus.Staging != git.Untracked {
  1649→			staged = append(staged, path)
  1650→		}
  1651→	}
  1652→	return staged
  1653→}
  1654→
  1655→// getLastPrompt retrieves the most recent user prompt from a session's shadow branch.
  1656→// Returns empty string if no prompt can be retrieved.
  1657→func (s *ManualCommitStrategy) getLastPrompt(repo *git.Repository, state *SessionState) string {
  1658→	shadowBranchName := getShadowBranchNameForCommit(state.BaseCommit, state.WorktreeID)
  1659→	refName := plumbing.NewBranchReferenceName(shadowBranchName)
  1660→	ref, err := repo.Reference(refName, true)
  1661→	if err != nil {
  1662→		return ""
  1663→	}
  1664→
  1665→	// Extract session data to get prompts for commit message generation
  1666→	// Pass agent type to handle different transcript formats (JSONL for Claude, JSON for Gemini)
  1667→	// Pass 0 for checkpointTranscriptStart since we're extracting all prompts, not calculating token usage
  1668→	sessionData, err := s.extractSessionData(repo, ref.Hash(), state.SessionID, nil, state.AgentType, "", 0, state.Phase.IsActive())
  1669→	if err != nil || len(sessionData.Prompts) == 0 {
  1670→		return ""
  1671→	}
  1672→
  1673→	// Return the last prompt (most recent work before commit)
  1674→	return sessionData.Prompts[len(sessionData.Prompts)-1]
  1675→}
  1676→
  1677→// HandleTurnEnd dispatches strategy-specific actions emitted when an agent turn ends.
  1678→// The primary job is to finalize all checkpoints from this turn with the full transcript.
  1679→//
  1680→// During a turn, PostCommit writes provisional transcript data (whatever was available
  1681→// at commit time). HandleTurnEnd replaces that with the complete session transcript
  1682→// (from prompt to stop event), ensuring every checkpoint has the full context.
  1683→//
  1684→//nolint:unparam // error return required by interface but hooks must return nil
  1685→func (s *ManualCommitStrategy) HandleTurnEnd(state *SessionState) error {
  1686→	// Finalize all checkpoints from this turn with the full transcript.
  1687→	//
  1688→	// IMPORTANT: This is best-effort - errors are logged but don't fail the hook.
  1689→	// Failing here would prevent session cleanup and could leave state inconsistent.
  1690→	// The provisional transcript from PostCommit is already persisted, so the
  1691→	// checkpoint isn't lost - it just won't have the complete transcript.
  1692→	errCount := s.finalizeAllTurnCheckpoints(state)
  1693→	if errCount > 0 {
  1694→		logCtx := logging.WithComponent(context.Background(), "checkpoint")
  1695→		logging.Warn(logCtx, "HandleTurnEnd completed with errors (best-effort)",
  1696→			slog.String("session_id", state.SessionID),
  1697→			slog.Int("error_count", errCount),
  1698→		)
  1699→	}
  1700→	return nil
  1701→}
  1702→
  1703→// finalizeAllTurnCheckpoints replaces the provisional transcript in each checkpoint
  1704→// created during this turn with the full session transcript.
  1705→//
  1706→// This is called at turn end (stop hook). During the turn, PostCommit wrote whatever
  1707→// transcript was available at commit time. Now we have the complete transcript and
  1708→// replace it so every checkpoint has the full prompt-to-stop context.
  1709→//
  1710→// Returns the number of errors encountered (best-effort: continues processing on error).
  1711→func (s *ManualCommitStrategy) finalizeAllTurnCheckpoints(state *SessionState) int {
  1712→	if len(state.TurnCheckpointIDs) == 0 {
  1713→		return 0 // No mid-turn commits to finalize
  1714→	}
  1715→
  1716→	logCtx := logging.WithComponent(context.Background(), "checkpoint")
  1717→
  1718→	logging.Info(logCtx, "finalizing turn checkpoints with full transcript",
  1719→		slog.String("session_id", state.SessionID),
  1720→		slog.Int("checkpoint_count", len(state.TurnCheckpointIDs)),
  1721→	)
  1722→
  1723→	errCount := 0
  1724→
  1725→	// Read full transcript from live transcript file
  1726→	if state.TranscriptPath == "" {
  1727→		logging.Warn(logCtx, "finalize: no transcript path, skipping",
  1728→			slog.String("session_id", state.SessionID),
  1729→		)
  1730→		state.TurnCheckpointIDs = nil
  1731→		return 1 // Count as error - all checkpoints will be skipped
  1732→	}
  1733→
  1734→	fullTranscript, err := os.ReadFile(state.TranscriptPath)
  1735→	if err != nil || len(fullTranscript) == 0 {
  1736→		msg := "finalize: empty transcript, skipping"
  1737→		if err != nil {
  1738→			msg = "finalize: failed to read transcript, skipping"
  1739→		}
  1740→		logging.Warn(logCtx, msg,
  1741→			slog.String("session_id", state.SessionID),
  1742→			slog.String("transcript_path", state.TranscriptPath),
  1743→			slog.Any("error", err),
  1744→		)
  1745→		state.TurnCheckpointIDs = nil
  1746→		return 1 // Count as error - all checkpoints will be skipped
  1747→	}
  1748→
  1749→	// Extract prompts and context from the full transcript
  1750→	prompts := extractUserPrompts(state.AgentType, string(fullTranscript))
  1751→	contextBytes := generateContextFromPrompts(prompts)
  1752→
  1753→	// Redact secrets before writing — matches WriteCommitted behavior.
  1754→	// The live transcript on disk contains raw content; redaction must happen
  1755→	// before anything is persisted to the metadata branch.
  1756→	fullTranscript, err = redact.JSONLBytes(fullTranscript)
  1757→	if err != nil {
  1758→		logging.Warn(logCtx, "finalize: transcript redaction failed, skipping",
  1759→			slog.String("session_id", state.SessionID),
  1760→			slog.String("error", err.Error()),
  1761→		)
  1762→		state.TurnCheckpointIDs = nil
  1763→		return 1 // Count as error - all checkpoints will be skipped
  1764→	}
  1765→	for i, p := range prompts {
  1766→		prompts[i] = redact.String(p)
  1767→	}
  1768→	contextBytes = redact.Bytes(contextBytes)
  1769→
  1770→	// Open repository and create checkpoint store
  1771→	repo, err := OpenRepository()
  1772→	if err != nil {
  1773→		logging.Warn(logCtx, "finalize: failed to open repository",
  1774→			slog.String("error", err.Error()),
  1775→		)
  1776→		state.TurnCheckpointIDs = nil
  1777→		return 1 // Count as error - all checkpoints will be skipped
  1778→	}
  1779→	store := checkpoint.NewGitStore(repo)
  1780→
  1781→	// Update each checkpoint with the full transcript
  1782→	for _, cpIDStr := range state.TurnCheckpointIDs {
  1783→		cpID, parseErr := id.NewCheckpointID(cpIDStr)
  1784→		if parseErr != nil {
  1785→			logging.Warn(logCtx, "finalize: invalid checkpoint ID, skipping",
  1786→				slog.String("checkpoint_id", cpIDStr),
  1787→				slog.String("error", parseErr.Error()),
  1788→			)
  1789→			errCount++
  1790→			continue
  1791→		}
  1792→
  1793→		updateErr := store.UpdateCommitted(context.Background(), checkpoint.UpdateCommittedOptions{
  1794→			CheckpointID: cpID,
  1795→			SessionID:    state.SessionID,
  1796→			Transcript:   fullTranscript,
  1797→			Prompts:      prompts,
  1798→			Context:      contextBytes,
  1799→			Agent:        state.AgentType,
  1800→		})
  1801→		if updateErr != nil {
  1802→			logging.Warn(logCtx, "finalize: failed to update checkpoint",
  1803→				slog.String("checkpoint_id", cpIDStr),
  1804→				slog.String("error", updateErr.Error()),
  1805→			)
  1806→			errCount++
  1807→			continue
  1808→		}
  1809→
  1810→		logging.Info(logCtx, "finalize: checkpoint updated with full transcript",
  1811→			slog.String("checkpoint_id", cpIDStr),
  1812→			slog.String("session_id", state.SessionID),
  1813→		)
  1814→	}
  1815→
  1816→	// Clear turn checkpoint IDs. Do NOT update CheckpointTranscriptStart here — it was
  1817→	// already set correctly by PostCommit: condenseAndUpdateState sets it to the total
  1818→	// transcript lines when condensing, and carryForwardToNewShadowBranch resets it to 0
  1819→	// when carry-forward is active. Overwriting here would break carry-forward by making
  1820→	// sessionHasNewContent think the transcript is fully consumed (no growth).
  1821→	state.TurnCheckpointIDs = nil
  1822→
  1823→	return errCount
  1824→}
  1825→
  1826→// filesChangedInCommit returns the set of files changed in a commit by diffing against its parent.
  1827→func filesChangedInCommit(commit *object.Commit) map[string]struct{} {
  1828→	result := make(map[string]struct{})
  1829→
  1830→	commitTree, err := commit.Tree()
  1831→	if err != nil {
  1832→		return result
  1833→	}
  1834→
  1835→	var parentTree *object.Tree
  1836→	if commit.NumParents() > 0 {
  1837→		parent, err := commit.Parent(0)
  1838→		if err != nil {
  1839→			return result
  1840→		}
  1841→		parentTree, err = parent.Tree()
  1842→		if err != nil {
  1843→			return result
  1844→		}
  1845→	}
  1846→
  1847→	if parentTree == nil {
  1848→		// Initial commit — all files are new
  1849→		if iterErr := commitTree.Files().ForEach(func(f *object.File) error {
  1850→			result[f.Name] = struct{}{}
  1851→			return nil
  1852→		}); iterErr != nil {
  1853→			return result
  1854→		}
  1855→		return result
  1856→	}
  1857→
  1858→	changes, err := parentTree.Diff(commitTree)
  1859→	if err != nil {
  1860→		return result
  1861→	}
  1862→	for _, change := range changes {
  1863→		name := change.To.Name
  1864→		if name == "" {
  1865→			name = change.From.Name
  1866→		}
  1867→		result[name] = struct{}{}
  1868→	}
  1869→	return result
  1870→}
  1871→
  1872→// subtractFiles returns files that are NOT in the exclude set.
  1873→func subtractFiles(files []string, exclude map[string]struct{}) []string {
  1874→	var remaining []string
  1875→	for _, f := range files {
  1876→		if _, excluded := exclude[f]; !excluded {
  1877→			remaining = append(remaining, f)
  1878→		}
  1879→	}
  1880→	return remaining
  1881→}
  1882→
  1883→// carryForwardToNewShadowBranch creates a new shadow branch at the current HEAD
  1884→// containing the remaining uncommitted files and all session metadata.
  1885→// This enables the next commit to get its own unique checkpoint.
  1886→func (s *ManualCommitStrategy) carryForwardToNewShadowBranch(
  1887→	logCtx context.Context,
  1888→	repo *git.Repository,
  1889→	state *SessionState,
  1890→	remainingFiles []string,
  1891→) {
  1892→	store := checkpoint.NewGitStore(repo)
  1893→
  1894→	// Don't include metadata directory in carry-forward. The carry-forward branch
  1895→	// only needs to preserve file content for comparison - not the transcript.
  1896→	// Including the transcript would cause sessionHasNewContent to always return true
  1897→	// because CheckpointTranscriptStart is reset to 0 for carry-forward.
  1898→	result, err := store.WriteTemporary(context.Background(), checkpoint.WriteTemporaryOptions{
  1899→		SessionID:         state.SessionID,
  1900→		BaseCommit:        state.BaseCommit,
  1901→		WorktreeID:        state.WorktreeID,
  1902→		ModifiedFiles:     remainingFiles,
  1903→		MetadataDir:       "",
  1904→		MetadataDirAbs:    "",
  1905→		CommitMessage:     "carry forward: uncommitted session files",
  1906→		IsFirstCheckpoint: false,
  1907→	})
  1908→	if err != nil {
  1909→		logging.Warn(logCtx, "post-commit: carry-forward failed",
  1910→			slog.String("session_id", state.SessionID),
  1911→			slog.String("error", err.Error()),
  1912→		)
  1913→		return
  1914→	}
  1915→	if result.Skipped {
  1916→		logging.Debug(logCtx, "post-commit: carry-forward skipped (no changes)",
  1917→			slog.String("session_id", state.SessionID),
  1918→		)
  1919→		return
  1920→	}
  1921→
  1922→	// Update state for the carry-forward checkpoint.
  1923→	// CheckpointTranscriptStart = 0 is intentional: each checkpoint is self-contained with
  1924→	// the full transcript. This trades storage efficiency for simplicity:
  1925→	// - Pro: Each checkpoint is independently readable without needing to stitch together
  1926→	//   multiple checkpoints to understand the session history
  1927→	// - Con: For long sessions with multiple partial commits, each checkpoint includes
  1928→	//   the full transcript, which could be large
  1929→	// An alternative would be incremental checkpoints (only new content since last condensation),
  1930→	// but this would complicate checkpoint retrieval and require careful tracking of dependencies.
  1931→	state.StepCount = 1
  1932→	state.CheckpointTranscriptStart = 0
  1933→	state.LastCheckpointID = ""
  1934→	// NOTE: TurnCheckpointIDs is intentionally NOT cleared here. Those checkpoint
  1935→	// IDs from earlier in the turn still need finalization with the full transcript
  1936→	// when HandleTurnEnd runs at stop time.
  1937→
  1938→	logging.Info(logCtx, "post-commit: carried forward remaining files",
  1939→		slog.String("session_id", state.SessionID),
  1940→		slog.Int("remaining_files", len(remainingFiles)),
  1941→	)
  1942→}
  1943→
```

> TOOL

tool_use Grep
id: toolu_01ESvaaC7JhWBdQMwUigYNvD
```json
{
  "pattern": "setupSessionWithCheckpoint",
  "path": "/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/strategy",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result
id: toolu_01ESvaaC7JhWBdQMwUigYNvD
```
Found 2 files
cmd/entire/cli/strategy/phase_postcommit_test.go
cmd/entire/cli/strategy/mid_turn_commit_test.go
```

> AGENT

Now let me check the relevant parts of the code - the `PrepareTranscript` method and agent types to understand the sentinel wait behavior.

> TOOL

tool_use Grep
id: toolu_016RjLe2P3xpRFCNf2Bs5H6v
```json
{
  "pattern": "PrepareTranscript",
  "path": "/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/agent",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result
id: toolu_016RjLe2P3xpRFCNf2Bs5H6v
```
Found 4 files
cmd/entire/cli/agent/opencode/lifecycle_test.go
cmd/entire/cli/agent/opencode/lifecycle.go
cmd/entire/cli/agent/agent.go
cmd/entire/cli/agent/claudecode/lifecycle.go
```

> TOOL

tool_use Grep
id: toolu_014UK34GXzdf6aNT2jgpzdps
```json
{
  "pattern": "AgentTypeClaudeCode",
  "path": "/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/agent",
  "output_mode": "content",
  "head_limit": 10
}
```

> TOOL

tool_result
id: toolu_014UK34GXzdf6aNT2jgpzdps
```
cmd/entire/cli/agent/registry.go:101:	AgentTypeClaudeCode AgentType = "Claude Code"
cmd/entire/cli/agent/claudecode/claude.go:42:	return agent.AgentTypeClaudeCode

[Showing results with pagination = limit: 10, offset: 0]
```

> TOOL

tool_use Grep
id: toolu_01XYjjdUrGaYHiHipeUrstPH
```json
{
  "pattern": "func.*setupGitRepo",
  "path": "/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/strategy",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result
id: toolu_01XYjjdUrGaYHiHipeUrstPH
```
Found 1 file
cmd/entire/cli/strategy/phase_wiring_test.go
```

> TOOL

tool_use Grep
id: toolu_014bFwmHck6f5Afo1jD5XT6P
```json
{
  "pattern": "func setupGitRepo",
  "path": "/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/strategy/phase_wiring_test.go",
  "output_mode": "content",
  "-A": 30
}
```

> TOOL

tool_result
id: toolu_014bFwmHck6f5Afo1jD5XT6P
```
172:func setupGitRepo(t *testing.T) string {
173-	t.Helper()
174-
175-	dir := t.TempDir()
176-
177-	repo, err := git.PlainInit(dir, false)
178-	require.NoError(t, err)
179-
180-	// Configure git for commits
181-	cfg, err := repo.Config()
182-	require.NoError(t, err)
183-	cfg.User.Name = "Test User"
184-	cfg.User.Email = "test@test.com"
185-	err = repo.SetConfig(cfg)
186-	require.NoError(t, err)
187-
188-	// Create initial commit (required for HEAD to exist)
189-	wt, err := repo.Worktree()
190-	require.NoError(t, err)
191-
192-	// Create a test file
193-	testFile := filepath.Join(dir, "test.txt")
194-	require.NoError(t, writeTestFile(testFile, "initial content"))
195-
196-	_, err = wt.Add("test.txt")
197-	require.NoError(t, err)
198-
199-	_, err = wt.Commit("initial commit", &git.CommitOptions{})
200-	require.NoError(t, err)
201-
202-	return dir
```

> TOOL

tool_use Grep
id: toolu_01HsqU4Qpyo3b4M6ckBc7NUG
```json
{
  "pattern": "func.*PrepareTranscript",
  "path": "/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/agent/claudecode/lifecycle.go",
  "output_mode": "content",
  "-A": 30
}
```

> TOOL

tool_result
id: toolu_01HsqU4Qpyo3b4M6ckBc7NUG
```
126:func (c *ClaudeCodeAgent) PrepareTranscript(sessionRef string) error {
127-	waitForTranscriptFlush(sessionRef, time.Now())
128-	return nil
129-}
130-
131-// CalculateTokenUsage computes token usage from the transcript starting at the given line offset.
132-func (c *ClaudeCodeAgent) CalculateTokenUsage(sessionRef string, fromOffset int) (*agent.TokenUsage, error) {
133-	// Subagent transcripts live in <transcriptDir>/<sessionID>/subagents/
134-	// but we don't have the sessionID here. The caller should pass the transcript path
135-	// which may contain the session ID in its directory structure.
136-	// For now, compute subagentsDir from the transcript path structure.
137-	return CalculateTotalTokenUsage(sessionRef, fromOffset, "")
138-}
139-
140-// --- Internal hook parsing functions ---
141-
142-func (c *ClaudeCodeAgent) parseSessionStart(stdin io.Reader) (*agent.Event, error) {
143-	raw, err := agent.ReadAndParseHookInput[sessionInfoRaw](stdin)
144-	if err != nil {
145-		return nil, err
146-	}
147-	return &agent.Event{
148-		Type:       agent.SessionStart,
149-		SessionID:  raw.SessionID,
150-		SessionRef: raw.TranscriptPath,
151-		Timestamp:  time.Now(),
152-	}, nil
153-}
154-
155-func (c *ClaudeCodeAgent) parseTurnStart(stdin io.Reader) (*agent.Event, error) {
156-	raw, err := agent.ReadAndParseHookInput[userPromptSubmitRaw](stdin)
```

> TOOL

tool_use Grep
id: toolu_0112uokr582h595NdtbNDnpS
```json
{
  "pattern": "func waitForTranscriptFlush",
  "path": "/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/agent/claudecode",
  "output_mode": "content",
  "-A": 30
}
```

> TOOL

tool_result
id: toolu_0112uokr582h595NdtbNDnpS
```
cmd/entire/cli/agent/claudecode/lifecycle.go:237:func waitForTranscriptFlush(transcriptPath string, hookStartTime time.Time) {
/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/agent/claudecode/lifecycle.go-238-	const (
/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/agent/claudecode/lifecycle.go-239-		maxWait      = 3 * time.Second
/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/agent/claudecode/lifecycle.go-240-		pollInterval = 50 * time.Millisecond
/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/agent/claudecode/lifecycle.go-241-		tailBytes    = 4096
/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/agent/claudecode/lifecycle.go-242-		maxSkew      = 2 * time.Second
/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/agent/claudecode/lifecycle.go-243-	)
/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/agent/claudecode/lifecycle.go-244-
cmd/entire/cli/agent/claudecode/lifecycle.go-245-	logCtx := logging.WithComponent(context.Background(), "agent.claudecode")
cmd/entire/cli/agent/claudecode/lifecycle.go-246-	deadline := time.Now().Add(maxWait)
/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/agent/claudecode/lifecycle.go-247-	for time.Now().Before(deadline) {
/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/agent/claudecode/lifecycle.go-248-		if checkStopSentinel(transcriptPath, tailBytes, hookStartTime, maxSkew) {
/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/agent/claudecode/lifecycle.go-249-			logging.Debug(logCtx, "transcript flush sentinel found",
/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/agent/claudecode/lifecycle.go-250-				slog.Duration("wait", time.Since(hookStartTime)),
/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/agent/claudecode/lifecycle.go-251-			)
/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/agent/claudecode/lifecycle.go-252-			return
/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/agent/claudecode/lifecycle.go-253-		}
/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/agent/claudecode/lifecycle.go-254-		time.Sleep(pollInterval)
/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/agent/claudecode/lifecycle.go-255-	}
/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/agent/claudecode/lifecycle.go-256-	logging.Warn(logCtx, "transcript flush sentinel not found within timeout, proceeding",
/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/agent/claudecode/lifecycle.go-257-		slog.Duration("timeout", maxWait),
/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/agent/claudecode/lifecycle.go-258-	)
/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/agent/claudecode/lifecycle.go-259-}
/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/agent/claudecode/lifecycle.go-260-
/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/agent/claudecode/lifecycle.go-261-// checkStopSentinel reads the tail of the transcript file and looks for the sentinel.
/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/agent/claudecode/lifecycle.go-262-func checkStopSentinel(path string, tailBytes int64, hookStartTime time.Time, maxSkew time.Duration) bool {
cmd/entire/cli/agent/claudecode/lifecycle.go-263-	f, err := os.Open(path) //nolint:gosec // path comes from agent hook input
/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/agent/claudecode/lifecycle.go-264-	if err != nil {
/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/agent/claudecode/lifecycle.go-265-		return false
/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/agent/claudecode/lifecycle.go-266-	}
/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/agent/claudecode/lifecycle.go-267-	defer f.Close()
```

> AGENT

Good, now I have a clear picture. The `waitForTranscriptFlush` has a 3s max timeout. The fix guards `PrepareTranscript` calls with `state.Phase.IsActive()` in both `extractNewModifiedFilesFromLiveTranscript` and `extractModifiedFilesFromLiveTranscript`. Let me now check the imports already used and write the test.

> TOOL

tool_use Grep
id: toolu_01XwoKgTujJndx5Awt8bpvpD
```json
{
  "pattern": "AgentType",
  "path": "/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/strategy/manual_commit_types.go",
  "output_mode": "content",
  "-C": 2
}
```

> TOOL

tool_result
id: toolu_01XwoKgTujJndx5Awt8bpvpD
```
39-	CheckpointsCount int             `json:"checkpoints_count"`
40-	FilesTouched     []string        `json:"files_touched"`
41:	Agent            agent.AgentType `json:"agent,omitempty"` // Human-readable agent name (e.g., "Claude Code")
42-	IsTask           bool            `json:"is_task,omitempty"`
43-	ToolUseID        string          `json:"tool_use_id,omitempty"`
```

> AGENT

Now let me check the `SessionState` struct for the relevant fields.

> TOOL

tool_use Grep
id: toolu_015MuvdC14Y5zcQeDErCfU88
```json
{
  "pattern": "AgentType.*agent\\.AgentType",
  "path": "/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/strategy/manual_commit_types.go",
  "output_mode": "content",
  "-C": 3
}
```

> TOOL

tool_result
id: toolu_015MuvdC14Y5zcQeDErCfU88
```
No matches found
```

> TOOL

tool_use Grep
id: toolu_01HEfnmusx4v9FUFiG12Hdim
```json
{
  "pattern": "AgentType",
  "path": "/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/strategy/manual_commit_session.go",
  "output_mode": "content",
  "-C": 2
}
```

> TOOL

tool_result
id: toolu_01HEfnmusx4v9FUFiG12Hdim
```
193-// transcriptPath is the path to the live transcript file (for mid-session commit detection).
194-// userPrompt is the user's prompt text (stored truncated as FirstPrompt for display).
195:func (s *ManualCommitStrategy) initializeSession(repo *git.Repository, sessionID string, agentType agent.AgentType, transcriptPath string, userPrompt string) (*SessionState, error) {
196-	head, err := repo.Head()
197-	if err != nil {
--
237-		StepCount:             0,
238-		UntrackedFilesAtStart: untrackedFiles,
239:		AgentType:             agentType,
240-		TranscriptPath:        transcriptPath,
241-		FirstPrompt:           truncatePromptForStorage(userPrompt),
```

> TOOL

tool_use Grep
id: toolu_013xtfTXU6aRoy19RGYMqGU7
```json
{
  "pattern": "type SessionState struct",
  "path": "/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/strategy",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result
id: toolu_013xtfTXU6aRoy19RGYMqGU7
```
No files found
```

> TOOL

tool_use Grep
id: toolu_0122W8f6NopP4idmHJ1zPzJq
```json
{
  "pattern": "SessionState",
  "path": "/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/strategy/manual_commit_types.go",
  "output_mode": "content",
  "-C": 1,
  "head_limit": 5
}
```

> TOOL

tool_result
id: toolu_0122W8f6NopP4idmHJ1zPzJq
```
25-
26:// SessionState is an alias for session.State.
27-// Previously this was a separate struct with manual conversion functions.
28:type SessionState = session.State
29-

[Showing results with pagination = limit: 5, offset: 0]
```

> TOOL

tool_use Grep
id: toolu_011HuPYZvG4BRhEunyPiDs4i
```json
{
  "pattern": "AgentType.*AgentType",
  "path": "/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/session/state.go",
  "output_mode": "content",
  "-C": 2
}
```

> TOOL

tool_result
id: toolu_011HuPYZvG4BRhEunyPiDs4i
```
115-
116-	// AgentType identifies the agent that created this session (e.g., "Claude Code", "Gemini CLI", "Cursor")
117:	AgentType agent.AgentType `json:"agent_type,omitempty"`
118-
119-	// Token usage tracking (accumulated across all checkpoints in this session)
```

> AGENT

Good. Now I have all the context I need. Let me write the test. The key points:

1. Set `state.TranscriptPath` to a real file path
2. Set `state.AgentType = agent.AgentTypeClaudeCode` (this triggers `PrepareTranscript` → `waitForTranscriptFlush` with 3s timeout)
3. Set phase to IDLE/ENDED
4. Time the `PostCommit()` call and assert < 2s

The guard is in `extractNewModifiedFilesFromLiveTranscript` (line 1151) and `extractModifiedFilesFromLiveTranscript` (line 1204) - both check `state.Phase.IsActive()` before calling `PrepareTranscript`.

> TOOL

tool_use Read
id: toolu_012e2sBW7NM87ncGhYWd9EV6
```json
{
  "file_path": "/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/strategy/phase_postcommit_test.go",
  "offset": 1,
  "limit": 25
}
```

> TOOL

tool_result
id: toolu_012e2sBW7NM87ncGhYWd9EV6
```
     1→package strategy
     2→
     3→import (
     4→	"context"
     5→	"os"
     6→	"path/filepath"
     7→	"testing"
     8→	"time"
     9→
    10→	"github.com/entireio/cli/cmd/entire/cli/checkpoint"
    11→	"github.com/entireio/cli/cmd/entire/cli/checkpoint/id"
    12→	"github.com/entireio/cli/cmd/entire/cli/paths"
    13→	"github.com/entireio/cli/cmd/entire/cli/session"
    14→	"github.com/entireio/cli/cmd/entire/cli/trailers"
    15→
    16→	"github.com/go-git/go-git/v5"
    17→	"github.com/go-git/go-git/v5/plumbing"
    18→	"github.com/go-git/go-git/v5/plumbing/object"
    19→	"github.com/stretchr/testify/assert"
    20→	"github.com/stretchr/testify/require"
    21→)
    22→
    23→const testNewActiveSessionID = "new-active-session"
    24→
    25→// TestPostCommit_ActiveSession_CondensesImmediately verifies that PostCommit on
```

> AGENT

Now I need to add the `agent` import and the two test functions. Let me add the import and the tests at the end of the file.

> TOOL

tool_use Edit
id: toolu_01R35yairSj5qET5HVPbiCvv
```json
{
  "replace_all": false,
  "file_path": "/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/strategy/phase_postcommit_test.go",
  "old_string": "\t\"github.com/entireio/cli/cmd/entire/cli/checkpoint\"\n\t\"github.com/entireio/cli/cmd/entire/cli/checkpoint/id\"\n\t\"github.com/entireio/cli/cmd/entire/cli/paths\"\n\t\"github.com/entireio/cli/cmd/entire/cli/session\"\n\t\"github.com/entireio/cli/cmd/entire/cli/trailers\"",
  "new_string": "\t\"github.com/entireio/cli/cmd/entire/cli/agent\"\n\t\"github.com/entireio/cli/cmd/entire/cli/checkpoint\"\n\t\"github.com/entireio/cli/cmd/entire/cli/checkpoint/id\"\n\t\"github.com/entireio/cli/cmd/entire/cli/paths\"\n\t\"github.com/entireio/cli/cmd/entire/cli/session\"\n\t\"github.com/entireio/cli/cmd/entire/cli/trailers\""
}
```

> TOOL

tool_result
id: toolu_01R35yairSj5qET5HVPbiCvv
```
The file /Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/strategy/phase_postcommit_test.go has been updated successfully.
```

> AGENT

Now add the two test functions at the end of the file.

> TOOL

tool_use Read
id: toolu_01SE2BWNuXiyx7PNorA2EPu7
```json
{
  "file_path": "/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/strategy/phase_postcommit_test.go",
  "offset": 1830
}
```

> TOOL

tool_result
id: toolu_01SE2BWNuXiyx7PNorA2EPu7
```
  1830→
  1831→	assert.Equal(t, idleOriginalStepCount, idleState.StepCount,
  1832→		"IDLE session with empty FilesTouched should NOT be condensed")
  1833→	assert.Equal(t, session.PhaseIdle, idleState.Phase,
  1834→		"IDLE session should remain IDLE")
  1835→	// BaseCommit is NOT updated for non-ACTIVE sessions (updateBaseCommitIfChanged skips them)
  1836→}
  1837→
```

> TOOL

tool_use Edit
id: toolu_0142ApDtNfCPNe8RrMgsNHU8
```json
{
  "replace_all": false,
  "file_path": "/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/strategy/phase_postcommit_test.go",
  "old_string": "\tassert.Equal(t, idleOriginalStepCount, idleState.StepCount,\n\t\t\"IDLE session with empty FilesTouched should NOT be condensed\")\n\tassert.Equal(t, session.PhaseIdle, idleState.Phase,\n\t\t\"IDLE session should remain IDLE\")\n\t// BaseCommit is NOT updated for non-ACTIVE sessions (updateBaseCommitIfChanged skips them)\n}",
  "new_string": "\tassert.Equal(t, idleOriginalStepCount, idleState.StepCount,\n\t\t\"IDLE session with empty FilesTouched should NOT be condensed\")\n\tassert.Equal(t, session.PhaseIdle, idleState.Phase,\n\t\t\"IDLE session should remain IDLE\")\n\t// BaseCommit is NOT updated for non-ACTIVE sessions (updateBaseCommitIfChanged skips them)\n}\n\n// TestPostCommit_IdleSession_SkipsSentinelWait is a regression test verifying that\n// PostCommit for an IDLE session with AgentType=ClaudeCode and a TranscriptPath\n// completes quickly without hitting the 3s sentinel timeout in PrepareTranscript.\n//\n// Before the fix, extractNewModifiedFilesFromLiveTranscript and\n// extractModifiedFilesFromLiveTranscript called PrepareTranscript unconditionally,\n// which triggered waitForTranscriptFlush (3s timeout) even for idle/ended sessions\n// where the transcript was already fully flushed.\n//\n// After the fix, PrepareTranscript is only called when state.Phase.IsActive().\nfunc TestPostCommit_IdleSession_SkipsSentinelWait(t *testing.T) {\n\tdir := setupGitRepo(t)\n\tt.Chdir(dir)\n\n\trepo, err := git.PlainOpen(dir)\n\trequire.NoError(t, err)\n\n\ts := &ManualCommitStrategy{}\n\tsessionID := \"test-idle-skip-sentinel\"\n\n\t// Initialize session and save a checkpoint\n\tsetupSessionWithCheckpoint(t, s, repo, dir, sessionID)\n\n\t// Set phase to IDLE, set AgentType to Claude Code, and set TranscriptPath\n\t// Without TranscriptPath, the PrepareTranscript code path is never reached.\n\t// Without AgentType=ClaudeCode, the sentinel wait is not triggered.\n\tstate, err := s.loadSessionState(sessionID)\n\trequire.NoError(t, err)\n\tstate.Phase = session.PhaseIdle\n\tstate.LastInteractionTime = nil\n\tstate.FilesTouched = []string{\"test.txt\"}\n\tstate.AgentType = agent.AgentTypeClaudeCode\n\n\t// Create a transcript file so PrepareTranscript would be triggered if not guarded\n\ttranscriptFile := filepath.Join(dir, \".entire\", \"transcript-\"+sessionID+\".jsonl\")\n\trequire.NoError(t, os.MkdirAll(filepath.Dir(transcriptFile), 0o755))\n\trequire.NoError(t, os.WriteFile(transcriptFile, []byte(`{\"type\":\"human\"}`+\"\\n\"), 0o644))\n\tstate.TranscriptPath = transcriptFile\n\n\trequire.NoError(t, s.saveSessionState(state))\n\n\t// Create a commit WITH the Entire-Checkpoint trailer\n\tcommitWithCheckpointTrailer(t, repo, dir, \"s1s2s3s4s5s6\")\n\n\t// Time PostCommit — before the fix this would take ~3s+ due to sentinel timeout\n\tstart := time.Now()\n\terr = s.PostCommit()\n\telapsed := time.Since(start)\n\trequire.NoError(t, err)\n\n\t// Assert it completes well under the 3s sentinel timeout.\n\t// Normal PostCommit for these tests runs in <500ms (git operations only).\n\tassert.Less(t, elapsed, 2*time.Second,\n\t\t\"IDLE session PostCommit should skip sentinel wait and complete in <2s, took %v\", elapsed)\n\n\t// Verify condensation still happened correctly\n\tsessionsRef, err := repo.Reference(plumbing.NewBranchReferenceName(paths.MetadataBranchName), true)\n\trequire.NoError(t, err, \"entire/checkpoints/v1 branch should exist after condensation\")\n\tassert.NotNil(t, sessionsRef)\n}\n\n// TestPostCommit_EndedSession_SkipsSentinelWait is the same regression test as\n// TestPostCommit_IdleSession_SkipsSentinelWait but for ENDED phase sessions.\n// Both IDLE and ENDED sessions should skip the sentinel wait since their\n// transcripts are already fully flushed.\nfunc TestPostCommit_EndedSession_SkipsSentinelWait(t *testing.T) {\n\tdir := setupGitRepo(t)\n\tt.Chdir(dir)\n\n\trepo, err := git.PlainOpen(dir)\n\trequire.NoError(t, err)\n\n\ts := &ManualCommitStrategy{}\n\tsessionID := \"test-ended-skip-sentinel\"\n\n\t// Initialize session and save a checkpoint\n\tsetupSessionWithCheckpoint(t, s, repo, dir, sessionID)\n\n\t// Set phase to ENDED, set AgentType to Claude Code, and set TranscriptPath\n\tstate, err := s.loadSessionState(sessionID)\n\trequire.NoError(t, err)\n\tnow := time.Now()\n\tstate.Phase = session.PhaseEnded\n\tstate.EndedAt = &now\n\tstate.FilesTouched = []string{\"test.txt\"}\n\tstate.AgentType = agent.AgentTypeClaudeCode\n\n\t// Create a transcript file so PrepareTranscript would be triggered if not guarded\n\ttranscriptFile := filepath.Join(dir, \".entire\", \"transcript-\"+sessionID+\".jsonl\")\n\trequire.NoError(t, os.MkdirAll(filepath.Dir(transcriptFile), 0o755))\n\trequire.NoError(t, os.WriteFile(transcriptFile, []byte(`{\"type\":\"human\"}`+\"\\n\"), 0o644))\n\tstate.TranscriptPath = transcriptFile\n\n\trequire.NoError(t, s.saveSessionState(state))\n\n\t// Create a commit WITH the Entire-Checkpoint trailer\n\tcommitWithCheckpointTrailer(t, repo, dir, \"e1e2e3e4e5e6\")\n\n\t// Time PostCommit — before the fix this would take ~3s+ due to sentinel timeout\n\tstart := time.Now()\n\terr = s.PostCommit()\n\telapsed := time.Since(start)\n\trequire.NoError(t, err)\n\n\t// Assert it completes well under the 3s sentinel timeout\n\tassert.Less(t, elapsed, 2*time.Second,\n\t\t\"ENDED session PostCommit should skip sentinel wait and complete in <2s, took %v\", elapsed)\n\n\t// Verify condensation still happened correctly\n\tsessionsRef, err := repo.Reference(plumbing.NewBranchReferenceName(paths.MetadataBranchName), true)\n\trequire.NoError(t, err, \"entire/checkpoints/v1 branch should exist after condensation\")\n\tassert.NotNil(t, sessionsRef)\n}"
}
```

> TOOL

tool_result
id: toolu_0142ApDtNfCPNe8RrMgsNHU8
```
The file /Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/strategy/phase_postcommit_test.go has been updated successfully.
```

> AGENT

Now let me run the tests to make sure they pass.

> TOOL

tool_use Bash
id: toolu_01PLPmsAGwwY7PBckkagY61r
```json
{
  "command": "go test -run \"TestPostCommit_(Idle|Ended)Session_SkipsSentinelWait\" ./cmd/entire/cli/strategy/ -v -timeout 30s 2>&1",
  "description": "Run the two new sentinel wait skip tests",
  "timeout": 60000
}
```

> TOOL

tool_result ERROR
id: toolu_01PLPmsAGwwY7PBckkagY61r
```
Exit code 1
=== RUN   TestPostCommit_IdleSession_SkipsSentinelWait
Created shadow branch 'entire/b2b3d54-e3b0c4' and committed changes
2026/02/24 14:21:51 INFO checkpoint saved component=checkpoint strategy=manual-commit checkpoint_type=session checkpoint_count=1 modified_files=1 new_files=0 deleted_files=0 shadow_branch=entire/b2b3d54-e3b0c4 branch_created=true
--- FAIL: TestPostCommit_IdleSession_SkipsSentinelWait (0.07s)
panic: invalid checkpoint ID "s1s2s3s4s5s6": must be 12 lowercase hex characters [recovered, repanicked]

goroutine 23 [running]:
testing.tRunner.func1.2({0x10315aba0, 0x140004582b0})
	/Users/soph/.local/share/mise/installs/go/1.25.6/src/testing/testing.go:1872 +0x190
testing.tRunner.func1()
	/Users/soph/.local/share/mise/installs/go/1.25.6/src/testing/testing.go:1875 +0x31c
panic({0x10315aba0?, 0x140004582b0?})
	/Users/soph/.local/share/mise/installs/go/1.25.6/src/runtime/panic.go:783 +0x120
github.com/entireio/cli/cmd/entire/cli/checkpoint/id.MustCheckpointID({0x102fc3f35, 0xc})
	/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/checkpoint/id/id.go:47 +0x64
github.com/entireio/cli/cmd/entire/cli/strategy.commitFilesWithTrailer(0x140001036c0, 0x140002fa7e0, {0x14000118850, 0x6a}, {0x102fc3f35, 0xc}, {0x140017c9df8, 0x1, 0x0?})
	/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/strategy/phase_postcommit_test.go:1322 +0x54
github.com/entireio/cli/cmd/entire/cli/strategy.commitWithCheckpointTrailer(0x140001036c0, 0x140002fa7e0, {0x14000118850, 0x6a}, {0x102fc3f35, 0xc})
	/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/strategy/phase_postcommit_test.go:1312 +0x70
github.com/entireio/cli/cmd/entire/cli/strategy.TestPostCommit_IdleSession_SkipsSentinelWait(0x140001036c0)
	/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/strategy/phase_postcommit_test.go:1880 +0x30c
testing.tRunner(0x140001036c0, 0x103221d60)
	/Users/soph/.local/share/mise/installs/go/1.25.6/src/testing/testing.go:1934 +0xc8
created by testing.(*T).Run in goroutine 1
	/Users/soph/.local/share/mise/installs/go/1.25.6/src/testing/testing.go:1997 +0x364
FAIL	github.com/entireio/cli/cmd/entire/cli/strategy	0.446s
FAIL

=== RUN   TestPostCommit_IdleSession_SkipsSentinelWait
Created shadow branch 'entire/b2b3d54-e3b0c4' and committed changes
2026/02/24 14:21:51 INFO checkpoint saved component=checkpoint strategy=manual-commit checkpoint_type=session checkpoint_count=1 modified_files=1 new_files=0 deleted_files=0 shadow_branch=entire/b2b3d54-e3b0c4 branch_created=true
--- FAIL: TestPostCommit_IdleSession_SkipsSentinelWait (0.07s)
panic: invalid checkpoint ID "s1s2s3s4s5s6": must be 12 lowercase hex characters [recovered, repanicked]

goroutine 23 [running]:
testing.tRunner.func1.2({0x10315aba0, 0x140004582b0})
	/Users/soph/.local/share/mise/installs/go/1.25.6/src/testing/testing.go:1872 +0x190
testing.tRunner.func1()
	/Users/soph/.local/share/mise/installs/go/1.25.6/src/testing/testing.go:1875 +0x31c
panic({0x10315aba0?, 0x140004582b0?})
	/Users/soph/.local/share/mise/installs/go/1.25.6/src/runtime/panic.go:783 +0x120
github.com/entireio/cli/cmd/entire/cli/checkpoint/id.MustCheckpointID({0x102fc3f35, 0xc})
	/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/checkpoint/id/id.go:47 +0x64
github.com/entireio/cli/cmd/entire/cli/strategy.commitFilesWithTrailer(0x140001036c0, 0x140002fa7e0, {0x14000118850, 0x6a}, {0x102fc3f35, 0xc}, {0x140017c9df8, 0x1, 0x0?})
	/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/strategy/phase_postcommit_test.go:1322 +0x54
github.com/entireio/cli/cmd/entire/cli/strategy.commitWithCheckpointTrailer(0x140001036c0, 0x140002fa7e0, {0x14000118850, 0x6a}, {0x102fc3f35, 0xc})
	/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/strategy/phase_postcommit_test.go:1312 +0x70
github.com/entireio/cli/cmd/entire/cli/strategy.TestPostCommit_IdleSession_SkipsSentinelWait(0x140001036c0)
	/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/strategy/phase_postcommit_test.go:1880 +0x30c
testing.tRunner(0x140001036c0, 0x103221d60)
	/Users/soph/.local/share/mise/installs/go/1.25.6/src/testing/testing.go:1934 +0xc8
created by testing.(*T).Run in goroutine 1
	/Users/soph/.local/share/mise/installs/go/1.25.6/src/testing/testing.go:1997 +0x364
FAIL	github.com/entireio/cli/cmd/entire/cli/strategy	0.446s
FAIL
```

> AGENT

The checkpoint IDs must be 12 lowercase hex characters. Let me fix them.

> TOOL

tool_use Edit
id: toolu_01KnhMQLiC6HEKkMg4zidXP3
```json
{
  "replace_all": false,
  "file_path": "/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/strategy/phase_postcommit_test.go",
  "old_string": "\tcommitWithCheckpointTrailer(t, repo, dir, \"s1s2s3s4s5s6\")",
  "new_string": "\tcommitWithCheckpointTrailer(t, repo, dir, \"a1a2a3a4a5a6\")"
}
```

> TOOL

tool_result
id: toolu_01KnhMQLiC6HEKkMg4zidXP3
```
The file /Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/strategy/phase_postcommit_test.go has been updated successfully.
```

> AGENT

Wait, "a1a2a3a4a5a6" is already used by another test. Let me use unique hex IDs.

> TOOL

tool_use Grep
id: toolu_01HvmwkSwQMw3kRHbTAK9PeE
```json
{
  "pattern": "commitWithCheckpointTrailer.*\"[a-f0-9]+\"",
  "path": "/Users/soph/Work/entire/devenv/cli_experiments/cmd/entire/cli/strategy/phase_postcommit_test.go",
  "output_mode": "content"
}
```

> TOOL

tool_result
id: toolu_01HvmwkSwQMw3kRHbTAK9PeE
```
49:	commitWithCheckpointTrailer(t, repo, dir, "a1b2c3d4e5f6")
99:	commitWithCheckpointTrailer(t, repo, dir, "b2c3d4e5f6a1")
149:	commitWithCheckpointTrailer(t, repo, dir, "c3d4e5f6a1b2")
231:	commitWithCheckpointTrailer(t, repo, dir, "d4e5f6a1b2c3")
295:	commitWithCheckpointTrailer(t, repo, dir, "e5f6a1b2c3d4")
352:	commitWithCheckpointTrailer(t, repo, dir, "f6a1b2c3d4e5")
408:	commitWithCheckpointTrailer(t, repo, dir, "a1b2c3d4e5f7")
471:	commitWithCheckpointTrailer(t, repo, dir, "b2c3d4e5f6a2")
531:	commitWithCheckpointTrailer(t, repo, dir, "c3d4e5f6a1b3")
592:	commitWithCheckpointTrailer(t, repo, dir, "e5f6a1b2c3d5")
1125:	commitWithCheckpointTrailer(t, repo, dir, "a1b2c3d4e5f6")
1158:	commitWithCheckpointTrailer(t, repo, dir, "c3d4e5f6a1b2")
1194:	commitWithCheckpointTrailer(t, repo, dir, "a1b2c3d4e5f6")
1400:	commitWithCheckpointTrailer(t, repo, dir, "a1b2c3d4e5f6")
1483:	commitWithCheckpointTrailer(t, repo, dir, "b1c2d3e4f5a6")
1880:	commitWithCheckpointTrailer(t, repo, dir, "a1a2a3a4a5a6")
1934:	commitWithCheckpointTrailer(t, repo, dir, "e1e2e3e4e5e6")
```

> AGENT

The IDs don't need to be globally unique across tests since each test has its own isolated repo. But `a1a2a3a4a5a6` is already valid hex. Let me also fix the ENDED test ID - `e1e2e3e4e5e6` is valid hex too. Let me just run the tests now.

> TOOL

tool_use Bash
id: toolu_01KcRo7rBwKLQJ8KAc3W4SHs
```json
{
  "command": "go test -run \"TestPostCommit_(Idle|Ended)Session_SkipsSentinelWait\" ./cmd/entire/cli/strategy/ -v -timeout 30s 2>&1",
  "description": "Run the sentinel wait skip tests",
  "timeout": 60000
}
```

> TOOL

tool_result
id: toolu_01KcRo7rBwKLQJ8KAc3W4SHs
```
=== RUN   TestPostCommit_IdleSession_SkipsSentinelWait
Created shadow branch 'entire/12d9137-e3b0c4' and committed changes
2026/02/24 14:22:07 INFO checkpoint saved component=checkpoint strategy=manual-commit checkpoint_type=session checkpoint_count=1 modified_files=1 new_files=0 deleted_files=0 shadow_branch=entire/12d9137-e3b0c4 branch_created=true
2026/02/24 14:22:07 INFO attribution calculated component=attribution agent_lines=1 human_added=0 human_modified=0 human_removed=0 total_committed=1 agent_percentage=100 accumulated_user_added=0 accumulated_user_removed=0 files_touched=1
[entire] Condensed session test-idl: a1a2a3a4a5a6 (1 checkpoints)
2026/02/24 14:22:07 INFO session condensed component=checkpoint strategy=manual-commit checkpoint_id=a1a2a3a4a5a6 checkpoints_condensed=1 transcript_lines=1
[entire] Cleaned up shadow branch: entire/12d9137-e3b0c4
2026/02/24 14:22:07 INFO shadow branch deleted component=checkpoint strategy=manual-commit shadow_branch=entire/12d9137-e3b0c4
--- PASS: TestPostCommit_IdleSession_SkipsSentinelWait (0.09s)
=== RUN   TestPostCommit_EndedSession_SkipsSentinelWait
Created shadow branch 'entire/72c51bd-e3b0c4' and committed changes
2026/02/24 14:22:07 INFO checkpoint saved component=checkpoint strategy=manual-commit checkpoint_type=session checkpoint_count=1 modified_files=1 new_files=0 deleted_files=0 shadow_branch=entire/72c51bd-e3b0c4 branch_created=true
2026/02/24 14:22:07 INFO attribution calculated component=attribution agent_lines=1 human_added=0 human_modified=0 human_removed=0 total_committed=1 agent_percentage=100 accumulated_user_added=0 accumulated_user_removed=0 files_touched=1
[entire] Condensed session test-end: e1e2e3e4e5e6 (1 checkpoints)
2026/02/24 14:22:07 INFO session condensed component=checkpoint strategy=manual-commit checkpoint_id=e1e2e3e4e5e6 checkpoints_condensed=1 transcript_lines=1
[entire] Cleaned up shadow branch: entire/72c51bd-e3b0c4
2026/02/24 14:22:07 INFO shadow branch deleted component=checkpoint strategy=manual-commit shadow_branch=entire/72c51bd-e3b0c4
--- PASS: TestPostCommit_EndedSession_SkipsSentinelWait (0.05s)
PASS
ok  	github.com/entireio/cli/cmd/entire/cli/strategy	0.483s
```

> AGENT

Both tests pass and complete in ~50-90ms, well under the 2s threshold. Now let me run the full test suite and lint to make sure nothing is broken.

> TOOL

tool_use Bash
id: toolu_01T4jTQaueue7SyZt3qHUCNk
```json
{
  "command": "mise run fmt 2>&1",
  "description": "Format code",
  "timeout": 30000
}
```

> TOOL

tool_result
id: toolu_01T4jTQaueue7SyZt3qHUCNk
```
[fmt] $ gofmt -s -w .
```

> TOOL

tool_use Bash
id: toolu_01XJRCRbTZVGhrcEA36q5AXD
```json
{
  "command": "mise run lint 2>&1",
  "description": "Lint check",
  "timeout": 120000
}
```

> TOOL

tool_result
id: toolu_01XJRCRbTZVGhrcEA36q5AXD
```
[lint:gofmt] $ ~/Work/entire/devenv/cli_experiments/mise-tasks/lint/gofmt
[lint:go] $ ~/Work/entire/devenv/cli_experiments/mise-tasks/lint/go
[lint:gomod] $ ~/Work/entire/devenv/cli_experiments/mise-tasks/lint/gomod
[lint:shellcheck] $ ~/Work/entire/devenv/cli_experiments/mise-tasks/lint/shellc…
[lint:gofmt] Finished in 56.4ms
[lint:gomod] Finished in 81.2ms
[lint:shellcheck] Finished in 173.0ms
[lint:go] 0 issues.
[lint:go] Finished in 2.35s
[lint] $ ~/Work/entire/devenv/cli_experiments/mise-tasks/lint/_default
[lint] Finished in 3.1ms
Finished in 2.35s
```

> TOOL

tool_use Bash
id: toolu_01LW7astZNeeFNdC3uwXWtWP
```json
{
  "command": "mise run test:ci 2>&1",
  "description": "Run all tests (unit + integration)",
  "timeout": 300000
}
```

> TOOL

tool_result
id: toolu_01LW7astZNeeFNdC3uwXWtWP
```
[test:ci] $ go test -tags=integration -race ./...
?   	github.com/entireio/cli/cmd/entire	[no test files]
ok  	github.com/entireio/cli/cmd/entire/cli	4.635s
ok  	github.com/entireio/cli/cmd/entire/cli/agent	1.486s
ok  	github.com/entireio/cli/cmd/entire/cli/agent/claudecode	3.053s
ok  	github.com/entireio/cli/cmd/entire/cli/agent/geminicli	2.588s
ok  	github.com/entireio/cli/cmd/entire/cli/agent/opencode	5.476s
?   	github.com/entireio/cli/cmd/entire/cli/agent/testutil	[no test files]
ok  	github.com/entireio/cli/cmd/entire/cli/benchutil	2.197s [no tests to run]
?   	github.com/entireio/cli/cmd/entire/cli/buildinfo	[no test files]
ok  	github.com/entireio/cli/cmd/entire/cli/checkpoint	2.976s
ok  	github.com/entireio/cli/cmd/entire/cli/checkpoint/id	(cached)
ok  	github.com/entireio/cli/cmd/entire/cli/integration_test	57.278s
?   	github.com/entireio/cli/cmd/entire/cli/jsonutil	[no test files]
ok  	github.com/entireio/cli/cmd/entire/cli/logging	(cached)
ok  	github.com/entireio/cli/cmd/entire/cli/paths	(cached)
ok  	github.com/entireio/cli/cmd/entire/cli/session	3.490s
ok  	github.com/entireio/cli/cmd/entire/cli/settings	3.697s
ok  	github.com/entireio/cli/cmd/entire/cli/strategy	25.352s
ok  	github.com/entireio/cli/cmd/entire/cli/stringutil	2.748s
ok  	github.com/entireio/cli/cmd/entire/cli/summarize	3.389s
ok  	github.com/entireio/cli/cmd/entire/cli/telemetry	(cached)
?   	github.com/entireio/cli/cmd/entire/cli/testutil	[no test files]
ok  	github.com/entireio/cli/cmd/entire/cli/textutil	(cached)
ok  	github.com/entireio/cli/cmd/entire/cli/trailers	(cached)
ok  	github.com/entireio/cli/cmd/entire/cli/transcript	(cached)
ok  	github.com/entireio/cli/cmd/entire/cli/validation	(cached)
ok  	github.com/entireio/cli/cmd/entire/cli/versioncheck	(cached)
ok  	github.com/entireio/cli/redact	3.393s
```

> AGENT

All tests pass, including integration tests. Formatting and linting are clean.

The two new tests verify the fix:

- **`TestPostCommit_IdleSession_SkipsSentinelWait`** — Sets up an IDLE session with `AgentType=ClaudeCode` and a real `TranscriptPath`, runs `PostCommit()`, and asserts it completes in under 2 seconds (actual: ~90ms). Before the fix, this would take 3s+ due to the sentinel timeout.

- **`TestPostCommit_EndedSession_SkipsSentinelWait`** — Same pattern but for ENDED phase. Both non-active phases should skip the `PrepareTranscript` call since their transcripts are already fully flushed.
