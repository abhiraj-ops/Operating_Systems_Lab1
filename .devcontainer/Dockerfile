# syntax=docker/dockerfile:1
# =============================================================================
# Operating Systems Lab - VS Code dev container (Ubuntu 22.04)
# =============================================================================
# Build context is the REPOSITORY ROOT:
#
#   docker build -t os-lab-dev -f .devcontainer/Dockerfile .
#
# Open the folder in VS Code and choose "Reopen in Container" to get a full
# Ubuntu workspace with gcc, Python 3.10 and every lab dependency ready.
# =============================================================================

FROM ubuntu:22.04

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# --- 1. Repositories --------------------------------------------------------
# The minimal ubuntu image ships the "main" component only; a couple of the
# lab utilities (gnuplot, ...) live in "universe", so it is enabled here.
RUN echo "deb http://archive.ubuntu.com/ubuntu jammy universe" \
        > /etc/apt/sources.list.d/universe.list \
    && apt-get update

# --- 2. Toolchain ------------------------------------------------------------
# build-essential   -> gcc / g++ / make for the C labs (fork, exec, threads, IPC)
# python3.10        -> the scheduling simulations and the pytest suite
# gdb / strace      -> for tracing syscalls, the way Lab 1 is about
# procps / psmisc   -> ps, kill, top for observing process state
# manpages          -> man 2 fork / man 2 pthread_mutex_*
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        curl \
        gdb \
        git \
        gnuplot \
        iproute2 \
        make \
        manpages \
        manpages-dev \
        net-tools \
        procps \
        psmisc \
        python3 \
        python3-pip \
        python3.10 \
        python3.10-dev \
        python3.10-venv \
        strace \
        sudo \
        time \
        unzip \
        vim \
        wget \
    && rm -rf /var/lib/apt/lists/*

# --- 2. Python tooling (lint + tests, same as the GitHub workflow) -----------
RUN pip3 install --no-cache-dir --upgrade pip \
    && pip3 install --no-cache-dir flake8 pytest \
    && rm -rf /root/.cache/pip

# --- 3. Non-root development user -------------------------------------------
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m -s /bin/bash $USERNAME \
    && echo "$USERNAME ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && mkdir -p /workspace \
    && chown -R $USERNAME:$USERNAME /workspace /home/$USERNAME

USER $USERNAME

WORKDIR /workspace
