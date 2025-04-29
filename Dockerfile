FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.12 \
    python3.12-venv \
    python3-pip \
    pipx \
    && rm -rf /var/lib/apt/lists/*

# Point python3 and python to python3.12
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.12 1 \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1

# Add pipx binaries to PATH and install hatch
ENV PATH="/root/.local/bin:$PATH"
RUN pipx install hatch && \
       ln -s /root/.local/bin/hatch /usr/local/bin/hatch

# Set working directory and copy files
WORKDIR /app
COPY pyproject.toml /app/
COPY src/examples /app/src/examples

# Set environment variables for hatch
ENV HATCH_ENV_TYPE_VIRTUAL_PATH=/opt/venv
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Create virtual environment using hatch
RUN hatch env create

# Use full path or adjust PATH again
CMD ["hatch", "run"]
