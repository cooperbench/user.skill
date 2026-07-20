FROM python:3.12-slim

# Non-root agent user (matches task.toml [agent] user = "agent")
RUN useradd --create-home --shell /bin/bash agent \
 && mkdir -p /sim && chown -R agent:agent /sim

WORKDIR /sim
COPY history.md /sim/history.md
RUN chown -R agent:agent /sim/history.md
# Seed an empty answer file the agent will overwrite.
RUN touch /sim/answer.txt && chown agent:agent /sim/answer.txt
