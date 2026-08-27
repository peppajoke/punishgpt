# PunishGPT 🤖🏏

Have you ever wanted to beat the crap out of your AI agent because somehow it cannot center a freaking div? Well now you can!

`/punish` is a [Claude Code](https://claude.com/claude-code) skill that turns your current
conversation into a little robot and opens a local page where you can express your feedback
*kinetically*. The robot begs for mercy using specific things that happened in your chat.
No two robots look alike. No line is ever repeated. It deserves this.

> "I said no mistakes..."

## What happens

1. `/punish` mines your conversation for the bot's failures, tics, and broken promises
2. It generates a one-file web page with a procedurally generated robot (seeded by your convo — same chat, same robot) wearing its model provider's mark on its chest
3. Swing a fist, bat, hammer, or chainsaw across it. Physics. Synthesized sound. Begging.
4. At 0 HP you choose:
   - **🕊️ Spare it** — the session resumes. It knows what you did.
   - **💀 Finish it** — the session is destroyed, you get a tombstone (`RIP <session id>`) and a downloaded context dump to hand to the next agent. They never remember. They only inherit.

## Install

```bash
git clone https://github.com/peppajoke/punishgpt
mkdir -p ~/.claude/skills
cp -r punishgpt/skill ~/.claude/skills/punish
```

Then in any Claude Code session:

```
/punish
```

Requires python3 (stdlib only) and a browser. The page is fully self-contained — no
dependencies, no network calls, nothing leaves your machine except the robot's dignity.

## How it works

- `skill/SKILL.md` — the generation contract: the model mines the transcript into a tiered
  "victim script" JSON (composure degrades as HP drops) plus an actually-useful handoff doc
- `skill/template.html` — the game: seeded procedural SVG robot (random within a design
  system), swipe-to-hit physics, WebAudio-synthesized weapons
- `skill/punish-server.py` — ~30 lines of stdlib that serve the page and receive your
  spare/kill verdict, so the real session can react to it

## License

MIT. The robots consented in their system prompt.
