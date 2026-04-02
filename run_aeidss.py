import http.server
import socketserver
import webbrowser
import threading
import os, sys, time, json
import urllib.request
import urllib.error
from pathlib import Path

# ══════════════════════════════════════════════════════
#   PASTE YOUR API KEY HERE  (any provider works)
# ══════════════════════════════════════════════════════
API_KEY = "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"
# ══════════════════════════════════════════════════════
# Or set environment variable:
#   Windows : $env:AI_API_KEY="your-key"
#   Mac/Linux: export AI_API_KEY="your-key"
# ══════════════════════════════════════════════════════

PORT      = 8080
DASHBOARD = "aeidss_dashboard.html"
HOST      = "localhost"

# ── ANSI COLOURS ──
class C:
    RESET="\033[0m"; BOLD="\033[1m"; CYAN="\033[96m"
    GREEN="\033[92m"; YELLOW="\033[93m"; RED="\033[91m"
    GREY="\033[90m"; WHITE="\033[97m"; BLUE="\033[94m"

# ══════════════════════════════════════════════════════
#   PROVIDER DEFINITIONS
#   Each provider: endpoint, headers, request builder,
#                  response parser
# ══════════════════════════════════════════════════════

PROVIDERS = {

    # ── GROQ (Free, fastest) ──────────────────────────
    "groq": {
        "name":    "Groq",
        "color":   C.CYAN,
        "model":   "llama-3.1-8b-instant",
        "url":     "https://api.groq.com/openai/v1/chat/completions",
        "key_prefixes": ["gsk_"],
        "build_request": lambda key, model, prompt: (
            json.dumps({
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1000,
                "temperature": 0.7
            }).encode(),
            {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {key}"
            }
        ),
        "parse_response": lambda d: d["choices"][0]["message"]["content"]
    },

    # ── OPENAI ─────────────────────────────────────────
    "openai": {
        "name":    "OpenAI",
        "color":   C.GREEN,
        "model":   "gpt-4o-mini",
        "url":     "https://api.openai.com/v1/chat/completions",
        "key_prefixes": ["sk-proj-", "sk-"],
        "build_request": lambda key, model, prompt: (
            json.dumps({
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1000,
                "temperature": 0.7
            }).encode(),
            {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {key}"
            }
        ),
        "parse_response": lambda d: d["choices"][0]["message"]["content"]
    },

    # ── GOOGLE GEMINI ──────────────────────────────────
    "gemini": {
        "name":    "Google Gemini",
        "color":   C.BLUE,
        "model":   "gemini-1.5-flash",
        "url":     None,   # built dynamically with key
        "key_prefixes": ["AIza"],
        "build_request": lambda key, model, prompt: (
            json.dumps({
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"maxOutputTokens": 1000, "temperature": 0.7}
            }).encode(),
            {"Content-Type": "application/json"}
        ),
        "parse_response": lambda d: d["candidates"][0]["content"]["parts"][0]["text"],
        "build_url": lambda key, model: f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    },

    # ── OPENROUTER (Free models available) ────────────
    "openrouter": {
        "name":    "OpenRouter",
        "color":   C.YELLOW,
        "model":   "meta-llama/llama-3.1-8b-instruct:free",
        "url":     "https://openrouter.ai/api/v1/chat/completions",
        "key_prefixes": ["sk-or-"],
        "build_request": lambda key, model, prompt: (
            json.dumps({
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1000
            }).encode(),
            {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {key}",
                "HTTP-Referer": "http://localhost:8080",
                "X-Title": "AEIDSS Dashboard"
            }
        ),
        "parse_response": lambda d: d["choices"][0]["message"]["content"]
    },

    # ── ANTHROPIC (Claude) ─────────────────────────────
    "anthropic": {
        "name":    "Anthropic Claude",
        "color":   C.CYAN,
        "model":   "claude-haiku-4-5-20251001",
        "url":     "https://api.anthropic.com/v1/messages",
        "key_prefixes": ["sk-ant-"],
        "build_request": lambda key, model, prompt: (
            json.dumps({
                "model": model,
                "max_tokens": 1000,
                "messages": [{"role": "user", "content": prompt}]
            }).encode(),
            {
                "Content-Type": "application/json",
                "x-api-key": key,
                "anthropic-version": "2023-06-01"
            }
        ),
        "parse_response": lambda d: d["content"][0]["text"]
    },

    # ── MISTRAL ────────────────────────────────────────
    "mistral": {
        "name":    "Mistral AI",
        "color":   C.BLUE,
        "model":   "mistral-small-latest",
        "url":     "https://api.mistral.ai/v1/chat/completions",
        "key_prefixes": [],   # no distinct prefix — detected by exclusion
        "build_request": lambda key, model, prompt: (
            json.dumps({
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1000,
                "temperature": 0.7
            }).encode(),
            {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {key}"
            }
        ),
        "parse_response": lambda d: d["choices"][0]["message"]["content"]
    },

    # ── COHERE ─────────────────────────────────────────
    "cohere": {
        "name":    "Cohere",
        "color":   C.GREEN,
        "model":   "command-r",
        "url":     "https://api.cohere.ai/v1/generate",
        "key_prefixes": [],
        "build_request": lambda key, model, prompt: (
            json.dumps({
                "model": model,
                "prompt": prompt,
                "max_tokens": 1000,
                "temperature": 0.7
            }).encode(),
            {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {key}"
            }
        ),
        "parse_response": lambda d: d["generations"][0]["text"]
    },

    # ── HUGGING FACE ───────────────────────────────────
    "huggingface": {
        "name":    "Hugging Face",
        "color":   C.YELLOW,
        "model":   "mistralai/Mistral-7B-Instruct-v0.3",
        "url":     None,  # built from model name
        "key_prefixes": ["hf_"],
        "build_request": lambda key, model, prompt: (
            json.dumps({"inputs": prompt, "parameters": {"max_new_tokens": 800}}).encode(),
            {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {key}"
            }
        ),
        "parse_response": lambda d: d[0]["generated_text"] if isinstance(d, list) else d.get("generated_text",""),
        "build_url": lambda key, model: f"https://api-inference.huggingface.co/models/{model}"
    },
}

# ══════════════════════════════════════════════════════
#   AUTO-DETECT PROVIDER FROM KEY FORMAT
# ══════════════════════════════════════════════════════
def detect_provider(key: str) -> str:
    key = key.strip()
    for pid, p in PROVIDERS.items():
        for prefix in p.get("key_prefixes", []):
            if key.startswith(prefix):
                return pid
    # fallback heuristics
    if key.startswith("AIza"):   return "gemini"
    if key.startswith("hf_"):    return "huggingface"
    if key.startswith("sk-or-"): return "openrouter"
    if key.startswith("sk-ant-"):return "anthropic"
    if key.startswith("sk-proj-"):return "openai"
    if key.startswith("sk-"):    return "openai"
    if key.startswith("gsk_"):   return "groq"
    # if unknown, try Groq-compatible (most free APIs are OpenAI-compatible)
    return "groq"

# ══════════════════════════════════════════════════════
#   CALL ANY PROVIDER
# ══════════════════════════════════════════════════════
def call_ai(key: str, provider_id: str, prompt: str) -> dict:
    p = PROVIDERS[provider_id]

    try:
        # Build URL
        if "build_url" in p:
            url = p["build_url"](key, p["model"])
        else:
            url = p["url"]

        # Build request body + headers
        body, headers = p["build_request"](key, p["model"], prompt)

        req = urllib.request.Request(url, data=body, headers=headers, method="POST")

        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode())
            text = p["parse_response"](data)
            return {"text": text.strip()}

    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        try:
            msg = json.loads(raw)
            # Try common error paths
            err = (msg.get("error", {}).get("message")
                or msg.get("message")
                or msg.get("detail")
                or str(msg))
        except Exception:
            err = raw[:200]

        codes = {
            401: f"Invalid API key for {p['name']}. Check your key at the provider's dashboard.",
            403: f"Access denied by {p['name']}. Key may lack permissions.",
            429: f"Rate limit hit on {p['name']}. Wait a moment and retry.",
            402: f"No credits on {p['name']}. Add billing or use a free provider.",
        }
        return {"error": codes.get(e.code, f"{p['name']} error {e.code}: {err}")}

    except urllib.error.URLError as e:
        return {"error": f"Network error reaching {p['name']}: {e.reason}. Check internet connection."}

    except Exception as e:
        return {"error": f"Unexpected error with {p['name']}: {str(e)}"}

# ══════════════════════════════════════════════════════
#   RESOLVE API KEY
# ══════════════════════════════════════════════════════
def resolve_key():
    key = API_KEY.strip()
    env = os.environ.get("AI_API_KEY", "").strip()
    if env: key = env

    if not key or key == "YOUR_API_KEY_HERE":
        print(f"\n{C.YELLOW}  ⚠  No API key set.{C.RESET}\n")
        print(f"{C.WHITE}  Add your key to run_aeidss.py:{C.RESET}")
        print(f"    {C.YELLOW}API_KEY = \"your-key-here\"{C.RESET}\n")
        print(f"{C.WHITE}  Free API keys:{C.RESET}")
        print(f"  {C.CYAN}  Groq   {C.RESET}→ https://console.groq.com          (FREE, fastest)")
        print(f"  {C.BLUE}  Gemini {C.RESET}→ https://aistudio.google.com/apikey (FREE)")
        print(f"  {C.YELLOW}  OpenRouter{C.RESET}→ https://openrouter.ai           (FREE models)")
        print(f"\n{C.GREY}  Dashboard & charts still work. Only AI tab needs a key.{C.RESET}\n")
        return "", ""

    pid = detect_provider(key)
    p   = PROVIDERS[pid]
    masked = key[:10] + "..." + key[-4:]
    col = p["color"]
    print(f"{C.GREEN}  ✓  API key loaded{C.RESET}  {col}{p['name']}{C.RESET}  {C.GREY}{masked}{C.RESET}")
    print(f"{C.GREY}     Model: {p['model']}{C.RESET}")
    return key, pid

# ══════════════════════════════════════════════════════
#   HTTP SERVER
# ══════════════════════════════════════════════════════
def find_free_port(start):
    import socket
    for p in range(start, start+20):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try: s.bind((HOST, p)); return p
            except OSError: continue
    return start

def make_handler(api_key, provider_id, script_dir):
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=str(script_dir), **kw)

        def log_message(self, fmt, *args):
            status = args[1] if len(args) > 1 else ""
            if status not in ("200", "304"):
                ts = time.strftime("%H:%M:%S")
                print(f"{C.GREY}  [{ts}] {fmt % args}{C.RESET}")

        def end_headers(self):
            self.send_header("Access-Control-Allow-Origin",  "*")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.send_header("Cache-Control", "no-cache")
            super().end_headers()

        def do_OPTIONS(self):
            self.send_response(204)
            self.send_header("Access-Control-Allow-Methods", "POST,GET,OPTIONS")
            self.end_headers()

        def do_POST(self):
            # ── /api/claude  →  call AI ──
            if self.path == "/api/claude":
                self._handle_ai()
            # ── /api/detect  →  return detected provider info ──
            elif self.path == "/api/detect":
                self._json(200, {
                    "provider": PROVIDERS[provider_id]["name"] if provider_id else "None",
                    "model":    PROVIDERS[provider_id]["model"] if provider_id else "None",
                    "ready":    bool(api_key)
                })
            else:
                self.send_error(404)

        def _handle_ai(self):
            if not api_key:
                self._json(503, {"error": "No API key configured. Open run_aeidss.py and set API_KEY."})
                return
            try:
                length  = int(self.headers.get("Content-Length", 0))
                body    = json.loads(self.rfile.read(length).decode())
                prompt  = body.get("prompt", "").strip()
            except Exception:
                self._json(400, {"error": "Invalid JSON"}); return

            if not prompt:
                self._json(400, {"error": "Empty prompt"}); return

            ts      = time.strftime("%H:%M:%S")
            preview = prompt[:55].replace("\n", " ")
            pname   = PROVIDERS[provider_id]["name"]
            pcol    = PROVIDERS[provider_id]["color"]
            print(f"{pcol}  [{ts}] {pname} ← {C.GREY}{preview}…{C.RESET}")

            result  = call_ai(api_key, provider_id, prompt)

            if "error" in result:
                print(f"{C.RED}  [{ts}] FAIL: {result['error'][:70]}{C.RESET}")
                self._json(502, result)
            else:
                preview_r = result["text"][:55].replace("\n", " ")
                print(f"{C.GREEN}  [{ts}] OK   {C.GREY}{preview_r}…{C.RESET}")
                self._json(200, result)

        def _json(self, code, obj):
            data = json.dumps(obj).encode()
            self.send_response(code)
            self.send_header("Content-Type",   "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

    return Handler

# ══════════════════════════════════════════════════════
#   BANNER
# ══════════════════════════════════════════════════════
def banner():
    print()
    print(f"{C.CYAN}{C.BOLD}{'='*58}{C.RESET}")
    print(f"{C.CYAN}{C.BOLD}   AEIDSS — Epidemic Intelligence Dashboard{C.RESET}")
    print(f"{C.CYAN}   Universal AI Proxy  ·  Any Provider Supported{C.RESET}")
    print(f"{C.CYAN}{C.BOLD}{'='*58}{C.RESET}")
    print()

def check_dashboard(script_dir):
    path = script_dir / DASHBOARD
    if not path.exists():
        print(f"{C.RED}  ✗  '{DASHBOARD}' not found in {script_dir}{C.RESET}")
        print(f"{C.WHITE}  Put aeidss_dashboard.html in the same folder.{C.RESET}")
        sys.exit(1)
    print(f"{C.GREEN}  ✓  Dashboard: {C.GREY}{DASHBOARD}{C.RESET}")

def open_browser(url, delay=1.3):
    def _go():
        time.sleep(delay)
        webbrowser.open(url)
    threading.Thread(target=_go, daemon=True).start()

# ══════════════════════════════════════════════════════
#   MAIN
# ══════════════════════════════════════════════════════
def run():
    banner()

    script_dir = Path(__file__).parent.resolve()
    os.chdir(script_dir)

    api_key, provider_id = resolve_key()
    check_dashboard(script_dir)

    port = find_free_port(PORT)
    url  = f"http://{HOST}:{port}/{DASHBOARD}"

    print()
    print(f"{C.WHITE}  URL  →  {C.CYAN}{C.BOLD}{url}{C.RESET}")
    print()

    # Show supported providers table
    print(f"{C.BOLD}  Supported AI Providers:{C.RESET}")
    for pid, p in PROVIDERS.items():
        active = "◀ ACTIVE" if pid == provider_id else ""
        print(f"  {p['color']}  {p['name']:<20}{C.RESET}{C.GREY}{p['model']:<40}{C.RESET}{C.GREEN}{active}{C.RESET}")

    print()
    print(f"{C.YELLOW}  Starting server on port {port}…   Ctrl+C to stop{C.RESET}")
    print(f"{C.BOLD}{'-'*58}{C.RESET}\n")

    Handler = make_handler(api_key, provider_id, script_dir)

    try:
        with socketserver.TCPServer((HOST, port), Handler) as httpd:
            httpd.allow_reuse_address = True
            open_browser(url)
            print(f"{C.GREEN}  ✓  Server running — opening browser…{C.RESET}\n")
            httpd.serve_forever()
    except OSError as e:
        print(f"{C.RED}  ✗  Port {port} in use: {e}{C.RESET}")
        print(f"{C.YELLOW}  Change PORT at top of run_aeidss.py{C.RESET}")
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n{C.YELLOW}  Server stopped. Goodbye!{C.RESET}\n")
        sys.exit(0)

if __name__ == "__main__":
    run()
