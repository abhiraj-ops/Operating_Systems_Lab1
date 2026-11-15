# =============================================================================
# Operating Systems Lab - build, run, test
# =============================================================================
# The container ships gcc, python3.10, make, gdb and strace, so every target
# below works identically inside and outside the dev container.
#
#   make            compile + run every lab
#   make build      compile the C labs
#   make run        run every lab, capturing the transcript in <lab>/output/
#   make test       pytest -q
#   make lint       flake8 (same checks as the GitHub workflow)
#   make clean      remove binaries and __pycache__
#
# Layout convention used by this repository:
#   <lab>/src/*.c|*.py   source
#   <lab>/output/        compiled binary + captured transcript
# The C labs are executed from inside <lab>/output/ so the files they create
# (process_output.txt, ...) land next to the other lab output.
# =============================================================================

CC     := gcc
CFLAGS := -std=c17 -Wall -Wextra -O2 -g -pthread
PYTHON := python3

LAB_DIRS := Lab1 Lab2 Lab3 Lab4 Capstone

C_SRCS  := $(sort $(foreach d,$(LAB_DIRS),$(wildcard $(d)/*/src/*.c)))
PY_SRCS := $(sort $(foreach d,$(LAB_DIRS),$(wildcard $(d)/*/src/*.py)))

.PHONY: all build run test lint clean list

all: build run

list:
	@echo "C labs:"
	@for s in $(C_SRCS);  do echo "  $$s"; done
	@echo "Python labs:"
	@for s in $(PY_SRCS); do echo "  $$s"; done

build:
	@for src in $(C_SRCS); do \
	  bin=$$(echo $$src | sed 's#/src/#/output/#; s#\.c$$##'); \
	  mkdir -p $$(dirname $$bin); \
	  $(CC) $(CFLAGS) -o $$bin $$src && echo "built $$bin"; \
	done

run: build
	@for src in $(C_SRCS); do \
	  bin=$$(echo $$src | sed 's#/src/#/output/#; s#\.c$$##'); \
	  out=$$(dirname $$bin)/terminal_output.txt; \
	  echo "=== $$bin ==="; \
	  ( cd $$(dirname $$bin) && ./$$(basename $$bin) 2>&1 ) | tee $$out; \
	done
	@for src in $(PY_SRCS); do \
	  lab=$$(dirname $$(dirname $$src)); \
	  out=$$lab/output/$$(basename $$src .py)_output.txt; \
	  echo "=== $$src ==="; \
	  mkdir -p $$(dirname $$out); \
	  $(PYTHON) $$src 2>&1 | tee $$out; \
	done

test:
	$(PYTHON) -m pytest -q

lint:
	$(PYTHON) -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	@$(PYTHON) -m flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

clean:
	@for src in $(C_SRCS); do \
	  bin=$$(echo $$src | sed 's#/src/#/output/#; s#\.c$$##'); \
	  rm -f $$bin; \
	done
	@find . -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true
	@find . -name '*.pyc' -delete 2>/dev/null || true
