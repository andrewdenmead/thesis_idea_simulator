"""
THESIS ADVICE LINE — ENGINE
A trimmed SimLearn variant for a single lesson: pairs of students, no
asymmetric-information roles, nine quick decision rounds, a persistent
"ask the professor" AI chat, and a closing writing task.

Content lives in content.py — copy that file's shape for a new variant of
this scenario; this file should not need scenario-specific edits.
"""

import streamlit as st
import os
import json
import uuid
import anthropic

# =========================================================================
# DEPLOYMENT CONFIG
# =========================================================================

TEACHER_PASSWORD = "business"
CLASS_NAME = "default"
PAIR_MAX = 2  # fixed — this scenario is pairs, not role-based groups

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
        "occupants": [],
        "notes": [],
        "current_round": 0,
        "round_choices": {},
        "professor_thread": [],
        "writing_draft": "",
        "writing_peer_feedback": None,
        "writing_summative": None,
        "writing_outcome": None,
        "left_students": False,
    }


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


def display_names(pstate):
    names = [o["name"].strip() for o in pstate["occupants"] if o.get("name", "").strip()]
    return " & ".join(names) if names else "—"


def ai_reply(client, brief, history, user_message):
    full_system = brief + KEYWORD_GUARD_INSTRUCTION
    messages = history + [{"role": "user", "content": user_message}]
    resp = client.messages.create(model=MODEL, max_tokens=300, system=full_system, messages=messages)
    return resp.content[0].text


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
    ("my_id", None),
    ("my_name", None),
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

    st.subheader("Active Pairs")
    for code in PAIR_CODENAMES:
        pstate = pairs[code]
        if pstate["occupants"]:
            rnd = min(pstate["current_round"] + 1, len(ROUNDS))
            st.write(f"**{code}** — {display_names(pstate)} — round {rnd}/{len(ROUNDS)}")

    st.subheader("Remove Individual Students")
    for code in PAIR_CODENAMES:
        pstate = pairs[code]
        for occ in list(pstate["occupants"]):
            if st.button(f"Remove {code} — {occ['name']}", key=f"rm_{code}_{occ['id']}"):
                pstate["occupants"].remove(occ)
                save_pairs(CLASS_NAME, pairs)
                st.rerun()

    st.subheader("Reset")
    col1, col2 = st.columns(2)
    with col1:
        reset_code = st.selectbox("Pair to reset", PAIR_CODENAMES)
        if st.button("Reset this pair"):
            pairs[reset_code] = new_pair_state()
            save_pairs(CLASS_NAME, pairs)
            st.success(f"{reset_code} reset.")
            st.rerun()
    with col2:
        if st.button("⚠️ Reset ALL pairs"):
            for code in PAIR_CODENAMES:
                pairs[code] = new_pair_state()
            save_pairs(CLASS_NAME, pairs)
            st.success("All pairs reset.")
            st.rerun()


if st.session_state.teacher_mode:
    teacher_dashboard()
    st.stop()

# =========================================================================
# PAIR SELECTION + NAME ENTRY
# =========================================================================

def pair_select_view():
    st.title(SCENARIO_TITLE)
    st.caption(f"{ORG_NAME} — choose your pair")
    pairs = load_pairs(CLASS_NAME)

    cols = st.columns(4)
    for i, code in enumerate(PAIR_CODENAMES):
        pstate = pairs[code]
        count = len(pstate["occupants"])
        with cols[i % 4]:
            if count < PAIR_MAX:
                label = f"{code} ({count}/{PAIR_MAX})"
                if count == 1:
                    label += f" — {display_names(pstate)} joined"
                if st.button(label, key=f"pair_{code}"):
                    st.session_state.pair = code
                    st.session_state.view = "name_entry"
                    st.rerun()
            else:
                st.button(f"{code} ({count}/{PAIR_MAX}) — {display_names(pstate)}",
                          key=f"pair_{code}_full", disabled=True)
                for occ in pstate["occupants"]:
                    if st.button(f"Rejoin as {occ['name']} ↩", key=f"rejoin_{code}_{occ['id']}"):
                        st.session_state.pair = code
                        st.session_state.my_id = occ["id"]
                        st.session_state.my_name = occ["name"]
                        st.session_state.view = "main"
                        st.rerun()


def name_entry_view():
    st.title("What's your name?")
    if st.button("← Back to pair selection"):
        st.session_state.pair = None
        st.session_state.view = "pair_select"
        st.rerun()
    name = st.text_input("Your name")
    if st.button("Join"):
        if name.strip():
            pairs = load_pairs(CLASS_NAME)
            pstate = pairs[st.session_state.pair]
            new_id = str(uuid.uuid4())[:8]
            pstate["occupants"].append({"name": name.strip(), "id": new_id})
            save_pairs(CLASS_NAME, pairs)
            st.session_state.my_id = new_id
            st.session_state.my_name = name.strip()
            st.session_state.view = "main"
            st.rerun()
        else:
            st.warning("Please enter a name.")


if st.session_state.view == "pair_select":
    pair_select_view()
    st.stop()
elif st.session_state.view == "name_entry":
    name_entry_view()
    st.stop()

# =========================================================================
# MAIN APP (student has joined a pair)
# =========================================================================

PAIR = st.session_state.pair
pairs = load_pairs(CLASS_NAME)
pstate = pairs[PAIR]

st.title(SCENARIO_TITLE)
st.caption(f"{ORG_NAME} — Pair: {PAIR} — You are {st.session_state.my_name}, with {display_names(pstate)}")

# --- Sidebar: Notes (shared between both partners) ---
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

    st.divider()
    if st.button("🔄 Refresh (see partner's progress)"):
        st.rerun()
    if not pstate.get("left_students"):
        if st.button("🚪 I have to leave"):
            pstate["left_students"] = True
            save_pairs(CLASS_NAME, pairs)
            st.rerun()

# --- Tabs ---
tab_context, tab_rounds, tab_professor, tab_writing = st.tabs(
    ["Context", DECISIONS_TAB_HEADER, f"Ask {PROFESSOR_NAME.split()[-1]}", "Writing"]
)

# --- Context Tab ---
with tab_context:
    st.write(CONTEXT_TEXT)
    st.warning(CONSTRAINT_TEXT)
    st.caption("Use the 📝 Shared Notes panel in the sidebar to save anything worth remembering.")

# --- Advice Rounds Tab ---
with tab_rounds:
    current = pstate["current_round"]

    if current > 0:
        with st.expander(f"Review your earlier advice ({current}/{len(ROUNDS)} rounds done)"):
            for r in ROUNDS[:current]:
                choice = pstate["round_choices"].get(r["id"], {}).get("choice")
                chosen_text = r["optA"] if choice == "A" else r["optB"] if choice == "B" else "—"
                st.write(f"**{r['stimulus_title']}** → {chosen_text}")

    if current >= len(ROUNDS):
        st.success("All nine rounds done. Head to the Writing tab to pull your advice together.")
    else:
        r = ROUNDS[current]
        st.caption(f"Phase {r['phase']} — {r['phase_label']} · Round {current + 1} of {len(ROUNDS)}")
        st.markdown(f"#### {r['stimulus_type']}: {r['stimulus_title']}")
        st.write(r["stimulus_body"])
        st.markdown(f"**{r['prompt']}**")

        existing = pstate["round_choices"].get(r["id"], {}).get("choice")
        opts_display = [f"A — {r['optA']}", f"B — {r['optB']}"]
        idx = 0 if existing == "A" else 1 if existing == "B" else None
        choice_display = st.radio("Your advice:", opts_display, index=idx, key=f"round_{r['id']}")

        if st.button("Confirm and continue", key=f"confirm_{r['id']}"):
            if choice_display is None:
                st.warning("Choose A or B first.")
            else:
                letter = "A" if choice_display.startswith("A") else "B"
                pstate["round_choices"][r["id"]] = {"choice": letter}
                pstate["current_round"] = current + 1
                save_pairs(CLASS_NAME, pairs)
                st.rerun()

# --- Ask the Professor Tab ---
with tab_professor:
    st.info(PROFESSOR_INTRO)
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
        ai_text = ai_reply(client, PROFESSOR_BRIEF, history, prof_msg.strip())
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
Write a {WRITING_TASK_LABEL} addressed to {WRITING_ADDRESSEE} (~{WRITING_WORD_TARGET} words).

Your email should:
- Pull your advice across all nine rounds into ONE coherent recommendation — not nine separate tips
- State clearly what you think Jonas should do next, and why
- Acknowledge the strongest reason he might disagree with you, and answer it
- Sound like a real message from a friend, not a formal report

Check the round summary in the Advice Rounds tab if you need a reminder of what you chose.
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
English {WRITING_TASK_LABEL}, written by a language learner. This is NOT a grade — it is peer-style
feedback on a draft.

Scenario context: {PEER_FEEDBACK_CONTEXT}

The student's draft:
{draft}

Give 2-3 sentences of feedback: one genuine strength, and one specific, constructive suggestion focused
on either clarity of recommendation, coherence across the nine rounds, or handling of the strongest
counter-argument. Be warm and encouraging. Do not correct grammar.

Important:
- Read the draft carefully. Do not say the student missed something if it is present, even if stated
  briefly or informally.
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

The student already received this draft feedback:
{pstate['writing_peer_feedback']}

The student's final submission:
{draft}

Propose a grade band (Excellent / Good / Satisfactory / Needs Development), then give exactly one
sentence of feedback on each of these three dimensions:

1. **Coherence** — does the advice across all nine rounds add up to one clear recommendation, or does
   it contradict itself?
2. **Reasoning** — is the recommendation justified, not just stated?
3. **Handling disagreement** — does it acknowledge a real reason Jonas might push back, and answer it?

Then give ONE overall development point — the single most useful thing to work on next. Do not repeat
points already made. Do not correct grammar.

Important:
- Read the submission carefully before evaluating. Do not say the student missed something if it is
  present, even if stated briefly or informally.
- A student who takes a clear position and handles one real objection should score at least Good, even
  if some rounds get less attention than others."""
            with st.spinner("Grading..."):
                summative = call_claude(client, prompt, draft, max_tokens=600)
            pstate["writing_summative"] = summative
            save_pairs(CLASS_NAME, pairs)
            st.rerun()

    if pstate.get("writing_summative"):
        st.success(pstate["writing_summative"])

        if st.button("Show what happened next"):
            choices_summary = "\n".join(
                f"- {r['stimulus_title']}: "
                f"{'Option A — ' + r['optA'] if pstate['round_choices'].get(r['id'], {}).get('choice') == 'A' else 'Option B — ' + r['optB'] if pstate['round_choices'].get(r['id'], {}).get('choice') == 'B' else '—'}"
                for r in ROUNDS
            )
            prompt = f"""You are writing a short fictional follow-up about Jonas, a final-year
Business/Management student. Set six weeks after the events described.
Write it as a brief, warm, slightly wry personal update — as if a mutual friend is catching you up —
150-200 words, past tense.
Be specific — refer to the actual choices made below and show their realistic consequences.
Show real trade-offs. Not purely positive, not purely negative.
If the combination of choices was strategically weak, reflect that honestly but kindly.

JONAS'S BACKGROUND:
{OUTCOME_PROMPT_CONTEXT}

THE ADVICE HE WAS GIVEN AND FOLLOWED:
{choices_summary}"""
            with st.spinner("Writing the follow-up..."):
                outcome = call_claude(client, prompt, "Write the update now.", max_tokens=400)
            pstate["writing_outcome"] = outcome
            save_pairs(CLASS_NAME, pairs)
            st.rerun()

    if pstate.get("writing_outcome"):
        st.markdown("### What happened next")
        st.write(pstate["writing_outcome"])
