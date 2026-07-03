"""
THE BRAND BRIEF — ENGINE
A trimmed SimLearn variant for a single lesson: one shared screen per group
(no individual logins), nine quick decisions across three gated stages, a
persistent "ask the professor" AI chat, and a closing writing task.

Content lives in content.py — copy that file's shape for a new variant of
this scenario; this file should not need scenario-specific edits.
"""

import streamlit as st
import os
import json
import anthropic

# =========================================================================
# DEPLOYMENT CONFIG
# =========================================================================

TEACHER_PASSWORD = "business"
CLASS_NAME = "default"

from content import *  # noqa: F401,F403

st.set_page_config(page_title=f"{ORG_NAME} — {SCENARIO_TITLE}", layout="wide")

# =========================================================================
# CONSTANTS / HELPERS
# =========================================================================

PAIR_CODENAMES = ["Boot", "Iron", "Top Hat", "Battleship", "Thimble", "Wheelbarrow", "Car", "Dog",
                  "Cat", "Kite", "Anchor", "Compass"]
MODEL = "claude-haiku-4-5-20251001"

KEYWORD_GUARD_INSTRUCTION = """

IMPORTANT — ABOUT THE STUDENTS' WRITING: Grammar, spelling, and vocabulary mistakes are completely
normal and fine — this is a language-learning exercise, never correct or criticise their English.
Respond normally to any message that is a real attempt at a sentence or question, however imperfect.

However, if the message is just a string of keywords or fragments with no real sentence structure —
something a real person genuinely could not understand as a message (for example: "which source
better?" with nothing else) — do NOT answer the question they seem to be hinting at. Instead, reply
briefly and in character (1-2 sentences) asking them to write it as a proper message. Stay in
character and keep it natural, not robotic.

The test is simple: would a real person understand this as an actual message — a real claim or
question, even if short or ungrammatical? A terse but real message like "is depth better than
breadth here" DOES count and should be answered normally. Only bare topic words with no real
question at all should get the "please rephrase" response."""


def state_dir(class_name):
    base = "/tmp/simlearn/" if os.path.exists("/app") else os.path.expanduser("~/simlearn/")
    d = f"{base}{class_name}"
    os.makedirs(d, exist_ok=True)
    return d


STATE_DIR = state_dir(CLASS_NAME)


def pairs_path(class_name):
    return f"{state_dir(class_name)}/pairs.json"


def new_pair_state():
    return {
        "claimed": False,
        "notes": [],
        "decision_draft": {},  # decision_id -> {"choice": "A"/"B", "however": str}
        "phase_submitted": {},  # phase_id -> bool
        "phase_feedback": {},  # phase_id -> professor's feedback text
        "professor_thread": [],
        "writing_draft": "",
        "writing_peer_feedback": None,
        "writing_summative": None,
        "writing_outcome": None,
    }


def sync_decision_note(notes_list, prefix, content):
    """Keep a single, up-to-date note entry for a given decision instead of
    appending a fresh duplicate every time the pair edits it."""
    notes_list[:] = [n for n in notes_list if not n.startswith(prefix)]
    if content:
        notes_list.append(prefix + content)


def load_pairs(class_name):
    path = pairs_path(class_name)
    if os.path.exists(path):
        with open(path) as f:
            data = json.load(f)
    else:
        data = {}
    changed = False
    for code in PAIR_CODENAMES:
        if code not in data:
            data[code] = new_pair_state()
            changed = True
    if changed:
        save_pairs(class_name, data)
    return data


def save_pairs(class_name, pairs):
    with open(pairs_path(class_name), "w") as f:
        json.dump(pairs, f)


def ai_reply(client, brief, history, user_message, enable_web_search=False):
    full_system = brief + KEYWORD_GUARD_INSTRUCTION
    messages = history + [{"role": "user", "content": user_message}]
    kwargs = dict(model=MODEL, max_tokens=300, system=full_system, messages=messages)
    if enable_web_search:
        kwargs["max_tokens"] = 700
        kwargs["tools"] = [{
            "type": "web_search_20250305",
            "name": "web_search",
            "allowed_domains": ["htw-berlin.de"],
            "max_uses": 3,
        }]
    resp = client.messages.create(**kwargs)
    # With web search enabled, the response can include tool_use / tool_result blocks
    # alongside text — concatenate only the text blocks for what gets shown to students.
    return "".join(block.text for block in resp.content if getattr(block, "type", None) == "text")


def call_claude(client, system, user_content, max_tokens=500):
    resp = client.messages.create(
        model=MODEL, max_tokens=max_tokens, system=system,
        messages=[{"role": "user", "content": user_content}],
    )
    return resp.content[0].text


# =========================================================================
# LOGIN
# =========================================================================

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if not st.session_state.api_key:
    env_anthropic = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if env_anthropic:
        st.session_state.api_key = env_anthropic
    else:
        st.error("API key not configured. Check Railway environment variables.")
        st.stop()

os.makedirs(STATE_DIR, exist_ok=True)
client = anthropic.Anthropic(api_key=st.session_state.api_key)

if "class_authenticated" not in st.session_state:
    st.session_state.class_authenticated = False

if not st.session_state.class_authenticated:
    st.title(SCENARIO_TITLE)
    st.caption(ORG_NAME)
    pw = st.text_input("Class password", type="password")
    if st.button("Enter"):
        if pw == os.environ.get("CLASS_PASSWORD", ""):
            st.session_state.class_authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password.")
    st.stop()

# =========================================================================
# SESSION STATE DEFAULTS
# =========================================================================

for key, default in [
    ("view", "pair_select"),
    ("pair", None),
    ("teacher_mode", False),
    ("teacher_authenticated", False),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# =========================================================================
# SIDEBAR — teacher access
# =========================================================================

with st.sidebar:
    if not st.session_state.teacher_mode:
        if st.button("🧑‍🏫 Teacher dashboard"):
            st.session_state.teacher_mode = True
            st.rerun()

# =========================================================================
# TEACHER DASHBOARD
# =========================================================================

def teacher_dashboard():
    st.title("Teacher Dashboard")
    if st.button("← Back to student view"):
        st.session_state.teacher_mode = False
        st.session_state.teacher_authenticated = False
        st.rerun()

    if not st.session_state.teacher_authenticated:
        pw = st.text_input("Teacher password", type="password", key="teacher_pw")
        if st.button("Unlock"):
            if pw == TEACHER_PASSWORD:
                st.session_state.teacher_authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password.")
        return

    pairs = load_pairs(CLASS_NAME)

    st.subheader("Round-by-round notes (not an answer key)")
    for line in ROUND_TEACHER_NOTES:
        st.write(f"- {line}")

    st.subheader("Key Facts Summary")
    for line in KEY_FACTS_SUMMARY:
        st.write(f"- {line}")

    st.subheader(f"Ask the Professor — {PROFESSOR_NAME}'s brief")
    with st.expander("Show system prompt"):
        st.code(PROFESSOR_BRIEF)

    st.subheader("Active Groups")
    for code in PAIR_CODENAMES:
        pstate = pairs[code]
        if pstate["claimed"]:
            stages_done = sum(1 for p in PHASES if pstate["phase_submitted"].get(p["id"]))
            st.write(f"**{code}** — {stages_done}/{len(PHASES)} stages submitted")

    st.subheader("Reset")
    col1, col2 = st.columns(2)
    with col1:
        reset_code = st.selectbox("Group to reset", PAIR_CODENAMES)
        if st.button("Reset this group"):
            pairs[reset_code] = new_pair_state()
            save_pairs(CLASS_NAME, pairs)
            st.success(f"{reset_code} reset.")
            st.rerun()
    with col2:
        if st.button("⚠️ Reset ALL groups"):
            for code in PAIR_CODENAMES:
                pairs[code] = new_pair_state()
            save_pairs(CLASS_NAME, pairs)
            st.success("All groups reset.")
            st.rerun()


if st.session_state.teacher_mode:
    teacher_dashboard()
    st.stop()

# =========================================================================
# GROUP SELECTION (one shared screen per group — no individual login)
# =========================================================================

def pair_select_view():
    st.title(SCENARIO_TITLE)
    st.caption(f"{ORG_NAME} — as a group, choose one screen to work on together")
    pairs = load_pairs(CLASS_NAME)

    cols = st.columns(4)
    for i, code in enumerate(PAIR_CODENAMES):
        pstate = pairs[code]
        with cols[i % 4]:
            label = f"{code} (in progress — click to continue)" if pstate["claimed"] else code
            if st.button(label, key=f"pair_{code}"):
                if not pstate["claimed"]:
                    pstate["claimed"] = True
                    save_pairs(CLASS_NAME, pairs)
                st.session_state.pair = code
                st.session_state.view = "main"
                st.rerun()


if st.session_state.view == "pair_select":
    pair_select_view()
    st.stop()

# =========================================================================
# MAIN APP (group has claimed a screen)
# =========================================================================

if not st.session_state.pair:
    st.session_state.view = "pair_select"
    st.rerun()
    st.stop()

PAIR = st.session_state.pair
pairs = load_pairs(CLASS_NAME)
pstate = pairs[PAIR]

st.title(SCENARIO_TITLE)
st.caption(f"{ORG_NAME} — Group: {PAIR}")

# --- Sidebar: Notes ---
with st.sidebar:
    st.markdown("### 📝 Shared Notes")
    with st.form(key="note_form", clear_on_submit=True):
        note_input = st.text_input("Quick note", key="note_input", label_visibility="collapsed",
                                    placeholder="Type a note, press Enter...")
        note_submitted = st.form_submit_button("Add")
    if note_submitted and note_input.strip():
        pstate["notes"].append(note_input.strip())
        save_pairs(CLASS_NAME, pairs)
        st.rerun()

    for idx, n in enumerate(pstate["notes"]):
        nc1, nc2 = st.columns([5, 1])
        nc1.write(n)
        if nc2.button("✕", key=f"del_note_{idx}"):
            pstate["notes"].pop(idx)
            save_pairs(CLASS_NAME, pairs)
            st.rerun()

# --- Tabs ---
phase_tab_labels = [f"Stage {i+1}: {p['label']}" for i, p in enumerate(PHASES)]
tab_context, *phase_tabs, tab_professor, tab_writing = st.tabs(
    ["Context"] + phase_tab_labels + [f"Ask {PROFESSOR_NAME.split()[-1]}", "Writing"]
)

# --- Context Tab ---
with tab_context:
    st.write(CONTEXT_TEXT)
    st.warning(CONSTRAINT_TEXT)
    st.caption("Use the 📝 Shared Notes panel in the sidebar to save anything worth remembering.")

# --- Stage Tabs (gated — each stage unlocks after the previous is submitted) ---
for i, (phase, tab) in enumerate(zip(PHASES, phase_tabs)):
    with tab:
        if i > 0 and not pstate["phase_submitted"].get(PHASES[i - 1]["id"]):
            st.info(
                f"Complete Stage {i} and submit it to {PROFESSOR_NAME} first — this stage unlocks "
                "once you have her feedback."
            )
            continue

        st.caption(phase["intro"])
        submitted = pstate["phase_submitted"].get(phase["id"], False)

        if submitted:
            st.success(f"**{PROFESSOR_NAME}'s feedback:**\n\n{pstate['phase_feedback'].get(phase['id'], '')}")
            st.markdown("##### Your choices this stage")
            for d in phase["decisions"]:
                draft = pstate["decision_draft"].get(d["id"], {})
                choice = draft.get("choice")
                chosen_text = d["optA"] if choice == "A" else d["optB"] if choice == "B" else "—"
                st.write(f"**{d['stimulus_title']}** → {chosen_text}")
                if draft.get("however", "").strip():
                    st.caption(f"However: {draft['however'].strip()}")
        else:
            all_complete = True
            for d in phase["decisions"]:
                st.markdown(f"#### {d['stimulus_type']}: {d['stimulus_title']}")
                st.write(d["stimulus_body"])
                st.markdown(f"**{d['prompt']}**")

                draft = pstate["decision_draft"].get(d["id"], {"choice": None, "however": ""})
                opts_display = [f"A — {d['optA']}", f"B — {d['optB']}"]
                idx = 0 if draft.get("choice") == "A" else 1 if draft.get("choice") == "B" else None
                choice_display = st.radio("Your decision:", opts_display, index=idx, key=f"choice_{d['id']}")
                however_val = st.text_area(
                    HOWEVER_PROMPT, value=draft.get("however", ""), key=f"however_{d['id']}", height=70,
                )

                letter = "A" if choice_display and choice_display.startswith("A") else (
                    "B" if choice_display and choice_display.startswith("B") else None
                )
                if letter != draft.get("choice") or however_val != draft.get("however", ""):
                    pstate["decision_draft"][d["id"]] = {"choice": letter, "however": however_val}
                    note_prefix = f"[{d['stimulus_title']}] "
                    note_content = (
                        f"Chose: {d['optA'] if letter == 'A' else d['optB']} — However, {however_val.strip()}"
                        if letter and however_val.strip() else None
                    )
                    sync_decision_note(pstate["notes"], note_prefix, note_content)
                    save_pairs(CLASS_NAME, pairs)
                if not letter or not however_val.strip():
                    all_complete = False
                st.divider()

            if st.button(f"Submit Stage {i + 1} to {PROFESSOR_NAME}", key=f"submit_{phase['id']}"):
                if not all_complete:
                    st.warning("Please choose an option and write a however for every decision before submitting.")
                else:
                    next_phase = PHASES[i + 1] if i + 1 < len(PHASES) else None
                    decisions_summary = "\n".join(
                        f"- {d['stimulus_title']}: chose "
                        f"\"{d['optA'] if pstate['decision_draft'][d['id']]['choice'] == 'A' else d['optB']}\" "
                        f"— however, {pstate['decision_draft'][d['id']]['however'].strip()}"
                        for d in phase["decisions"]
                    )
                    if next_phase:
                        lookahead = (
                            f"Give one concrete thing to keep in mind heading into Stage {i + 2} "
                            f"({next_phase['label']}) — a consideration to hold onto, not the answer."
                        )
                    else:
                        lookahead = (
                            "Since this was the final stage, close with a genuine, encouraging note about "
                            "their thinking so far, without previewing what should go in their proposal "
                            "email."
                        )
                    stage_instruction = f"""

You have just received a written submission from the group for Stage {i + 1} ({phase['label']}) of
planning their thesis. Reply warmly and in character, 4-6 sentences: comment genuinely on their
reasoning, referencing something specific from what they wrote below, then {lookahead} Do not
correct their English."""
                    full_system = PROFESSOR_BRIEF + stage_instruction
                    with st.spinner(f"Sending to {PROFESSOR_NAME}..."):
                        feedback = call_claude(client, full_system, decisions_summary, max_tokens=350)
                    pstate["phase_feedback"][phase["id"]] = feedback
                    pstate["phase_submitted"][phase["id"]] = True
                    save_pairs(CLASS_NAME, pairs)
                    st.rerun()

# --- Ask the Professor Tab ---
with tab_professor:
    st.info(PROFESSOR_INTRO)
    st.caption(
        f"⚠️ {PROFESSOR_NAME} can look up real information from HTW Berlin's website when you ask "
        "about actual BIB procedures, deadlines, or requirements. Treat her answers as a helpful "
        "starting point, not the final word — always confirm anything that matters (deadlines, "
        "forms, ECTS, submission rules) with the real BIB Administration Office before relying on it."
    )
    thread = pstate["professor_thread"]
    for msg in thread:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**{PROFESSOR_NAME}:** {msg['content']}")

    with st.form(key="prof_form", clear_on_submit=True):
        prof_msg = st.text_input("Write a message", key="prof_input")
        prof_sent = st.form_submit_button("Send")
    if prof_sent and prof_msg.strip():
        history = [{"role": m["role"], "content": m["content"]} for m in thread]
        ai_text = ai_reply(client, PROFESSOR_BRIEF, history, prof_msg.strip(), enable_web_search=True)
        thread.append({"role": "user", "content": prof_msg.strip()})
        thread.append({"role": "assistant", "content": ai_text})
        pstate["professor_thread"] = thread
        save_pairs(CLASS_NAME, pairs)
        st.rerun()

# --- Writing Tab ---
with tab_writing:
    with st.expander("Show our shared notes"):
        for n in pstate["notes"]:
            st.write(f"- {n}")

    st.markdown(f"""
Write a short {WRITING_TASK_LABEL} (~{WRITING_WORD_TARGET} words) for the thesis direction your
group has been shaping.

A good abstract:
- Pulls your reasoning across all three stages into ONE coherent direction — not nine separate points
- States the research question or aim clearly
- Says how you'd actually investigate it (your methodology choice from Stage 3)
- Acknowledges a real limitation of this direction, rather than pretending it has none

Check your answers in the three Stage tabs if you need a reminder of what you chose.
""")

    if "writing_draft_box" not in st.session_state:
        st.session_state.writing_draft_box = pstate.get("writing_draft", "")

    draft = st.text_area("Your draft:", value=st.session_state.writing_draft_box, height=250, key="draft_box")
    if draft != pstate.get("writing_draft", ""):
        pstate["writing_draft"] = draft
        save_pairs(CLASS_NAME, pairs)

    if st.button("Get draft feedback"):
        if not draft.strip():
            st.warning("Please write something first.")
        else:
            prompt = f"""You are giving brief, encouraging formative feedback on a {LEVEL}-level Academic
English {WRITING_TASK_LABEL}, written by language learners. This is NOT a grade — it is peer-style
feedback on a draft.

Scenario context: {PEER_FEEDBACK_CONTEXT}

The group's draft:
{draft}

Give 2-3 sentences of feedback: one genuine strength, and one specific, constructive suggestion focused
on either clarity of the research question, coherence across the three stages, or honest acknowledgment
of a limitation. Be warm and encouraging. Do not correct grammar.

Important:
- Read the draft carefully. Do not say something is missing if it is present, even if stated briefly
  or informally.
- Credit the argument being made, not the format."""
            with st.spinner("Getting feedback..."):
                feedback = call_claude(client, prompt, draft)
            pstate["writing_peer_feedback"] = feedback
            save_pairs(CLASS_NAME, pairs)
            st.rerun()

    if pstate.get("writing_peer_feedback"):
        st.info(pstate["writing_peer_feedback"])

        if st.button("Submit final version for grading"):
            prompt = f"""You are proposing a formative grade band (not a final grade — the teacher always
decides) for a {LEVEL}-level Academic English {WRITING_TASK_LABEL}.

Scenario context:
{FINAL_FEEDBACK_CONTEXT}

The group already received this draft feedback:
{pstate['writing_peer_feedback']}

The group's final submission:
{draft}

Propose a grade band (Excellent / Good / Satisfactory / Needs Development), then give exactly one
sentence of feedback on each of these three dimensions:

1. **Coherence** — does the reasoning across all three stages add up to one clear direction, or does
   it contradict itself?
2. **Clarity of aim and method** — is the research question clear, and does the methodology actually
   fit it?
3. **Honesty about limitations** — does it acknowledge a real weakness or likely objection to this
   direction, rather than glossing over it?

Then give ONE overall development point — the single most useful thing to work on next. Do not repeat
points already made. Do not correct grammar.

Important:
- Read the submission carefully before evaluating. Do not say something is missing if it is present,
  even if stated briefly or informally.
- A group that takes a clear position and is honest about one real limitation should score at least
  Good, even if some stages get less attention than others."""
            with st.spinner("Grading..."):
                summative = call_claude(client, prompt, draft, max_tokens=600)
            pstate["writing_summative"] = summative
            save_pairs(CLASS_NAME, pairs)
            st.rerun()

    if pstate.get("writing_summative"):
        st.success(pstate["writing_summative"])

        st.markdown("---")
        st.markdown("##### How did it actually go?")
        st.caption(
            "Get a short, honest reflection on how this direction would likely have played out — "
            "what would have worked, what challenges you'd likely have hit, and the real outcomes of "
            "the choices your group made."
        )
        if st.button("See how it went"):
            choices_summary = "\n".join(
                f"- {d['stimulus_title']}: "
                f"{(d['optA'] if pstate['decision_draft'].get(d['id'], {}).get('choice') == 'A' else d['optB'] if pstate['decision_draft'].get(d['id'], {}).get('choice') == 'B' else '—')}"
                f" (however: {pstate['decision_draft'].get(d['id'], {}).get('however', '').strip() or '—'})"
                for p in PHASES for d in p["decisions"]
            )
            prompt = f"""You are writing a short, honest "how it actually went" reflection on the
thesis-planning choices a group of students made, listed below. This is NOT a story — it's a grounded,
realistic reflection covering three things: (1) how the process would likely have worked out overall,
(2) the specific challenges this combination of choices would likely have created, and (3) the real
outcomes — what they'd have gained and what it would have cost them.
150-200 words, second person plural ("you" / "your group"), grounded and specific — refer to the
actual choices below, not generic advice.
Show real trade-offs. Not purely positive, not purely negative.
If the combination of choices was strategically weak or contradictory across stages, say so honestly
but kindly — this is a rehearsal, and that's exactly the kind of thing worth learning from a rehearsal.

BACKGROUND:
{OUTCOME_PROMPT_CONTEXT}

THE CHOICES MADE AND THE REASONING BEHIND THEM:
{choices_summary}"""
            with st.spinner("Working out how it would have gone..."):
                outcome = call_claude(client, prompt, "Write the reflection now.", max_tokens=400)
            pstate["writing_outcome"] = outcome
            save_pairs(CLASS_NAME, pairs)
            st.rerun()

    if pstate.get("writing_outcome"):
        st.markdown("### How it went")
        st.write(pstate["writing_outcome"])

        st.markdown("---")
        st.caption("Want to try it with different choices?")
        if st.button("🔁 Play again"):
            # Clear cached widget values for this session — Streamlit remembers each
            # widget's last value by key and ignores index=/value= on rerun, so a plain
            # data reset alone wouldn't clear what's shown on screen.
            for p in PHASES:
                for d in p["decisions"]:
                    st.session_state.pop(f"choice_{d['id']}", None)
                    st.session_state.pop(f"however_{d['id']}", None)
            st.session_state.pop("draft_box", None)
            st.session_state.pop("writing_draft_box", None)
            st.session_state.pop("prof_input", None)

            pairs[PAIR] = new_pair_state()
            pairs[PAIR]["claimed"] = True
            save_pairs(CLASS_NAME, pairs)
            st.rerun()
