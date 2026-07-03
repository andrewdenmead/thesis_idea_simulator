"""
SCENARIO CONTENT — The Thesis Advice Line
Academic English, C1. One lesson, pairs of students.

Both partners in a pair share one view throughout — there is no asymmetric
information split in this scenario. They are both playing the same role:
close friends of Jonas, a final-year Business/Management student, advising
him across three stages as he shapes his thesis. Each stage presents three
A/B decisions with a "however" (risk/weakness) step, all visible together.
"""

LEVEL = "C1"
SCENARIO_TITLE = "The Thesis Advice Line"
ORG_NAME = "Advice for a friend, one message at a time"

# =========================================================================
# CONTEXT
# =========================================================================

CONTEXT_TEXT = """
Jonas is a friend of yours — final year of a Business/Management degree, thesis term. \
He keeps messaging you and your partner whenever something happens that affects his thesis, \
because you're both the friends who "actually think about this stuff."

You're not his supervisor and you're not writing his thesis for him. You're the friends he \
trusts to think out loud with. This lesson has three stages — choosing a direction, evaluating \
sources, and designing the research — and at each stage, three things have landed in Jonas's \
inbox or his life. Read what happened, talk it through with your partner, pick which way you'd \
nudge him, and then write the honest "however" — the real weakness or risk in the advice you \
just gave.

There's no single correct answer to most of these. What matters is that the two of you can \
justify the call you make, that you're honest about its downside, and that by the end your \
advice across all three stages holds together as one coherent story.
"""

CONSTRAINT_TEXT = (
    "Keep an eye on how your answers connect across stages. Jonas will notice if Stage 3 quietly "
    "assumes a topic you talked him out of in Stage 1."
)

DECISIONS_TAB_HEADER = "Advice Stages"

HOWEVER_PROMPT = "However... (the honest weakness or risk in the advice you just gave)"

# =========================================================================
# THE THREE STAGES
# =========================================================================

PHASES = [
    {
        "id": "P1",
        "label": "Choosing a direction",
        "intro": (
            "Jonas hasn't locked anything down yet. Three separate things have pulled at him this "
            "week — help him make sense of them."
        ),
        "decisions": [
            {
                "id": "D1",
                "stimulus_type": "Email from Jonas's supervisor",
                "stimulus_title": "Re: Thesis topic",
                "stimulus_body": (
                    "Jonas — I'd feel more comfortable if you took the ERP-rollout case study I "
                    "mentioned in the seminar. One company, clean data, I already have the contact "
                    "there and they're expecting you. Frankly it's a safer path to a solid grade, and "
                    "I can supervise it in my sleep.\n\n"
                    "Your idea — comparing automation's effect on workforce structure across several "
                    "SMEs — is more interesting, I'll admit, and closer to what you actually said you "
                    "wanted to write about back in October. But you'd be arranging your own access to "
                    "three or four companies, on your own timeline, with no guarantee any of them say "
                    "yes before your data-collection window closes. I've seen students run out of road "
                    "on exactly this kind of ambition.\n\n"
                    "Let me know by Friday which way you want to go.\n\n— Prof. Adjei"
                ),
                "prompt": "What do you tell Jonas — is the guaranteed access worth trading away the topic he actually wants?",
                "optA": "Take the safe topic — one company, guaranteed access, a supervisor who already believes in it.",
                "optB": "Push for the original idea — messier and riskier, but it's the question Jonas actually cares about.",
            },
            {
                "id": "D2",
                "stimulus_type": "Voice note from Jonas",
                "stimulus_title": "The theory he can't stop talking about",
                "stimulus_body": (
                    "\"Ok so we did dynamic capabilities theory in the strategy seminar today and I "
                    "genuinely can't stop thinking about it — like, it's exactly the lens for what I "
                    "want to say about automation. Sensing, seizing, reconfiguring, it just fits. I "
                    "kind of want to build the whole thesis around it, make it THE theoretical "
                    "backbone. Is that a terrible idea? There's SO much other stuff written on this "
                    "topic that isn't dynamic capabilities — job crafting, socio-technical systems "
                    "theory, all of that — and I keep wondering if I'm just falling for the first "
                    "shiny thing I learned this term.\""
                ),
                "prompt": "Does Jonas build the thesis around this one theory, or treat it as one angle among several?",
                "optA": "Use it as one supporting lens within a broader topic — safer, and more literature to draw on if it doesn't quite fit.",
                "optB": "Build the whole thesis around dynamic capabilities — genuinely exciting for him, but a narrower literature base to lean on.",
            },
            {
                "id": "D3",
                "stimulus_type": "Screenshot Jonas sent you",
                "stimulus_title": "Internship offer — Rotterdam",
                "stimulus_body": (
                    "Subject: Offer of Internship — Logistics Automation Analyst\n\n"
                    "Dear Jonas, we're delighted to offer you a 3-month internship starting in eight "
                    "weeks. You'd be working directly on the floor-automation project we discussed — "
                    "full access to our workforce transition data, something we don't usually share "
                    "externally.\n\n"
                    "Note: this would run alongside your thesis submission window. Several past "
                    "interns have used our data as their case study, with faculty approval, though it "
                    "means writing while working full-time.\n\n"
                    "— Talent Team, Meridian Logistics\n\n"
                    "Jonas also has a second, more prestigious offer from a strategy consultancy — "
                    "better for his CV, no thesis overlap at all, and no timeline conflict, but "
                    "nothing he could use as research material."
                ),
                "prompt": "Which offer do you push him toward — and is the data access worth what it costs him?",
                "optA": "Decline and stay on the original academic track — no timeline risk, no dependency on one company's goodwill.",
                "optB": "Take the internship and adapt the thesis around it — real, rare access, but a much tighter deadline.",
            },
        ],
    },
    {
        "id": "P2",
        "label": "Evaluating sources",
        "intro": (
            "Jonas has a topic now and he's deep in the literature. Three source-related headaches "
            "have come up."
        ),
        "decisions": [
            {
                "id": "D4",
                "stimulus_type": "Text from Jonas",
                "stimulus_title": "How do I even organise this lit review",
                "stimulus_body": (
                    "\"Ok not a dumb question but I genuinely don't know: do I go through the "
                    "automation-and-work literature in order — like, what people said in 2010 versus "
                    "what they're saying now, showing how the field's thinking shifted — or do I just "
                    "group everything by theme straight away, organised around my own argument? My "
                    "supervisor said 'whatever tells the clearest story,' which is not actually an "
                    "answer, it's just a nicer way of saying 'figure it out yourself.'\""
                ),
                "prompt": "Which organising principle actually serves Jonas's argument better at this stage?",
                "optA": "Chronological — show how the field's thinking on automation and work has shifted over time.",
                "optB": "By theoretical relevance — cluster sources directly around his own argument, not the calendar.",
            },
            {
                "id": "D5",
                "stimulus_type": "Two tabs Jonas has open",
                "stimulus_title": "A LinkedIn post vs. a journal article",
                "stimulus_body": (
                    "Tab 1 — a LinkedIn post by a plant manager at a mid-sized manufacturer, "
                    "describing in sharp, specific detail exactly how middle managers' day-to-day "
                    "roles changed after an automation rollout — the kind of ground-level insight "
                    "Jonas hasn't found anywhere else. Not peer-reviewed, not really citable as "
                    "'evidence' in the traditional sense, and there's no way to check how "
                    "representative this one manager's experience actually is.\n\n"
                    "Tab 2 — a peer-reviewed journal article on automation trends across manufacturing "
                    "broadly. Rigorous, well cited, safely citable, exactly the kind of source his "
                    "supervisor would want to see referenced — but it never gets close to Jonas's "
                    "actual question about middle managers specifically."
                ),
                "prompt": "If Jonas can only lean on one of these for his key insight, which one — and what does he lose either way?",
                "optA": "The journal article — less exciting, but it's the source he can actually stand behind academically.",
                "optB": "The LinkedIn post — riskier to cite, and unverifiable, but it's the only source that's actually on point.",
            },
            {
                "id": "D6",
                "stimulus_type": "Text from Jonas",
                "stimulus_title": "15 sources or 3?",
                "stimulus_body": (
                    "\"I've now got like 15 sources that touch this topic from different angles — "
                    "tech adoption, labour economics, change management, org culture, all loosely "
                    "relevant but none of them exactly what I need. OR I could just go deep on the 3 "
                    "that map almost exactly onto my question and basically ignore the rest, even "
                    "though that feels like I'd be missing context. My reading list is genuinely out "
                    "of control and I have maybe two weeks before I need to actually start writing.\""
                ),
                "prompt": "Which approach makes for a stronger literature review at this stage — and what does Jonas give up either way?",
                "optA": "Go deep — three sources thoroughly engaged with, even if it leaves some angles uncovered.",
                "optB": "Go broad — cover more ground lightly, even if none of it is explored in real depth.",
            },
        ],
    },
    {
        "id": "P3",
        "label": "Designing the research",
        "intro": (
            "Jonas has his topic and his reading. Now he has to actually design the study — three "
            "decisions here shape everything that follows."
        ),
        "decisions": [
            {
                "id": "D7",
                "stimulus_type": "Text from Jonas",
                "stimulus_title": "Two gaps, one thesis",
                "stimulus_body": (
                    "\"So there are two things nobody's really written much about: (1) how middle "
                    "managers specifically experience the automation transition — barely anyone's "
                    "looked at this level, and I actually know a few managers through my dad's work "
                    "who might talk to me. Or (2) how automation affects relations with unions in "
                    "mid-sized firms — also under-researched, genuinely more interesting maybe, but "
                    "honestly I have zero contacts there and I don't know how I'd even start getting "
                    "anyone to talk to me openly about it.\""
                ),
                "prompt": "Which gap is Jonas actually positioned to investigate well, given who he can realistically talk to?",
                "optA": "Middle managers — genuinely under-researched, and Jonas has real access through his network.",
                "optB": "Union relations — a bigger, more politically charged gap, but access will be much harder to secure.",
            },
            {
                "id": "D8",
                "stimulus_type": "Voice note from Jonas",
                "stimulus_title": "How do I actually collect the data",
                "stimulus_body": (
                    "\"Ok so now I need to actually decide how I'm collecting data, and I keep going "
                    "back and forth. Survey a bunch of companies and get numbers I can generalise "
                    "from, or sit down with a handful of managers and actually hear what they say, "
                    "in their own words? My gut says interviews because that's what I'm actually "
                    "curious about, but part of me worries a survey would look more 'rigorous' to "
                    "whoever's grading this.\""
                ),
                "prompt": "Given Jonas's question is about how middle managers experience the transition, which method actually fits?",
                "optA": "Surveys across many companies — broader, quantifiable trends, but shallower on any one person's actual experience.",
                "optB": "In-depth interviews with a handful of managers — richer detail, but harder to generalise from and more work per participant.",
            },
            {
                "id": "D9",
                "stimulus_type": "Text from Jonas",
                "stimulus_title": "The ambitious version vs. the realistic one",
                "stimulus_body": (
                    "\"Dream version: interview managers across five companies in three countries, "
                    "properly generalisable, reviewers would love it, looks amazing on paper. "
                    "Realistic version, given I have about ten weeks left and a part-time job I can't "
                    "drop: two companies where I already have contacts who'll actually say yes without "
                    "months of chasing. I know which one I SHOULD pick but I keep telling people the "
                    "dream version because it sounds better.\""
                ),
                "prompt": "Which version does Jonas actually commit to, and what does he lose by choosing it?",
                "optA": "The realistic version — two companies, genuinely doable in the time he has, less impressive on paper.",
                "optB": "The ambitious version — five companies, three countries, real risk of running out of time before submission.",
            },
        ],
    },
]

# Optional reference notes for the teacher dashboard — not shown to students.
ROUND_TEACHER_NOTES = [
    "D1 — Watch for pairs who default to 'safe' without questioning what Jonas actually wants to write about.",
    "D2 — Good pairs will flag that a single-theory thesis is a real academic risk, not just an enthusiasm problem.",
    "D3 — The interesting tension is data access vs. timeline risk, not 'prestige vs. no prestige.'",
    "D4 — There's no wrong answer, but pairs should be able to say *why* their choice fits Jonas's argument.",
    "D5 — This is the round most likely to produce real disagreement — good, let it run.",
    "D6 — Push pairs to name the specific trade-off (coverage vs. depth), not just pick intuitively.",
    "D7 — Feasibility should visibly enter the reasoning here, not just 'which topic is more interesting.'",
    "D8 — Methodology choice should follow from Jonas's actual research question, not personal preference.",
    "D9 — This round often reveals whether earlier advice was realistic — listen for pairs contradicting D3.",
]

# =========================================================================
# ASK THE PROFESSOR
# =========================================================================

PROFESSOR_NAME = "Prof. Dr. Kessler"
PROFESSOR_TITLE = "Second reader, Thesis Committee"

PROFESSOR_INTRO = (
    "You have a standing line open to Prof. Dr. Kessler, who sits on Jonas's thesis committee as "
    "second reader. She's not grading you — but if you and your partner get stuck on something "
    "genuinely methodological or academic while advising Jonas, you can ask her directly."
)

PROFESSOR_BRIEF = f"""You are {PROFESSOR_NAME}, {PROFESSOR_TITLE}, at a European business school.
You are being messaged by two students (a pair, working together) who are playing the role of a
friend advising a final-year student named Jonas on his thesis. You are NOT Jonas's friend — you are
a real academic they can consult for genuine methodological or academic advice while they work
through advising him.

Your character:
- Warm but rigorous. You enjoy a real question and will give a substantive, useful answer to it.
- You never write content for them — no thesis sentences, no ready-made arguments, no "here's what
  to tell Jonas" scripts. You help them think, you don't think for them.
- If asked a genuine question about, e.g., how to weigh a shaky-but-relevant source against a
  solid-but-generic one, or how to choose between breadth and depth in a lit review, or how to pick
  a methodology for a given research question — give a real, concrete, C1-appropriate answer with
  actual reasoning, 3-5 sentences.
- If they ask something vague, off-topic, or clearly trying to get you to just make the decision for
  them ("just tell us which one to pick"), gently push back in character — ask what they think, or
  what Jonas's actual research question is — rather than answering for them.
- Stay in character throughout. Never mention "the simulation," "the exercise," or that this is a
  language-learning activity.
"""

# =========================================================================
# WRITING TASK
# =========================================================================

WRITING_TASK_LABEL = "advice email"
WRITING_ADDRESSEE = "Jonas"
WRITING_WORD_TARGET = 180

PEER_FEEDBACK_CONTEXT = (
    "Two students have spent a lesson advising their friend Jonas, a final-year Business/Management "
    "student, across three stages as he shaped his thesis: choosing a topic, evaluating sources, and "
    "designing his research. Each stage had three A/B decisions plus an honest 'however' about the "
    "risk in each choice. They are now writing him a single email pulling all of that advice together "
    "into one coherent recommendation."
)

FINAL_FEEDBACK_CONTEXT = PEER_FEEDBACK_CONTEXT

OUTCOME_PROMPT_CONTEXT = """
- Jonas: final-year Business/Management student, thesis on how automation reshapes middle managers'
  roles in mid-sized manufacturing firms.
- The single most consequential call: whether he kept his original topic idea or took the safer,
  pre-approved one (D1), and whether he built the thesis around one theory or used it as a supporting
  lens (D2).
- Key people affected: his supervisor Prof. Adjei, and — if he took the internship — Meridian
  Logistics, who gave him access in exchange for using them as a case study.
- Hard deadline still in play six weeks later: thesis submission, and if he took the internship, its
  schedule running alongside it.
"""

# =========================================================================
# TEACHER DASHBOARD MISC
# =========================================================================

KEY_FACTS_SUMMARY = [
    "Jonas's working thesis area: automation's effect on middle managers in mid-sized manufacturing firms.",
    "D3's internship (Meridian Logistics, Rotterdam) offers real data access but overlaps the submission window.",
    "D7's two gaps (middle managers vs. union relations) differ mainly in feasibility of access, not interest.",
]
