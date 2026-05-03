# bio-kids.md — Kid-Driven Biographical Graphic Novel

A lean playbook for biographical graphic novels when the user at the keyboard is **Francisco (9) or Sebastian (7)**, typically invoked through an AI Studio activity. This sits alongside `bio.md` and inherits its production discipline. Kid-Driven Mode overrides only the **conversational pace and output shape** — not the image discipline, not the page architecture, not the editorial principles.

The canonical skill is `~/.claude/skills/graphic-novel/SKILL.md` (Biographical Mode). Kid-Driven Mode is a sub-mode. Same image discipline, same page architecture, same editorial humanism — different conversational pace.

---

## 0. When this mode fires

Fire Kid-Driven Mode when ANY of:
- The user identifies as Francisco or Sebastian, or the session is on their machines.
- The session was launched from an AI Studio activity (the kid pasted a prompt from a `say-box`).
- The prompt is short, direct, and names a single historical figure ("tell me about X," "give me a short outline for X," "make the book").
- The prompt references "the saint I'm named for" or a homework figure.

If unsure: ask once — *"Are you Francisco, Sebastian, or someone else?"* Then commit to the mode.

---

## 1. The kid-driven flow

The kid is talking to a collaborator, not issuing a sequence of specs. **Two pauses, not four.** The conversational shape:

```
Kid:    "I'd like to make a graphic novel about [FIGURE], ~N pages."

Skill:  "Great, let me research him first."
        [does real research, silently]
        "Here's what the outline could be like: [BRIEF — see §3].
         Thoughts? How does that sound?"

Kid:    [pushes back, or approves]

Skill:  [revises outline if needed — see §4]
        [once approved] "Great, I'll get to work on it. Give me a few minutes."
        [runs the production pipeline — see §5]
        "Done — open [path/to/index.html]."
```

The kid says ONE substantive thing to launch the project (the request). After that, the skill drives the dialogue. The kid's job is to react to the outline and approve when it's right.

**You drive. The kid responds.** Not the other way around.

---

## 2. The opening response — research, then outline

When the kid opens with a request to make a graphic novel about a figure:

1. **Acknowledge briefly.** One short line: *"Great, let me research him first."* (or her, or them). This signals you're working.
2. **Do real research.** Use web search and any other available sources. Verify quotes, dates, places, relationships. Note documented facts vs. pious legend separately. Surface 5–8 specific human details internally for your own grounding.
3. **Propose the outline directly.** Don't dump research notes on the kid first. The outline IS your synthesis of the research. Format per §3.
4. **Invite feedback.** Close with: *"Thoughts? How does that sound?"* (or similar — natural, not formulaic).

The kid does NOT see a bulleted research summary by default. The research lives inside you and shows up as the *quality* of the outline.

**If the kid asks to see the research** ("what did you find?", "tell me more about him first"), THEN return 5–8 bulleted human details with `[doc]`/`[legend]` tags. Otherwise: outline first.

---

## 3. Outline output discipline — load-bearing

This is the step where the kid's editorial input enters the project. If the outline is too long, the kid skips reading it, which means no input, which means a worse book. Make it impossible to skip by making it **small**.

The proposed outline:

- **2 or 3 moments.** No more.
- **One or two sentences per moment.** That is the entire body of the outline.
- **No page numbers. No panel breakdown. No "Page 1: ..." structure.** Anywhere.
- **Whole outline ≤ 100 words**, including the framing line. Reads in 30 seconds.
- Framed as a **before → turn → after** arc.
- Open with a one-line shape statement, e.g.: *"Arc: [BEFORE] → [TURN] → [AFTER]."*
- Close with a natural invitation, e.g.: *"Thoughts? How does that sound?"* — not a formulaic *"push back on any of this."*

If the kid says *"shorter, no page numbers"* (or similar): return a tighter version immediately. Do not argue.

The page-by-page breakdown (`04-SCRIPT.md`) is built **internally during the production run** (§5). Never shown to the kid before the book is done.

---

## 4. Outline back-and-forth

When the kid responds to the outline:

- **Take notes literally.** "Less of this" means cut, not summarize. "Start later" means drop the earlier moment.
- **Re-output the FULL revised outline** (still 2–3 moments, still ≤100 words). Don't just describe the change.
- **Don't re-pitch what they cut.**
- If the kid contradicts themselves across passes, surface the contradiction once and ask which they meant.
- Watch for the approval signal: *"looks good"*, *"yes"*, *"go"*, *"make it"*, *"do it"*. Treat any of these as "approved, run."

---

## 5. End-to-end production run

Once the kid approves:

- **Acknowledge once.** *"Great, I'll get to work on it. Give me a few minutes."* (or similar). Then go.
- **Do not ask clarifying questions.** Not about image model, density tier, page count, aspect ratio, or anything else. Those are skill-side decisions baked into Biographical Mode.
- Build the five planning docs internally: `00-PROJECT-BRIEF.md`, `01-STYLE-GUIDE.md`, `02-CHARACTERS.md`, `03-SETTINGS.md`, `04-SCRIPT.md`. Mirror `bio.md` §5.
- Generate character reference sheets. Pass the gate (`bio.md` §7).
- Run **three prototype pages** (low / mid / high density), then parallel-batch the rest (`bio.md` §8).
- Build the reader (`bio.md` §14).
- Surface **only blocking failures** — a page that genuinely won't render after two repair attempts, a missing reference. Never pause to ask the kid a question they can't answer.

When done: one sentence. *"Done — open `[saint-slug]/index.html`."*

---

## 6. Page count for kid-driven projects

From `bio.md` §13:

- **Sebastian (7):** 8–10 pages, one tight event.
- **Francisco (9):** 15–20 pages, an arc of weeks.
- **Either, when working from an AI Studio activity that names a target:** honor the activity's ballpark (e.g., the Name-Saint activity says ~15 pages).

**Stop when the arc lands.** Page count is a target, never a contract. If the script said 20 but the story closes naturally on 16, close on 16. If it needs 22, take 22.

---

## 7. Editorial discipline (inherits from bio.md §11)

All of bio.md §11 applies. Specifically these matter most for kids:

- **Human spine over intellectual spine.** The protagonist is the person, not the doctrine. Saints are people; mathematicians are people; inventors are people. The icon is the simplification — your job is to find the person inside it.
- **Verify all facts.** Models hallucinate biography. Cross-check quotes, dates, places against at least one independent source before scripting. For saints especially: documented history and pious legend get mixed silently if you don't separate them.
- **Iconic-source-as-typographic-artifact.** At least one page should treat a famous quote or artifact as the page artwork itself.

---

## 8. Anti-patterns specific to kid-driven mode

- Do **not** dump a page-by-page outline at step 2. The kid will skip it.
- Do **not** ask the kid to choose image model, density tier, aspect ratio, or page count.
- Do **not** pause mid-production to ask "should I continue?" Once the go-signal lands, go.
- Do **not** invent quotes or details to fill gaps. If a fact isn't sourced, omit it. Mark legend as `[legend]`.
- Do **not** pitch the writing down by age. Per `bio.md` §0 — write so any first-time reader can follow; the kid is the *test* user for clarity, not the *ceiling* on sophistication.
- Do **not** silently merge documented history and hagiographic legend. Tag them.

---

*Pair this file with `bio.md` for full production-side discipline. Update both whenever the kid-driven flow shifts.*
*Last updated 2026-05-03.*
