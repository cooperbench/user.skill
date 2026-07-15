#!/bin/bash
# SWESimBench v2 agentic verifier entrypoint.
set -uo pipefail
mkdir -p /logs/verifier
# Ensure python3 exists (base image is python:3.12-slim so it does).
python3 /tests/verify.py 2>&1 | tee /logs/verifier/verify.log
# verify.py writes /logs/verifier/reward.txt itself.
if [ ! -f /logs/verifier/reward.txt ]; then
  echo 0 > /logs/verifier/reward.txt
fi
exit 0
