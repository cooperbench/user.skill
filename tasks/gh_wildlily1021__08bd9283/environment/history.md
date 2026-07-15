> DEVELOPER

有个需求，需要你去改一些旧程序，编几个图。public\data\frames\configs里需要添加一些帧去适配我要编的东西。右侧遥测界面(依据右侧这张遥测结果图修改)：
将“激光链路标准测试设备”改为“激光模拟器”；增加“波长状态：1563nm”；“信号功率”采用1000~1200之间的随机数；“频偏估计值”采用-50~+50之间的随机数；”编码方式“默认”RS编码“；“发送速率”、“接收速率”默认“5G”；”载波同步锁定“、”定时同步锁定“、”帧同步锁定“默认“锁定”；"译码前误bit数""译码后误bit数"修改为"译码前误码率""译码后误码率"，默认”0“；”帧计数“默认”625000“；”数据帧计数“默认”0“；”误帧计数“默认”0“；”数据误帧计数“默认”0“；删除”粗测距“”细测距“”测距值（ps）“”测距值（cm）“ 第一张遥测界面图为“波长状态：1563nm”；第二张遥测界面图为“波长状态：1540nm”；
第一张遥测界面图“译码前误码率”改为“6.3e-7”
第一张遥测界面图“帧计数”改为“0”；第二张遥测界面图“译码前误码率”改为“3.5e-2”、“译码后误码率”改为“2.3e-2”
第一张遥控设置界面图为，编码方式切换为”LDPC“的图；第二张遥测界面图为”编码方式“默认”LDPC编码“
四张遥测界面图“发送速率”、“接收速率”分别为”2.5G“、”1.25G“、”625M“、”312.5M“，对应的”帧计数“分别为”312500“、”156250“、”78125“、”39062“
第一张遥测界面图”数据帧计数“修改为“59219”
 你先理解一下。让子agent检索可能需要改什么

> DEVELOPER

有个需求，需要你去改一些旧程序，编几个图。public\data\frames\configs里需要添加一些帧去适配我要编的东西。右侧遥测界面(依据右侧这张遥测结果图修改)：
将“激光链路标准测试设备”改为“激光模拟器”；增加“波长状态：1563nm”；“信号功率”采用1000~1200之间的随机数；“频偏估计值”采用-50~+50之间的随机数；”编码方式“默认”RS编码“；“发送速率”、“接收速率”默认“5G”；”载波同步锁定“、”定时同步锁定“、”帧同步锁定“默认“锁定”；"译码前误bit数""译码后误bit数"修改为"译码前误码率""译码后误码率"，默认”0“；”帧计数“默认”625000“；”数据帧计数“默认”0“；”误帧计数“默认”0“；”数据误帧计数“默认”0“；删除”粗测距“”细测距“”测距值（ps）“”测距值（cm）“ 第一张遥测界面图为“波长状态：1563nm”；第二张遥测界面图为“波长状态：1540nm”；
第一张遥测界面图“译码前误码率”改为“6.3e-7”
第一张遥测界面图“帧计数”改为“0”；第二张遥测界面图“译码前误码率”改为“3.5e-2”、“译码后误码率”改为“2.3e-2”
第一张遥控设置界面图为，编码方式切换为”LDPC“的图；第二张遥测界面图为”编码方式“默认”LDPC编码“
四张遥测界面图“发送速率”、“接收速率”分别为”2.5G“、”1.25G“、”625M“、”312.5M“，对应的”帧计数“分别为”312500“、”156250“、”78125“、”39062“
第一张遥测界面图”数据帧计数“修改为“59219”
 你先理解一下。让子agent检索可能需要改什么。应该不需要改代码（可能要改点名字）。主要是加几个帧配置，让到时候能够直接本地收发（帧格式无所谓，只要收发都有这些参数，然后收到之后就可以显示出来），然后就能截图了（我只为截图）。

> AGENT

明白了。核心目标是：**加几条帧配置，让本地收发能跑起来，截 4 张不同参数组合的遥测界面图**。不改核心代码逻辑，最多改个显示名称。

让子 agent 并行检索三个方向：帧配置结构、遥测显示组件、现有的激光相关代码。

> TOOL

tool_use Agent
id: call_322a79e28c1e400c990790ed
```json
{
  "description": "检索帧配置结构",
  "subagent_type": "Explore",
  "prompt": "Thoroughness: medium\n\nExplore the frame configuration structure in `public/data/frames/configs/`. I need to understand:\n1. What JSON files exist there and their naming convention\n2. The schema/structure of a frame config (fields, types, how parameters are defined)\n3. Any existing configs related to \"激光\" (laser) or \"链路\" (link) or \"SCOE\" or telemetry\n4. How frame configs are consumed — search for imports/references to these config files in the old codebase (`src/` not `rewrite/`)\n\nAlso check `public/data/frames/` for any index or registry file that lists available frames.\n\nReport the full JSON structure of at least one representative config file."
}
```

> TOOL

tool_use Agent
id: call_b5e10023f6ca4d7997f764bd
```json
{
  "description": "检索遥测显示组件",
  "subagent_type": "Explore",
  "prompt": "Thoroughness: medium\n\nSearch the OLD codebase (`src/` NOT `rewrite/`) for the right-side telemetry display interface. The user mentions a \"遥测界面\" that currently shows fields like \"激光链路标准测试设备\", \"信号功率\", \"频偏估计值\", \"编码方式\", \"发送速率\", \"接收速率\", \"载波同步锁定\", \"定时同步锁定\", \"帧同步锁定\", \"译码前误bit数\", \"译码后误bit数\", \"帧计数\", \"数据帧计数\", \"误帧计数\", \"数据误帧计数\", \"粗测距\", \"细测距\", \"测距值\".\n\nFind:\n1. The Vue component(s) that render this telemetry display\n2. How field labels are defined (hardcoded strings? from config? from frame data?)\n3. How the fields map to data — what determines which fields show up\n4. Any relevant store or data flow for telemetry results\n\nReport file paths and key code snippets showing the field rendering logic."
}
```

> TOOL

tool_use Agent
id: call_13cc5eb6f979455b8761abe7
```json
{
  "description": "检索激光模拟器相关代码",
  "subagent_type": "Explore",
  "prompt": "Thoroughness: medium\n\nSearch the OLD codebase (`src/` NOT `rewrite/`) for anything related to:\n1. \"激光链路标准测试设备\" — where this string appears\n2. \"激光模拟器\" — if it already exists anywhere\n3. \"波长状态\" or \"wavelength\" — any wavelength-related fields\n4. How the telemetry simulation/local send-receive works — search for \"localSend\", \"local send\", \"模拟\", \"simulate\" patterns in context of frame sending/receiving\n\nAlso check if there's a way to do local loopback (send and receive locally) for screenshot purposes — look for any \"local\" or \"loopback\" or \"自发自收\" patterns in the serial/network communication code.\n\nReport all file paths and relevant code found."
}
```

> TOOL

tool_result
id: call_13cc5eb6f979455b8761abe7
```
Now let me compile the final report with all the findings:

## Search Report: OLD Codebase Analysis

Based on my thorough search of the `src/` directory (excluding `rewrite/`), here are my findings:

### 1. **"激光链路标准测试设备" - Device Name**
**Found in 2 files:**
- `/mnt/d/code/frontend/dongfanghong/src/pages/home/HomePage.vue` (line 4)
- `/mnt/d/code/frontend/dongfanghong/src/components/layout/HeaderBar.vue` (line 8)

**Usage:** This is the application title displayed in the header and home page.

### 2. **"激光模拟器" - Laser Simulator**
**NOT FOUND** - No existing laser simulator functionality in the old codebase.

### 3. **"波长状态" or "wavelength" - Wavelength State**
**NOT FOUND** - No wavelength-related fields or functionality exist in the current codebase.

### 4. **Telemetry Simulation/Local Send-Receive**
**Key findings:**

**A. Local Send Instance (SCOE Frame Management)**
- `/mnt/d/code/frontend/dongfanghong/src/stores/frames/scoeFrameInstancesStore.ts` (lines 40, 146, 156, 164, 174, 184, 200, 216, 581)
  - Contains `localSendInstance` ref for editing frame instances
  - Contains `localReceiveCommand` ref for editing receive commands
  - Used for local editing before applying changes to actual instances

**B. Frame Sending Infrastructure**
- `/mnt/d/code/frontend/dongfanghong/src/composables/frames/sendFrame/useUnifiedSender.ts`
  - Unified sending router for both serial and network connections
  - `sendFrameInstance()` function (line 69) handles frame sending
  - Supports both serial (`sendToSerial()`) and network (`sendToNetwork()`) sending
  
**C. Frame Receiving Infrastructure**
- `/mnt/d/code/frontend/dongfanghong/src/stores/frames/receiveFramesStore.ts`
  - `handleReceivedData()` […]

> TOOL

tool_result
id: call_322a79e28c1e400c990790ed
```
Perfect! Now I have a comprehensive understanding. Let me create the final report:

## Frame Configuration Structure Analysis Report

Based on my exploration of `/mnt/d/code/frontend/dongfanghong/public/data/frames/configs/`, here are my findings:

### 1. JSON Files and Naming Convention

**Files found:**
- 20 JSON config files: `1.json`, `2.json`, `3.json`, `4.json`, `5.json`, `6.json`, `7.json`, `8.json`, `9.json`, `10.json`, `11.json`, `12.json`, `13.json`, `15.json`, `17.json`, `18.json`, `19.json`, `111.json`, `12345.json`, `测试.json`, `综测仪.json`

**Naming convention:**
- Numeric IDs (most common): `1.json`, `2.json`, etc.
- Descriptive Chinese names: `测试.json`, `综测仪.json`
- Mixed alphanumeric: `111.json`, `12345.json`

**Additional directories:**
- `/public/data/frames/receiveConfig/` - Contains receive configurations
- `/public/data/frames/sendInstances/` - Contains send instances  
- `/public/data/frames/taskConfigs/` - Contains task configurations
- `/public/data/frames/templates/` - Contains templates

### 2. Frame Configuration Schema/Structure

Each config file contains an **array of frame objects**. Here's the complete schema:

**Frame Object Structure:**
```typescript
{
  // Core identification
  id: string;                    // Unique identifier (e.g., "NK001", "SCOE-S-001")
  lastId: string;                // Previous ID for tracking changes
  name: string;                  // Human-readable name
  description: string;           // Optional description
  
  // Frame classification
  direction: "send" | "receive";  // Communication direction
  frameType: "custom" | "control"; // Frame type classification
  protocol: "custom";             // Protocol type
  
  // Field definitions (the core structure)
  fields: FrameField[];
  
  // Metadata
  timestamp: […]

> TOOL

tool_result
id: call_b5e10023f6ca4d7997f764bd
```
Now I have a complete understanding of the telemetry display system. Let me create a comprehensive report:

Based on my thorough exploration of the codebase, I've found the complete telemetry display interface system. Here's my report:

## Telemetry Display Interface Analysis

### 1. Vue Components that Render Telemetry Display

**Main Display Components:**
- **`/mnt/d/code/frontend/dongfanghong/src/pages/ReceiveFramePage.vue`** - Main page that switches between edit and display modes
- **`/mnt/d/code/frontend/dongfanghong/src/components/frames/receive/DataDisplay/DataDisplayContainer.vue`** - Container for the dual-table display layout  
- **`/mnt/d/code/frontend/dongfanghong/src/components/frames/receive/DataDisplay/DataTable.vue`** - Actual table component that renders telemetry fields

**Key Rendering Logic from DataTable.vue (lines 32-84):**
```vue
const columns = [
  { name: 'index', label: '编号', field: 'index', align: 'center' as const },
  { name: 'label', label: '数据名称', field: 'label', align: 'left' as const },
  { name: 'displayValue', label: '值', field: 'displayValue', align: 'center' as const },
  { name: 'hexValue', label: '十六进制', field: 'hexValue', align: 'center' as const },
  { name: 'favorite', label: '收藏', field: 'favorite', align: 'center' as const },
  { name: 'actions', label: '操作', field: 'actions', align: 'center' as const },
];
```

### 2. Field Labels Definition

**Field labels are defined in frame template JSON configurations** stored in:
- `/mnt/d/code/frontend/dongfanghong/dist/electron/Packaged/linux-unpacked/resources/public/data/frames/configs/10.json`

**Three telemetry frames found:**

1. **"系统状态帧" (R-FPGA-003)** - System […]

> AGENT

好的，三个 agent 的结果回来了。让我再确认一下现有遥测帧的具体结构。

> TOOL

tool_use Read
id: call_b1d7f48db3444c0f88552f55
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/public/data/frames/configs/10.json",
  "limit": 50
}
```

> TOOL

tool_use Grep
id: call_490fafc1aa2c4667b6049849
```json
{
  "pattern": "激光链路标准测试设备",
  "output_mode": "content",
  "-n": true,
  "context": 2,
  "path": "/mnt/d/code/frontend/dongfanghong/src"
}
```

> TOOL

tool_result
id: call_b1d7f48db3444c0f88552f55
```
1	[
2	  {
3	    "id": "NK001",
4	    "lastId": "NK001",
5	    "name": "光多普勒复位指令",
6	    "description": "",
7	    "direction": "send",
8	    "frameType": "custom",
9	    "protocol": "custom",
10	    "fields": [
11	      {
12	        "id": "uN6RewEHGco0Tyqqsra4Q",
13	        "name": "帧头码",
14	        "dataType": "uint8",
15	        "length": 1,
16	        "description": "",
17	        "validOption": {
18	          "isChecksum": false,
19	          "startFieldIndex": "0",
20	          "endFieldIndex": "0",
21	          "checksumMethod": "sum8"
22	        },
23	        "defaultValue": "0xFF",
24	        "inputType": "input",
25	        "configurable": false,
26	        "options": [],
27	        "dataParticipationType": "direct"
28	      },
29	      {
30	        "id": "RoTJNa6Amew1cpP6YXU4M",
31	        "name": "指令类型",
32	        "dataType": "uint8",
33	        "length": 1,
34	        "description": "",
35	        "validOption": {
36	          "isChecksum": false,
37	          "startFieldIndex": "0",
38	          "endFieldIndex": "0",
39	          "checksumMethod": "sum8"
40	        },
41	        "defaultValue": "0x00",
42	        "inputType": "input",
43	        "configurable": false,
44	        "options": [],
45	        "dataParticipationType": "direct"
46	      },
47	      {
48	        "id": "ZmfP9zO3ZoIZbprSLAvZa",
49	        "name": "控制字节1",
50	        "dataType": "uint8",
```

> TOOL

tool_result
id: call_490fafc1aa2c4667b6049849
```
/mnt/d/code/frontend/dongfanghong/src/pages/home/HomePage.vue-2-    <div class="flex flex-col">
/mnt/d/code/frontend/dongfanghong/src/pages/home/HomePage.vue-3-        <header class="text-center mb-8">
src/pages/home/HomePage.vue:4:            <h1 class="text-3xl font-semibold text-[#3b82f6] mb-2">激光链路标准测试设备</h1>
/mnt/d/code/frontend/dongfanghong/src/pages/home/HomePage.vue-5-        </header>
/mnt/d/code/frontend/dongfanghong/src/pages/home/HomePage.vue-6-    </div>
--
/mnt/d/code/frontend/dongfanghong/src/components/layout/HeaderBar.vue-6-          <img src="../../assets/icons/logo.svg" alt="RS485" class="h-[20px] w-[20px]" />
/mnt/d/code/frontend/dongfanghong/src/components/layout/HeaderBar.vue-7-        </div>
src/components/layout/HeaderBar.vue:8:        <div class="text-[16px] font-medium text-white m-0 tracking-wide">激光链路标准测试设备</div>
/mnt/d/code/frontend/dongfanghong/src/components/layout/HeaderBar.vue-9-      </div>
/mnt/d/code/frontend/dongfanghong/src/components/layout/HeaderBar.vue-10-
```

> TOOL

tool_use Grep
id: call_0b86d1827389462389d7974f
```json
{
  "pattern": "R-FPGA-00[123]",
  "path": "/mnt/d/code/frontend/dongfanghong/public/data/frames/configs/10.json",
  "output_mode": "content",
  "-n": true,
  "context": 0
}
```

> TOOL

tool_use Bash
id: call_160c093642aa4b94906e2253
```json
{
  "command": "wc -l /mnt/d/code/frontend/dongfanghong/public/data/frames/configs/10.json",
  "description": "Count lines in 10.json"
}
```

> TOOL

tool_result
id: call_0b86d1827389462389d7974f
```
355:    "id": "R-FPGA-001",
356:    "lastId": "R-FPGA-001",
546:    "id": "R-FPGA-003",
547:    "lastId": "R-FPGA-003",
881:    "id": "R-FPGA-002",
882:    "lastId": "R-FPGA-002",
2082:              "frameId": "R-FPGA-003",
```

> TOOL

tool_result
id: call_160c093642aa4b94906e2253
```
6138
```

> TOOL

tool_use Read
id: call_5d4436cd569a47698777ef49
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/public/data/frames/configs/10.json",
  "offset": 350,
  "limit": 200
}
```

> TOOL

tool_use Read
id: call_b91e472a3b7e4db28b671d54
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/public/data/frames/configs/10.json",
  "offset": 540,
  "limit": 350
}
```

> TOOL

tool_result
id: call_5d4436cd569a47698777ef49
```
350	      "includeLengthField": false
351	    },
352	    "identifierRules": []
353	  },
354	  {
355	    "id": "R-FPGA-001",
356	    "lastId": "R-FPGA-001",
357	    "name": "帧统计数据",
358	    "description": "",
359	    "direction": "receive",
360	    "frameType": "custom",
361	    "protocol": "custom",
362	    "fields": [
363	      {
364	        "id": "Y05eqFmYqrpIBnjq22Wtd",
365	        "name": "帧头",
366	        "dataType": "uint32",
367	        "length": 4,
368	        "description": "",
369	        "validOption": {
370	          "isChecksum": false,
371	          "startFieldIndex": "0",
372	          "endFieldIndex": "0",
373	          "checksumMethod": "sum8"
374	        },
375	        "defaultValue": "0x1ACF0001",
376	        "inputType": "input",
377	        "configurable": false,
378	        "options": [],
379	        "dataParticipationType": "direct"
380	      },
381	      {
382	        "id": "tELTPm2DsSLG2bAhjCZbR",
383	        "name": "译码前总bit数",
384	        "dataType": "uint64",
385	        "length": 8,
386	        "description": "",
387	        "validOption": {
388	          "isChecksum": false,
389	          "startFieldIndex": "0",
390	          "endFieldIndex": "0",
391	          "checksumMethod": "sum8"
392	        },
393	        "defaultValue": "0",
394	        "inputType": "input",
395	        "configurable": false,
396	        "options": [],
397	        "dataParticipationType": "direct"
398	      },
399	      {
400	        "id": "NtNNkamVYldFab8TK5A4t",
401	        "name": "译码前误bit数",
402	        "dataType": "uint64",
403	        "length": 8,
404	        "description": "",
405	        "validOption": {
406	          "isChecksum": false,
407	          "startFieldIndex": "0",
408	          "endFieldIndex": "0",
409	          "checksumMethod": "sum8"
410	        },
411	        "defaultValue": "0",
412	        "inputType": "input",
413	        "configurable": false,
414	        "options": [],
415	        "dataParticipationType": "direct"
416	      },
417	      {
418	        "id": "tmh5HQ23r1zhSspq6CuN1",
419	        "name": […]

> TOOL

tool_result
id: call_b91e472a3b7e4db28b671d54
```
540	        "value": "0x1ACF0001",
541	        "logicOperator": "and"
542	      }
543	    ]
544	  },
545	  {
546	    "id": "R-FPGA-003",
547	    "lastId": "R-FPGA-003",
548	    "name": "系统状态帧",
549	    "description": "",
550	    "direction": "receive",
551	    "frameType": "custom",
552	    "protocol": "custom",
553	    "fields": [
554	      {
555	        "id": "Y05eqFmYqrpIBnjq22Wtd",
556	        "name": "帧头",
557	        "dataType": "uint32",
558	        "length": 4,
559	        "description": "",
560	        "validOption": {
561	          "isChecksum": false,
562	          "startFieldIndex": "0",
563	          "endFieldIndex": "0",
564	          "checksumMethod": "sum8"
565	        },
566	        "defaultValue": "0x1ACF0003",
567	        "inputType": "input",
568	        "configurable": false,
569	        "options": [],
570	        "dataParticipationType": "direct"
571	      },
572	      {
573	        "id": "Y1uW6Ez-IPtiBuoQ20CIn",
574	        "name": "信号功率",
575	        "dataType": "uint16",
576	        "length": 2,
577	        "factor": 1,
578	        "description": "",
579	        "validOption": {
580	          "isChecksum": false,
581	          "startFieldIndex": "0",
582	          "endFieldIndex": "0",
583	          "checksumMethod": "sum8"
584	        },
585	        "defaultValue": "0",
586	        "inputType": "input",
587	        "configurable": false,
588	        "options": [],
589	        "dataParticipationType": "direct"
590	      },
591	      {
592	        "id": "Fod-V0Bm5_zK56vSBfiWk",
593	        "name": "频偏估计值",
594	        "dataType": "int32",
595	        "length": 4,
596	        "factor": "0.000001",
597	        "description": "",
598	        "validOption": {
599	          "isChecksum": false,
600	          "startFieldIndex": "0",
601	          "endFieldIndex": "0",
602	          "checksumMethod": "sum8"
603	        },
604	        "defaultValue": "0",
605	        "inputType": "input",
606	        "configurable": false,
607	        "options": [],
608	        "dataParticipationType": "direct"
609 […]

> TOOL

tool_use Read
id: call_1a87412532df498ab77895dc
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/public/data/frames/configs/10.json",
  "limit": 100,
  "offset": 880
}
```

> TOOL

tool_result
id: call_1a87412532df498ab77895dc
```
880	  {
881	    "id": "R-FPGA-002",
882	    "lastId": "R-FPGA-002",
883	    "name": "测距帧",
884	    "description": "",
885	    "direction": "receive",
886	    "frameType": "custom",
887	    "protocol": "custom",
888	    "fields": [
889	      {
890	        "id": "uInt4TYH6mOW_ZJQvb51w",
891	        "name": "帧头",
892	        "dataType": "uint32",
893	        "length": 4,
894	        "factor": 1,
895	        "description": "",
896	        "validOption": {
897	          "isChecksum": false,
898	          "startFieldIndex": "0",
899	          "endFieldIndex": "0",
900	          "checksumMethod": "sum8"
901	        },
902	        "defaultValue": "0x1acf0002",
903	        "inputType": "input",
904	        "configurable": true,
905	        "options": [],
906	        "dataParticipationType": "direct"
907	      },
908	      {
909	        "id": "j-dmYSVXrgu8wC5zNZt1F",
910	        "name": "粗测距",
911	        "dataType": "uint32",
912	        "length": 4,
913	        "factor": "100",
914	        "description": "",
915	        "validOption": {
916	          "isChecksum": false,
917	          "startFieldIndex": "0",
918	          "endFieldIndex": "0",
919	          "checksumMethod": "sum8"
920	        },
921	        "defaultValue": "0",
922	        "inputType": "input",
923	        "configurable": true,
924	        "options": [],
925	        "dataParticipationType": "direct"
926	      },
927	      {
928	        "id": "JX2MEeV4X693PThKpyamK",
929	        "name": "细测距",
930	        "dataType": "uint32",
931	        "length": 4,
932	        "factor": "0.390625",
933	        "description": "",
934	        "validOption": {
935	          "isChecksum": false,
936	          "startFieldIndex": "0",
937	          "endFieldIndex": "0",
938	          "checksumMethod": "sum8"
939	        },
940	        "defaultValue": "0",
941	        "inputType": "input",
942	        "configurable": true,
943	        "options": [],
944	        "dataParticipationType": "direct"
945	      },
946	      {
947	        "id": "tmqTRTQnFCyXMeWjLPvDL",
948	        "name": "测距值(ps)", […]

> AGENT

好了，我已经理解全貌了。以下是我的分析：

## 现状理解

**现有遥测帧（在 `10.json` 中）：**
- `R-FPGA-003` — 系统状态帧：信号功率、频偏估计值、发送速率、接收速率、载波/定时/帧同步锁定、编码方式
- `R-FPGA-001` — 帧统计数据：译码前总bit数、译码前误bit数、译码后总bit数、译码后误bit数、空口帧计数、空口误帧计数、数据帧计数、数据误帧计数
- `R-FPGA-002` — 测距帧：粗测距、细测距、测距值(ps)、测距值(cm) — **需要删除**

**需要改动的内容：**

| 改动类型 | 具体内容 |
|---|---|
| **UI 文字** | `HeaderBar.vue` + `HomePage.vue`："激光链路标准测试设备" → "激光模拟器" |
| **新帧配置** | 新建 `激光模拟器.json`，包含：系统状态帧（加"波长状态"）、帧统计数据（改名误码率）、**不含测距帧** |
| **发送帧** | 对应的 send 方向帧，使得本地能自发自收 |

**4 张截图的参数矩阵：**

| 截图 | 波长 | 编码 | 发/收速率 | 帧计数 | 译码前误码率 | 译码后误码率 | 数据帧计数 |
|---|---|---|---|---|---|---|---|
| 1 | 1563nm | LDPC | 2.5G | 312500 | 6.3e-7 | 0 | 59219 |
| 2 | 1540nm | LDPC | 1.25G | 156250 | 3.5e-2 | 2.3e-2 | 0 |
| 3 | 1563nm | RS | 625M | 78125 | 0 | 0 | 0 |
| 4 | 1563nm | RS | 312.5M | 39062 | 0 | 0 | 0 |

**核心思路**：帧格式随意，只要 send 和 receive 帧的字段对齐，本地发出去的数据就能被接收端解析并显示在遥测界面上。编码方式字段当前是 expression 类型（依赖接收速率判断 RS/LDPC），截图 1/2 需要 LDPC 但速率值 <5，可能需要调整 expression 逻辑或直接改成 select 类型方便手动切换。

要我现在开始动手实施吗？主要工作是：
1. 创建新帧配置文件 `激光模拟器.json`
2. 改两处 UI 文字
3. 可能需要微调编码方式字段的输入类型