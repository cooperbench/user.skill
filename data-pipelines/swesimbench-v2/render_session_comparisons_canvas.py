#!/usr/bin/env python3
"""Render the deterministic train/held session comparison sample."""
import json
from pathlib import Path

ROOT = Path("/data/swesimbench-v2-harbor")
DATA = ROOT / "session_comparison_sample.json"
OUT = Path(
    "/home/ubuntu/.cursor/projects/data/canvases/"
    "train-held-session-comparisons.canvas.tsx"
)

payload = json.loads(DATA.read_text())
data_json = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))

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
  Text,
  useCanvasState,
  useHostTheme,
} from "cursor/canvas";

const data = __DATA__;

type Comparison = (typeof data.comparisons)[number];
type Session = Comparison["train"];
type Turn = Session["excerpt"][number];

function TurnRow({ turn }: { turn: Turn }) {
  const theme = useHostTheme();
  const role = turn.role === "user" ? "DEVELOPER" : turn.role.toUpperCase();
  return (
    <div
      style={{
        padding: "10px 12px",
        borderLeft: `3px solid ${turn.matched ? theme.accent.primary : theme.stroke.secondary}`,
        background: turn.matched ? theme.fill.tertiary : "transparent",
      }}
    >
      <Row gap={8} align="center" wrap>
        <Code>turn {turn.index}</Code>
        <Pill size="sm" active={turn.matched}>{role}</Pill>
        {turn.matched && <Text size="small" weight="semibold">shared message</Text>}
      </Row>
      <Text style={{ margin: "7px 0 0", whiteSpace: "pre-wrap" }}>{turn.text}</Text>
    </div>
  );
}

function SessionPanel({ title, session }: { title: string; session: Session }) {
  return (
    <Card>
      <CardHeader trailing={<Pill active={title === "Held-out"}>{title}</Pill>}>
        {session.repo}
      </CardHeader>
      <CardBody>
        <Stack gap={12}>
          <Stack gap={4}>
            <Text size="small" tone="tertiary"><Code>{session.sid}</Code></Text>
            <Text size="small" tone="quaternary">
              {session.start_time} · {session.source} · {session.turns} total turns
            </Text>
          </Stack>
          <Divider />
          <Stack gap={4}>
            {session.excerpt.map((turn) => <TurnRow turn={turn} />)}
          </Stack>
        </Stack>
      </CardBody>
    </Card>
  );
}

function SharedMessages({ comparison }: { comparison: Comparison }) {
  return (
    <section>
      <H3 style={{ margin: 0 }}>Exact normalized messages shared by this pair</H3>
      <Stack gap={10} style={{ marginTop: 10 }}>
        {comparison.matches.map((match, index) => (
          <div style={{ padding: "10px 0" }}>
            <Row gap={8} align="center" wrap>
              <Pill size="sm">{index + 1}</Pill>
              <Text size="small" tone="tertiary">
                train turn {match.train_turn} · held turn {match.held_turn}
              </Text>
            </Row>
            <Text style={{ margin: "6px 0 0" }}>“{match.text}”</Text>
            {(match.train_timestamp || match.held_timestamp) && (
              <Text size="small" tone="quaternary" style={{ margin: "4px 0 0" }}>
                timestamps: {match.train_timestamp || "missing"} / {match.held_timestamp || "missing"}
              </Text>
            )}
          </div>
        ))}
      </Stack>
    </section>
  );
}

export default function SessionComparisonCanvas() {
  const theme = useHostTheme();
  const options = data.comparisons.map((comparison) => ({
    value: comparison.developer,
    label: `${comparison.developer} · ${comparison.pair_overlap_messages} shared`,
  }));
  const [developer, setDeveloper] = useCanvasState<string>(
    "train-held-comparison-developer",
    options[0].value,
  );
  const comparison =
    data.comparisons.find((item) => item.developer === developer) || data.comparisons[0];

  return (
    <div style={{ minHeight: "100%", background: theme.bg.editor, color: theme.text.primary, padding: "28px 30px" }}>
      <Stack gap={24}>
        <Stack gap={8}>
          <Row gap={8} align="center" wrap>
            <Pill active>SWESimBench v2 QC</Pill>
            <Text size="small" tone="tertiary">10 overlap-prioritized developers · deterministic session sample</Text>
          </Row>
          <H1 style={{ margin: 0 }}>Train versus held-out session comparisons</H1>
          <Text tone="secondary" style={{ maxWidth: 930, margin: 0 }}>
            Developers are prioritized by exact substantial user-message overlap. For each developer,
            one overlap-bearing held-out session is selected with a fingerprint-seeded random draw,
            then paired with the train session sharing the most messages.
          </Text>
        </Stack>

        <Row justify="space-between" align="end" gap={18} wrap>
          <Stack gap={4}>
            <H2 style={{ margin: 0 }}>{comparison.developer}</H2>
            <Text size="small" tone="tertiary" style={{ margin: 0 }}>
              Selection seed <Code>{comparison.selection_seed}</Code>
            </Text>
          </Stack>
          <Select value={comparison.developer} onChange={setDeveloper} options={options} style={{ minWidth: 310 }} />
        </Row>

        <Grid columns={3} gap={12}>
          <Stat value={comparison.developer_overlap_messages} label="shared messages across all splits" />
          <Stat value={comparison.pair_overlap_messages} label="shared messages in selected pair" />
          <Stat value={comparison.reconstruction_match ? "Yes" : "No"} label="reconstruction matcher fired" tone={comparison.reconstruction_match ? "warning" : "success"} />
        </Grid>

        <Callout
          tone={comparison.reconstruction_match ? "warning" : "success"}
          title={comparison.reconstruction_match ? "Potential duplicate session" : "Separate sessions under the reconstruction policy"}
        >
          Message repetition alone is retained as developer behavior. A pair is merged only when timestamps
          or a strongly ordered conversational spine indicate that two records reconstruct one source session.
        </Callout>

        <SharedMessages comparison={comparison} />

        <Grid columns="minmax(0, 1fr) minmax(0, 1fr)" gap={18} align="start">
          <SessionPanel title="Train" session={comparison.train} />
          <SessionPanel title="Held-out" session={comparison.held} />
        </Grid>

        <Text size="small" tone="quaternary" style={{ margin: 0 }}>
          Policy <Code>{data.policy_version}</Code> · excerpts show ±2 turns around up to three longest shared messages · all text comes from scrubbed canonical traces
        </Text>
      </Stack>
    </div>
  );
}
'''

OUT.write_text(template.replace("__DATA__", data_json))
print(f"wrote {OUT} ({OUT.stat().st_size:,} bytes)")
