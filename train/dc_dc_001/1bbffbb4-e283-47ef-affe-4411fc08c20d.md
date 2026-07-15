> DEVELOPER

请深入调查 /root/shared-nvme/openbmb/infllmv2_cuda_impl/ 目录，搞清楚以下问题：

1. 读取 setup.py，看 CUDA arch 编译目标是否包含 sm_120
2. 检查 build/ 目录结构，看是否有已编译的 .so 文件
3. 读取 infllm_v2/infllmv2_sparse_attention.py（重点看 infllmv2_attn_stage1 函数周围的代码，特别是 GPU 架构检查逻辑）
4. 检查 /root/shared-nvme/openbmb/infllmv2_cuda_impl/csrc/ 下是否有 sm_120 相关的修改
5. 读取 /root/shared-nvme/openbmb/docs/ 下的所有文档（特别是 bug_fixes.md）中关于 infllmv2 / FlashAttention / Blackwell / sm_120 的记录
6. 检查 /root/shared-nvme/openbmb/logs/ 下所有日志文件（按修改时间列举），读取最近几个（特别是 sglang_sparse_probe.log, sglang_dense_probe.log, sglang_server.log），看服务是否已经成功跑起来过
7. 检查 /root/shared-nvme/openbmb/scripts/ 目录下的脚本内容
8. 检查 /root/shared-nvme/openbmb/outputs/ 目录下是否有评测结果

请把所有文件内容完整返回，不要省略关键信息。

> AGENT

正在并行读取与搜索相关文件。

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/infllmv2_cuda_impl/setup.py",
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/infllmv2_cuda_impl/setup.py"
}
```

> TOOL

tool_result read_file_v2
```
null
```

> TOOL

tool_use glob_file_search
```json
{
  "targetDirectory": "/root/shared-nvme/openbmb/infllmv2_cuda_impl/build",
  "globPattern": "**/*"
}
```

> TOOL

tool_result glob_file_search
```
null
```

> TOOL

tool_use ripgrep_raw_search
```json
{
  "pattern": "sm_120|120",
  "path": "/root/shared-nvme/openbmb/infllmv2_cuda_impl/csrc",
  "caseInsensitive": false
}
```

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/infllmv2_cuda_impl/infllm_v2/infllmv2_sparse_attention.py",
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/infllmv2_cuda_impl/infllm_v2/infllmv2_sparse_attention.py"
}
```

> TOOL

tool_result read_file_v2
```
null
```

> TOOL

tool_use glob_file_search
```json
{
  "targetDirectory": "/root/shared-nvme/openbmb/docs",
  "globPattern": "**/*"
}
```

> TOOL

tool_result glob_file_search
```
null
```

> TOOL

tool_use glob_file_search
```json
{
  "targetDirectory": "/root/shared-nvme/openbmb/logs",
  "globPattern": "**/*"
}
```

> TOOL

tool_result glob_file_search
```
null
```

> TOOL

tool_use glob_file_search
```json
{
  "targetDirectory": "/root/shared-nvme/openbmb/scripts",
  "globPattern": "**/*"
}
```

> TOOL

tool_result glob_file_search
```
null
```

> TOOL

tool_use glob_file_search
```json
{
  "targetDirectory": "/root/shared-nvme/openbmb/outputs",
  "globPattern": "**/*"
}
```

> TOOL

tool_result glob_file_search
```
null
```

> TOOL

tool_use ripgrep_raw_search
```json
{
  "pattern": "\\.so",
  "path": "/root/shared-nvme/openbmb/infllmv2_cuda_impl",
  "caseInsensitive": false
}
```

> TOOL

tool_use glob_file_search
```json
{
  "targetDirectory": "/root/shared-nvme/openbmb/infllmv2_cuda_impl",
  "globPattern": "**/*.so"
}
```

> TOOL

tool_result glob_file_search
```
null
```

> TOOL

tool_use ripgrep_raw_search
```json
{
  "pattern": "infllmv2|FlashAttention|Blackwell|sm_120",
  "path": "/root/shared-nvme/openbmb/docs",
  "caseInsensitive": true
}
```

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/docs/bug_fixes.md",
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/docs/bug_fixes.md"
}
```

> TOOL

tool_result read_file_v2
```
null
```

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/logs/sglang_sparse_probe.log",
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/logs/sglang_sparse_probe.log"
}
```

> TOOL

tool_result read_file_v2
```
null
```

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/logs/sglang_dense_probe.log",
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/logs/sglang_dense_probe.log"
}
```

> TOOL

tool_result read_file_v2
```
null
```

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/logs/sglang_server.log",
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/logs/sglang_server.log"
}
```

> TOOL

tool_result read_file_v2
```
null
```

> TOOL

tool_use ripgrep_raw_search
```json
{
  "pattern": "Ampere|sm_80|compute_capability|SM86|device_prop",
  "path": "/root/shared-nvme/openbmb/infllmv2_cuda_impl/csrc",
  "caseInsensitive": false
}
```

> TOOL

tool_use ripgrep_raw_search
```json
{
  "pattern": "varlen_fwd_stage1",
  "path": "/root/shared-nvme/openbmb/infllmv2_cuda_impl",
  "caseInsensitive": false
}
```

> TOOL

tool_use run_terminal_command_v2
```json
{
  "command": "ls -lt /root/shared-nvme/openbmb/logs/",
  "cwd": "",
  "options": {
    "timeout": 30000
  },
  "parsingResult": {
    "executableCommands": [
      {
        "name": "ls",
        "args": [
          {
            "type": "word",
            "value": "-lt"
          },
          {
            "type": "word",
            "value": "/root/shared-nvme/openbmb/logs/"
          }
        ],
        "fullText": "ls -lt /root/shared-nvme/openbmb/logs/"
      }
    ]
  },
  "commandDescription": "List logs by modification time (newest first)"
}
```

> TOOL

tool_result run_terminal_command_v2
```
null
```

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/docs/nvfp4_quantization_report.md",
  "limit": 50,
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/docs/nvfp4_quantization_report.md"
}
```

> TOOL

tool_result read_file_v2
```
null
```

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/docs/nvfp4_plan.md",
  "limit": 300,
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/docs/nvfp4_plan.md"
}
```

> TOOL

tool_result read_file_v2
```
null
```

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/docs/evaluation-guide.md",
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/docs/evaluation-guide.md"
}
```

> TOOL

tool_result read_file_v2
```
null
```

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/docs/official-image-env.md",
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/docs/official-image-env.md"
}
```

> TOOL

tool_result read_file_v2
```
null
```

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/infllmv2_cuda_impl/csrc/flash_attn/flash_api.cpp",
  "offset": 340,
  "limit": 100,
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/infllmv2_cuda_impl/csrc/flash_attn/flash_api.cpp"
}
```

> TOOL

tool_result read_file_v2
```
null
```

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/infllmv2_cuda_impl/csrc/flash_attn/flash_api.cpp",
  "offset": 760,
  "limit": 120,
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/infllmv2_cuda_impl/csrc/flash_attn/flash_api.cpp"
}
```

> TOOL

tool_result read_file_v2
```
null
```

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_launch_template.h",
  "offset": 255,
  "limit": 100,
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_launch_template.h"
}
```

> TOOL

tool_result read_file_v2
```
null
```

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/scripts/run_public_eval_full.sh",
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/scripts/run_public_eval_full.sh"
}
```

> TOOL

tool_result read_file_v2
```
null
```

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/scripts/start_public_eval_server.sh",
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/scripts/start_public_eval_server.sh"
}
```

> TOOL

tool_result read_file_v2
```
null
```

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/scripts/replay_failed_cases.sh",
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/scripts/replay_failed_cases.sh"
}
```

> TOOL

tool_result read_file_v2
```
null
```

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/scripts/run_public_eval_full.py",
  "limit": 80,
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/scripts/run_public_eval_full.py"
}
```

> TOOL

tool_result read_file_v2
```
null
```

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/scripts/replay_failed_cases.py",
  "limit": 80,
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/scripts/replay_failed_cases.py"
}
```

> TOOL

tool_result read_file_v2
```
null
```

> TOOL

tool_use ripgrep_raw_search
```json
{
  "pattern": "Ampere GPUs or newer",
  "path": "/root/shared-nvme/openbmb/infllmv2_cuda_impl",
  "caseInsensitive": false
}
```

> TOOL

tool_use ripgrep_raw_search
```json
{
  "pattern": "TORCH_CHECK.*sm",
  "path": "/root/shared-nvme/openbmb/infllmv2_cuda_impl/csrc",
  "caseInsensitive": false
}
```

> TOOL

tool_use ripgrep_raw_search
```json
{
  "pattern": "FlashAttention only supports Ampere",
  "path": "/root/shared-nvme/openbmb",
  "caseInsensitive": false
}
```

> TOOL

tool_use ripgrep_raw_search
```json
{
  "pattern": "Ampere|is_sm8x|cc_major == 12",
  "path": "/root/shared-nvme/openbmb/infllmv2_cuda_impl/csrc",
  "caseInsensitive": false
}
```

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/infllmv2_cuda_impl/csrc/flash_attn/flash_api.cpp",
  "offset": 870,
  "limit": 200,
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/infllmv2_cuda_impl/csrc/flash_attn/flash_api.cpp"
}
```

> TOOL

tool_result read_file_v2
```
null
```

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/outputs/full_public_eval_live/summary_final.json",
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/outputs/full_public_eval_live/summary_final.json"
}
```

> TOOL

tool_result read_file_v2
```
null
```

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/outputs/full_public_eval_live/summary_incremental.json",
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/outputs/full_public_eval_live/summary_incremental.json"
}
```

> TOOL

tool_result read_file_v2
```
null
```

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/outputs/20260326_174305/summary.json",
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/outputs/20260326_174305/summary.json"
}
```

> TOOL

tool_result read_file_v2
```
null
```

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/outputs/20260326_163026/summary.json",
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/outputs/20260326_163026/summary.json"
}
```

> TOOL

tool_result read_file_v2
```
null
```

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/outputs/replay_failed_cases/20260326_122046/summary.json",
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/outputs/replay_failed_cases/20260326_122046/summary.json"
}
```

> TOOL

tool_result read_file_v2
```
null
```

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/logs/sglang_probe.log",
  "limit": 80,
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/logs/sglang_probe.log"
}
```

> TOOL

tool_result read_file_v2
```
null
```

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/logs/sglang_test.log",
  "limit": 80,
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/logs/sglang_test.log"
}
```

> TOOL

tool_result read_file_v2
```
null
```

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/logs/sglang_debug_small.log",
  "limit": 130,
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/logs/sglang_debug_small.log"
}
```

> TOOL

tool_result read_file_v2
```
null
```

> TOOL

tool_use run_terminal_command_v2
```json
{
  "command": "for f in /root/shared-nvme/openbmb/logs/*.log; do stat -c '%Y %n' \"$f\"; done | sort -rn | awk '{print $2}'",
  "cwd": "",
  "options": {
    "timeout": 30000
  },
  "parsingResult": {
    "executableCommands": [
      {
        "name": "stat",
        "args": [
          {
            "type": "word",
            "value": "-c"
          },
          {
            "type": "raw_string",
            "value": "'%Y %n'"
          },
          {
            "type": "string",
            "value": "\"$f\""
          }
        ],
        "fullText": "stat -c '%Y %n' \"$f\""
      },
      {
        "name": "sort",
        "args": [
          {
            "type": "word",
            "value": "-rn"
          }
        ],
        "fullText": "sort -rn"
      },
      {
        "name": "awk",
        "args": [
          {
            "type": "raw_string",
            "value": "'{print $2}'"
          }
        ],
        "fullText": "awk '{print $2}'"
      }
    ]
  },
  "commandDescription": "Sort log files by mtime descending"
}
```

> TOOL

tool_result run_terminal_command_v2
```
null
```

> TOOL

tool_use read_file_v2
```json
{
  "targetFile": "/root/shared-nvme/openbmb/docs/nvfp4_quantization_report.md",
  "offset": 50,
  "charsLimit": 1000000,
  "effectiveUri": "/root/shared-nvme/openbmb/docs/nvfp4_quantization_report.md"
}
```

> TOOL

tool_result read_file_v2
```
null
```

> TOOL

tool_use glob_file_search
```json
{
  "targetDirectory": "/root/shared-nvme/openbmb/infllmv2_cuda_impl/infllm_v2",
  "globPattern": "**/*"
}
```

> TOOL

tool_result glob_file_search
```
null
```

> TOOL

tool_use ripgrep_raw_search
```json
{
  "pattern": ".",
  "path": "/root/shared-nvme/openbmb/infllmv2_cuda_impl/infllm_v2/__init__.py",
  "caseInsensitive": false
}
```

> AGENT

以下为只读调查结论；路径均使用绝对路径 `/root/shared-nvme/openbmb/...`。

---

## 1. `setup.py` 与 CUDA Arch（是否包含 sm_120）

`/root/shared-nvme/openbmb/infllmv2_cuda_impl/setup.py` 在 `CUDA_HOME` 可用时按 **nvcc 报告版本** 累加架构，并在最后统一加 `-gencode`：

- 始终包含 **80**（Ampere）。
- `bare_metal_version >= 11.8` 时追加 **90**。
- `bare_metal_version >= 12.8` 时追加 **120**（注释写明对应 Blackwell）。

循环逻辑为对每个 `arch` 执行  
`-gencode arch=compute_${arch},code=sm_${arch}`，因此 **在 CUDA 工具链版本 ≥ 12.8 的配置下，编译目标会包含 sm_120**。

相关片段：

```100:110:/root/shared-nvme/openbmb/infllmv2_cuda_impl/setup.py
    # Auto-detect supported GPU archs based on CUDA toolkit version
    # 80: A100 (Ampere), 90: H100 (Hopper, CUDA 11.8+), 120: B100/B200 (Blackwell, CUDA 12.8+)
    supported_archs = ["80"]
    if CUDA_HOME is not None:
        if bare_metal_version >= Version("11.8"):
            supported_archs.append("90")
        if bare_metal_version >= Version("12.8"):
            supported_archs.append("120")

    for arch in supported_archs:
        cc_flag.extend(["-gencode", f"arch=compute_{arch},code=sm_{arch}"])
```

---

## 2. `build/` 目录与已编译 `.so`

在 `/root/shared-nvme/openbmb/infllmv2_cuda_impl/build` 下检索到的内容为：

- `temp.linux-x86_64-cpython-310/`：`.ninja_log`、`build.ninja`
- `lib.linux-x86_64-cpython-310/infllm_v2/`：若干 **Python 文件副本**（如 `infllmv2_sparse_attention.py`、`__init__.py` 等）

**未发现** `*.so`（全树 `**/*.so` 搜索为 0；`.gitignore` 含 `*.so`）。  
`infllm_v2/` 源码目录下列出文件亦无 `C*.so`。因此：**当前仓库内这一棵 `infllmv2_cuda_impl` 要么未在本路径完成扩展编译落盘，要么 `.so` 在安装目录/被忽略路径中**；运行时若仍能 `import` `C`，通常来自环境中已安装的同名包。

---

## 3. `infllmv2_attn_stage1`（Python）与 GPU 检查

文件：`/root/shared-nvme/openbmb/infllmv2_cuda_impl/infllm_v2/infllmv2_sparse_attention.py`

- **`infllmv2_attn_stage1`（约 483–611 行）在 Python 层没有** `torch.cuda.get_device_capability` / `sm_120` 等 **GPU 架构分支**。
- 逻辑为：可选 `softmax_scale`、tensor 连续化、按 GQA  reshape `q`，然后调用 **`infllm_cuda.varlen_fwd_stage1(...)`**（即 C++/CUDA 扩展）。

架构相关排查需在 **`mha_varlen_fwd_stage1`（C++）** 及 **`run_mha_fwd` / launch 模板** 中完成（见下节）。

---

## 4. `csrc/` 与 sm_120

在 `/root/shared-nvme/openbmb/infllmv2_cuda_impl/csrc` 下对 `sm_120`、`120` 等 **无匹配**（无针对 Blackwell 的硬编码字样）。  
**sm_120 是否参与产物**由上层 **`setup.py` 的 `cc_flag`** 决定，而非在 `csrc` 里写死。

`flash_api.cpp` 中 **`mha_varlen_fwd_stage1`** 仍 **读取** `cc_major/cc_minor` 并设置 `is_sm8x`、`is_sm90`，但 **“FlashAttention only supports Ampere GPUs or newer.” 的 `TORCH_CHECK` 在仓库源码里已全部注释掉**（与其它几个 forward 入口一致）。例如 stage1 一段：

```811:824:/root/shared-nvme/openbmb/infllmv2_cuda_impl/csrc/flash_attn/flash_api.cpp
    auto [cc_major, cc_minor] = get_compute_capability(get_current_device());
    // bool is_sm75 = cc_major == 7 && cc_minor == 5;
    bool is_sm8x = cc_major == 8 && cc_minor >= 0;
    bool is_sm90 = cc_major == 9 && cc_minor == 0;
    // TORCH_CHECK(is_sm90 || is_sm8x, "FlashAttention only supports Ampere GPUs or newer.");
    ...
    if (q_dtype == torch::kBFloat16) {
        // TORCH_CHECK(is_sm90 || is_sm8x, "bfloat16 is only supported on Ampere GPUs or newer");
    }
```

`flash_fwd_launch_template.h` 里仅有 **`cc_major == 8 && cc_minor > 0`** 的 `is_sm8x` 分支，用于 **kernel 变体选择**，**未**出现 `12`/Blackwell 特化；Blackwell 上会走 **`else` 分支**（与 “非 sm86+ 的 8.x” 同类路径），属运行期启发式，不是 sm_120 专用实现。

**与日志的矛盾**：`logs/sglang_sparse_probe.log` / `sglang_debug_small.log` 中仍出现 **`RuntimeError: FlashAttention only supports Ampere GPUs or newer.`**，而 **当前仓库里的对应 `TORCH_CHECK` 已注释**。合理解释是：**实际加载的 `infllm_v2` C 扩展二进制与当前工作区源码不一致**（例如环境内旧 wheel/`setup.py install` 产物未重编），需以环境中 `infllm_v2.C` 的实际 `.so` 为准核对。

---

## 5. `docs/` 中与 infllmv2 / FlashAttention / Blackwell / sm_120

### `bug_fixes.md`（全文要点，无 sm_120 专节）

路径：`/root/shared-nvme/openbmb/docs/bug_fixes.md`（共 98 行）。与 infllmv2 直接相关段落：

- **§1 infllm_v2**：写明 conda 已装 `infllm_v2`、代码 **硬导入**；并说明 **当前 NVFP4 推理路径未走稀疏 attention backend**，**一般不调用 infllm_v2 的两个 kernel**，稀疏路径里只参与 TopK。
- **§6**：`quantize_nvfp4.py` 校准需暂时 `sparse_config = None`，导出前要还原，否则 `has_sparse_attention = False`、无法用 `minicpm_flashinfer` 等。

**全文未出现** “sm_120”“Blackwell”“FlashAttention” 等字样（我已读完整文件）。

### 其他文档摘录

| 文件 | 相关内容 |
|------|----------|
| `docs/nvfp4_plan.md` §九 | FA3 标为 SM90、**SM_120 不支持**；FA4 写 SM80/90/100/**SM120**、beta、CUDA 13，短期不可用 |
| `docs/evaluation-guide.md` | 评测 GPU：**RTX PRO 6000，Blackwell** |
| `docs/official-image-env.md` | `infllmv2_cuda_impl` 镜像内 **`python setup.py install`**；**sgl-kernel** 用 `TORCH_CUDA_ARCH_LIST="12.0;12.0a"` **针对 sm_120** 重编 |

`docs/nvfp4_quantization_report.md` 为 NVFP4 量化审计长文（层统计、ModelOpt、改进建议等），**不涉及** infllmv2 kernel 或 sm_120 运行时细节。完整内容见该路径（约 381 行）。

---

## 6. `logs/` 日志（列举与关键内容）

目录下共有 9 个 `.log`（glob）：  
`sglang_debug_small.log`, `sglang_sparse_probe.log`, `sglang_dense_probe.log`, `sglang_probe.log`, `sglang_test.log`, `quantize_v3.log`, `quantize_debug.log`, `sglang_server.log`, `quantize_nvfp4.log`。  
沙箱内 `ls -lt`/`stat` 无可用输出，以下按 **日志内时间戳** 归纳近因：

| 日志 | 时间戳（文内） | 结论摘要 |
|------|----------------|----------|
| `sglang_debug_small.log` | 2026-03-26 **15:07** | `minicpm_flashinfer` + `dense_as_sparse`，CUDA Graph 捕获时在 **`infllmv2_attn_stage1` → `varlen_fwd_stage1`** 报 **FlashAttention only supports Ampere…**，调度器失败 |
| `sglang_sparse_probe.log` | **13:34** | 同上失败路径（端口 30003，`dense_as_sparse=True`） |
| `sglang_dense_probe.log` | **13:28** | **`attention_backend=flashinfer`**，`force_dense_minicpm=True`，**权重与 Graph 成功**；**Uvicorn 30002 正常**；`openai_harmony` 缺失仅影响部分 OpenAI 路由；**有多条 200 OK** |
| `sglang_probe.log` | **13:18** | 早期失败：`ModuleNotFoundError: sparse_kernel_extension` |
| `sglang_test.log` | **13:12** | **`Not enough memory` / `mem_fraction_static=0.85`** |
| `sglang_server.log` | **02:32** | **MiniCPM-SALA-NVFP4**（v1 路径）、`flashinfer`、`disable_cuda_graph=True`、**服务 30000 起来并成功处理请求** |

**结论**：  
- **稀疏路径（`minicpm_flashinfer` + 实际走到 `infllmv2_attn_stage1`）在 Graph 捕获阶段失败**，与上面 **Ampere 报错** 一致。  
- **稠密/非稀疏探测（`sglang_dense_probe.log`）服务已成功跑起来并完成推理请求。**  
- **整体上服务在多种配置下曾有成功实例**（尤其 dense probe 与早期 v1 `sglang_server.log`）。

---

## 7. `scripts/` 脚本

| 文件 | 作用（概要） |
|------|----------------|
| `run_public_eval_full.sh` | `cd` 到 openbmb，执行 `soar` 的 `python3 scripts/run_public_eval_full.py`，默认 `--api-base http://127.0.0.1:30000`、`MiniCPM-SALA-NVFP4-v2`、`--concurrency 8`。**注意**：第 10–11 行 **`--concurrency 8` 后缺少行尾 `\`**，`--mem-fraction-static` 可能被当作单独命令（shell 脚本瑕疵）。 |
| `start_public_eval_server.sh` | 设置 `PYTHONPATH=.../demo-sala/sglang/python:.../infllmv2_cuda_impl`，启动 `sglang.launch_server`，**`minicpm_flashinfer`、`dense-as-sparse`、8192 chunk** 等 |
| `replay_failed_cases.sh` | 调用 `replay_failed_cases.py`，固定失败样本索引重放 |
| `run_public_eval_full.py` |  públic 评测：并发请求、`outputs/full_public_eval_live` 增量写盘、`max_seq_len` 默认 262144 等 |
| `replay_failed_cases.py` | 硬编码 `FAILED_INDICES` 列表，对失败题重跑并写 `outputs/replay_failed_cases/...` |

---

## 8. `outputs/` 评测结果

存在多组结果，摘要如下（**不代表官方 `eval_model.py` 唯一口径**，部分为自建脚本输出）：

- `outputs/full_public_eval_live/summary_final.json`：`ori_accuracy` **65.8**，`overall_accuracy` **82.25**，150 样本，`duration` ~2340 s。  
- `summary_incremental.json`：仅完成 **34/150**，部分准确率 **70.59%**。  
- `outputs/20260326_174305/summary.json`：`ori_accuracy` **81.33**，`overall_accuracy` **100**（相对基准 80 的展示方式需结合脚本）。  
- `outputs/20260326_163026/summary.json`：`ori_accuracy` **75.0**，`overall_accuracy` **93.75**。  
- `outputs/replay_failed_cases/20260326_122046/summary.json`：23 例中 **ok=2，err=21**。

另有 `full_public_eval/chunks/`、`predictions*.jsonl` 等中间产物。

---

## 汇总表

| 问题 | 结论 |
|------|------|
| sm_120 是否在 setup 目标里 | **条件满足（CUDA ≥ 12.8）时会加入 compute_120/sm_120** |
| build 里是否有 .so | **未见**；`infllm_v2` 源码树亦无 `C*.so` |
| `infllmv2_attn_stage1` GPU 检查 | **Python 无**；C++ 里相关 **Ampere TORCH_CHECK 在源码中已注释** |
| csrc sm_120 修改 | **无**；架构由 `setup.py` 的 gencode 决定 |
| docs | `bug_fixes.md` **无 Blackwell/sm_120 专论**；`nvfp4_plan` / `official-image-env` / `evaluation-guide` 有 Blackwell 或 sm_120 上下文 |
| 服务是否成功跑过 | **是**：`sglang_dense_probe.log`、`sglang_server.log` 有完整启动与 **200 OK**；稀疏 + infllmv2 stage1 路径在多个 log 中 **CUDA Graph 阶段失败** |

若你需要下一步在 Agent 模式下 **强制对齐“源码 vs 已安装 `infllm_v2.C`”**（重编扩展或查 `site-packages` 中 `.so`），可以切换模式后由我改环境并验证。
