> SYSTEM

# AGENTS.md instructions for /home/pjensen/Repos/JSHack

<INSTRUCTIONS>
@/home/pjensen/.codex/RTK.md

--- project-doc ---

# AGENTS.md - JSHack Field Manual

JSHack is a zero-dependency browser roguelike: pure JavaScript, pure ES modules,
ECS architecture, Deno tooling. This file is optimized for coding agents. Prefer
the commands below over manual spelunking.

Deeper docs:

- [README.md](README.md)
- [SEPARATION_MANIFEST.md](docs/architecture/SEPARATION_MANIFEST.md)
- [RUNTIME_TOPOLOGY_DOCTRINE.md](docs/architecture/RUNTIME_TOPOLOGY_DOCTRINE.md)
- [TEN_COMMANDMENTS.md](docs/architecture/TEN_COMMANDMENTS.md)
- [ecs-js/AGENTS.md](src/lib/ecs-js/AGENTS.md)

---

## Hard Laws

- **No build step.** Pure ES modules. No webpack, babel, JSX, TypeScript, or
  bundling.
- **Deno, not Node.** Tests and tools run with Deno. Default test command:
  `deno test --allow-read`.
- **JavaScript only.** Keep source as `.js` / `.mjs`.
- **Mobile-first.** Touch is primary; desktop keyboard is secondary.
- **Separation is law.** `rules/` never imports `display/` or `bridge/`;
  `display/` never imports `rules/`; `bridge/` projects read-only rule state.
- **No system-to-system calls.** Systems communicate with `world.emit` /
  `world.on`; scheduler owns ordering.
- **New events use concrete event classes.** Any new event contract must define
  a concrete `EcsEvent` class and emit an instance with
  `world.emit(new Event(...))`. Do not introduce string-only events or parallel
  string re-emits for new contracts.
- **Touched listener installers use canonical extensions.** Any new listener
  installer, or any existing listener installer touched during a task, must use
  `defineExtension(...)` […]

> DEVELOPER

swung weapon tints should convey any enchantment

poision -> green
magic -> blue
fire -> flaming

I could have sworn we did this previously, you will not find it in `entire` so you can skip that step. 

do you understand what I'm saying?

> AGENT

Yes.

You want the visual tint/effect on the weapon swing animation to reflect the weapon’s enchantment or damage flavor:

- poison enchantment: swing tint/effect should be green
- magic enchantment: swing tint/effect should be blue
- fire enchantment: swing should look flaming, not just recolored

I understand this as a presentation change driven by existing weapon/enchantment state, ideally projected through the existing rules/bridge/display boundaries rather than hardcoding display guesses. I’ll skip Entire lookup as requested.

> DEVELOPER

riiiiight, but there are many more weapon echantments, dips, and beyond -- really think about it before moving please.

> AGENT

I’ll inspect the content/effect model and the current swing rendering path before proposing anything, because this sounds like it needs a generic visual-affordance rule rather than a three-case patch.

> TOOL

tool_use exec_command
id: call_V2dxKejYYko5BhSwazWCsyqR
```json
{
  "cmd": "rg -n \"swing|weapon|enchant|enchantment|dip|tint|flame|poison|magic|damageType|element|elemental\" src tests docs --glob '!src/lib/**'",
  "workdir": "/home/pjensen/Repos/JSHack",
  "max_output_tokens": 20000
}
```

> TOOL

tool_use exec_command
id: call_7eaJJsRAHruRFCTc7HDDfTip
```json
{
  "cmd": "rg -n \"attack|melee|strike|slash|trail|projectile|animation|effect\" src/display src/bridge src/rules --glob '!src/lib/**'",
  "workdir": "/home/pjensen/Repos/JSHack",
  "max_output_tokens": 20000
}
```

> TOOL

tool_use exec_command
id: call_HXQlNXc6IerprZyI6ZSe8TjU
```json
{
  "cmd": "rg --files src/content src/rules/data src/rules/components src/display src/bridge tests | sort",
  "workdir": "/home/pjensen/Repos/JSHack",
  "max_output_tokens": 20000
}
```

> TOOL

tool_result
id: call_V2dxKejYYko5BhSwazWCsyqR
```
Chunk ID: bd4087
Wall time: 0.0003 seconds
Process exited with code 0
Original token count: 96420
Output:
Warning: truncated output (original token count: 96420)
Total output lines: 3743

tests/batLoot.test.mjs:7:Deno.test("bat uses dedicated non-weapon loot table", () => {
tests/deathCleanup.test.mjs:26:  if (eq?.weapon) e.weapon = eq.weapon;
tests/deathCleanup.test.mjs:34:  world.add(wid, ItemInfo, { type: 'equip', slot: 'weapon', weight: 1, value: 0, description: '', count: 1, bonuses: { attack }, rarity: 1, rarityName: 'common', affixes: [] });
tests/deathCleanup.test.mjs:42:  const hero = makeActor(world, 'Hero', { weapon: bigSword }, 10);
tests/deathCleanup.test.mjs:118:    slot: "weapon",
tests/aiWeaponPickup.test.mjs:3:// Sapient humanoid monsters pick up weapons from the floor when unarmed and hunting.
tests/aiWeaponPickup.test.mjs:27:/** Minimal weapon entity sitting on the floor. */
tests/aiWeaponPickup.test.mjs:32:    type: 'weapon', slot: 'weapon', weight: 10, value: 50,
tests/aiWeaponPickup.test.mjs:39:/** Create a lich (intelligence 10, humanoid) at (x,y) with no weapon equipped. */
tests/aiWeaponPickup.test.mjs:46:    weapon: null, armor: null, head: null, neck: null, belt: null,
tests/aiWeaponPickup.test.mjs:53:    kineticDRDerived: 0, fireResistDerived: 0, poisonResistDerived: 0,
tests/aiWeaponPickup.test.mjs:70:Deno.test("lich picks up an adjacent weapon when unarmed and hunting", () => {
tests/aiWeaponPickup.test.mjs:78:  assertEquals(eq.weapon, sword, 'lich should have equipped the sword');
tests/aiWeaponPickup.test.mjs:79:  assertEquals(resolveEquipmentView(world, lich).weapon, sword, 'pickup should mirror main-hand topology');
tests/aiWeaponPickup.test.mjs:83:Deno.test("lich picks up weapon from adjacent tile (not just same tile)", () => {
tests/aiWeaponPickup.test.mjs:91:  assertEquals(eq.weapon, sword, […]

> TOOL

tool_result
id: call_7eaJJsRAHruRFCTc7HDDfTip
```
Chunk ID: 69e138
Wall time: 0.0002 seconds
Process exited with code 0
Original token count: 66406
Output:
Warning: truncated output (original token count: 66406)
Total output lines: 2658

src/display/palette/base.js:166:  book_phase_strike:    { glyph: "?", fg: "#66ccff", glow: "#2299cc", baseScale: 0.7 },
src/display/audio/audioWiring.js:49:  cave_bear: "cave_bear:attack",
src/display/audio/audioWiring.js:50:  rat: "rat:attack",
src/display/audio/audioWiring.js:51:  grid_bug: "insect:attack",
src/display/audio/audioWiring.js:52:  centipede: "insect:attack",
src/display/audio/audioWiring.js:53:  spider: "spider:attack",
src/display/audio/audioWiring.js:54:  cave_spider: "spider:attack",
src/display/audio/audioWiring.js:55:  phase_spider: "spider:attack",
src/display/audio/audioWiring.js:218:  const raw = payload?.sound || payload?.kind || payload?.effect || payload?.status || payload?.type || "";
src/display/audio/audioWiring.js:441:  'spell:phase_strike',
src/display/audio/audioWiring.js:540:    "melee:miss",
src/display/audio/audioWiring.js:541:    "melee:hit",
src/display/audio/audioWiring.js:668:  function playWeaponWhoosh({ weaponId, attacker, at, offhand }) {
src/display/audio/audioWiring.js:670:    playCombatLayers(planWeaponWhoosh({ itemInfo: info, offhand }), at || (attacker != null ? getPosition(attacker) : null));
src/display/audio/audioWiring.js:747:  world.on('combat:melee:attack', ({ attacker, weaponId, weaponFamily, at, offhand }) => {
src/display/audio/audioWiring.js:749:    playCombatLayers(planWeaponWhoosh({ itemInfo: info, offhand, fallbackFamily: null }), at || (attacker != null ? getPosition(attacker) : null));
src/display/audio/audioWiring.js:752:  world.on('combat:melee:miss', ({ attacker, weaponId, weaponFamily, at, offhand }) => {
src/display/audio/audioWiring.js:754:    playCombatLayers(planWeaponWhoosh({ itemInfo: info, offhand, fallbackFamily: null }), at || (attacker != null ? getPosition(attacker) : null));
src/display/audio/audioWiring.js:757:  world.on('combat:fumble', ({ attacker, weaponId, at }) => {
src/display/audio/audioWiring.js:758:    playWeaponDeflect({ weaponId, at, entityId: attacker, hard: false, volume: 0.72 });
src/display/audio/audioWiring.js:761:  world.on('combat:dodge', ({ attacker, weaponId, weaponFamily, at, offhand }) => {
src/display/audio/audioWiring.js:763:    playCombatLayers(planWeaponWhoosh({ itemInfo: […]

> TOOL

tool_result
id: call_HXQlNXc6IerprZyI6ZSe8TjU
```
Chunk ID: b87325
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 7332
Output:
src/bridge/schema/weaponVfxProfiles.js
src/bridge/schema/weaponVfxResolver.js
src/bridge/schema/worldView.js
src/content/abilityHandler.js
src/content/define.js
src/content/helpers.js
src/content/index.js
src/content/install.js
src/content/interactables/crypt/index.js
src/content/interactables/fountain/index.js
src/content/interactables/index.js
src/content/interactables/mailbox/index.js
src/content/interactables/rift/index.js
src/content/items/armors.js
src/content/items/belts.js
src/content/items/boots.js
src/content/items/dawnbreaker.js
src/content/items/economy.js
src/content/items/fishingRod.js
src/content/items/gloves.js
src/content/items/helms.js
src/content/items/index.js
src/content/items/legs.js
src/content/items/lodbrokSerpentBoundBreeches.js
src/content/items/necks.js
src/content/items/offhands.js
src/content/items/potionOfRadiance.js
src/content/items/potions.js
src/content/items/rangedWeapons.js
src/content/items/rings.js
src/content/items/scrolls.js
src/content/items/spellbooks.js
src/content/items/sunVessel.js
src/content/items/sunsword.js
src/content/items/wands.js
src/content/items/weapons.js
src/content/monsters/animals.js
src/content/monsters/barrowWight.js
src/content/monsters/humanoids.js
src/content/monsters/index.js
src/content/monsters/special.js
src/content/monsters/undead.js
src/content/registry.js
src/content/scriptCtx.js
src/content/vfxWiring.js
src/content/weaponHookBridge.js
src/content/worldFacade.js
src/display/audio/audioEngine.js
src/display/audio/audioWiring.js
src/display/audio/audioWiringExtension.js
src/display/audio/biomeAmbientController.js
src/display/audio/combatAudioAdapter.js
src/display/audio/combatPack.js
src/display/audio/combatSoundResolver.js
src/display/audio/fountainAmbientController.js
src/display/audio/index.js
src/display/audio/localEmitterAmbientController.js
src/display/audio/sounds.js
src/display/audio/worldAmbientController.js
src/display/camera/controller.js
src/display/camera/follow.js
src/display/camera/shake.js
src/display/camera/utils.js
src/display/camera/zoomPunch.js
src/display/composition/cameraEffects.js
src/display/composition/debugOverlay.js
src/display/composition/effectOrchestrator.js
src/display/composition/index.js
src/display/composition/postLightingRedraw.js
src/display/composition/setupDisplayRuntime.js
src/display/composition/targetingReticle.js
src/display/fx/aggroFxController.js
src/display/fx/boltFxController.js
src/display/fx/bumpFxController.js
src/display/fx/cloudFx.js
src/display/fx/deathEssenceFxController.js
src/display/fx/deathJingle.js
src/display/fx/deathLootArcFx.js
src/display/fx/deathVfxController.js
src/display/fx/delayedDeathFxController.js
src/display/fx/equipBadges.js
src/display/fx/flyingFxController.js
src/display/fx/fxEntries.js
src/display/fx/fxGeom.js
src/display/fx/hitstopController.js
src/display/fx/meleeSlashFx.js
src/display/fx/pickupFxController.js
src/display/fx/polymorphSmokeFx.js
src/display/fx/procStateGlyphs.js
src/display/fx/projectileFx.js
src/display/fx/projectileImpactTracker.js
src/display/fx/projectileMiss.js
src/display/fx/recoilFxController.js
src/display/fx/rootedVineFx.js
src/display/fx/slideFxController.js
src/display/fx/sparksFxController.js
src/display/fx/spellAreaFx.js
src/display/fx/spiritPointerFx.js
src/display/fx/spiritWispFx.js
src/display/fx/statusPresentationDelayController.js
src/display/fx/surfaceAreaFx.js
src/display/fx/teleportFxController.js
src/display/fx/throwFxController.js
src/display/fx/weatherFx.js
src/display/input/InputManager.js
src/display/input/InputRouter.js
src/display/input/actions.js
src/display/input/gestureRecognizers.js
src/display/input/inputLock.js
src/display/input/inputSettings.js
src/display/input/lockdown.js
src/display/lighting/engine.js
src/display/lighting/field/fov.js
src/display/lighting/sources/index.js
src/display/lighting/sources/temporalPatterns.js
src/display/palette/base.js
src/display/palette/equipment.js
src/display/palette/index.js
src/display/palette/packs/armor.js
src/display/palette/packs/rings.js
src/display/palette/packs/weapons.js
src/display/passes/glyphs/atlas.js
src/display/passes/lightmask/index.js
src/display/passes/vfx/glyph/README.md
src/display/passes/vfx/glyph/effects/aegisWard.js
src/display/passes/vfx/glyph/effects/bleedPulse.js
src/display/passes/vfx/glyph/effects/dragonBreath.js
src/display/passes/vfx/glyph/effects/frozenCrystal.js
src/display/passes/vfx/glyph/effects/index.js
src/display/passes/vfx/glyph/effects/neonPulse.js
src/display/passes/vfx/glyph/effects/poisonPulse.js
src/display/passes/vfx/glyph/effects/shockArc.js
src/display/passes/vfx/glyph/glyph_vfx.js
src/display/passes/vfx/particles/particlePool.js
src/display/passes/vfx/particles/statusEmitterController.js
src/display/passes/vfx/text/floatText.js
src/display/ui/alchemyBenchOverlay.js
src/display/ui/anvilOverlay.js
src/display/ui/bubbleDialog.js
src/display/ui/charCreation.js
src/display/ui/characterOverlay.js
src/display/ui/combatLogTooltip.js
src/display/ui/concentricGauge.js
src/display/ui/cookingFireOverlay.js
src/display/ui/debugConsole.js
src/display/ui/debugGraph.js
src/display/ui/dialogOverlay.js
src/display/ui/enchantingBenchOverlay.js
src/display/ui/hud.js
src/display/ui/inventoryOverlay.js
src/display/ui/inventoryUtils.js
src/display/ui/lockPickingOverlay.js
src/display/ui/mailboxOverlay.js
src/display/ui/memoryGraph.js
src/display/ui/messageMore.js
src/display/ui/mobileRadial.js
src/display/ui/monsterChooserOverlay.js
src/display/ui/overlay.js
src/display/ui/overlayRenders.js
src/display/ui/overlayUtils.js
src/display/ui/petMenu.js
src/display/ui/pinnedItemSlots.js
src/display/ui/shopOverlay.js
src/display/ui/spellDock.js
src/display/ui/statusLine.js
src/display/ui/tileInspector.js
src/display/ui/wiring/deityUiWiring.js
src/display/ui/wiring/eventUiWiring.js
src/display/ui/wiring/floatTextWiring.js
src/display/ui/wiring/fountainPresentationExtension.js
src/display/ui/wiring/fountainUiExtension.js
src/display/ui/wiring/goreEngine.js
src/display/ui/wiring/messageWiring.js
src/display/ui/wiring/messages/combatMessages.js
src/display/ui/wiring/messages/creatureMessages.js
src/display/ui/wiring/messages/economyMessages.js
src/display/ui/wiring/messages/environmentMessages.js
src/display/ui/wiring/messages/fountainMessages.js
src/display/ui/wiring/messages/itemMessages.js […]

> AGENT

The first pass shows there is already a dedicated weapon VFX pipeline (`weaponVisuals`, bridge profiles, `meleeSlashFx`) plus separate systems for affixes, coatings, status emitters, and proc-state visuals. I’m narrowing on where “what is visually active on this weapon right now” should be resolved so dips, socket/proc enchantments, and authored weapons all share one rule.

> TOOL

tool_use exec_command
id: call_QXofaBvgrSARy7jPD7DtKbTV
```json
{
  "cmd": "sed -n '1,260p' src/bridge/schema/weaponVfxResolver.js",
  "workdir": "/home/pjensen/Repos/JSHack",
  "max_output_tokens": 20000
}
```

> TOOL

tool_use exec_command
id: call_lODbOp3YN287lx1zaKGdL5dw
```json
{
  "cmd": "sed -n '1,260p' src/bridge/schema/weaponVfxProfiles.js",
  "workdir": "/home/pjensen/Repos/JSHack",
  "max_output_tokens": 20000
}
```

> TOOL

tool_use exec_command
id: call_GM5kbwlITwwfyefubk0Tunxj
```json
{
  "cmd": "sed -n '1,280p' src/display/fx/meleeSlashFx.js",
  "workdir": "/home/pjensen/Repos/JSHack",
  "max_output_tokens": 20000
}
```

> TOOL

tool_use exec_command
id: call_VXkfMi7s4TSQPsUzRnxJx45F
```json
{
  "cmd": "sed -n '1,260p' src/rules/data/weaponCoatings.js",
  "workdir": "/home/pjensen/Repos/JSHack",
  "max_output_tokens": 20000
}
```

> TOOL

tool_result
id: call_QXofaBvgrSARy7jPD7DtKbTV
```
Chunk ID: 604835
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 1462
Output:
// bridge/schema/weaponVfxResolver.js
// Resolves equipped-weapon VFX projections from canonical profile data.

import { Equipment } from "../../rules/components/Equipment.js";
import { ItemInfo } from "../../rules/components/ItemInfo.js";
import { NamedIdentity } from "../../rules/components/NamedIdentity.js";
import { listWeaponVfxProfiles } from "./weaponVfxProfiles.js";

const DEFAULT_SLOTS = Object.freeze(["weapon", "offhand"]);
const PROJECTILE_SLOTS = Object.freeze(["ranged"]);
const SLOT_RANK = Object.freeze({
  ranged: 0,
  weapon: 1,
  offhand: 2,
});

/**
 * @param {unknown} raw
 * @returns {string}
 */
function normalizeId(raw) {
  return String(raw || "").trim().toLowerCase();
}

/**
 * @param {string} raw
 * @returns {string}
 */
function normalizeAffixId(raw) {
  const key = normalizeId(raw);
  return key.startsWith("affix:") ? key.slice(6) : key;
}

/**
 * @param {import('./weaponVfxProfiles.js').WeaponVfxProfile} profile
 * @param {{ slot:string, identity:string, affixes:Set<string>, coatingKind:string }} state
 * @returns {boolean}
 */
function matchesProfile(profile, state) {
  const match = profile?.match || null;
  if (!match) return false;

  const slotFilter = Array.isArray(match.slots) ? match.slots.map(normalizeId).filter(Boolean) : [];
  if (slotFilter.length > 0 && !slotFilter.includes(state.slot)) return false;

  const matchIdentities = Array.isArray(match.identities) ? match.identities.map(normalizeId).filter(Boolean) : [];
  const matchAffixes = Array.isArray(match.affixes) ? match.affixes.map(normalizeAffixId).filter(Boolean) : [];
  const matchCoatings = Array.isArray(match.coatingKinds) ? match.coatingKinds.map(normalizeId).filter(Boolean) : [];

  if (matchIdentities.includes(state.identity)) return true;
  if (matchCoatings.includes(state.coatingKind)) return true;
  for (const affix of […]

> TOOL

tool_result
id: call_lODbOp3YN287lx1zaKGdL5dw
```
Chunk ID: 1922cc
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 1843
Output:
// bridge/schema/weaponVfxProfiles.js
// Canonical display manifest for equipped-weapon VFX projection.

const FIRE_AFFIXES = Object.freeze(["flaming", "firestorm1", "soulfire1"]);
const VENOM_AFFIXES = Object.freeze(["venomous1", "plague1"]);
const STORM_AFFIXES = Object.freeze(["chainlightning1", "capacitive1"]);
const FROST_AFFIXES = Object.freeze(["frostbite1"]);
const SOUL_AFFIXES = Object.freeze(["souldrain1", "agony1"]);
const BLOOD_AFFIXES = Object.freeze(["hemorrhage1", "berserk1"]);
const CAUSTIC_AFFIXES = Object.freeze(["caustic1"]);

/**
 * @typedef {{
 *   id: string,
 *   priority: number,
 *   match: {
 *     affixes?: readonly string[],
 *     identities?: readonly string[],
 *     coatingKinds?: readonly string[],
 *     slots?: readonly string[],
 *   },
 *   carryAnchor?: {
 *     forward?: number,
 *     lateral?: number,
 *     vertical?: number,
 *   },
 *   carryEmitter?: Record<string, any>,
 *   carryLight?: {
 *     radius: number,
 *     color: [number, number, number],
 *     flicker?: {
 *       mode?: "sin",
 *       base?: number,
 *       amp?: number,
 *       speed?: number,
 *       phase?: number,
 *     },
 *   },
 *   projectileEmitter?: {
 *     style?: string,
 *   },
 * }} WeaponVfxProfile
 */

/** @type {readonly WeaponVfxProfile[]} */
const WEAPON_VFX_PROFILES = Object.freeze([
  Object.freeze({
    id: "holy_weapon",
    priority: 360,
    match: Object.freeze({
      identities: Object.freeze(["sunsword"]),
    }),
    carryAnchor: Object.freeze({ forward: 0.40, lateral: 0.18, vertical: -0.05 }),
    carryEmitter: Object.freeze({
      rate: 6,
      angle: -Math.PI / 2,
      spread: Math.PI / 6,
      speed: […]

> TOOL

tool_result
id: call_GM5kbwlITwwfyefubk0Tunxj
```
Chunk ID: ed4b2a
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 2410
Output:
// display/fx/meleeSlashFx.js
// Melee attack visual language: sweeps, stabs, impacts, parry sparks, dodge whiffs.
// Each weapon class + attack kind maps to a distinct visual primitive so combat
// reads expressively — no two consecutive swings should look identical.
// Only fires for weapon-wielding melee (impactProfile.weaponClass !== 'unarmed').

import { MeleeSlashFx } from "./fxEntries.js";

// ── Timing ─────────────────────────────────────────────────────────────────
const SWEEP_TTL       = 0.14;   // sword/axe arc lifetime
const STAB_TTL        = 0.11;   // dagger thrust
const IMPACT_TTL      = 0.13;   // mace/blunt burst
const PARRY_TTL       = 0.10;   // metallic spark
const WHIFF_TTL       = 0.16;   // ghostly miss trail (lingers slightly)
const OFFHAND_DELAY   = 0.15;   // match bump/gore offhand delay

// ── Weapon colour palettes [r, g, b] ──────────────────────────────────────
const COL_BLADE   = [220, 230, 240]; // pale steel
const COL_AXE     = [240, 220, 200]; // warm steel
const COL_BLUNT   = [255, 200, 140]; // amber
const COL_DAGGER  = [240, 245, 255]; // cold white
const COL_DEFAULT = [230, 230, 230]; // neutral
const COL_PARRY   = [255, 255, 220]; // bright metallic yellow-white
const COL_WHIFF   = [180, 190, 210]; // ghostly blue-grey

// […]

> TOOL

tool_result
id: call_VXkfMi7s4TSQPsUzRnxJx45F
```
Chunk ID: 9b5a75
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 1571
Output:
import { ItemInfo } from '../components/ItemInfo.js';
import { Stamina } from '../components/Stamina.js';
import { combatSeed, mulberry32, rngInt } from '../utils/rng.js';
import { upsertTimedEffect } from '../utils/effectSemantics.js';
import { ensureActiveEffects } from '../utils/effects.js';
import { effectiveMaxStamina } from '../utils/passiveBonuses.js';
import { applyHealing } from '../utils/applyHealing.js';
import { ELEMENT_TINT_POISON } from './elementTints.js';

export const WEAPON_COATING_DEFS = Object.freeze({
  poison: Object.freeze({
    // Higher proc rate to make applied poison meaningfully tactical while still
    // allowing occasional non-proc hits for variability.
    chancePct: 75,
    consumeOnHit: true,
    seedSalt: 0xc0470001,
    emitEvent: 'proc:poisoned',
    elementTint: ELEMENT_TINT_POISON,
    effect: Object.freeze({ key: 'poison', turnsLeft: 4, potency: 2, stacks: 1 }),
  }),
  paralysis: Object.freeze({
    chancePct: 40,
    consumeOnHit: true,
    seedSalt: 0xc0470002,
    emitEvent: 'proc:paralyzed',
    elementTint: null,
    effect: Object.freeze({ key: 'stun', turnsLeft: 4, potency: 1, stacks: 1 }),
  }),
  blindness: Object.freeze({
    chancePct: 50,
    consumeOnHit: true,
    seedSalt: 0xc0470003,
    emitEvent: 'proc:blinded',
    elementTint: null,
    effect: Object.freeze({ key: 'blinded', turnsLeft: 3, potency: 1, stacks: 1 }),
  }),
  confusion: Object.freeze({
    chancePct: 45,
    consumeOnHit: true,
    seedSalt: 0xc0470004,
    emitEvent: 'proc:confused',
    elementTint: null,
    effect: Object.freeze({ key: 'confused', turnsLeft: 3, potency: 1, stacks: 1 }),
  }),
  hallucination: Object.freeze({
    chancePct: 35,
    consumeOnHit: true,
    seedSalt: 0xc0470005,
    emitEvent: […]

> AGENT

The important discovery: `meleeSlashFx` already has an `elementTint` hook, but current bridge profile resolution only exposes carry/projectile VFX, not the swing’s semantic tint/style. The likely fix is to extend the existing profile manifest/resolver so swing arcs consume the same resolved weapon state instead of separately re-inferring affixes in display code.

> TOOL

tool_use exec_command
id: call_76acouKjSnZe94zHN8nTpIbw
```json
{
  "cmd": "sed -n '260,620p' src/display/fx/meleeSlashFx.js",
  "workdir": "/home/pjensen/Repos/JSHack",
  "max_output_tokens": 24000
}
```

> TOOL

tool_use exec_command
id: call_CqEGlix3yZXPbo2MFoZWbHci
```json
{
  "cmd": "sed -n '1,260p' src/rules/data/affixes.js",
  "workdir": "/home/pjensen/Repos/JSHack",
  "max_output_tokens": 24000
}
```

> TOOL

tool_use exec_command
id: call_r7AUDbUXoaFfGGsFHTjzN9sz
```json
{
  "cmd": "sed -n '260,620p' src/rules/data/affixes.js",
  "workdir": "/home/pjensen/Repos/JSHack",
  "max_output_tokens": 24000
}
```

> TOOL

tool_use exec_command
id: call_E3IM6nh9CHewxV1v2ju461kc
```json
{
  "cmd": "sed -n '1,220p' src/rules/data/elementTints.js",
  "workdir": "/home/pjensen/Repos/JSHack",
  "max_output_tokens": 16000
}
```

> TOOL

tool_result
id: call_76acouKjSnZe94zHN8nTpIbw
```
Chunk ID: bc43bf
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 3462
Output:
  }
  return stops[stops.length - 1][1];
}

// ── Angle helpers ─────────────────────────────────────────────────────────

// Resolve the primary direction for the slash VFX.
// facingVector (attacker's facing) takes priority; impactVector is the fallback.
function resolveBaseAngle(facingVec, impactVec) {
  if (facingVec && Number.isFinite(facingVec.dx) && Number.isFinite(facingVec.dy)) {
    const mag = Math.hypot(facingVec.dx, facingVec.dy);
    if (mag > 0) return Math.atan2(facingVec.dy, facingVec.dx);
  }
  if (impactVec) return Math.atan2(impactVec.dy || 0, impactVec.dx || 0);
  return 0;
}

// Simple deterministic jitter from a counter
function jitter(counter) {
  const x = Math.sin(counter * 7.31 + 2.17) * 0.5 + 0.5; // 0..1
  return (x - 0.5) * 0.5; // [-0.25, 0.25] radians
}

// ═══════════════════════════════════════════════════════════════════════════
// Controller
// ═══════════════════════════════════════════════════════════════════════════
export function createMeleeSlashFxController() {
  /** @type {MeleeSlashFx[]} */
  const _active = [];

  /** @type {{fx: MeleeSlashFx, delay: number}[]} */
  const _pending = [];

  // Per-attacker swing counter for alternation (left/right sweeps)
  /** @type {Map<number, number>} */
  const _swingCounter = new Map();

  function nextSwing(attackerId, offhand) {
    if (offhand) return _swingCounter.get(attackerId) || 0;
    const n = (_swingCounter.get(attackerId) || 0) + 1;
    _swingCounter.set(attackerId, n);
    return n;
  }

  // Dual-wield direction pairings — picked randomly each […]

> TOOL

tool_result
id: call_CqEGlix3yZXPbo2MFoZWbHci
```
Chunk ID: 0c8447
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 2388
Output:
// Affix definitions: triggers can be onBeforeHit, onHit, onDamaged, onKill, onEquip, onUnequip
// Scripts are registered via the central scripting router.
import { mulberry32, rngInt, combatSeed } from "../utils/rng.js";
import { ActiveEffects } from "../components/ActiveEffects.js";
import { Vitality } from "../components/Vitality.js";
import { Position } from "../components/Position.js";
import { Faction } from "../components/Faction.js";
import { Mana } from "../components/Mana.js";
import { Stamina } from "../components/Stamina.js";
import { registerScript, ScriptVerb } from "../scripting.js";
import { dealDamage } from "../utils/dealDamage.js";
import { forEachInRadius } from "../utils/spatialIndex.js";
import { areFactionsHostile } from "../utils/factionHostility.js";
import { upsertTimedEffect } from "../utils/effectSemantics.js";
import { effectiveMaxMana, effectiveMaxStamina } from "../utils/passiveBonuses.js";
import { ELEMENT_TINT_FIRE, ELEMENT_TINT_POISON, ELEMENT_TINT_FROST, ELEMENT_TINT_ACID, ELEMENT_TINT_ELECTRIC } from "./elementTints.js";

const AFFIX_THORNS = "affix:thorns1";
const AFFIX_VAMP = "affix:vamp1";
const AFFIX_FIERCE = "affix:fierce";
const AFFIX_GUARD = "affix:guard1";
const AFFIX_LIFE = "affix:life1";
const AFFIX_ATTUNED = "affix:attuned1";
const AFFIX_FIRE_WARD = "affix:fireWard1";
const AFFIX_POISON_WARD = "affix:poisonWard1";
const AFFIX_KINETIC_WARD = "affix:kineticWard1";
const AFFIX_CAUSTIC = "affix:caustic1";
const AFFIX_CAPACITIVE = "affix:capacitive1";
const AFFIX_INSULATED = "affix:insulated1";
const AFFIX_LUCKY = "affix:lucky1";
const AFFIX_VENOMOUS = "affix:venomous1";
const AFFIX_CHAIN_LIGHTNING = "affix:chainLightning1";
const AFFIX_FIRESTORM = "affix:firestorm1";
const AFFIX_SOUL_DRAIN […]

> TOOL

tool_result
id: call_r7AUDbUXoaFfGGsFHTjzN9sz
```
Chunk ID: d6059e
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 3476
Output:
registerScript(AFFIX_SOUL_DRAIN, {
  [ScriptVerb.AffixOnHit]: (world, ctx) => {
    if (!procRoll(world, ctx.attacker, ctx.defender, 0xc0ffee12, 18)) return;
    const amt = Math.max(1, Math.floor(ctx.damage / 2));
    ctx.healAttacker(amt);
    world.emit("proc:soulDrain", { actor: ctx.attacker, target: ctx.defender, amount: amt });
  },
});

registerScript(AFFIX_BERSERK, {
  [ScriptVerb.AffixOnHit]: (world, ctx) => {
    if (!procRoll(world, ctx.attacker, ctx.defender, 0xc0ffee13, 10)) return;
    upsertEffect(world, ctx.attacker, { key: "berserk", turnsLeft: 5, potency: 1, stacks: 1 });
    world.emit("proc:berserking", { actor: ctx.attacker, target: ctx.defender });
  },
});

registerScript(AFFIX_SHIELD_WALL, {
  [ScriptVerb.AffixOnDamaged]: (world, ctx) => {
    if (!procRoll(world, ctx.attacker, ctx.defender, 0xc0ffee14, 15)) return;
    upsertEffect(world, ctx.defender, { key: "stoneskin", turnsLeft: 4, potency: 2, stacks: 1 });
    world.emit("proc:shieldWall", { actor: ctx.defender, target: ctx.attacker });
  },
});

registerScript(AFFIX_MANA_SURGE, {
  [ScriptVerb.AffixOnHit]: (world, ctx) => {
    if (!procRoll(world, ctx.attacker, ctx.defender, 0xc0ffee15, 20)) return;
    const mana = world.get(ctx.attacker, Mana);
    if (!mana) return;
    const maxMana = effectiveMaxMana(world, ctx.attacker, mana);
    mana.mana = Math.min(maxMana, (Number(mana.mana) || 0) + 3);
    world.emit("proc:manaSurge", { actor: ctx.attacker, amount: 3 });
  },
});

registerScript(AFFIX_EXECUTIONER, {
  [ScriptVerb.AffixOnBeforeHit]: (world, ctx) => {
    const vit = world.get(ctx.defender, Vitality);
    if (!vit) return;
    if (vit.hp / vit.maxHp >= 0.3) return;
    ctx.damage += 3;
    world.emit("proc:executioner", { actor: ctx.attacker, target: ctx.defender […]

> TOOL

tool_result
id: call_E3IM6nh9CHewxV1v2ju461kc
```
Chunk ID: eeade2
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 157
Output:
// Canonical element-tint identifiers.
// Rules-side data (affixes, coatings, effect defs) reference these keys.
// Display-side VFX maps each key to an RGB colour.
export const ELEMENT_TINT_FIRE     = 'fire';
export const ELEMENT_TINT_POISON   = 'poison';
export const ELEMENT_TINT_FROST    = 'frost';
export const ELEMENT_TINT_ACID     = 'acid';
export const ELEMENT_TINT_ELECTRIC = 'electric';

// Every valid tint key in one set, for quick membership checks.
export const ELEMENT_TINT_KEYS = Object.freeze([
  ELEMENT_TINT_FIRE,
  ELEMENT_TINT_POISON,
  ELEMENT_TINT_FROST,
  ELEMENT_TINT_ACID,
  ELEMENT_TINT_ELECTRIC,
]);

```

> TOOL

tool_use exec_command
id: call_f47udLDnUnfruL9Ay3JGmrDK
```json
{
  "cmd": "rg -n \"AFFIX_DEFS|elementTint|visual|procState|weaponVfx|impactProfile|combat:melee:attack|meleeSlash\" src tests --glob '!src/lib/**'",
  "workdir": "/home/pjensen/Repos/JSHack",
  "max_output_tokens": 30000
}
```

> TOOL

tool_use exec_command
id: call_FlJ2Kbzvsz2GTiscY89Mu7Yw
```json
{
  "cmd": "sed -n '1,260p' tests/worldViewWeaponVfxProfiles.test.mjs",
  "workdir": "/home/pjensen/Repos/JSHack",
  "max_output_tokens": 20000
}
```

> TOOL

tool_use exec_command
id: call_lFC7uZAnKOxmJE98vXcIFW4K
```json
{
  "cmd": "sed -n '1,260p' tests/projectileWeaponVfx.test.mjs",
  "workdir": "/home/pjensen/Repos/JSHack",
  "max_output_tokens": 20000
}
```

> TOOL

tool_use exec_command
id: call_fybVJBi6UVQql8xEU0jaSEXF
```json
{
  "cmd": "sed -n '1,240p' tests/statusEmitterWeaponVfx.test.mjs",
  "workdir": "/home/pjensen/Repos/JSHack",
  "max_output_tokens": 20000
}
```

> TOOL

tool_result
id: call_f47udLDnUnfruL9Ay3JGmrDK
```
Chunk ID: 5d8d06
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 9335
Output:
src/bridge/schema/weaponVfxProfiles.js:1:// bridge/schema/weaponVfxProfiles.js
src/main.js:71:import { drawProcStateBadges, getProcStateVisual, procBadgeWorldCenter } from "./display/fx/procStateGlyphs.js";
src/main.js:2411: * @param {any} procState
src/main.js:2413:function formatProcStateDetail(procState) {
src/main.js:2414:  const label = String(procState?.name || "").trim() || humanizeProcStateKey(procState?.key);
src/main.js:2415:  const detail = String(procState?.description || "").trim();
src/main.js:2416:  const stacks = Math.max(1, Number(procState?.stacks || 1) | 0);
src/main.js:2417:  const turnsLeft = Math.max(0, Number(procState?.turnsLeft || 0) | 0);
src/main.js:2418:  const potency = Number.isFinite(Number(procState?.potency)) ? Number(procState?.potency) : 1;
src/main.js:2431: * @returns {null | { entity:any, procState:any }}
src/main.js:2436:  /** @type {null | { entity:any, procState:any, d2:number }} */
src/main.js:2440:    const procStates = Array.isArray(entity?.procStates) ? entity.procStates : [];
src/main.js:2441:    if (!procStates.length) continue;
src/main.js:2442:    for (let j = 0; j < procStates.length; j++) {
src/main.js:2443:      const procState = procStates[j];
src/main.js:2444:      const vis = getProcStateVisual(procState?.key);
src/main.js:2452:      if (!best || d2 < best.d2) best = { entity, procState, d2 };
src/main.js:2455:  return best ? { entity: best.entity, procState: best.procState } : null;
src/main.js:2772:      text: `${who}: ${formatProcStateDetail(hit.procState)}`,
src/main.js:3155:  meleeSlashFx,
src/main.js:4557:  // Use visual HP — add back damage whose projectile hasn't arrived yet
src/main.js:4558:  const hp = impactTracker.visualHp(e.id, rawHp, maxHp, now);
src/main.js:4600:  const hp = impactTracker.visualHp(e.id, rawHp, maxHp, _fxTime); […]

> TOOL

tool_result
id: call_FlJ2Kbzvsz2GTiscY89Mu7Yw
```
Chunk ID: e1f997
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 1552
Output:
import "./helpers/installContentCatalog.mjs";
import { assert, assertEquals } from "jsr:@std/assert";
import { World } from "../src/lib/ecs-js/index.js";
import { buildWorldView } from "../src/bridge/schema/worldView.js";
import { Player } from "../src/rules/components/Player.js";
import { Position } from "../src/rules/components/Position.js";
import { NamedIdentity } from "../src/rules/components/NamedIdentity.js";
import { ItemInfo } from "../src/rules/components/ItemInfo.js";
import { Equipment } from "../src/rules/components/Equipment.js";
import { Brain } from "../src/rules/components/Brain.js";
import { buildCatalogItem } from "../src/rules/data/itemCatalogLoader.js";
import "../src/content/items/sunsword.js";
import { installContent } from "../src/content/install.js";
installContent();

function createItem(world, {
  identity,
  type = "weapon",
  affixes = [],
  coating = null,
} = {}) {
  const id = world.create();
  world.add(id, NamedIdentity, { name: identity, identity });
  const info = {
    type,
    slot: "",
    weight: 1,
    value: 1,
    description: "",
    count: 1,
    bonuses: {},
    twoHanded: false,
    rarity: 1,
    rarityName: "common",
    affixes: Array.isArray(affixes) ? affixes.slice() : [],
  };
  if (coating) info.coating = coating;
  world.add(id, ItemInfo, info);
  return id;
}

Deno.test("worldView projects dual-wield weapon VFX profiles per slot", () => {
  const world = new World({ seed: 31 });
  const player = world.create();
  world.add(player, Player, {});
  world.add(player, Position, { x: 3, y: 4 });
  world.add(player, NamedIdentity, { name: […]

> TOOL

tool_result
id: call_lFC7uZAnKOxmJE98vXcIFW4K
```
Chunk ID: b49388
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 677
Output:
import { assert } from "jsr:@std/assert";
import { World } from "../src/lib/ecs-js/index.js";
import { Position } from "../src/rules/components/Position.js";
import { Equipment } from "../src/rules/components/Equipment.js";
import { ItemInfo } from "../src/rules/components/ItemInfo.js";
import { NamedIdentity } from "../src/rules/components/NamedIdentity.js";
import { createProjectileFxController } from "../src/display/fx/projectileFx.js";

function addWeapon(world, identity, affixes = []) {
  const id = world.create();
  world.add(id, NamedIdentity, { name: identity, identity });
  world.add(id, ItemInfo, {
    type: "weapon",
    subtype: "bow",
    slot: "",
    weight: 1,
    value: 1,
    description: "",
    count: 1,
    bonuses: {},
    twoHanded: false,
    rarity: 1,
    rarityName: "common",
    affixes: Array.isArray(affixes) ? affixes.slice() : [],
  });
  return id;
}

Deno.test("projectile FX can inherit ranged-shot style from weapon VFX profile while preserving arrow/spell pathways", () => {
  const world = new World({ seed: 91 });
  const attacker = world.create();
  const target = world.create();
  world.add(attacker, Position, { x: 2, y: 2 });
  world.add(target, Position, { x: 7, y: 2 });

  const venomBow = addWeapon(world, "venom_bow", ["venomous1"]);
  world.add(attacker, Equipment, { ranged: venomBow });

  const controller = createProjectileFxController({
    world,
    cam: {},
    fx: { pool: { spawn() {} } },
    getPosition: (id) => {
      const pos = world.get(id, […]

> TOOL

tool_result
id: call_fybVJBi6UVQql8xEU0jaSEXF
```
Chunk ID: 38ae10
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 1429
Output:
import { assert, assertEquals } from "jsr:@std/assert";
import { createStatusEmitterController } from "../src/display/passes/vfx/particles/statusEmitterController.js";

function makeWorld() {
  const listeners = new Map();
  return {
    on(event, handler) {
      const bucket = listeners.get(event) || [];
      bucket.push(handler);
      listeners.set(event, bucket);
    },
    emit(event, payload) {
      const bucket = listeners.get(event) || [];
      for (let i = 0; i < bucket.length; i++) bucket[i](payload);
    },
  };
}

function makeFxHarness() {
  const ensured = [];
  const removed = [];
  const stepCalls = [];
  return {
    ensured,
    removed,
    stepCalls,
    fx: {
      ensureEmitter(key, cfg) {
        ensured.push({ key, cfg });
      },
      removeEmitter(key) {
        removed.push(key);
      },
      step(dtSec, origins) {
        stepCalls.push({
          dtSec: Number(dtSec || 0),
          origins: Array.isArray(origins) ? origins.map((origin) => ({ ...origin })) : [],
        });
      },
    },
  };
}

Deno.test("status emitter controller resolves per-slot weapon profile emitters/lights", () => {
  const world = makeWorld();
  const harness = makeFxHarness();
  const controller = createStatusEmitterController({ world, fx: harness.fx });

  const view = {
    entities: [
      {
        id: 7,
        kind: "player",
        pos: { x: 10, y: 5 },
        facing: { dx: 1, dy: 0 },
        tags: [],
        weaponVfx: [
          {
            id: "venom_weapon",
            slot: "weapon",
            carryAnchor: { forward: […]

> TOOL

tool_use exec_command
id: call_CuaZ01xFavu2ZQzKkui1BIEx
```json
{
  "cmd": "sed -n '1,190p' src/rules/systems/combatSystem.js",
  "workdir": "/home/pjensen/Repos/JSHack",
  "max_output_tokens": 20000
}
```

> TOOL

tool_use exec_command
id: call_HMX0MoBO3Ovsl3jo8rrFtWxI
```json
{
  "cmd": "sed -n '700,820p' src/rules/data/affixes.js",
  "workdir": "/home/pjensen/Repos/JSHack",
  "max_output_tokens": 16000
}
```

> TOOL

tool_use exec_command
id: call_hu7IQGIor7fUhvo9CMzEbrhB
```json
{
  "cmd": "sed -n '700,790p' src/display/fx/meleeSlashFx.js",
  "workdir": "/home/pjensen/Repos/JSHack",
  "max_output_tokens": 12000
}
```

> TOOL

tool_use exec_command
id: call_ATibMHonRUhCHItUu6EsKKsQ
```json
{
  "cmd": "sed -n '160,230p' src/content/define.js",
  "workdir": "/home/pjensen/Repos/JSHack",
  "max_output_tokens": 12000
}
```

> TOOL

tool_result
id: call_CuaZ01xFavu2ZQzKkui1BIEx
```
Chunk ID: 9f3a15
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 2271
Output:
// src/rules/systems/combatSystem.js
// Processes AttackIntent: computes damage using derived stats, emits events for affix triggers, applies Vitality changes.

import { AttackIntent } from '../components/Intents/AttackIntent.js';
import { Equipment, NON_AMMO_GEAR_SLOTS } from '../components/Equipment.js';
import { Vitality } from '../components/Vitality.js';
import { applyHealing } from '../utils/applyHealing.js';
import { ItemInfo } from '../components/ItemInfo.js';
import { Faction } from '../components/Faction.js';
import { Player } from '../components/Player.js';
import { STAMINA_REGEN_COOLDOWN } from '../data/regenConstants.js';
import { Position } from '../components/Position.js';
import { Stamina } from '../components/Stamina.js';
import { NamedIdentity } from '../components/NamedIdentity.js';
import { ActiveEffects } from '../components/ActiveEffects.js';
import { COMBAT_POSTURES } from '../components/CombatPosture.js';
import { mulberry32, rngInt, rollDice, combatSeed, pct } from '../utils/rng.js';
import { dealDamage } from '../utils/dealDamage.js';
import { areFactionsHostile } from '../utils/factionHostility.js';
import { resolveCombatSnapshot } from '../utils/resolveCombatSnapshot.js';
import { applyWeaponCoatingOnHit, WEAPON_COATING_DEFS } from '../data/weaponCoatings.js';
import { createStatusEvent } from '../../shared/events/statusEvent.js';
import { Beatitude, BUC_CURSED, BUC_BLESSED } from '../components/Beatitude.js';
import { CreatureType, CREATURE_TYPES } from '../components/CreatureType.js';
import { Traits } from '../components/Traits.js';
import {
    createLegacyCombatFrame,
    runLegacyMonsterHook,
} from '../utils/legacyAffixDispatch.js';
import { ensureEquippedAffixTopology } from '../utils/affixTopology.js';
import { buildProcContext, applyPendingDamageProcPhase, applyReactionProcPhase } from […]

> TOOL

tool_result
id: call_HMX0MoBO3Ovsl3jo8rrFtWxI
```
Chunk ID: abd7a2
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 2032
Output:
  const source = (spec?.triggerScripts && typeof spec.triggerScripts === "object") ? spec.triggerScripts : null;
  const out = Object.create(null);
  if (source) {
    for (const [trigger, refs] of Object.entries(source)) {
      const list = normalizeRefList(refs);
      if (list.length > 0) out[String(trigger)] = list;
    }
    return out;
  }

  const legacyTriggers = Array.isArray(spec?.triggers) ? spec.triggers : [];
  const legacyScript = spec?.script ?? null;
  for (let i = 0; i < legacyTriggers.length; i++) {
    const trigger = String(legacyTriggers[i] || "");
    const list = normalizeRefList(null, legacyScript);
    if (trigger && list.length > 0) out[trigger] = list;
  }
  return out;
}

function normalizePassiveRefs(spec) {
  if (Array.isArray(spec?.passiveRefs)) return normalizeRefList(spec.passiveRefs);
  if (Array.isArray(spec?.passives)) return normalizeRefList(spec.passives);
  return normalizeRefList(null, spec?.passive ?? spec?.passiveRef ?? null);
}

function normalizeAffixRecord(id, spec) {
  const normalizedId = String(id || "").trim();
  if (!normalizedId) throw new Error("affix id is required");
  const slots = Array.isArray(spec?.slots) ? spec.slots.map((slot) => String(slot || "")).filter(Boolean) : [];
  const triggerScripts = normalizeTriggerScripts(spec);
  const passiveRefs = normalizePassiveRefs(spec);
  return Object.freeze({
    id: normalizedId,
    name: String(spec?.name || normalizedId),
    description: String(spec?.description || ""),
    slots: Object.freeze(slots),
    weight: Number(spec?.weight || 0),
    elementTint: spec?.elementTint || null,
    passiveRefs: Object.freeze(passiveRefs),
    triggerScripts: Object.freeze(Object.fromEntries(
      Object.entries(triggerScripts).map(([trigger, refs]) => [trigger, Object.freeze(refs.slice())]),
    )), […]

> TOOL

tool_result
id: call_hu7IQGIor7fUhvo9CMzEbrhB
```
Chunk ID: 743721
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 997
Output:
    ctx.lineWidth = fx.lineWidth;
    ctx.setLineDash([0.08, 0.06]);
    ctx.beginPath();
    ctx.arc(fx.x, fx.y, R, fx.startAngle, fx.startAngle + currentSweep, currentSweep < 0);
    ctx.stroke();
    ctx.setLineDash([]);
  }

  // ── Event wiring ──────────────────────────────────────────────────────

  function installListeners({ world, getPosition, isPlayer }) {
    // Melee hit: spawn weapon-appropriate slash VFX
    world.on('damaged', (ev) => {
      const { source, target, amount, critical, impactProfile, impactVector, offhand, cause } = ev;
      // Only fire for melee weapon hits (impactProfile present, cause is melee)
      if (!impactProfile) return;
      if (cause !== 'melee') return;

      // Skip unarmed — this visual language is for weapon-wielders only
      const weaponClass = impactProfile.weaponClass || 'weapon';
      if (weaponClass === 'unarmed') return;

      const a = Number(source || 0) | 0;
      const t = Number(target || 0) | 0;
      if (!(a > 0) || !(t > 0)) return;

      const apos = getPosition(a);
      const tpos = getPosition(t);
      if (!tpos) return;

      // Place FX origin 60% from attacker toward target — near the weapon's reach,
      // close to the attacker's facing dot rather than centered on the target.
      const ox = apos ? apos.x + (tpos.x - apos.x) * 0.6 : tpos.x;
      const oy = apos ? […]

> TOOL

tool_result
id: call_ATibMHonRUhCHItUu6EsKKsQ
```
Chunk ID: 84663d
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 869
Output:
    weight: Number(def.weight ?? 1),
    value: Number(def.value ?? 0),
    description: def.description || def.name,
    identified: def.identified ?? false,
    tags: Array.isArray(def.tags) ? def.tags.slice() : [],
  };

  // Equipment-specific
  if (catalogKind === 'equipment') {
    catalogEntry.bonuses = def.bonuses || {};
    catalogEntry.damageDice = def.damageDice || null;
    catalogEntry.damageType = def.damageType || null;
    catalogEntry.staminaCost = def.staminaCost ?? null;
    catalogEntry.twoHanded = def.twoHanded || false;
    catalogEntry.maxSockets = def.maxSockets || 0;
    if (def.combatFlavor) catalogEntry.combatFlavor = def.combatFlavor;
    if (def.range) catalogEntry.range = def.range;
    if (def.affixes) catalogEntry.affixes = def.affixes;
    if (def.subtype) catalogEntry.subtype = def.subtype;
    if (def.beatitude) catalogEntry.beatitude = def.beatitude;
    if (Array.isArray(def.procPackages) && def.procPackages.length > 0) catalogEntry.procPackages = def.procPackages.slice();
    if (def.tags) catalogEntry.tags = def.tags;
    if (def.maxCharges != null) catalogEntry.maxCharges = def.maxCharges;
    if (def.charges != null) catalogEntry.charges = def.charges;
    if (def.dropRequirement) catalogEntry.dropRequirement = def.dropRequirement;

    // Swing profile — authored weapon VFX identity
    if (def.swingProfile) {
      const sp = def.swingProfile;
      if (sp.lengthCm) catalogEntry.weaponLengthCm = sp.lengthCm;
      if (sp.tint || sp.density || sp.alphaStops || sp.widthScale || sp.handleStart) {
        catalogEntry.weaponVfxProfile = {};
        if (sp.density === 'heavy')  catalogEntry.weaponVfxProfile.length = 1.18;
        if (sp.density === 'light')  catalogEntry.weaponVfxProfile.length = 0.85;
        if (sp.length)      catalogEntry.weaponVfxProfile.length = sp.length;
        if (sp.widthScale)   catalogEntry.weaponVfxProfile.widthScale = sp.widthScale;
        if (sp.handleStart)  catalogEntry.weaponVfxProfile.handleStart […]

> AGENT

There is already more coverage than the initial examples: weapon affixes have `elementTint`, coatings have `elementTint`, and attacker active effects can contribute tint through `EFFECT_DEFS`. The gap is that this is rules-combat-hit-specific today, so missed swings/attack swings and carry VFX projection can diverge, and non-element magical effects without `elementTint` have no generic blue fallback.

> TOOL

tool_use exec_command
id: call_DlMHI4uuAoh5iRurDJd5hYPm
```json
{
  "cmd": "sed -n '460,530p' src/rules/data/effectDefs.js",
  "workdir": "/home/pjensen/Repos/JSHack",
  "max_output_tokens": 12000
}
```

> TOOL

tool_use exec_command
id: call_hmaxFITjCSTwnJUPgQsfPEm9
```json
{
  "cmd": "rg -n \"ignite_weapons|poison_blade|magic|elementTint|weapon.*effect|coating|dip\" src/rules/data src/content src/rules/content tests --glob '!src/lib/**'",
  "workdir": "/home/pjensen/Repos/JSHack",
  "max_output_tokens": 26000
}
```

> TOOL

tool_use exec_command
id: call_RoON113O757YEYN1fc6wWJnO
```json
{
  "cmd": "sed -n '320,570p' src/rules/systems/combatSystem.js",
  "workdir": "/home/pjensen/Repos/JSHack",
  "max_output_tokens": 22000
}
```

> TOOL

tool_use exec_command
id: call_uZKnOi5WerpzUlpfMzXpBot8
```json
{
  "cmd": "sed -n '1,220p' src/rules/components/ItemInfo.js",
  "workdir": "/home/pjensen/Repos/JSHack",
  "max_output_tokens": 12000
}
```

> TOOL

tool_result
id: call_DlMHI4uuAoh5iRurDJd5hYPm
```
Chunk ID: 7ce489
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 380
Output:
    id: "dark_sight",
    keys: ["dark_sight"],
    operation: "none",
    statuses: ["dark_sight"],
    description: "Dark sight. See in complete darkness.",
  },
  {
    id: "battle_fury",
    keys: ["battle_fury"],
    operation: "none",
    statuses: ["battle_fury"],
    description: "Battle fury. Combat prowess heightened.",
  },
  {
    id: "lichdom_echo",
    keys: ["lichdom_echo"],
    operation: "none",
    statuses: ["lichdom_echo"],
    description: "Lichdom echo. Undead resilience.",
  },
  {
    id: "fey_grace",
    keys: ["fey_grace"],
    operation: "none",
    statuses: ["fey_grace"],
    description: "Fey grace. Movement enhanced, magic surging.",
  },
  {
    id: "bloodthirst",
    keys: ["bloodthirst"],
    operation: "none",
    statuses: ["bloodthirst"],
    description: "Bloodthirst. Healing from attacks.",
  },
  // ── Buff / Rotation ability statuses ──────────────────────────────
  {
    id: "fire_weapon",
    keys: ["fire_weapon"],
    operation: "none",
    statuses: ["fire_weapon"],
    elementTint: "fire",
    description: "Fire weapon. Attacks deal fire damage.",
  },
  {
    id: "marked",
    keys: ["marked", "mark_of_death"],
    operation: "none",
    statuses: ["marked"],
    description: "Marked. Enemies track you more easily.",
  },
  {
    id: "stasis",
    keys: ["stasis"],
    operation: "none",
    statuses: ["stasis"],
    description: "Stasis. Time flows differently around you.",
  },
];

```

> TOOL

tool_result
id: call_hmaxFITjCSTwnJUPgQsfPEm9
```
Chunk ID: 9c20b1
Wall time: 0.0001 seconds
Process exited with code 0
Original token count: 11091
Output:
Warning: truncated output (original token count: 11091)
Total output lines: 425

tests/dataIntegrity.test.mjs:39:    ].includes(item.type) || ['magic', 'equipment', 'food', 'material', 'seed', 'ingredient'].includes(item.catalogKind);
tests/audioNewSounds.test.js:24:    "water:magic",
tests/itemMaterials.test.mjs:63:Deno.test("createItemById routes magic items through materialized loader", () => {
tests/messageWiring.test.mjs:143:      coating: { kind: "poison", charges: 12 },
tests/messageWiring.test.mjs:157:  assert(messageLog.entries[0].text.includes("coat"), "poison coat message should mention coating");
tests/stoneskinPotionHooks.test.mjs:148:Deno.test("stoneskin potion on_dip (via apply pipeline) petrifies target item", () => {
tests/stoneskinPotionHooks.test.mjs:174:  assert(!world.isAlive(potion), "dipping should consume stoneskin potion");
tests/chestLootBalance.test.mjs:43:Deno.test("chest:magic drop count stays non-empty and within max roll bound", () => {
tests/chestLootBalance.test.mjs:44:  assertChestRollBounds("chest:magic", 3, 120);
tests/chestLootBalance.test.mjs:53:  assertChestEquipEntriesResolve("chest:magic", 3, 120);
tests/chestLootBalance.test.mjs:72:Deno.test("chest:magic never drops more than 1 weapon", () => {
tests/chestLootBalance.test.mjs:75:    const drops = resolveLootTable("chest:magic", rng, 3);
tests/fountainRuleAuthoring.test.mjs:127:    ["drink", "dip"],
tests/fountainRuleAuthoring.test.mjs:133:    ["drink", "dip", "purify"],
tests/fountainRuleAuthoring.test.mjs:139:    ["drink", "dip"],
tests/enchantingBench.test.mjs:65:  assertEquals(crafted[0]?.metadata?.rarity, "magic");
tests/applyDataDriven.test.mjs:83:  daggerInfoBefore.coating = { kind: "poison", charges: 5 };
tests/applyDataDriven.test.mjs:92:  assert(daggerInfo?.coating, "dagger should receive a coating payload");
tests/applyDataDriven.test.mjs:93:  assertEquals(daggerInfo.coating.kind, "poison");
tests/applyDataDriven.test.mjs:94:  assertEquals(daggerInfo.coating.charges, 17, "poison coating should add granted charges on top of existing");
src/rules/data/materialReactions.js:76:    id: "water_dip_sets_potion_beatitude",
src/rules/data/materialReactions.js:77:    sourceEvents: ["water:dipped"],
src/rules/data/materialReactions.js:79:    eventKind: "water:dipped",
src/rules/data/materialReactions.js:108:    id: "water_dip_sets_equipment_beatitude",
src/rules/data/materialReactions.js:109:    sourceEvents: ["water:dipped"],
src/rules/data/materialReactions.js:111:    eventKind: "water:dipped",
src/rules/data/materialReactions.js:113:      // Holy water two-step: cursed → uncursed first, then […]

> TOOL

tool_result
id: call_RoON113O757YEYN1fc6wWJnO
```
Chunk ID: 7188d3
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 2960
Output:
                return true;
            }
        }
    }

    breakStealthOnOffense(world, source, { reason: 'attack', mode: 'melee', targetId: target });
    const positional = getPositionalAttackBonus(world, source, target);
    const actionTags = Array.isArray(tags) ? [...tags, `relation:${positional.relation}`] : [`relation:${positional.relation}`];
    const attackPos = world.get(source, Position);
    const weaponFamily = resolveEventWeaponFamily(world, weaponId);
    world.emit('combat:melee:attack', {
        attacker: source,
        defender: target,
        weaponId: weaponId || 0,
        weaponFamily,
        offhand: !!offhand,
        at: attackPos ? { x: attackPos.x, y: attackPos.y } : undefined,
    });
    let attackBonus = atkSnapshot.attackBonus + hitPenalty + positional.attackBonus;
    const armorClass = defSnapshot.armorClass;

    const seed = combatSeed(world.seed, world.step, source, target, seedSalt);
    const r = mulberry32(seed);
    const d20 = rngInt(r, 1, 20);
    const totalToHit = d20 + attackBonus;
    let isCrit = d20 === 20;
    const isNat1 = d20 === 1;

    if (!isCrit && (isNat1 || totalToHit < armorClass)) {
        world.emit?.('status', createStatusEvent({ id: target, kind: 'miss', source }));
        applyPendingDamageProcPhase(world, source, buildProcContext('onMiss', {
            source, target, item: weaponId || 0, damage: 0,
            damageType: 'physical', crit: false, tags: actionTags, scratch: {}, offhand,
        }), () => r());
        return true;
    }

    // ── Dodge check: defender's evade stat grants a chance to avoid the hit entirely ──
    if (!isCrit && defSnapshot.evade > […]

> TOOL

tool_result
id: call_uZKnOi5WerpzUlpfMzXpBot8
```
Chunk ID: 1dae07
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 947
Output:
import { defineComponent } from "../../lib/ecs-js/index.js";
/**
 * ItemInfo — rules-side description of an item.
 * Used for inventory logic, weight calculations, equipment slots, etc.
 * No display names, glyphs, or color info.
 */
export const ItemInfo = defineComponent(
  "ItemInfo",
  {
    type: "", // logical category, e.g. "weapon", "potion", "scroll"
    slot: "", // intended equipment or container slot, e.g. "hand", "bag"
    weight: 0, // numeric weight (for encumbrance or turn cost)
    value: 0, // optional numeric value for trade/scoring
    description: "", // flavor text description of the item
    count: 1, // stacking count; >=1 for any item entity
    bonuses: {}, // flat bonuses: { attack, defense, maxHp, critChance, critMult, ... }
    twoHanded: false, // requires both hands; blocks offhand slot
    rarity: 1,
    rarityName: "common",
    // Legacy compatibility arrays. Runtime affixes/enchantments/sockets should
    // prefer attached topology nodes; see RUNTIME_TOPOLOGY_DOCTRINE.md.
    affixes: [], // list of affix ids applied to this item (rules/data/affixes)
    sockets: [], // gem ids socketed into this item (e.g. ['gem_ruby'])
    maxSockets: 0, // maximum number of gem sockets this item can hold
    weaponLengthCm: null, // physical weapon length […]

> TOOL

tool_use exec_command
id: call_iYE9VQ5ZCeykatQDa7A5KLJU
```json
{
  "cmd": "sed -n '1,220p' /home/pjensen/.codex/RTK.md",
  "workdir": "/home/pjensen/Repos/JSHack",
  "max_output_tokens": 12000
}
```

> TOOL

tool_result
id: call_iYE9VQ5ZCeykatQDa7A5KLJU
```
Chunk ID: a1d97a
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 121
Output:
# RTK - Rust Token Killer (Codex CLI)

**Usage**: Token-optimized CLI proxy for shell commands.

## Rule

Always prefix shell commands with `rtk`.

Examples:

```bash
rtk git status
rtk cargo test
rtk npm run build
rtk pytest -q
```

## Meta Commands

```bash
rtk gain            # Token savings analytics
rtk gain --history  # Recent command savings history
rtk proxy <cmd>     # Run raw command without filtering
```

## Verification

```bash
rtk --version
rtk gain
which rtk
```

```

> AGENT

I have enough repo context to see the main design choice now. The implementation can be generic, but I need to lock how broad the fallback should be so we do not make every “magic rarity” item glow blue by accident.

> TOOL

tool_use request_user_input
id: call_wOvT8k3rt1KOjs4qTijBL3jy
```json
{
  "autoResolutionMs": 60000,
  "questions": [
    {
      "header": "Fallback",
      "id": "magic_fallback",
      "question": "For weapon effects that are magical but not elemental, what should produce the blue swing treatment?",
      "options": [
        {
          "label": "Explicit only (Recommended)",
          "description": "Only affixes/coatings/effects with an authored visual affinity or element tint affect swings; avoids accidental blue noise."
        },
        {
          "label": "Any enchantment",
          "description": "Any weapon affix/enchantment without a stronger tint falls back to blue; more visible but less semantically precise."
        },
        {
          "label": "Any magic rarity",
          "description": "Any equipped magic-rarity weapon falls back to blue; broadest and likely visually noisy."
        }
      ]
    },
    {
      "header": "Outcomes",
      "id": "swing_outcomes",
      "question": "Which melee outcomes should show the weapon's enchantment styling?",
      "options": [
        {
          "label": "All swings (Recommended)",
          "description": "Hits, misses, dodges, and parries use the same weapon visual affinity so the swing itself communicates the enchantment."
        },
        {
          "label": "Hits only",
          "description": "Only successful damage arcs change; misses and dodges stay neutral."
        },
        {
          "label": "Hits and misses",
          "description": "Ordinary misses inherit styling, but dodge/parry reactions remain neutral."
        }
      ]
    }
  ]
}
```

> TOOL

tool_result
id: call_wOvT8k3rt1KOjs4qTijBL3jy
```
{"answers":{"magic_fallback":{"answers":["Explicit, remember, this might be from an echantment, a gemstone, anything -- so while I was saying blue, it almost certaonly will not cover the whole concept (e..g) void weapon, electric weapon, and so on.\n\ncatch my drift?"]},"swing_outcomes":{"answers":["All swings (Recommended)"]}}}
```

> AGENT

That matches the architecture I’m seeing: this should be an authored “weapon visual affinity” contract, not a magic-blue fallback. I’ll shape the plan around resolving the strongest active visual affinity from affixes, coatings, socket/proc topology, item identity, and actor weapon-buff effects, then feeding that into every melee swing outcome.

> TOOL

tool_use exec_command
id: call_y1mz0zzupkMU4MfyPFaTOiDJ
```json
{
  "cmd": "rtk sed -n '1,240p' src/rules/data/gemSocketAffixes.js",
  "workdir": "/home/pjensen/Repos/JSHack",
  "max_output_tokens": 18000
}
```

> TOOL

tool_use exec_command
id: call_MOLVQk65ko2Ev1uWVLxxRfLp
```json
{
  "cmd": "rtk sed -n '1,260p' src/rules/data/procPackages.js",
  "workdir": "/home/pjensen/Repos/JSHack",
  "max_output_tokens": 22000
}
```

> TOOL

tool_use exec_command
id: call_6rjsBonSchkG1RFkk2MaqxDZ
```json
{
  "cmd": "rtk rg -n \"GemSocketNode|ProcNode|EnchantmentNode|StatusEffectNode|descendantsWith|childrenWith|attached|effectNode|procPackage|visual|elementTint\" src/rules src/bridge tests --glob '!src/lib/**'",
  "workdir": "/home/pjensen/Repos/JSHack",
  "max_output_tokens": 30000
}
```

> TOOL

tool_result
id: call_y1mz0zzupkMU4MfyPFaTOiDJ
```
Chunk ID: 489c3d
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 2995
Output:
// rules/data/gemSocketAffixes.js
// Registers affix definitions and passive scripts for gem socket affixes.
// Provides attachGemSocketNodes() for attaching proc topology to a weapon.
// Call installGemSocketListener(world) once during world setup.

import { registerAffixDefinition } from "./affixes.js";
import { registerScript, ScriptVerb } from "../scripting.js";
import {
  addAttachedComponent,
  attachProcNode,
  gateEventKind,
  gateChance,
  effectApplyStatus,
  effectBonusDamageFlat,
  effectRestoreResource,
  effectAddCritChance,
} from "../utils/statProcAuthoring.js";
import { GemSocketNode } from "../components/GemSocketNode.js";
import { Charges } from "../components/Charges.js";
import { Equipment } from "../components/Equipment.js";
import { ItemInfo } from "../components/ItemInfo.js";
import {
  addCharges,
  resolveCharges,
  spendCharges,
} from "../utils/charges.js";

// ── Passive script keys ──────────────────────────────────────────
const S_RUBY     = "gem_socket:ruby:passive";
const S_SAPPHIRE = "gem_socket:sapphire:passive";
const S_EMERALD  = "gem_socket:emerald:passive";
const S_DIAMOND  = "gem_socket:diamond:passive";
const S_TOPAZ    = "gem_socket:topaz:passive";
const S_AMETHYST = "gem_socket:amethyst:passive";
const S_OPAL     = "gem_socket:opal:passive";
const S_OBSIDIAN = "gem_socket:obsidian:passive";
const S_GARNET   = "gem_socket:garnet:passive";
const S_JACINTH  = "gem_socket:jacinth:passive";
const S_AQUAMARINE = "gem_socket:aquamarine:passive";
const S_VOIDSTONE  = "gem_socket:voidstone:passive";
const S_FLUORITE   = "gem_socket:fluorite:passive";

// ── Fluorite charge/discharge thresholds ─────────────────────────
const FLUO_MAX_CHARGES      = 6;  // stacks to full charge
const FLUO_DISCHARGE_MIN    = 3;  // minimum stacks to discharge
const FLUO_DAMAGE_PER_STACK = 2;  // bonus electric damage per […]

> TOOL

tool_result
id: call_MOLVQk65ko2Ev1uWVLxxRfLp
```
Chunk ID: a334df
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 2342
Output:
import { children } from "../../lib/ecs-js/index.js";
import { destroySubtree } from "../../lib/ecs-js/hierarchy.js";
import { ActiveEffects } from "../components/ActiveEffects.js";
import { Faction } from "../components/Faction.js";
import { ItemInfo } from "../components/ItemInfo.js";
import { Lifespan } from "../components/Lifespan.js";
import { NamedIdentity } from "../components/NamedIdentity.js";
import { Owner } from "../components/Owner.js";
import { PetState } from "../components/PetState.js";
import { Position } from "../components/Position.js";
import { ProcPackageNode } from "../components/ProcPackageNode.js";
import { Vitality } from "../components/Vitality.js";
import { isOpaque } from "../environment/dungeon/tileMap.js";
import { registerScript, getScriptHandlers, ScriptVerb } from "../scripting.js";
import { ensureActiveEffects } from "../utils/effects.js";
import { upsertTimedEffect } from "../utils/effectSemantics.js";
import { areFactionsHostile } from "../utils/factionHostility.js";
import { chebyshevScalar } from "../utils/distance.js";
import { findNearestValidTileAround } from "../utils/queries.js";
import { spawnMonsterEntity } from "../utils/spawnMonsterEntity.js";
import {
  addAttachedComponent,
  attachDerivedExpression,
  attachProcNode,
  exprAddConst,
  gateChance,
  gateEventKind,
  gateHasActionTag,
} from "../utils/statProcAuthoring.js";

export const PROC_PACKAGE_KEYS = Object.freeze({
  EchoStrike: "procPackage:echoStrike",
  RicochetTheology: "procPackage:ricochetTheology",
  DoomClock: "procPackage:doomClock",
  SoulMortgage: "procPackage:soulMortgage",
  CataclysmChain: "procPackage:cataclysmChain",
  BloodTithe: "procPackage:bloodTithe",
  FoolsErrand: "procPackage:foolsErrand",
  VenomClock: "procPackage:venomClock",
  HollowTide: "procPackage:hollowTide",
  DeathAscendant: "procPackage:deathAscendant",
  ThunderGod: "procPackage:thunderGod",
  BloodCovenant: "procPackage:bloodCovenant",
  PredatorMark: "procPackage:predatorMark",
  SoulAscendant: "procPackage:soulAscendant",
  EternalHunger: "procPackage:eternalHunger",
  EclipseHammer: "procPackage:eclipseHammer",
  GlacierSigil: "procPackage:glacierSigil",
  ConductionLens: "procPackage:conductionLens",
  EchoGrimoire: "procPackage:echoGrimoire",
  SerpentBoundBreeches: "procPackage:serpentBoundBreeches", […]

> TOOL

tool_result
id: call_6rjsBonSchkG1RFkk2MaqxDZ
```
Chunk ID: c9bf78
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 11317
Output:
Warning: truncated output (original token count: 11317)
Total output lines: 438

tests/itemGrouping.test.mjs:5:Deno.test("groupDisplayItems coalesces visually identical items and sums counts", () => {
tests/statusEffectApplication.test.mjs:7:import { StatusEffectNode } from "../src/rules/components/StatusEffectNode.js";
tests/statusEffectApplication.test.mjs:35:  assertEquals(world.get(node, StatusEffectNode), {
tests/statusEffectApplication.test.mjs:123:  assertEquals([...world.query(StatusEffectNode)].length, 1);
tests/runtimeTopologyComponents.test.mjs:7:  StatusEffectNode,
tests/runtimeTopologyComponents.test.mjs:15:  world.add(node, StatusEffectNode, {
tests/runtimeTopologyComponents.test.mjs:37:  assertEquals(world.get(node, StatusEffectNode), {
tests/shopkeeperSystem.test.mjs:167:Deno.test("shopkeeperSystem blocks exiting shop with unpaid attached debt even when item is gone", () => {
tests/shopkeeperSystem.test.mjs:202:  assert(!world.has(playerId, MoveIntent), "move intent should be consumed when attached debt is unpaid");
tests/shopkeeperSystem.test.mjs:205:  assert(blocked[0].bill === 120, "event should report attached debt total");
tests/actionTransaction.test.mjs:6:import { EnchantmentNode } from "../src/rules/components/EnchantmentNode.js";
tests/actionTransaction.test.mjs:9:import { descendantsWith } from '../src/rules/utils/topology.js';
tests/actionTransaction.test.mjs:159:  const nodes = [...descendantsWith(world, e, EnchantmentNode)];
tests/weaponVisuals.test.mjs:28:Deno.test("buildCatalogItem propagates weapon visual metadata into ItemInfo", () => {
tests/weaponVisuals.test.mjs:59:Deno.test("weapon visual overrides take priority over inferred defaults", () => {
tests/aggroTargetVisualEvents.test.mjs:103:Deno.test("taunt steering shifts aggro target visuals to the taunter", () => {
tests/agentTools.test.mjs:151:Deno.test("content-id audit classifies definitions, tests, visuals, and references", () => {
tests/agentTools.test.mjs:166:    "visual",
tests/topologyHelpers.test.mjs:5:  childrenWith,
tests/topologyHelpers.test.mjs:6:  descendantsWith,
tests/topologyHelpers.test.mjs:28:Deno.test("childrenWith yields direct matching children in ECS child order", () => {
tests/topologyHelpers.test.mjs:39:  assertEquals([...childrenWith(world, parent, Marker)], [
tests/topologyHelpers.test.mjs:58:Deno.test("descendantsWith yields matching descendants depth-first", () => {
tests/topologyHelpers.test.mjs:71: […]

> AGENT

<proposed_plan>
# Weapon Swing Visual Affinity

**Summary**
- Treat “swing color/effect” as an authored weapon visual affinity, not a generic magic fallback.
- Resolve the strongest active affinity from weapon identity, affixes/enchantments, coatings/dips, socketed gems, proc packages, and actor weapon-buff effects.
- Apply it to all melee swing outcomes: hit, miss, dodge, and parry.

**Key Changes**
- Add a rules-side resolver, likely near `src/rules/data/weaponVisuals.js`, that returns a compact payload like:
  `{ id, elementTint, swingStyle, priority }`.
- Feed that resolver from:
  - affix `elementTint` / future `visualAffinity`
  - coating definitions, including existing dip coating kinds
  - `EnchantmentNode` / affix topology descendants
  - `GemSocketNode` and proc-package topology with authored affinity mappings
  - active actor effects such as `fire_weapon`
- Extend combat melee event payloads so miss/dodge/parry paths carry the same impact/swing profile that hits already carry.
- Extend `meleeSlashFx` to consume `swingStyle` in addition to `elementTint`:
  - poison/acid/frost/electric/etc. tint the weapon trail
  - fire/flame uses a flaming treatment, not just orange recolor
  - void/arcane/blood/etc. are explicit authored styles only, no broad “magic rarity = blue” rule
- Reuse the resolver in bridge weapon VFX projection so carry/projectile/swing semantics do not drift.

**Tests**
- Add resolver tests for:
  - poison coating -> […]