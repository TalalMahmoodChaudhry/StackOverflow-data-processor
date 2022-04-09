FROM debian:11-slim AS build
RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes python3-venv gcc libpython3-dev && \
    python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip setuptools wheel

FROM build AS build-venv
COPY requirements.txt requirements.txt
RUN /venv/bin/pip install --disable-pip-version-check -r /requirements.txt

FROM gcr.io/distroless/python3-debian11
COPY --from=build-venv /venv /venv

WORKDIR /app/

COPY database/ database/
COPY input_data/ input_data/
COPY schemas/ schemas/
COPY constants.py .
COPY download_stacks.py .
COPY main.py .
COPY file_operations.py .
COPY import_helpers.py .
COPY logging_handlers.py .

ENTRYPOINT ["/venv/bin/python3", "-m", "main"]