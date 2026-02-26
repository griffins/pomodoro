FROM python:3.12-slim

# Install uv for fast Python package management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Prevent .pyc files and enable unbuffered output for real-time logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Use dummy SDL drivers so pygame initializes in a headless container
ENV SDL_VIDEODRIVER=dummy
ENV SDL_AUDIODRIVER=dummy

# Install system dependencies:
# - SDL2 libraries for pygame
# - VLC for audio playback (cvlc)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libsdl2-dev \
        libsdl2-mixer-dev \
        libsdl2-image-dev \
        libsdl2-ttf-dev \
        vlc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first to leverage Docker layer caching
COPY pyproject.toml uv.lock ./
COPY .python-version* ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source files
COPY pomodoro.py new_task.py sql_file.py config.py countdown_timer.py tone.py ./

# Copy sound files
COPY end-alarm-tone.mp3 start-alarm-tone.mp3 ./

# Copy test file
COPY test_pomodoro.py ./

# Run as non-root user for security
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

CMD ["python", "pomodoro.py", "-i"]
