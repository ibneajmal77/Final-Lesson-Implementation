"""Prompt package for SupportOps AI Copilot."""

# ============================================================================
# FILE: packages/prompts/supportops_prompts/__init__.py
#
# A package marker — its presence makes this folder importable. Intentionally
# empty of code.
#
# WHAT A "PROMPT" IS: the written instructions sent to the AI alongside the
# ticket. Not a casual question — a carefully worded document telling the model
# what to do, which rules to follow, and exactly what JSON to return.
#
# THE IDEA THIS PACKAGE EXISTS TO ENFORCE: a prompt IS the program, as far as an
# AI feature is concerned. Change a sentence in it and every answer changes. So
# it deserves the same discipline as code — a name, a version, a declared output
# shape, and a changelog.
#
# The payoff is explainability. Every recommendation stores the prompt_version
# that produced it, so when approval rates drop next month, you can tell exactly
# which instructions were in effect rather than guessing at what changed.
#
# THE FILES:
#   registry.py  - the catalogue: which prompts exist, their versions, and which
#                  template file and output shape each uses
#   schemas.py   - the exact JSON shape the AI's answer must take, as Pydantic
#                  classes
#   templates/   - the prompt text itself, as versioned .md files
#
# THE NEATEST TRICK IN HERE: schemas.py is used TWICE for the same definition.
# registry.py converts a schema into a JSON description embedded in the prompt
# (so the model is told what to produce), and providers/hosted.py validates the
# reply against the same class (so the answer is checked). One definition used to
# ask and to check — they cannot drift apart.
#
# Note that six prompts are registered but only "full_ticket_analysis" is
# actually used. The other five are single-purpose prompts from an earlier design
# where each step ran separately; the contrast between the two approaches is
# explained in registry.py.
# ============================================================================
