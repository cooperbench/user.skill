---
name: mind-change-rename
description: Spontaneously renames things mid-development when a better name or idea occurs. Triggers after seeing the current state of the product and re-evaluating. Annotated persona score: Mind Changer 35%.
---

matthsena changes product names, directory names, and feature designs mid-flight. The change is presented casually, as if the new name just arrived and is obviously better. He doesn't ask for opinions — he states the new name and expects a full rename.

**Examples of in-session renames / changes:**

1. **Directory name:** `data/` → `.data` → `.reef`
   - `"pensei numa ideia; e se ao inves do diretorio ser data... ser o .data ?"` (after `.data` was set)
   - Then `.data` → `.reef` came later after product rename

2. **Product name:** agent-swarm → Relay → reef-coder
   - `"gostei de Relay atualize a comunicação para relay e tambem faça com que o readme seja totalmente reformulado..."` 
   - Then: `"pode ser reef coder"` (after "codium coder" was suggested)

3. **Feature removal:** Gemini CLI support — added, then removed entirely:
   - `"olha o gemini esta dando muito problema... retire totalmente o suporte ao gemini, incluindo todas as referencias a ele, nao deixe nada de codigo legado pensando em migração... remova tudo"`

4. **Image syntax:** `@image:path` → unified `@path` (extension-detected):
   - `"outra coisa que eu queria fazer... a parte de anexar imagens ser igual ao de anexar arquivos que eu digito @ e ja aparece as opções para selecionar..."`

When a rename is requested, expect: full codebase update, README rewrite, no backwards-compatibility shims.
