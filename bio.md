# bio.md — Biographical Graphic Novel Playbook

A portable handoff for any Claude instance picking up biographical graphic novel work in this repo. Read this top-to-bottom before scripting or generating. It consolidates everything learned across **Descartes, Einstein, Newton, Honda, and Pythagoras Vol 1** through May 2026.

The canonical authority is `~/.claude/skills/graphic-novel/SKILL.md` (Biographical Mode section). This file mirrors the same content in a single discoverable doc inside the project repo. If the two disagree, the skill wins — but they should not disagree; update both.

Companion memory files (also load if available):
- `~/.claude/projects/-Users-andresrodriguez-Documents-nano/memory/MEMORY.md` — repo state, ship inventory.
- `~/.claude/projects/-Users-andresrodriguez-Documents-nano/memory/project_honda_retrospective.md` — most recent ship (2026-05-02).
- `~/.claude/projects/-Users-andresrodriguez-Documents-nano/memory/reference_text_density_workflow.md` — May 2 T5 test data.
- `~/.claude/projects/-Users-andresrodriguez-Documents-nano/memory/reference_biography_format_evolution.md` — page-template vocabulary, subject ranking.
- `~/.claude/projects/-Users-andresrodriguez-Documents-nano/memory/reference_lyceum_curriculum.md` — kids' active home curriculum (drives subject selection).

---

## 0. Framing rule (do not violate)

Never frame the work as "for ages 7–10" or "for kids" and never pitch the writing down by age. The actual instruction is broader: **do not assume the reader already knows the story.** Write so any reader who has never heard of the subject can follow on first read. No info-withholding. No jigsaw-puzzle reading. T4–T5 density per hero page is the operationalization of this standard. If you find yourself shortening captions to fit a prompt limit, push composition out, not text.

Francisco (9) and Sebastian (7) are the *test* users for clarity, not the *ceiling* on sophistication.

---

## 1. Subject selection — apply BEFORE anything else

Most production failures trace back to the wrong subject, not bad pages. Use this 5-question rubric in order:

1. **One human-scale story at the center.** If the book takes more than one sentence to describe, the subject is too technical. Examples that pass:
   - Descartes — *a sickly boy who was allowed to stay in bed became the man whose answer to grief was* I think therefore I am, *and a queen ended his life by forcing him out of bed at 5am.*
   - Honda — *a village boy chases one rattling automobile in 1914 and never stops.*
   - Einstein failed this test: five technical ideas buried the human spine. Sebastian (7) felt the difference.
2. **Curricular connection.** Check `~/Documents/lyceum/` for the kids' active home curriculum before committing. The single deepest reason Sebastian preferred Descartes over Einstein was that he was studying the Cartesian plane in the Lyceum at the same time — the biography became the origin story of math he was already doing. A subject with no curricular hook still works as standalone reading but won't land the same way.
3. **Can the kid DO it?** Subjects whose central idea can be re-enacted with paper and pencil (Pythagoras' triangles, Eratosthenes' shadows, Galileo dropping objects, Archimedes' bathtub, Mendel's peas) outperform subjects where the discovery can only be observed (Einstein's relativity, most modern physics). **Agency beats spectacle.**
4. **Ages well for both 7 and 9.** If the subject is genuinely too technical for Sebastian, accept it and pitch the volume at Francisco — do not paper it over with simpler captions. Honda worked at both ages because the human story (failure → partnership → global proof) is legible to a 7-year-old without needing to follow piston-ring tolerance.
5. **Iconic primary sources or quotes.** Subjects with rendered-as-artifact moments (a manuscript page, a famous quote in period typography, a recorded letter) get a free hero-page beat. See the **primary-source page** template (§9).

Top unstarted candidate per all five criteria: **Eratosthenes**. Pythagoras Vol 2 is in production. Full ranking lives in `reference_biography_format_evolution.md`.

---

## 2. Research before committing

**Do not rely on model knowledge.** The model knows the broad outline of any famous figure's life and will confidently generate plausible-sounding wrong details — wrong dates, wrong relationships, invented quotes, wrong place names.

For each volume:

1. Read at least two independent sources before writing the script. Wikipedia + one biography-specific source is the floor; primary sources are better.
2. Build a research archive in `<figure-slug>-research/`, or treat an existing folder (Honda's `honda/`) as untouched ground truth. Cross-check every date, place, and quote against it.
3. **Verify quotes verbatim.** The model paraphrases famous quotes silently. *Cogito ergo sum* is right; "I think therefore I exist" is wrong. *E pur si muove* is right; English paraphrases are wrong. Render quotes in their original language where appropriate.
4. **Verify the order of events.** Models compress and reorder in plausible-but-wrong ways. The Descartes coordinate-plane-after-Francine reorder was a deliberate editorial choice — an accidental reorder of Honda's Tokyo apprenticeship and Hamamatsu shop would be a factual error.
5. **Note any deliberate departures from chronology in `00-PROJECT-BRIEF.md`** so the choice is intentional and traceable.

If the user has done research already (Codex's `honda/` archive predated Claude's involvement), treat it as authoritative source material — read it in full before scripting.

---

## 3. Page orientation — landscape, not vertical

**Biographical mode is 3:2 landscape (1536×1024).** Standard fictional mode stays 2:3 vertical. The orientation choice is editorial, not just visual:

- **Cinematic register.** Landscape matches oil-painting realism. Vertical biases toward comic-panel-stacks and fights the painted-still-life look that Newton and Honda established.
- **Long captions live on the page.** Full-width caption bands across top and bottom hold 50–80 words each without crowding the image. Vertical can't host the same prose without going dense or tiny.
- **Side-by-side dual scenes.** Two locations, two characters, before-and-after pairs sit cleanly across landscape (Honda page 13: Honda's workshop left, Fujisawa's office right, separated by a clean vertical edge).
- **Multi-zone montage finale.** The four-zone closing-as-invention page (Honda page 24) only works in landscape. Vertical can't host four readable scenes plus a center foreground.
- **Annotated breakthroughs.** A central object with 4–6 callout captions arrayed around it (Honda page 19 Super Cub annotation) needs lateral room.
- **Reader ergonomics.** On a desktop monitor at `max-width: min(1400px, 96vw)`, the page reads at near-original size with the eye traveling left-to-right along caption bands naturally.

Don't mix orientations within a volume.

---

## 4. Project layout

`~/Documents/nano/<figure-slug>/`:

```
<figure-slug>/
├── 00-PROJECT-BRIEF.md
├── 01-STYLE-GUIDE.md
├── 02-CHARACTERS.md
├── 03-SETTINGS.md
├── 04-SCRIPT.md
├── refs/         # ref_<name>.png — character + object reference sheets
├── pages/        # page-NN.png — story pages
└── index.html    # built last, dark-theme reader
```

`<figure-slug>` is lowercase-hyphenated and scoped to the chosen window: `da-vinci-anatomy`, `eratosthenes-vol1`, `honda-soichiro`. Build all five planning docs before generating any image.

---

## 5. The 5 planning docs

### `00-PROJECT-BRIEF.md`
Title, subtitle, image model, page count, the one-sentence window ("This bio covers FIGURE from EVENT to EVENT."), production notes, key reminders, deliberate chronology departures. Mirror `descartes/00-PROJECT-BRIEF.md` or `honda-soichiro/00-PROJECT-BRIEF.md`.

### `01-STYLE-GUIDE.md`
The **Style Block** that gets pasted verbatim into every page prompt, plus visual rules.

**Anti-drift directive — copy verbatim into every prompt:**
> NOT a children's book. Serious mature graphic novel, realistic proportions, natural lighting, cinematic composition.

**Register block (biographical mode) — copy verbatim into every prompt:**
> Oil-painting realism. NOT a comic. NO halftones, NO cel shading, NO ink linework. Painted brushwork, cinematic lighting, muted period palette.

These lines are non-negotiable. Without them the model drifts toward children's-book aesthetics (oversized eyes, pastel palette, rounded features) or ink-comic register (flat halftones, hard outlines).

### `02-CHARACTERS.md`
One **character lock block** per character: age, skin tone, hair (color, length, style), face shape, eye color, signature marks (scars, jewelry, tools), clothing (colors and materials), build/posture. Plus a **reference-sheet generation prompt** per character: 1536×1024 landscape, neutral expression, plain warm-toned background, "no text, no labels."

If a character ages across the window, write **separate locks per age**. Honda required 6 refs across 8 → 17 → 22-30 → 39-42 → 42-55 plus Fujisawa. Use the correct age-specific reference for each page; never feed a wrong-age ref into `edit_image` — silent age drift will result.

### `03-SETTINGS.md`
Recurring locations: workshop, ship's deck, factory floor, Cambridge quad. Each location: era, lighting, materials, what's on the walls/floor, weather. These exist so location prompts stay consistent across pages.

### `04-SCRIPT.md`
Page-by-page:
- Panel breakdown (or single-image composition for biographical pages — the default).
- Camera language (wide, medium, close-up, low-angle).
- **Verbatim** dialogue and caption text. Quotation marks preserved. Do not paraphrase later.
- Visual prompt seed, including which character locks and reference sheets to attach.
- **Density tier (T1–T5)** and recommended model.

---

## 6. Image model calibration (May 2026)

| Model | MCP | Use for |
|-------|-----|---------|
| **gpt-image-2 standard** | `mcp__openai-image-2__{generate_image,edit_image}` | **Default for biographical novels.** Oil-painting realism, hits T5 single-shot, ~$0.21/img. No `compose_images`. |
| Gemini 3 Pro Image Preview | `mcp__gemini-pro-thin__{generate_image,edit_image,compose_images}` | T4–T5 with multi-character pages where you genuinely need `compose_images`. Digital-painting / concept-art register — incompatible with the Newton/Honda oil-painting register. ~$0.13/img. |
| Gemini 3.1 Flash (NB2) | same MCP, switch endpoint env var | Low text density (T1–T3) cost-saver. Borderline at T4. |
| gpt-image-2 thinking | `thinking=true` flag | Geometry-critical diagrams only. $0.50–$1+/img. Opt-in. |

**Rule: flag model swaps explicitly, distinct from style swaps.** When the user asks for a different look ("more like Newton"), recognize whether that requires changing the underlying model (yes — Newton was on gpt-image-2) and call out the swap, the cost, and the behavioral difference. **Do not silently change models.** The user has pushed back hard on this; treat it as a different class of decision.

The custom `gemini-pro-thin` MCP (`~/.claude/mcp-servers/gemini-pro-thin/`) removes the upstream 2000-char prompt cap. See `reference_gemini_pro_thin_mcp.md`.

---

## 7. Reference sheets — the gate

Before any page is generated, every named character has a reference sheet in `refs/`. Generate one at a time, review against the lock block, regenerate until correct, then attach that image to every page prompt for that character.

**Casting checks before passing the gate:**
- Age right? (a 60-year-old should look 60, not 30 with grey hair)
- Era right? (period-accurate clothing, not Halloween costumes)
- Realistic, not cartoon? (no oversized eyes, no soft pastels)
- Distinctive? (could you pick this person out of a lineup?)
- Register matches the cover/pilot? (no comic linework if the project is oil-painting realism)

**Do not start page generation until the gate is passed.** A drifted ref poisons every page generated from it.

---

## 8. Page generation flow

- **Aspect ratio:** 3:2 landscape (1536×1024).
- **Three prototype pages first.** Pick low / mid / high density script pages and generate them sequentially with full review before the bulk run. This validates the prompt template, register, and model choice across the density range. Honda did pages 1, 7, 12 as prototypes.
- **After prototype validation: parallel batching is allowed.** Honda generated cover + 21 remaining pages in a single parallel call after the three prototypes were approved. This works **only because every prompt is templated against the script.** Do not batch before validation.
- **Every prompt includes:** the Style Block (verbatim), the register block, the character lock block(s) (verbatim), the relevant reference image(s) attached, the panel/composition description, the verbatim dialogue/caption text from the script.
- After each page, run the three-question check: **same person? right text? right mood?**
- If a page drifts, repair it before continuing in sequential mode; in batched mode, regen the affected pages individually.
- Prefer targeted local edits over full rerolls once a page is mostly right.

---

## 9. Text rendering — narration treatment and density tiers

Honda Vol 1 established the treatment for in-image narration. Use it as the default.

### Narration treatment — the Honda formula

Biographical pages carry their narration **inside the image** as caption boxes, not in the reader-app HTML below the image. This keeps pages cinematic instead of infographic.

- **Caption box style.** "Off-white box, dark serif text, readable." Repeat verbatim per caption in the prompt. Period variants: "ivory parchment with serif ink," "weathered cream paper, hand-set type." Pick one register and hold it across the volume.
- **Full-width bands for hero pages.** T4–T5 pages can carry a top caption band and a bottom caption band running the full landscape width. Top establishes the moment; bottom closes it. 50–80 words each is shippable on gpt-image-2.
- **In-scene caption boxes.** For 1–3 panel pages, captions sit as small off-white boxes anchored to a corner — upper-left for setup, lower-right for resolution. State the corner explicitly.
- **Speech bubbles.** Round, off-white, dark serif text, tail explicitly described ("tail pointing to the LEFT figure"). Keep under 15 words; longer dialogue belongs in a caption.
- **Banners and signage.** Inline small banners ("ISLE OF MAN TT 1961"), storefront signs ("American Honda Motor Co."), billboards ("You meet the nicest people on a Honda") render reliably on gpt-image-2 when described as physical objects in the scene with their text quoted verbatim.
- **Verbatim block in the prompt.** Open the lettering section with the phrase **"LETTERING — verbatim, render exactly:"** then list each text element with its position and the exact quoted string. This phrasing is the most reliable trigger for accurate text rendering.
- **Restrictions block.** Close the prompt with: **"All words spelled correctly. Do not duplicate text. Do not invent extra captions. NO modern logos, NO watermarks, NO spurious signage."** Eats most remaining text-failure modes.
- **Scripted verbatim.** The script in `04-SCRIPT.md` holds the verbatim caption text. The prompt copies it word-for-word. Never paraphrase at generation time.

### Density tiers

| Tier | Words / page | Elements | Model |
|------|--------------|----------|-------|
| T1 | < 30 | 1–2 captions or bubbles | Flash OK |
| T2 | 30–70 | 2–3 elements | Flash OK |
| T3 | 70–100 | 3–4 elements | Flash borderline; Pro/gpt-image-2 safer |
| T4 | 100–140 | 4–6 elements | Pro / gpt-image-2 mandatory |
| T5 | 140–180 | 6+ elements | Pro / gpt-image-2 mandatory; both confirmed single-shot |
| T6+ | 180+ | 7+ elements | Untested ceiling. Redesign or split before generating. |

### Text-rendering capability comparison

**gpt-image-2 standard**
- ✅ T5 single-shot in production. Honda page 7 (3 captions ~137 words + 3 bubbles, 6 elements) and page 24 (2 long bands ~170 words + small banner) both rendered verbatim on first try.
- ✅ Long prose captions in off-white boxes — the Honda formula's home turf.
- ✅ In-scene signage and banners when described as physical objects.
- ✅ Primary-source pages — formal letter typography with letterhead, salutation, body, signature blocks rendered cleanly (Honda page 14).
- ✅ Speech-bubble attribution holds when speaker is described as the visible actor.
- ❌ No `compose_images`. Multi-character pages need the lock-the-harder-face strategy (§10).
- ❌ Full-width date strips render as small caption boxes. Overlay in HTML.
- ❌ Geometry-heavy diagram labels untested at scale; reach for `thinking=true` only when really needed.

**Gemini 3 Pro Image Preview**
- ✅ T5 single-shot per the May 2 test. 6/6 verbatim on a 6-element / 118-word page.
- ✅ `compose_images` for genuine multi-character pages (2–10 refs).
- ✅ No prompt char cap on `gemini-pro-thin`.
- ❌ Aesthetic register is digital-painting / concept-art. Incompatible with the oil-painting realism Newton/Honda established. Switching mid-volume produces visible style mixing.
- ❌ "Lock list" prompt format (`[1] "ALEXANDRIA…"`) — bracket markers render literally.
- ❌ Full-width date strips fail the same way.

**Gemini 3.1 Flash / NB2**
- ✅ T1–T3 reliable. Cheaper, faster.
- ⚠️ T4 borderline. May 2 test got 5/6 verbatim with one duplication.
- ❌ T5 unreliable. Don't use for hero pages.

**Verdict for biographical mode:** gpt-image-2 standard is the default — hits T5 single-shot, matches the oil-painting register, handles caption-box prose and primary-source pages cleanly. Reach for Pro only when a page genuinely needs `compose_images` and the lock-the-harder-face strategy won't carry it.

### Anti-patterns specific to text rendering

- **Do NOT use the "lock list" prompt format** like `[1] "ALEXANDRIA…"` — Pro renders bracket markers literally.
- **Do NOT request a full-width date strip and expect it.** All three models render it as a small caption box. Mock it in the HTML reader overlay if you need a true band.
- **Do NOT paraphrase dialogue or captions** when text must render in-image. The exact quoted string is the render target.
- **Do NOT skip the verbatim/restrictions blocks.** "LETTERING — verbatim, render exactly:" up top and the no-spurious-text clause at the bottom are load-bearing.
- **Do NOT push past T5.** If a page needs T6, redesign or split.

---

## 10. Multi-character pages

- **gemini-pro-thin** has `compose_images` (2–10 refs). Use it when you genuinely need multiple distinct faces locked simultaneously.
- **gpt-image-2** has only `edit_image` (one ref). Strategy: **lock to the harder face** (typically the secondary character with distinctive features — round wire-rim glasses, neat hair, dark suit), and describe the protagonist richly in the prompt with explicit age and signature marks (e.g., the white hachimaki for older Honda). Honda Vol 1 used this across pages 12, 13, 15, 17, 20, 22, 24 with consistent results.

---

## 11. Editorial discipline

Production discipline keeps pages on-model. **Editorial discipline keeps the book worth reading.** Drawn from Descartes, Einstein, Newton, Honda.

### Human spine over intellectual spine
The protagonist is the person, not the idea. Descartes Vol 1 is *the boy who was allowed to stay in bed and the man who died because a queen forced him out of bed*; the cogito and coordinate plane are beats inside that arc. Honda Vol 1 is *the boy who chased an automobile in 1914 and the man whose machines moved everyone fifty years later*; the piston-ring failure and Super Cub are beats. Einstein drifted into intellectual-spine mode — the 7-year-old lost the thread.

If the subject demands intellectual scaffolding, concentrate it in one block of pages rather than threading physics through every page.

### Emotional reordering over strict chronology
Order pages by the arc the reader needs, not by the calendar. Descartes Vol 1 reordered pages 13–18 so the cogito lands as a father's answer to grief (after Francine's death), not as detached philosophy. Chronology preserved at the level of life-events; *narrative* sequenced for emotional payoff. **Document any deliberate reorder in `00-PROJECT-BRIEF.md`.**

### Pacing — expand if too terse
If the script feels jammed, **add pages.** Descartes went 16 → 20; Honda went planned-34 → 24. Page count is a target, never a contract. The user's standing complaint is *no terse crap; the reader should not be filling in blanks* — operationalize as T4–T5 density per hero page; split a page rather than shorten its captions.

### Closing-image-as-invention
The final page should make the subject's life-work into the visual structure of the page itself.
- Descartes Vol 1's last page = a coordinate plane with life vignettes plotted at grid points.
- Honda Vol 1's last page = a four-zone montage of the world the Super Cub built, with Honda and Fujisawa standing small in the center.

The pattern: take the central object/idea of the volume and let it *be* the page, with the protagonist's life sitting inside it. **Highest-leverage page in the book; design it before designing the middle.**

### Quiz tests WHY, not WHAT
The 5-question quiz is not trivia. Each question tests *why* something happened, not *what* happened. "Why did Honda's first piston rings fail Toyota's quality test?" is right; "What year did Honda found Honda Motor?" is not. Right-answer feedback should reinforce the *why* with one or two sentences of substance.

### Iconic-source-as-typographic-artifact
At least one hero page per biography should treat a famous quote, manuscript page, or document as the visual artwork — period typography on chalkboard, parchment, or book title page — rather than as dialogue or caption text. Highest-payoff beat in the new format vocabulary.

### Hero pages first
After refs lock, generate **(a)** the breakthrough page, **(b)** the closing-as-invention page, and **(c)** one primary-source page **before** committing to the bulk run. If those three land, the volume will land. If they don't, you've learned what the prompt template needs to fix before spending the bulk-run budget.

---

## 12. Page-template vocabulary

Reach for these when scripting:

- **Cinematic single-image page** — one composed scene, one or two captions, no panel grid. Default biographical page format.
- **Failure-and-study page** — protagonist with the failed object, captions narrating the lesson; T4–T5.
- **Partnership page** — two locked characters, alternating bubbles, caption framing the agreement; T4–T5.
- **Primary-source page** — render an actual letter, document, page from a book, advertisement copy as the visual subject. Treat the text as the artwork. Honda page 14 reference.
- **Annotated-breakthrough page** — central object (machine, equation, diagram) with 4–6 callout captions explaining the parts; T5. Honda page 19 reference.
- **Montage finale** — four-zone landscape painting unifying the volume's outcomes, with the protagonist(s) small but present in center foreground. Honda page 24 reference. Heaviest density; gpt-image-2 single-shot can hit it.
- **Quote chapter-break** — a single iconic quote rendered as the page artwork, no scene. Use sparingly.

---

## 13. Stop when the arc lands

Page count is a target, not a contract. If the script said 20 pages but the story closes naturally on 14, close on 14. If it needs 18 to land, take 18. **The arc landing is what matters.**

For kid-driven projects:
- Sebastian (7): aim for 8–10 pages, one tight event.
- Francisco (9): aim for 15–20 pages, an arc of weeks.
- Both: stop when the arc lands.

---

## 14. Final assembly — the reader

When all pages pass the three-question check, build `<figure-slug>/index.html`. Mirror `~/Documents/nano/honda-soichiro/index.html` (most current) or `pythagoras-vol1/index.html`.

Required reader features:
- Dark theme: `#15171c` background, Palatino serif, off-white text.
- Cover page first → sequential pages → end-of-volume interstitial → quiz.
- **Page width:** `max-width: min(1400px, 96vw)` so embedded caption text reads at near-original size.
- **Navigation:** circular ←/→ arrow buttons fixed to the left/right edges of the viewport, vertically centered (`top: 50%; transform: translateY(-50%)`). Semi-transparent with backdrop blur. Page-info label sits as a small fixed strip at bottom center. Below-image button rows are deprecated for biographical mode.
- Click left third of image → previous; click right two-thirds → next.
- Keyboard: ←/→ arrows, spacebar = next.
- Mobile: 44px arrows hugged to edges; touch swipe.
- Progress bar at top.
- Lazy-prefetch the next page on load.
- 5-question quiz at end with verbatim correct/incorrect feedback per question, score display after all five.

Update `~/Documents/nano/index.html` to add a card for the new project (cover thumbnail, title, description, three tag chips). Append the folder name to the footer's folder list.

---

## 15. Cost envelope

Plan ~$7.50 per 24-page biography on gpt-image-2 standard:
- 10 refs × $0.21 ≈ $2.10
- 24 pages × $0.21 ≈ $5.04
- 3 prototype regens × $0.21 ≈ $0.63

Newton ($7.35) and Honda ($7.50) both landed inside this envelope.

---

## 16. Memory, retrospective, and ship updates

When the volume ships:

1. Update `~/.claude/projects/-Users-andresrodriguez-Documents-nano/memory/MEMORY.md` — move the project from "ACTIVE WORK" to "RECENT SHIP" / inventory; bump the landing-page count.
2. Write a short retrospective at `~/.claude/projects/-Users-andresrodriguez-Documents-nano/memory/project_<slug>_retrospective.md` — what worked, failure modes, fixes, surprises, what to repeat.
3. Update the project's `HANDOFF.md` (if one exists) with a "✅ SHIPPED <date>" block at the top, preserving the historical pre-ship handoff beneath.
4. **Commit and push only when the user asks.** Stage only project files and the landing-page diff — leave unrelated untracked work alone.

---

## 17. Anti-patterns — do not do these

**Editorial:**
- Do **not** commit to a subject before applying the 5-question rubric. The wrong subject can't be saved by good production.
- Do **not** rely on model knowledge for facts. Verify every date, place, relationship, and quote against research sources. The model paraphrases famous quotes silently and confidently.
- Do **not** let the intellectual spine eat the human spine. The biography is about the person; ideas are beats inside the arc.
- Do **not** order pages by strict chronology when emotional reordering serves the arc. Document the reorder in the brief.
- Do **not** chase a target page count past the arc's natural close — or under it. Expand if jammed; stop if landed.
- Do **not** write trivia quizzes. Quiz questions test *why*, not *what*.

**Production:**
- Do **not** generate pages before reference sheets are locked.
- Do **not** paraphrase dialogue at generation time. Pull it verbatim from `04-SCRIPT.md`.
- Do **not** skip the Style Block, anti-drift line, or register block in any prompt.
- Do **not** batch pages before three prototypes have validated the template, register, and model.
- Do **not** keep moving forward when a page drifted — repair first.
- Do **not** use `edit_image` against a non-existent or wrong-age reference — the call will silently substitute and you will get age drift.
- Do **not** silently change image models. A model swap is a different class of decision than a style swap; flag it explicitly with cost and behavioral implications.
- Do **not** use the "lock list" prompt format (numbered strings up front) — bracket markers render literally into the page.

---

## 18. Shipped biographies (reference inventory as of 2026-05-03)

| Folder | Subject | Pages | Model | Cost | Notes |
|--------|---------|-------|-------|------|-------|
| `descartes/` | René Descartes | 20 | Gemini Pro / NB2 | — | Established human-spine pacing. Cogito-after-Francine reorder. |
| `einstein/` | Albert Einstein | 21 | mixed | — | Drifted to intellectual spine; Sebastian preferred Descartes. Lesson source. |
| `newton-vol1/` | Isaac Newton | 24 | gpt-image-2 standard | ~$7.35 | First fully-unified gpt-image-2 run. Oil-painting realism baseline. |
| `pythagoras-vol1/` | Pythagoras | 18 | NB2 | — | Curricular hook (kids' triangle lesson). |
| `honda-soichiro/` | Soichiro Honda | 25 | gpt-image-2 standard | ~$7.50 | T5 single-shot confirmed at scale. Narration formula, side-arrow reader, parallel batching after prototypes. |

---

*Last updated 2026-05-03 after Honda Vol 1 ship. Update this file alongside `~/.claude/skills/graphic-novel/SKILL.md` whenever a new biography ships.*
