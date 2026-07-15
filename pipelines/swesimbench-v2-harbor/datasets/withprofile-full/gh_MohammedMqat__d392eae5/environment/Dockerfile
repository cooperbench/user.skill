FROM python:3.12-slim

# Non-root agent user (matches task.toml [agent] user = "agent")
RUN useradd --create-home --shell /bin/bash agent \
 && mkdir -p /sim && chown -R agent:agent /sim

WORKDIR /sim
COPY --chown=agent:agent sim/history.md /sim/history.md
COPY --chown=agent:agent sim/profile.md /sim/profile.md
# Seed an empty answer file the agent will overwrite.
RUN touch /sim/answer.txt && chown agent:agent /sim/answer.txt
