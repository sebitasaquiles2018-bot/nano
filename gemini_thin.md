# gemini_thin.md — Image-MCP setup notes

How to get the two custom image-generation MCPs registered with Claude Code on a fresh machine, plus prompting best practices for the model that's now the biographical-mode default.

This file is portable: a fresh Claude instance landing in this repo should be able to read it top-to-bottom and rebuild the toolchain end-to-end without other context. Companion to `bio.md` (the biographical workflow itself).

The two MCPs:

| MCP | Lives at | Wraps | Used for |
|---|---|---|---|
| `gemini-pro-thin` | `~/.claude/mcp-servers/gemini-pro-thin/` | Gemini 3 Pro / NB2 (Flash) image endpoints | Pages that genuinely need `compose_images` (2–10 ref locks at once); cheap T1–T3 pages on Flash |
| `openai-image-2` | `~/.claude/mcp-servers/openai-image-2/` | OpenAI gpt-image-2 (`/v1/images/{generations,edits}`) | **Default for biographical novels** — oil-painting realism register, T5 single-shot text rendering |

Both are local stdio MCPs. Both are project-scoped (registered under the nano project's block in `~/.claude.json`, not globally).

---

## Part A — `gemini-pro-thin` (Gemini wrapper, no prompt cap)

### Why it exists

The upstream `gemini-nanobanana-mcp` npm package enforces a **wrapper-side** prompt-length limit of 2000 characters. The underlying Gemini API has no such cap. Under that wrapper, biographical-mode prompts (Style Block + register block + character lock + panel description + verbatim lettering + restrictions block) routinely exceed 2000 chars — and the wrapper either errored with a `too_big`-style rejection or quietly trimmed the prompt, dropping the load-bearing disambiguation at the end. Either way: a recurring failure mode that wasted budget on bad pages.

`gemini-pro-thin` is a drop-in replacement at the tool-name level. Same surface, no cap, plus small ergonomic improvements (overwrites instead of `_1`/`_2` collision suffixes; longer 120s timeout for slow Pro responses on T5 pages).

### Package contents

```
~/.claude/mcp-servers/gemini-pro-thin/
├── index.mjs           # ~330 lines, the actual MCP server
├── package.json        # depends on @modelcontextprotocol/sdk
├── node_modules/       # populated by `npm install`
└── HANDOFF.md          # build notes (not required at runtime)
```

Tool surface (called as `mcp__gemini-pro-thin__*`):

- `generate_image(prompt, saveToFilePath)`
- `edit_image(prompt, image{path|dataBase64, mimeType?}, saveToFilePath)`
- `compose_images(prompt, images[2..10], saveToFilePath)`
- `style_transfer` is intentionally **not** implemented.

### Setup from scratch

1. **Create the folder** — `mkdir -p ~/.claude/mcp-servers/gemini-pro-thin && cd ~/.claude/mcp-servers/gemini-pro-thin`

2. **`package.json`:**

   ```json
   {
     "name": "gemini-pro-thin-mcp",
     "version": "0.1.0",
     "private": true,
     "type": "module",
     "main": "index.mjs",
     "dependencies": { "@modelcontextprotocol/sdk": "^1.17.4" }
   }
   ```

3. **`index.mjs`** — the canonical copy is the file already at `~/.claude/mcp-servers/gemini-pro-thin/index.mjs`. Architectural shape: reads `GEMINI_API_KEY` and `GEMINI_IMAGE_ENDPOINT` from env, exits on missing; exposes 3 tools over stdio; per call, builds a `:generateContent` request (text part + optional inline-data image parts), POSTs to `${ENDPOINT}?key=...`, retries up to 3× on 429/5xx with exponential backoff, 120s per-request timeout; saves the first inline image part to `saveToFilePath` (overwriting), creates parent dirs as needed; allowed inputs `image/{png,jpeg,webp,gif}`; rejects `../` traversal.

4. **`npm install`** — pulls only `@modelcontextprotocol/sdk` and transitive deps.

5. **Register in `~/.claude.json`** under the nano project's `mcpServers`:

   ```json
   "gemini-pro-thin": {
     "type": "stdio",
     "command": "node",
     "args": ["/Users/andresrodriguez/.claude/mcp-servers/gemini-pro-thin/index.mjs"],
     "env": {
       "GEMINI_API_KEY": "<google-ai-studio-key>",
       "GEMINI_IMAGE_ENDPOINT": "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent"
     }
   }
   ```

   Path must be absolute — `~` and relative paths are not honored.

6. **Restart Claude Code.** New tool names appear as `mcp__gemini-pro-thin__{generate_image,edit_image,compose_images}`.

7. **Smoke test.** Call `generate_image` with a >2000-char prompt and confirm: returns a saved PNG, no error, no `_1` suffix on the filename, image visibly matches the subject. Save artifact to `output/imagegen/smoke/gemini-pro-thin-smoke-<date>.png`.

### Env vars

- **`GEMINI_API_KEY`** — required Google AI Studio key. MCP exits at startup if missing.
- **`GEMINI_IMAGE_ENDPOINT`** — required, full URL **including** `:generateContent`. Switches model identity without touching the server:
  - Pro: `https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent`
  - Flash (NB2): `https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent`

For nano, the endpoint is currently pinned to **Pro** because biographical hero pages are calibrated to Pro's T5 ceiling. Switch to Flash for cheap T1–T3 pages by editing the env var and restarting.

### Behavior diff vs upstream nanobanana

| Aspect | nanobanana | gemini-pro-thin |
|---|---|---|
| Prompt char cap | 2000 | none |
| File collision | `_1`, `_2`, ... | overwrites directly |
| Timeout | shorter | 120s |
| `style_transfer` | yes | omitted |

---

## Part B — `openai-image-2` (gpt-image-2 wrapper, cost-disciplined)

### Why it exists

Built 2026-04-22 during Newton Vol 1 production as a fallback for geometry-critical pages where Gemini drifted (orbital diagrams, distance comparisons, Principia synthesis). Honda Vol 1 then promoted it to **default** for biographical mode after register tests showed gpt-image-2 produces the oil-painting realism the user wanted (vs Gemini Pro's digital-painting / concept-art register), and the May 2 test plus Honda production confirmed gpt-image-2 standard hits T5 single-shot.

The MCP is built around one operational rule: **`thinking` mode is opt-in only, never sent by default.** A prior bad experience on Codex (which forced thinking mode silently) ran up large bills; this wrapper exists in part to make that impossible.

### Package contents

```
~/.claude/mcp-servers/openai-image-2/
├── index.mjs           # ~250 lines
├── package.json
├── package-lock.json
├── node_modules/
└── HANDOFF.md
```

Tool surface (called as `mcp__openai-image-2__*`):

- `generate_image(prompt, saveToFilePath, [size, quality, thinking])`
- `edit_image(prompt, imagePath, saveToFilePath, [size, quality, thinking])`

No `compose_images`. gpt-image-2 only takes one input image per `edit_image` call. Multi-character pages use the lock-the-harder-face strategy (see Part C and `bio.md` §10).

### Setup from scratch

1. **Create the folder** — `mkdir -p ~/.claude/mcp-servers/openai-image-2 && cd ~/.claude/mcp-servers/openai-image-2`

2. **`package.json`:**

   ```json
   {
     "name": "openai-image-2-mcp",
     "version": "0.1.0",
     "type": "module",
     "main": "index.mjs",
     "bin": { "openai-image-2-mcp": "index.mjs" },
     "dependencies": { "@modelcontextprotocol/sdk": "^1.0.0" },
     "engines": { "node": ">=18" }
   }
   ```

3. **`index.mjs`** — canonical copy lives at `~/.claude/mcp-servers/openai-image-2/index.mjs`. Architectural shape: reads `OPENAI_API_KEY` (required), `OPENAI_IMAGE_MODEL` (default `gpt-image-2`), `OPENAI_BASE_URL` (default `https://api.openai.com/v1`); generate calls POST `/images/generations` JSON; edit calls POST `/images/edits` multipart with the image as a Blob; default `size=1024x1024`, `quality=high`, `n=1`; **only sends a `reasoning: { effort: "high" }` field when the caller passes `thinking: true`** — never by default; saves `b64_json` if returned, else fetches `url`, writes to `saveToFilePath`.

4. **`npm install`.**

5. **Get an OpenAI API key.** Sign in to platform.openai.com → API keys → create new secret key. **Pre-test gotcha:** the billing **hard limit** at Settings → Limits is separate from your credit balance. Adding credit doesn't raise it. If you hit `billing_limit_user_error`, raise the limit there before debugging anything else.

6. **Register in `~/.claude.json`** under the nano project's `mcpServers`:

   ```json
   "openai-image-2": {
     "type": "stdio",
     "command": "node",
     "args": ["/Users/andresrodriguez/.claude/mcp-servers/openai-image-2/index.mjs"],
     "env": {
       "OPENAI_API_KEY": "<openai-api-key>",
       "OPENAI_IMAGE_MODEL": "gpt-image-2"
     }
   }
   ```

7. **Restart Claude Code.** Tool names appear as `mcp__openai-image-2__{generate_image,edit_image}`.

8. **Smoke test** — call `generate_image` with `size: "1536x1024"`, default quality, no thinking. Confirm a saved PNG, the `OK gpt-image-2 (standard, q=high, 1536x1024)` text response, and a visible image matching the prompt. The Newton Vol 1 baseline regression is `output/imagegen/smoke/page-15-mcp-standard-test.png`.

### Defaults — the whole point

- `model`: `gpt-image-2`
- `size`: `1024x1024` (use `1536x1024` for biographical landscape pages)
- `quality`: `high`
- `thinking`: **NOT SENT** unless the caller explicitly passes `thinking: true`

**Rule: never pass `thinking: true` without a documented reason.** Acceptable reasons: dense optical/geometric diagram, multi-element synthesis page where standard mode visibly fails after retry. Standard mode hit T5 single-shot on Honda — thinking is rarely needed.

### Costs (April–May 2026 reference)

| Mode | Approx cost / 1024×1024 high-quality call |
|---|---|
| NB2 / Gemini Flash standard | $0.067 |
| Gemini Pro | ~$0.13 |
| **gpt-image-2 standard** | **~$0.21** |
| gpt-image-2 thinking | $0.50–$1+ (variable) |

A 24-page biographical novel on gpt-image-2 standard lands ~$7.50 (10 refs + 24 pages + 3 prototype regens). Newton ($7.35) and Honda ($7.50) both inside this envelope.

### Operational reminders

- The OpenAI key in `~/.claude.json` is the live secret. **Rotate when it leaks** (one was pasted into a chat transcript on 2026-04-22 and flagged for rotation). Never embed the key in committed docs or repo files.
- Codex and Claude both pulling from the same OpenAI key on the same project can collide on rate limits. If image calls suddenly fail with 429s, check whether another agent is also generating.
- `saveToFilePath` is overwritten without prompting — version important pages by giving them unique names rather than relying on the wrapper to preserve old ones.
- The MCP only handles single-image inputs. To do "multi-character" pages on gpt-image-2, lock to one face via `edit_image` and describe the other character richly in the prompt (Part C).

### Common failure modes

| Symptom | Cause / fix |
|---|---|
| `OPENAI_API_KEY not set in env` at startup | env block missing in MCP registration; restart after adding |
| `OpenAI generate failed: 401` | bad / revoked key; rotate and update `~/.claude.json` |
| `OpenAI generate failed: 400 ... billing_limit_user_error` | platform.openai.com → Settings → Limits → raise hard limit |
| `OpenAI generate failed: 429` | rate-limited; retry, or another agent is also hitting the key |
| Returned `url` instead of `b64_json` | normal; the wrapper fetches the URL and writes bytes anyway |
| Image is square when you wanted landscape | pass `size: "1536x1024"` explicitly; the default is `1024x1024` |

---

## Part C — Prompting best practices for `gpt-image-2`

Calibrated against Newton Vol 1 (24 pages) and Honda Vol 1 (25 pages incl. cover). These rules are an addendum to the graphic-novel skill at `~/.claude/skills/graphic-novel/SKILL.md` (Biographical Mode section) and to `bio.md`. They apply specifically to `mcp__openai-image-2__{generate_image,edit_image}` in standard mode — Gemini and the gpt-image-2 thinking-mode call have different sweet spots.

### C.1 Aspect ratio and size

- Biographical mode: **`size: "1536x1024"`** (3:2 landscape). Always pass it explicitly; the wrapper default is square.
- Cover and four-zone montage finale pages also at `1536x1024`. Don't switch to `2048x2048` for "more detail" — gpt-image-2's text rendering is calibrated at 1.5K and the upscaling loses caption legibility.
- Vertical 2:3 fictional graphic novels would use `1024x1536`, but biographical mode is landscape.

### C.2 Prompt structure (the Honda template)

A page prompt has six blocks in this order. Every block is verbatim-paste-able from `04-SCRIPT.md`; do not paraphrase at generation time.

1. **Style Block** — the medium, palette, camera language. Repeated verbatim every page. Holds the volume's visual identity.
2. **Register block (mandatory):**
   > Oil-painting realism. NOT a comic. NO halftones, NO cel shading, NO ink linework. Painted brushwork, cinematic lighting, muted period palette.
3. **Anti-drift directive (mandatory):**
   > NOT a children's book. Serious mature graphic novel, realistic proportions, natural lighting, cinematic composition.
4. **Character lock block(s)** — pasted from `02-CHARACTERS.md`, age-appropriate version. For multi-character pages, see C.7.
5. **Composition / panel description** — single composed scene preferred over panel grids; specify camera (wide, medium, close-up, low angle), foreground / midground / background actions, lighting.
6. **Lettering block** — opens with the verbatim trigger phrase, lists each text element with corner / band placement and the exact quoted string. Closes with the restrictions block. See C.5.

Order matters. Style → register → anti-drift → character lock → scene → lettering. The model anchors on early tokens; putting lettering last keeps text from bleeding into character description.

### C.3 Character lock locks the *visual*, not the *idea*

Lock blocks specify: age, skin tone, hair (color, length, style), face shape, eye color, signature marks (scars, jewelry, tools), clothing (colors and materials), build/posture. They do **not** say "Honda" or "Descartes" by name. The model knows the names of famous figures and will drift toward stock-photo Wikipedia portraits if you let the name carry the lock. **The visual description is the lock.**

For child characters, append: `Realistic child anatomy. NOT cute, NOT mascot proportions, NOT oversized eyes.` Without this, the model drifts toward children's-book aesthetic even with the anti-drift directive.

### C.4 References — `edit_image` is the lock

- For any page with a named character, **always** use `edit_image` against the age-appropriate reference sheet from `refs/`. `generate_image` from text alone will drift on face geometry across pages.
- Pre-flight check before every `edit_image`: confirm the reference file actually exists at the path you're about to pass. The MCP doesn't fail loudly on missing refs — passing a wrong-age or non-existent ref leads to silent age drift across the volume. Honda page-12 protoypte was generated against a non-existent ref because the file hadn't been built yet; the result was reused as if it were locked. Don't.
- One reference per `edit_image` call. For multi-character pages: see C.7.

### C.5 Text rendering — the verbatim and restrictions blocks

gpt-image-2 standard hits T5 (6+ elements, 140–180 words) single-shot when the lettering block is structured. The trigger phrasing matters.

**Open the lettering block with this exact phrase:**

> LETTERING — verbatim, render exactly:

Then list each text element on its own line: position + exact quoted string. Examples:

- `Top caption band, full width: "By the early 1960s, Honda was no longer chasing the world…"`
- `Bottom caption band, full width: "…The next part of the story would ask whether the same idea could survive its own success."`
- `Speech bubble, tail to the LEFT figure: "It has to be cheap, clean, and easy."`
- `Storefront sign, foreground right: "American Honda Motor Co."`
- `Banner across upper-left zone: "ISLE OF MAN TT 1961"`

**Close every prompt with the restrictions block:**

> All words spelled correctly. Do not duplicate text. Do not invent extra captions. NO modern logos, NO watermarks, NO spurious signage.

These two phrases together eat the great majority of text-rendering failure modes (paraphrased captions, repeated bubbles, invented signage in the background, modern Honda or Toyota logos sneaking into 1948 scenes).

### C.6 Caption box style — the Honda formula

Every caption gets the phrase **"off-white box, dark serif text, readable"** in the prompt. Period variants exist ("ivory parchment with serif ink," "weathered cream paper, hand-set type") — pick one and hold it across the whole volume.

- **Full-width bands** for hero pages: top band sets the moment (50–80 words), bottom band closes it (50–80 words). gpt-image-2 confirmed at 170 words across two bands on Honda page 24, single shot.
- **In-scene caption boxes** for 1–3 panel pages: anchor to a corner explicitly ("upper-left for setup," "lower-right for resolution").
- **Speech bubbles** round, off-white, dark serif text, tail described by visible target ("tail to the bearded scholar at the sundial"), not by name. Under 15 words even on gpt-image-2.
- **Banners and signage** as physical objects in the scene with text quoted verbatim — render reliably (storefront signs, race banners, billboards, primary-source documents). One of the highest-payoff hero-page formats.

### C.7 Multi-character pages — lock the harder face

gpt-image-2 has only one `edit_image` ref slot. Strategy:

1. **Pick the harder face to lock** — typically the secondary character with distinctive features (round wire-rim glasses, neat hair, dark suit; or older Fujisawa with his round face and neat side-part). The protagonist is usually easier to describe in prose and has a signature mark you can lean on (the white hachimaki for older Honda, the wire-rim spectacles for Newton).
2. **Pass that face's ref to `edit_image`.**
3. **Describe the other character richly in the prompt** with explicit age, signature marks, and pose. Honda Vol 1 used this on pages 12, 13, 15, 17, 20, 22, 24 with consistent results across the volume.

If the page genuinely needs both faces locked simultaneously, that's the one case to reach for `gemini-pro-thin`'s `compose_images` — at the cost of switching aesthetic register mid-volume, which is visible.

### C.8 Failure-mode recipes

| Failure | Fix |
|---|---|
| Caption text paraphrased | Move text into the `LETTERING — verbatim, render exactly:` block; quote it; never paraphrase in prompt prose |
| Duplicated bubbles / repeated captions | Add the restrictions block; if persists, simplify scene composition (the model duplicates when it doesn't know where to anchor) |
| Spurious background signage / fake newspapers / modern logos | Restrictions block; explicitly say "NO billboards" or "NO posters in background" if the scene has wall space |
| Children-book aesthetic on a child character | Anti-drift directive + the realistic-child-anatomy clause; regenerate, don't try to repair |
| Age drift on recurring character | Wrong-age ref was passed; recheck `refs/` filename; use the correct age-phase ref |
| Full-width date strip rendered as small box | Known failure across all three models. Mock the band in the HTML reader overlay; don't try harder in the prompt |
| Geometry-critical diagram fumbled | This is the rare opt-in case for `thinking: true` — document the reason, regenerate with the flag |
| Two characters look like the same person | Increase prose contrast (different ages, different distinctive features); or switch the locked face per C.7 |

### C.9 Anti-patterns specific to gpt-image-2

- Don't use the `[1] "STRING…"` "lock list" prompt format — bracket markers render literally on Pro and have shown up on gpt-image-2 too.
- Don't pass `quality: "low"` or `medium` to "save money" on biographical pages. Caption legibility collapses; you'll regenerate at high anyway and end up paying more.
- Don't pass `thinking: true` reflexively. Standard mode hit T5 across 24 Honda pages without thinking.
- Don't request a true full-width date strip and expect it. All three models render date strips as small caption boxes; overlay in HTML reader if you need a real band.
- Don't rely on the model to know the subject. The face it produces from "Honda" alone is not Honda. Always feed an `edit_image` ref.
- Don't paraphrase dialogue or captions when text must render in-image. The exact quoted string is the render target.

---

## Cross-references

- `bio.md` — biographical-mode workflow (the producer of these prompts).
- `~/.claude/skills/graphic-novel/SKILL.md` — canonical skill, both modes.
- `~/.claude/projects/-Users-andresrodriguez-Documents-nano/memory/reference_gemini_pro_thin_mcp.md` — compact memory note for the Gemini wrapper.
- `~/.claude/projects/-Users-andresrodriguez-Documents-nano/memory/reference_openai_image_2_mcp.md` — compact memory note for the OpenAI wrapper.
- `~/.claude/projects/-Users-andresrodriguez-Documents-nano/memory/reference_image_model.md` — model ladder (Pro / Flash / gpt-image-2).
- `~/.claude/projects/-Users-andresrodriguez-Documents-nano/memory/reference_text_density_workflow.md` — May 2 T5 test data.

*Last updated 2026-05-03 after Honda Vol 1 ship. Update both this file and the corresponding memory references whenever an MCP shape, env var, default endpoint, or prompt-template rule changes.*
