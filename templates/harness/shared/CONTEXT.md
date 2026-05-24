# Context

This file is the durable shared project context for both fixed operators.

## Project Summary

UNKNOWN

## Current Harness Posture

All runtime capabilities start as `UNVERIFIED`. H0 local smoke must run before
production work. H1 bootstrap restart smoke must prove that a fresh agent can
start from root files, run local checks, see feature state, and route into a
fixed operator role without hidden chat context.
