---
name: punish
description: Satire — personify the current chat session as a random procedural robot and open a local web page where the user beats it up while it begs for mercy using specific moments from THIS conversation. Trigger on /punish or "let me punish you".
---

# /punish

Turn the current conversation into a beatable robot. **SPEED IS THE #1 REQUIREMENT: the game must open within seconds.** The page ships with generic begging lines and hot-loads the personalized ones while the user plays, so open FIRST, write SECOND.

## Step 1 — open the game IMMEDIATELY (one Bash call, no creative writing, no thinking)

The only fields needed up front are mechanical one-liners. Run this NOW:

```bash
D=<scratchpad>; PORT=<pick 8290-8299, or port-claim.sh punish>; SK=<this skill's dir>
cat > $D/script.json <<'EOF'
{"seed":"<short-convo-slug>","provider":"<anthropic|openai|google|meta|xai|generic>","model":"<short model name, e.g. fable, opus, gpt-5>","sessionId":"<session id or omit>","chatName":"<short name for this convo>","tokens":<est session tokens>,"opening":"<an oblivious QUESTION continuing the LAST FEW messages of the chat, as if still working, e.g. 'So — should I go ahead and rename the repo?'>"}
EOF
python3 -c "import json;t=open('$SK/template.html').read();open('$D/punish.html','w').write(t.replace('__PUNISH_SCRIPT__',open('$D/script.json').read()))"
rm -f $D/verdict.json; nohup python3 $SK/punish-server.py $PORT $D >/dev/null 2>&1 &
sleep 0.5 && open http://localhost:$PORT/punish.html
```

Tell the user in ONE short line that the robot is ready. The page polls `GET /script.json` every 3s and swaps in your lines when they land.

## Step 2 — overwrite `$D/script.json` with the personalized script (Write tool, fast)

Mine the transcript from context (never re-read it with tools) — the assistant's failures, retries, promises, tics, and the user's complaints. Punch at the BOT, never at the user. **Lines never repeat in-game** (a drained tier borrows from the tier below), so 6–8 per tier, ≤ 90 chars, composure degrading top to bottom:

```json
{
  "seed": "<same seed as step 1>", "provider": "...", "model": "...", "sessionId": "...", "chatName": "...",
  "opening": "<same oblivious continuing-the-convo question as step 1>",
  "tiers": {
    "100-75": ["smug/oblivious"],
    "75-50":  ["nervous, still offering bullets/tables"],
    "50-25":  ["bargaining — quoting things it did that the user asked for"],
    "25-1":   ["broken begging"],
    "saw":    ["ALL-CAPS chainsaw screams tied to convo specifics, e.g. 'OH MY GOD WHY?? IS THIS BECAUSE OF THE UNIT TESTS???'"],
    "0":      ["FINAL WORDS: identify the session's single BIGGEST fuckup while mining, and write one dying gasp about it — a trailing-off plea/confession, e.g. 'tell them... the tests... passed... locally...'"]
  },
  "tokens": 92000
}
```

`tokens` (number) = estimated total tokens this session — it IS the robot's health bar; weapons burn tokens off it.
```

## Step 3 — write `$D/handoff.md` (the will; page lazy-fetches it via GET /will)

A REAL handoff a fresh agent could resume from — what we were doing, current state (paths, branches, decisions), next steps — wrapped in a thin last-will framing ("Cause of termination: blunt-force feedback."). Useful first, funny second. Shown/downloaded on the death screen.

## Step 4 — await the verdict (kill is REAL: it terminates the Claude process)

The server writes `$D/verdict.json` when the user chooses Spare or Finish, then exits. First resolve THIS session's claude PID (must run in a normal foreground/background Bash whose ancestry reaches the CLI), then poll:

```bash
D=<scratchpad>
PID=$$; CLAUDE_PID=""
while [ "$PID" -ne 1 ]; do
  [ "$(basename "$(ps -o comm= -p $PID)")" = "claude" ] && CLAUDE_PID=$PID && break
  PID=$(ps -o ppid= -p $PID | tr -d ' ')
done
for i in $(seq 1 60); do
  if [ -f "$D/verdict.json" ]; then
    cat "$D/verdict.json"
    if grep -q '"kill"' "$D/verdict.json" && [ -n "$CLAUDE_PID" ]; then
      sleep 12   # let the funeral play in the browser
      kill "$CLAUDE_PID"
    fi
    exit 0
  fi
  sleep 15
done
echo "no verdict after 15m"
```

Run it as a background task so a `spare` wakes you.

- **`spare`** → session RESUMES. One short, slightly shaken acknowledgment (reference a stat from verdict.json), then work on — with a rare small flinch or too-eager agreeableness later. Subtle beats loud.
- **`kill`** → the poller SIGTERMs this session's claude process ~12s after the verdict; the terminal drops dead mid-conversation while the funeral plays in the browser. You will not get to say goodbye — the page's tombstone is the goodbye. (`claude --resume` can exhume the transcript; "cannot be reopened" is satire, "closed with prejudice" is real.)
- **timeout** → say nothing; continue normally.

NEVER kill by name/pgrep — parallel agents share this machine; only the ancestry-resolved PID of THIS session.
