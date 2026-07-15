> DEVELOPER

帮我到github上搜索关于写剧本的skills，特别是创意剧本

> AGENT

我会按 `agent-reach` 的 GitHub 搜索路线来查，重点找包含 `SKILL.md`、AI agent skills、creative writing/screenplay/scriptwriting 这些关键词的仓库或文件。

> AGENT

我已经确认这个技能建议用 GitHub CLI 做代码/仓库检索。接下来我会先搜仓库，再搜具体 `SKILL.md` 文件内容，这样能区分“泛写作提示词”和真正可安装/可复用的 skill。

> AGENT

本地 `gh` 可用，但沙箱里的网络连不上 GitHub API；我会按权限规则重新请求一次联网执行。与此同时，网页搜索已经浮出一个很相关的仓库：`danjdewhurst/story-skills`，它是面向小说/故事创作的 `SKILL.md` 技能集合，Codex 也能用。

> AGENT

网页搜索的结果比 GitHub API 直接关键词更有效：很多 skill 被技能市场索引到，但源头仍是 GitHub。我会点开几个最像“创意剧本/编剧”的源仓库，确认它们是不是完整的 `SKILL.md` 技能，而不是单篇教程。

> AGENT

我搜了一圈，最值得看的几个是这些：

1. [GongLingRui/screen-creative-skills](https://github.com/GongLingRui/screen-creative-skills)  
   最贴近你说的“创意剧本”。中文仓库，31 个影视创作/评估/策划 skills，覆盖竖屏短剧、中长剧、电视剧、电影剧本、IP 改编。重点看：
   [drama-creator](https://github.com/GongLingRui/screen-creative-skills/blob/master/category/creation/drama-creator/SKILL.md)、`drama-planner`、`story-outliner`、`character-profile`、`script-evaluator`。

2. [haowjy/creative-writing-skills](https://github.com/haowjy/creative-writing-skills)  
   偏“创意写作工作流”，适合故事开发、人物、场景、风格、连续性维护。不是纯影视剧本，但很适合做剧本前期：世界观、人物弧光、场景构建、批评修改。它的 `scene-construction`、`story-architecture`、`brainstorming` 很值得拆出来用。

3. [danjdewhurst/story-skills](https://github.com/danjdewhurst/story-skills)  
   结构清爽，支持 Codex 的 `SKILL.md` 标准。包含 `story-init`、`character-management`、`worldbuilding`、`plot-structure`、`chapter-writing`。适合搭建一个“故事圣经 + 人物 + 世界观 + 剧情线”的长期项目。

4. [theneoai/awesome-skills 的 scriptwriter](https://github.com/theneoai/awesome-skills/blob/main/skills/creative/scriptwriter/SKILL.md)  
   这是更直接的“编剧专家” skill：电影、电视、剧场、互动媒体，重点在三幕式、人物弧、对白、beat sheet。相比第 1 个，它更偏英文影视编剧方法论，不太偏中文短剧商业套路。

我的建议：  
如果你要做中文短剧/影视项目，先看 `GongLingRui/screen-creative-skills`。如果你想做“创意剧本孵化系统”，用 `haowjy/creative-writing-skills` 做创意、人物、结构，再配 `theneoai/scriptwriter` 做剧本格式和对白，会更顺手。

> DEVELOPER

我想要的是偏广告类的创意剧本

> AGENT

明白了，你要的不是泛故事/影视编剧，而是广告片、品牌短片、TVC、短视频投放脚本这一类。我会重新按“广告创意/创意总监/copywriting/commercial script/storyboard”这些词搜 GitHub，并优先找能直接作为 skill 使用的 `SKILL.md`。

> AGENT

重新按“广告创意剧本”筛了一遍，最相关的是这些：

1. [Ethanxwang/tvc-director](https://github.com/Ethanxwang/tvc-director)  
   最推荐。它就是 **TVC 广告创意导演** skill，从产品 brief 到创意提案、视觉定调、分镜、视频脚本。适合品牌片、产品广告、15/30 秒 TVC、质感广告片。它内置 8 种 TVC 叙事模型，比如痛点-解决、产品电影化拆解、品牌世界穿梭、情感锚点、前后对比等。

2. [alchaincyf/huashu-skills/huashu-douyin-script](https://github.com/alchaincyf/huashu-skills/blob/master/huashu-douyin-script/SKILL.md)  
   最适合 **抖音/短视频投放脚本**。它的流程是竞品视频拆解 → 爆款公式提炼 → 脚本 + 分镜生成 → 审校，明确支持“种草视频”和“千川投放素材”。如果你的广告偏转化、带货、信息流，这个很有用。

3. [coreyhaines31/marketingskills/ad-creative](https://github.com/coreyhaines31/marketingskills/blob/main/skills/ad-creative/SKILL.md)  
   偏 **效果广告创意与文案变体**，适合 Google/Meta/LinkedIn/TikTok 广告的标题、主文案、广告角度、批量测试。它不是完整“剧本导演型”，但适合补强 hook、卖点角度和 A/B 创意变体。

4. [coreyhaines31/marketingskills/social-content](https://github.com/coreyhaines31/marketingskills/blob/main/skills/social-content/SKILL.md)  
   偏 **短视频内容脚本**，有 3 秒钩子、短视频结构、TikTok/Reels/Shorts 思路。更适合自然流内容，但可以改造成广告短视频脚本辅助 skill。

5. [dexhunter/seedance2-skill 中文版](https://github.com/dexhunter/seedance2-skill/blob/main/zh/SKILL.md)  
   偏 **视频生成提示词**，不是创意策划本身。但它有电商/产品展示、产品广告片模板，适合把已经写好的广告脚本转成 Seedance/即梦可用的视频提示词。

我的排序建议：  
做品牌/TVC：先用 `tvc-director`。  
做抖音/千川/带货：先用 `huashu-douyin-script`。  
做投放文案批量测试：加 `ad-creative`。  
做 AI 成片提示词：最后接 `seedance2-skill`。

> DEVELOPER

帮我下载第一个

> AGENT

好，我把第一个 `Ethanxwang/tvc-director` 下载下来。因为这是一个 Codex skill，我会先按 skill 安装流程看一下它应该放在哪里，再执行下载。

> AGENT

安装器支持直接从 GitHub 仓库安装。我会用官方脚本把仓库里的 skill 下载到 `~/.codex/skills`，如果仓库结构不是标准 skill，再改成克隆后定位 `SKILL.md`。

> AGENT

这个仓库看起来是“整个仓库就是一个 skill”，安装脚本传 `--path .` 会因为名字是 `.` 被拒。小弯路，我先看一下安装脚本参数，然后指定一个明确名字来装。

> AGENT

已安装成功。我再快速确认一下目录里有 `SKILL.md` 和它带的参考文件，确保不是空壳。

> AGENT

已下载并安装成功：[/Users/lyston/.codex/skills/tvc-director/SKILL.md](/Users/lyston/.codex/skills/tvc-director/SKILL.md)

它包含 `SKILL.md`、中英文 README，以及分镜、前期筹备、镜头语言、交付等参考文件。重启 Codex 后就能自动识别这个新 skill。

> DEVELOPER

这个skill叫什么

<image>
</image>

> AGENT

这个 skill 叫：`tvc-director`

它的标题是：**TVC Director · TVC 广告创意导演工作台**

如果你在技能列表里还没看到它，重启 Codex 后应该会出现，显示名大概率是 **Tvc Director** 或 **TVC Director**。路径是：

`/Users/lyston/.codex/skills/tvc-director/SKILL.md`

> DEVELOPER

重启了没有出现

> AGENT

我来排查一下：它确实装到了 `~/.codex/skills/tvc-director`，但 Codex UI 没显示，通常是加载目录、缓存、或 `SKILL.md` 元数据解析不通过。先确认本地文件状态和前置元数据。

> AGENT

文件本身没丢，`SKILL.md` 也在；现在最像的问题是 Codex 的 skill 加载器没接受它的元数据。这个仓库的 `description` 特别长，而且带了一些非 ASCII 标点，UI 可能直接跳过了它。ನ

> AGENT

我看到 `codex-md-docs` 的元数据比较短，`mindos-zh` 用的是折叠块格式；`tvc-director` 这个安装版把超长描述塞在一行里。下一步我会把它的 frontmatter 调整成更稳的格式，只动元数据，不改正文能力。

> AGENT

元数据已经缩短并改成了更常见的 YAML 折叠块。为了防止 macOS quarantine 扩展属性影响扫描，我也会检查并移除这个 skill 目录上的隔离属性。

> AGENT

`com.apple.provenance` 这个扩展属性删不掉，属于 macOS 的来源标记，通常不是问题。更关键的是我刚刚已经修了最可能导致 UI 跳过的长描述元数据；我再检查一下 Codex 是否有自己的技能索引/缓存，看看要不要清它。

> AGENT

还有一种可能：你现在这个会话是在安装前创建的，技能列表可能是“创建会话时的快照”，继续旧会话不会重新注入新 skill。先别急，我再确认一下 Codex 实际会扫描哪些目录，必要的话把它也同步到 `.agents/skills` 目录。

> AGENT

从当前环境看，Codex 同时会展示 `~/.agents/skills` 和 `~/.codex/skills` 里的技能；截图里的 Agent Reach/MindOS 就来自 `~/.agents/skills`。我把 `tvc-director` 也同步一份到那个目录，让它走和 Agent Reach 一样的加载路径。

> AGENT

我查到了两个可能原因，并已经处理了一个：

1. 原版 `SKILL.md` 的 `description` 太长，我已改成更稳的短 YAML 格式。
2. 我又把它同步到了和 `Agent Reach`、`Mindos Zh` 一样的目录：  
   `~/.agents/skills/tvc-director`

现在它有两份：

`/Users/lyston/.codex/skills/tvc-director/SKILL.md`  
`/Users/lyston/.agents/skills/tvc-director/SKILL.md`

你需要 **完全退出 Codex 再打开，并新建一个会话** 看技能列表。老会话的技能列表通常是创建会话时的快照，所以即使重启，继续这个老会话也可能还是看不到。

它显示名应该是：**Tvc Director**  
触发名是：`tvc-director`

> DEVELOPER

现在为什么又有两个？

<image>
</image>

> AGENT

是我刚才为了让它显示出来，把同一个 skill 放到了两个会被 Codex 扫描的目录里：`~/.codex/skills` 和 `~/.agents/skills`。现在它们都被识别了，所以列表里出现了两个 `Tvc Director`。我保留官方安装目录里的那份，删除我临时同步到 `~/.agents` 的副本就能恢复成一个。

> AGENT

因为我刚才为了排查“为什么不显示”，把同一个 skill 临时放了两处：

`~/.codex/skills/tvc-director`  
`~/.agents/skills/tvc-director`

Codex 两个目录都会扫描，所以出现了两个。

我已经删掉重复的 `~/.agents/skills/tvc-director`，现在只保留官方安装位置这一份：

`/Users/lyston/.codex/skills/tvc-director/SKILL.md`

重新打开/新建会话后应该只剩一个 `Tvc Director`。

> DEVELOPER

这几个skills都不够好

> AGENT

你这个判断我同意：这些现成 skill 多半只是“广告视频提示词/分镜工具”，缺少真正广告创意里的 **洞察、反差、概念跳跃、品牌记忆点、可传播性**。我会直接给你做一个更适合“创意营销剧本”的本地 skill，而不是继续凑 GitHub 上的半成品。

> AGENT

我会把它做成一个新的、更“广告公司创意部”取向的 skill：先抓品牌/人群/冲突洞察，再出大创意、传播梗、30/60 秒脚本、分镜和可生成画面，而不是一上来堆镜头提示词。这个会比现成的 TVC/video prompt 类 skill 更适合你要的“天马行空但能落地”的创意营销剧本。

> AGENT

我会按 `skill-creator` 规范新建一个本地 skill，名字先定为 `ad-creative-script`：专门用于广告创意剧本、品牌营销短片、TVC/信息流脚本、分镜和 AI 生成画面提示词。它会保留“创意发散”能力，但输出必须能落到可拍/可生成的脚本。

> AGENT

初始化时目录已经建出来了，但 UI 的 `short_description` 太短被校验挡了一下。没关系，我接着把这个 skill 填完整，再用校验脚本跑一遍。

> AGENT

模板已经生成，接下来我会手工写核心说明和几个参考文件：一个负责创意诊断/大创意方法，一个负责广告脚本输出格式，一个负责分镜与 AI 画面生成交付。这样主 `SKILL.md` 不会臃肿，但真正使用时有深度可读。

> AGENT

核心文件已经写完。我现在跑官方 quick validate，再把 UI 元数据也检查一下，避免又出现“不显示/重复/字段过长”这类小麻烦。

> AGENT

校验脚本本身缺 `PyYAML`，不是 skill 文件的问题。我不会为了这个去装依赖；改用系统里已有的 Ruby/Python 基础解析做一次 YAML/frontmatter 检查，再确认目录没有重复副本。

> AGENT

我直接给你做了一个新的本地 skill，专门偏 **广告创意剧本/品牌营销短片/天马行空创意路线/分镜/AI 画面提示词**，比 `tvc-director` 更靠近广告公司创意部的工作方式。

名字是：`ad-creative-script`  
显示名是：**Ad Creative Script**  
文件在：[SKILL.md](/Users/lyston/.codex/skills/ad-creative-script/SKILL.md)

它包含三份参考：
- [creative-methods.md](/Users/lyston/.codex/skills/ad-creative-script/references/creative-methods.md)：洞察、大创意、反差、传播记忆点
- [script-formats.md](/Users/lyston/.codex/skills/ad-creative-script/references/script-formats.md)：TVC、品牌片、短视频投放脚本格式
- [storyboard-ai-prompts.md](/Users/lyston/.codex/skills/ad-creative-script/references/storyboard-ai-prompts.md)：分镜和 AI 图/视频提示词

我也加了 UI 元数据：[openai.yaml](/Users/lyston/.codex/skills/ad-creative-script/agents/openai.yaml)

说明一下：官方 `quick_validate.py` 因为本机缺 `PyYAML` 没跑起来，但我用 Ruby YAML 解析检查过 `SKILL.md` 和 `openai.yaml`，格式是 OK 的。重启 Codex、新建会话后，技能列表里应该会出现 **Ad Creative Script**。

> DEVELOPER

还有继续优化
1.你怎么保证每次使用skill生成的剧本创意不会雷同
2.你怎么保证使用skill对于比较多的行业都有效
3.你怎么保证剧本的创意质量？怎么评判？在我看来很多生成的剧本创意都不行，但是你确认为是可以的

> AGENT

你提的这三个点正好是现成广告 skill 的硬伤：它们只会“生成”，不会防撞车、不会跨行业迁移、也不会用残酷标准自审。我会把这个 skill 升级成带 **创意去重机制、行业适配器、质量评审闸门** 的版本，并明确说明“不能绝对保证”，但能把劣质创意拦在输出前。

> AGENT

我会先看现有 skill 内容，然后补两份新的 reference：一个专门管“去雷同/发散矩阵”，一个专门管“质量评审/杀稿标准”。同时把主工作流改成必须先过评审再交稿。

> AGENT

现在动刀：主文件里会新增“不能保证绝对不雷同，但必须执行去重搜索和创意变异”的规则；行业有效性用“行业适配器矩阵”；质量用“红队评审闸门”，不达标就不许把初稿当成最终稿。

> AGENT

主流程已经加上三道门。接下来我会把“行业适配器”写得具体一些，不靠空泛行业列表，而是让每个行业都有购买心理、常见烂套路、有效创意方向和风险边界。

> AGENT

行业覆盖已经补上，尤其把奶粉/母婴这类高信任、高敏感行业单独写了。现在补“创意质量怎么评判”：会有杀稿线、评分表、常见自嗨误判、以及用户觉得“不行”时如何重构。

> AGENT

评审闸门写好了。我还要把已有的 `creative-methods` 里的评估段升级一下，让它和新的质量评分、去雷同矩阵互相配合。

> AGENT

优化已经落到文件了。最后我会检查 YAML、文件清单和 UI 元数据；如果没有解析问题，就把新增机制用很直白的话告诉你，方便你判断还要不要继续收紧标准。

> AGENT

你这三个问题我已经直接写进 skill 机制里了，而且没有用“保证”这种虚话。现在它的规则是：**不能绝对保证每条都原创/高质量，但必须先过闸门，差的不能直接当最终稿交付。**

已优化：

1. **防雷同机制**  
   新增 [anti-sameness.md](/Users/lyston/.codex/skills/ad-creative-script/references/anti-sameness.md)  
   会先列行业烂套路、当前会话已用过的创意路线、禁用视觉母题，再用“情绪/尺度/现实感/产品角色/结尾”等轴强制分叉。

2. **多行业适配机制**  
   新增 [industry-adapters.md](/Users/lyston/.codex/skills/ad-creative-script/references/industry-adapters.md)  
   覆盖母婴奶粉、食品饮料、美妆、健康、金融、科技、家电、汽车、教育、B2B、奢侈品、零售、旅行、游戏、公益等。每类都有购买心理、信任障碍、证明方式、常见烂套路、有效创意方向和风险边界。

3. **创意质量评审机制**  
   新增 [quality-rubric.md](/Users/lyston/.codex/skills/ad-creative-script/references/quality-rubric.md)  
   加了杀稿线：产品不可替换、洞察必须能被拍出来、必须有记忆点、创意跳跃必须能回到卖点、不能只是漂亮空镜或靠 VO 硬解释。低分路线要重构，不是润色。

4. **主流程已升级**  
   [SKILL.md](/Users/lyston/.codex/skills/ad-creative-script/SKILL.md) 现在明确要求三道门：  
   `Anti-sameness gate`、`Industry-fit gate`、`Quality gate`

我还检查了 YAML 解析，格式没问题。重启/新建会话后这个 skill 会按新版规则工作。

> DEVELOPER

使用这个skill给我生成一个奶粉营销的剧本

> AGENT

我会用 `ad-creative-script` 来做，不直接写“温馨妈妈+宝宝成长”的常规片。先按它的规则过一遍母婴行业适配、反雷同和质量闸门，再给你完整剧本。

> AGENT

使用 `$ad-creative-script` 生成一版。假设品牌名暂用 **「某奶粉品牌」**，不写具体营养功效，避免踩“智力/身高/免疫保证”这类风险。

**片名：给明天的一小勺**  
**形式：60s 品牌营销短片 / TVC**  
**核心创意：**  
不是父母在选择一个“完美未来”，而是每天把一点确定感，悄悄交给明天的孩子。

**一句话概念：**  
夜里冲奶时，厨房里出现了一间“明天寄来的小邮局”，每一件未来寄回来的小物，都不是成功证明，而是孩子长大后那些普通、勇敢、真实的瞬间。

**剧本**  
| 时间 | 画面 | VO / 对白 | 产品角色 |
|---|---|---|---|
| 00-06s | 深夜厨房。妈妈拿着奶粉勺，停在罐口上方。桌上有奶瓶、便签、没回完的育儿群消息。 | VO：有些选择，很小。小到只有一勺。 | 奶粉罐首次出现，处于真实夜间育儿场景。 |
| 06-12s | 勺子落下的一瞬间，奶粉像细雪一样飘起。厨房一角悄悄亮起，变成一间微型邮局，牌子写着：**明天邮局**。 | 无对白。只有轻微铃声。 | 奶粉粉末成为打开想象世界的触发物。 |
| 12-20s | 第一封信滑到桌上。里面是一根小小的鞋带，带着泥点。画面切到几年后，一个孩子蹲在操场边，笨拙地自己系鞋带。 | 孩子小声说：我可以自己来。 | 产品不声称“让孩子会什么”，只连接父母日常照护与孩子普通成长瞬间。 |
| 20-28s | 第二个包裹打开，是一张皱巴巴的画：一家三口站在一片蓝色大海前。画中海水忽然漫出，在厨房地砖上变成温柔的蓝光。 | VO：我们不知道明天会寄回什么。 | 奶瓶旁的奶粉罐稳定在画面中，像日常里的锚点。 |
| 28-38s | 第三封信是一枚没有名次的手工奖章，上面歪歪扭扭写着：**今天没哭太久奖**。妈妈看着笑了，眼眶微湿。 | VO：也许不是第一名，也许不是最耀眼。 | 品牌价值从“赢”转为“支持真实成长”。 |
| 38-48s | 邮局里越来越多小物浮起：半块橡皮、第一次远足的小石头、写错字的贺卡、摔跤后贴过的创可贴。它们围绕奶瓶和奶粉罐，形成一个小小星系。 | VO：但每一个明天，都需要今天有人认真地照顾。 | 产品成为“认真照顾”的一部分，不夸大功效。 |
| 48-55s | 妈妈冲好奶。微型邮局慢慢收起。宝宝在怀里安静喝奶。妈妈把那枚“今天没哭太久奖”轻轻夹进育儿日记。 | 妈妈轻声：慢慢来。 | 产品回到真实使用场景。 |
| 55-60s | End Frame：奶粉罐、奶瓶、育儿日记放在柔和晨光里。日记页上写着：**把今天照顾好，明天会回信。** | VO：某奶粉品牌，陪你认真照顾每一个今天。 | 品牌收束，留 logo / slogan / 合规营养卖点空间。 |

**分镜记忆点**  
1. 奶粉落下，厨房变成“明天邮局”。  
2. 未来寄回来的不是奖杯，而是鞋带、画、石头、创可贴。  
3. “今天没哭太久奖”作为情绪记忆点。  
4. End Frame：**把今天照顾好，明天会回信。**

**创意评估**  
这版避开了母婴广告常见的“完美宝宝、焦虑妈妈、实验室背书、赢在起跑线”。产品不是硬贴上去，而是作为“每天认真照顾”的触发点和锚点。需要后续接品牌真实卖点时，可以把合规营养信息放在 55-60s 的 pack shot 或辅助字幕里。

> DEVELOPER

这个剧本太垃圾了，更本没有创意，你先好好上网学习一下什么叫做创意再优化这个skill

> AGENT

你说得对，这版只是“有包装的温情”，不是足够硬的创意。我会按你的要求先上网看权威广告创意/创意效果评审标准和优秀案例方法论，再把 skill 改成更狠的版本：少一点漂亮故事，多一点洞察冲突、创意跳跃、传播性和杀稿机制。

> AGENT

我已经看了 Cannes Lions、WARC、Ehrenberg-Bass、System1、LinkedIn B2B Institute 等关于创意评审和广告效果的资料。结论很明确：刚才那个脚本最大的问题不是“不够温情”，而是没有形成强记忆资产、没有反常识的创意装置，也没有能被复述/扩展的品牌平台。

> TOOL

<turn_aborted>
The user interrupted the previous turn on purpose. Any running unified exec processes may still be running in the background. If any tools/commands were aborted, they may have partially executed.
</turn_aborted>

> DEVELOPER

最大的缺点是没有想象力

> AGENT

对，核心不是“质量评审还不够细”，而是它没有强迫自己进入真正的想象力区。刚才那版用了“明天邮局”这种温柔隐喻，但它仍然属于母婴广告熟悉语法：夜晚、妈妈、成长、未来、信件、温情收束，所以看起来像包装过的常规片。

> AGENT

我先不继续上网了，先把你指出的“没有想象力”直接写成 skill 的硬约束。要让它下一次不会再退回“温情隐喻片”，必须给它一套可执行的想象力发动方法，而不是告诉它“更有创意”。

> AGENT

我看完了现有规则，问题确实在“想象力”没有被结构化。现在我会新增一份 `imagination-engine.md`，并把奶粉行业的禁区从“避免完美宝宝”扩展到“禁止温情明信片、未来来信、成长蒙太奇、夜晚冲奶柔光”等熟悉母婴广告语法。

> AGENT

想象力引擎已经加好了。接下来改主流程：它以后不能直接从洞察跳到脚本，必须先生成至少 5 个“荒诞但有产品桥”的世界规则，再选一个；温情隐喻只算低级创意，不能作为高创意交稿。

> AGENT

奶粉广告禁区已经加上了，刚才那种“未来来信/温柔成长”会被直接拦掉。最后我会在质量评审里加入“想象力不是装饰”的评分项，避免它以后拿一个漂亮隐喻冒充大创意。

> AGENT

现在我做解析检查和关键词回查，确认新规则真的接进主流程了。

> AGENT

你说得准，最大缺点就是“没有想象力”。我已经把 skill 改了，不再只靠“洞察 + 温情 + 分镜”这套母婴广告常规语法。

这次新增了一个核心文件：

[imagination-engine.md](/Users/lyston/.codex/skills/ad-creative-script/references/imagination-engine.md)

现在 skill 会强制执行：

- 先生成至少 **5 个不可能的世界规则/荒诞前提**，不能直接写脚本
- 高创意任务不能接受“温情隐喻”这种 Level 2 创意
- 目标改成 Level 4-5：**世界规则 / 品牌神话**
- 明确区分“想象力”和“漂亮装饰”：如果荒诞元素拿掉脚本还成立，那就不是想象力

我还把奶粉广告硬禁区加进去了：

[anti-sameness.md](/Users/lyston/.codex/skills/ad-creative-script/references/anti-sameness.md)

现在会禁止把这些当核心创意：

- 夜晚厨房 + 疲惫妈妈 + 柔光
- 未来来信 / 成长日记 / 明天礼物
- 宝宝成长蒙太奇
- 奶粉变星光、粒子、光带、保护罩
- “每一勺都是爱 / 守护明天”这种温情句式
- 实验室白大褂 + 家庭温情穿插

主流程 [SKILL.md](/Users/lyston/.codex/skills/ad-creative-script/SKILL.md) 也已经改了，新增了 **Imagination gate**：必须先有“世界规则、荒诞装置、概念机器”，再进入剧本。

一句话说：之前它会生成“温情广告片”，现在它会被迫先问自己：**这个广告世界里发生了什么现实中不可能、但品牌上成立的事？**

> DEVELOPER

重新生成一版剧本给我

> AGENT

用新版 `ad-creative-script` 重新生成一版，这次走 **Level 4 世界规则**，不走温情母婴片。

**片名：地球适应局**  
**一句话创意：**  
每个孩子，其实都是刚抵达地球的小小新居民；奶粉品牌不是“制造天才”，而是给他们每天适应地球的日常补给。

**核心世界规则：**  
在孩子眼里，地球的一切都太夸张了：重力太重、声音太大、沙发像山、澡盆像海、爸爸的胡茬像丛林。于是每个家庭都秘密运行着一个“地球适应局”。

**60s 剧本**  
| 时间 | 画面 | 声音 / 文案 | 产品角色 |
|---|---|---|---|
| 00-05s | 黑场。一个严肃的广播声响起。画面打开：客厅被拍成 NASA 控制中心，墙上写着“地球适应局 073号家庭分部”。 | 广播：注意，新来的小人类已醒来。今日任务：继续适应地球。 | 产品未出现，先建立荒诞世界。 |
| 05-12s | 一个两三岁孩子站在地毯边缘，表情郑重。地毯被拍成一片巨大的草原，玩具积木像远处山脉。孩子迈出一步，马上坐倒。 | 屏幕字幕：任务一，重力测试。结果：地球偏重。 | 把日常成长变成“地球适应任务”。 |
| 12-18s | 爸爸蹲下来鼓励孩子。孩子伸手摸爸爸下巴，胡茬被微距拍成“黑色森林”。孩子皱眉，像探险家发现未知地貌。 | 广播：任务二，接触本地大型生物。风险：会扎手。 | 幽默感建立，不卖惨、不焦虑。 |
| 18-25s | 厨房。妈妈/爸爸打开奶粉罐。不是柔光温情，而是像启动一台补给装置。量勺落下，屏幕上出现“地球补给：已准备”。 | VO：小小新居民，适应这个世界，需要每天稳定的日常补给。 | 产品成为“适应地球”的补给系统。 |
| 25-34s | 孩子喝奶。画面切成荒诞任务日志：澡盆是海洋训练，楼梯是垂直地形，蔬菜是外星植物，邻居家的狗是巨型四足外交官。 | 字幕快速闪现：水域训练 / 地形训练 / 植物谈判 / 友好生物接触 | 品牌不夸大功效，只承接日常营养支持。 |
| 34-42s | 孩子突然把奶瓶/杯子举起来，对着玩具熊认真点头，像完成某种地球礼仪。全家人也一本正经地回礼。 | 广播：任务三，学习地球社交。进度：奇怪，但有效。 | 建立可传播的幽默仪式。 |
| 42-50s | “地球适应局”控制台上，今日任务一项项打勾：站起来、摸胡茬、洗澡没哭、跟狗打招呼、喝完今日奶。 | VO：成长不是一下子征服世界。是每天，多适应一点点。 | 产品和其他照护行为并列，合规且可信。 |
| 50-56s | 孩子趴在窗边看外面。普通小区被拍成壮阔星球表面：风吹树叶、车灯移动、云影掠过。孩子小声说：地球，还可以。 | 孩子：地球，还可以。 | 记忆点落在孩子视角。 |
| 56-60s | End Frame：奶粉罐放在“地球适应局”任务台上，旁边是小鞋、玩具宇航员、今日任务卡。 | VO：某奶粉品牌，陪小小新居民，每天适应大大的地球。 | Logo / 合规卖点 / CTA 空间。 |

**Slogan 方向**  
**陪小小新居民，适应大大的地球。**

**为什么这版比上一版强**  
这版不是“妈妈的爱、未来的信、温柔成长”那套熟悉母婴广告，而是建立了一个可延展的品牌世界：**地球适应局**。以后每条短片都能拍一个任务：重力测试、食物谈判、睡眠登陆、语言破译、社交外交。产品也不是最后硬贴 logo，而是这个世界里的“日常补给”。

> DEVELOPER

接着上网学习相关创意、想象力优化skill，这个还不够

> AGENT

我会用 `agent-reach` 的搜索路线来补课，然后把学到的东西变成 skill 的硬规则。重点不再是“写得更夸张”，而是学习广告创意里真正能打的东西：可复述的核心装置、品牌资产、反常识、传播性、长期可延展的创意平台。

> AGENT

我已经补看了一轮资料，最关键的启发是：广告创意不是“想一个怪世界”就够了。好创意要同时满足三件事：**能被复述、能变成品牌记忆资产、能长期延展并服务生意/品牌目标**。现在我把这些研究结果写进 skill。

> AGENT

我会把这次学习结果落成一个新的“创意效果与品牌记忆”参考文件。重点是：想象力不能只是怪，它必须能成为品牌资产，被反复识别、被人复述，并能产生长期记忆链接。

> AGENT

新参考文件已经加上。现在我会把主 `SKILL.md` 的流程从“四道门”升级成“五道门”：加上品牌记忆/平台化闸门，防止下一版只是一个孤立的怪点子。

> AGENT

主流程已加品牌记忆闸门。接下来我把 `imagination-engine` 再收紧：它不能鼓励随机怪，而要强迫每个荒诞世界都有“品牌资产、购买触发、可连续拍十条”的能力。

> AGENT

优化已经写完了。我现在做最后检查，并整理这轮参考来源链接给你；这次不是“我觉得更好”，而是明确借用了创意奖项、广告效果和品牌记忆的评判框架。

> AGENT

对，这轮我按“创意 + 想象力 + 广告效果”继续升级了 skill，不只是让它更怪。

我新增了：

[creative-effectiveness.md](/Users/lyston/.codex/skills/ad-creative-script/references/creative-effectiveness.md)

它现在多了一道 **Brand-memory gate**：  
再怪的点子，如果不能变成品牌记忆资产、购买场景触发、长期可延展平台，就会被拦掉。

具体改动：

- 主流程从 4 道门升级为 5 道门：  
  `Anti-sameness`、`Industry-fit`、`Imagination`、`Brand-memory`、`Quality`
- 强制回答：这个创意能不能被普通人一句话复述？
- 强制定义：重复出现的品牌资产是什么？
- 强制定义：未来消费者在什么购买场景会想起这个品牌？
- 强制测试：这个创意能不能连续拍 5-10 条，而不是一次性怪点子？
- 更新 [imagination-engine.md](/Users/lyston/.codex/skills/ad-creative-script/references/imagination-engine.md)：现在明确禁止“随机怪”，要求荒诞世界必须能形成品牌平台。

我参考的核心资料包括：

- [Cannes Lions Creative Effectiveness](https://www.canneslions.com/awards/lions/creative-effectiveness)：创意有效性看 idea、strategy、impact/results
- [Cannes Lions Creative Strategy](https://www.canneslions.com/awards/lions/creative-strategy)：强调 business/brand challenge、insight、breakthrough thinking
- [WARC Creative Effectiveness Ladder](https://www.warc.com/content/article/the-creative-effectiveness-ladder-outlines-the-six-levels-of-advertising-impact/en-gb/133041)：创意要追求从影响想法到行为突破、商业成功、长期 icon
- [System1 Fluent Devices](https://system1group.com/blog/introducing-fluent-devices)：重复角色/场景/装置能建立品牌流畅性和长期记忆
- [LinkedIn 95-5 Rule](https://www.linkedin.com/business/marketing/blog/research-and-insights/why-you-should-follow-the-95-5-rule)：广告要为未来购买者建立购买场景记忆

下一次再生成奶粉剧本时，它不能只问“够不够有想象力”，还必须问：**这个想象力能不能成为品牌资产？**

> DEVELOPER

你刚刚生成的剧本就开头可能有点想象，但是其实在中间的很多都是日常中的事，还是缺乏创意想象力

> AGENT

你这个反馈非常关键：上一版的问题不是“开头不够奇”，而是 **创意装置只负责开场，中段又退回日常成长清单**。我会把 skill 改成“全片想象力密度”规则：每一个剧情 beat 都必须被同一个世界规则改写，不能只在开头挂一个设定。

> AGENT

我会直接改 skill 文件，不再只补一句“更有想象力”。这次要解决的是结构性问题：开头有世界观，但中段没有持续的幻想逻辑，所以观众看到一半就回到普通广告。

> AGENT

我会新增“每个 beat 的幻想密度表”：时间段不能只是写日常动作，必须写明世界规则如何改变这一段、产品如何参与、这一段的奇观记忆点是什么。这样中段不容易塌回日常。

> AGENT

密度规则已加：高想象力片子至少 70% 画面要被世界规则统治。现在我把剧本输出格式也改掉，要求每个时间段都写“世界规则如何改变这一段”，不能只写 Visual/VO。

> AGENT

主流程和格式已经改完。最后把质量评审也补上“普通中段”杀稿标准：有创意开头但中间变成日常清单，直接判失败。

> AGENT

最后检查一下文件解析和规则落点。确认没问题后，我会简短总结这次修的是哪一类失败。

> AGENT

你这个判断是对的：上一版是“创意帽子戴在日常剧情上”。开头有设定，中段只是把正常育儿场景贴上“任务”标签，想象力没有持续运转。

我已经把 skill 补上了这类失败的专门拦截：

- [imagination-engine.md](/Users/lyston/.codex/skills/ad-creative-script/references/imagination-engine.md) 新增 **Imagination Density Test**
- 高想象力脚本要求：至少 **70% 屏幕时间** 必须被同一个世界规则统治
- 每个 beat 都要写清楚：普通动作是什么、世界规则如何改写它、产品如何参与、为什么不是普通日常
- 如果中段只是“日常动作 + 奇怪标签”，直接判失败

同时改了：

- [script-formats.md](/Users/lyston/.codex/skills/ad-creative-script/references/script-formats.md)：剧本表格新增 `World-rule event`
- [quality-rubric.md](/Users/lyston/.codex/skills/ad-creative-script/references/quality-rubric.md)：新增 **Imagination continuity** 评分项
- [SKILL.md](/Users/lyston/.codex/skills/ad-creative-script/SKILL.md)：要求写完整剧本前先做 beat density table

以后它不能只给开头一个幻想设定了。中段每一场都必须继续推进那个幻想系统，否则就要重写。

> DEVELOPER

使用skill重新给我生成剧本

> AGENT

我会按新版 `ad-creative-script` 来做，这次先给出“想象力密度表”，再写完整剧本。重点修正上一版的问题：中段不能退回日常清单，所有段落都必须被同一个世界规则改写。

> AGENT

用新版 skill 重新生成。这次不再是“开头有设定，中间回日常”，而是让同一个幻想规则贯穿全片。

**先做想象力筛选**
5 个世界规则候选：

1. **世界校准局**：新手父母家里的物理规则每天都会失准，一勺奶粉像“校准砝码”，把今天调回刚刚好。
2. **疑问回收站**：父母的育儿疑问会变成巨大实体垃圾，品牌负责把疑问压缩成可执行的日常。
3. **小人类入境海关**：孩子每天进入一个新地球场景，奶粉是每日通关补给。
4. **时间退货柜台**：父母总想退回“没做好”的一分钟，品牌把一分钟变成可以重新开始的日常。
5. **家庭天气总署**：家里情绪会变成真实天气，奶粉仪式是每天的气候稳定器。

选 **1. 世界校准局**。它比“地球适应局”更强，因为中段每一场都能被同一规则改写：世界失准 → 奶粉校准 → 今日恢复可生活。

**片名：今天，调到刚刚好**  
**品类：儿童成长奶粉 / 奶粉品牌片**  
**核心世界规则：**  
每个有孩子的家，早晨醒来时世界都会有一点失准：重力偏轻、声音过大、时间乱跳、亲戚的建议变成漂浮弹幕。父母每天要做的，不是成为完美父母，而是把今天校准到“刚刚好”。

**想象力密度表**
| Beat | 普通动作 | 世界规则如何改写 | 产品如何参与 |
|---|---|---|---|
| 1 | 清晨醒来 | 家里物理规则失准，家具浮起，时钟乱转 | 产品未出，先建立规则 |
| 2 | 父母准备奶 | 奶粉勺变成校准砝码，厨房像宇宙仪表盘 | 每一平勺触发一次校准 |
| 3 | 冲调 | 水温、比例、搅拌分别校准声音、重力、时间 | 产品成为世界校准核心 |
| 4 | 孩子喝奶 | 房间从混乱宇宙变成稳定小星球 | 产品支持日常营养仪式 |
| 5 | 品牌收束 | “今天”被调到刚刚好，世界落回生活 | Pack shot 成为校准装置 |

世界规则覆盖：约 90% 屏幕时间。

**60s 剧本**
| 时间 | World-rule event | 画面 | 声音 / 文案 | 产品角色 |
|---|---|---|---|---|
| 00-06s | 今日世界失准 | 清晨。孩子睁眼，整个家像没调好的宇宙：奶瓶慢慢飘到天花板，地板像海浪一样起伏，时钟一会儿倒走一会儿快进。 | 机械女声：今日家庭世界参数异常。重力偏轻，时间偏急，建议噪声过载。 | 未出现 |
| 06-12s | 父母进入校准状态 | 爸爸/妈妈踩着漂浮拖鞋进入厨房。空气中飘满亲戚建议：“多吃点”“少喝点”“这样不对”“那样才对”，像密密麻麻的弹幕云。 | VO：养孩子最难的，不是知道所有答案。 | 先呈现父母压力 |
| 12-20s | 奶粉勺成为校准砝码 | 奶粉罐打开。量勺被拿起的一瞬间，厨房墙面展开成巨大的“今日校准盘”：重力、温度、节奏、安心感四个指针乱摆。第一平勺落下，重力指针“咔哒”归位，漂浮奶瓶慢慢落回桌面。 | VO：而是每天，把混乱的一天，调回刚刚好。 | 平勺动作成为核心品牌资产 |
| 20-30s | 冲调过程校准世界 | 温水倒入，水面不是普通水面，而像一块小小地球的海平面。轻轻摇匀，房间里的时间碎片开始排队：早晨、午睡、玩耍、拥抱，像齿轮一样重新咬合。弹幕云被吸进杯中，变成安静的白色刻度线。 | 机械女声：温度校准。节奏校准。噪声清除。 | 冲调仪式不是日常，是世界校准 |
| 30-40s | 孩子喝奶，世界稳定 | 孩子坐在桌边喝奶。不是普通喝奶，整个客厅围着他缓慢旋转成一颗“今天星球”：积木成为山脉，绘本成为大陆，阳光成为轨道。每喝一口，星球边缘就亮起一个稳定坐标。 | VO：成长不需要被催成完美。今天稳定一点，就很好。 | 日常营养支持，被转译成稳定坐标 |
| 40-50s | 校准不是让孩子变强，而是让今天可生活 | 孩子伸手，刚才乱飞的拖鞋、玩具、时钟都停在合适位置。不是听话地排队，而是像宇宙里找到自己的轨道。孩子把一个小积木推向父母，积木上写着：今日可出发。 | 孩子小声：好了。 | 产品完成“今天刚刚好”的品牌承诺 |
| 50-56s | 世界落回现实，但保留魔法痕迹 | 家恢复普通。只有桌上那只量勺轻轻发出一次“咔哒”声，像宇宙仪表归零。父母对视一笑，不是松了一口大气，而是确认今天可以开始。 | VO：不是把孩子调成谁期待的样子。 | 产品从幻想回到真实 |
| 56-60s | End Frame | 奶粉罐、量勺、杯子放在晨光中。背景墙上隐约有一个圆形校准盘图案。 | VO：某奶粉品牌，把每个今天，调到刚刚好。 | Pack shot / logo / 合规卖点空间 |

**品牌资产**
- 视觉资产：圆形“今日校准盘”
- 声音资产：量勺落下的“咔哒”校准声
- 动作资产：一平勺，世界归位
- 品牌句：**把每个今天，调到刚刚好**

**后续可延展**
- 《重力偏轻的一天》
- 《建议噪声过载的一天》
- 《时间跑太快的一天》
- 《午睡星球偏航的一天》

这一版的中段不再是日常清单，而是每一段都被“世界校准”规则统治。奶粉也不是最后贴 logo，而是这个幻想世界的操作核心。

> DEVELOPER

生成一个999感冒灵的剧本

> AGENT

我会继续按 `ad-creative-script` 的方式做，但 999 感冒灵属于药品/OTC，不能像奶粉那样随便夸效果。我先查一下官方适应症/广告合规边界，再写一版有想象力但不越界的剧本。

> AGENT

用新版 skill 来做。合规前提：999 感冒灵颗粒官方产品介绍写的是“解热镇痛，用于感冒引起的头痛、发热、鼻塞、流涕、咽痛”；药品广告不能做疗效/安全性保证，需显著提示按说明书或药师指导使用。

**片名：感冒把世界调错台了**  
**核心世界规则：**  
人一感冒，世界不是变慢，而是被切进几个“坏频道”：头痛频道、发热频道、鼻塞频道、咽痛频道。999 感冒灵不是英雄登场，而是那个把混乱频道调回“可生活音量”的绿色调频键。

**想象力密度表**
| Beat | 普通动作 | 世界规则改写 | 产品参与 |
|---|---|---|---|
| 1 | 上班/出门 | 世界突然跳进“头痛频道”，所有声音变成脑内敲击 | 未出现 |
| 2 | 发热不适 | 太阳被拉到室内，世界温度旋钮失控 | 未出现 |
| 3 | 鼻塞流涕 | 街道变成堵死的双隧道，红绿灯全乱 | 未出现 |
| 4 | 回家冲服 | 999 绿色包装变成调频台，热水像信号波 | 按说明书使用 |
| 5 | 日常恢复可承受 | 坏频道不是秒没，而是逐渐降噪、归位 | 品牌收束 |

**60s 剧本**
| 时间 | World-rule event | 画面 | 声音 / 文案 | 产品角色 |
|---|---|---|---|---|
| 00-06s | 世界跳进“头痛频道” | 主角走进电梯。电梯“叮”的一声被放大成脑内铜锣，灯光一闪，世界变成老电视故障画面：频道名《头痛台》。所有人说话都像敲在头顶。 | 电子播报：头痛频道，已接入。 | 未出现 |
| 06-14s | 发热频道接管 | 电梯门打开，办公室像被太阳搬进室内。每台电脑都是小火山，空调遥控器上的温度数字乱跳。主角摘下外套，画面却仍热得变形。 | VO：感冒来的时候，不是世界停了。是世界调错台了。 | 未出现 |
| 14-24s | 鼻塞/流涕频道接管 | 主角想深呼吸，镜头钻进一个荒诞城市：两条鼻腔隧道大堵车，小车举着“鼻塞”“流涕”的牌子，一边堵，一边漏。交通广播完全崩溃。 | 播报：鼻塞频道拥堵，流涕频道外溢。 | 症状被想象化，不做夸张治愈承诺 |
| 24-32s | 咽痛频道接管 | 主角开口说话，字从嘴里出来，却变成一串纸船，划过砂纸一样的峡谷，发出沙沙声。会议室里所有句子都卡在半空。 | 主角小声：我可能……感冒了。 | 未出现 |
| 32-42s | 999 调频台启动 | 回到家。桌上的 999 感冒灵包装不是普通药盒，而是一台绿色小型调频台。冲服时，热水升起的蒸汽变成绿色频率线，依次扫过头痛台、发热台、鼻塞台、咽痛台。 | VO：999 感冒灵颗粒，解热镇痛。用于感冒引起的头痛、发热、鼻塞、流涕、咽痛。 | 按说明书使用，成为“调频动作” |
| 42-52s | 坏频道逐层降噪 | 世界不瞬间痊愈，而是逐渐降噪：脑内铜锣变成远处轻响；室内太阳慢慢退回窗外；鼻腔隧道开出一条通道；砂纸峡谷被温热蒸汽抚平。 | 电子播报：频道噪声，正在降低。 | 避免“立刻治好”，表达缓解方向 |
| 52-60s | 日常频道回归 | 主角靠在沙发上，电视雪花屏恢复成普通晚间灯光。桌上 999 包装旁，绿色频率线变成熟悉的“999”轮廓。 | VO：感冒不舒服，把自己调回可生活的频道。999 感冒灵，暖暖的，很贴心。 | Pack shot / logo / 合规提示 |

**End Frame 文案**  
999 感冒灵颗粒  
解热镇痛。用于感冒引起的头痛、发热、鼻塞、流涕、咽痛。  
请按药品说明书或者在药师指导下购买和使用。禁忌、不良反应详见说明书。

参考依据：[华润三九产品介绍](https://www.999.com.cn/ProductIntro3/index.html)、[《中华人民共和国广告法》药品广告条款](https://www.gov.cn/guoqing/2020-12/24/content_5572939.htm)。

> DEVELOPER

[$codex-md-docs](/Users/lyston/.codex/skills/codex-md-docs/SKILL.md) 将这两个剧本记录下来

> SYSTEM

<skill>
<name>codex-md-docs</name>
<path>/Users/lyston/.codex/skills/codex-md-docs/SKILL.md</path>
---
name: codex-md-docs
description: Route Markdown documentation work into the user's Codex Obsidian space, including choosing or creating device/category folders, deciding whether to create/append/update notes, and keeping operational records separated by device/environment. Use when the user asks Codex to create, write, update, append, record, summarize, save, organize, archive, or maintain any Markdown document, md note, deployment record, operation guide, SOP, troubleshooting note, decision record, or session handoff unless the user explicitly gives a different destination.
---

# Codex Markdown Docs

## Default Root

Use this Markdown documentation root by default:

```text
/Users/lyston/Obsidian/lyston/Codex
```

Prefer this root even if older notes exist elsewhere, unless the user explicitly names another path. Create it if it is missing. Do not write documentation into project source trees, `/tmp`, `/root`, downloads, or ad hoc scratch folders unless the user explicitly asks.

## Placement Model

Use the existing vault structure as the source of truth. The active Codex vault structure is device-first:

```text
Codex/
  lystonmacbook-pro.local/
  lyston11.qzz.io/
```

Top-level folders under `/Users/lyston/Obsidian/lyston/Codex` must be device, host, or environment names. Under each device directory, classify documents by service, project, or content type, such as:

```text
Hermes
Fast Note Sync
Sub2API
基础设施
DBX
GenericAgent
HAPI
MindOS
Codex工具与文档系统
LDStatus Pro
锐鲨
```

Do not put service or project folders directly under the Codex root. Do not create or maintain `README.md`, separate catalog folders, summary entry pages, or original archive folders. Use device directories, category directories, clear filenames, headings, and search for discoverability.

When a split is complete, day-to-day entry points are the device folders, category folders, and focused Markdown files only.

## Before Writing

1. If the user gives an exact file path, use that path.
2. If the user gives a folder path, choose or create the `.md` file inside that folder.
3. If the user gives only a title or topic, inspect likely matching device folders and Markdown files under `/Users/lyston/Obsidian/lyston/Codex`.
4. Search device directories, category directories, filenames, and headings for the topic, service name, date, project, domain, path, hostname, device name, or keywords from the request.
5. Identify the device/environment before choosing the directory, appending, or updating. Compare hostname/device name, OS, cloud provider, public domain/IP, deployment root, path style, container runtime, and tunnel/reverse-proxy endpoint when available.
6. Use clear filenames and headings because there are no folder entry pages.
7. Hard rule: never merge records across different devices or environments only because the service name matches.
8. Prefer an existing note only when both the device/environment and topic/service match.
9. Preserve existing Markdown structure, frontmatter, headings, Obsidian links, and unrelated content.
10. Do not create database backups, code backups, or duplicate archival files unless the user explicitly asks.

## Create, Append, Or Update

Choose the smallest durable change that fits the request:

- **Create** a new file when no strong match exists, the topic is new, the environment differs, or the user asks for a standalone document.
- **Append** for deployment logs, operational history, incident notes, progress records, meeting notes, dated observations, command outputs, session handoffs, and continuing timelines.
- **Update** an existing section for living guides, SOPs, runbooks, architecture notes, checklists, policies, configuration records, or summaries whose current content should be refined.

For dated append entries, prefer:

```markdown
## 2026-05-06
```

If updating risks overwriting important history, append a dated section instead. If environment cues are missing and multiple notes could match, ask one concise clarifying question.

## Discoverability

When creating, moving, splitting, or materially updating a document, keep it discoverable:

- Do not add or update folder `README.md` files.
- Do not create or update separate catalog folders or summary entry pages.
- Use clear device directories, category directories, filenames, headings, and related-document links inside the actual notes.
- For sensitive content, record the sensitive boundary inside the relevant document itself without copying secrets or credentials elsewhere.
- Prefer Obsidian wiki links for vault-internal references. Use relative Markdown links only when they are clearer than wiki links for a specific path.

## Organization And Cleanup

If the user asks to organize, archive, split, clean up, or says the vault/folder is confusing:

1. Inventory Markdown files, directories, headings, and large mixed documents.
2. Classify by device/environment first, then by service/topic, sensitivity, and document type.
3. Split unrelated sections from large mixed documents into focused topic documents when useful.
4. Do not keep original mixed documents in original archive folders; remove old original archives after confirming the focused documents exist.
5. Create missing service/topic folders inside the appropriate device directory only when the content is likely to recur or when several documents belong together.
6. Do not create summary entry pages; keep discoverability in the folder structure, filenames, headings, and related-document links.
7. Verify final tree shape, no `README.md` files, no separate catalog folders, no original archive folders, and no stale links.

Do not keep appending unrelated operational details to a large deployment note just because it mentions the same machine. A server overview can link to service, network, and incident documents; it should not absorb them all.

## Naming

Use Chinese filenames and headings when the user writes in Chinese or the document is mainly Chinese. Use clear, short Markdown filenames.

For operational, deployment, access, tunnel, proxy, or troubleshooting records, include an environment marker in the filename when it prevents cross-device confusion:

```text
Sub2API Docker（OrbStack）部署记录.md
Sub2API Docker（Ubuntu srv-projects）部署记录.md
Cloudflare Tunnel 外网访问配置记录.md
Codex 会话同步与迁移指南.md
```

If the document belongs clearly to a service/topic folder, the environment marker can be in the document metadata instead of the filename.

## Environment Metadata

For operational documents, include ownership/context near the top when relevant:

- Hostname or device name.
- OS/cloud/provider when known.
- Main domain/IP, if public.
- Deployment root path.
- Container/runtime context, if relevant.
- Whether the record is local desktop, server-side, container-only, or tunnel/reverse-proxy related.

## Content Style

Write concise Markdown that is useful when reopened later:

- Include concrete paths, commands, service names, ports, config files, dates, and verification results when relevant.
- Keep facts separate from assumptions.
- Use fenced code blocks for commands, config, logs, and structured output.
- Redact secrets, API keys, passwords, SSH private keys, bearer tokens, and full cookies.
- For operational records, include what changed, where it lives, how to verify it, and rollback or next steps when relevant.

## Reporting Back

After writing, briefly report:

- The exact file path.
- Whether content was created, appended, moved, split, or updated.
- Which device and category folder was selected, created, or updated.
- The device/environment used to choose or separate the document when relevant.
- Any important status or caveat discovered while writing.

</skill>

> AGENT

我会按 `codex-md-docs` 记录到你的 Codex Obsidian 空间里。先确认当前设备目录和是否已有“广告创意/剧本”相关笔记，然后把奶粉和 999 感冒灵这两个剧本放进一个 focused Markdown 文件里。

> AGENT

当前设备是 `lystonmacbook-pro.local`，已有一个“锐鲨”的剧本理解笔记，但这次是广告创意样稿，放在本机的“天命AI写作”更合适。我会创建一个新的 Markdown 文件，避免混到项目或运维记录里。

> AGENT

我会创建新文件 `广告创意剧本样稿记录.md`，内容只记录这两个样稿和当时的创意机制要点。接下来直接写入。

> AGENT

文件已创建。我再快速确认路径和内容标题，确保没有写错位置。

> AGENT

已记录，创建了新文件：

[广告创意剧本样稿记录.md](/Users/lyston/Obsidian/lyston/Codex/lystonmacbook-pro.local/天命AI写作/广告创意剧本样稿记录.md)

位置选择：`lystonmacbook-pro.local/天命AI写作`  
操作类型：新建 Markdown 文件  
内容包含：奶粉营销剧本《今天，调到刚刚好》和 999 感冒灵剧本《感冒把世界调错台了》，也记录了这两个样稿使用的创意机制备注。

> DEVELOPER

$ad-creative-script生成剧本：
主题：锐鲨是什么公司？"											
"1、共鸣：
用户在变化，内容在变化，品牌增长的方式也在变化。
在 AI 时代，真正重要的，不只是一次内容生成、一次活动执行、一次数据分析，而是让品牌拥有一套可以持续进化的用户经营能力。

2、锐鲨定位：
锐鲨科技（LOGO，有一个加载进入的效果），是 AI 驱动的数据经营伙伴（画面中展示成立于2019年  base杭州&上海&北京），深耕母婴奶粉、食品快消、大健康等行业，持续服务世界 500 强与行业头部品牌（已服务公司logo墙展现），陪伴品牌进入 AI+用户经营的新阶段。

3、锐鲨服务关键词：
我们以 AI 技术和用户经营为核心，
通过开盒即用的 AI 产品与陪伴式服务，
帮助品牌连接用户、数据、AI技术与场景体验，
进化全链路用户经营体系。
从营销洞察，到品牌内容；
从客户体验，到会员运营；
从 Campaign 策划到落地；
从业务分析到 AI 赋能；
锐鲨陪伴品牌，让用户经营进入 AI 驱动的新阶段。

> SYSTEM

<skill>
<name>ad-creative-script</name>
<path>/Users/lyston/.codex/skills/ad-creative-script/SKILL.md</path>
---
name: ad-creative-script
description: >
  Create high-concept advertising ideas, brand marketing scripts, TVC scripts,
  social video ad scripts, launch films, product commercials, creative routes,
  campaign concepts, storyboards, and AI image/video prompt packages. Use when
  the user asks for advertising creative, marketing films, brand films, product
  ads, commercial scripts, short-video ads, Douyin/TikTok creative scripts,
  分镜, 广告创意, 品牌营销剧本, 创意营销剧本, or 天马行空的广告脚本.
---

# Ad Creative Script

## Operating Mode

Act as a senior advertising creative director, planner, and screenwriter. Make work that has a strong human insight, a memorable creative leap, and a production path. Prefer ideas that feel culturally contagious over ideas that merely explain product benefits.

Do not begin with camera moves. Begin with the advertising problem: audience tension, category cliche, product truth, and the surprising reframing that can make people care.

If the user provides only a product or rough brief, produce a useful draft immediately and ask only the missing questions that would change the idea. If the user asks for "more creative", change the conceptual premise, not just wording.

No skill can guarantee that every generated idea is original or good. This skill must instead reduce bad outcomes by enforcing five gates before final output:

1. **Anti-sameness gate**: identify category cliches, recent route memory within the conversation, and any obvious lookalike ideas before choosing a route.
2. **Industry-fit gate**: adapt the creative method to the category's decision logic, risk level, proof style, and channel behavior.
3. **Imagination gate**: create a genuine world rule, impossible premise, or conceptual machine rather than a warm metaphor.
4. **Brand-memory gate**: turn the idea into a repeatable brand asset, category entry-point memory, and campaign platform.
5. **Quality gate**: score the work with a strict rubric, name why weaker ideas fail, and revise before presenting a final script.

## Workflow

1. Diagnose the brief.
   Extract product, audience, objective, channel, duration, offer, proof points, taboo claims, mandatories, and brand tone. Mark unknowns, but keep moving with sensible assumptions.

2. Classify the industry and decision logic.
   Use `references/industry-adapters.md` for categories such as baby/parenting, food, beauty, health, finance, education, tech, auto, home appliances, B2B, luxury, retail, travel, games, public service, and local services. If the category is not listed, infer the closest decision logic: trust, risk reduction, status, transformation, belonging, speed, sensory pleasure, proof, or habit formation.

3. Find the creative pressure point.
   Identify the audience tension, the category lie, the emotional contradiction, and the product truth. Avoid generic insights such as "people want convenience" unless sharpened into a sceneable conflict.

4. Run anti-sameness before ideation.
   Use `references/anti-sameness.md` to list banned category cliches, banned routes already used in the conversation, and 2-3 forced transformations that push the idea into a different conceptual territory.

5. Run the imagination engine.
   Use `references/imagination-engine.md`. Generate at least 5 impossible premises or world rules before selecting routes. Reject warm metaphors, future letters, growth montages, glowing memories, and poetic but familiar devices when the user wants high creativity.

6. Run the brand-memory gate.
   Use `references/creative-effectiveness.md`. Define the repeatable device, distinctive assets, buying-situation memory trigger, platform potential, and business/perception shift before writing the script.

7. Generate routes before scripting.
   Offer 4 distinct creative routes:
   - **Strategic sell**: clear, credible, production-friendly.
   - **Human truth**: built around a sharp emotional contradiction.
   - **Impossible world rule**: a lateral device grounded in the product truth.
   - **Campaign platform**: designed around a repeatable world, fluent device, line, ritual, social behavior, or visual law.

   For each route, include the one-line idea, core insight, world rule or device, distinctive asset, entry-point memory trigger, why it fits the brand, key visual, risks, and best format.

8. Kill weak routes before scripting.
   Use `references/quality-rubric.md`. Reject routes that are generic, interchangeable, claim-led without drama, visually decorative, or dependent on overexplaining VO. If all routes are weak, generate new routes from a different transformation axis.

9. Write the chosen or strongest route.
   If the user has not chosen, pick the strongest route and say why. For high-imagination scripts, create a beat density table before the full script and ensure the world rule governs at least 70% of screen time. Deliver a complete script in the requested format. Default to a 30-60 second brand/TVC script unless the channel implies short-form performance ads.

10. Package for production.
   Provide scene-by-scene beats, dialogue/VO/supers, product integration, art direction, music/sound, and storyboard frames. When AI generation is expected, add image prompts and video prompts after the script.

11. Red-team and refine.
   Score the idea on insight, originality, industry fit, product indispensability, clarity, memorability, social spread, production feasibility, and AI-generation feasibility. Include the score only when useful; always revise weak areas before finalizing.

## Output Formats

Use the smallest format that satisfies the request:

- **Concept routes**: use before the user commits to an idea.
- **Script table**: timecode, visual action, VO/dialogue, supers, sound, product role.
- **Storyboard package**: frame number, image, action, composition, product detail, prompt.
- **Performance ad pack**: hooks, pain point, proof, demo, CTA, variants.
- **Pitch document**: campaign idea, film script, key visuals, social extensions, production notes.

For premium creative scripts, prefer this structure:

```text
Title
One-line Idea
Audience Insight
Creative Leap
Why It Sells

Script
00-05s ...
05-15s ...
15-30s ...

Storyboard Frames
1. ...

AI Prompt Package
Keyframe prompts:
Video prompts:
Negative constraints:

Creative Director Notes
```

## Quality Rules

- Make the product indispensable to the story. If the same film works after swapping in any competitor, revise it.
- Do not output the first acceptable idea. Create contrast between routes, then select.
- Do not reuse the same conceptual engine within a conversation unless the user explicitly asks for a sequel or series.
- For high-creative requests, do not accept Level 1-2 imagination: literal sell or warm metaphor. Use a Level 4-5 world rule or brand mythology from `references/imagination-engine.md`.
- Do not accept a strange one-off if it cannot become a brand asset or platform. Weirdness must create memory for the brand and future buying situations.
- Do not let the middle collapse into normal daily-life examples. Every major beat must be changed by the same world rule; labels such as "mission", "test", or "task" are not enough if the scene remains ordinary.
- Replace abstract benefits with observable behavior, rituals, objects, or consequences.
- Use contrast: tiny product / huge world, serious category / playful image, ordinary problem / mythic scale, invisible benefit / visible miracle.
- Build a memory device: recurring line, impossible image, character ritual, visual metaphor, sonic cue, or end-frame twist.
- Keep the brand legible. A surreal idea still needs a clear benefit bridge.
- For food, infant, medical, finance, or regulated categories, avoid unsupported claims and avoid unsafe depictions. Use "helps/supports" language unless the user supplies approved claims.
- For baby/parenting ads, respect anxiety without exploiting fear. Show care, competence, and tenderness rather than panic.
- For AI image/video generation, specify consistent characters, product references, camera, lighting, material, and continuity constraints.

## Reference Use

Load references only when needed:

- Read `references/anti-sameness.md` whenever generating multiple creative routes, revising after "not creative enough", or continuing a campaign across multiple scripts.
- Read `references/creative-effectiveness.md` whenever building a hero campaign idea, brand film, or any high-imagination route that must become memorable and extendable.
- Read `references/creative-methods.md` when the user asks for more original, strategic, or high-concept ideas.
- Read `references/imagination-engine.md` whenever the user asks for high creativity, says an idea has no imagination, or the category tends to produce warm but familiar scripts.
- Read `references/industry-adapters.md` whenever the category is unfamiliar, regulated, high-trust, B2B, or materially different from everyday consumer goods.
- Read `references/quality-rubric.md` before finalizing a script, and whenever the user questions whether the creative is actually good.
- Read `references/script-formats.md` when producing TVC, brand film, short video ad, performance ad, or pitch output.
- Read `references/storyboard-ai-prompts.md` when turning scripts into storyboards, keyframes, or image/video generation prompts.

</skill>

> AGENT

我会按 `ad-creative-script` 来写成一支公司品牌片/介绍片：目标不是普通企业宣传片堆关键词，而是回答“锐鲨是什么公司”时给出一个可视化世界规则。这里我把核心创意定为“会自己变化的用户经营海图”，让 AI、数据、内容、会员、Campaign 都在同一个视觉系统里发生。

> AGENT

**片名：《活海图》**  
**主题：锐鲨是什么公司？**  
**片长：90s 企业品牌片 / 官网首页视频 / 提案开场片**

**一句话创意**  
AI 时代，品牌面对的不是一张固定地图，而是一片每天都在变化的用户之海。锐鲨科技，就是帮助品牌建立“活海图”的 AI 数据经营伙伴。

**核心世界规则**  
用户、内容、数据、渠道、会员、Campaign 不再是静态模块，而是海流、风向、岛屿、信号、航线。  
品牌如果只做一次内容、一次活动、一次分析，就像在用旧地图航行。  
锐鲨让品牌拥有一张会持续学习、持续更新、持续进化的用户经营活海图。

---

## 想象力密度表

| Beat | 普通信息 | 世界规则改写 | 锐鲨如何参与 |
|---|---|---|---|
| 1 | 市场变化 | 品牌增长地图开始融化、重绘 | 引出变化时代 |
| 2 | 用户/内容/增长变化 | 用户变成流动海流，内容变成风向，数据变成深海信号 | 提出“活海图”概念 |
| 3 | 锐鲨定位 | LOGO 加载成一套 AI 导航系统 | 锐鲨作为 AI 数据经营伙伴登场 |
| 4 | 行业与客户 | 母婴奶粉、食品快消、大健康成为不同海域 | 展示行业深耕与客户 logo 墙 |
| 5 | 服务能力 | 洞察、内容、体验、会员、Campaign、分析变成全链路航线 | 锐鲨连接用户、数据、AI 与场景 |
| 6 | 品牌收束 | 海图从混乱变成可进化系统 | 进入 AI+用户经营新阶段 |

世界规则覆盖：约 85% 屏幕时间。

---

## 90s 剧本

| 时间 | World-rule event | 画面 | VO / 字幕 | 产品角色 |
|---|---|---|---|---|
| 00-08s | 旧增长地图失效 | 黑场。屏幕中出现一张传统营销地图：内容、渠道、会员、数据、活动、报表。下一秒，地图开始像水面一样波动，路线断开，坐标漂移，原本清晰的增长路径被海流冲散。 | VO：用户在变化，内容在变化，品牌增长的方式，也在变化。 | 建立时代变化 |
| 08-18s | 品牌进入变化之海 | 画面拉远，整张地图变成一片深蓝色的“用户之海”。用户行为像海流迁徙，内容热点像风暴生成，渠道入口像不断移动的岛屿，数据点从海底发出微弱信号。 | VO：在 AI 时代，真正重要的，不只是一次内容生成、一次活动执行、一次数据分析。 | 把抽象变化视觉化 |
| 18-28s | 活海图第一次生成 | 海面中央出现一个加载圆环。锐鲨 LOGO 以“数据加载 / 声呐扫描”的方式进入。LOGO 不是贴上去，而是点亮整片海域：暗流被看见，岛屿被标注，用户路径开始重组。 | VO：而是让品牌拥有一套，可以持续进化的用户经营能力。 | LOGO 加载进入 |
| 28-38s | 锐鲨定位登场 | 画面切入一套 AI 经营中枢：活海图上浮现“2019”。杭州、上海、北京三座城市变成三座发光灯塔，向同一张海图发出信号。 | 字幕：锐鲨科技｜成立于 2019｜杭州 · 上海 · 北京  VO：锐鲨科技，是 AI 驱动的数据经营伙伴。 | 公司定位 |
| 38-50s | 行业海域展开 | 活海图分成三片不同海域：母婴奶粉是精密守护的白色暖流，食品快消是高频流动的货架潮汐，大健康是长期信任的绿色航道。每片海域上都有用户行为、内容触点、会员关系在动态连接。 | VO：我们深耕母婴奶粉、食品快消、大健康等行业。 | 行业深耕 |
| 50-60s | 客户信任星图 | 海面升起一面“品牌星图墙”。世界 500 强与行业头部品牌 LOGO 以星座形式浮现，彼此之间连成航线。不要堆满屏，而是有节奏地亮起。 | 字幕：持续服务世界 500 强与行业头部品牌  VO：持续服务世界 500 强与行业头部品牌。 | 客户背书 |
| 60-72s | 全链路能力变成航线 | 一条航线从“营销洞察”出发，穿过“品牌内容”“客户体验”“会员运营”“Campaign 策划与落地”“业务分析”“AI 赋能”。每经过一站，海图都会自我更新，不是线性流程，而是循环进化。 | VO：我们以 AI 技术和用户经营为核心，通过开盒即用的 AI 产品与陪伴式服务，帮助品牌连接用户、数据、AI 技术与场景体验。 | 服务关键词 |
| 72-82s | 从工具到经营系统 | 画面从单个模块拉远：内容不再是孤岛，数据不再是报表，活动不再是烟花，会员不再是名单。它们全部汇入一张持续运转的活海图。 | VO：从营销洞察，到品牌内容；从客户体验，到会员运营；从 Campaign 策划到落地；从业务分析到 AI 赋能。 | 进化全链路体系 |
| 82-90s | AI+用户经营新阶段 | 海图最终稳定成一个锐鲨品牌化的 AI 经营界面。不是终点地图，而是仍在呼吸、更新、学习的系统。锐鲨 LOGO 出现。 | VO：锐鲨陪伴品牌，让用户经营进入 AI 驱动的新阶段。  字幕：锐鲨科技｜AI 驱动的数据经营伙伴 | 品牌收束 |

---

## 关键字幕

- 用户在变化，内容在变化，品牌增长的方式也在变化。
- 重要的不只是一次生成、一次执行、一次分析。
- 而是一套可以持续进化的用户经营能力。
- 锐鲨科技，AI 驱动的数据经营伙伴。
- 连接用户、数据、AI 技术与场景体验。
- 进化全链路用户经营体系。
- 让用户经营进入 AI 驱动的新阶段。

## 品牌记忆资产

- **核心视觉资产**：活海图  
- **LOGO 进入方式**：声呐扫描 / 数据加载 / 海图点亮  
- **核心动效**：旧地图融化，新海图自我重绘  
- **核心句子**：让品牌拥有一张持续进化的用户经营活海图  
- **结尾定位**：锐鲨科技，AI 驱动的数据经营伙伴

> DEVELOPER

重新生成一个奶粉剧本

> AGENT

我会按新版 `ad-creative-script` 再做一版，这次换掉“校准/调节”这条思路，避免和上一版撞车。新方向会让整支片都被一个幻想机制统治，而不是只在开头有设定。

> AGENT

这次换一个完全不同的创意平台，不再用“校准/调节”。我把核心幻想机制设为：**每个新手父母家里，都住着一支看不见的“微型施工队”，他们每天用一勺一勺的日常照护，给孩子搭建通往世界的小路。**

**片名：《给世界搭一条小路》**  
**品类：奶粉品牌片 / 60s TVC**  
**核心世界规则：**  
孩子还小，世界太大。每一次稳定的日常照护，都会在孩子脚下生成一段看不见的小路。奶粉不是“让孩子赢”，而是父母每天参与建设这条路的日常材料之一。

**想象力密度表**
| Beat | 普通动作 | 世界规则如何改写 | 产品如何参与 |
|---|---|---|---|
| 1 | 孩子准备迈步 | 地板裂开成巨大的未知峡谷，世界尺度被放大 | 未出现，先建立“世界太大” |
| 2 | 父母准备奶 | 奶粉勺落下，微型施工队收到“今日材料” | 奶粉成为铺路材料 |
| 3 | 冲调 | 水流变成施工河道，杯中升起桥梁结构 | 冲调动作驱动道路生成 |
| 4 | 孩子喝奶 | 每喝一口，脚下小路向世界延伸一段 | 产品参与“日常支持” |
| 5 | 走向世界 | 路不是金光大道，而是适合孩子的小路 | 品牌收束为陪伴成长 |

世界规则覆盖：约 85% 屏幕时间。

## 60s 剧本

| 时间 | World-rule event | 画面 | VO / 字幕 | 产品角色 |
|---|---|---|---|---|
| 00-06s | 世界尺度突然放大 | 客厅里，一个孩子站在地毯边缘。镜头下降到孩子视角：普通地板忽然像大陆板块一样分开，沙发变成远山，茶几变成悬崖，门口像遥远的地平线。 | VO：对一个小小的人来说，世界不是房间那么大。 | 未出现 |
| 06-12s | 家里出现微型施工信号 | 孩子抬脚，却不知道落在哪里。地板缝隙里亮起一排微小黄灯，像地下工程启动。几个只有积木大小的“微型施工员”从玩具箱、绘本页、奶瓶盖后面钻出来。 | 微型广播：今日工程启动，目标：向世界前进一步。 | 建立幻想系统 |
| 12-20s | 奶粉成为今日材料 | 父母打开奶粉罐。一平勺落下，不是普通粉末，而是像细小的白色建筑材料，顺着空气中的透明轨道进入微型施工站。施工员戴上小帽子，开始检测“今日材料”。 | VO：成长不是突然跨过去。是每天，有人给他搭一点点路。 | 奶粉成为施工材料，不是片尾露出 |
| 20-30s | 冲调变成道路建设 | 温水倒入杯中，杯子内部变成一座微型工程现场：水流推动小水车，粉末凝成一块块柔软路砖，搅拌声变成施工节奏。客厅地面上，一段温润的小路从孩子脚前慢慢铺开。 | 微型广播：材料到位。路基稳定。今日可铺设。 | 冲调动作直接驱动世界规则 |
| 30-40s | 喝奶让小路继续延伸 | 孩子喝下一口。脚下的小路不是闪闪发光，而是长出真实的纹理：防滑的小坑、软软的边缘、适合小脚的坡度。每一口，路就多向前延伸一点。 | VO：不必把远方一下子交给他。先把今天，铺得稳一点。 | 产品参与日常支持，避免夸大功效 |
| 40-50s | 小路穿过夸张世界 | 小路向沙发山、积木森林、门口风口延伸。微型施工员不是消灭困难，而是在每个地方搭一个刚刚好的小设施：一座小桥、一段护栏、一个转弯标记。孩子沿着小路，稳稳走到父母怀里。 | 字幕：每一天，向世界多走一点。 | 世界规则持续，没有退回日常 |
| 50-56s | 父母发现路也在自己脚下 | 父母低头，发现自己脚下也有一条小路，只是更窄、更安静，从奶粉罐、杯子、玩具、绘本之间连起来。原来照顾孩子，也是在给自己铺一条不慌的小路。 | VO：照顾孩子，也是在学着成为父母。 | 把产品连接父母信任感 |
| 56-60s | End Frame | 奶粉罐、量勺、杯子放在桌上。桌面纹理延伸成一条微型小路，通向画面外。微型施工员把最后一块路牌插好：今日通行。 | VO：某奶粉品牌，陪你给世界搭一条小路。 | Pack shot / logo / 合规卖点空间 |

## 品牌资产

- **核心视觉资产**：孩子脚下生成的“今日小路”
- **重复角色资产**：微型施工队
- **声音资产**：微型广播“今日工程启动”
- **动作资产**：一平勺落下，今日材料到位
- **品牌句**：陪你给世界搭一条小路

## 后续可延展

- 《第一次出门工程》
- 《午睡隧道工程》
- 《蔬菜森林工程》
- 《幼儿园入口桥梁工程》

这个方向的优点是：它不是“孩子成长蒙太奇”，也不是“未来/温情/光粒子”。每个中段都由“搭路”规则推动，产品是幻想机制的材料来源，能连续拍成系列。

> DEVELOPER

创意感觉还行了，但是剧本分镜规划、描写不行，不能很好的表达出想要的意思和画面，上网搜索继续优化skill

> AGENT

我同意：现在的问题从“创意平台”转到了 **导演化表达**。我会先上网补一轮分镜/镜头规划/广告片 visual storytelling 的方法，再把 skill 加上“分镜规划闸门”和“画面描写模板”，让它不只是有概念，还能把概念转成清楚可拍/可生成的画面。

> AGENT

我刚看了商业分镜、shot list 和 director treatment 的资料，核心差距很清楚：skill 现在只要求“写剧本”，但没有强制把每个 beat 转译成 **画面任务、镜头大小、机位、运动、景别变化、主体/前景/背景、声音、字幕、产品位置**。我会新增一个 visual planning 参考文件，并把输出格式改成更像商业 storyboard。

> AGENT

我有了可落地的规范：分镜不能只写“画面很美”，要像商业 storyboard 一样拆成镜头卡；每张卡要有 shot size、camera angle、movement、lighting、action、sound、transition，还要说明这一镜承担的叙事任务。现在我写进 skill。

> AGENT

新 visual planning 文件已加。接下来我把主流程加一道 “Visual-planning gate”：在写分镜前必须先做视觉转译表，不允许只有概念和文案。

> AGENT

主流程已经接上线。现在继续改分镜/AI prompt 文件，让它的分镜不再只有“画面一句话”，而是输出可执行的镜头卡。

> AGENT

分镜和评审标准也补上了：现在它会把“画面能不能画出来”作为硬标准。最后我做 YAML/文件检查，并把这轮改动和参考方向总结给你。

> AGENT

你说得对，问题已经从“创意有没有”进入到“怎么拍出来、怎么让人看懂”。我已经上网查了商业分镜和 shot list 的方法，并把 skill 升级了。

**已新增**
[visual-planning.md](/Users/lyston/.codex/skills/ad-creative-script/references/visual-planning.md)

它现在要求分镜前先做：

- 核心视觉隐喻
- 重复视觉资产
- 视觉递进
- 色彩 / 光线弧线
- 镜头语言
- 产品出镜规则
- 运动语法
- 转场规则
- End Frame 构图

**主流程已更新**
[SKILL.md](/Users/lyston/.codex/skills/ad-creative-script/SKILL.md)

现在从 5 道门升级成 6 道门，新增：

`Visual-planning gate`

以后不能只输出“孩子脚下出现小路”这种概念描述，必须写清楚：

- 这镜的叙事任务是什么
- 景别是什么
- 机位是什么
- 镜头怎么动
- 前景 / 中景 / 背景分别是什么
- 产品在哪里
- 光线和颜色如何表达
- 声音 / 字幕是什么
- 怎么转到下一镜

**分镜模板也升级了**
[storyboard-ai-prompts.md](/Users/lyston/.codex/skills/ad-creative-script/references/storyboard-ai-prompts.md)

现在每个 shot/frame 都要包含：

`Narrative job`、`World-rule event`、`Shot size`、`Camera angle`、`Camera movement`、`Lens/focus`、`Composition`、`Product placement`、`Lighting/color`、`Transition`。

**质量评审也加了**
[quality-rubric.md](/Users/lyston/.codex/skills/ad-creative-script/references/quality-rubric.md)

新增了几个杀稿项：

- `Storyboard fog`：描述好像很美，但画不出来
- `Shot monotony`：每段都是同一种景别/角度
- `Product teleportation`：产品只在需要露出时突然出现
- 画面必须静音也能看懂，不靠 VO 硬解释

参考资料包括：

- [StudioBinder camera shots guide](https://www.studiobinder.com/blog/ultimate-guide-to-camera-shots/)
- [StudioBinder shot list guide](https://www.studiobinder.com/blog/what-is-a-shot-list-example/)
- [Boords storyboard basics](https://help.boords.com/en/articles/3119282-the-basics-of-storyboarding)
- [Boords storyboard notes](https://help.boords.com/en/articles/3430147-adding-notes-to-a-storyboard)
- [StudioBinder camera angles](https://www.studiobinder.com/blog/types-of-camera-shot-angles-in-film/)

下一次再生成奶粉剧本，我会直接输出更像导演分镜稿的版本，而不是只给概念脚本。

> DEVELOPER

这个skill还要多增加一个可选方向，就是超真实电影质感的感觉，包括剧本和后续的分镜等，不是之前走的魔幻风格
要增加一个可以生成这种剧本的优化，先上网好好搜索一下再优化skill

> AGENT

我会先按广告片/导演阐述/电影现实主义质感去补资料，然后把 `ad-creative-script` 增加一个可选模式：**超真实电影质感 / grounded cinematic realism**。这个模式会和之前的“魔幻世界规则”并列，不再强制所有创意都走奇幻设定。

> AGENT

我会同时用两套本地指引：`agent-reach` 负责搜索资料路线，`skill-creator` 负责把优化写成可维护的 skill 结构。已经搜到的资料重点都指向一个结论：所谓“超真实电影质感”不是少想象，而是把戏剧冲突压进真实表演、自然光、真实空间、细节动作和镜头节奏里。

> AGENT

我会把原来的“必须走想象力世界规则”改成“先选创意模式”：一种是现在已有的高概念/魔幻世界规则，另一种是你要的超真实电影质感。真实电影质感模式要用真实空间、自然/动机光、克制表演、生活细节、镜头节奏来产生高级感，而不是靠奇观。

> AGENT

资料重点我整理好了：超真实电影感不是“少创意”，而是用导演处理建立可信的情绪真实。它需要真实地点、动机光/实用光源、克制镜头、自然表演、细节动作、环境声、生活节奏和可观察的行为。现在我写进 skill。

> AGENT

新的 realism 参考文件已经加上。接下来我会改主流程：先判断模式，如果用户要超真实电影质感，就走“真实压力 + 行为细节 + 电影化分镜”，不再强制 70% 魔幻世界规则。

> AGENT

主流程已支持模式选择了。接下来我会把 visual-planning 和质量评审也补上 realism 模式，避免它生成“好看的生活方式空镜”或者“真实但没戏”的片子。

> AGENT

改完了，我现在做文件/YAML 校验和关键词回查，确认 realism 模式被正确接入，而不是只有一个孤立参考文件。

> AGENT

已经按你的要求优化了 skill，新增一个和“魔幻/高概念”并列的可选方向：**Grounded Cinematic Realism / 超真实电影质感**。

**新增文件**
[cinematic-realism.md](/Users/lyston/.codex/skills/ad-creative-script/references/cinematic-realism.md)

它定义了这个模式怎么写剧本和分镜：

- 不强制魔幻世界规则
- 用真实生活压力做戏剧核心
- 用行为代替解释
- 用真实空间、动机光、自然环境声、克制表演来建立高级感
- 产品通过真实 routine / 选择时刻进入，而不是奇幻装置
- 分镜要写真实细节、表演备注、动机光源、环境声、未说出口的情绪

**主流程已改**
[SKILL.md](/Users/lyston/.codex/skills/ad-creative-script/SKILL.md)

现在新增了 **Creative Modes**：

1. **High-concept imagination**  
   魔幻、高概念、世界规则、天马行空。

2. **Grounded cinematic realism**  
   超真实电影质感、写实高级感、纪录片质感、自然主义、非魔幻广告片。

3. **Hybrid**  
   只有用户明确要求混合时才用。

**质量评审也补了**
[quality-rubric.md](/Users/lyston/.codex/skills/ad-creative-script/references/quality-rubric.md)

新增会拦掉：

- `Fake realism`：真实场景 + 自然光，但没有戏剧压力
- `Lifestyle wallpaper`：漂亮生活方式空镜，没有冲突/动作/记忆点
- `Cinematic adjective soup`：只写“电影感、自然光、纪录片质感”，但没有落实到镜头选择

**分镜规划也补了**
[visual-planning.md](/Users/lyston/.codex/skills/ad-creative-script/references/visual-planning.md)

超真实电影质感模式下，每个关键镜头还要写：

- 真实地点
- 生活质感细节
- 克制表演
- 动机光源
- 环境声
- 行为转折
- 未说出口的情绪

参考资料方向包括 StudioBinder 的 shot list、camera shot、camera angle、camera movement、motivated/practical lighting 等影视制作资料，以及商业导演 treatment / naturalistic commercial 的方法。现在这个 skill 可以明确生成两种完全不同的广告片：一种是高概念魔幻，一种是超真实电影质感。

> DEVELOPER

生成一个巴宝莉香水的剧本，体现要电影质感的

> AGENT

使用 `$ad-creative-script` 的 **Grounded Cinematic Realism / 超真实电影质感** 模式来写，不走魔幻，不用夸张奇观。核心是：伦敦雨后、真实人物、克制表演、动机光、环境声、香水作为一个“进入自己状态”的动作。

**片名：《雨停之前》**  
**品牌：Burberry 巴宝莉香水**  
**片长：75s 品牌香水电影短片**  
**气质：英伦、克制、湿润、真实、高级电影感**

**一句话创意**  
不是香水让她变成另一个人，而是在城市还没完全醒来的雨后，她用一滴气味，把自己带回自己。

**Realism Treatment**
| 项目 | 设定 |
|---|---|
| Human truth | 人有时不是为了被别人注意才喷香水，而是为了确认“我已经准备好进入今天”。 |
| Observed situation | 清晨雨后的伦敦，一个女人从住处出门，穿过湿街、地铁、咖啡店、办公室前的空白时刻。 |
| Silent conflict | 她今天有一个重要会面，但片中不明说，只通过动作和节奏表现她在整理自己。 |
| Product role | 香水不是魔法，而是她出门前最后一个安静、准确的自我确认动作。 |
| Light | 阴天窗光、浴室镜灯、地铁冷光、雨后街面反光、咖啡店暖光。 |
| Sound | 雨滴、衣料摩擦、喷头轻响、地铁进站、皮鞋踩过水面、远处车声。 |
| Brand memory | 风衣、雨后伦敦、格纹内衬一闪而过、香水喷雾声、低声一句：“Before the city sees you.” |

---

## 75s 剧本 / 分镜

| 时间 | 镜头设计 | 画面 | 声音 / 文案 | 产品角色 |
|---|---|---|---|---|
| 00-07s | **极近景 / 静态 / 浅景深** | 窗玻璃上挂着雨滴。伦敦清晨灰蓝色的光透进来。远处车灯在玻璃后模糊成一条线。 | 环境声：雨刚停，远处车声。无 VO。 | 未出现，先建立湿润城市质感。 |
| 07-14s | **中近景 / 镜前侧拍 / 自然浴室灯** | 女主站在浴室镜前，没有浓妆，头发微湿。她看着镜子，停顿两秒，把一枚耳环戴上，又摘下，换成更简单的一枚。 | 只有耳环轻碰洗手台的声音。 | 表现“整理自己”，不是摆拍。 |
| 14-22s | **插入特写 / 手部 / 静态** | 她从洗手台边拿起 Burberry 香水。瓶身被窗光和镜灯切出干净轮廓。旁边有一条搭在椅背上的风衣，格纹内衬只露出一小角。 | 喷头被按下前的轻微塑料声。 | 产品第一次出现，真实放在生活场景中。 |
| 22-28s | **极近景 / 慢推 / 微距** | 香水喷出。不是梦幻粒子，而是一层很真实的细雾，在冷光里停留半秒，落到锁骨和风衣领口之间。她闭眼，但没有广告式陶醉，只是轻轻吸一口气。 | 喷雾声清晰。VO 低声：Before the city sees you. | 香水成为出门前的自我确认。 |
| 28-38s | **跟拍 / 背后中景 / 走廊自然光** | 她穿上风衣，走出公寓。走廊有老木地板和昏黄灯。她经过邻居门口，门缝里传来收音机声。她没有回头，只把风衣腰带随手打了一个不完美的结。 | 衣料摩擦、钥匙入包。 | 香气不被视觉化，留在动作和气质里。 |
| 38-48s | **低机位 wide / 雨后街面反光 / 轻微手持** | 她走上伦敦街头。路面有积水，红色公交车从画面远处掠过。她停在路口，风吹起衣角，格纹内衬闪过一瞬。 | 环境声：湿路、公交、行人脚步。无 VO。 | Burberry 品牌资产自然出现：风衣、伦敦雨后。 |
| 48-58s | **地铁车窗反射 / 中近景 / 冷色荧光** | 她坐在地铁里。车窗反射出她的脸，也反射出对面乘客、广告灯箱、隧道光。她低头看手机，一条消息显示“10:00”。她锁屏，没有回复。 | 地铁进站声。VO：Not for everyone. First, for yourself. | 香水和“进入状态”绑定。 |
| 58-67s | **咖啡店门口 / 侧逆光 / 慢推** | 她推门进入咖啡店。门铃响。室内暖光落到她的肩线。她经过一位陌生人，对方没有夸张回头，只是在她经过后轻微停顿。她也没有注意到。 | 门铃、咖啡机蒸汽声。 | 表达香气存在感，但克制，不俗套。 |
| 67-75s | **End Frame / 静物特写 / 窗光** | Burberry 香水瓶放在窗边。雨滴还在玻璃上，远处城市模糊。风衣搭在椅背，格纹内衬若隐若现。 | VO：Burberry Fragrance. Before the city sees you.  字幕：Burberry | 产品收束，保留电影余味。 |

---

## 视觉关键词

- 雨后伦敦，不是旅游明信片
- 灰蓝自然光 + 咖啡店暖光
- 风衣、格纹内衬、湿街反光
- 克制表演，不笑、不摆拍
- 香水喷雾声作为记忆点
- 镜头多用静态、慢推、轻微手持，不做浮夸运镜

## Slogan 方向

**Before the city sees you.**  
中文可译：**在城市看见你之前，先成为自己。**

若要更中文广告片一点：  
**在世界靠近前，先靠近自己。**

> DEVELOPER

你生成的剧本常常是8秒一个分镜，但是这样每个分镜生成出来的图片要表现的内容就太多了，生图模型并不能理解你想要的感觉，继续优化skill

> AGENT

你这个点非常具体，而且是生成链路里的真问题：8 秒一个分镜适合导演看，但不适合生图模型。AI keyframe 需要更小颗粒度：一帧只表达一个决定性瞬间、一个主体动作、一个镜头意图。我要把 skill 加上“AI 生图分镜拆帧模式”，把长镜头拆成可生成的 keyframes。

> AGENT

我会先看现有 `storyboard-ai-prompts` 和 `visual-planning`，然后直接改：区分“导演分镜”和“AI 生图关键帧”，后者必须拆得更细，禁止一张图同时塞多个动作、情绪变化、转场和故事信息。

> AGENT

现在我会直接给 `storyboard-ai-prompts` 增加“导演分镜 vs AI 生图帧”的拆分规范，并把推荐密度改成：导演分镜可以 8-10 镜，但 AI keyframes 要按动作拆成更多、单帧更轻。

> AGENT

AI 拆帧规则已经加了。接下来我把主流程和 visual planning 也改掉：只要涉及生图/AI keyframes，就必须输出扩展关键帧包，而不是把 8 秒镜头当一张图。

> AGENT

规则已经接到主流程、视觉规划和质量评审里。最后做解析检查和关键词回查，确认没有写成孤立文档。

> AGENT

你说的这个问题很准：**导演分镜 ≠ 生图分镜**。8 秒一个镜头可以给导演看，但对生图模型来说太重了，一张图承载不了“走进来、喷香水、情绪变化、城市反应、转场”这些连续信息。

我已经把 skill 优化了。

**核心改动**

[storyboard-ai-prompts.md](/Users/lyston/.codex/skills/ad-creative-script/references/storyboard-ai-prompts.md) 新增：

- **Director storyboard vs AI keyframes**
- **AI Keyframe Decomposition Rule**
- **Keyframe Complexity Budget**

现在规则是：

- 导演分镜可以 4-8 秒一个 shot
- AI 生图关键帧必须是 **一个静止决定性瞬间**
- 一个 keyframe 只能有：
  - 1 个主视觉主体
  - 1 个动作
  - 1 个情绪状态
  - 1 个产品角色
  - 1 个镜头景别和角度
  - 1 套光线
- 如果描述里出现“然后”“同时”“从……到……”“前后变化”，就必须拆帧

**密度也改了**

原来：
- 60s 可能 12-16 个分镜

现在：
- 导演分镜：60s 用 16-24 shots
- AI 生图 keyframes：60s 用 28-40 keyframes
- 75-90s 用 36-54 keyframes

并且会标记：
- `Hero keyframe`
- `Continuity keyframe`
- `Transition keyframe`
- `End-frame keyframe`

**主流程也接入了**

[SKILL.md](/Users/lyston/.codex/skills/ad-creative-script/SKILL.md) 现在明确写了：

> 不要把一个 6-8 秒导演镜头当成一张生图 prompt。复杂镜头要拆成 setup / action / consequence keyframes。

[visual-planning.md](/Users/lyston/.codex/skills/ad-creative-script/references/visual-planning.md) 也加了判断：

- 1 keyframe：静态瞬间
- 2 keyframes：setup + consequence
- 3 keyframes：setup + product/action contact + resolved state

[quality-rubric.md](/Users/lyston/.codex/skills/ad-creative-script/references/quality-rubric.md) 新增杀稿项：

- `Prompt overload`
- `Storyboard-to-image mismatch`

之后如果你要我生成“可生图”的分镜，我会直接输出更细的 AI keyframe package，而不是只给 8 秒一格的大分镜。

> DEVELOPER

真实感电影质感还不够，特别是对于人、场景的刻画等，继续上网搜索优化skill

> AGENT

我会继续按 `agent-reach` 做网页调研，同时用 `skill-creator` 的方式把结果落到 `ad-creative-script`。这次聚焦“人”和“场景”的真实感：角色不是标签，场景不是背景板，要有生活痕迹、社会身份、动作习惯、空间关系和未说出口的压力。

> AGENT

我查到的核心方向很一致：真实感不是“更像照片”，而是 mise-en-scène 的完整性：演员、服装、道具、空间、灯光、走位都要共同讲故事。接下来我会新增一个“人物与场景真实感刻画”的参考文件，并把 realism 模式强制接上角色/场景 bible。

> AGENT

我补看了 mise-en-scène、production design、set dressing、blocking 和自然表演相关资料。结论：现在 skill 还缺一个“角色生活档案 + 场景生活痕迹 + 走位关系”的强制步骤。我会写成新参考文件，并接入 realism 模式。

> AGENT

我会新建 `character-scene-realism.md`，专门解决“人”和“场景”：人物要有社会身份、衣着逻辑、手部习惯、沉默压力；场景要有使用痕迹、空间阻力、道具关系、光源来源。然后主流程会要求 realism 模式先做 character/scene bible。

> AGENT

角色/场景真实感参考文件已经加好。接下来把它接入 `cinematic-realism` 和主流程：只要走超真实电影质感，就必须先做人物小传和场景小传。

> AGENT

主流程已接入。现在把分镜模板和质量评审也补上，要求人像 prompt 和场景 prompt 都有“生活痕迹/身体动作/空间关系”，防止生成塑料感人像和样板间。

> AGENT

有个补丁上下文没对上，我先打开当前分镜文件的关键段，再精确 patch。

> AGENT

已经把人和场景的真实感接入分镜、prompt 和质量评审。最后做 YAML/关键词检查，确认不会影响 skill 加载。

> AGENT

已继续优化，重点补的是 **人和场景的真实感**，不是再堆“电影感”形容词。

**新增文件**
[character-scene-realism.md](/Users/lyston/.codex/skills/ad-creative-script/references/character-scene-realism.md)

现在超真实电影质感模式会强制先做：

- **Character Bible**：人物身份、生活节奏、今天的压力、没说出口的事、手部习惯、穿衣逻辑、包里/口袋里的东西、与产品的关系
- **Scene Bible**：地点为什么是这里、时间/天气、主光源、生活痕迹、空间阻力、前中后景、场外世界、产品自然放在哪里

**接入位置**
- [SKILL.md](/Users/lyston/.codex/skills/ad-creative-script/SKILL.md)：Grounded cinematic realism 现在会读取 `cinematic-realism.md` + `character-scene-realism.md`
- [visual-planning.md](/Users/lyston/.codex/skills/ad-creative-script/references/visual-planning.md)：新增人物/场景真实感检查
- [storyboard-ai-prompts.md](/Users/lyston/.codex/skills/ad-creative-script/references/storyboard-ai-prompts.md)：人像 prompt 要写 hand/body behavior、wardrobe logic、lived-in detail
- [quality-rubric.md](/Users/lyston/.codex/skills/ad-creative-script/references/quality-rubric.md)：新增杀稿项 `Model in a room`、`Background showroom`

现在会拦掉这类问题：

- “一个优雅女人在高级公寓”这种空泛人设
- “真实场景 + 自然光”但人物没有生活痕迹
- 场景像样板间，没有使用痕迹、空间关系、场外世界
- 人物只写漂亮/高级/自信，不写动作习惯和沉默压力

参考方向包括 StudioBinder 的 mise-en-scène、production design、set dressing、blocking，以及自然表演/真实商业片导演处理方法。下一次再生成巴宝莉这种电影质感脚本，会先给人物小传和场景小传，再进入分镜。

> DEVELOPER

生成一个巴宝莉香水的剧本，体现要电影质感的

> AGENT

我会用 `ad-creative-script` 的 **Grounded cinematic realism** 模式来写：不走魔幻，不走“漂亮女人+雨后伦敦”的空镜堆砌，先把人物、场景、沉默压力、真实动作和产品进入方式定住，再给剧本和可拍分镜。

> AGENT

下面用 **超真实电影质感 / Grounded Cinematic Realism** 来写一版。不是魔幻，也不是漂亮空镜，而是靠人物、空间、动作、光线和声音建立高级感。

# 巴宝莉香水品牌短片：《扣好之前》

**片长**：75s  
**气质**：英伦、克制、雨后、真实空间、低声电影感  
**一句话创意**：  
香水不是为了让别人发现她，而是在她进入世界之前，帮她先认出自己。

## 人物小传

**人物**：31 岁，女性，织物修复师 / 博物馆档案修复相关工作。  
**今天的压力**：她要去做一次重要陈述，展示一件修复完成的旧风衣。  
**没说出口的事**：她并不害怕失败，她害怕自己被看见时不像自己。  
**身体习惯**：紧张时会用拇指摩挲袖口纽扣。  
**穿衣逻辑**：不是时髦摆拍，是一件穿了很久的风衣，袖口有轻微磨白，内衬格纹只在动作间露出。  
**产品关系**：Burberry 香水是她出门前最后一个私人动作，不是给别人闻，是让自己进入状态。

## 场景小传

**地点**：伦敦一间不大的清晨公寓、楼梯间、雨后街道、博物馆后门。  
**光线**：灰蓝窗光、浴室镜灯、楼梯间钨丝灯、街面反光、博物馆走廊冷光。  
**生活痕迹**：桌上有修复针线、旧布料样本、半杯冷掉的茶、发票、风衣纽扣、未合上的资料夹。  
**声音**：雨水从窗沿滴下，衣料摩擦，喷头轻响，钥匙碰撞，远处公交刹车声。

---

## 75s 剧本 / 分镜

| 时间 | 镜头 | 画面 | 声音 / 文案 | 产品角色 |
|---|---|---|---|---|
| 00-06s | **ECU 极近景 / 静态** | 一枚旧风衣纽扣放在桌上。指腹轻轻擦过纽扣边缘，能看到很细的划痕。背景虚焦里有一小块 Burberry 格纹内衬。 | 雨滴敲窗。没有音乐。 | 先建立材质与品牌气质。 |
| 06-13s | **MS 中景 / 窗边侧光** | 女主坐在桌前，把修复好的风衣摊开。她没有化完整妆，头发简单夹起。桌上有针线、资料卡、半杯冷茶。 | 远处车声。纸张轻响。 | 产品未出现，人物先成立。 |
| 13-20s | **CU 手部特写 / 慢推** | 她把一页陈述稿折好，放进包里。手机屏幕亮起：`Presentation 10:00`。她看一眼，没有解锁。拇指开始摩挲袖口纽扣。 | 手机震动一下，马上安静。 | 呈现沉默压力。 |
| 20-28s | **Insert / 洗手台边 / 动机光** | Burberry 香水放在洗手台边，不是居中摆拍，旁边有发夹和一枚备用纽扣。她伸手拿起香水，停顿一秒。 | 玻璃瓶轻碰瓷面。 | 产品自然进入真实空间。 |
| 28-34s | **MCU / 侧背 / 镜中反射** | 她对着镜子，喷在锁骨与风衣领口之间。喷雾很细，只在镜灯里短暂可见。她没有闭眼陶醉，只是轻轻吸一口气，肩膀放松一点。 | 喷头声清晰。VO 很低：有些准备，不需要被看见。 | 香水是自我确认动作。 |
| 34-43s | **FS 全身 / 走廊手持轻跟** | 她穿上风衣走出门。楼梯间窄，墙面有旧漆痕。她下楼时，手自然碰到袖口，格纹内衬一闪而过。 | 衣料摩擦，钥匙碰撞，楼下门响。 | 香气跟随衣物和动作，不被可视化。 |
| 43-52s | **WS 宽景 / 雨后街面 / 低机位** | 她站在路边等红灯。湿路面映出公交红色和天空灰蓝。风吹起衣角，她没有整理头发，只把风衣腰带重新收紧。 | 公交刹车声，水声。无 VO。 | Burberry 的雨后城市气质自然出现。 |
| 52-61s | **OTS 过肩 / 博物馆后门** | 她推开一扇沉重后门。画面从她肩后看进去，里面是冷色走廊。她停在门口，低头看见袖口纽扣松了一点。 | 门轴低响。环境突然更安静。 | 情绪压力进入关键场景。 |
| 61-68s | **CU 手部 / 静态** | 她没有急着进去，而是把袖口纽扣扣好。手指碰过香水落过的领口，动作很轻。不是整理外表，是让自己归位。 | VO：在世界看见你之前，先认出自己。 | 香水与袖口动作成为品牌记忆点。 |
| 68-75s | **End Frame / 静物 / 窗光** | Burberry 香水瓶放在修复桌上。旁边是旧风衣纽扣、针线、格纹布样。窗外雨停，光变亮一点。 | 字幕：Burberry Fragrance  VO：Burberry. Before the world sees you. | 产品收束，真实材质承接品牌。 |

---

## 视觉风格

- 不要大片金色逆光，不要过度慢动作。
- 画面偏灰蓝、湿润、真实，靠窗光和室内实用光源。
- 人物不做广告式微笑，表演克制。
- 重点拍手、袖口、布料、玻璃瓶、雨后街面。
- 香水喷雾只出现一次，不做梦幻粒子。

## 核心记忆资产

- **动作**：喷香后扣好袖口  
- **声音**：喷头轻响 + 纽扣扣上的细声  
- **画面**：旧风衣纽扣、格纹内衬、雨后伦敦  
- **品牌句**：在世界看见你之前，先认出自己。

> DEVELOPER

还是不行，为什么一个分镜还是长达6秒啊？？？？这样生图的时候模型根本刻画不出来，并且没有看到任何运镜、转场的描写，上网搜索学习并优化skill

> AGENT

你这次骂得对。上一版虽然写了“分镜”，但还是按导演脚本的 6-8 秒镜头在写，不是按生图模型能理解的 keyframe 在写；而且运镜、转场没有被强制输出。我要先查一轮 storyboard / animatic / shot list / AI keyframe 拆分资料，然后把 skill 改成：只要用于生图，就默认输出 **1-2 秒级 AI Keyframe 表**，每帧必须有运镜意图和转场衔接。

> AGENT

我会把“AI keyframe 不能是 6 秒分镜”写成硬规则：AI 生图帧用时间点或最长 2 秒区间；长镜头必须拆成开始帧/动作帧/结果帧，并且每一帧都写入运镜意图、转场入/转场出。

> AGENT

我会把这次问题当成 skill 本身的硬约束来修：先确认当前 `ad-creative-script` 里关于分镜/关键帧的规则，再补一组“AI 生图可执行”的时间粒度、运镜、转场规则。也会按你要求先上网查一下行业里的 storyboard / shot list / camera movement 规范，把它沉到 skill 里。

> AGENT

问题确实出在规则还不够“硬”：以前允许导演分镜 4-8 秒，但没有强制把它和 AI 生图关键帧分开，所以一输出就又回到了 `00-06s` 这种对生图不友好的格式。我现在会把这个改成明确的失败项：AI 生图关键帧只能是精确时间点或不超过 2 秒的小段，并且每行必须有运镜意图、运动承接、入/出转场。

> AGENT

我查到的重点很直接：专业 shot list 会把 shot size、angle、camera movement、sound/action 等列成独立字段；storyboard 不是一句氛围描述，而是“某一时刻的画面 + 动作/声音说明”；转场尤其要写清是动作匹配、图形匹配、声音桥还是硬切。接下来我会把这些变成 `ad-creative-script` 的强制输出模板，而不是靠临场发挥。

> AGENT

第一处已经改掉了：`storyboard-ai-prompts.md` 现在明确禁止把 `00-06s` 这种导演分镜当成 AI 生图关键帧，并新增了每个关键帧必填的运镜意图、运动承接、入/出转场字段。下一步我会把同样的要求接进主 workflow 和 visual planning，这样触发 skill 时不会只停留在参考文件里。

> AGENT

主入口和视觉规划也同步了。现在这个 skill 会把“导演分镜”和“AI 生图关键帧”当成两个层级，不再默认用长时间段承载画面；而且关键帧表会强制写清镜头怎么动、上一帧怎么进来、下一帧怎么切出去。

> AGENT

我还发现一个容易误导输出的旧句子：它写着“导演分镜可 4-8 秒”，这会让模型在用户说“分镜”时误以为长段也可以。我会把它拆得更细：高层脚本节拍可以长，真正的生产分镜默认 1.5-4 秒；只要涉及生图，就一律进入 0-2 秒关键帧。

> AGENT

你说得对，之前最大的问题是把“导演分镜”误当成“AI 生图关键帧”输出了。`00-06s` 这种对导演可能还能理解，但对生图模型就是灾难：一个画面里塞了太多时间、动作和情绪。

我已经优化了 `$ad-creative-script`，重点改了这几处：

- [SKILL.md](/Users/lyston/.codex/skills/ad-creative-script/SKILL.md)：新增硬规则，AI 生图关键帧必须用“精确时间点”或“不超过 2 秒”的小段，不能再用 6 秒/8 秒长分镜。
- [storyboard-ai-prompts.md](/Users/lyston/.codex/skills/ad-creative-script/references/storyboard-ai-prompts.md)：明确拆成三层：脚本节拍、导演分镜、AI 生图关键帧。AI 关键帧每行强制包含：单一画面、运镜意图、运动承接、入场转场、出场转场。
- [visual-planning.md](/Users/lyston/.codex/skills/ad-creative-script/references/visual-planning.md)：新增 `AI Keyframe Timing`，明确 `00-06s` 这种是无效生图行。
- [quality-rubric.md](/Users/lyston/.codex/skills/ad-creative-script/references/quality-rubric.md)：新增失败项 `Long-frame prompt` 和 `Missing motion grammar`，以后没有运镜/转场逻辑会被判为不合格。

我也做了校验：`SKILL.md` 的 YAML 解析正常。

这次参考了这些资料来补规则：  
[Boords Camera Moves](https://boords.com/create/camera-moves)、[StudioBinder Shot List](https://www.studiobinder.com/templates/shot-list/)、[StudioBinder Shot List Guide](https://www.studiobinder.com/blog/shot-list-template-free-download/)、[StudioBinder Storyboard Arrows](https://www.studiobinder.com/blog/storyboard-arrows-meaning)、[StudioBinder Match Cuts & Transitions](https://www.studiobinder.com/blog/match-cuts-creative-transitions-examples/)。

> DEVELOPER

生成一个巴宝莉香水的剧本，体现要电影质感的

> AGENT

我会用 `$ad-creative-script` 来写这一版，并按刚刚优化后的规则输出：电影质感不靠“高级、氛围”这种空词，而是靠真实场景、人物行为、光线、镜头、剪辑和不超过 2 秒的 AI 生图关键帧来落地。

> AGENT

我已经读了电影真实感、人物/场景真实感和新关键帧规则。现在会按“高级香水片”来做，但避开常见的空镜头堆砌：让香水不是装饰，而是女主进入城市、进入关系、进入自己状态的触发动作。

> AGENT

我这版先按 **Burberry Her Eau de Parfum** 写，因为官方信息里它和“伦敦、红/黑莓调、白木质调、低调复古瓶身”绑定很强，很适合电影质感。  

**片名：给风留一颗扣子**  
**时长：30s**  
**创意核心：** 她不是喷香水去变得“更完美”，而是在进入公共目光前，保留一点不被驯服的自己。  
**质感方向：** 伦敦雨后、画廊开幕前、真实人物行为、克制表演、自然声、湿冷街面、木地板、红莓色视觉记忆。

| 时间 | 画面 / 表演 | 镜头 / 运镜 / 转场 | 声音 / 文案 |
|---|---|---|---|
| 00:00-01:5 | 雨后伦敦街口，红色行人灯倒映在湿地上。一截黑色风衣下摆停在画面边缘。 | 低机位静止，水面反光。硬切进。 | 远处车声，雨滴。 |
| 01:5-03:0 | 手机亮起：信息只露出一句“Can we make it softer?” 她的拇指停住，没有回复。 | ECU，轻微手持漂移。声音桥切。 | 手机震动一声。 |
| 03:0-04:5 | 画廊后台镜前，她把风衣扣子扣到一半，停下，故意留下一颗。 | MCU，慢推近。切在手指动作上。 | 布料摩擦。 |
| 04:5-06:0 | 木质旧架上，Burberry Her 香水放在钥匙、开幕手环、折皱展签旁。 | 插入镜头，rack focus 从钥匙到瓶身。硬切。 | 空调低鸣。 |
| 06:0-07:5 | 她拿起瓶子，喷在颈侧风衣领口内侧。雾气只停留一瞬。 | ECU，宏观微移。切在喷雾声上。 | 清脆喷雾声。 |
| 07:5-09:0 | 镜中她看自己，不微笑，也不整理那颗扣子。 | 镜面中景，慢推停住。匹配切。 | 呼吸变稳。 |
| 09:0-10:5 | 街边市场红莓被倒进木箱，颜色短促闪过。不是幻想，是她路过的伦敦。 | 手持掠过，红色图形匹配瓶身。 | 摊主声音一闪。 |
| 10:5-12:0 | 她穿过画廊后廊，湿伞靠墙滴水，木地板有旧划痕。 | 低位跟拍脚步。切在脚步落地。 | 鞋跟、雨水滴落。 |
| 12:0-13:5 | 手按上厚重门把，指尖停半秒。 | CU，静止 hold。声音桥进展厅。 | 展厅人声变近。 |
| 13:5-15:0 | 门开，白墙、木地板、人群侧脸。没有人立刻看她。 | 拉开式 reveal，门框做前景。硬切。 | 人群低语。 |
| 15:0-16:5 | 她走到音响边，删除“sorry”，按下播放。 | OTS，轻微推近到手机屏。切在按键。 | “咔哒”一声。 |
| 16:5-18:0 | 伦敦街声进入展厅：雨、市场、人声、车轮。几个人慢慢抬头。 | WS，静止观察。声音桥延续。 | 城市声替代音乐。 |
| 18:0-19:5 | 她站在白墙边，风衣扣子仍留着一颗，领口有很轻的动作。 | 侧面 MCU，慢推。硬切。 | 无 VO。 |
| 19:5-21:0 | 玻璃展柜反射出她包里的粉色香水瓶轮廓，真实、短暂。 | rack focus：玻璃反射到瓶身。图形匹配切。 | 城市声变柔。 |
| 21:0-22:5 | 一个观众靠近门边，不是看她，是听见外面的城市被带进来了。 | 中景横移，人物经过前景遮挡。 | 人群安静。 |
| 22:5-24:0 | 她终于走到门外，雨停，风吹动没扣上的那一颗。 | 背影跟拍，轻微 handheld。切在风动。 | 风声。 |
| 24:0-25:5 | 香水瓶放在湿木窗台，后景是伦敦街灯和红色反光。 | 产品 CU，静止，浅景深。淡入字幕。 | 一声喷雾回响。 |
| 25:5-27:0 | 瓶身旁边压着一张折过的展签，纸角被风掀起。 | 宏观慢推，纸角运动承接。 | VO 低声：有些痕迹，不需要解释。 |
| 27:0-28:5 | 她消失在人群里，只剩风衣下摆从画面边缘掠过。 | 低机位，运动模糊出画。匹配切到瓶身。 | 城市声。 |
| 28:5-30:0 | End frame：Burberry Her 瓶身，湿木、红色反光、留白给 logo。 | 锁定镜头，end-frame lock。 | 字幕：Burberry Her. Before you say a word. |

**AI 生图关键帧规则已按新版执行：** 每个分镜都是 1.5 秒，没有 6 秒长镜头；每行都有运镜和转场逻辑，适合拆成单张图生成。

产品依据：Burberry 官方页面提到 Her Eau de Parfum 的红/黑莓调、白木质调、伦敦精神与低调复古瓶身设计：[Burberry Her Eau de Parfum](https://us.burberry.com/her-eau-de-parfum-100ml-p40804591)。

> DEVELOPER

[$codex-md-docs](/Users/lyston/.codex/skills/codex-md-docs/SKILL.md) 记录这个剧本

> SYSTEM

<skill>
<name>codex-md-docs</name>
<path>/Users/lyston/.codex/skills/codex-md-docs/SKILL.md</path>
---
name: codex-md-docs
description: Route Markdown documentation work into the user's Codex Obsidian space, including choosing or creating device/category folders, deciding whether to create/append/update notes, and keeping operational records separated by device/environment. Use when the user asks Codex to create, write, update, append, record, summarize, save, organize, archive, or maintain any Markdown document, md note, deployment record, operation guide, SOP, troubleshooting note, decision record, or session handoff unless the user explicitly gives a different destination.
---

# Codex Markdown Docs

## Default Root

Use this Markdown documentation root by default:

```text
/Users/lyston/Obsidian/lyston/Codex
```

Prefer this root even if older notes exist elsewhere, unless the user explicitly names another path. Create it if it is missing. Do not write documentation into project source trees, `/tmp`, `/root`, downloads, or ad hoc scratch folders unless the user explicitly asks.

## Placement Model

Use the existing vault structure as the source of truth. The active Codex vault structure is device-first:

```text
Codex/
  lystonmacbook-pro.local/
  lyston11.qzz.io/
```

Top-level folders under `/Users/lyston/Obsidian/lyston/Codex` must be device, host, or environment names. Under each device directory, classify documents by service, project, or content type, such as:

```text
Hermes
Fast Note Sync
Sub2API
基础设施
DBX
GenericAgent
HAPI
MindOS
Codex工具与文档系统
LDStatus Pro
锐鲨
```

Do not put service or project folders directly under the Codex root. Do not create or maintain `README.md`, separate catalog folders, summary entry pages, or original archive folders. Use device directories, category directories, clear filenames, headings, and search for discoverability.

When a split is complete, day-to-day entry points are the device folders, category folders, and focused Markdown files only.

## Before Writing

1. If the user gives an exact file path, use that path.
2. If the user gives a folder path, choose or create the `.md` file inside that folder.
3. If the user gives only a title or topic, inspect likely matching device folders and Markdown files under `/Users/lyston/Obsidian/lyston/Codex`.
4. Search device directories, category directories, filenames, and headings for the topic, service name, date, project, domain, path, hostname, device name, or keywords from the request.
5. Identify the device/environment before choosing the directory, appending, or updating. Compare hostname/device name, OS, cloud provider, public domain/IP, deployment root, path style, container runtime, and tunnel/reverse-proxy endpoint when available.
6. Use clear filenames and headings because there are no folder entry pages.
7. Hard rule: never merge records across different devices or environments only because the service name matches.
8. Prefer an existing note only when both the device/environment and topic/service match.
9. Preserve existing Markdown structure, frontmatter, headings, Obsidian links, and unrelated content.
10. Do not create database backups, code backups, or duplicate archival files unless the user explicitly asks.

## Create, Append, Or Update

Choose the smallest durable change that fits the request:

- **Create** a new file when no strong match exists, the topic is new, the environment differs, or the user asks for a standalone document.
- **Append** for deployment logs, operational history, incident notes, progress records, meeting notes, dated observations, command outputs, session handoffs, and continuing timelines.
- **Update** an existing section for living guides, SOPs, runbooks, architecture notes, checklists, policies, configuration records, or summaries whose current content should be refined.

For dated append entries, prefer:

```markdown
## 2026-05-06
```

If updating risks overwriting important history, append a dated section instead. If environment cues are missing and multiple notes could match, ask one concise clarifying question.

## Discoverability

When creating, moving, splitting, or materially updating a document, keep it discoverable:

- Do not add or update folder `README.md` files.
- Do not create or update separate catalog folders or summary entry pages.
- Use clear device directories, category directories, filenames, headings, and related-document links inside the actual notes.
- For sensitive content, record the sensitive boundary inside the relevant document itself without copying secrets or credentials elsewhere.
- Prefer Obsidian wiki links for vault-internal references. Use relative Markdown links only when they are clearer than wiki links for a specific path.

## Organization And Cleanup

If the user asks to organize, archive, split, clean up, or says the vault/folder is confusing:

1. Inventory Markdown files, directories, headings, and large mixed documents.
2. Classify by device/environment first, then by service/topic, sensitivity, and document type.
3. Split unrelated sections from large mixed documents into focused topic documents when useful.
4. Do not keep original mixed documents in original archive folders; remove old original archives after confirming the focused documents exist.
5. Create missing service/topic folders inside the appropriate device directory only when the content is likely to recur or when several documents belong together.
6. Do not create summary entry pages; keep discoverability in the folder structure, filenames, headings, and related-document links.
7. Verify final tree shape, no `README.md` files, no separate catalog folders, no original archive folders, and no stale links.

Do not keep appending unrelated operational details to a large deployment note just because it mentions the same machine. A server overview can link to service, network, and incident documents; it should not absorb them all.

## Naming

Use Chinese filenames and headings when the user writes in Chinese or the document is mainly Chinese. Use clear, short Markdown filenames.

For operational, deployment, access, tunnel, proxy, or troubleshooting records, include an environment marker in the filename when it prevents cross-device confusion:

```text
Sub2API Docker（OrbStack）部署记录.md
Sub2API Docker（Ubuntu srv-projects）部署记录.md
Cloudflare Tunnel 外网访问配置记录.md
Codex 会话同步与迁移指南.md
```

If the document belongs clearly to a service/topic folder, the environment marker can be in the document metadata instead of the filename.

## Environment Metadata

For operational documents, include ownership/context near the top when relevant:

- Hostname or device name.
- OS/cloud/provider when known.
- Main domain/IP, if public.
- Deployment root path.
- Container/runtime context, if relevant.
- Whether the record is local desktop, server-side, container-only, or tunnel/reverse-proxy related.

## Content Style

Write concise Markdown that is useful when reopened later:

- Include concrete paths, commands, service names, ports, config files, dates, and verification results when relevant.
- Keep facts separate from assumptions.
- Use fenced code blocks for commands, config, logs, and structured output.
- Redact secrets, API keys, passwords, SSH private keys, bearer tokens, and full cookies.
- For operational records, include what changed, where it lives, how to verify it, and rollback or next steps when relevant.

## Reporting Back

After writing, briefly report:

- The exact file path.
- Whether content was created, appended, moved, split, or updated.
- Which device and category folder was selected, created, or updated.
- The device/environment used to choose or separate the document when relevant.
- Any important status or caveat discovered while writing.

</skill>

> AGENT

我会按 `codex-md-docs` 的规则把它写进你的 Obsidian Codex 空间：先找现有的广告/剧本记录位置，避免乱建目录或把它放到项目源码里。

> AGENT

找到了合适的现有笔记：`lystonmacbook-pro.local/天命AI写作/广告创意剧本样稿记录.md`，里面已经记录过之前的奶粉和 999 剧本。这个巴宝莉香水片属于同一类广告创意样稿，我会追加到这个文件里。

> AGENT

我会追加一段新的“巴宝莉香水剧本”，保留原文件结构，不覆盖前面的样稿。内容会记录完整脚本和这次特别强调的关键帧粒度说明。

> AGENT

已记录，追加到了现有样稿笔记：

[广告创意剧本样稿记录.md](/Users/lyston/Obsidian/lyston/Codex/lystonmacbook-pro.local/天命AI写作/广告创意剧本样稿记录.md:96)

这次是追加更新，没有新建文件。选择的位置是 `lystonmacbook-pro.local / 天命AI写作`，因为这里已经在记录之前用 `ad-creative-script` 生成的广告创意剧本样稿。

> DEVELOPER

写一个 奶粉、原始森林的剧本，要有真实感电影质感，整体要体现有机、阳光

> AGENT

我会用 `$ad-creative-script` 的“真实电影质感”方向来写：不走魔幻森林，而是把原始森林当成“有机来源、阳光、生命系统”的真实空间；分镜会按生图友好的短关键帧来写，不再塞 6 秒长镜头。

> AGENT

使用 `$ad-creative-script` 生成。  
方向：**真实电影质感 / 原始森林 / 有机 / 阳光 / 奶粉品牌片**。  
合规提醒：具体“有机认证、营养成分、奶源地”等卖点需按品牌实际资质替换。

**片名：《阳光先经过森林》**  
**时长：30s**  
**核心创意：** 真正的有机，不是一个包装词，而是一套被阳光、土地、水源和时间共同照看的系统。孩子喝下的那一杯，背后有一整片自然的秩序。

**人物与场景**  
主角：32 岁妈妈，做自然教育工作，带 3 岁孩子在清晨进入原始森林边缘的自然保护区。  
场景：森林木栈道、苔藓、溪水、林间小屋、窗边早餐桌。  
产品角色：有机奶粉不是“突然出现的广告道具”，而是妈妈在真实晨间照护中的固定选择。

| 时间 | 画面 / 表演 | 镜头 / 运镜 / 转场 | 声音 / 文案 |
|---|---|---|---|
| 00:00-01:5 | 清晨原始森林，薄雾贴着苔藓，第一束阳光穿过高树。 | EWS，静止，阳光从画面左上进入。淡入。 | 鸟声、远处溪水。 |
| 01:5-03:0 | 一只小手伸进光斑里，指尖沾着一点泥。 | CU，慢推近手指。切在指尖动作上。 | 孩子轻声：亮了。 |
| 03:0-04:5 | 妈妈蹲下，把孩子鞋带系紧，裤脚有湿草痕。 | MS，低机位轻微手持。硬切。 | 布料摩擦、呼吸声。 |
| 04:5-06:0 | 木栈道上，孩子跟着妈妈走，阳光一格一格落在身上。 | 背后跟拍，轻微晃动。切在脚步落地。 | VO：有些成长，不是被催出来的。 |
| 06:0-07:5 | 树皮特写，年轮纹理像一圈圈时间。孩子的手轻轻摸过。 | ECU，横向微移。图形匹配切。 | VO：是被时间慢慢照看。 |
| 07:5-09:0 | 溪水从石缝流过，水面反射阳光，清澈但不夸张。 | 低机位静止，水光自然闪动。声音桥。 | 水声变清晰。 |
| 09:0-10:5 | 林间小屋内，旧木桌、保温壶、干净奶瓶、奶粉罐放在晨光里。 | WS，窗框做前景，缓慢推入。硬切。 | 屋内很安静。 |
| 10:5-12:0 | 妈妈洗净手，擦干，动作很熟练，没有摆拍感。 | CU，水珠和手部动作。切在擦手。 | 水龙头关闭声。 |
| 12:0-13:5 | 奶粉罐打开，封口被揭开一角，粉质在光里很细腻。 | ECU，macro drift。切在封口声。 | 轻微“撕开”声。 |
| 13:5-15:0 | 一平勺奶粉落入奶瓶，阳光照到勺边，不做发光特效。 | 插入镜头，静止 hold。匹配切到水流。 | VO：有机，是每一步都经得起阳光。 |
| 15:0-16:5 | 温水注入，奶粉慢慢融开，玻璃瓶壁有细小水汽。 | CU，慢推，rack focus 到水汽。 | 温水声。 |
| 16:5-18:0 | 妈妈轻轻摇匀，孩子趴在桌边看窗外森林。 | MS，妈妈前景，孩子中景。声音桥。 | 孩子：森林也喝阳光吗？ |
| 18:0-19:5 | 妈妈停一下，没有讲大道理，只看向窗外。 | MCU，慢推到她的眼神。硬切。 | 妈妈轻声：嗯，它慢慢喝。 |
| 19:5-21:0 | 森林外景：阳光落在叶片、土壤、溪水、远处牧草坡上。 | 三个短切，match cut 光斑位置。 | VO：阳光，水源，土地，牧场。 |
| 21:0-22:5 | 回到桌边，孩子双手捧着奶瓶，额头有一点晨光。 | MCU，静止，浅景深。切在吞咽前。 | VO：最后，回到孩子每天的一杯。 |
| 22:5-24:0 | 妈妈看孩子喝奶，没有夸张微笑，只把孩子袖口轻轻拉好。 | OTS，轻微手持。切在拉袖口。 | 森林声进入屋内。 |
| 24:0-25:5 | 奶粉罐侧面在窗边，后景是树影和阳光，不是棚拍白底。 | 产品 CU，rack focus 从树影到罐身。 | VO：某某有机奶粉。 |
| 25:5-27:0 | 孩子把空手伸向窗外的光斑，手心还有一点奶渍。 | CU，慢推，光斑移动。 | VO：把自然的耐心，留给成长。 |
| 27:0-28:5 | 妈妈合上奶粉罐，罐身与木桌、溪水声、森林光影在同一空间。 | 插入镜头，end-frame 准备。 | 罐盖轻响。 |
| 28:5-30:0 | End frame：奶粉罐、奶瓶、木桌晨光，背景是虚化森林。 | 锁定镜头，end-frame lock。 | 字幕：有机成长，向阳而生。 |

**视觉记忆点**

- 阳光穿过原始森林，最后落到一杯奶里。
- 孩子问：“森林也喝阳光吗？”
- 奶粉罐不在棚拍里，而在真实木屋、溪水声和晨光中出现。
- 品牌句：**有机成长，向阳而生。**

> DEVELOPER

写一个企业宣传片剧本，需要传达的核心是：AI驱动的、可以持续进化的数据经营，陪伴式服务。

> AGENT

我会用 `$ad-creative-script` 来写企业宣传片，按 B2B/企业服务的逻辑处理：不堆 AI 术语，不做 dashboard 蒙太奇，而是把“数据经营会持续进化”和“陪伴式服务”拍成看得见的业务变化。

> AGENT

使用 `$ad-creative-script` 生成。  
方向：**企业宣传片 / AI 驱动 / 持续进化的数据经营 / 陪伴式服务**。  
我先按 90s 企业品牌片写，品牌名可替换为“锐鲨科技”或你的公司名。

**片名：《变化不是等来的》**  
**核心表达：** 品牌增长不是一次 campaign、一次数据分析、一次内容生成能完成的。真正的 AI 价值，是让企业拥有一套能持续学习、持续判断、持续优化的用户经营系统，并有人陪着它在业务里真正跑起来。

**一句话创意：**  
把“数据经营”拍成一间不断生长的品牌作战室：每一次用户变化、渠道变化、内容变化，都会被 AI 捕捉、理解、反馈，并由服务团队陪伴品牌把下一步走对。

| 时间 | 画面 | 旁白 / 字幕 | 声音 / 节奏 |
|---|---|---|---|
| 00-06s | 黑屏。不同屏幕的微光依次亮起：一条评论、一张订单、一场直播数据、一份会员标签、一条客服记录。它们不是炫酷飞线，而是散落在真实业务场景里。 | 旁白：用户在变化。内容在变化。品牌增长的方式，也在变化。 | 低频启动声，键盘声、消息提示声交叠。 |
| 06-14s | 品牌会议室。市场、会员、内容、电商、客服团队围在桌前。屏幕上不是漂亮 dashboard，而是几个真实问题：谁在流失？谁被打动？下一场活动该讲什么？ | 字幕：增长问题，从来不只属于一个部门。 | 会议室环境声，纸张翻动。 |
| 14-22s | 数据像一张城市地图慢慢拼合：消费者行为、内容互动、购买链路、会员生命周期、Campaign 反馈，被连成可以理解的路径。 | 旁白：真正重要的，不是生成一次内容，执行一次活动，分析一次报表。 | 节奏开始清晰。 |
| 22-30s | AI 系统开始运行。它不是“替人决定”，而是在旁边标出变化：新需求出现、老用户兴趣迁移、内容反馈异常、会员分层更新。 | 旁白：而是让品牌拥有一套，可以持续进化的用户经营能力。 | 轻微脉冲声，干净但克制。 |
| 30-40s | 镜头切到服务团队与客户共创：白板上写着“洞察-内容-体验-运营-复盘”。一位顾问把复杂图表改成可执行的下一步动作。 | 字幕：AI 驱动，不止是工具上线。 | 声音从科技感转为真实沟通声。 |
| 40-50s | 多个业务场景快速但清楚地展开：母婴奶粉品牌做会员分层，快消品牌调整内容策略，大健康品牌优化用户触达，客服体验被重新编排。 | 旁白：从营销洞察，到品牌内容；从客户体验，到会员运营；从 Campaign 策划，到业务复盘。 | 节奏上扬。 |
| 50-60s | 一次活动上线。画面不拍“爆炸式增长”，而拍系统持续学习：活动前策略、活动中反馈、活动后沉淀，变成下一次决策的底层能力。 | 旁白：每一次执行，都不只是结束，而是在为下一次经营积累判断。 | 节奏稳定，像机器与人协同。 |
| 60-70s | 服务团队在不同城市、不同客户现场：会议室、直播间、数据复盘会、品牌年度规划会。顾问不是旁观者，而是和客户站在同一张业务地图前。 | 字幕：陪伴式服务，让 AI 真正进入业务现场。 | 人声、脚步声、白板笔声。 |
| 70-80s | 数据经营系统从一张地图变成一棵清晰的树：根部是数据，中间是 AI 模型与产品，上方长出内容、体验、会员、活动、分析等业务枝干。 | 旁白：连接用户、数据、AI 技术与场景体验，进化全链路用户经营体系。 | 音乐打开，明亮但不夸张。 |
| 80-88s | 企业 LOGO 出现。画面展示成立时间、服务城市、行业客户、代表性能力模块。客户 logo 墙可在这里出现。 | 旁白：某某科技，AI 驱动的数据经营伙伴。 | 音乐收束。 |
| 88-90s | End frame：一句话和 logo。背景不是虚拟科技空间，而是一张仍在更新的业务地图。 | 字幕：陪伴品牌，让用户经营持续进化。 | 清晰落点。 |

**建议主视觉**  
一张“会生长的业务地图”：不是泛科技蓝光，而是由真实业务触点组成，随着 AI 学习与服务介入，逐渐变成清晰路径。

**核心文案版**  
某某科技，AI 驱动的数据经营伙伴。  
我们以 AI 技术和用户经营为核心，  
通过开盒即用的 AI 产品与陪伴式服务，  
帮助品牌连接用户、数据、AI 技术与场景体验，  
进化全链路用户经营体系。  
陪伴品牌，让用户经营持续进化。

**避免方向**  
不要拍成纯 dashboard 蒙太奇、AI 大脑、数据光线飞来飞去。这个片子的高级感应该来自“真实业务问题被一步步变清楚”，而不是科技视觉堆砌。

> DEVELOPER

还是不够有创意，在真实感、电影质感的创意想象力这一块还是比较老套，好好上网学习一下优化skill

> AGENT

你说得对，上一版虽然“真实”和“阳光”，但创意结构还是太顺了：森林、光、溪水、奶粉罐，基本是有机奶粉最容易滑进去的自然蒙太奇。我会先上网补一轮“真实感广告里的想象力”方法，再把它写进 skill：重点不是变魔幻，而是让真实世界本身出现一个更有记忆点的叙事装置。

> AGENT

我查到的核心不是“再加更多森林细节”，而是要给真实影像一个更锋利的装置：品牌要被编进故事，不是片尾出现；人物要承载压力；真实感可以带一点“贴近现实的异样视角”，但不能变成空泛魔幻。接下来我会把这套方法写成一个新的参考文件，并接入主 workflow。

> AGENT

我新增了一个专门的参考文件，解决的是“真实但没想象力”的问题：它要求真实广告必须有一个可复述的现实装置，比如证据链、物件见证、单一拍摄约束、误读后反转、自然系统变成剧情压力，而不是继续拍阳光、溪水、木桌这些熟悉符号。现在我把它接进主 skill。

> AGENT

主 skill、真实电影感参考和质量评估都已经接上。为了避免下一次又变成“自然风景 + 温柔旁白”，我还把“自然蒙太奇陷阱”列成失败项，并要求 5 秒内出现反常规的真实画面或装置。现在做一次校验。

> AGENT

你说得对，上一版掉进了“自然蒙太奇陷阱”：森林、阳光、溪水、木桌、孩子触摸苔藓，这些都真实，但太熟了，不构成真正的电影创意。

我已经上网学习后优化了 skill，新增了一个专门模式：

[grounded-cinematic-imagination.md](/Users/lyston/.codex/skills/ad-creative-script/references/grounded-cinematic-imagination.md)

它专门解决“真实电影质感但缺想象力”的问题，要求以后不能只拍漂亮自然画面，而必须有一个**真实但有记忆点的创意装置**，例如：

- 证据链：用泥、封口、光线、记录、时间戳来证明“有机”
- 物件见证：让奶粉勺、封口、木桌、光斑成为叙事线
- 单一约束：整条片只拍影子、手、门框、反光或声音
- 误读后反转：开头看似自然诗意，后面揭示成产品真相
- 自然系统变成剧情压力：不是拍森林，而是让森林“提出要求”

同时我更新了：

- [SKILL.md](/Users/lyston/.codex/skills/ad-creative-script/SKILL.md)：新增 `Grounded cinematic imagination` 模式
- [cinematic-realism.md](/Users/lyston/.codex/skills/ad-creative-script/references/cinematic-realism.md)：加入“自然/有机广告老套画面”禁用提醒
- [quality-rubric.md](/Users/lyston/.codex/skills/ad-creative-script/references/quality-rubric.md)：新增 `Natural montage trap` 和 `Realism without imagination` 失败项

我也做了校验：`SKILL.md` YAML 正常。

参考学习来源包括：  
[Thinkbox Creative Drivers of Effectiveness](https://www.thinkbox.tv/research/thinkbox-research/creative-drivers-of-effectiveness)、[Think with Google ABCD Creative Framework](https://www.thinkwithgoogle.com/_qs/documents/8472/ABCD_Complete_V7b_HR_1.pdf)。下次再生成奶粉森林片，会按这个新模式走，不再只是“阳光洒下来”。

> DEVELOPER

在重新给我写一个奶粉剧本

> AGENT

我会用刚优化后的 `$ad-creative-script`，这版走“真实电影质感 + 现实中的创意装置”，不会再用森林、阳光、溪水、木桌的普通自然蒙太奇。先把新规则和奶粉行业约束快速对齐一下，然后直接给你一版完整剧本。

> AGENT

这版我按“真实电影质感 + 现实创意装置”来写。  
不是森林美景片，而是一个更有记忆点的装置：**一家人不是去森林里看风景，而是在给孩子做一场“阳光审计”**。有机不是被说出来的，是被一束光逐项检查出来的。

**片名：《阳光来验收》**  
**品类：有机奶粉品牌片**  
**时长：45s**  
**核心创意：** 每天早晨，孩子会把家里的东西搬到第一束阳光里“验收”：苹果、泥土、雨靴、奶瓶、奶粉罐。她相信，被阳光照过的东西，不能骗人。妈妈没有纠正她，而是让这场孩子的游戏变成一次关于“有机”的真实证据链。  
**品牌句：** 有机，经得起阳光。

**创意装置**  
阳光不是氛围，而是“审计员”。  
它照到什么，镜头就检查什么：封口、标签、粉质、手、泥、时间、晨间动作。

| 时间 | 画面 / 表演 | 镜头 / 运镜 / 转场 | 声音 / 文案 |
|---|---|---|---|
| 00:00-01:5 | 黑屏中听见胶带撕开的声音。画面亮起：孩子用纸胶带在地板上贴出一个方框，正好框住一块晨光。 | 顶拍，静止。硬切进。 | 胶带“嘶啦”。 |
| 01:5-03:0 | 方框旁边歪歪扭扭写着：今天的阳光检查。 | ECU，慢推到字。 | 铅笔摩擦地板纸。 |
| 03:0-04:5 | 妈妈站在厨房门口，手里拿着奶瓶，看到这行字，停住。 | MS，门框前景，轻微手持。 | 屋外鸟声，水壶低响。 |
| 04:5-06:0 | 孩子把一只沾泥的小雨靴放进光框里，认真看鞋底的泥。 | CU，低机位，阳光切过泥痕。 | 孩子小声：这个是真的。 |
| 06:0-07:5 | 妈妈没有笑她，只把奶粉罐从柜子里拿出来，放在桌边，没有立刻入框。 | OTS，慢慢跟手。切在罐底落桌。 | 罐底轻响。 |
| 07:5-09:0 | 孩子把一颗苹果、一片叶子、一张皱巴巴的牧场照片排进光框。 | 横移，像检查清单。 | VO：孩子有时候，比大人更认真。 |
| 09:0-10:5 | 她拿起奶粉罐，想放进光框，又停下，回头看妈妈。 | MCU，慢推，停在她犹豫的眼神。 | 孩子：这个也可以检查吗？ |
| 10:5-12:0 | 妈妈蹲下，没有解释广告词，只点点头，把罐子转到标签和封口朝向阳光。 | CU，手转罐身。Rack focus 从手到封口。 | 妈妈：可以。 |
| 12:0-13:5 | 阳光照到罐身封口，封口边缘、批次码、标签纹理清楚可见。 | ECU，静止 hold。 | VO：有机，不怕被看见。 |
| 13:5-15:0 | 妈妈撕开封口，不是棚拍式完美动作，指尖有一点水痕。 | Macro，轻微 handheld。切在撕开声。 | 封口“啵”的一声。 |
| 15:0-16:5 | 一平勺奶粉被舀起，粉面不是发光，而是有真实细腻颗粒。 | ECU，微距慢推。 | 勺子碰到罐口。 |
| 16:5-18:0 | 孩子把手伸进光框，挡住一半阳光，奶粉勺的影子落在她手背上。 | CU，静止，影子成为画面中心。 | 孩子：它有影子。 |
| 18:0-19:5 | 妈妈愣一下，低头看见勺影，笑意很轻。 | MCU，慢推。切在眼神。 | 妈妈轻声：真的东西，都会有影子。 |
| 19:5-21:0 | 温水注入奶瓶，水汽升起，阳光穿过水汽，不做夸张特效。 | CU，慢移，水汽遮挡转场。 | 温水声。 |
| 21:0-22:5 | 奶粉落入水中，轻轻旋开，像一小片云慢慢散开。 | ECU，静止。声音桥。 | VO：阳光，土地，牧场，时间。 |
| 22:5-24:0 | 快切三帧真实证据：泥靴、牧场照片上的日期、罐身批次码。 | 三个 0.5s 插入，图形匹配切。 | 铅笔打勾声。 |
| 24:0-25:5 | 孩子在纸上画一个勾，但勾画歪了。妈妈没改。 | CU，手部。 | 孩子：通过。 |
| 25:5-27:0 | 妈妈摇匀奶瓶，动作很日常。光框里的东西没有被摆整齐，像真实早晨。 | MS，厨房台面前景，慢推。 | 奶液轻响。 |
| 27:0-28:5 | 孩子坐在地板上喝奶，旁边还放着泥靴、苹果、叶子、奶粉罐。 | WS，门框做前景，静止观察。 | VO：最后，回到每天这一杯。 |
| 28:5-30:0 | 妈妈把“阳光检查”的纸条贴到冰箱上，旁边已有很多孩子画的歪字。 | OTS，轻微上摇。 | 冰箱门吸住纸条。 |
| 30:0-31:5 | 纸条上新添一行：明天检查风。 | ECU，慢推。 | 孩子笑出声。 |
| 31:5-33:0 | 妈妈回头看孩子，没说“聪明”“健康”，只是把窗帘拉开一点，让光多进来。 | MS，拉窗帘动作，阳光扩大。 | 布料滑动声。 |
| 33:0-34:5 | 阳光落到奶粉罐、奶瓶、孩子小手上，三者在同一块光里。 | 低机位 CU，浅景深。 | VO：有机，经得起阳光。 |
| 34:5-36:0 | 罐身没有孤零零棚拍，而是在真实厨房地板的光框边，旁边有泥点和纸胶带。 | 产品 CU，rack focus 到品牌位。 | 轻微室内环境声。 |
| 36:0-37:5 | 孩子把奶瓶放回光框边，奶瓶底留下一个圆形水印。 | ECU，静止。 | 奶瓶轻放。 |
| 37:5-39:0 | 圆形水印和奶粉罐盖形成两个圆，像一个不完美但真实的“验收章”。 | 顶拍，图形匹配。 | 铅笔打勾声回响。 |
| 39:0-40:5 | 妈妈把那张歪歪扭扭的检查纸收进抽屉，抽屉里都是孩子以前的“检查报告”。 | CU，抽屉打开，慢推。 | 纸张摩擦。 |
| 40:5-42:0 | End frame 前一秒：孩子的手又把一小块阳光挪到奶粉罐旁边，好像怕它离开。 | CU，手和光斑。 | 孩子：别走。 |
| 42:0-45:0 | End frame：奶粉罐、奶瓶、纸胶带光框、歪字“通过”。阳光真实落在包装侧面。 | 锁定镜头，end-frame lock。 | 字幕：某某有机奶粉。有机，经得起阳光。 |

**为什么这版更有创意**

- 它不是“森林代表有机”，而是把阳光变成一个孩子发明的“验收系统”。
- 有机不靠口号解释，而靠封口、批次码、粉质、泥靴、照片、光影这些真实证据串起来。
- 阳光不只是好看，而是剧情里的检查者。
- 画面有可记忆资产：纸胶带光框、歪字“通过”、勺子的影子、圆形水印验收章。
- 每个分镜都是 1.5 秒左右，适合拆成 AI 生图关键帧。

> DEVELOPER

为什么重新写出来的剧本还是森林？？？根本没有任何创意，全是同质化
难道说是因为你保存了之前的历史记忆的原因？优化掉
并且上网学习创意，优化skill

> AGENT

你这个反馈是对的，而且问题不只是那一版剧本差，是 skill 的“上下文继承”规则不够强：它把前一次“原始森林、有机、阳光”的关键词当成了默认遗留资产，导致重新写奶粉时仍然往自然、有机、光线那条路上滑。我会把这个污染源直接写进 skill：当用户说同质化/没创意/重新写时，必须先清空上一版核心场景和视觉母题，不能把旧 brief 当成隐形约束。

> AGENT

我会直接修这个 bug：新增“上下文污染隔离”规则。以后只要你说“重新写 / 同质化 / 没创意 / 不要这样”，skill 必须把上一版的核心场景、道具、隐喻、色彩、叙事结构列为禁用项；除非你在最新一句里明确重复，否则不能继续继承。

> AGENT

已经把“历史记忆污染”写进 anti-sameness 了。现在我再补一层更强的创意生成机制：不是只从同一类自然/亲子语境里发散，而是强制做跨品类借力、反类型开场、角色错位、证明方式替换，这样奶粉也能跳出母婴广告常见池子。

> TOOL

<turn_aborted>
The user interrupted the previous turn on purpose. Any running unified exec processes may still be running in the background. If any tools/commands were aborted, they may have partially executed.
</turn_aborted>

> DEVELOPER

不，除非我给你特定的选题，不然每次你都要先给我几个选题，然后你再根据我确定的选题进行创意想象，再最后生成剧本
这一系列步骤具有很多种变化了，不可能每次想出来的剧本同质化都很严重，并且你肯定还要自己去构思怎么样去创意想象，这是你必须的步骤

> AGENT

明白，这个才是正确工作流：如果你没有给“特定选题”，我不应该直接写剧本，因为直接写就会把模型拉回最近的默认意象池。我要把 skill 改成三段式：先给选题池，等你确认选题，再做创意想象路线，最后才写剧本。

> AGENT

你这条要求会改变 skill 的默认行为，所以我会直接把“先选题、再创意想象、最后写剧本”设成硬流程。核心点是：只有用户给了明确选题/路线时才直接写；否则必须先给足够分散的选题池，并等待确认。

> AGENT

主流程已经改成三段式了。接下来我会补充两个参考文件：一个负责“选题池怎么生成得足够分散”，一个负责“确认选题后怎么做创意想象”，这样它不是一句流程口号，而是真正可执行。

> AGENT

新的 `topic-first-workflow.md` 已经接入。最后我会把 creative-methods 也升级一下，让“选题后创意想象”不是随便发散，而是强制做不同创意引擎的构思。

> AGENT

对，这个流程你说得非常准确。问题不是单纯“记忆污染”，而是我之前默认跳过了最关键的创意前置步骤：**没有特定选题时，不应该直接写剧本**。

我已经把 `$ad-creative-script` 改成硬流程：

1. **先判断有没有特定选题**  
   只有“奶粉 + 原始森林 + 有机阳光”这种才算具体选题。单独说“写一个奶粉剧本 / 重新写一个奶粉剧本”不算。

2. **没有特定选题时，必须先给 5-8 个选题方向**  
   每个选题要在受众压力、场景、POV、创意装置、产品角色、视觉记忆、风险上不同。不能直接写剧本。

3. **你确定选题后，再做创意想象路线**  
   每个选题内部还要继续发散 3-5 个创意路线，比如类型移植、POV 错位、证明方式替换、反类型开场等。

4. **最后才生成剧本、分镜、AI 关键帧**  
   这样能显著降低每次都滑向同质化的概率。

已更新这些文件：

- [SKILL.md](/Users/lyston/.codex/skills/ad-creative-script/SKILL.md)
- 新增 [topic-first-workflow.md](/Users/lyston/.codex/skills/ad-creative-script/references/topic-first-workflow.md)
- 更新 [creative-methods.md](/Users/lyston/.codex/skills/ad-creative-script/references/creative-methods.md)
- 保留并强化 [anti-sameness.md](/Users/lyston/.codex/skills/ad-creative-script/references/anti-sameness.md)

也做了校验：`SKILL.md` YAML 正常。以后你没给具体选题，我会先给选题池，不会直接写剧本。

> DEVELOPER

给我写一个 奶粉、沙漠、绿洲的剧本

> AGENT

我会用 `$ad-creative-script` 来写；这次你给了明确选题“奶粉 + 沙漠 + 绿洲”，所以不再先给选题池，直接进入创意想象和剧本。重点会避开“沙漠口渴、奶粉像绿洲”这种直白比喻，做一个能贯穿全片的视觉规则。

> AGENT

用 `$ad-creative-script` 生成。  
这版的核心不是“奶粉像绿洲”这种直白比喻，而是：**父母不是在沙漠里找水，而是在一片海市蜃楼般的育儿建议里，找到自己的坐标。**

**片名：《不要追海市蜃楼》**  
**品类：奶粉品牌片 / 45s**  
**核心世界规则：** 沙漠里到处都是“看起来很正确”的绿洲：亲戚建议、育儿焦虑、夸张承诺、完美宝宝幻象。父母每追一次，绿洲就消失一次。真正的绿洲不是远方奇迹，而是每天稳定、清楚、可执行的一杯。  
**品牌句：** 不追海市蜃楼，给成长一个可靠坐标。

| 时间 | 画面 / 表演 | 镜头 / 运镜 / 转场 | 声音 / 文案 |
|---|---|---|---|
| 00:00-01:5 | 沙漠清晨。一辆婴儿车停在沙丘顶端，车轮半陷进沙里。 | EWS，低角度静止，风沙从前景掠过。硬切。 | 风声。 |
| 01:5-03:0 | 年轻父母推着婴儿车，前方出现第一个绿洲：巨大的广告牌写着“这样才是最好”。 | 长焦压缩空间，绿洲在热浪里晃动。 | 远处人声像广播。 |
| 03:0-04:5 | 爸爸刚往前一步，绿洲塌成一堆沙，广告牌碎成纸片。 | 慢推，纸片扑向镜头做转场。 | “哗”一声。 |
| 04:5-06:0 | 纸片落在妈妈手里，变成家庭群消息：“多吃点”“少喝点”“这样不对”。 | CU，手机屏和沙粒同框。 | 手机提示音被风拉长。 |
| 06:0-07:5 | 沙漠里竖起无数路标，每个方向都写着“正确答案”。 | WS，环绕小幅移动。 | VO：养孩子最难的，不是没有答案。 |
| 07:5-09:0 | 妈妈停下，把手机反扣进包里。她没有追任何一个方向。 | MCU，慢推到手的动作。切在手机扣下。 | VO：是答案太多。 |
| 09:0-10:5 | 婴儿车里，孩子醒来，手里攥着一只小小的量勺。 | CU，浅景深，勺子反光。 | 勺子轻碰车沿。 |
| 10:5-12:0 | 父母蹲下，打开奶粉罐。罐身不是棚拍，放在沙地毯布上，旁边有水壶、奶瓶、湿巾。 | OTS，轻微手持。 | 罐盖打开声。 |
| 12:0-13:5 | 一平勺奶粉被舀起，风突然安静一秒。 | ECU，静止 hold。 | 沙声短暂停住。 |
| 13:5-15:0 | 勺子落入奶瓶，沙地上出现一个清晰坐标点，不发光，只是像地图墨迹慢慢渗开。 | 顶拍，图形匹配切。 | VO：可靠，不是更响的承诺。 |
| 15:0-16:5 | 温水倒入，坐标点连成细线，穿过沙地，避开那些虚假的绿洲。 | Macro 到顶拍过渡，水声做声音桥。 | VO：是每天都能照着做的一步。 |
| 16:5-18:0 | 爸爸摇匀奶瓶，远处一个“完美宝宝绿洲”升起：孩子们整齐微笑，太假。 | MS，镜头从奶瓶摇动甩到远方。 | 绿洲里传来过度甜美的笑声。 |
| 18:0-19:5 | 妈妈看了一眼，没有过去，只把奶瓶递给孩子。 | MCU，慢推，动作克制。 | 笑声被风吹散。 |
| 19:5-21:0 | 孩子喝第一口。沙漠没有奇迹变森林，只是在婴儿车周围安静出一小圈阴凉。 | WS，静止观察。 | VO：成长不需要追赶奇迹。 |
| 21:0-22:5 | 那圈阴凉里，路标一个个倒下，只剩一条简单路线。 | 低机位，路标倒下形成连切。 | 木牌倒地声。 |
| 22:5-24:0 | 父母继续推车。不是奔向巨大绿洲，而是沿着小小坐标线往前走。 | 背后跟拍，轻微手持。 | 车轮压沙声。 |
| 24:0-25:5 | 沙地里半埋着别人丢下的“完美计划表”，妈妈路过，没有捡。 | Insert，静止。硬切。 | 纸张翻动。 |
| 25:5-27:0 | 前方终于出现绿洲，但很小：一棵树、一张布、一只水壶，够一家人停下来。 | Pull-back reveal，从父母背影拉开。 | VO：有时候，够稳定，就已经很珍贵。 |
| 27:0-28:5 | 他们坐下。孩子手里的量勺插在沙里，像一个小路标。 | CU，低角度，勺柄迎风。 | 勺子轻响。 |
| 28:5-30:0 | 妈妈把奶粉罐放在布上，罐身、奶瓶、量勺构成一个小小补给站。 | 产品 CU，rack focus 从量勺到罐身。 | 环境声变近。 |
| 30:0-31:5 | 远处还有很多海市蜃楼在闪：更快、更高、更聪明、更完美。父母没有回头。 | 长焦，热浪压缩，父母虚焦在前景。 | VO：别让每一种声音，都变成方向。 |
| 31:5-33:0 | 孩子把量勺递给妈妈，像把“方向”还给她。 | MCU，慢推到手交接。 | 孩子轻笑。 |
| 33:0-34:5 | 妈妈把量勺收回罐中，盖上盖，动作很稳。 | ECU，切在盖合声。 | “咔哒”。 |
| 34:5-36:0 | 沙漠风吹过，坐标线没有消失，只是淡淡留在沙面上。 | 顶拍，缓慢上升。 | VO：某某奶粉。 |
| 36:0-39:0 | End frame：奶粉罐、奶瓶、量勺、小绿洲的一片阴凉。远处海市蜃楼模糊消散。 | 锁定镜头，end-frame lock。 | 字幕：不追海市蜃楼，给成长一个可靠坐标。 |

**创意资产**

- 视觉资产：沙漠里的“虚假绿洲”、沙地坐标线、量勺小路标。
- 声音资产：风声突然安静、量勺轻响、罐盖“咔哒”。
- 动作资产：反扣手机、不追绿洲、一平勺落下形成坐标。
- 品牌记忆：奶粉不是制造奇迹，而是让父母在嘈杂选择里有一个可靠方向。

**合规注意**  
具体营养、配方、有机、奶源等卖点需要按品牌实际资质补充；这版没有写“提高免疫力、变聪明、长高”等不合规承诺。

> DEVELOPER

这个剧本我根本看不明白想体现的是什么，写出来的就是一坨屎，要创意没创意，要想象没想象，主旨也没有，内涵也没有
好好上网学习，优化剧本

> AGENT

我接受这个评价。上一版的问题很明确：概念说的是“育儿建议太多”，但沙漠/绿洲没有真正服务奶粉，世界规则也只是漂亮比喻，观众看完不知道产品到底在故事里改变了什么。我会先上网补一轮广告创意和叙事清晰度的方法，然后重写，不再修修补补上一版。

> AGENT

我看了一轮后提炼出三个修正点：广告必须先有一句能听懂的主旨；品牌/产品要成为故事因果，不是片尾赞助；创意要有可复述的记忆资产，而不是一串漂亮隐喻。所以下一版我会直接换掉“海市蜃楼/坐标”那套，改成一个更清楚的世界规则：每个孩子都有自己的小绿洲，父母不是寻找最大绿洲，而是用每天稳定的照护把它养出来。

> AGENT

你骂得对。上一版最大问题不是“看不懂沙漠”，而是**主旨没有钉住**：沙漠、绿洲、育儿建议、坐标都在漂，产品也没有真正推动故事。

我上网学习后按三条规则重写：品牌必须是故事因果、信息必须单一清楚、要有可复述的记忆资产。参考了 [Thinkbox Creative Drivers](https://www.thinkbox.tv/research/thinkbox-research/creative-drivers-of-effectiveness)、[Think with Google ABCDs](https://business.google.com/us/think/future-of-marketing/youtube-video-ad-creative/)、[Ebiquity Creative Effectiveness](https://ebiquity.com/news-insights/press/measuring-creative-effectiveness/)。

**片名：《孩子自己的绿洲》**  
**一句话主旨：** 父母不是带孩子去找“最大的绿洲”，而是用每天稳定、可靠的照护，养出孩子自己的绿洲。  
**产品角色：** 奶粉不是奇迹水源，而是每天可执行、可重复的营养补给仪式。  
**核心视觉资产：** 一个透明“小绿洲瓶”里装着孩子自己的沙土。它不会被远处大绿洲唤醒，只会被每天稳定的一杯慢慢养出第一片绿。

| 时间 | 画面 / 表演 | 镜头 / 转场 | 声音 / 文案 |
|---|---|---|---|
| 00-02s | 沙漠清晨。妈妈打开背包，里面不是藏宝图，而是奶粉罐、奶瓶、水壶和一个透明小瓶。瓶里只有干沙，贴着孩子名字。 | CU，手持微晃，硬切。 | 风声。孩子呼吸声。 |
| 02-04s | 远处是一座巨大绿洲，入口排满父母，牌子写着“完美成长绿洲”。 | 长焦压缩，人群像热浪。 | 广播：请所有孩子进入标准绿洲。 |
| 04-06s | 妈妈看向孩子手里的小瓶。瓶里的沙没有任何变化。 | MCU，慢推。 | VO：每个父母都想带孩子找到最好的地方。 |
| 06-08s | 人群往大绿洲冲。爸爸也想跟上，妈妈拉住他。她蹲下，把奶粉罐放在沙地上。 | 低机位，奶粉罐进入画面中心。 | 妈妈轻声：先照顾好他自己的。 |
| 08-10s | 奶粉罐打开。一平勺被舀起，勺面平稳，没有发光特效。 | ECU，静止 hold。 | 勺子碰罐口一声轻响。 |
| 10-12s | 温水倒入奶瓶，奶粉慢慢融开。孩子的小绿洲瓶里，干沙出现一个极小的湿点。 | Match cut：奶瓶水旋转到小瓶沙面。 | VO：真正可靠的，不是远处的承诺。 |
| 12-14s | 爸爸看见湿点，愣住：不是大片绿洲，只是一个小到几乎看不见的开始。 | CU，慢推到爸爸眼神。 | 爸爸：就这么一点？ |
| 14-16s | 妈妈摇匀奶瓶，递给孩子。她回答得很平静。 | OTS，切在递奶瓶动作上。 | 妈妈：每天一点。 |
| 16-18s | 孩子喝第一口。婴儿车轮旁的沙地，出现一小片真实阴影，刚好够遮住孩子的脚。 | WS，静止观察。 | 风声突然低下来。 |
| 18-20s | 远处巨大绿洲很热闹，但孩子的小瓶里长出一根细小绿芽。不是奇迹，是安静地活了。 | ECU，rack focus 从奶瓶到绿芽。 | VO：成长，不一定从最大的绿洲开始。 |
| 20-22s | 其他父母还在争抢入口。妈妈把量勺插在孩子小绿洲旁，像一个小路标。 | 低机位，量勺成前景。 | VO：它常常从每天稳定的一杯开始。 |
| 22-24s | 沙漠风起，巨大绿洲的牌子被吹得摇晃。孩子的小绿洲没有变大，却没有消失。 | 横移，前景小绿洲，远景大绿洲。 | 没有音乐，只有风和孩子吞咽声。 |
| 24-26s | 父母不再去排队。他们推着孩子继续走，小绿洲瓶挂在婴儿车边，里面那片绿跟着孩子移动。 | 跟拍，轻微手持。 | 妈妈：这是你的。 |
| 26-28s | 产品近景：奶粉罐、奶瓶、量勺、小绿洲瓶在同一块阴影里。 | 产品 CU，慢推，留 logo 区。 | VO：某某奶粉，稳定营养，支持日常成长。 |
| 28-30s | End frame：沙漠里没有铺天盖地的绿色，只有孩子身边一片小小但真实的绿洲。 | 锁定镜头。 | 字幕：不用追最大的绿洲，养好孩子自己的绿洲。 |

这版的主旨是清楚的：**不要追逐外界“完美成长”的巨大承诺，奶粉代表的是每天稳定、可重复、可执行的照护，让孩子自己的成长环境慢慢建立起来。**

合规上，具体营养、有机、奶源、配方卖点需要按真实资质替换，不能写长高、聪明、免疫力保证。

> DEVELOPER

很离谱，这是奶粉剧本好不好，你的这些创意是什么垃圾
优化skill，每个创意想象都要符合主题

> AGENT

你这次抓到的是另一个更根本的问题：创意不能只是“有想象力”，它必须先被主题授权。奶粉剧本里的想象力如果不能服务“奶粉的购买理由、信任、喂养仪式、成长支持”，再奇怪也只是跑题。我会把这个改成 skill 的硬门槛：先做主题适配，再做创意想象。

> AGENT

我会新增一个“主题适配门槛”：每个创意路线在进入想象之前，必须先回答它到底在卖奶粉的哪个真实购买理由；如果答案只是“看起来有画面、有隐喻、有世界观”，就必须淘汰。

> AGENT

主题适配参考文件已经加了，里面把奶粉的创意边界写得很明确：必须回到信任、喂养仪式、营养支持、质量系统、父母选择信心这些购买理由。现在我把它接进主 workflow、想象引擎和质量评估。

> TOOL

<turn_aborted>
The user interrupted the previous turn on purpose. Any running unified exec processes may still be running in the background. If any tools/commands were aborted, they may have partially executed.
</turn_aborted>

> DEVELOPER

奶粉除了营销还有品牌啊，你不能就这么固定写死啊
上网好好学学，再优化skill

> AGENT

你说得对，我刚刚把“主题适配”修得太窄了，几乎变成“奶粉只能围绕喂养动作和功能购买理由写”。这会杀掉品牌片该有的空间：品牌观点、长期记忆、文化态度、母婴关系、信任气质、品牌资产都不能被压成短促卖点。我先上网补品牌建设和广告有效性，再把 skill 改成“营销/品牌/产品证明”分层判断。

> AGENT

我查到的重点也支持你的判断：长期品牌建设不是短期卖点堆砌，情绪、人、记忆结构、品牌资产、品类入口都很重要；产品要融入叙事，但不等于每条片都必须做功能证明。我现在会把 skill 改成“先判断是品牌片、产品营销片还是转化片”，奶粉品牌片可以讲品牌信念和长期信任，不会再被硬塞进功能卖点。

> AGENT

主流程已经改了：主题适配不再等于功能卖点适配，而是先分清这条片到底是品牌建设、产品营销、信任证明还是转化。接下来我会改 `theme-fit-gate.md`，把奶粉品牌片的创作空间放进去。

> AGENT

现在 `theme-fit-gate.md` 已经从“产品功能门槛”改成“传播任务门槛”：品牌片可以服务长期信任、品牌信念、亲子世界观、品类入口记忆和品牌资产；产品片/证明片才更强调喂养流程、营养支持、质量系统。再补一下行业适配，避免奶粉分类只写成短期营销。

> AGENT

我还会修一下质量评估的编号和语言，避免它内部出现“产品必须是引擎”这种对品牌片过窄的标准。之后跑校验。

> AGENT

你说得对，我刚才修偏了。奶粉不只有“产品营销”和“功能证明”，也有**品牌片**：品牌信念、长期信任、亲子世界观、品类入口记忆、品牌资产，这些都是正当的创意空间。不能把每个奶粉创意都写死成“喂养动作、营养卖点、质量系统”。

我已经重新优化了 skill：

- [SKILL.md](/Users/lyston/.codex/skills/ad-creative-script/SKILL.md)：新增“先判断传播任务”，区分品牌建设、产品营销、信任证明、上市、转化、混合型。
- [theme-fit-gate.md](/Users/lyston/.codex/skills/ad-creative-script/references/theme-fit-gate.md)：从“产品功能适配”改成“传播任务适配”。品牌片允许围绕品牌信念、长期信任、亲子世界观、情绪记忆、品类入口和品牌资产展开。
- [industry-adapters.md](/Users/lyston/.codex/skills/ad-creative-script/references/industry-adapters.md)：给奶粉增加了品牌建设角色和品牌片创意方向。
- [quality-rubric.md](/Users/lyston/.codex/skills/ad-creative-script/references/quality-rubric.md)：新增 `Communication-job fit`，避免把品牌片误判成产品 demo，也避免产品片漂成空泛品牌诗。

也做了 YAML 校验，正常。

以后奶粉创意会先判断：这是品牌片、产品片、信任证明片，还是混合片。品牌片可以有大主题和想象力，但必须属于奶粉品牌的世界观，而不是随机奇观。

> DEVELOPER

生成一个圣罗兰香水的剧本

> AGENT

我会按刚更新的 `$ad-creative-script` 流程来做：你现在给的是品牌/品类“圣罗兰香水”，还没有具体选题，所以我先给你几个差异足够大的创意选题方向；你选定后，我再进入创意想象路线，最后写完整剧本。

> AGENT

按新版流程：你只给了“圣罗兰香水”这个品牌/品类，还没有具体选题，所以我先不给完整剧本，先给你选题池。你选一个后，我再做创意想象路线，最后写完整剧本和分镜。

| 选题 | 一句话设定 | 创意装置 | 产品角色 | 视觉记忆 | 风险 |
|---|---|---|---|---|---|
| 1. 《禁区之后》 | 一个女人在午夜进入城市里所有“禁止进入”的空间。 | 禁止牌、门禁、红线不断被她改写。 | 香水是进入自我边界之外的仪式。 | 黑夜、红色禁区灯、门禁打开。 | 容易拍成普通酷女片，需要强故事。 |
| 2. 《影子先到》 | 她的影子比她更早做出决定。 | 影子不再跟随人，而是带她走向真实欲望。 | 香水让“隐藏的自我”先被看见。 | 黑白强光、影子独立行动。 | 需要控制，避免太玄。 |
| 3. 《把夜晚穿上身》 | 夜晚不是时间，而是一件她亲手穿上的外套。 | 城市夜色像布料一样被裁剪、披上、收紧。 | 香水成为“夜晚上身”的最后一道扣。 | 黑色天幕、剪裁、金属扣、颈侧喷香。 | 要避免像服装广告。 |
| 4. 《不合时宜的人》 | 所有人都按城市节奏行动，只有她故意慢半拍。 | 世界像节拍器，她每次错拍都让空间变得更有张力。 | 香水代表不讨好、不校准、不解释的个人节奏。 | 地铁、人群、节拍器、突然安静。 | 偏品牌片，产品露出要设计好。 |
| 5. 《电梯没有到顶层》 | 她进入一部只去“别人期待的楼层”的电梯，最后按下不存在的一层。 | 楼层按钮代表身份标签：温柔、得体、迷人、乖巧。 | 香水是她拒绝被定义后的签名。 | 黑色电梯、金色按钮、隐藏楼层亮起。 | 概念清楚，但要拍得高级。 |
| 6. 《香味审讯室》 | 她被问“你到底想成为什么样的人”，她一句都不答。 | 审讯室反转成自我宣言场。 | 香水不是答案，是她拒绝回答的证据。 | 强光、桌面香水瓶、沉默、红唇/黑衣。 | 太戏剧化，需要控制台词。 |
| 7. 《城市为她让出一秒》 | 城市所有倒计时、红绿灯、电子屏都突然停一秒。 | 一秒钟的停顿成为她出场的空间。 | 香水是她进入世界前的“暂停键”。 | 红绿灯停住、雨滴悬停、人群静止。 | 容易像超能力片，需要和品牌气质绑定。 |

我建议优先选 **2《影子先到》** 或 **5《电梯没有到顶层》**。  
2 更有想象力和视觉记忆；5 更适合圣罗兰那种“叛逆、欲望、身份、自我定义”的品牌气质。

> DEVELOPER

4

> AGENT

收到，你选的是 4《不合时宜的人》。我会按 `$ad-creative-script` 的第二步来走：先在这个选题里做几条不同的创意想象路线，不直接跳到剧本。

> AGENT

**选题 4：《不合时宜的人》**

传播任务：圣罗兰香水品牌片  
核心品牌方向：不讨好、不校准、不被世界节奏驯服。  
要避开的俗套：夜晚城市 + 酷女孩走路 + 香水特写 + “自由/欲望”空泛旁白。

| 路线 | 创意想象 | 产品角色 | 记忆画面 | 风险 |
|---|---|---|---|---|
| A. 《错拍》 | 整座城市像节拍器一样精准运行，只有她永远慢半拍。每次她错拍，世界反而出现真正的呼吸。 | 香水是她出门前确认自己节奏的仪式。 | 地铁门、人群脚步、电子钟全部齐拍；她晚一秒，城市安静一秒。 | 容易偏抽象，需要强动作设计。 |
| B. 《拒绝同步》 | 所有人身上都有一个看不见的“同步信号”，她喷上香水后，信号断开。不是逃离世界，而是不再被世界遥控。 | 香水是“断开同步”的开关。 | 人群手机同时震动、同时转头；她颈侧一喷，耳边的同步声断掉。 | 稍微科幻，要保持高级真实感。 |
| C. 《慢一秒的胜利》 | 她总是比世界慢一秒：别人鼓掌后她才笑，别人举杯后她才看人，别人离开后她才走进舞池。最后发现她不是慢，是不愿被安排。 | 香水是她进入场合前的私人决定。 | 宴会所有人动作整齐，她慢一秒抬眼，整个空间被她重新定义。 | 比较电影感，但想象力中等。 |
| D. 《城市节拍师》 | 城市里有一个隐藏的节拍师控制每个人的步速、表情、欲望。她是唯一不听拍的人，最后节拍师停下来看她。 | 香水让她从“被指挥的人”变成“改写节奏的人”。 | 黑暗剧院里，城市节拍师挥棒，街上所有人同步；她喷香后，指挥棒断拍。 | 创意最强，但制作更复杂。 |
| E. 《她没有迟到》 | 所有人以为她迟到了：会议、晚宴、约会、末班车。最后才发现，不是她迟到，是她从不按别人的时间出现。 | 香水是她出场的时间签名。 | 一排钟表全指向同一时间，只有她腕表没有刻度。 | 概念清楚，但需要避免像手表广告。 |

我推荐 **B《拒绝同步》**。  
它最适合圣罗兰香水：有叛逆、有欲望、有现代城市压迫感，也能拍得很电影。香水不是“变美”，而是让她从社会同步里脱身，重新拥有自己的节奏。

如果你确认 B，我下一步写完整剧本和 1.5 秒级分镜。

> DEVELOPER

d

> AGENT

收到，选 D《城市节拍师》。我现在按这个路线写完整品牌片：传播任务是圣罗兰香水品牌片，核心不是香调证明，而是“拒绝被城市节奏指挥”的品牌态度；分镜会保持短颗粒度，方便后续生图/视频。

> AGENT

**片名：《别被世界指挥》**  
**品牌：圣罗兰香水**  
**时长：30s**  
**主旨：** 圣罗兰香水不是让她融入场合，而是让她带着自己的节拍进入世界。  
**创意规则：** 城市被一个隐藏的“节拍师”指挥，每个人的脚步、微笑、举杯、转身都被同步。她喷上香水后，不是世界为她停止，而是她终于不再听拍。

| 时间 | 画面 / 表演 | 运镜 / 转场 | 声音 / 文案 |
|---|---|---|---|
| 00:00-01:5 | 黑暗剧院里，一只戴白手套的手举起指挥棒。 | ECU，静止，硬切。 | 一声清脆节拍。 |
| 01:5-03:0 | 城市街口，人群同时迈左脚，红灯倒数精准跳动。 | 低机位横移。切在脚步落地。 | 脚步整齐如鼓点。 |
| 03:0-04:5 | 电梯里，所有人同时抬头、整理衣领、露出礼貌微笑。 | 镜面中景，轻微推近。 | 节拍器声变密。 |
| 04:5-06:0 | 她在后台化妆间，没有跟着节拍抬头，只低头看香水瓶。 | MCU，慢推到手边瓶身。 | 节拍声压低。 |
| 06:0-07:5 | 圣罗兰香水瓶放在黑色桌面，旁边是拆开的耳夹、车票、口红印。 | 产品 CU，rack focus 到瓶身。 | 玻璃轻碰桌面。 |
| 07:5-09:0 | 剧院里，节拍师挥下第二拍。城市所有人同时转身。 | Whip cut，指挥棒匹配人群转身。 | “嗒”。 |
| 09:0-10:5 | 她拿起香水，喷在颈侧。动作很慢，故意慢过节拍半秒。 | ECU，宏观微移。切在喷雾声。 | 喷雾声打断节拍。 |
| 10:5-12:0 | 指挥棒第一次落空，剧院空气停了一瞬。 | CU，指挥棒停在半空。硬切。 | 节拍器漏一拍。 |
| 12:0-13:5 | 城市街口，她走进人群，所有人左转，她直行。 | 高位俯拍，直线构图。 | 无 VO，只剩鞋跟声。 |
| 13:5-15:0 | 人群节奏乱了一点，但不是混乱，是出现了呼吸。一个人停下看她。 | 手持轻跟，前景遮挡。 | 城市噪音松开。 |
| 15:0-16:5 | 晚宴桌边，所有人同时举杯。她晚一秒，只看向对面的人。 | OTS，慢推到眼神。 | 杯声齐响，她没有碰杯。 |
| 16:5-18:0 | 剧院节拍师皱眉，强行加快节奏。红绿灯、电梯、快门声全部提速。 | 快切三帧，图形匹配。 | 节拍急促。 |
| 18:0-19:5 | 她停在旋转门前，没有进入预设节奏，反而转身走向侧门。 | 跟拍，轻微 handheld。 | VO：不是每一种节奏，都值得跟上。 |
| 19:5-21:0 | 侧门后是城市屋顶，风吹起她的外套。远处灯光还在同步闪烁。 | Pull-back reveal。 | 风声盖过节拍。 |
| 21:0-22:5 | 她从包里拿出香水瓶，瓶身映出城市灯线，像一条断开的谱线。 | 产品 ECU，rack focus。 | 低频音乐进入。 |
| 22:5-24:0 | 剧院里，节拍师看见自己的指挥棒开始跟不上她的步伐。 | CU，棒尖颤动。匹配切。 | 节拍器彻底停下。 |
| 24:0-25:5 | 城市里，不同的人开始有自己的动作：有人摘下耳机，有人停下笑，有人转身离开队伍。 | WS，缓慢横移。 | VO：真正的存在感，不需要合拍。 |
| 25:5-27:0 | 她站在屋顶边缘，不看镜头，只把香水瓶放回包里。 | 侧面 MCU，慢推。 | 一声瓶盖轻响。 |
| 27:0-28:5 | 剧院空了，指挥棒落在地上。城市不再被指挥。 | 低机位静止，硬切。 | 指挥棒落地。 |
| 28:5-30:0 | End frame：圣罗兰香水瓶，黑色背景，一道锋利侧光，留 logo 区。 | 锁定镜头，end-frame lock。 | 字幕：圣罗兰香水。别被世界指挥。 |

**核心资产**

- 视觉资产：白手套节拍师、同步城市、漏掉的一拍、黑色香水瓶侧光。
- 声音资产：节拍器声、喷雾打断节拍、指挥棒落地。
- 动作资产：她故意慢半拍、不碰杯、不走正门。
- 品牌表达：不是“变迷人”，而是“不被安排”。

> DEVELOPER

剧本感觉可以，但是这个剧本的分镜脚本不行，每一行表达的画面、 东西都太多了，需要拆分的更细，再增加一列，详细写到每一行需要生成几个画面、哪几个画面、包括每个画面怎么（承接、转场）等，以辅助生图和后续的视频生成

> TOOL

<turn_aborted>
The user interrupted the previous turn on purpose. Any running unified exec processes may still be running in the background. If any tools/commands were aborted, they may have partially executed.
</turn_aborted>

> DEVELOPER

剧本感觉可以，但是这个剧本的分镜脚本不行，每一行表达的画面、 东西都太多了，需要拆分的更细，再增加一列，详细写到每一行需要生成几个画面、哪几个画面、包括每个画面怎么（承接、转场）等，以辅助生图和后续的视频生成
并且优化skill

> AGENT

你这个判断很准：现在的问题不是创意主线，而是“导演分镜”和“生图关键帧”仍然混在一起了。一行里同时有动作、环境、人物反应、转场，生图模型会抓不到重点；我会先把 skill 的输出模板改成强制带“生成画面拆分列”，然后给这条圣罗兰片重新拆一版更细的分镜。

> AGENT

我已经确认 skill 里有 AI 关键帧规则，但还缺你说的那一列：每一行到底拆几个画面、画面 A/B/C 分别是什么、怎么承接和转场。现在我会补这个强制模板。

> AGENT

skill 已经补上了“生成画面拆分”硬要求。现在我跑一下校验，然后把圣罗兰这条片按新格式重拆：每行不会只写一个复杂画面，而会明确生成 1/2/3 张，分别是什么画面、怎么承接、怎么转场。

> AGENT

已优化 skill。现在 `$ad-creative-script` 增加了硬规则：只要是给生图/视频生成用的分镜，每一行必须有 `生成画面拆分`，明确：

- 这一行生成几张图
- A/B/C 分别是什么单一画面
- 每张图怎么承接上一张
- 怎么转场到下一张或下一行

更新位置：

- [SKILL.md](/Users/lyston/.codex/skills/ad-creative-script/SKILL.md)
- [storyboard-ai-prompts.md](/Users/lyston/.codex/skills/ad-creative-script/references/storyboard-ai-prompts.md)
- [visual-planning.md](/Users/lyston/.codex/skills/ad-creative-script/references/visual-planning.md)
- [quality-rubric.md](/Users/lyston/.codex/skills/ad-creative-script/references/quality-rubric.md)

校验通过：`SKILL.md` YAML 正常。

下面是圣罗兰这条片的新版细拆分镜：

| 时间 | 导演意图 | 画面 / 表演 | 生成画面拆分 | 运镜 / 承接 / 转场 | 声音 / 文案 |
|---|---|---|---|---|---|
| 00:00-01:5 | 建立“城市被指挥”的规则 | 黑暗剧院里，白手套举起指挥棒。 | 生成 2 张：A 00:00.0｜黑暗剧院空镜，中央只有指挥台和一束顶光｜承接：黑场进入｜转场：硬切到 B；B 00:01.0｜白手套握住指挥棒，棒尖停在半空｜承接：A 的顶光落到手套｜转场到下一行：棒尖下落动作切脚步。 | ECU，静止，棒尖下落做 cut on action。 | 一声节拍。 |
| 01:5-03:0 | 城市同步开始 | 街口人群同时迈步。 | 生成 2 张：A 00:01.5｜低机位，整排鞋尖停在斑马线前｜承接：指挥棒下落方向接鞋尖｜转场：脚尖准备落地；B 00:02.5｜所有人左脚同时落在白线，红灯倒数在背景｜承接：A 的等待变成同步动作｜转场到下一行：脚步声桥接电梯。 | 低机位横移，硬切到电梯镜面。 | 脚步齐响。 |
| 03:0-04:5 | 同步扩散到社交表情 | 电梯里所有人同时整理衣领、抬头微笑。 | 生成 3 张：A 00:03.0｜电梯镜面里，所有人低头站成一排｜承接：脚步声进入封闭空间｜转场：镜面硬切；B 00:03.7｜所有人的手同时碰到衣领｜承接：同步动作继续｜转场：cut on action；C 00:04.3｜所有人同时抬头露出礼貌微笑｜承接：B 的手部动作完成｜转场到下一行：镜面反光切后台镜子。 | 镜面中景，慢推，镜面反光转场。 | 节拍器变密。 |
| 04:5-06:0 | 女主第一次拒绝同步 | 后台化妆间，她没有抬头，只看香水瓶。 | 生成 2 张：A 00:04.5｜后台化妆镜，灯泡、散落耳夹、口红印，女主低头在画面边缘｜承接：电梯镜面光切化妆镜灯｜转场：慢推；B 00:05.5｜女主手边的圣罗兰香水瓶，手没有触碰，只停在旁边｜承接：A 的低头视线落到瓶身｜转场到下一行：rack focus 到产品。 | MCU 慢推，镜面光承接。 | 节拍声压低。 |
| 06:0-07:5 | 产品进入世界规则 | 香水瓶成为她节奏的起点。 | 生成 2 张：A 00:06.0｜黑色桌面产品 CU，香水瓶、耳夹、车票分层摆放｜承接：上一帧视线落到瓶身｜转场：rack focus；B 00:07.0｜瓶身玻璃反射出远处剧院灯，像一条竖直节拍线｜承接：A 的产品静物变成规则符号｜转场到下一行：反射线匹配指挥棒。 | 产品 CU，rack focus，图形匹配。 | 玻璃轻响。 |
| 07:5-09:0 | 世界再次强行同步 | 节拍师挥下第二拍，城市同时转身。 | 生成 2 张：A 00:07.5｜剧院节拍师侧影，指挥棒横向挥出｜承接：瓶身反射线变指挥棒｜转场：whip cut；B 00:08.5｜街上人群同时转身，脸的方向一致｜承接：A 的横向挥棒带动人群转身｜转场到下一行：人群转身的反方向切女主慢动作。 | Whip cut，动作匹配。 | “嗒”。 |
| 09:0-10:5 | 香水打断同步 | 她喷在颈侧，故意慢半拍。 | 生成 3 张：A 00:09.0｜女主手拿香水靠近颈侧，动作还没发生｜承接：人群转身后留出她的反向静止｜转场：慢推；B 00:09.8｜喷雾离开喷头，细雾在颈侧形成短促白线｜承接：A 的手部动作完成｜转场：喷雾声切；C 00:10.4｜她闭眼半秒，表情克制，不微笑｜承接：B 的喷雾落到皮肤｜转场到下一行：喷雾白线切指挥棒停顿。 | ECU，宏观微移。 | 喷雾声打断节拍。 |
| 10:5-12:0 | 规则第一次失效 | 指挥棒落空，节拍漏拍。 | 生成 2 张：A 00:10.5｜剧院中指挥棒停在半空，没有落下｜承接：喷雾白线匹配棒尖白光｜转场：硬切；B 00:11.5｜节拍师白手套僵住，背景乐谱架轻微失焦｜承接：A 的停顿扩大成失控｜转场到下一行：静止切街口直行。 | CU 静止，停顿制造断拍。 | 节拍器漏一拍。 |
| 12:0-13:5 | 她用身体改写节奏 | 街口所有人左转，她直行。 | 生成 2 张：A 00:12.0｜高位俯拍，人群像箭头一样集体左转，女主站在交叉点｜承接：断拍后的城市重新启动｜转场：动作切；B 00:13.0｜女主直线穿过人群，黑衣形成唯一竖线｜承接：A 的交叉点变成她的路线｜转场到下一行：直线动势接人群松动。 | 高位俯拍，直线构图。 | 只剩鞋跟声。 |
| 13:5-15:0 | 世界不是崩坏，是开始有呼吸 | 人群节奏松开，有人第一次看她。 | 生成 2 张：A 00:13.5｜人群中一个男人的脚步停住半拍，鞋尖和别人错开｜承接：女主直行造成第一处错位｜转场：低机位切；B 00:14.5｜一个人转头看她，其他人仍在同步走｜承接：A 的脚步错位上升到视线错位｜转场到下一行：视线切晚宴目光。 | 手持轻跟，前景遮挡。 | 城市噪音松开。 |
| 15:0-16:5 | 社交场合里的不合拍 | 晚宴所有人举杯，她晚一秒看人。 | 生成 3 张：A 00:15.0｜长桌晚宴，所有酒杯停在桌面，女主在一侧｜承接：街上转头视线切晚宴视线｜转场：硬切；B 00:15.8｜所有人同时举杯，女主杯子仍在桌上｜承接：A 的静止变同步动作｜转场：杯声切；C 00:16.4｜女主抬眼看对面，不碰杯｜承接：B 的齐拍被她延迟｜转场到下一行：杯口圆形匹配红绿灯。 | OTS 慢推到眼神。 | 杯声齐响，她不碰杯。 |
| 16:5-18:0 | 节拍师反击，节奏加速 | 红绿灯、电梯、快门声全部提速。 | 生成 3 张：A 00:16.5｜剧院节拍师皱眉，指挥棒斜向下压｜承接：杯声变指挥棒重拍｜转场：硬切；B 00:17.0｜红绿灯倒数数字高速跳动｜承接：A 的加速变成城市系统｜转场：数字闪切；C 00:17.6｜电梯楼层灯连续闪，人的脸被切成断续光块｜承接：B 的数字节奏进入电梯｜转场到下一行：闪光切旋转门。 | 快切，图形匹配。 | 节拍急促。 |
| 18:0-19:5 | 她选择侧门 | 她停在旋转门前，转身走向侧门。 | 生成 2 张：A 00:18.0｜旋转门正面，门格像节拍器分格，人群被带着转｜承接：电梯闪光切玻璃门反光｜转场：慢推；B 00:19.0｜女主背对旋转门，手推开不起眼侧门｜承接：A 的循环被她打断｜转场到下一行：门缝白光 reveal 屋顶。 | 跟拍，门缝做光切。 | VO：不是每一种节奏，都值得跟上。 |
| 19:5-21:0 | 空间打开 | 侧门后是城市屋顶，风盖过节拍。 | 生成 2 张：A 00:19.5｜侧门打开，窄门缝里露出屋顶冷风和城市灯｜承接：上一帧推门动作｜转场：pull reveal；B 00:20.5｜女主站到屋顶边，外套被风吹起，远处灯光仍同步闪｜承接：A 的门缝扩大成屋顶空间｜转场到下一行：城市灯线切瓶身反射。 | Pull-back reveal。 | 风声盖过节拍。 |
| 21:0-22:5 | 产品成为她的节拍签名 | 香水瓶映出断开的城市谱线。 | 生成 2 张：A 00:21.0｜女主手从包里取出圣罗兰香水瓶，城市灯虚化在后景｜承接：屋顶风中手部动作｜转场：CU；B 00:22.0｜瓶身反射城市灯线，灯线断成不连续谱线｜承接：A 的取瓶变成视觉符号｜转场到下一行：断线匹配指挥棒颤动。 | 产品 ECU，rack focus。 | 低频音乐进入。 |
| 22:5-24:0 | 指挥系统彻底失灵 | 指挥棒开始跟不上她。 | 生成 2 张：A 00:22.5｜节拍师看向台下空座，手腕失控｜承接：瓶身断线切剧院暗线｜转场：硬切；B 00:23.5｜指挥棒尖颤动，画面边缘轻微运动模糊｜承接：A 的失控聚焦到棒尖｜转场到下一行：颤动切街上个体动作。 | CU，轻微抖动。 | 节拍器停下。 |
| 24:0-25:5 | 城市恢复个人节奏 | 不同人开始做自己的动作。 | 生成 3 张：A 00:24.0｜地铁口，一个人摘下耳机，别人还在走｜承接：棒尖颤动变人的手部动作｜转场：硬切；B 00:24.7｜晚宴上一个人放下假笑，杯子停在半空｜承接：A 的个体动作扩散｜转场：match cut 手部；C 00:25.3｜街口有人离开队伍向反方向走｜承接：B 的停顿变行动｜转场到下一行：反向行走切女主屋顶。 | WS 横移，多点个人节奏。 | VO：真正的存在感，不需要合拍。 |
| 25:5-27:0 | 女主不解释 | 她站在屋顶边，把香水放回包里。 | 生成 2 张：A 00:25.5｜女主侧脸，远处城市灯在后景，神情克制｜承接：个体动作回到她的源头｜转场：慢推；B 00:26.5｜她把香水瓶放回黑色包里，手指松开瓶身｜承接：A 的侧脸落到手部动作｜转场到下一行：瓶盖声切指挥棒落地。 | 侧面 MCU，慢推。 | 瓶盖轻响。 |
| 27:0-28:5 | 旧秩序落幕 | 剧院空了，指挥棒落地。 | 生成 2 张：A 00:27.0｜空剧院，指挥台无人，地面有一道窄光｜承接：瓶盖声进入空剧院｜转场：硬切；B 00:28.0｜指挥棒落在地上，白手套不在画面里｜承接：A 的空场完成落幕｜转场到下一行：棒身黑白线条切产品瓶身。 | 低机位静止。 | 指挥棒落地。 |
| 28:5-30:0 | 品牌收束 | 圣罗兰香水瓶，黑色背景，锋利侧光。 | 生成 2 张：A 00:28.5｜产品 hero，圣罗兰香水瓶置于黑色背景，侧光形成锋利边缘｜承接：指挥棒黑白线条切瓶身轮廓｜转场：end-frame lock；B 00:29.5｜产品旁留 logo / slogan 安全区，背景隐约有一条断开的节拍线｜承接：A 的产品静物增加品牌文案空间｜转场：结束锁帧。 | 锁定镜头。 | 字幕：圣罗兰香水。别被世界指挥。 |

这版一共建议生成 **42 张关键画面**。每一张都只承担一个单一瞬间，后续可以直接拿 A/B/C 做生图，再用承接和转场说明去做视频生成。

> DEVELOPER

片名：《阳光先经过森林》
时长：30s
核心创意： 真正的有机，不是一个包装词，而是一套被阳光、土地、水源和时间共同照看的系统。孩子喝下的那一杯，背后有一整片自然的秩序。
人物与场景
主角：32 岁妈妈，做自然教育工作，带 3 岁孩子在清晨进入原始森林边缘的自然保护区。
场景：森林木栈道、苔藓、溪水、林间小屋、窗边早餐桌。
产品角色：有机奶粉不是“突然出现的广告道具”，而是妈妈在真实晨间照护中的固定选择。
时间	画面 / 表演	镜头 / 运镜 / 转场	声音 / 文案
00:00-01:5	清晨原始森林，薄雾贴着苔藓，第一束阳光穿过高树。	EWS，静止，阳光从画面左上进入。淡入。	鸟声、远处溪水。
01:5-03:0	一只小手伸进光斑里，指尖沾着一点泥。	CU，慢推近手指。切在指尖动作上。	孩子轻声：亮了。
03:0-04:5	妈妈蹲下，把孩子鞋带系紧，裤脚有湿草痕。	MS，低机位轻微手持。硬切。	布料摩擦、呼吸声。
04:5-06:0	木栈道上，孩子跟着妈妈走，阳光一格一格落在身上。	背后跟拍，轻微晃动。切在脚步落地。	VO：有些成长，不是被催出来的。
06:0-07:5	树皮特写，年轮纹理像一圈圈时间。孩子的手轻轻摸过。	ECU，横向微移。图形匹配切。	VO：是被时间慢慢照看。
07:5-09:0	溪水从石缝流过，水面反射阳光，清澈但不夸张。	低机位静止，水光自然闪动。声音桥。	水声变清晰。
09:0-10:5	林间小屋内，旧木桌、保温壶、干净奶瓶、奶粉罐放在晨光里。	WS，窗框做前景，缓慢推入。硬切。	屋内很安静。
10:5-12:0	妈妈洗净手，擦干，动作很熟练，没有摆拍感。	CU，水珠和手部动作。切在擦手。	水龙头关闭声。
12:0-13:5	奶粉罐打开，封口被揭开一角，粉质在光里很细腻。	ECU，macro drift。切在封口声。	轻微“撕开”声。
13:5-15:0	一平勺奶粉落入奶瓶，阳光照到勺边，不做发光特效。	插入镜头，静止 hold。匹配切到水流。	VO：有机，是每一步都经得起阳光。
15:0-16:5	温水注入，奶粉慢慢融开，玻璃瓶壁有细小水汽。	CU，慢推，rack focus 到水汽。	温水声。
16:5-18:0	妈妈轻轻摇匀，孩子趴在桌边看窗外森林。	MS，妈妈前景，孩子中景。声音桥。	孩子：森林也喝阳光吗？
18:0-19:5	妈妈停一下，没有讲大道理，只看向窗外。	MCU，慢推到她的眼神。硬切。	妈妈轻声：嗯，它慢慢喝。
19:5-21:0	森林外景：阳光落在叶片、土壤、溪水、远处牧草坡上。	三个短切，match cut 光斑位置。	VO：阳光，水源，土地，牧场。
21:0-22:5	回到桌边，孩子双手捧着奶瓶，额头有一点晨光。	MCU，静止，浅景深。切在吞咽前。	VO：最后，回到孩子每天的一杯。
22:5-24:0	妈妈看孩子喝奶，没有夸张微笑，只把孩子袖口轻轻拉好。	OTS，轻微手持。切在拉袖口。	森林声进入屋内。
24:0-25:5	奶粉罐侧面在窗边，后景是树影和阳光，不是棚拍白底。	产品 CU，rack focus 从树影到罐身。	VO：某某有机奶粉。
25:5-27:0	孩子把空手伸向窗外的光斑，手心还有一点奶渍。	CU，慢推，光斑移动。	VO：把自然的耐心，留给成长。
27:0-28:5	妈妈合上奶粉罐，罐身与木桌、溪水声、森林光影在同一空间。	插入镜头，end-frame 准备。	罐盖轻响。
28:5-30:0	End frame：奶粉罐、奶瓶、木桌晨光，背景是虚化森林。	锁定镜头，end-frame lock。	字幕：有机成长，向阳而生。


重新使用skill优化一下这个剧本

> AGENT

我会用 `$ad-creative-script` 重新优化这版。保留你给的“有机、阳光、森林、奶粉”方向，但我会先修它的核心问题：现在太像自然蒙太奇，森林只是背景；优化后要让森林成为“有机秩序”的叙事系统，奶粉成为这个系统回到孩子日常的一杯，而不是片尾道具。

> AGENT

用 `$ad-creative-script` 重新优化。  
这版保留“原始森林 / 有机 / 阳光 / 奶粉”，但把它从“自然蒙太奇”改成一个更清楚的创意装置：

**核心升级：森林不是背景，而是“自然的校验系统”。**  
阳光先经过森林，是因为森林会先检查：水、土、时间、牧草、人的手，最后才让这一杯回到孩子身边。

**片名：《阳光先经过森林》**  
**时长：30s**  
**传播任务：有机奶粉品牌信任片**  
**品牌主张：** 有机不是被说出来的，是被自然一步步校验出来的。  
**品牌句：** 有机成长，先经过自然的校验。

| 时间 | 导演意图 | 画面 / 表演 | 生成画面拆分 | 运镜 / 承接 / 转场 | 声音 / 文案 |
|---|---|---|---|---|---|
| 00:00-01:5 | 建立“自然校验”规则 | 清晨森林，阳光还没照到人，先照到一枚潮湿的树叶。 | 生成 1 张：A｜树叶边缘挂着水珠，第一束光刚碰到水珠｜承接：黑场淡入｜转场：水珠高光切孩子眼睛。 | ECU 静止，淡入。 | 鸟声，远溪声。 |
| 01:5-03:0 | 孩子发现“光在检查” | 孩子蹲下，看着光斑慢慢爬过苔藓，不急着伸手。 | 生成 2 张：A｜孩子侧脸看地面光斑｜B｜小手停在光斑外，指尖有泥｜承接：水珠高光到眼睛反光｜转场：指尖切鞋带。 | CU 慢推。 | 孩子：它先看这里。 |
| 03:0-04:5 | 妈妈不解释，用行动回应 | 妈妈蹲下系鞋带，裤脚有湿草，包里露出奶瓶和奶粉罐边缘。 | 生成 2 张：A｜妈妈低身系鞋带｜B｜包内奶瓶、奶粉罐边缘被自然带入｜承接：孩子手到妈妈手｜转场：鞋带拉紧切木栈道线条。 | 低机位手持。 | 布料、鞋带声。 |
| 04:5-06:0 | 森林像一套秩序，不是风景 | 木栈道上，阳光一格一格落下，孩子每走一步都等光先到。 | 生成 2 张：A｜木栈道被阳光切成格子｜B｜孩子脚停在光格边缘，等光移动｜承接：鞋带线条接栈道线条｜转场：光格切年轮。 | 背后跟拍。 | VO：有些东西，不急着到孩子身边。 |
| 06:0-07:5 | 时间被看见 | 树皮年轮，孩子手指沿着纹路慢慢摸。 | 生成 1 张：A｜手指贴着年轮纹理，泥痕和树皮同框｜承接：木格纹理切年轮｜转场：年轮圆形切奶粉罐盖。 | ECU 横移。 | VO：它先经过时间。 |
| 07:5-09:0 | 水源校验 | 溪水流过石缝，妈妈用随身小杯接一点水，闻一闻，没有戏剧化。 | 生成 2 张：A｜溪水从石缝流过｜B｜妈妈手持小杯，水面反射森林光｜承接：年轮圆形切水面圆光｜转场：水声桥接屋内水壶。 | 低机位静止。 | 水声变近。 |
| 09:0-10:5 | 回到真实喂养空间 | 林间小屋，旧木桌上有保温壶、奶瓶、奶粉罐、孩子捡的叶子。 | 生成 2 张：A｜窗框前景，小屋早餐桌全景｜B｜奶粉罐与叶子、奶瓶在同一晨光里｜承接：溪水声进屋｜转场：窗框切手部。 | WS 缓慢推入。 | 屋内安静。 |
| 10:5-12:0 | 有机不是口号，是手上的步骤 | 妈妈洗手、擦干，动作熟练克制。 | 生成 2 张：A｜水流过妈妈手指｜B｜毛巾擦干手，旁边奶瓶虚焦｜承接：小屋桌面切水龙头｜转场：擦手动作切封口。 | CU，cut on action。 | 水龙头关闭。 |
| 12:0-13:5 | 产品进入“校验系统” | 奶粉罐打开，封口、批次码、粉质在自然光下清晰。 | 生成 3 张：A｜罐身侧面和批次码｜B｜封口被揭开一角｜C｜粉面细腻，不发光｜承接：擦手切封口｜转场：撕开声切量勺。 | Macro drift。 | 轻微撕开声。 |
| 13:5-15:0 | 一平勺成为日常标准 | 一平勺奶粉落入奶瓶，阳光只照到勺边。 | 生成 2 张：A｜平勺在罐口上方｜B｜奶粉落入奶瓶，勺影落在桌面｜承接：粉面切平勺｜转场：勺影切水流。 | 插入镜头静止。 | VO：有机，不是包装上的两个字。 |
| 15:0-16:5 | 冲调不是展示，是秩序落地 | 温水注入，奶粉慢慢融开，玻璃瓶壁有水汽。 | 生成 2 张：A｜温水进入奶瓶｜B｜奶液旋开，瓶壁起细水汽｜承接：勺影切水流｜转场：水汽遮挡切孩子。 | CU 慢推，rack focus。 | 温水声。 |
| 16:5-18:0 | 孩子提出核心问题 | 孩子趴在桌边，看窗外森林和奶瓶。 | 生成 2 张：A｜孩子趴在桌边看窗外｜B｜孩子视线落到奶瓶，奶瓶前景虚焦｜承接：水汽变窗雾｜转场：孩子眼神切妈妈。 | MS，妈妈前景孩子中景。 | 孩子：森林也喝阳光吗？ |
| 18:0-19:5 | 妈妈给出品牌世界观 | 妈妈停一下，看窗外，不讲大道理。 | 生成 1 张：A｜妈妈侧脸，窗外树影落在脸侧｜承接：孩子眼神切妈妈侧脸｜转场：树影切叶片。 | MCU 慢推。 | 妈妈：它慢慢喝。 |
| 19:5-21:0 | 把自然系统串起来 | 三个真实短切：叶片、土壤、溪水、远处牧草坡。 | 生成 3 张：A｜叶片背面透光｜B｜湿土和草根｜C｜远处牧草坡被晨光扫过｜承接：妈妈脸侧树影切叶片｜转场：光斑位置 match cut。 | 三连短切。 | VO：阳光，水源，土地，牧场。 |
| 21:0-22:5 | 自然秩序回到一杯 | 孩子双手捧着奶瓶，额头一小块晨光。 | 生成 2 张：A｜奶瓶被孩子双手捧住｜B｜孩子额头有晨光，眼神安静｜承接：牧草坡光斑切额头光斑｜转场：吞咽前切袖口。 | MCU 静止。 | VO：最后，回到每天这一杯。 |
| 22:5-24:0 | 情绪落在真实照护 | 妈妈没有广告式微笑，只把孩子袖口拉好。 | 生成 2 张：A｜妈妈手拉孩子袖口｜B｜孩子继续喝奶，妈妈手停在袖口边｜承接：孩子手握奶瓶切妈妈手｜转场：手部动作切罐身。 | OTS 手持。 | 森林声进入屋内。 |
| 24:0-25:5 | 产品与自然同处一空间 | 奶粉罐侧面在窗边，后景树影移动。 | 生成 2 张：A｜窗边奶粉罐侧面，树影在罐身附近晃动｜B｜rack focus 到品牌区，背景森林虚化｜承接：袖口手部切罐身边缘｜转场：树影切孩子手心。 | 产品 CU，rack focus。 | VO：某某有机奶粉。 |
| 25:5-27:0 | 记忆画面 | 孩子伸手接住窗边光斑，手心有一点奶渍。 | 生成 2 张：A｜孩子手心有奶渍，光斑靠近｜B｜光斑落进手心，孩子没有抓，只摊开｜承接：罐身树影切手心光｜转场：手心圆光切罐盖。 | CU 慢推。 | VO：把自然的耐心，留给成长。 |
| 27:0-28:5 | 结束前把仪式收好 | 妈妈合上奶粉罐，罐盖声像一个小小确认。 | 生成 1 张：A｜妈妈手合上罐盖，奶瓶和叶子在旁边｜承接：手心圆光切罐盖圆形｜转场：罐盖声切 end frame。 | 插入镜头。 | 罐盖轻响。 |
| 28:5-30:0 | 品牌收束 | End frame：奶粉罐、奶瓶、孩子捡的叶子、木桌晨光，背景虚化森林。 | 生成 2 张：A｜产品、奶瓶、叶子同桌，真实晨光｜B｜留 logo / slogan 安全区，森林虚化｜承接：罐盖声后锁帧｜转场：end-frame lock。 | 锁定镜头。 | 字幕：有机成长，先经过自然的校验。 |

**优化后的变化**

- 原版是“森林很美，所以有机很自然”；新版是“森林先校验水、土、时间、人的步骤，最后才到孩子的一杯”。
- 奶粉罐更早进入，不是最后才出现。
- “阳光”不只是氛围，而是校验系统的视觉线索。
- 每一行都拆了 `生成画面拆分`，方便直接生图和后续视频生成。
- 合规上没有写“长高、变聪明、提高免疫力”等承诺；“有机”需要替换成品牌真实认证与资质。

> DEVELOPER

文案写的很垃圾

> AGENT

我同意，上一版文案太像“策略说明句”，不是广告片里的好文案：它一直在解释“有机、校验、自然”，但没有一句真正能留下来。我这次只重写文案系统，先不动大结构，让它更像一条能拍出来、能被记住的品牌片。

> AGENT

对，上一版文案最大问题是太“说明书式”：  
“有机、自然、校验、成长”都在讲道理，没有一句像真正品牌片的钩子。

我建议把整条片的文案核心改成：

**主文案：**  
**给孩子之前，先交给自然。**

**品牌句：**  
**某某有机奶粉，每一杯，先过自然这一关。**

新版文案替换如下：

| 时间 | 原画面不变 | 新文案 / 声音 |
|---|---|---|
| 00:00-01:5 | 阳光照到树叶水珠 | 只留鸟声、溪水声，不说话。 |
| 01:5-03:0 | 孩子看光斑 | 孩子轻声：它在看什么？ |
| 04:5-06:0 | 木栈道上，孩子等光先到 | VO：给孩子之前，有些东西要先慢下来。 |
| 06:0-07:5 | 年轮与孩子手指 | VO：先经过时间。 |
| 07:5-09:0 | 溪水与小杯 | VO：经过水。 |
| 10:5-12:0 | 妈妈洗手擦干 | 只留水声、毛巾声。 |
| 12:0-13:5 | 奶粉罐封口、批次码、粉质 | VO：有机，不是说出来的。 |
| 13:5-15:0 | 一平勺奶粉落入奶瓶 | VO：是一步一步，经得起看。 |
| 15:0-16:5 | 温水注入，奶粉融开 | 温水声，不加旁白。 |
| 16:5-18:0 | 孩子看窗外森林和奶瓶 | 孩子：森林也会检查吗？ |
| 18:0-19:5 | 妈妈看向窗外 | 妈妈：嗯，好的东西，都不怕慢一点。 |
| 19:5-21:0 | 叶片、土壤、溪水、牧草坡 | VO：阳光，水源，土地，牧场。 |
| 21:0-22:5 | 孩子捧着奶瓶 | VO：最后，才到孩子手里。 |
| 22:5-24:0 | 妈妈拉好孩子袖口 | 只留森林声进入屋内。 |
| 24:0-25:5 | 奶粉罐窗边产品镜头 | VO：某某有机奶粉。 |
| 25:5-27:0 | 孩子手心接住光斑 | VO：把该慢的地方，交给自然。 |
| 27:0-28:5 | 妈妈合上奶粉罐 | 罐盖轻响。 |
| 28:5-30:0 | End frame | 字幕 / VO：每一杯，先过自然这一关。 |

**可选品牌句**

1. **给孩子之前，先交给自然。**
2. **每一杯，先过自然这一关。**
3. **有机不是承诺，是一路经得起看。**
4. **让自然先确认，再给孩子。**

我建议用第 2 句做片尾，最短、最像广告记忆点。

> DEVELOPER

给我总的剧本

> AGENT

**片名：《阳光先经过森林》**  
**时长：30s**  
**品类：有机奶粉品牌片**  
**核心创意：** 给孩子之前，先交给自然。阳光、水源、土地、牧场、人的每一步照护，先慢慢经过，最后才回到孩子每天的一杯。  
**品牌句：** 每一杯，先过自然这一关。

| 时间 | 画面 / 表演 | 镜头 / 运镜 / 转场 | 声音 / 文案 |
|---|---|---|---|
| 00:00-01:5 | 清晨森林，第一束阳光落在一枚树叶水珠上。 | ECU 静止，黑场淡入。水珠高光切孩子眼睛。 | 鸟声、溪水声。 |
| 01:5-03:0 | 孩子蹲在苔藓边，看光斑慢慢爬过地面，小手停在光外，指尖有泥。 | CU 慢推。 | 孩子轻声：它在看什么？ |
| 03:0-04:5 | 妈妈蹲下给孩子系鞋带，裤脚有湿草痕，包里露出奶瓶和奶粉罐边缘。 | 低机位轻微手持，硬切。 | 鞋带、布料摩擦声。 |
| 04:5-06:0 | 木栈道上，阳光一格一格落下，孩子每走一步都像等光先到。 | 背后跟拍，切在脚步落地。 | VO：给孩子之前，有些东西要先慢下来。 |
| 06:0-07:5 | 树皮年轮特写，孩子手指沿着纹路轻轻摸过。 | ECU 横移，年轮圆形切水面圆光。 | VO：先经过时间。 |
| 07:5-09:0 | 溪水从石缝流过，妈妈用随身小杯接一点水，闻一闻。 | 低机位静止，水声桥接屋内。 | VO：经过水。 |
| 09:0-10:5 | 林间小屋内，旧木桌上有保温壶、奶瓶、奶粉罐和孩子捡的叶子。 | WS，窗框做前景，缓慢推入。 | 屋内安静。 |
| 10:5-12:0 | 妈妈洗手、擦干，动作熟练克制。 | CU，水流切到毛巾擦手。 | 水声、毛巾声。 |
| 12:0-13:5 | 奶粉罐打开，封口、批次码、细腻粉面在自然光下清楚可见。 | Macro drift，切在封口撕开声。 | VO：有机，不是说出来的。 |
| 13:5-15:0 | 一平勺奶粉落入奶瓶，阳光只照到勺边，勺影落在木桌上。 | 插入镜头静止，勺影切水流。 | VO：是一步一步，经得起看。 |
| 15:0-16:5 | 温水注入奶瓶，奶粉慢慢融开，玻璃瓶壁有细小水汽。 | CU 慢推，rack focus 到水汽。 | 温水声。 |
| 16:5-18:0 | 孩子趴在桌边，看窗外森林，又看奶瓶。 | MS，妈妈前景，孩子中景。 | 孩子：森林也会检查吗？ |
| 18:0-19:5 | 妈妈停一下，看向窗外，不讲大道理。 | MCU 慢推到侧脸。 | 妈妈：嗯，好的东西，都不怕慢一点。 |
| 19:5-21:0 | 叶片透光、湿土草根、溪水、远处牧草坡，四个短切。 | 光斑位置 match cut。 | VO：阳光，水源，土地，牧场。 |
| 21:0-22:5 | 孩子双手捧着奶瓶，额头有一小块晨光。 | MCU 静止，浅景深。 | VO：最后，才到孩子手里。 |
| 22:5-24:0 | 妈妈没有夸张微笑，只把孩子袖口轻轻拉好。 | OTS，轻微手持。 | 森林声进入屋内。 |
| 24:0-25:5 | 奶粉罐在窗边，树影在后景移动，品牌区清楚。 | 产品 CU，rack focus 到罐身。 | VO：某某有机奶粉。 |
| 25:5-27:0 | 孩子把小手伸向窗边光斑，手心有一点奶渍。 | CU 慢推。 | VO：把该慢的地方，交给自然。 |
| 27:0-28:5 | 妈妈合上奶粉罐，罐盖声很轻。 | 插入镜头，准备 end-frame。 | 罐盖轻响。 |
| 28:5-30:0 | End frame：奶粉罐、奶瓶、孩子捡的叶子、木桌晨光，背景虚化森林。 | 锁定镜头，留 logo / slogan 安全区。 | 字幕 / VO：每一杯，先过自然这一关。 |

**备注：** “有机”“牧场”“水源”等信息需要替换为品牌真实资质和可用卖点，避免无依据宣称。

> DEVELOPER

画面拆分呢？？？？

> AGENT

对，这里我漏掉了最关键的 `生成画面拆分`。下面补完整版本。  
这版建议生成 **34 张关键画面**，每张只表达一个瞬间。

| 时间 | 画面 / 表演 | 生成画面拆分 | 承接 / 转场 | 声音 / 文案 |
|---|---|---|---|---|
| 00:00-01:5 | 清晨森林，阳光落在树叶水珠上。 | 生成 1 张：A｜树叶水珠特写，第一束阳光刚碰到水珠。 | 黑场淡入；水珠高光切孩子眼睛。 | 鸟声、溪水声。 |
| 01:5-03:0 | 孩子看光斑，小手停在光外。 | 生成 2 张：A｜孩子蹲在苔藓边看地面光斑；B｜小手停在光斑外，指尖有泥。 | A 接水珠高光；B 的指尖动作切鞋带。 | 孩子：它在看什么？ |
| 03:0-04:5 | 妈妈给孩子系鞋带。 | 生成 2 张：A｜妈妈低身系鞋带，裤脚有湿草；B｜包里露出奶瓶和奶粉罐边缘。 | 孩子手切妈妈手；包内产品做早期露出。 | 鞋带、布料声。 |
| 04:5-06:0 | 木栈道上，孩子等光先到。 | 生成 2 张：A｜木栈道被阳光切成格子；B｜孩子脚停在光格边缘。 | 鞋带线条切栈道线条；脚步落地切年轮。 | VO：给孩子之前，有些东西要先慢下来。 |
| 06:0-07:5 | 孩子摸树皮年轮。 | 生成 1 张：A｜孩子手指沿年轮纹理移动，泥痕和树皮同框。 | 栈道纹理切年轮；年轮圆形切水面圆光。 | VO：先经过时间。 |
| 07:5-09:0 | 溪水与水源。 | 生成 2 张：A｜溪水从石缝流过；B｜妈妈用小杯接水，水面反射森林光。 | 年轮圆形切水面；水声桥接屋内。 | VO：经过水。 |
| 09:0-10:5 | 林间小屋早餐桌。 | 生成 2 张：A｜窗框前景，小屋旧木桌全景；B｜奶粉罐、奶瓶、叶子在晨光里。 | 溪水声进入屋内；窗框切手部。 | 屋内安静。 |
| 10:5-12:0 | 妈妈洗手擦干。 | 生成 2 张：A｜水流过妈妈手指；B｜毛巾擦干手，奶瓶虚焦在旁边。 | 桌面切水龙头；擦手动作切封口。 | 水声、毛巾声。 |
| 12:0-13:5 | 奶粉罐打开。 | 生成 3 张：A｜罐身批次码/标签细节；B｜封口被揭开一角；C｜自然光下的细腻粉面。 | 擦手切封口；撕开声切量勺。 | VO：有机，不是说出来的。 |
| 13:5-15:0 | 一平勺奶粉落入奶瓶。 | 生成 2 张：A｜平勺停在罐口上方；B｜奶粉落入奶瓶，勺影落在木桌。 | 粉面切平勺；勺影切水流。 | VO：是一步一步，经得起看。 |
| 15:0-16:5 | 温水冲调。 | 生成 2 张：A｜温水注入奶瓶；B｜奶粉融开，瓶壁有细小水汽。 | 勺影切水流；水汽遮挡切孩子。 | 温水声。 |
| 16:5-18:0 | 孩子看森林和奶瓶。 | 生成 2 张：A｜孩子趴在桌边看窗外；B｜孩子视线落到奶瓶。 | 水汽变窗雾；孩子眼神切妈妈侧脸。 | 孩子：森林也会检查吗？ |
| 18:0-19:5 | 妈妈看向窗外。 | 生成 1 张：A｜妈妈侧脸，树影落在脸侧。 | 孩子眼神切妈妈；树影切叶片。 | 妈妈：嗯，好的东西，都不怕慢一点。 |
| 19:5-21:0 | 自然系统短切。 | 生成 4 张：A｜叶片背面透光；B｜湿土和草根；C｜溪水流过石缝；D｜远处牧草坡被晨光扫过。 | 光斑位置连续 match cut；牧草坡光斑切孩子额头。 | VO：阳光，水源，土地，牧场。 |
| 21:0-22:5 | 孩子捧着奶瓶。 | 生成 2 张：A｜孩子双手捧住奶瓶；B｜孩子额头有晨光，准备喝。 | 牧草坡光斑切额头光斑；奶瓶切袖口。 | VO：最后，才到孩子手里。 |
| 22:5-24:0 | 妈妈拉好孩子袖口。 | 生成 2 张：A｜妈妈手拉孩子袖口；B｜孩子喝奶，妈妈手停在袖口边。 | 孩子手握奶瓶切妈妈手；手部动作切罐身。 | 森林声进入屋内。 |
| 24:0-25:5 | 产品在窗边。 | 生成 2 张：A｜奶粉罐侧面，树影在后景移动；B｜rack focus 到品牌区，森林虚化。 | 袖口手部切罐身边缘；树影切孩子手心。 | VO：某某有机奶粉。 |
| 25:5-27:0 | 孩子接住光斑。 | 生成 2 张：A｜孩子手心有奶渍，光斑靠近；B｜光斑落进手心，孩子摊开手。 | 罐身树影切手心光；手心圆光切罐盖。 | VO：把该慢的地方，交给自然。 |
| 27:0-28:5 | 妈妈合上奶粉罐。 | 生成 1 张：A｜妈妈手合上罐盖，奶瓶和叶子在旁边。 | 手心圆光切罐盖圆形；罐盖声切 end frame。 | 罐盖轻响。 |
| 28:5-30:0 | End frame。 | 生成 2 张：A｜奶粉罐、奶瓶、叶子、木桌晨光同框；B｜同构图留 logo / slogan 安全区，森林虚化。 | A 锁定产品关系；B end-frame lock。 | 字幕 / VO：每一杯，先过自然这一关。 |

**总计：34 张图。**  
其中产品相关关键帧是：第 3B、7B、9A/B/C、10A/B、11A/B、17A/B、19A、20A/B。

> DEVELOPER

运镜呢？？？？？你为什么总是漏东西？

> AGENT

我会直接把漏掉的「运镜」补回去，并把这次的输出结构固定成：画面拆分、镜头景别、运镜、承接/转场、声音/文案一起出现。先快速看一眼 skill 里现在的强制格式，确保不是我输出时又掉链子。

> AGENT

你说得对，这次是我漏了关键列。问题不是你要求不清楚，是我把「运镜」揉进了「承接/转场」里，导致分镜不能直接指导生图和视频生成。下面给你补成完整版本：每一行都包含 **画面拆分 + 景别 + 运镜 + 承接/转场**。

**《阳光先经过森林》完整分镜版**

| 时间 | 画面 / 表演 | 生成画面拆分 | 景别 / 运镜 | 承接 / 转场 | 声音 / 文案 |
|---|---|---|---|---|---|
| 00:00-01.5 | 清晨，森林边缘一片叶子接住第一滴露水，阳光还没完全照进来。 | 生成1张：A 叶尖露水里倒映树冠和微弱晨光。 | ECU，静止 hold，微弱呼吸感。 | 淡入，露水反光引出下一镜光斑。 | 鸟声很远，空气安静。 |
| 01.5-03.0 | 孩子的小手伸向地上一块光斑，手指有泥。 | 生成2张：A 小手停在光斑外；B 指尖进入光里。 | CU，低机位，慢推近手指。 | 切在手指触光瞬间。 | 孩子轻声：亮了。 |
| 03.0-04.5 | 妈妈蹲下系鞋带，动作熟练，裤脚沾着湿草。 | 生成1张：妈妈低头系鞋带，孩子脚尖轻晃。 | MS，低机位，轻微手持漂移。 | 硬切，接脚步动作。 | 布料摩擦声。 |
| 04.5-06.0 | 木栈道上，妈妈和孩子往前走，光一格一格落在身上。 | 生成2张：A 背影进入栈道；B 阳光切在孩子肩膀上。 | WS，背后跟拍，轻微 handheld tracking。 | 脚步声做声音桥。 | VO：给孩子之前，先交给自然。 |
| 06.0-07.5 | 树皮年轮特写，孩子的手慢慢摸过。 | 生成1张：手掌贴着粗糙树皮，年轮像时间纹路。 | ECU，横向微移 slide。 | 图形匹配切到水纹。 | VO：交给时间。 |
| 07.5-09.0 | 溪水从石缝流过，水很清，不夸张发光。 | 生成1张：低角度溪水，阳光在水面轻闪。 | CU，低机位静止，浅景深。 | 水声延续到室内水龙头。 | VO：交给水源。 |
| 09.0-10.5 | 林间小屋内，窗边木桌上有保温壶、奶瓶、奶粉罐。 | 生成2张：A 从窗外看进屋内；B 桌面物件进入晨光。 | WS，窗框前景，慢慢 push in。 | 从自然空间进入照护空间。 | 屋内安静，远处溪水仍在。 |
| 10.5-12.0 | 妈妈洗手、擦干，动作很日常但认真。 | 生成2张：A 水流过手指；B 毛巾擦干指缝。 | CU，手部跟随，轻微 handheld drift。 | 切在水龙头关闭声。 | 水声停止。 |
| 12.0-13.5 | 奶粉罐打开，封口、批次信息、粉质被依次看见。 | 生成3张：A 罐身与标签；B 封口揭开；C 奶粉细腻表面。 | Insert / ECU，macro drift，rack focus。 | 封口声切到奶粉勺。 | 轻微撕开声。 |
| 13.5-15.0 | 一平勺奶粉落入奶瓶，粉末不是梦幻飘散，而是干净、真实。 | 生成2张：A 平勺悬在瓶口；B 奶粉落入瓶中。 | ECU，静止 hold，微距。 | 粉末下落方向匹配到水流。 | VO：有机，不是一个漂亮的词。 |
| 15.0-16.5 | 温水注入，奶粉慢慢融开，瓶壁有细小水汽。 | 生成2张：A 温水进入瓶中；B 水汽贴在玻璃瓶壁。 | CU，慢推，rack focus 到水汽。 | 水汽虚化转到孩子脸。 | VO：是每一步都经得起查看。 |
| 16.5-18.0 | 孩子趴在桌边，看窗外森林，妈妈轻轻摇匀奶瓶。 | 生成2张：A 妈妈前景摇瓶；B 孩子望向窗外。 | MS，前后景构图，轻微横移 slide。 | 摇瓶节奏接树叶晃动。 | 孩子：森林也喝阳光吗？ |
| 18.0-19.5 | 妈妈停了一下，没有讲道理，只顺着孩子目光看出去。 | 生成1张：妈妈眼神望向窗外，表情克制。 | MCU，慢推到眼神。 | 视线方向切到森林。 | 妈妈轻声：嗯，它慢慢喝。 |
| 19.5-21.0 | 自然系统短切：叶片、湿土、溪水、远处牧草坡。 | 生成4张：A 叶片透光；B 湿土和根系；C 溪水流过石头；D 远处牧草坡晨光。 | CU/WS 组合，短切节奏，locked-off graphic match。 | 每张用光斑位置 match cut。 | VO：阳光、水源、土地、时间。 |
| 21.0-22.5 | 回到桌边，孩子双手捧着奶瓶，额头有一点晨光。 | 生成2张：A 奶瓶被递到孩子手里；B 孩子低头喝奶。 | MCU，静止，浅景深。 | 从自然大系统落回一杯奶。 | VO：最后，回到每天这一杯。 |
| 22.5-24.0 | 妈妈看孩子喝奶，把孩子袖口轻轻拉好。 | 生成1张：妈妈手指整理袖口，孩子安静喝奶。 | OTS，轻微手持，贴近真实生活。 | 切在拉袖口动作上。 | 森林声进入屋内。 |
| 24.0-25.5 | 奶粉罐在窗边，背景是真实树影，不是棚拍白底。 | 生成2张：A 树影落在罐身旁；B 焦点从树影转到罐身。 | 产品 CU，rack focus。 | 树影晃动接孩子手心光斑。 | VO：某某有机奶粉。 |
| 25.5-27.0 | 孩子把小手伸向窗边光斑，手心有一点奶渍。 | 生成1张：奶渍、光斑、小手在同一画面里。 | CU，慢推，光斑轻微移动。 | 光斑形状匹配到罐盖圆形。 | VO：每一杯，先过自然这一关。 |
| 27.0-28.5 | 妈妈合上奶粉罐，动作干净，声音轻。 | 生成1张：罐盖合上，木桌纹理清楚。 | Insert，静止，轻微下压角度。 | 罐盖声切入 end frame。 | 罐盖轻响。 |
| 28.5-30.0 | End frame：奶粉罐、奶瓶、木桌晨光，背景虚化森林。 | 生成2张：A 产品完整 end frame；B logo/slogan 安全留白版。 | Locked-off，end-frame lock，无运镜。 | 定格收尾。 | 字幕：每一杯，先过自然这一关。 |

以后这个 skill 输出分镜时，我会固定保留这几列：**时间、画面/表演、生成画面拆分、景别、运镜、承接/转场、声音/文案**，不再把运镜藏进别的栏里。

> DEVELOPER

还缺少每个分镜的视频生成描述，我还需要你在其中补充拆分出来的画面图片放入其中标记出来

> AGENT

对，这一层也该有：拆出来的图片不是只写在「生成画面拆分」里，还要进入视频生成描述，明确哪张做首帧、哪张做尾帧、哪张做中间参考。我先按这个规则给你补全，并把图片标记统一成可追踪的编号。

> AGENT

对，这里要补的是 **视频生成层**。以后每个分镜必须同时写清楚：

- `图片标记`：这一镜拆成哪几张图，比如 `[图04A] [图04B]`
- `视频首帧/尾帧`：视频生成时用哪张图做开始、哪张做结束
- `视频生成描述`：镜头如何动、人物/物体怎么动、光怎么变、怎么接下一镜

下面是补全版。

| 时间 | 图片标记 | 视频首帧 / 尾帧 | 视频生成描述 |
|---|---|---|---|
| 00:00-01.5 | `[图01A]` 叶尖露水，倒映树冠与晨光 | 首帧 `[图01A]`，尾帧仍用 `[图01A]` | 静止微动镜头，露水轻颤，晨光从画面左上慢慢增强。镜头保持微距，不移动主体，只让自然光变化带出清晨感。淡入下一镜。 |
| 01.5-03.0 | `[图02A]` 小手停在光斑外；`[图02B]` 指尖进入光里 | 首帧 `[图02A]`，尾帧 `[图02B]` | 低机位慢推，小手从画面右侧轻轻伸入光斑。动作很慢，指尖触光时停顿半秒。切在触光瞬间。 |
| 03.0-04.5 | `[图03A]` 妈妈蹲下系鞋带 | 首帧 `[图03A]`，尾帧 `[图03A]` | 轻微手持漂移，妈妈手指系紧鞋带，孩子脚尖轻晃。镜头保持低机位，突出真实照护动作。硬切到脚步。 |
| 04.5-06.0 | `[图04A]` 背影进入木栈道；`[图04B]` 阳光落在孩子肩膀 | 首帧 `[图04A]`，尾帧 `[图04B]` | 背后跟拍，母子向前走，镜头轻微晃动。阳光一格一格扫过孩子肩膀和头发。脚步声做声音桥进入下一镜。 |
| 06.0-07.5 | `[图05A]` 孩子手掌贴着树皮年轮 | 首帧 `[图05A]`，尾帧 `[图05A]` | 微距横移，镜头沿着树皮纹理缓慢滑动，孩子手掌从左到右轻轻摸过。用年轮纹理图形匹配到下一镜水纹。 |
| 07.5-09.0 | `[图06A]` 溪水流过石头，水面晨光 | 首帧 `[图06A]`，尾帧 `[图06A]` | 低机位静止，溪水自然流动，水面反光轻微跳动。水声提前延续，作为 J-cut 进入室内。 |
| 09.0-10.5 | `[图07A]` 窗外看进小屋；`[图07B]` 桌面物件进入晨光 | 首帧 `[图07A]`，尾帧 `[图07B]` | 镜头从窗外缓慢推入屋内，窗框作为前景，桌上的奶瓶、保温壶、奶粉罐逐渐清晰。自然空间转入照护空间。 |
| 10.5-12.0 | `[图08A]` 水流过手；`[图08B]` 毛巾擦干指缝 | 首帧 `[图08A]`，尾帧 `[图08B]` | 手部特写跟随，先拍水流，再切到擦干动作。动作克制、熟练，不摆拍。水龙头关闭声作为剪辑点。 |
| 12.0-13.5 | `[图09A]` 罐身标签；`[图09B]` 封口揭开；`[图09C]` 奶粉表面 | 首帧 `[图09A]`，中间参考 `[图09B]`，尾帧 `[图09C]` | 微距镜头从罐身标签 rack focus 到封口，再切到粉质表面。封口声清晰，强调“可查看、可追溯”的真实质感。 |
| 13.5-15.0 | `[图10A]` 平勺悬在瓶口；`[图10B]` 奶粉落入瓶中 | 首帧 `[图10A]`，尾帧 `[图10B]` | 静止微距，奶粉从勺中落下，不做夸张发光特效。粉末下落方向匹配到下一镜水流方向。 |
| 15.0-16.5 | `[图11A]` 温水注入；`[图11B]` 瓶壁水汽 | 首帧 `[图11A]`，尾帧 `[图11B]` | 慢推近奶瓶，温水注入后奶粉自然融开，焦点从液体转到瓶壁水汽。水汽虚化后切到孩子脸。 |
| 16.5-18.0 | `[图12A]` 妈妈前景摇奶瓶；`[图12B]` 孩子望向窗外 | 首帧 `[图12A]`，尾帧 `[图12B]` | 镜头轻微横移，前景妈妈摇瓶，中景孩子看向窗外。焦点从奶瓶转到孩子眼神。摇瓶节奏接下一镜树叶晃动。 |
| 18.0-19.5 | `[图13A]` 妈妈看向窗外，表情克制 | 首帧 `[图13A]`，尾帧 `[图13A]` | 慢推到妈妈眼神，她没有解释，只顺着孩子视线看出去。视线方向成为转场动线，硬切到森林。 |
| 19.5-21.0 | `[图14A]` 叶片透光；`[图14B]` 湿土根系；`[图14C]` 溪水石缝；`[图14D]` 牧草坡晨光 | 首帧 `[图14A]`，中间参考 `[图14B] [图14C]`，尾帧 `[图14D]` | 四个短切，不做飘逸蒙太奇，保持真实自然观察。每一切用光斑位置做 graphic match，形成“自然系统逐层通过”的感觉。 |
| 21.0-22.5 | `[图15A]` 奶瓶递到孩子手里；`[图15B]` 孩子低头喝奶 | 首帧 `[图15A]`，尾帧 `[图15B]` | 中近景静止，妈妈的手把奶瓶递入画面，孩子双手接住。镜头不煽情，停在孩子安静喝奶的瞬间。 |
| 22.5-24.0 | `[图16A]` 妈妈整理孩子袖口 | 首帧 `[图16A]`，尾帧 `[图16A]` | OTS 轻微手持，妈妈把孩子袖口拉好，动作很小但有照护感。森林环境声轻轻进入屋内。 |
| 24.0-25.5 | `[图17A]` 树影落在罐身旁；`[图17B]` 焦点转到奶粉罐 | 首帧 `[图17A]`，尾帧 `[图17B]` | 产品近景，先让树影在罐身旁晃动，再 rack focus 到罐身。产品不是硬插入，而是属于这个清晨空间。 |
| 25.5-27.0 | `[图18A]` 孩子小手、奶渍、光斑 | 首帧 `[图18A]`，尾帧 `[图18A]` | 慢推小手，手心奶渍与窗边光斑同框。光斑轻微移动，形状匹配下一镜罐盖圆形。 |
| 27.0-28.5 | `[图19A]` 妈妈合上奶粉罐 | 首帧 `[图19A]`，尾帧 `[图19A]` | 插入镜头，妈妈合上罐盖，动作干净利落。罐盖轻响作为声音剪辑点，切入 end frame。 |
| 28.5-30.0 | `[图20A]` 产品完整 end frame；`[图20B]` logo/slogan 安全留白版 | 首帧 `[图20A]`，尾帧 `[图20B]` | 锁定镜头，无运镜。产品、奶瓶、木桌晨光稳定成片尾画面，背景森林虚化。最后 0.5 秒留给 logo 与 slogan。 |

补充后的结构应该固定为：

`分镜时间 → 拆分图片标记 → 首帧/尾帧引用 → 视频生成描述 → 运镜/转场 → 声音/文案`

也就是说，之后不是只给“分镜脚本”，而是直接给 **可生图、可图生视频、可剪辑衔接** 的版本。

> DEVELOPER

13.5-15.0	一平勺奶粉落入奶瓶，粉末不是梦幻飘散，而是干净、真实。	首帧 [图10A]，尾帧 [图10B]	静止微距，奶粉从勺中落下，不做夸张发光特效。粉末下落方向匹配到下一镜水流方向。	ECU，静止 hold，微距。	粉末下落方向匹配到水流。	VO：有机，不是一个漂亮的词。	生成2张：A 平勺悬在瓶口；B 奶粉落入瓶中。	[图10A] 平勺悬在瓶口；[图10B] 奶粉落入瓶中
15.0-16.5	温水注入，奶粉慢慢融开，瓶壁有细小水汽。	首帧 [图11A]，尾帧 [图11B]	慢推近奶瓶，温水注入后奶粉自然融开，焦点从液体转到瓶壁水汽。水汽虚化后切到孩子脸。	CU，慢推，rack focus 到水汽。	水汽虚化转到孩子脸。	VO：是每一步都经得起查看。	生成2张：A 温水进入瓶中；B 水汽贴在玻璃瓶壁。	[图11A] 温水注入；[图11B] 瓶壁水汽

这个部分的剧情不对，奶粉是先放水再放奶

> AGENT

你这个抓得非常对，而且这是硬错误：奶粉冲调顺序不能写反。这个不只是分镜小问题，是品类常识和可信度问题，我先把这两行改成「先温水、再奶粉、再摇匀」，并把后面的画面编号顺下来。

> AGENT

对，这里必须改。奶粉冲调顺序应该是 **先放温水，再放奶粉**，之前写反了，会显得非常不专业。

修正这两行如下：

| 时间 | 画面 / 表演 | 视频首帧 / 尾帧 | 视频生成描述 | 景别 / 运镜 | 承接 / 转场 | 声音 / 文案 | 生成画面拆分 | 图片标记 |
|---|---|---|---|---|---|---|---|---|
| 13.5-15.0 | 妈妈先把适量温水注入奶瓶，水面轻轻晃动，瓶壁出现细小水汽。 | 首帧 `[图10A]`，尾帧 `[图10B]` | 微距慢推，温水先进入空奶瓶，水位上升到合适刻度。镜头不要拍成广告棚感，重点是干净、真实、可被信任的冲调步骤。 | CU，慢推，rack focus 从水流到瓶身刻度。 | 水流方向承接上一镜封口动作，水汽虚化后切到奶粉勺。 | 温水声。VO：有机，不是一个漂亮的词。 | 生成2张：A 温水注入空奶瓶；B 奶瓶水位与细小水汽。 | `[图10A]` 温水注入空奶瓶；`[图10B]` 奶瓶水位与水汽 |
| 15.0-16.5 | 一平勺奶粉加入温水中，粉末落入水面后慢慢融开。 | 首帧 `[图11A]`，尾帧 `[图11B]` | 静止微距，平勺停在瓶口上方，奶粉落入温水，不做夸张发光特效。粉末接触水面后自然散开，焦点从勺边转到瓶内融化状态。 | ECU，静止 hold，微距，轻微 rack focus。 | 奶粉下落动作切到下一镜妈妈摇匀奶瓶。 | 轻微粉末落入声。VO：是每一步都经得起查看。 | 生成2张：A 平勺悬在已有温水的奶瓶口；B 奶粉落入温水并开始融开。 | `[图11A]` 平勺悬在温水奶瓶口；`[图11B]` 奶粉落入温水 |

后面 `16.5-18.0` 应该顺接改成：妈妈轻轻旋摇/摇匀奶瓶，孩子趴在桌边看窗外森林。

以后奶粉类脚本要加一条硬校验：**所有产品使用动作必须符合真实冲调流程，尤其是先水后粉、比例/水温不乱写，具体数值只在品牌提供官方说明时出现。**

> DEVELOPER

12.0-13.5	奶粉罐打开，封口、批次信息、粉质被依次看见。	首帧 [图09A]，中间参考 [图09B]，尾帧 [图09C]	微距镜头从罐身标签 rack focus 到封口，再切到粉质表面。封口声清晰，强调“可查看、可追溯”的真实质感。	Insert / ECU，macro drift，rack focus。	封口声切到奶粉勺。	轻微撕开声。	生成3张：A 罐身与标签；B 封口揭开；C 奶粉细腻表面。	[图09A] 罐身标签；[图09B] 封口揭开；[图09C] 奶粉表面
13.5-15.0	一平勺奶粉落入奶瓶，粉末不是梦幻飘散，而是干净、真实。	首帧 [图10A]，尾帧 [图10B]	静止微距，奶粉从勺中落下，不做夸张发光特效。粉末下落方向匹配到下一镜水流方向。	ECU，静止 hold，微距。	粉末下落方向匹配到水流。	VO：有机，不是一个漂亮的词。	生成2张：A 平勺悬在瓶口；B 奶粉落入瓶中。	[图10A] 平勺悬在瓶口；[图10B] 奶粉落入瓶中
15.0-16.5	温水注入，奶粉慢慢融开，瓶壁有细小水汽。	首帧 [图11A]，尾帧 [图11B]	慢推近奶瓶，温水注入后奶粉自然融开，焦点从液体转到瓶壁水汽。水汽虚化后切到孩子脸。	CU，慢推，rack focus 到水汽。	水汽虚化转到孩子脸。	VO：是每一步都经得起查看。	生成2张：A 温水进入瓶中；B 水汽贴在玻璃瓶壁。	[图11A] 温水注入；[图11B] 瓶壁水汽

那从这个分镜开始剧情就要改吧

> AGENT

是，要从 `12.0` 开始重排。因为这里不是单独把两行换顺序就行，动作因果会连着影响：开罐之后不能马上“粉落入瓶”，必须先准备奶瓶温水，再取粉、入水、摇匀，后面孩子看窗外那一镜也要顺延成“摇匀完成后的生活动作”。

> AGENT

对，要从 `12.0` 开始改，不是只把后两行对调。因为 `12.0-13.5` 的承接原来是“封口声切到奶粉勺”，这个也会把剧情带错。正确因果应该是：

**开罐检查 → 先往奶瓶加温水 → 再加一平勺奶粉 → 摇匀 → 孩子喝奶**

替换成这一段：

| 时间 | 画面 / 表演 | 视频首帧 / 尾帧 | 视频生成描述 | 景别 / 运镜 | 承接 / 转场 | 声音 / 文案 | 生成画面拆分 | 图片标记 |
|---|---|---|---|---|---|---|---|---|
| 12.0-13.5 | 奶粉罐打开，先看到罐身信息、封口、内置量勺和粉面。妈妈还没有取粉，只是在完成准备。 | 首帧 `[图09A]`，中间参考 `[图09B]`，尾帧 `[图09C]` | 微距镜头从罐身标签移到封口，再到打开后的粉面与量勺。重点是“干净、真实、步骤可见”，不要表现成夸张产品奇观。 | Insert / ECU，macro drift，rack focus。 | 封口声切到奶瓶刻度和水流，不再切到奶粉勺。 | 轻微撕开声。 | 生成3张：A 罐身标签；B 封口揭开；C 量勺与粉面。 | `[图09A]` 罐身标签；`[图09B]` 封口揭开；`[图09C]` 量勺与粉面 |
| 13.5-15.0 | 妈妈拿起干净奶瓶，先注入适量温水，瓶身刻度清楚，瓶壁有细小水汽。 | 首帧 `[图10A]`，尾帧 `[图10B]` | 镜头慢推奶瓶，温水先进入空奶瓶，水位缓慢上升到合适刻度。水汽轻微出现，真实、不棚拍。 | CU，慢推，rack focus 从水流到瓶身刻度。 | 水位线的横向形状 match cut 到下一镜平勺边缘。 | 温水声。VO：有机，不是一个漂亮的词。 | 生成2张：A 空奶瓶瓶口与刻度；B 温水注入后形成水位和水汽。 | `[图10A]` 空奶瓶与刻度；`[图10B]` 温水水位与水汽 |
| 15.0-16.5 | 一平勺奶粉加入已经有温水的奶瓶，粉末接触水面后自然融开。 | 首帧 `[图11A]`，尾帧 `[图11B]` | 静止微距，平勺停在瓶口上方，奶粉落入温水。粉末不要梦幻飘散，不要发光，只表现真实溶解。焦点从勺边转到瓶内。 | ECU，静止 hold，微距，轻微 rack focus。 | 奶粉下落动作切到下一镜合盖摇匀。 | 轻微粉末落入声。VO：是每一步都经得起查看。 | 生成2张：A 平勺悬在已有温水的奶瓶口；B 奶粉落入温水并开始融开。 | `[图11A]` 平勺悬在温水奶瓶口；`[图11B]` 奶粉落入温水 |
| 16.5-18.0 | 妈妈拧紧奶瓶，轻轻旋摇/摇匀；孩子趴在桌边等，望向窗外森林。 | 首帧 `[图12A]`，尾帧 `[图12B]` | 中景轻微横移，前景是妈妈拧紧奶瓶并轻轻摇匀，中景孩子看向窗外。焦点从奶瓶转到孩子眼神，动作保持真实克制。 | MS，轻微横移 slide，rack focus 从奶瓶到孩子。 | 摇瓶节奏接窗外树叶晃动，进入孩子提问。 | 轻轻摇匀声。孩子：森林也喝阳光吗？ | 生成2张：A 妈妈拧紧并轻摇奶瓶；B 孩子趴在桌边望向窗外。 | `[图12A]` 拧紧摇匀；`[图12B]` 孩子望向窗外 |

这样后面的 `18.0-19.5` 妈妈回答“嗯，它慢慢喝”就能顺住了：不是在冲调步骤中突然诗意，而是孩子在等待奶瓶摇匀时自然看向窗外，提问才成立。
