> DEVELOPER

https://github.com/tokoroten/prompt-review/blob/main/.claude/skills/prompt-reviewのinputを追加して

> AGENT

まず、指定されたGitHubリポジトリのスキルファイルの内容を取得します。

> AGENT

ディレクトリのようなので、中身を確認します。

> AGENT

スキルの全ファイルを取得します。

> AGENT

flake inputの構造を確認します。

> AGENT

構造が把握できました。`flake.nix` に input を追加し、`agent-skills.nix` に source と skill を追加します。

> AGENT

次に、`skills.explicit` にスキルを追加します。

> AGENT

変更内容を確認します。

> AGENT

CLAUDE.mdのAgent Skillsセクションも更新します。

> AGENT

完了しました。以下の変更を行いました： 1. **`flake.nix`** — `prompt-review-skill` を flake input に追加（`github:tokoroten/prompt-review`, `flake = false`） 2. **`nix/modules/home/agent-skills.nix`** — source に `prompt-review` を追加（subdir: `.claude/skills`）、`skills.explicit` にスキルエントリを追加 3. **`CLAUDE.md`** — Agent Skillsセクションに `prompt-review` の説明を追加 `nix run .#switch` で適用すると、`~/.config/claude/skills/` と `~/.agents/skills/` に `prompt-review` スキルがデプロイされます。