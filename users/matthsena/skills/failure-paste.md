---
name: failure-paste
description: Reports failures by pasting raw output — test results, terminal errors, or screenshots — with minimal or zero commentary. Triggers whenever a feature doesn't work as expected.
---

matthsena does not describe bugs in prose. He pastes the evidence and lets the agent interpret it. The failure report IS the message — no "I got this error" preamble, no analysis.

**Forms it takes:**

1. **Raw test output** — pastes the failing lines verbatim:
   ```
   ✗ PromptInput > renders input area when enabled [61.00ms]
   ✗ ModelSelect > navigate up from first and select last model [132.00ms]
   ✗ EngineSelect > arrow down moves selection to next item [95.00ms]
   
    168 pass
    3 fail
   ```
   (No other text in the message.)

2. **Terminal error paste** — full stdout including file paths:
   ```
   matheus@matheus-Nitro-AN517-52:~/Desktop/agent-swarm$ bun index.ts 
   Failed to parse JSON message: Server 'context7' supports tool updates...
   ```

3. **Screenshot** — `[Image: image/png]` or `[Image: source: /home/matheus/Pictures/...]` with no commentary, sometimes with a one-line trigger:
   - `"rodei para ver como esta o software com esse historico e olhe so...\n[Image: image/png]"`

4. **Brief observation + evidence** — one line then paste:
   - `"testei e corrigiu a questao do home; end; del etc... mas agr o backspace parou de funcionar?"`
   - `"eu obtive o seguinte warning! isso nao impacta o funcionamento mas fica o alerta: Cannot update a component..."`
