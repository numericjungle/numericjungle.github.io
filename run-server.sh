#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Helper: print header
log() { printf "\033[1;34m[dev]\033[0m %s\n" "$*"; }
warn() { printf "\033[1;33m[warn]\033[0m %s\n" "$*"; }
err() { printf "\033[1;31m[err]\033[0m %s\n" "$*"; }

incremental_metadata_is_stale() {
  local metadata_file=".jekyll-metadata"
  [[ -f "$metadata_file" ]] || return 1

  if command -v strings >/dev/null 2>&1; then
    local metadata_dump
    metadata_dump="$(strings "$metadata_file" 2>/dev/null || true)"

    if grep -Eq '/(node_modules|scrapers|__pycache__)/|/package(-lock)?\.json|/run-server\.sh|/post\.sh|/new_post\.py|/convert_math_delimiters\.py|/tmp_rovodev_server_output\.log' <<<"$metadata_dump"; then
      return 0
    fi

    while IFS= read -r tracked_line; do
      [[ "$tracked_line" == *"$SCRIPT_DIR/"* ]] || continue
      local tracked_path="${tracked_line#*"$SCRIPT_DIR/"}"
      tracked_path="$SCRIPT_DIR/$tracked_path"
      [[ -e "$tracked_path" ]] || return 0
    done <<<"$metadata_dump"
  fi

  return 1
}

reset_incremental_state_if_needed() {
  if incremental_metadata_is_stale; then
    warn "Resetting stale Jekyll incremental metadata before starting the dev server."
    rm -f .jekyll-metadata
  fi
}

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

# 3) Use local vendor/ bundle path for project dependencies (skip if already set)
if ! bundle config get path 2>/dev/null | grep -q 'vendor/bundle'; then
  bundle config set --local path 'vendor/bundle'
fi

# 4) Install gems — skip if Gemfile.lock hasn't changed since last successful install
LOCK_HASH_FILE=".bundle/gemfile_lock_hash"
CURRENT_HASH=$(md5 -q Gemfile.lock 2>/dev/null || md5sum Gemfile.lock 2>/dev/null | cut -d' ' -f1)
CACHED_HASH=$(cat "$LOCK_HASH_FILE" 2>/dev/null || true)

if [[ "$CURRENT_HASH" != "$CACHED_HASH" ]]; then
  log "Gemfile.lock changed — installing gems..."
  if ! bundle install; then
    warn "Initial bundle install failed; attempting to update bundler and retry."
    bundle update --bundler || true
    bundle install
  fi
  echo "$CURRENT_HASH" > "$LOCK_HASH_FILE"
else
  log "Gems up to date (Gemfile.lock unchanged)."
fi

# 5) Script flags
prod_mode=false
serve_args=()
serve_arg_count=0

for arg in "$@"; do
  case "$arg" in
    --prod)
      prod_mode=true
      ;;
    *)
      serve_args+=("$arg")
      serve_arg_count=$((serve_arg_count + 1))
      ;;
  esac
done

if [[ "$prod_mode" == true ]]; then
  export JEKYLL_ENV=production

  filtered_serve_args=()
  filtered_serve_arg_count=0
  ignored_draft_flags=false
  if [[ "$serve_arg_count" -gt 0 ]]; then
    for arg in "${serve_args[@]}"; do
      case "$arg" in
        --drafts|-D)
          ignored_draft_flags=true
          ;;
        *)
          filtered_serve_args+=("$arg")
          filtered_serve_arg_count=$((filtered_serve_arg_count + 1))
          ;;
      esac
    done
  fi
  serve_args=()
  serve_arg_count=$filtered_serve_arg_count
  if [[ "$filtered_serve_arg_count" -gt 0 ]]; then
    serve_args=("${filtered_serve_args[@]}")
  fi

  log "Production mode enabled (JEKYLL_ENV=production). Drafts will be excluded."
  if [[ "$ignored_draft_flags" == true ]]; then
    warn "Ignoring draft flags because --prod was set."
  fi
fi

# 6) Serve (jekyll serve builds automatically on startup; --incremental skips unchanged files)
#
# In dev mode we exclude the large CIFAR-10/MNIST data dirs (127 MB) from the
# Jekyll build and symlink them into _site instead.  keep_files in _config_dev.yml
# tells Jekyll not to wipe those symlinks between builds.
CONFIG_ARG="_config.yml"
if [[ "$prod_mode" == false ]]; then
  CONFIG_ARG="_config.yml,_config_dev.yml"
  reset_incremental_state_if_needed

  # Pre-create symlinks so keep_files can preserve them through the build.
  for data_dir in convnetjs/demo/cifar10 convnetjs/demo/mnist; do
    link="_site/$data_dir"
    if [[ ! -e "$link" ]]; then
      mkdir -p "$(dirname "$link")"
      ln -sfn "$(pwd)/$data_dir" "$link"
      log "Symlinked large data dir: _site/$data_dir"
    fi
  done
fi

log "Starting server... (pass --drafts to include drafts, or --prod to exclude drafts)"
if [[ "$serve_arg_count" -gt 0 ]]; then
  bundle exec jekyll serve --incremental --config "$CONFIG_ARG" "${serve_args[@]}"
else
  bundle exec jekyll serve --incremental --config "$CONFIG_ARG"
fi

# Note: We intentionally do NOT modify your shell profile or require rbenv here.
