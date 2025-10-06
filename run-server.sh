#!/usr/bin/env bash
set -euo pipefail

# Helper: print header
log() { printf "\033[1;34m[dev]\033[0m %s\n" "$*"; }
warn() { printf "\033[1;33m[warn]\033[0m %s\n" "$*"; }
err() { printf "\033[1;31m[err]\033[0m %s\n" "$*"; }

# 0) Initialize rbenv if it's installed
if command -v rbenv >/dev/null 2>&1; then
  eval "$(rbenv init - bash)" || true
  log "Initialized rbenv: $(ruby -v)"
elif [[ -d "$HOME/.rbenv" ]]; then
  export PATH="$HOME/.rbenv/bin:$PATH"
  eval "$(rbenv init - bash)" || true
  log "Initialized rbenv from ~/.rbenv: $(ruby -v)"
fi

# 1) Basic Ruby check
if ! command -v ruby >/dev/null 2>&1; then
  err "Ruby is not installed. Please install Ruby (>= 3.1.0 recommended)."
  err "Suggested: rbenv (https://github.com/rbenv/rbenv) or rvm."
  exit 1
fi

# Check Ruby version
RUBY_VERSION=$(ruby -v | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
RUBY_MAJOR=$(echo "$RUBY_VERSION" | cut -d. -f1)
RUBY_MINOR=$(echo "$RUBY_VERSION" | cut -d. -f2)

if [[ "$RUBY_MAJOR" -lt 3 ]] || [[ "$RUBY_MAJOR" -eq 3 && "$RUBY_MINOR" -lt 1 ]]; then
  err "Ruby version $RUBY_VERSION is too old. This project requires Ruby >= 3.1.0"
  err "Current Ruby: $(which ruby)"
  err ""
  err "To install Ruby 3.2.2 with rbenv:"
  err "  rbenv install 3.2.2"
  err "  rbenv global 3.2.2"
  err "  rbenv rehash"
  err ""
  err "Then restart your terminal or run: source ~/.bash_profile"
  exit 1
fi

log "Using Ruby $RUBY_VERSION from $(which ruby)"

# 2) Ensure Bundler is available and matches Gemfile.lock (if present)
ensure_bundler() {
  local lock_ver=""
  if [[ -f Gemfile.lock ]]; then
    # Extract version under the `BUNDLED WITH` section
    lock_ver=$(awk '/BUNDLED WITH/{getline; gsub(/^ +| +$/,"", $0); print $0}' Gemfile.lock || true)
  fi

  if command -v bundle >/dev/null 2>&1; then
    local current_bundler=$(bundle --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' || echo "")
    if [[ -n "$lock_ver" && "$current_bundler" != "$lock_ver" ]]; then
      log "Installing Bundler ${lock_ver} to match Gemfile.lock..."
      gem install bundler:"${lock_ver}" --no-document
      rbenv rehash 2>/dev/null || true
    fi
  else
    log "Bundler not found; installing it."
    if [[ -n "$lock_ver" ]]; then
      log "Installing Bundler ${lock_ver} (from Gemfile.lock)..."
      gem install bundler:"${lock_ver}" --no-document || gem install bundler --no-document
    else
      gem install bundler --no-document
    fi
    rbenv rehash 2>/dev/null || true
  fi
}

ensure_bundler

# 3) Use local vendor/ bundle path for project dependencies
bundle config set --local path 'vendor/bundle'

# 4) Install gems
log "Installing gems (this may take a minute on first run)..."
if ! bundle install; then
  warn "Initial bundle install failed; attempting to update bundler and retry."
  bundle update --bundler || true
  bundle install
fi

# 5) Build then serve
log "Building site..."
bundle exec jekyll build

log "Starting server... (pass --drafts to include drafts)"
if [[ ${1:-} != "" ]]; then
  bundle exec jekyll serve "$@"
else
  bundle exec jekyll serve
fi

# Note: We intentionally do NOT modify your shell profile or require rbenv here.
