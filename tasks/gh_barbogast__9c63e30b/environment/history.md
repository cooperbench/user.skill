> DEVELOPER

read spec.md, don't reply

> TOOL

tool_use Bash
id: toolu_01K9sCXiCvSMmr5GauWGYhqz
```json
{
  "command": "find . -maxdepth 3 -iname \"spec.md\" -not -path \"*/node_modules/*\"",
  "description": "Locate spec.md file"
}
```

> TOOL

tool_result
id: toolu_01K9sCXiCvSMmr5GauWGYhqz
```
./spec.md
```

> TOOL

tool_use Read
id: toolu_01KK81NvJ7CrggEUBPKv9gYj
```json
{
  "file_path": "/home/<USER>/git/paper-scan-processor/spec.md"
}
```

> TOOL

tool_result
id: toolu_01KK81NvJ7CrggEUBPKv9gYj
```
1	# Paper Scan Processor
2	
3	A desktop application for post-processing PDF files containing batches of scanned documents. The app has three modes: **Merge**, **Split**, and **Drive Upload**.
4	
5	## Tech stack
6	
7	- **Desktop framework**: Wails
8	- **Backend**: Go
9	- **Frontend**: TypeScript + React
10	- **UI components**: Mantine
11	- **Virtualization**: TanStack Virtual
12	- **Drag-and-drop**: dnd-kit
13	- **PDF manipulation**: pdfcpu
14	- **PDF rendering** (thumbnails): `pdftoppm` (Poppler, system install, called as subprocess)
15	
16	## Common elements
17	
18	Both modes include a thumbnail panel and a page detail panel, and support the same per-page editing operations.
19	
20	### Thumbnail panel
21	
22	A vertically scrolling strip of page thumbnails. Width is user-adjustable via a drag handle; thumbnails scale to fill the panel width. Rendering is on-demand and virtualized — only visible thumbnails (plus a small overscan buffer) are rendered at any given time.
23	
24	The Go backend exposes a per-page render method returning a base64-encoded PNG; the frontend requests thumbnails as they scroll into view (`pdftoppm` subprocess).
25	
26	#### Keyboard shortcuts
27	
28	| Key                    | Action                                     |
29	| ---------------------- | ------------------------------------------ […]

> AGENT

I've read spec.md.