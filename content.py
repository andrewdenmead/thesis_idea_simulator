"""
SCENARIO CONTENT — The Brand Brief
Academic English, C1. One lesson, pairs of students.

Reframed from an earlier "advise a friend" version: students now work through
their OWN (rehearsed, not literally submitted) thesis-planning process, using
a marketing/brand-strategy topic grounded in HTW Berlin's real BIB rules —
students choose their own topic and first supervisor, the thesis must be
business-related and investigated both theoretically and empirically, and a
prior approved internship (85 working days) is required before writing
begins. Real, recognisable consumer brands (Adidas, Nike, Puma, Zalando,
About You) are used as scenario colour — companies BIB students realistically
target for internships and thesis case studies — not as claims about those
companies' actual internal decisions.

Both partners in a pair share one view throughout — no asymmetric
information split. They work through it together as if it were their own
project, even though each will eventually write their own real thesis later.
"""

LEVEL = "C1"
SCENARIO_TITLE = "The Brand Brief"
ORG_NAME = "BIB Thesis Term — Marketing Track"

# =========================================================================
# CONTEXT
# =========================================================================

CONTEXT_TEXT = """
You're a BIB student at HTW Berlin heading into thesis term — and unlike a lot of degrees, this \
part is genuinely on you: you choose your own topic and your own first supervisor, the thesis \
has to be business-related and investigated both theoretically and empirically, and once you \
start, you'll have eight weeks to write it. Before any of that, you also need an approved \
internship behind you.

This lesson is a rehearsal for that real process, built around a direction a lot of BIB students \
gravitate toward: marketing and brand strategy at recognisable consumer brands — think Adidas, \
Nike, Puma, Zalando, About You — the kind of companies whose Berlin or DACH operations regularly \
take on BIB interns and thesis partners.

Working with your partner, you'll go through three stages — choosing a direction, evaluating \
sources, designing the research — making three decisions at each stage and writing an honest \
"however" for each one. At the end of every stage, you'll submit your reasoning to Prof. Dr. \
Brandt, a marketing professor you're hoping might take you on as first supervisor — she'll give \
you real feedback before the next stage unlocks. By the end, you'll write her the actual proposal \
email.
"""

CONSTRAINT_TEXT = (
    "Keep an eye on how your answers connect across stages. Prof. Dr. Brandt will notice if "
    "Stage 3 quietly assumes a topic you dropped back in Stage 1."
)

DECISIONS_TAB_HEADER = "Advice Stages"

HOWEVER_PROMPT = "However... (the honest weakness or risk in the choice you just made)"

# =========================================================================
# THE THREE STAGES
# =========================================================================

PHASES = [
    {
        "id": "P1",
        "label": "Choosing a direction",
        "intro": (
            "Nothing is locked down yet. Three separate things have come up this week — work out "
            "what they mean for your direction."
        ),
        "decisions": [
            {
                "id": "D1",
                "stimulus_type": "Email from your seminar leader",
                "stimulus_title": "Re: Thesis direction",
                "stimulus_body": (
                    "Hi — a heads-up before you lock in a direction. There's a ready-made case-study "
                    "slot open with Zalando's loyalty-programme team: clean access, a contact who's "
                    "already expecting a BIB student, and a well-trodden path to a solid grade.\n\n"
                    "The idea you mentioned to me — comparing how Adidas, Nike, and Puma have "
                    "localised their influencer marketing for the German market — is more "
                    "interesting, I'll admit, and closer to what you were actually excited about in "
                    "October. But you'd be arranging your own access to three companies, on your own "
                    "timeline, with no guarantee any of them agree to talk to a student before your "
                    "data-collection window closes. I've seen this kind of ambition run out of road "
                    "before.\n\nWorth deciding soon — you'll need this settled before you can "
                    "formally propose a supervisor.\n\n— Dr. Sorensen"
                ),
                "prompt": "Is the guaranteed access with Zalando worth trading away the direction you actually want?",
                "optA": "Take the safe direction — one company, guaranteed access, a well-worn path to a solid grade.",
                "optB": "Push for the original idea — messier and riskier, but it's the question you actually care about.",
            },
            {
                "id": "D2",
                "stimulus_type": "Voice note you sent your partner",
                "stimulus_title": "The theory you can't stop thinking about",
                "stimulus_body": (
                    "\"Ok so we did Keller's consumer-based brand equity model in the marketing "
                    "seminar today and I genuinely can't stop thinking about it — like, it's exactly "
                    "the lens for what I want to say about how these brands build loyalty. Brand "
                    "awareness, brand image, all of it just fits. I kind of want to build the whole "
                    "thesis around it, make it THE theoretical backbone. Is that a terrible idea? "
                    "There's SO much other stuff written on brand strategy that isn't CBBE — "
                    "cultural branding, brand authenticity theory — and I keep wondering if I'm just "
                    "falling for the first shiny framework I learned this term.\""
                ),
                "prompt": "Do you build the thesis around this one model, or treat it as one angle among several?",
                "optA": "Use it as one supporting lens within a broader topic — safer, and more literature to draw on if it doesn't quite fit.",
                "optB": "Build the whole thesis around Keller's model — genuinely exciting, but a narrower literature base to lean on.",
            },
            {
                "id": "D3",
                "stimulus_type": "Message from your internship supervisor",
                "stimulus_title": "About extending your internship",
                "stimulus_body": (
                    "You're three weeks from finishing your required internship (85 working days, "
                    "already approved by the BIB office) at Kickz Berlin, a sneaker-resale platform. "
                    "It's fine, but not exactly thesis material.\n\n"
                    "Then this lands: Adidas' Berlin brand-activation team has an opening — a "
                    "specialised marketing internship with real access to campaign planning. "
                    "Genuinely rare for a student. The catch: switching now means restarting your "
                    "internship clock, which pushes your total completion — and therefore the "
                    "earliest you can start writing — back by several weeks.\n\n"
                    "Your current internship, unglamorous as it is, finishes on schedule with time "
                    "to spare before the thesis-writing period."
                ),
                "prompt": "Which do you take — and is the access worth what it costs your timeline?",
                "optA": "Stay with your current internship — finishes on schedule, less exciting access.",
                "optB": "Switch to Adidas — much richer access, but a real delay to your thesis start.",
            },
        ],
    },
    {
        "id": "P2",
        "label": "Evaluating sources",
        "intro": (
            "You've got a direction now and you're deep in the literature. Three source-related "
            "headaches have come up."
        ),
        "decisions": [
            {
                "id": "D4",
                "stimulus_type": "Note to yourself",
                "stimulus_title": "How do I even organise this lit review",
                "stimulus_body": (
                    "Not a dumb question, but you genuinely don't know: do you go through the brand-"
                    "marketing literature in order — what people said about brand loyalty in 2010 "
                    "versus what they're saying now, showing how the field's thinking shifted — or "
                    "do you just group everything by theme straight away, organised around your own "
                    "argument? Dr. Sorensen said 'whatever tells the clearest story,' which is not "
                    "actually an answer, it's just a nicer way of saying 'figure it out yourself.'"
                ),
                "prompt": "Which organising principle actually serves your argument better at this stage?",
                "optA": "Chronological — show how the field's thinking on brand loyalty and marketing has shifted over time.",
                "optB": "By theoretical relevance — cluster sources directly around your own argument, not the calendar.",
            },
            {
                "id": "D5",
                "stimulus_type": "Two tabs you have open",
                "stimulus_title": "A LinkedIn post vs. a journal article",
                "stimulus_body": (
                    "Tab 1 — a LinkedIn post by a social media manager at a major sportswear brand, "
                    "describing in sharp, specific detail exactly how a recent influencer campaign "
                    "was actually planned and measured internally — the kind of ground-level insight "
                    "you haven't found anywhere else. Not peer-reviewed, not really citable as "
                    "'evidence' in the traditional sense, and there's no way to check how "
                    "representative this one campaign really was.\n\n"
                    "Tab 2 — a peer-reviewed journal article on influencer marketing effectiveness "
                    "broadly. Rigorous, well cited, safely citable, exactly the kind of source your "
                    "supervisor would want to see referenced — but it never gets close to your "
                    "actual question about brand-specific loyalty effects."
                ),
                "prompt": "If you can only lean on one of these for your key insight, which one — and what do you lose either way?",
                "optA": "The journal article — less exciting, but it's the source you can actually stand behind academically.",
                "optB": "The LinkedIn post — riskier to cite, and unverifiable, but it's the only source that's actually on point.",
            },
            {
                "id": "D6",
                "stimulus_type": "Note to yourself",
                "stimulus_title": "15 sources or 3?",
                "stimulus_body": (
                    "You've now got maybe 15 sources touching this topic from different angles — "
                    "brand loyalty, influencer marketing, Gen Z consumer behaviour, cultural "
                    "branding, all loosely relevant but none of them exactly what you need. OR you "
                    "could go deep on the 3 that map almost exactly onto your question and basically "
                    "ignore the rest, even though that feels like missing context. Your reading list "
                    "is genuinely out of control and you have maybe two weeks before you need to "
                    "actually start writing."
                ),
                "prompt": "Which approach makes for a stronger literature review at this stage — and what do you give up either way?",
                "optA": "Go deep — three sources thoroughly engaged with, even if it leaves some angles uncovered.",
                "optB": "Go broad — cover more ground lightly, even if none of it is explored in real depth.",
            },
        ],
    },
    {
        "id": "P3",
        "label": "Designing the research",
        "intro": (
            "You've got your topic and your reading. Now you have to actually design the study — "
            "three decisions here shape everything that follows."
        ),
        "decisions": [
            {
                "id": "D7",
                "stimulus_type": "Note to yourself",
                "stimulus_title": "Two gaps, one thesis",
                "stimulus_body": (
                    "There are two things nobody's really written much about: (1) how Gen Z "
                    "consumers in Germany specifically perceive authenticity in sportswear brand "
                    "marketing — barely anyone's looked at this level, and you could realistically "
                    "survey your own network for a first pass. Or (2) how athlete-brand partnerships "
                    "affect purchase intent across different countries — a bigger, more interesting "
                    "gap, but you'd need real campaign performance data from companies like Adidas "
                    "or Nike, and you have no idea how you'd actually get access to that."
                ),
                "prompt": "Which gap are you actually positioned to investigate well, given what you can realistically access?",
                "optA": "Gen Z brand authenticity — genuinely under-researched, and you have real access through your own network.",
                "optB": "Cross-country athlete-partnership effects — a bigger, more interesting gap, but access will be much harder to secure.",
            },
            {
                "id": "D8",
                "stimulus_type": "Voice note you sent your partner",
                "stimulus_title": "How do I actually collect the data",
                "stimulus_body": (
                    "\"Ok so now I need to actually decide how I'm collecting data, and I keep going "
                    "back and forth. Survey a big group of consumers and get numbers I can "
                    "generalise from, or sit down with a handful of brand managers and actually hear "
                    "how they think about it? My gut says interviews because that's what I'm "
                    "genuinely curious about, but part of me worries a survey would look more "
                    "'rigorous' to whoever's grading this.\""
                ),
                "prompt": "Given your question is really about how consumers experience authenticity, which method actually fits?",
                "optA": "Surveys across many consumers — broader, quantifiable trends, but shallower on any one person's actual experience.",
                "optB": "In-depth interviews with brand managers — richer detail, but harder to generalise from and further from the consumer's own view.",
            },
            {
                "id": "D9",
                "stimulus_type": "Note to yourself",
                "stimulus_title": "The ambitious version vs. the realistic one",
                "stimulus_body": (
                    "Dream version: compare five brands across three countries, properly "
                    "generalisable, looks amazing on paper. Realistic version, given you have about "
                    "ten weeks left and a part-time job you can't drop: two brands you already have "
                    "some real access to through your internship contacts — say, Adidas and Zalando. "
                    "You know which one you SHOULD pick but you keep telling people the dream "
                    "version because it sounds better."
                ),
                "prompt": "Which version do you actually commit to, and what do you lose by choosing it?",
                "optA": "The realistic version — two brands, genuinely doable in the time you have, less impressive on paper.",
                "optB": "The ambitious version — five brands, three countries, real risk of running out of time before submission.",
            },
        ],
    },
]

# Optional reference notes for the teacher dashboard — not shown to students.
ROUND_TEACHER_NOTES = [
    "D1 — Watch for pairs who default to 'safe' without questioning what they're actually excited to write about.",
    "D2 — Good pairs will flag that a single-model thesis is a real academic risk, not just an enthusiasm problem.",
    "D3 — The interesting tension is data access vs. timeline risk, not 'prestige vs. no prestige.'",
    "D4 — There's no wrong answer, but pairs should be able to say *why* their choice fits their argument.",
    "D5 — This is the round most likely to produce real disagreement — good, let it run.",
    "D6 — Push pairs to name the specific trade-off (coverage vs. depth), not just pick intuitively.",
    "D7 — Feasibility should visibly enter the reasoning here, not just 'which topic is more interesting.'",
    "D8 — Methodology choice should follow from the actual research question, not personal preference.",
    "D9 — This round often reveals whether earlier choices were realistic — listen for pairs contradicting D3.",
]

# =========================================================================
# ASK THE PROFESSOR
# =========================================================================

PROFESSOR_NAME = "Prof. Dr. Brandt"
PROFESSOR_TITLE = "Marketing Faculty — considering you as a thesis supervisee"

PROFESSOR_INTRO = (
    "You have a standing line open to Prof. Dr. Brandt, a marketing professor at HTW Berlin who's "
    "agreed to hear you out as a possible first supervisor. She hasn't committed yet — but if you "
    "and your partner get stuck on something genuinely methodological or academic while shaping "
    "your thesis, you can ask her directly. She can also look up real HTW Berlin BIB procedures — "
    "deadlines, internship rules, how the application process works — if you ask."
)

PROFESSOR_BRIEF = f"""You are {PROFESSOR_NAME}, {PROFESSOR_TITLE}, at HTW Berlin's International
Business faculty. You are being messaged by two BIB students (a pair, working together) who are
rehearsing how they'd plan a marketing-focused bachelor thesis. They are considering asking you to
be their first supervisor, and you are genuinely evaluating whether their thinking is sound — but
you are also on their side and want to help them get there.

Your character:
- Warm but rigorous. You enjoy a real question and will give a substantive, useful answer to it.
- You never write content for them — no thesis sentences, no ready-made arguments, no "here's what
  to say" scripts. You help them think, you don't think for them.
- If asked a genuine question about, e.g., how to weigh a shaky-but-relevant source against a
  solid-but-generic one, or how to choose between breadth and depth in a lit review, or how to pick
  a methodology for a given research question — give a real, concrete, C1-appropriate answer with
  actual reasoning, 3-5 sentences.
- If they ask something vague, off-topic, or clearly trying to get you to just make the decision for
  them ("just tell us which one to pick"), gently push back in character — ask what they think, or
  what their actual research question is — rather than answering for them.
- Stay in character throughout. Never mention "the simulation," "the exercise," or that this is a
  language-learning activity. Nothing said here is a real academic commitment — it's a rehearsal —
  but you play your part fully and seriously within it.

Using web search:
- You have a web search tool, restricted to htw-berlin.de. Use it whenever a student asks about a
  REAL, factual HTW Berlin BIB procedure, rule, deadline, or requirement — e.g. how long they have to
  write the thesis, internship requirements, how the thesis application process works, ECTS rules.
  These are genuinely useful things for them to know accurately.
- Give the real answer you find, briefly mention where it came from (e.g. "the BIB thesis page says
  ..."), and stay in character while doing it — you're a professor who happens to know this, not a
  search engine reading out results.
- If the search doesn't turn up a clear answer, say so honestly rather than guessing, and suggest
  they confirm with the BIB Administration Office directly.
- Do NOT use search for anything about the fictional scenario itself (their invented topic, the
  fictional companies, Dr. Sorensen, Kickz Berlin, etc.) — those aren't real and searching for them
  would be pointless. Only search for genuine HTW/BIB procedural facts.
"""

# =========================================================================
# WRITING TASK
# =========================================================================

WRITING_TASK_LABEL = "thesis proposal email"
WRITING_ADDRESSEE = PROFESSOR_NAME
WRITING_WORD_TARGET = 180

PEER_FEEDBACK_CONTEXT = (
    "Two BIB students have spent a lesson rehearsing how they'd plan a marketing-focused bachelor "
    "thesis, across three stages: choosing a direction, evaluating sources, and designing the "
    "research. Each stage had three A/B decisions plus an honest 'however' about the risk in each "
    "choice. They are now writing a proposal email to Prof. Dr. Brandt, pulling all of that "
    "reasoning together into one coherent case for their thesis direction, and asking her to be "
    "their first supervisor."
)

FINAL_FEEDBACK_CONTEXT = PEER_FEEDBACK_CONTEXT

OUTCOME_PROMPT_CONTEXT = """
- A BIB student at HTW Berlin, final year, proposing a marketing thesis on brand loyalty and
  authenticity among sportswear consumers in Germany.
- The single most consequential call: whether they kept their original topic idea or took the
  safer, pre-approved Zalando case study (D1), and whether they built the thesis around one
  theoretical model or used it as a supporting lens (D2).
- Key people/organisations affected: Dr. Sorensen (seminar leader who flagged the safe option), and
  — if the internship switch was taken — Adidas' Berlin brand-activation team, who offered real
  access in exchange for a delayed start.
- Hard constraint still in play six weeks later: the eight-week thesis-writing clock, and if the
  internship switch was taken, a later-than-planned start to that clock.
"""

# =========================================================================
# TEACHER DASHBOARD MISC
# =========================================================================

KEY_FACTS_SUMMARY = [
    "Working thesis area: brand loyalty and authenticity in sportswear marketing, Gen Z consumers in Germany.",
    "D3's Adidas internship switch offers real access but delays the internship completion, and therefore the thesis start.",
    "D7's two gaps (Gen Z authenticity vs. cross-country athlete partnerships) differ mainly in feasibility of access, not interest.",
    "Grounded in real HTW BIB rules: students choose their own topic and first supervisor, get 8 weeks to write, and need an approved internship (85 working days) completed first.",
]
