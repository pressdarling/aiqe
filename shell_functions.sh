#!/bin/bash
# AI Query Enhancer Shell Functions

ai_ask() {
    local tool=${1:-claude}
    local mode=${2:-year-append}
    local query="${@:3}"

    if [ -z "$query" ]; then
        echo "Usage: ai_ask <tool> <mode> <query>"
        echo "Tools: claude, codex, gemini, cursor, copilot"
        echo "Modes: year-append, context-inject, tech-focus, au-context"
        return 1
    fi

    local script_dir="$(dirname "${BASH_SOURCE[0]}")"
    python3 "$script_dir/ai_query_enhancer.py" --tool "$tool" --mode "$mode" "$query"
}

# Specific tool shortcuts
claude_ask() {
    ai_ask claude year-append "$@"
}

codex_ask() {
    ai_ask codex tech-focus "$@"
}

gemini_ask() {
    ai_ask gemini tech-focus "$@"
}

# Australian context helper
au_ask() {
    ai_ask claude au-context "$@"
}
