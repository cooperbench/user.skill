#!/usr/bin/env python3
"""Render the self-contained Cursor canvas for the cohort QC report."""
import json
from pathlib import Path

REPORT = Path("/data/swesimbench-v2-harbor/cohort_qc_report.json")
OUT = Path("/home/ubuntu/.cursor/projects/data/canvases/swesimbench-v2-cohort-qc.canvas.tsx")

report = json.loads(REPORT.read_text())
samples = {item["developer"]: item["messages"] for item in report["samples"]}
developers = []
for audit in report["developers"]:
    developers.append(
        {
            "developer": audit["developer"],
            "status": audit["status"],
            "flags": audit["flags"],
            "decisionNotes": audit["decision_notes"],
            "sources": audit["sources"],
            "trainTurns": audit["train_turns_manifest"],
            "heldTurns": audit["held_turns_manifest"],
            "trainSessions": audit["train_sessions"],
            "heldSessions": audit["held_sessions"],
            "heldSessionsFound": audit["held_sessions_found"],
            "manifestSessions": audit["manifest_sessions"],
            "indexedManifestSessions": audit["indexed_manifest_sessions"],
            "aliasDuplicates": audit["session_id_alias_duplicate_count"],
            "meanTurnsPerSession": audit["mean_manifest_turns_per_session"],
            "eligible": audit["eligible_held_messages"],
            "unique": audit["unique_eligible_messages"],
            "duplicateRate": audit["exact_duplicate_rate"],
            "noise": audit["noise_user_turns"],
            "compactions": audit["compaction_user_turns"],
            "secrets": audit["secret_like_user_turns"],
            "trainHeldOverlap": audit["repeated_substantial_messages_across_splits"],
            "topMessage": audit["top_repeated_message"],
            "topCount": audit["top_repeated_message_count"],
            "missingSessions": audit["missing_all_session_ids"],
            "messages": samples[audit["developer"]],
        }
    )

summary = report["summary"]
canvas_data = {
    "summary": summary,
    "developers": developers,
    "flagged": [dev for dev in developers if dev["status"] != "pass"],
    "secretMessageCount": sum(dev["secrets"] for dev in developers),
    "secretDeveloperCount": sum(dev["secrets"] > 0 for dev in developers),
    "missingSessionCount": sum(len(dev["missingSessions"]) for dev in developers),
}
data_json = json.dumps(canvas_data, ensure_ascii=False, separators=(",", ":"))

template = r'''import {
  Callout,
  Card,
  CardBody,
  CardHeader,
  Code,
  Divider,
  Grid,
  H1,
  H2,
  H3,
  Pill,
  Row,
  Select,
  Stack,
  Stat,
  Table,
  Text,
  useCanvasState,
  useHostTheme,
} from "cursor/canvas";

const data = __DATA__;

function FlagList({ flags }: { flags: string[] }) {
  if (!flags.length) return <Text size="small" tone="tertiary">No automated flags</Text>;
  return (
    <Row gap={6} wrap>
      {flags.map((flag) => <Pill size="sm">{flag.replaceAll("_", " ")}</Pill>)}
    </Row>
  );
}

function MessageRow({ message, index }: { message: (typeof data.developers)[number]["messages"][number]; index: number }) {
  const theme = useHostTheme();
  return (
    <div style={{ display: "grid", gridTemplateColumns: "32px minmax(0, 1fr)", gap: 12, padding: "12px 0" }}>
      <div
        style={{
          width: 26,
          height: 26,
          borderRadius: 999,
          display: "grid",
          placeItems: "center",
          background: theme.fill.tertiary,
          color: theme.text.tertiary,
          fontSize: 11,
          fontWeight: 700,
        }}
      >
        {index + 1}
      </div>
      <Stack gap={5}>
        <Text style={{ margin: 0 }}>{message.text}</Text>
        <Text size="small" tone="quaternary" style={{ margin: 0 }}>
          {message.source} · {message.words} words · turn {message.turn_index} · <Code>{message.sid}</Code>
        </Text>
      </Stack>
    </div>
  );
}

function DeveloperExplorer() {
  const options = data.developers.map((dev) => ({
    value: dev.developer,
    label: `${dev.developer} · ${dev.status}`,
  }));
  const [developer, setDeveloper] = useCanvasState<string>("qc-selected-developer", options[0].value);
  const selected = data.developers.find((dev) => dev.developer === developer) || data.developers[0];

  return (
    <section>
      <Row justify="space-between" align="end" gap={16} wrap>
        <Stack gap={4}>
          <H2 style={{ margin: 0 }}>Developer message explorer</H2>
          <Text size="small" tone="tertiary" style={{ margin: 0 }}>
            Up to ten deterministic-random eligible held-out messages per developer; secret-like values are redacted.
          </Text>
        </Stack>
        <Select value={selected.developer} onChange={setDeveloper} options={options} style={{ minWidth: 280 }} />
      </Row>

      <Card size="lg" style={{ marginTop: 14 }}>
        <CardHeader trailing={<Pill active={selected.status === "pass"}>{selected.status}</Pill>}>
          {selected.developer}
        </CardHeader>
        <CardBody>
          <Grid columns={4} gap={12}>
            <Stat value={selected.eligible} label="eligible held-out messages" />
            <Stat value={selected.indexedManifestSessions + " / " + selected.manifestSessions} label="all sessions indexed" />
            <Stat value={`${Math.round(selected.duplicateRate * 100)}%`} label="exact duplicate rate" />
            <Stat value={selected.noise} label="metadata/noise turns" />
          </Grid>
          <div style={{ margin: "14px 0" }}><FlagList flags={selected.flags} /></div>
          {selected.decisionNotes.length > 0 && (
            <Text size="small" tone="secondary" style={{ margin: "0 0 14px" }}>
              QC decision: {selected.decisionNotes.join(" · ")}
            </Text>
          )}
          <Divider />
          <Stack gap={0}>
            {selected.messages.map((message, index) => <MessageRow message={message} index={index} />)}
          </Stack>
        </CardBody>
      </Card>
    </section>
  );
}

export default function CohortQcCanvas() {
  const theme = useHostTheme();
  const s = data.summary;
  const reviewRows = data.flagged.map((dev) => [
    dev.developer,
    dev.flags.join(", ").replaceAll("_", " "),
    String(dev.eligible),
    `${Math.round(dev.duplicateRate * 100)}%`,
    String(dev.aliasDuplicates),
    String(dev.noise),
    String(dev.secrets),
  ]);

  return (
    <div style={{ minHeight: "100%", background: theme.bg.editor, color: theme.text.primary, padding: "28px 30px" }}>
      <Stack gap={26}>
        <Stack gap={8}>
          <Row gap={9} align="center" wrap>
            <Pill active>SWESimBench v2</Pill>
            <Text size="small" tone="tertiary">Canonical cohort quality control · fingerprinted reconstruction audit</Text>
          </Row>
          <H1 style={{ margin: 0 }}>{s.audited_users} developers retained after canonical cohort QC</H1>
          <Text tone="secondary" style={{ maxWidth: 850, margin: 0 }}>
            This audit checks session availability, chronological separation, placeholder/fake content, metadata noise,
            exact duplication, cross-split overlap, secret-like text, and eligible held-out volume.
          </Text>
        </Stack>

        <Grid columns={5} gap={12}>
          <Stat value={s.audited_users} label="developers audited" />
          <Stat value={s.status_counts.pass} label="automated pass" tone="success" />
          <Stat value={s.status_counts.pass_with_notes} label="retained with notes" tone="warning" />
          <Stat value={s.indexed_manifest_sessions + " / " + s.manifest_sessions} label="all sessions indexed" />
          <Stat value={s.sampled_messages} label="messages sampled" tone="info" />
        </Grid>

        <Callout tone="success" title="Synthetic placeholder screen">
          <Code>gh:mhaitana</Code> is excluded in the census and both eval builders. No other developer has fake session IDs or placeholder-pattern messages under the automated checks.
        </Callout>

        <Grid columns="minmax(0, 1fr) minmax(0, 1fr)" gap={20} align="start">
          <section>
            <H2 style={{ marginTop: 0 }}>High-priority findings</H2>
            <Stack gap={12}>
              <div style={{ borderLeft: `2px solid ${theme.stroke.secondary}`, paddingLeft: 14 }}>
                <H3 style={{ margin: 0 }}>Secret-like content</H3>
                <Text tone="secondary" style={{ margin: "4px 0 0" }}>
                  {data.secretMessageCount} held-out messages across {data.secretDeveloperCount} developers triggered the conservative scanner. All clean traces, profiles, contexts, targets, and canvas samples are scrubbed before use.
                </Text>
              </div>
              <div style={{ borderLeft: `2px solid ${theme.stroke.secondary}`, paddingLeft: 14 }}>
                <H3 style={{ margin: 0 }}>Metadata contamination</H3>
                <Text tone="secondary" style={{ margin: "4px 0 0" }}>
                  Injected wrappers are retained as <Code>SYSTEM</Code>, <Code>TOOL</Code>, or <Code>METADATA</Code> context and can no longer become developer targets. No clean user-role turn matched the metadata screen.
                </Text>
              </div>
              <div style={{ borderLeft: `2px solid ${theme.stroke.secondary}`, paddingLeft: 14 }}>
                <H3 style={{ margin: 0 }}>Missing indexed sessions</H3>
                <Text tone="secondary" style={{ margin: "4px 0 0" }}>
                  {data.missingSessionCount} of {s.manifest_sessions} canonical train/held sessions are missing. SWE-chat is now indexed by the same coverage-complete builder as Entire, Crawl, and DataClaw.
                </Text>
              </div>
              <div style={{ borderLeft: `2px solid ${theme.stroke.secondary}`, paddingLeft: 14 }}>
                <H3 style={{ margin: 0 }}>Resolved duplication</H3>
                <Text tone="secondary" style={{ margin: "4px 0 0" }}>
                  {s.dedup_rule_counts.exact_transcript || 0} exact transcript groups and {s.reconstructed_session_events} reconstructed-session groups were collapsed. {s.cross_split_dedup_events} dedup decisions crossed the original train/held boundary and were conservatively assigned to training.
                </Text>
              </div>
            </Stack>
          </section>

          <Card>
            <CardHeader trailing={<Pill>{s.eligible_held_messages} eligible</Pill>}>Integrity checks that passed globally</CardHeader>
            <CardBody>
              <Stack gap={10}>
                <Text><Text as="span" weight="semibold">0</Text> shared session IDs across developers</Text>
                <Text><Text as="span" weight="semibold">0</Text> train/held session overlaps</Text>
                <Text><Text as="span" weight="semibold">0</Text> train/held overlaps after embedded-UUID normalization</Text>
                <Text><Text as="span" weight="semibold">0</Text> invalid chronological splits</Text>
                <Text><Text as="span" weight="semibold">0</Text> remaining fake session IDs</Text>
                <Text><Text as="span" weight="semibold">0</Text> remaining placeholder-pattern users</Text>
                <Text><Text as="span" weight="semibold">{s.shared_substantial_messages_across_developers}</Text> substantial message shared across developers</Text>
              </Stack>
            </CardBody>
          </Card>
        </Grid>

        <DeveloperExplorer />

        <section>
          <H2>Retained developers with QC notes</H2>
          <Table
            headers={["Developer", "Automated flags", "Eligible", "Dup.", "Aliases", "Noise", "Secrets"]}
            rows={reviewRows}
            columnAlign={["left", "left", "right", "right", "right", "right", "right"]}
            striped
          />
        </section>

        <Callout tone="info" title="QC decisions">
          Repeated messages across genuinely separate sessions remain eligible behavior. Only sessions with strong ordered-context evidence—matching timestamps or a near-complete shared developer-turn sequence—are merged; low-point developers remain visible as lower-power per-developer estimates.
        </Callout>

        <Text size="small" tone="quaternary" style={{ margin: 0 }}>
          Source: canonical clean manifest plus Entire, Claude Crawl, DataClaw, and SWE-chat full traces · up to 10 samples/developer selected with SHA-256-seeded randomness · audit generated July 13, 2026
        </Text>
      </Stack>
    </div>
  );
}
'''

OUT.write_text(template.replace("__DATA__", data_json))
print(f"wrote {OUT} ({OUT.stat().st_size:,} bytes)")
