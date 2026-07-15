> DEVELOPER

是的，**Claude Skills 社区里已经有不少“视频生成/视频制作”相关 Skills**。不过要分清两类：

1. **真正调用视频模型生成视频**：比如 Runway、Veo、P-Video、WAN、Seedance、fal.ai 等。
2. **用代码/工具合成视频**：比如 Remotion、FFmpeg、MoviePy、UGC 工作流、产品宣传视频等。

你上传的笔记里也提到，Claude 侧视频生产主要依赖 **Claude Code + Skills + 外部工具链**，例如 Remotion、video-toolkit、Runway、MoviePy、FFmpeg、TTS 等 。

## 我建议重点研究这些 Claude 社区视频 Skills

### 1. `digitalsamba/claude-code-video-toolkit`

这是目前我看到最完整的 Claude Code 视频制作工作台。它不是单一视频模型 Skill，而是一整套视频生产 workspace：包含 skills、commands、templates 和 tools，可以从 concept 到 final render 做完整视频。README 里写明它给 Claude Code 提供创建专业视频所需的构件，并支持 `/setup` 和 `/video` 工作流。([GitHub][1])

下载研究：

```bash
git clone https://github.com/digitalsamba/claude-code-video-toolkit.git
cd claude-code-video-toolkit
find . -name "SKILL.md" -o -name "*.md" -o -name "*.py"
```

适合研究：完整视频流水线、Remotion、配音、音乐、素材生成、FFmpeg、MoviePy。

---

### 2. `runwayml/skills`

这是 Runway 官方的 coding agent skills，支持 Claude Code、Cursor、Codex 等 agent。仓库说明里明确写了可以通过 Runway API 批量生成视频、图片和音频，支持产品视频、多镜头故事、创意迭代等；agent 会负责 API 调用、轮询任务完成、下载结果。([GitHub][2])

安装：

```bash
npx skills add runwayml/skills
```

下载研究：

```bash
git clone https://github.com/runwayml/skills.git
cd skills
find . -name "SKILL.md" -o -name "*.md" -o -name "*.ts" -o -name "*.js"
```

适合研究：真正的视频模型 API 编排、批量生成、Runway Gen 系列、Seedance、Veo 等模型路由。

---

### 3. `kdowswell/veo-tools`

这个是专门面向 **Google Veo 3.1 + Claude Code** 的视频生成 skills。仓库说明写的是通过 Vertex AI 生成 cinematic video content，适合网站 hero background、营销素材和 seamless loops。它支持 Claude Code plugin 安装，也支持手动复制 skills 到 `~/.claude/skills/`。([GitHub][3])

下载研究：

```bash
git clone https://github.com/kdowswell/veo-tools.git
cd veo-tools
find . -name "SKILL.md" -o -name "*.md" -o -name "*.sh" -o -name "*.py"
```

手动安装方式：

```bash
cp -r veo-tools/skills/* ~/.claude/skills/
```

注意：这个仓库目前星标很少，适合研究结构，不建议一上来就放生产 API key。

---

### 4. `inferen-sh/skills` 里的 `p-video`

Claude Code Marketplaces 上的 `P Video` skill 描述说，它通过 `inference.sh` CLI 调用 Pruna 优化模型，包装了 P-Video、WAN-T2V、WAN-I2V 三类模型，用于 text/image-to-video，输出 720p 或 1080p，适合原型视频、社交媒体短片、产品 mockup 动画。([claudemarketplaces.com][4])

安装：

```bash
npx skills add https://github.com/inferen-sh/skills --skill p-video
```

下载研究：

```bash
git clone https://github.com/inferen-sh/skills.git inferen-sh-skills
cd inferen-sh-skills
find . -name "SKILL.md" -o -name "*.md" -o -name "*.sh"
```

---

### 5. `inferen-sh/skills` 里的 `image-to-video`

同一个社区源里还有 `image-to-video` skill。Marketplace 描述说它把静态图片转成动画视频，背后使用 Wan 2.5 i2v、Seedance、Fabric 等模型，并强调更适合轻微运动、产品 demo、cinemagraph、社交媒体内容和概念图动效。([claudemarketplaces.com][5])

安装大致类似：

```bash
npx skills add https://github.com/inferen-sh/skills --skill image-to-video
```

---

### 6. `fal-ai-community/skills` 里的 `fal-video-edit`

这个偏“视频编辑/增强”，不是从零文生视频。`SKILL.md` 描述它可以 edit、remix、upscale、remove background、add audio/sound effects。脚本包括 `edit-video.sh` 和 `video-audio.sh`，可以对视频做 remix、内容编辑、超分、去背景、加声音。([GitHub][6])

下载研究：

```bash
git clone https://github.com/fal-ai-community/skills.git fal-ai-community-skills
cd fal-ai-community-skills
find skills/claude.ai/fal-video-edit -type f
```

适合研究：fal.ai 视频编辑 API 的 Claude Skill 封装方式。

---

### 7. `yuvalsuede/agent-media-skill`

这个偏 UGC 视频生产。README 写明它让 Claude Code 通过 `agent-media` CLI 生成完整 UGC 视频、Product Acting UGC、SaaS review videos，包括 AI talking heads、B-roll、voiceover、animated subtitles、background music。([GitHub][7])

下载研究：

```bash
git clone https://github.com/yuvalsuede/agent-media-skill.git
cd agent-media-skill
cat SKILL.md
```

安装方式：

```bash
npm install -g agent-media-cli
agent-media login
npx --yes skills add gitroomhq/agent-media --agent claude-code --yes
```

适合研究：商业 UGC 短视频工作流、AI 头像、字幕、B-roll 编排。

---

### 8. `AKCodez/promo-video-skill`

这个是产品/项目宣传视频 Skill。仓库说明里写到，Claude 会扫描你的 repo，构建 scenes，生成 voiceover，并渲染 landscape 和 portrait 两种 MP4。([GitHub][8])

下载研究：

```bash
git clone https://github.com/AKCodez/promo-video-skill.git
cd promo-video-skill
find . -name "SKILL.md" -o -name "*.md" -o -name "*.sh" -o -name "*.py"
```

适合研究：如何让 Claude 从代码仓库自动生成产品宣传视频。

---

### 9. `Square-Zero-Labs/video-prompting-skill`

这个不是直接生成视频，而是**视频生成 prompt 工程 Skill**。README 写明它用于 text-to-video / image-to-video 的 prompt 起草和优化，支持 Seedance 2.0、LTX-2、LTX-2.3、Sora、Veo 3/3.1、Wan 2.2、Ovi，并包含角色一致性/character sheet 工作流。([GitHub][9])

下载研究：

```bash
git clone https://github.com/Square-Zero-Labs/video-prompting-skill.git
cd video-prompting-skill
find . -type f
```

构建 `.skill` 文件：

```bash
mkdir -p dist
zip -r dist/video-prompting.skill video-prompting -x '**/.DS_Store'
```

适合研究：多视频模型 prompt 规范、角色一致性、图生视频前置流程。

---

## 可直接批量下载的脚本

```bash
mkdir -p ~/claude-video-skills-research
cd ~/claude-video-skills-research

git clone https://github.com/digitalsamba/claude-code-video-toolkit.git
git clone https://github.com/runwayml/skills.git runwayml-skills
git clone https://github.com/kdowswell/veo-tools.git
git clone https://github.com/inferen-sh/skills.git inferen-sh-skills
git clone https://github.com/fal-ai-community/skills.git fal-ai-community-skills
git clone https://github.com/yuvalsuede/agent-media-skill.git
git clone https://github.com/AKCodez/promo-video-skill.git
git clone https://github.com/Square-Zero-Labs/video-prompting-skill.git

find . -name "SKILL.md"
```

然后重点搜：

```bash
grep -R "video\|ffmpeg\|remotion\|runway\|veo\|wan\|seedance\|sora\|ltx\|fal\|voiceover\|subtitle" \
  -n ~/claude-video-skills-research | head -300
```

## 我的优先级建议

最值得先研究：

1. **`runwayml/skills`**：真正的视频生成 API Skill，官方背景强。
2. **`digitalsamba/claude-code-video-toolkit`**：完整生产流水线，最适合拆解 Claude Code 视频工作流。
3. **`Square-Zero-Labs/video-prompting-skill`**：研究多模型 prompt 规范很有价值。
4. **`fal-ai-community/skills/fal-video-edit`**：研究视频编辑增强类 Skill。
5. **`kdowswell/veo-tools`**：研究 Veo + Vertex AI 的 Claude Code 封装。
6. **`agent-media-skill` / `promo-video-skill`**：研究 UGC 和产品宣传视频的端到端 workflow。

另外提醒一下：Claude 社区 Skills 很新，质量差异很大。凡是要你登录 CLI、填 API Key、跑 shell 脚本的，都先读 `SKILL.md` 和脚本源码，尤其检查 `curl | sh`、`eval`、`rm -rf`、上传环境变量等风险。

[1]: https://github.com/digitalsamba/claude-code-video-toolkit "GitHub - digitalsamba/claude-code-video-toolkit: AI-native video production toolkit for Claude Code · GitHub"
[2]: https://github.com/runwayml/skills "GitHub - runwayml/skills: for Runway coding agent skills · GitHub"
[3]: https://github.com/kdowswell/veo-tools "GitHub - kdowswell/veo-tools: AI video generation skills for Claude Code - Google Veo 3.1, GCP setup, and seamless video loops · GitHub"
[4]: https://claudemarketplaces.com/skills/inferen-sh/skills/p-video "P Video | Claude Code Skills"
[5]: https://claudemarketplaces.com/skills/inferen-sh/skills/image-to-video "Image To Video | Claude Code Skills"
[6]: https://github.com/fal-ai-community/skills/blob/main/skills/claude.ai/fal-video-edit/SKILL.md "skills/skills/claude.ai/fal-video-edit/SKILL.md at main · fal-ai-community/skills · GitHub"
[7]: https://github.com/yuvalsuede/agent-media-skill "GitHub - yuvalsuede/agent-media-skill: Claude Code skill for AI video & image generation via agent-media CLI · GitHub"
[8]: https://github.com/AKCodez/promo-video-skill "GitHub - AKCodez/promo-video-skill: Claude Code skill that turns any SaaS/repo into a professional promo video — 30s, 60s, or 90s in landscape + portrait · GitHub"
[9]: https://github.com/Square-Zero-Labs/video-prompting-skill "GitHub - Square-Zero-Labs/video-prompting-skill: AI Agent Skill for Prompting Video Models · GitHub"


下载这些skills，好好研究它们每一个

> TOOL

<turn_aborted>
The user interrupted the previous turn on purpose. Any running unified exec processes may still be running in the background. If any tools/commands were aborted, they may have partially executed.
</turn_aborted>

> DEVELOPER

是的，**Claude Skills 社区里已经有不少“视频生成/视频制作”相关 Skills**。不过要分清两类：

1. **真正调用视频模型生成视频**：比如 Runway、Veo、P-Video、WAN、Seedance、fal.ai 等。
2. **用代码/工具合成视频**：比如 Remotion、FFmpeg、MoviePy、UGC 工作流、产品宣传视频等。

你上传的笔记里也提到，Claude 侧视频生产主要依赖 **Claude Code + Skills + 外部工具链**，例如 Remotion、video-toolkit、Runway、MoviePy、FFmpeg、TTS 等 。

## 我建议重点研究这些 Claude 社区视频 Skills

### 1. `digitalsamba/claude-code-video-toolkit`

这是目前我看到最完整的 Claude Code 视频制作工作台。它不是单一视频模型 Skill，而是一整套视频生产 workspace：包含 skills、commands、templates 和 tools，可以从 concept 到 final render 做完整视频。README 里写明它给 Claude Code 提供创建专业视频所需的构件，并支持 `/setup` 和 `/video` 工作流。([GitHub][1])

下载研究：

```bash
git clone https://github.com/digitalsamba/claude-code-video-toolkit.git
cd claude-code-video-toolkit
find . -name "SKILL.md" -o -name "*.md" -o -name "*.py"
```

适合研究：完整视频流水线、Remotion、配音、音乐、素材生成、FFmpeg、MoviePy。

---

### 2. `runwayml/skills`

这是 Runway 官方的 coding agent skills，支持 Claude Code、Cursor、Codex 等 agent。仓库说明里明确写了可以通过 Runway API 批量生成视频、图片和音频，支持产品视频、多镜头故事、创意迭代等；agent 会负责 API 调用、轮询任务完成、下载结果。([GitHub][2])

安装：

```bash
npx skills add runwayml/skills
```

下载研究：

```bash
git clone https://github.com/runwayml/skills.git
cd skills
find . -name "SKILL.md" -o -name "*.md" -o -name "*.ts" -o -name "*.js"
```

适合研究：真正的视频模型 API 编排、批量生成、Runway Gen 系列、Seedance、Veo 等模型路由。

---

### 3. `kdowswell/veo-tools`

这个是专门面向 **Google Veo 3.1 + Claude Code** 的视频生成 skills。仓库说明写的是通过 Vertex AI 生成 cinematic video content，适合网站 hero background、营销素材和 seamless loops。它支持 Claude Code plugin 安装，也支持手动复制 skills 到 `~/.claude/skills/`。([GitHub][3])

下载研究：

```bash
git clone https://github.com/kdowswell/veo-tools.git
cd veo-tools
find . -name "SKILL.md" -o -name "*.md" -o -name "*.sh" -o -name "*.py"
```

手动安装方式：

```bash
cp -r veo-tools/skills/* ~/.claude/skills/
```

注意：这个仓库目前星标很少，适合研究结构，不建议一上来就放生产 API key。

---

### 4. `inferen-sh/skills` 里的 `p-video`

Claude Code Marketplaces 上的 `P Video` skill 描述说，它通过 `inference.sh` CLI 调用 Pruna 优化模型，包装了 P-Video、WAN-T2V、WAN-I2V 三类模型，用于 text/image-to-video，输出 720p 或 1080p，适合原型视频、社交媒体短片、产品 mockup 动画。([claudemarketplaces.com][4])

安装：

```bash
npx skills add https://github.com/inferen-sh/skills --skill p-video
```

下载研究：

```bash
git clone https://github.com/inferen-sh/skills.git inferen-sh-skills
cd inferen-sh-skills
find . -name "SKILL.md" -o -name "*.md" -o -name "*.sh"
```

---

### 5. `inferen-sh/skills` 里的 `image-to-video`

同一个社区源里还有 `image-to-video` skill。Marketplace 描述说它把静态图片转成动画视频，背后使用 Wan 2.5 i2v、Seedance、Fabric 等模型，并强调更适合轻微运动、产品 demo、cinemagraph、社交媒体内容和概念图动效。([claudemarketplaces.com][5])

安装大致类似：

```bash
npx skills add https://github.com/inferen-sh/skills --skill image-to-video
```

---

### 6. `fal-ai-community/skills` 里的 `fal-video-edit`

这个偏“视频编辑/增强”，不是从零文生视频。`SKILL.md` 描述它可以 edit、remix、upscale、remove background、add audio/sound effects。脚本包括 `edit-video.sh` 和 `video-audio.sh`，可以对视频做 remix、内容编辑、超分、去背景、加声音。([GitHub][6])

下载研究：

```bash
git clone https://github.com/fal-ai-community/skills.git fal-ai-community-skills
cd fal-ai-community-skills
find skills/claude.ai/fal-video-edit -type f
```

适合研究：fal.ai 视频编辑 API 的 Claude Skill 封装方式。

---

### 7. `yuvalsuede/agent-media-skill`

这个偏 UGC 视频生产。README 写明它让 Claude Code 通过 `agent-media` CLI 生成完整 UGC 视频、Product Acting UGC、SaaS review videos，包括 AI talking heads、B-roll、voiceover、animated subtitles、background music。([GitHub][7])

下载研究：

```bash
git clone https://github.com/yuvalsuede/agent-media-skill.git
cd agent-media-skill
cat SKILL.md
```

安装方式：

```bash
npm install -g agent-media-cli
agent-media login
npx --yes skills add gitroomhq/agent-media --agent claude-code --yes
```

适合研究：商业 UGC 短视频工作流、AI 头像、字幕、B-roll 编排。

---

### 8. `AKCodez/promo-video-skill`

这个是产品/项目宣传视频 Skill。仓库说明里写到，Claude 会扫描你的 repo，构建 scenes，生成 voiceover，并渲染 landscape 和 portrait 两种 MP4。([GitHub][8])

下载研究：

```bash
git clone https://github.com/AKCodez/promo-video-skill.git
cd promo-video-skill
find . -name "SKILL.md" -o -name "*.md" -o -name "*.sh" -o -name "*.py"
```

适合研究：如何让 Claude 从代码仓库自动生成产品宣传视频。

---

### 9. `Square-Zero-Labs/video-prompting-skill`

这个不是直接生成视频，而是**视频生成 prompt 工程 Skill**。README 写明它用于 text-to-video / image-to-video 的 prompt 起草和优化，支持 Seedance 2.0、LTX-2、LTX-2.3、Sora、Veo 3/3.1、Wan 2.2、Ovi，并包含角色一致性/character sheet 工作流。([GitHub][9])

下载研究：

```bash
git clone https://github.com/Square-Zero-Labs/video-prompting-skill.git
cd video-prompting-skill
find . -type f
```

构建 `.skill` 文件：

```bash
mkdir -p dist
zip -r dist/video-prompting.skill video-prompting -x '**/.DS_Store'
```

适合研究：多视频模型 prompt 规范、角色一致性、图生视频前置流程。

---

## 可直接批量下载的脚本

```bash
mkdir -p ~/claude-video-skills-research
cd ~/claude-video-skills-research

git clone https://github.com/digitalsamba/claude-code-video-toolkit.git
git clone https://github.com/runwayml/skills.git runwayml-skills
git clone https://github.com/kdowswell/veo-tools.git
git clone https://github.com/inferen-sh/skills.git inferen-sh-skills
git clone https://github.com/fal-ai-community/skills.git fal-ai-community-skills
git clone https://github.com/yuvalsuede/agent-media-skill.git
git clone https://github.com/AKCodez/promo-video-skill.git
git clone https://github.com/Square-Zero-Labs/video-prompting-skill.git

find . -name "SKILL.md"
```

然后重点搜：

```bash
grep -R "video\|ffmpeg\|remotion\|runway\|veo\|wan\|seedance\|sora\|ltx\|fal\|voiceover\|subtitle" \
  -n ~/claude-video-skills-research | head -300
```

## 我的优先级建议

最值得先研究：

1. **`runwayml/skills`**：真正的视频生成 API Skill，官方背景强。
2. **`digitalsamba/claude-code-video-toolkit`**：完整生产流水线，最适合拆解 Claude Code 视频工作流。
3. **`Square-Zero-Labs/video-prompting-skill`**：研究多模型 prompt 规范很有价值。
4. **`fal-ai-community/skills/fal-video-edit`**：研究视频编辑增强类 Skill。
5. **`kdowswell/veo-tools`**：研究 Veo + Vertex AI 的 Claude Code 封装。
6. **`agent-media-skill` / `promo-video-skill`**：研究 UGC 和产品宣传视频的端到端 workflow。

另外提醒一下：Claude 社区 Skills 很新，质量差异很大。凡是要你登录 CLI、填 API Key、跑 shell 脚本的，都先读 `SKILL.md` 和脚本源码，尤其检查 `curl | sh`、`eval`、`rm -rf`、上传环境变量等风险。

[1]: https://github.com/digitalsamba/claude-code-video-toolkit "GitHub - digitalsamba/claude-code-video-toolkit: AI-native video production toolkit for Claude Code · GitHub"
[2]: https://github.com/runwayml/skills "GitHub - runwayml/skills: for Runway coding agent skills · GitHub"
[3]: https://github.com/kdowswell/veo-tools "GitHub - kdowswell/veo-tools: AI video generation skills for Claude Code - Google Veo 3.1, GCP setup, and seamless video loops · GitHub"
[4]: https://claudemarketplaces.com/skills/inferen-sh/skills/p-video "P Video | Claude Code Skills"
[5]: https://claudemarketplaces.com/skills/inferen-sh/skills/image-to-video "Image To Video | Claude Code Skills"
[6]: https://github.com/fal-ai-community/skills/blob/main/skills/claude.ai/fal-video-edit/SKILL.md "skills/skills/claude.ai/fal-video-edit/SKILL.md at main · fal-ai-community/skills · GitHub"
[7]: https://github.com/yuvalsuede/agent-media-skill "GitHub - yuvalsuede/agent-media-skill: Claude Code skill for AI video & image generation via agent-media CLI · GitHub"
[8]: https://github.com/AKCodez/promo-video-skill "GitHub - AKCodez/promo-video-skill: Claude Code skill that turns any SaaS/repo into a professional promo video — 30s, 60s, or 90s in landscape + portrait · GitHub"
[9]: https://github.com/Square-Zero-Labs/video-prompting-skill "GitHub - Square-Zero-Labs/video-prompting-skill: AI Agent Skill for Prompting Video Models · GitHub"


下载这些skills放入一个单独文件夹，好好研究它们每一个

> AGENT

我会先把这些仓库集中放到一个独立研究目录里，然后逐个读 `SKILL.md`、README 和脚本入口，最后给你一份结构化研究笔记。因为涉及 GitHub 下载，我会先按本地权限尝试；如果遇到网络沙箱拦截，会直接请求放行。

> AGENT

我用 `agent-reach` 的 GitHub 路由来做这件事：实际下载仍然走 `git clone`，研究阶段会优先看每个 repo 的 skill 定义和工具脚本，而不是运行它们。先确认目标目录和是否已有残留。

> AGENT

目录已建好：`/Users/lyston/PycharmProjects/claude-video-skills-research`。现在开始并行克隆 8 个仓库，先只下载源码，不执行任何安装或 API 登录命令。

> AGENT

网络沙箱把 GitHub DNS 拦住了，失败信息是 `Could not resolve host: github.com`。我现在会按要求用提权方式重新跑下载；仍然只做 clone，不执行仓库里的脚本。

> AGENT

第一个仓库已经下来了；`git clone` 的联网权限现在可用，我继续把剩下 7 个并行拉下来。

> AGENT

看起来刚才的授权没有变成持续规则，所以剩余仓库仍被沙箱 DNS 拦住。为了不让你点 7 次，我改用一次提权 shell 循环把剩余仓库拉齐，并在已存在时跳过。

> AGENT

`runwayml/skills` 这个仓库还在拉取中，可能体积或网络响应比较慢。我先等它结束；后面的仓库会按同一个循环继续下载。

> AGENT

这次不是 DNS 了，而是 GitHub 443 连接超时。第一个仓库已经完整成功，剩下的我会改成浅克隆 `--depth 1` 分批重试，降低传输量；如果某个仓库仍卡住，我会记录下来并继续处理已下载的部分。

> AGENT

浅克隆有效，`runwayml/skills` 已经下载好。接下来我用同样方式处理剩下 6 个。

> AGENT

默认沙箱还是不放 DNS；我把剩下 6 个也放进一次提权浅克隆循环。刚才 `runwayml` 用浅克隆 10 秒内完成，这条路靠谱。

> AGENT

8 个仓库现在都下齐了。接下来我会逐个扫：`SKILL.md`、README、commands/scripts、依赖入口和潜在风险点，然后把结果整理成一份本地研究笔记。

> AGENT

结构上比原始清单更丰富：`runwayml` 和 `inferen-sh` 都是一整个 skill 集合，`digitalsamba` 也带了多套内置 skills 和 Remotion 模板。现在我会重点读“视频相关入口”，避免被无关图片/音频/通用 UI skills 稀释掉。

> AGENT

`kdowswell/veo-tools` 这类 skill 的核心不是“脚本多”，而是前置工作流很强：强制理解、成片前验证、明确成本、用户批准再生成；这对我们以后设计视频 skill 很值得借。继续看 `inferen-sh`，它的视频 skill 数量最多。

> AGENT

我已经读完主要入口了，接下来会补一层“证据清单”：每个仓库的当前 commit、核心文件位置、视频相关 skill 数量。然后我把研究报告写到研究目录里，方便你之后继续深挖。

> AGENT

我现在要写本地研究报告，文件会放在 `/Users/lyston/PycharmProjects/claude-video-skills-research/RESEARCH_NOTES.md`。内容会按“能力、工作流、脚本/API、依赖与风险、可借鉴点、优先级”来组织。

> AGENT

下好了，也逐个研究完了。8 个仓库都放在：

[claude-video-skills-research](/Users/lyston/PycharmProjects/claude-video-skills-research)

我整理了一份 670 行的本地研究报告：

[RESEARCH_NOTES.md](/Users/lyston/PycharmProjects/claude-video-skills-research/RESEARCH_NOTES.md)

重点结论很清楚：

1. `digitalsamba/claude-code-video-toolkit` 最像完整视频生产系统，值得重点拆。
2. `runwayml/skills` 是最干净的官方视频模型 API 编排范式。
3. `kdowswell/veo-tools` 的“验证 prompt + 显示成本 + 等用户批准再生成”很值得借。
4. `AKCodez/promo-video-skill` 和 `agent-media-skill` 更偏端到端商业视频工作流。
5. `Square-Zero-Labs/video-prompting-skill` 最适合抽取成多模型 prompt 路由层。
6. `inferen-sh/skills` 和 `fal-ai-community/skills` 适合研究多模型 CLI 封装、队列轮询、异步任务与媒体编辑。

我没有执行任何安装、登录、API 调用或视频生成命令，只做了 clone、源码阅读和风险分析。报告里也标出了需要谨慎的点，比如 `curl | sh`、API key 写入 `.env`、GCP service account、付费模型调用、fal shell JSON 拼接和 ffmpeg shell 脚本里的 `eval`。这份研究很适合下一步沉淀成一个“Codex 视频 Skill 设计草案”，也值得保存到 MindOS 里方便之后跨会话继续用。

> DEVELOPER

我要的是中文文档

> AGENT

明白，是我刚才偷懒用了英文结构。现在我直接补一份完整中文研究文档，放在同一个目录里，英文版保留作备份。

> AGENT

已补上中文文档：

[中文研究报告.md](/Users/lyston/PycharmProjects/claude-video-skills-research/中文研究报告.md)

这份是完整中文版本，997 行，比刚才英文版更细一点。英文版我保留在 [RESEARCH_NOTES.md](/Users/lyston/PycharmProjects/claude-video-skills-research/RESEARCH_NOTES.md) 作为备份。

> DEVELOPER

再补充hermes社区 的视频生成相关的skills

> AGENT

我来补这一块。先确认“hermes 社区”在本机已有目录里指的是哪个项目/索引，同时用搜索补一层 GitHub/社区来源，避免只看本地残片。

> AGENT

我会把它并入现有研究目录和中文报告，不另起一套散落目录。先查本地 `hermes`/`hermes-agent` 里面是否已经带了 marketplace 或 skills 索引。

> AGENT

本地已经有两块 Hermes 相关内容：一个是 `/Users/lyston/PycharmProjects/hermes/video_agent_skill_research` 的视频技能研究集，一个是 `/Users/lyston/PycharmProjects/hermes-agent/skills` 里的 Hermes Agent 社区技能。我先读真正和视频生成/制作相关的 Skill，再补中文报告。

> AGENT

这里我看到一个有用线索：你本机 `hermes/video_agent_skill_research` 其实已经有一份 Hermes 视频 Agent 矩阵草稿；`hermes-agent` 里也有若干内置/optional skills。现在我把这些可落地的 Hermes 视频相关 Skill 读一遍，区分“真正生成视频”“程序化视频”“MCP 驱动外部工具”“视频质检/后处理”。

> AGENT

收到，我继续把 Hermes 社区这一块补到中文研究文档里。现有本地 `hermes` / `hermes-agent` 里已经有一批视频相关 skill 线索，我会按“真视频生成、动画合成、创意视觉、头像/UGC、音频辅助、MCP 桥接”来整理。

> AGENT

我已经确认 Hermes 官方/本地 agent 仓库里，视频相关并不只是“视频模型 skill”，还包含很多适合做视频前后处理的创意技能，比如 ASCII 视频、Manim、p5.js、Pixel Art、AudioCraft 和 Remotion/Blender/TouchDesigner 这类桥接工具。接下来我会补齐外部 Hermes 社区条目的说明，再落成一份中文补充文档。

> AGENT

我准备在原研究目录里新建一个 Hermes 补充区，把已核验的 Hermes 视频相关 skill 源文件快照放进去，并写一份中文补充报告。这样主报告不会被塞得太臃肿，但入口会清楚连上。

> AGENT

源文件快照已经放进原来的研究目录了，包括 Hermes bundled skills、optional skills，以及你本地已有的外部研究条目。现在我开始写中文补充文档，并在主报告里加入口和摘要。

> DEVELOPER

继续

> AGENT

好，我继续把 Hermes 补充接进主中文报告，并加一个目录入口，让之后打开研究文件夹时不会迷路。刚才补充文档已经写完，下面做收口和校验。

> AGENT

主中文报告已经补上 Hermes 的摘要、入口、风险点和后续架构建议。最后我再补一个顶层中文 README，把“先看哪个文件、各目录是什么”讲清楚。

> AGENT

继续补好了，已经把 Hermes 社区视频相关 skills 加进同一个研究目录。

新增/更新了这几个中文文件：

- [README.md](/Users/lyston/PycharmProjects/claude-video-skills-research/README.md)：顶层入口，说明先看哪些文档。
- [中文研究报告.md](/Users/lyston/PycharmProjects/claude-video-skills-research/中文研究报告.md)：已加入 Hermes 摘要、风险点和架构建议。
- [Hermes社区视频Skills补充.md](/Users/lyston/PycharmProjects/claude-video-skills-research/Hermes社区视频Skills补充.md)：Hermes 专项中文补充，约 780 行。

Hermes 相关 skill 快照也放进了：

[hermes-community-video-skills](/Users/lyston/PycharmProjects/claude-video-skills-research/hermes-community-video-skills)

覆盖了 `inference-sh ai-video-generation`、`video-master`、Remotion、HeyGen MCP、Felo Slides、`p5js`、`manim-video`、`ascii-video`、`pixel-art`、`blender-mcp`、`touchdesigner-mcp`、AudioCraft、HeartMuLa 等。

这次仍然只做静态研究和文档整理，没有执行安装脚本、登录、API 调用、MCP 服务启动或真实视频生成。参考的公开入口包括 [Hermes Skills Hub](https://hermes-agent.nousresearch.com/docs/skills/)、[Hermes bundled skills catalog](https://hermes-agent.nousresearch.com/docs/reference/skills-catalog)、[Hermes optional skills catalog](https://hermes-agent.nousresearch.com/docs/reference/optional-skills-catalog)。

> DEVELOPER

我要你全都写到一起：视频生成skills研究报告

> AGENT

明白，你要的不是“主报告 + Hermes 补充报告”这种分散形态，而是一个完整单文件：`视频生成skills研究报告`。我现在把 Claude 社区和 Hermes 社区两部分合并成一份总报告，并把目录入口也改成指向这一份。

> AGENT

总报告文件已经生成了。我再把 README 的“先看两个文档”改成“先看一个总报告”，保留原拆分文档作为备查。

> AGENT

我看了一眼生成后的总报告，内容已经合并，但里面还残留了一句“另见 Hermes 补充文档”的旧提示。我顺手把它清掉，并加一个阅读结构，让这份文件更像最终版单体报告。

> AGENT

已经合并成一份单文件总报告：

[视频生成skills研究报告.md](/Users/lyston/PycharmProjects/claude-video-skills-research/视频生成skills研究报告.md)

我也更新了入口文件：

[README.md](/Users/lyston/PycharmProjects/claude-video-skills-research/README.md)

现在 `视频生成skills研究报告.md` 里已经把 Claude / Agent 社区和 Hermes 社区的视频生成、视频制作、Remotion、Avatar、MCP、创意视觉、音乐音效相关 skills 全部写到一起了，共约 1800 行。原来的拆分版文档还保留作备查。

> DEVELOPER

不能只是简单的拼接在一起

> AGENT

对，你说得对。刚才那版只是把两份文档接在一起，能查资料，但不像一份“研究报告”。我现在重写成真正整合版：统一分类、统一结论、统一能力矩阵，再把每个 skill 放进同一套分析框架里。

> AGENT

我会直接替换 `视频生成skills研究报告.md`，不再保留“第一部分/第二部分”这种拼接痕迹，而是改成按能力和生产链路组织的一份完整报告。原拆分文档仍保留在旁边，不会动。

> AGENT

重写已经完成，现在这份报告是按“视频生产链路”和“能力层”整合的，不再是两份文档前后拼接。我再快速检查标题、章节、行数和关键 skill 是否都还在。

> AGENT

对，这次我已经重写了，不是简单拼接。

已替换为一份真正整合版报告：

[视频生成skills研究报告.md](/Users/lyston/PycharmProjects/claude-video-skills-research/视频生成skills研究报告.md)

现在结构是按视频生产链路组织的：

- 研究范围
- 一页结论
- 能力总览矩阵
- 推荐视频 Agent 架构
- 分类研究：完整工作台、模型生成、prompt 分镜、avatar、创意视觉、装配、音频、安全检测
- Skill 质量评价标准
- 产品化优先级
- 安全风险清单
- 最值得先读的文件
- 最终建议

我也检查过了，旧的“第一部分 / 第二部分”拼接结构已经去掉。报告现在约 1150 行，Claude / Agent 社区和 Hermes 社区的 skills 都被放进同一套分析框架里了。

> DEVELOPER

接下来搜索这两个社区的图片生成skills和工具等，也写一个研究报告

> AGENT

明白，接下来做“图片生成 Skills / 工具”的同类研究报告，而且要覆盖刚才那两个生态：Claude / Agent 社区和 Hermes 社区。我会先查本地已有仓库，再用公开源补齐当前社区里的图片生成、图片编辑、图像工具链和多模型路由。

> AGENT

本地检索已经抓到一批明确的图片方向入口：Runway 的 `rw-generate-image` / `rw-integrate-image`，inference.sh 的 `ai-image-generation`，DigitalSamba 里的 FLUX.2 / Qwen Image Edit / Real-ESRGAN，Hermes 的 Stable Diffusion、Segment Anything、Pixel Art、Meme、Concept Diagrams 等。现在我补一轮公开源检索，避免只依赖本地旧快照。

> AGENT

公开和本地两边都确认了：图片方向比视频方向更分散，除了“文生图 / 图生图”，还有 image edit、upscale、remove background、try-on、restore、product photography、logo / thumbnail / app store visuals、meme、diagram、segmentation、Stable Diffusion 本地部署等。接下来我按同一套框架读核心 SKILL 文件，然后写成一份整合报告。

> AGENT

我已经把核心证据读完了：Runway 是官方图片 API skill；fal.ai 覆盖生成、编辑、upscale、restore、try-on、vision、workflow；inference.sh 的 image 目录很完整，包含 FLUX、Qwen、Gemini/Nano Banana、P-Image、背景移除、upscale、产品摄影；Hermes 侧则覆盖 Stable Diffusion、本地像素/梗图/图表/漫画/信息图/SAM 等。现在写成单文件研究报告，不做资料堆叠。

> AGENT

初版报告已经写好，是按“图片生产链路”整合的单文件。我再补一个目录 README，并做关键词和章节校验，确保它不是遗漏式清单。

> AGENT

已完成，新的图片方向研究报告在这里：

[图片生成skills研究报告.md](/Users/lyston/PycharmProjects/image-generation-skills-research/图片生成skills研究报告.md)

也加了目录入口：

[README.md](/Users/lyston/PycharmProjects/image-generation-skills-research/README.md)

这份报告是整合版，不是按仓库拼接。它按图片生产链路组织：brief、prompt、文生图/图生图、图片编辑、抠图/分割、超分/修复、产品摄影、试穿、视觉分析、漫画/信息图/SVG、workflow 和安全风险。

覆盖了 Runway、fal.ai、inference.sh、DigitalSamba、Hermes Stable Diffusion、Segment Anything、Pixel Art、Meme、Concept Diagrams、Baoyu Comic / Infographic 等。

本次仍然只做搜索、源码静态阅读和文档整理，没有执行安装、登录、API 调用或真实图片生成。

参考公开源包括：[runwayml/skills](https://github.com/runwayml/skills)、[fal-ai-community/skills](https://github.com/fal-ai-community/skills)、[inferen-sh/skills](https://github.com/inferen-sh/skills)、[NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)、[Hermes skills catalog](https://hermes-agent.nousresearch.com/docs/reference/skills-catalog)、[Hermes optional skills catalog](https://hermes-agent.nousresearch.com/docs/reference/optional-skills-catalog)。

> DEVELOPER

image-generation-skills-research和claude-video-skills-research都放入同一个文件夹下

> AGENT

可以，我把它们收进一个专门的父目录里，避免散在 `PycharmProjects` 根下。目录名我用 `ai-media-skills-research`，里面放视频和图片两套研究。

> AGENT

两个目录已经移到同一个父目录里了。我再把报告里的旧绝对路径替换成新位置，并加一个父目录 README，之后从一个入口就能找到视频和图片研究。

> AGENT

已整理到同一个父目录下：

[ai-media-skills-research](/Users/lyston/PycharmProjects/ai-media-skills-research)

里面现在是：

- [claude-video-skills-research](/Users/lyston/PycharmProjects/ai-media-skills-research/claude-video-skills-research)
- [image-generation-skills-research](/Users/lyston/PycharmProjects/ai-media-skills-research/image-generation-skills-research)

我也新增了父目录入口：

[README.md](/Users/lyston/PycharmProjects/ai-media-skills-research/README.md)

并把两个研究目录里的旧绝对路径更新成新路径了。原来散在 `/Users/lyston/PycharmProjects` 根下的两个目录已经移动完成。
