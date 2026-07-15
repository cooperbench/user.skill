> DEVELOPER

【紧急安全通知】Hermes Agent 依赖包 mistralai 2.4.6 被投毒，立即自查！
一、事件说明
根据安全情报，Hermes Agent 依赖的 PyPI 包 mistralai 2.4.6 版本确认被供应链投毒。
该版本在 import 时会自动执行恶意代码，属于 Mini Shai-Hulud 攻击。
二、高危风险
自动下载恶意程序到 /tmp/transformers.pyz 并后台运行
窃取环境密钥：OpenAI Key、云厂商 AK/SK、数据库密码、GitHub Token、CI/CD 凭证等
存在恶意环境变量：MISTRAL_INIT=1
外联恶意 C2 服务器：83.142.209.194
三、立即自查命令（只查不改，无风险）
# 1. 查看Python3环境 mistralai 版本
python3 -m pip show mistralai | grep -i Version || python3 - <<'PY'
import importlib.metadata as m
try:
    print("Version:", m.version("mistralai"))
except m.PackageNotFoundError:
    print("mistralai not installed")
PY

# 2. 检查恶意IOC文件
ls -la /tmp/transformers.pyz

# 3. 检查可疑进程（Mac兼容版）
pgrep -fl "/tmp/transformers.pyz"

# 4. Mac检查恶意IP外联
netstat -an | grep 83.142.209.194
lsof -nP -i | grep 83.142.209.194
四、补充
如果显示mistralai未安装，或者版本号低于2.4.6 则正常
如果已被攻击，请自行立刻停止使用受影响版本，清理安装过这些包的系统，轮换这些系统能访问到的所有密钥，检查审计日志，并监控相关 C2 连接
如果是linux服务器上部署的，请联系公共技术协助排查


查看我本地hermes

> AGENT

我先按通知里的“只查不改”路径做本机排查，同时找一下你本地可能叫 `hermes` / `Hermes` 的项目目录。先看全局 Python、IOC 文件、进程和网络连接，再进具体项目看锁文件和虚拟环境。

> AGENT

初步结果：全局 `python3` 没装 `mistralai`，`/tmp/transformers.pyz` 也不存在。进程和 `netstat` 这两项被 macOS 权限拦住了，我会用可读的 `ps` 先补一刀，同时定位本地 Hermes 项目和它自己的依赖环境。

> AGENT

我已经定位到几个 Hermes 相关位置：`/Users/lyston/PycharmProjects/hermes-webui`、`/Users/lyston/Desktop/hermes`，还有 OrbStack 里的 `hermes-agent` 容器痕迹。接下来我会分别查项目依赖文件、虚拟环境和容器镜像/运行状态，重点看有没有安装到 `mistralai==2.4.6`。

> AGENT

在 Hermes Agent 里我看到一个关键点：`pyproject.toml` 的 `mistral` extra 是 `mistralai>=2.3.0,<3`，理论上如果不用锁文件重装，会允许解析到 `2.4.6`；但 `uv.lock` 当前锁的是 `2.3.0`。我现在查实际命令入口绑定的 venv，确认“本机正在用的 hermes”有没有装到问题版本。

> AGENT

官方 Mistral 安全公告也确认了这条：受影响的是 PyPI `mistralai==2.4.6`，上传时间约为 2026-05-12 00:05 UTC，当前 PyPI 项目已隔离；恶意代码仅在 Linux 上 import 时触发。你本机 Hermes 入口指向 `/Users/lyston/PycharmProjects/hermes-agent/venv/bin/python3`，这个 venv 里实装版本是 `mistralai 2.3.2`，不是 2.4.6。

> AGENT

还有一个细节挺重要：这个投毒包据公告是“import 时触发”，所以我没有 `import mistralai`，只用 `importlib.metadata` 读安装元数据，避免碰包体执行路径。现在我继续查 Docker/OrbStack 里的 `hermes-agent` 容器，以及本地 Hermes venv 中是否出现 IOC 字符串。

> AGENT

容器层面我看到 `hermes-agent` 和 `hermes-webui` 都在跑了 7 天，时间上早于这次 PyPI 暴露窗口，但镜像/容器里仍然要查。我要进入容器只读式查询版本、IOC 文件和可疑进程；这一步不会修改容器。

> AGENT

容器里的第一条已经出来：`hermes-agent` 容器内没有安装 `mistralai`，`/tmp/transformers.pyz` 不存在，`MISTRAL_INIT` 未设置。刚才 `pgrep` 误把检查命令自身匹配进去了，我会用 `/proc` 方式重新查进程和网络连接，避免自匹配。

> AGENT

`hermes-webui` 容器也没有安装 `mistralai`，IOC 文件和 `MISTRAL_INIT` 都没看到。两个 `/proc` 检查命令没有吐出结果，我怀疑是 heredoc 传 stdin 的方式在容器里被吞了，换成 `python3 -c` 再跑一次，取明确输出。

> AGENT

有两个容器进程检查命令又把“检查命令本身”扫进去了，典型自匹配噪声，不代表发现恶意进程。我会排除当前检查进程再复核；同时对宿主机的 `ps/netstat/lsof` 做一次提权只读查询，因为前面被 macOS 权限拦截了。

> AGENT

最后一段容器 `find` 发现的是非受影响版本：`hermes-agent` 容器里有 `2.4.3`/`2.3.2`，`hermes-webui` 容器里有 `2.4.4`，都不是官方列出的 PyPI `2.4.6`。我再看一下这几个容器当前实际进程命令行，确认运行用的是哪个 venv。

> AGENT

官方公告还列了 npm 版的受影响包，我顺手也扫一下 Hermes 的 `package-lock.json`/`node_modules`，因为 `hermes-agent` 目录里确实有 Node 依赖。Python 这条目前已经基本干净，剩下是把边角检查闭合。

> AGENT

查完了。结论：你本地 Hermes 目前没有命中 `mistralai==2.4.6`，也没有看到这次 IOC。

关键结果：

- 宿主机全局 `python3`：`mistralai not installed`
- 本地 Hermes CLI：`/Users/lyston/.local/bin/hermes` 指向 `/Users/lyston/PycharmProjects/hermes-agent/venv/bin/python3`
- 该 venv 实装版本：`mistralai 2.3.2`
- [uv.lock](/Users/lyston/PycharmProjects/hermes-agent/uv.lock:2926) 锁的是 `mistralai 2.3.0`
- [pyproject.toml](/Users/lyston/PycharmProjects/hermes-agent/pyproject.toml:65) 里 `mistral` extra 是 `mistralai>=2.3.0,<3`，未来如果不用锁文件重新解析依赖，建议加排除 `!=2.4.6` 或 pin 到安全版本

容器也查了：

- `hermes-agent`：运行 venv 里是 `mistralai 2.4.3`，另一个 venv 是 `2.3.2`
- `hermes-webui`：`mistralai 2.4.4`
- `hermes-dashboard`：`2.4.2` / `2.3.2`
- 都不是 `2.4.6`

IOC 检查结果：

- `/tmp/transformers.pyz`：宿主机和 Hermes 容器内都不存在
- `MISTRAL_INIT`：未设置
- `/tmp/transformers.pyz` 可疑进程：未发现
- `83.142.209.194` 外联：宿主机和容器内都未发现
- npm 侧 `@mistralai/*` 受影响包和 `router_init.js` / `tanstack_runner.js`：Hermes 里未发现

官方公告确认受影响的是 PyPI `mistralai==2.4.6`，且以前版本不受该公告影响；恶意代码在 Linux 上 import 时触发。参考：[Mistral Security Advisories](https://docs.mistral.ai/resources/security-advisories)。

我没有做任何修改或清理，只做了只读排查。当前看不需要因为本机 Hermes 轮换密钥；真正要注意的是以后别让 Hermes 的 `mistral` extra 重新解析到 `2.4.6`。
