# Setting Up gemini-nanobanana-mcp for Claude Code

Guide for configuring the [gemini-nanobanana-mcp](https://github.com/Junhan2/gemini-nanobanana-mcp) MCP server — a wrapper around Google Gemini image generation that exposes four tools: `generate_image`, `edit_image`, `compose_images`, and `style_transfer`.

---

## Prerequisites

- **Node.js >= 18** — check with `node --version`
- **Gemini API key** — get one free at https://aistudio.google.com/apikey

---

## Step 1: Get a Gemini API Key

1. Go to https://aistudio.google.com/apikey
2. Sign in with your Google account
3. Click **Create API key**
4. Copy the key (starts with `AIzaSy...`)

---

## Step 2: Choose Your Config File

There are **two separate config files** depending on where you're running MCP:

| Context | Config File |
|---|---|
| **Claude Desktop** (GUI app) | See platform paths below |
| **Claude Code** (CLI) | `.mcp.json` in your project root |

### Claude Desktop config paths

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json` (typically `C:\Users\<you>\AppData\Roaming\Claude\claude_desktop_config.json`)

### Claude Code config path

- `.mcp.json` in your project working directory (e.g., `~/my-project/.mcp.json`)

---

## Step 3: Configure the MCP Server

### Option A: Claude Desktop (npx — simplest)

Add the `mcpServers` block to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "gemini-nanobanana-mcp": {
      "command": "npx",
      "args": ["gemini-nanobanana-mcp@latest"],
      "env": {
        "GEMINI_API_KEY": "YOUR_API_KEY_HERE",
        "GEMINI_IMAGE_ENDPOINT": "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent"
      }
    }
  }
}
```

### Option B: Claude Code CLI (.mcp.json)

Create `.mcp.json` in your project root:

```json
{
  "mcpServers": {
    "gemini-nanobanana-mcp": {
      "command": "npx",
      "args": ["gemini-nanobanana-mcp@latest"],
      "env": {
        "GEMINI_API_KEY": "YOUR_API_KEY_HERE",
        "GEMINI_IMAGE_ENDPOINT": "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent",
        "DEFAULT_SAVE_DIR": "/absolute/path/to/your/image/output/folder",
        "AUTO_SAVE": "true"
      }
    }
  }
}
```

---

## Step 4: Choose Your Model (Important!)

The npm package hardcodes a default model that may be outdated. Use the `GEMINI_IMAGE_ENDPOINT` env var to override it. Available models as of March 2026:

| Model | Endpoint Model ID | Best For |
|---|---|---|
| **Gemini 2.5 Flash Image** (GA) | `gemini-2.5-flash-image` | Fast generation, good quality |
| **Gemini 3 Pro Image Preview** | `gemini-3-pro-image-preview` | Best text rendering, highest fidelity, graphic novels |
| ~~Gemini 2.5 Flash Image Preview~~ | ~~`gemini-2.5-flash-image-preview`~~ | **SHUT DOWN Jan 2026 — do not use** |

### Recommendation

- For **graphic novel / comic production**: use `gemini-3-pro-image-preview` — significantly better text in speech bubbles, character consistency, and panel layouts.
- For **quick image generation**: use `gemini-2.5-flash-image` — faster and cheaper.

Set the endpoint in your config:

```json
"GEMINI_IMAGE_ENDPOINT": "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent"
```

Or for the faster model:

```json
"GEMINI_IMAGE_ENDPOINT": "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent"
```

> **Note**: If the package updates and fixes its default model, you can remove `GEMINI_IMAGE_ENDPOINT` and it will use whatever the package defaults to. But as of March 2026, the override is necessary.

---

## Step 5: Verify Setup

1. **Restart Claude Desktop** (fully quit and reopen, not just close the window)
   — or for Claude Code CLI, restart your `claude` session.
2. You should see **4 tools** available:
   - `generate_image` — text-to-image
   - `edit_image` — modify an existing image with a prompt
   - `compose_images` — combine multiple input images with a prompt
   - `style_transfer` — apply style from one image to another
3. Test with a simple generation prompt to confirm the connection works.

---

## Environment Variables Reference

| Variable | Required | Description |
|---|---|---|
| `GEMINI_API_KEY` | Yes | Your Google AI Studio API key |
| `GEMINI_IMAGE_ENDPOINT` | Recommended | Full endpoint URL to override the hardcoded model |
| `DEFAULT_SAVE_DIR` | No | Absolute path where generated images are saved (default: `~/Downloads/gemini-images`) |
| `AUTO_SAVE` | No | `"true"` or `"false"` — auto-save generated images (default: `"true"`) |
| `LOG_LEVEL` | No | Logging verbosity |
| `MCP_NAME` | No | Override the server name |

---

## Windows-Specific Notes

### validateFilePath Patch (Windows only)

On Windows, the MCP server's `process.cwd()` defaults to `C:\Windows\System32`, which causes the `validateFilePath` function to reject ALL absolute paths — both for saving images and uploading reference images.

**To fix**, locate the cached package:

```
C:\Users\<you>\AppData\Local\npm-cache\_npx\<hash>\node_modules\gemini-nanobanana-mcp\build\index.js
```

Find the `validateFilePath` function and change it from:

```javascript
function validateFilePath(path) {
    const normalizedPath = resolve(path);
    const basePath = resolve('.');
    return normalizedPath.startsWith(basePath) && !path.includes('..') && !path.includes('~');
}
```

To:

```javascript
function validateFilePath(path) {
    return !path.includes('..');
}
```

### Preventing npx from overwriting the patch

Using `npx gemini-nanobanana-mcp@latest` can re-download and overwrite your patch. To prevent this, point directly at the patched file in your config:

```json
{
  "mcpServers": {
    "gemini-nanobanana-mcp": {
      "command": "node",
      "args": ["C:\\Users\\<you>\\AppData\\Local\\npm-cache\\_npx\\<hash>\\node_modules\\gemini-nanobanana-mcp\\build\\index.js"],
      "env": {
        "GEMINI_API_KEY": "YOUR_API_KEY_HERE",
        "GEMINI_IMAGE_ENDPOINT": "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent",
        "DEFAULT_SAVE_DIR": "C:\\Users\\<you>\\path\\to\\output",
        "AUTO_SAVE": "true"
      }
    }
  }
}
```

### Path format

Always use **full absolute Windows paths** with double backslashes in JSON:

```
"C:\\Users\\paqui\\OneDrive\\Documents\\my-project\\images"
```

---

## Tool Usage Quick Reference

### generate_image
Best for images with no reference input (standalone scenes, backgrounds, character reference sheets).

### compose_images
Best for pages where you need **character consistency** — upload character reference sheet images and the model will match them. Requires **minimum 2 input images**.

### edit_image
Best for fixing a specific element in an already-generated image.

### style_transfer
Best for applying a consistent art style from one image to another.

### Prompt limit
All four tools enforce a **2000-character hard limit** on the prompt field. Keep prompts concise.

---

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| 404 error mentioning `gemini-2.5-flash-image-preview` | Deprecated model | Add `GEMINI_IMAGE_ENDPOINT` env var pointing to `gemini-2.5-flash-image` or `gemini-3-pro-image-preview` |
| File path rejected on Windows | `validateFilePath` blocks absolute paths | Apply the patch described above |
| Images not saving | `DEFAULT_SAVE_DIR` path doesn't exist or isn't writable | Create the directory first, use absolute paths |
| `compose_images` timeout | Too many large reference images + complex prompt | Retry once, simplify prompt, reduce to 2 refs |
| Garbled text in speech bubbles | Model limitation | Keep dialogue under 10-12 words per bubble. For silent panels, explicitly say "NO text" |
| Tools don't appear after restart | Config file syntax error or wrong file | Validate JSON, make sure you're editing the right config file for your context |

---

## Lessons Learned (from actual setup on Windows, March 2026)

These are hard-won tips from getting this running end-to-end. Read these before you start — they'll save you multiple restart cycles.

### 1. The default model is broken out of the box

The npm package (as of March 2026) hardcodes `gemini-2.5-flash-image-preview` as the default model. Google shut this model down in January 2026. You **will** get a 404 error on every generation attempt if you don't override it. The `GEMINI_IMAGE_ENDPOINT` env var is not optional — it's required for the package to work at all right now.

### 2. The env var override works — but only from the config file

We initially tried patching the cached `index.js` file directly (changing the hardcoded model ID in the source code). This didn't stick because `npx gemini-nanobanana-mcp@latest` re-downloads a fresh copy on every launch, overwriting the patch. The reliable fix is the `GEMINI_IMAGE_ENDPOINT` env var in your config JSON. That said, on our first attempt, the env var didn't seem to take effect until we got the full endpoint URL exactly right — make sure it's the complete URL including `:generateContent` at the end.

### 3. The model you choose matters a lot for graphic novels

We tested both available models side by side on the same comic book prompt (two characters, multiple panels, speech bubbles):

- **`gemini-2.5-flash-image`** (GA): Produced a workable comic page but the last panel had garbled text and visual artifacts. Speech bubbles were mostly legible but inconsistent. Fine for quick one-off images.

- **`gemini-3-pro-image-preview`**: Dramatically better. Text in speech bubbles was crisp and perfectly legible across all panels. Character consistency was noticeably stronger. Panel composition was more sophisticated. The model even added creative touches (title banners, extra dialogue that fit the scene). This is the one to use for any multi-panel narrative work.

### 4. "Fully quit" means fully quit

On both Windows and macOS, closing the Claude Desktop window doesn't necessarily kill the process. The MCP server config is read at launch time. After every config change, you need to fully quit (check the system tray on Windows, check the dock menu on macOS) and relaunch. We burned several cycles thinking a config change hadn't worked when it just hadn't been picked up yet.

### 5. Claude Desktop and Claude Code are completely separate

The `claude_desktop_config.json` and `.mcp.json` are independent configs for independent apps. An MCP server configured in one will NOT appear in the other. If you need the tools in both Claude Desktop and Claude Code CLI, configure the server in both files. The env vars and server settings can differ between them (e.g., different `DEFAULT_SAVE_DIR` paths).

### 6. Windows path hell is real

On Windows:
- Git Bash `~` resolves to `C:\Users\<you>\` — NOT `C:\Users\<you>\OneDrive\Documents\...`
- JSON config files need double backslashes: `C:\\Users\\paqui\\...`
- The `DEFAULT_SAVE_DIR` must be an absolute path that already exists
- The `cwd` field in MCP config does NOT reliably set the server's working directory on Windows — don't depend on it
- If you use OneDrive, be extra careful with paths — OneDrive folder redirection means `Documents` might be under `OneDrive\Documents`, not directly under your user profile

### 7. Test with text-heavy prompts, not just simple images

Our first successful generation (a cat at a restaurant) looked great but didn't stress-test what we actually needed. It wasn't until we tried a multi-panel comic with speech bubbles that we discovered `gemini-2.5-flash-image` wasn't up to the task. If you're setting this up for graphic novel work, test with a 3-4 panel comic page with dialogue in every panel. That's the real quality bar.

### 8. The 2000-character prompt limit is enforced server-side

This isn't a soft suggestion — the MCP server will reject prompts over 2000 characters. For graphic novel pages with multiple panels and dialogue, you need to write lean prompts. Cut atmospheric adjectives first, reduce panel count second, shorten dialogue third. Never cut character actions or the style block.

### 9. compose_images needs at least 2 images

If you're generating a page with only one character, you still need to provide 2 reference images to use `compose_images`. Use the character ref plus a style reference, or include a second character's ref even if they're minor in the scene. If a page has no characters at all, use `generate_image` instead.

### 10. Check the GitHub issues before debugging

The repo has a small but active issues list. The 404 model error was already reported as issue #2 before we hit it. A quick check at https://github.com/Junhan2/gemini-nanobanana-mcp/issues could save significant debugging time.
