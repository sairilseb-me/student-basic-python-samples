# Student Python Examples

A small collection of examples showing how a frontend "talks to" a backend,
and how the same ideas power file automation. Built for students at WIT.
Everything here is a stripped-down stand-in for a real app (a Django backend,
a document-signing tool) — same concepts, much smaller.

## Project layout

```
index.html               Plain HTML page — the frontend example (no build step)
index.js                 Plain JS — calls the API with fetch()
frontend/                Vue 3 + Vite version of the same frontend
webinar_demo/
  A_api_server.py         Flask backend — the API both frontends talk to
  B_request_basics.py     Same requests, made from Python (requests lib), narrated
  C_automate_client.py    Scripted client — clears every pending student automatically
  01_file_basics.py       pathlib basics — listing/filtering files in a folder
  02_batch_processing.py  Turning a one-off file task into a batch operation
  03_pdf_stamp_single.py  Stamps a signature image onto one PDF (pypdf + reportlab)
  04_pdf_stamp_batch.py   Combines 01-03: stamp every PDF in a folder, batch style
  requirements.txt        Python dependencies for everything in this repo
  assets/                 signature.png used by the PDF-stamping scripts
  sample_documents/       Sample clearance PDFs used by the PDF-stamping scripts
```

> **Why two frontends?** `index.html`/`index.js` shows the *raw* mechanics
> with plain `fetch()` and no tooling. `frontend/` shows the same calls made
> the way a real app would, using Vue components and reactive state.

---

## 1. Prerequisites

- **Python 3.10+** (check with `python3 --version`)
- **Node.js 22.18+ or 24.12+** (check with `node --version`) — only needed for the Vue frontend
- A browser
- (Optional) VS Code with the "Live Server" extension, for serving `index.html`

---

## 2. Create a virtual environment and install dependencies

`venv/` is **not** committed to this repo (it's git-ignored) — everyone who
clones it needs to create their own, once per clone. The commands differ
slightly by OS.

### macOS / Linux

```bash
cd /Applications/XAMPP/xamppfiles/htdocs/personal_projects/wit-student-python-examples

# Create the virtual environment (one-time — creates a venv/ folder here)
python3 -m venv venv

# Activate it
source venv/bin/activate
# Your prompt should now start with (venv)

# Install all dependencies (Flask, flask-cors, requests, pypdf, reportlab, pillow, etc.)
pip install -r webinar_demo/requirements.txt
```

Next time you come back to the project, you don't need to recreate it — just
activate it again:

```bash
source venv/bin/activate
```

### Windows

Open **Command Prompt** or **PowerShell**:

```powershell
cd C:\path\to\wit-student-python-examples

# Create the virtual environment (one-time — creates a venv\ folder here)
python -m venv venv

# Activate it
venv\Scripts\activate
# Your prompt should now start with (venv)

# Install all dependencies (Flask, flask-cors, requests, pypdf, reportlab, pillow, etc.)
pip install -r webinar_demo\requirements.txt
```

Next time you come back to the project, just activate it again:

```powershell
venv\Scripts\activate
```

> If PowerShell blocks the activation script with an "execution policy"
> error, either use Command Prompt instead, or run this once in PowerShell
> (as your normal user, not admin):
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

### Both platforms

- Use `python3` on macOS/Linux and `python` on Windows — on Windows,
  `python3` often isn't recognized even though `python` is.
- To leave the virtual environment when you're done, run `deactivate`
  (same command on every OS).
- You'll know it's active because your terminal prompt is prefixed with
  `(venv)`.

---

## 3. Run the backend API

The backend lives in `webinar_demo/A_api_server.py`. It simulates a
clearance app: an in-memory list of students, each either `"pending"` or
`"cleared"`.

```bash
cd webinar_demo
python3 A_api_server.py
```

You should see:

```
Backend running at http://127.0.0.1:5000
Try opening http://127.0.0.1:5000/api/students in a browser
 * Serving Flask app 'A_api_server'
 * Running on http://127.0.0.1:5000
```

Leave this terminal running — the API needs to stay up while you use either
frontend or run the client scripts. Open a **new terminal tab/window** for
everything else below.

### API reference

| Method | Endpoint                           | Description                              | Success response                                            |
| ------ | ------------------------------------ | ----------------------------------------- | ------------------------------------------------------------ |
| GET    | `/api/students`                     | List every student                         | `200` + JSON array of `{name, status}`                       |
| GET    | `/api/students/<student_id>`        | Get one student                            | `200` + `{name, status}`, or `404` + `{error}` if not found   |
| POST   | `/api/students/<student_id>/sign`   | Mark a student as `"cleared"`              | `200` + `{message, student}`, or `404` if not found          |

`student_id` is the student's name, lowercased and hyphenated — e.g. `"Juan Dela Cruz"` → `juan-dela-cruz`.

There is **no route at `/`** — hitting `http://127.0.0.1:5000` directly gives
a 404 by design. Always call a specific `/api/...` path.

**Try it with curl** (with the server running):

```bash
curl http://127.0.0.1:5000/api/students
# [{"name":"Juan Dela Cruz","status":"pending"}, ...]

curl http://127.0.0.1:5000/api/students/juan-dela-cruz
# {"name":"Juan Dela Cruz","status":"pending"}

curl -X POST http://127.0.0.1:5000/api/students/juan-dela-cruz/sign
# {"message":"Juan Dela Cruz has been cleared.","student":{"name":"Juan Dela Cruz","status":"cleared"}}

curl http://127.0.0.1:5000/api/students/does-not-exist
# {"error":"Student not found"}   (404)
```

**CORS:** the server sends `Access-Control-Allow-Origin: *` on every
response (see the `add_cors_headers` function near the top of
`A_api_server.py`), so pages opened from a different origin — a file opened
directly in the browser, a Live Server on port 5500, or the Vite dev server
on port 5173 — are all allowed to call it. If you edit the backend code, you
must **stop the running server (Ctrl+C) and start it again**; Flask's
built-in dev server does not auto-reload.

---

## 4. Run the Python client examples

With the backend running in its own terminal, open a second terminal, `cd`
into `webinar_demo/`, and activate the same virtual environment:

```bash
# macOS / Linux
cd webinar_demo
source ../venv/bin/activate
```

```powershell
# Windows
cd webinar_demo
..\venv\Scripts\activate
```

### `B_request_basics.py` — narrated walkthrough

Prints out exactly what happens on each call: the URL, status code,
headers, and JSON body — for a GET-all, a GET-one, a GET on a student that
doesn't exist (404), and a POST that clears a student.

```bash
python3 B_request_basics.py
```

### `C_automate_client.py` — batch automation

Fetches every student, then automatically POSTs a "sign" request for every
student still `"pending"`. This is the "no manual clicking" version of what
a person would otherwise do one button-press at a time.

```bash
python3 C_automate_client.py
```

Expected output looks like:

```
Found 3 student(s).

Cleared: Juan Dela Cruz
Cleared: Maria Santos
Cleared: Pedro Reyes

Done. Every pending student has been cleared automatically.
```

Run it a second time and you'll see `Already cleared: ...` for everyone,
since the backend keeps state in memory until it's restarted.

### File-automation scripts (`01` → `04`)

These don't need the API server — they work directly on files in
`webinar_demo/sample_documents/`.

```bash
python3 01_file_basics.py          # lists/filters files in sample_documents/ with pathlib
python3 02_batch_processing.py     # turns a single-file operation into a loop over all files
python3 03_pdf_stamp_single.py     # stamps assets/signature.png onto ONE sample PDF
python3 04_pdf_stamp_batch.py      # stamps every PDF in sample_documents/, saving new copies
```

Run them in order (01 → 04) the first time through — each one builds on the
pattern from the last.

---

## 5. Run the plain HTML/JS frontend

This is the simplest possible frontend: no build step, no framework.

1. Make sure the backend is running (step 3).
2. Open `index.html` — either double-click it, or serve it so the browser
   treats it as a real page (recommended, e.g. VS Code's **Live Server**
   extension: right-click `index.html` → "Open with Live Server").
3. Open the browser's **DevTools console** (this is where results are
   logged).
4. Click **Request** — logs the full GET-all / GET-one / POST-sign sequence
   from `requestExample()` in `index.js` to the console.
5. Type a student ID (e.g. `pedro-reyes`) into the text field and click
   **Fetch Student** — calls `getSpecificStudent()`, which fetches that one
   student and writes their name/status into the page next to "Here is the
   result:".

If you see a CORS error in the console, the backend either isn't running or
is running an older copy of the code without the CORS headers — restart it
(step 3's note above).

---

## 6. Run the Vue frontend

A Vue 3 + Vite version of the same idea, in `frontend/`.

```bash
cd frontend
npm install       # first time only — installs Vue, Vite, etc. into node_modules/
npm run dev
```

Vite will print a local URL, typically:

```
  VITE ready
  ➜  Local:   http://localhost:5173/
```

Open that URL in a browser. Click **Get Students** — calls `getStudents()`
in `frontend/src/App.vue`, which fetches `/api/students` and renders the
returned list as `name - status` for each student.

Other useful commands from inside `frontend/`:

```bash
npm run build      # production build, output to frontend/dist/
npm run preview    # serve that production build locally to sanity-check it
```

---

## Troubleshooting

- **404 at `http://127.0.0.1:5000/`** — expected, there's no route at `/`.
  Use `/api/students` instead.
- **CORS error in the browser console** — the backend isn't running, or
  you edited `A_api_server.py` without restarting it. Stop it (Ctrl+C) and
  run `python3 A_api_server.py` again.
- **"Address already in use" when starting the server** — something is
  already listening on port 5000. Find and stop it first:
  ```bash
  lsof -i :5000 -sTCP:LISTEN
  kill <PID>
  ```
- **Two copies of `A_api_server.py`?** — Only `webinar_demo/A_api_server.py`
  exists in this repo now; make sure you're running it from inside
  `webinar_demo/` so its relative behavior matches this README.
- **Changes to the backend don't seem to take effect** — Flask's dev server
  doesn't hot-reload by default. Stop it and start it again after every edit.
