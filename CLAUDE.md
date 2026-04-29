# Nano Project - Session Learnings

## Project Overview
This is an AI-generated art portfolio repo. The user creates graphic novels, renders, and creative experiments using Gemini image generation (via MCP) and Claude Code. The GitHub repo is at: https://github.com/sebitasaquiles2018-bot/nano

## Gemini MCP Tools Available
- `generate_image` — Text-to-image generation. Supports a `prompt` and optional `saveToFilePath`.
- `edit_image` — Edit an existing image with a prompt. Accepts image via `path` or `dataBase64`.
- `compose_images` — Combine 2-10 input images with a guiding prompt. Critical for character consistency.
- `style_transfer` — Transfer style from a style image to a base image.

## Graphic Novel Creation Workflow (Proven)

### Step 1: Character Reference Sheets
- Generate character turnaround/reference sheets FIRST before creating story pages.
- Prompt pattern: "Character reference sheet of [character]. Full body front view and side view. [Costume/appearance details]. Bold ink outlines, comic book coloring, clean white background, character turnaround sheet style."
- These references ensure visual consistency across all panels.
- Save refs in the project folder (e.g., `graphic_novel/ref_einstein.png`).

### Step 2: Compose Pages Using References
- Use `compose_images` (NOT `generate_image`) for story pages — pass character reference sheets as input images.
- This keeps characters looking consistent across pages.
- Prompt pattern: "Graphic novel PAGE [N] with 2 panels. Use the character designs from the reference images exactly for consistency. Panel 1: [scene description]. Speech bubble [character]: '[dialogue]'. Panel 2: [scene description]. Speech bubble [character]: '[dialogue]'. Bold graphic novel art style, dramatic lighting, vibrant comic book colors, professional lettering, page number '[N]' at bottom."

### Step 3: Cover Page
- Generate cover AFTER story pages so you know the visual style.
- Use `compose_images` with the same character refs for consistency.
- Include: title, character hero poses, dramatic background, issue number, tagline.

### CRITICAL: Always Create ALL Reference Sheets BEFORE Generating Pages
- **This is the #1 rule.** Before generating ANY story pages, create reference sheets for EVERY character (heroes, villains, side characters).
- Generate refs using `generate_image` (NOT compose), save them in the project folder.
- Then use ALL refs together in `compose_images` for every page to maintain consistency.
- If a new character is introduced mid-story (e.g., a villain), STOP and create their reference sheet first before continuing.
- Each new issue/part should have its own folder (e.g., `graphic_novel_p2/`) with copies of all character refs inside it.

### Key Learnings & Tips
1. **2 panels per page works best.** 6-panel pages are too complex and may fail (API returns no image).
2. **Keep prompts detailed but focused.** Describe each panel clearly with scene, characters, actions, and dialogue.
3. **Speech bubble text works!** Gemini can render readable text in speech bubbles when explicitly described in the prompt.
4. **"Spider-Man" may be blocked** due to copyright. Use alternative names like "Spider-Strike" for the character reference, but the compose tool can still produce Spider-Man-like characters when working from a reference sheet.
5. **Realistic vs comic style:** Add "Photorealistic rendering, cinematic lighting, highly detailed faces" for realism, or "Bold graphic novel art style, vibrant comic book colors, ink outlines" for comic style.
6. **Page numbers:** Include "page number 'N' at bottom" in the prompt and they render correctly.
7. **Image sizes:** Generated images are typically 500KB-1.1MB JPEG files.
8. **Failed generations:** If `generate_image` fails with "No image data returned," simplify the prompt or break into fewer panels.
9. **New characters need refs first.** Don't start generating pages with a new character until their reference sheet exists.

## Folder Structure
```
nano/
├── CLAUDE.md                          # This file - session learnings
├── .gitignore
├── MCP-SETUP-GUIDE.md
├── gaming_pc.png                      # Standalone renders
├── einstein_newton_chat.png
├── einstein_newton_realistic.png
├── graphic_novel/                     # Issue #1: The Multiverse Equation
│   ├── index.html                     # HTML reader (dark theme, keyboard nav, fullscreen)
│   ├── cover.png
│   ├── ref_einstein.png               # Character reference sheet
│   ├── ref_spiderhero.png             # Character reference sheet
│   ├── page1.png
│   ├── page2.png
│   └── page3.png
├── graphic_novel_p2/                  # Issue #2: The Dark Equation
│   ├── index.html                     # HTML reader for Part 2
│   ├── cover.png
│   ├── ref_einstein.png               # Character ref (copied for consistency)
│   ├── ref_spiderhero.png             # Character ref (copied for consistency)
│   ├── ref_drvoid.png                 # New villain reference sheet
│   ├── p2_page1.png - p2_page6.png   # Story pages
│   └── ...
└── images/                            # Other images
```

### Convention: Each new issue gets its own folder
- `graphic_novel/` = Issue #1
- `graphic_novel_p2/` = Issue #2
- Each folder contains its own character refs, pages, cover, and index.html reader.

## Git & GitHub Setup
- GitHub CLI (`gh`) is installed via winget and authenticated as `sebitasaquiles2018-bot`.
- Git identity for this repo: `sebitasaquiles2018-bot` / `sebitasaquiles2018-bot@users.noreply.github.com`
- Remote: `origin` -> `https://github.com/sebitasaquiles2018-bot/nano.git`
- `gh` binary path: `/c/Program Files/GitHub CLI/gh.exe` (needs `export PATH="/c/Program Files/GitHub CLI:$PATH"` in bash).

## HTML Reader
- Located at `graphic_novel/index.html` — a self-contained single-file reader.
- Features: dark theme, thumbnail strip, page navigation (prev/next + dots), keyboard arrows, click-to-fullscreen.
- Pages are defined in a JS array at the top of the script — easy to add new pages.
- To add a new page: just add `{ src: 'pageN.png', label: 'Page N' }` to the `pages` array.

## fal.ai Video Generation (Veo 3.1)

For generating short videos (e.g., a historical figure delivering a quote with native lip sync), use the `video-quote` skill at `~/.claude/skills/video-quote/SKILL.md`.

### Auth
- API key is stored in the **`FAL_KEY`** user env var (set persistently via PowerShell `[System.Environment]::SetEnvironmentVariable('FAL_KEY', '...', 'User')`). **Never commit the key to this repo.**
- Verify with `echo $FAL_KEY` (bash) or `$env:FAL_KEY` (PowerShell). Restart the shell after setting.

### Gold path: image-to-video with native lip sync
1. Generate a photoreal start frame (Nano Banana Pro), 720p+, 16:9 or 9:16, ≤ 8 MB.
2. **Upload to fal storage**: `POST https://rest.alpha.fal.ai/storage/upload/initiate` with `{file_name, content_type}` → returns `{file_url, upload_url}`. PUT the bytes to `upload_url` (no auth header on PUT — signed URL carries auth).
3. **Submit** to `https://queue.fal.run/fal-ai/veo3.1/image-to-video` with `{prompt, image_url, duration:"8s", resolution:"720p", aspect_ratio:"auto", generate_audio:true}`.
4. **Poll** `status_url` every **15s** (don't go shorter — fal returns same status for ~10s windows). ~75s inference.
5. **GET** `response_url` → download `result.video.url` to local mp4.

Auth header on all calls: `Authorization: Key $FAL_KEY`.

### Slug gotcha
Not all model URLs are prefixed with `fal-ai/` — some vendors are namespaced directly (e.g., `bytedance/seedance-2.0/...`). Symptom of wrong slug: status `COMPLETED` instantly + result fetch returns `{"detail":"Path /xxx not found"}`. Fix: WebFetch the model's `/api` page to confirm.

### Payload discipline
`jq` is not always available — use `python3 -c 'import json; print(json.dumps(...))'`. Always echo the payload before submitting; an empty `-d ""` body silently submits with defaults (cost wasted, no error).

### Veo 3.1 prompting (the cardinal rule)
**The start frame locks identity.** Do not re-describe face/clothing/fixed scenery — the prompt is for *motion, dialogue, sound* between t=0 and t=8s. Five-component structure: subject+position → micro-action → quoted line with speech verb → ambient/SFX → style guard. Optimal 150–300 chars. Dialogue ≤ 15 words. See the skill for full details.

## Future Session Notes
- When creating new graphic novels, always start with character reference sheets.
- Use `compose_images` with refs for all story pages.
- The user prefers realistic style with readable speech bubble text.
- Commit and push after new content is created — user likes keeping the repo up to date.
