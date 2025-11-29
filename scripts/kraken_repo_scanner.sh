#!/bin/bash
echo "=== Kraken Repo Scanner ==="
echo
echo "Scanning filesystem for Git repositories..."
echo

# Limit search paths to avoid crawling entire disk
SEARCH_PATHS=("/home" "/mnt" "/opt" "/srv")

REPO_FOUND=false

for BASE in "${SEARCH_PATHS[@]}"; do
    if [ -d "$BASE" ]; then
        while IFS= read -r -d '' gitdir; do
            REPO_FOUND=true
            REPO_PATH=$(dirname "$gitdir")

            echo "Found repository: $REPO_PATH"
            cd "$REPO_PATH" || continue

            BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)

            if ! git diff --quiet; then
                CHANGES="yes"
            else
                CHANGES="no"
            fi

            UNTRACKED=$(git ls-files --others --exclude-standard | wc -l)
            CONFLICTS=$(git diff --name-only --diff-filter=U | wc -l)
            LAST_COMMIT=$(git log -1 --pretty=format:"%cr" 2>/dev/null)

            git fsck --no-progress --no-reflog >/dev/null 2>&1
            if [ $? -eq 0 ]; then
                INTEGRITY="OK"
            else
                INTEGRITY="Issues detected"
            fi

            echo "  Branch: $BRANCH"
            echo "  Uncommitted changes: $CHANGES"
            echo "  Untracked files: $UNTRACKED"
            echo "  Merge conflicts: $CONFLICTS"
            echo "  Last commit: $LAST_COMMIT"
            echo "  Integrity: $INTEGRITY"
            echo

        done < <(find "$BASE" -type d -name ".git" -print0 2>/dev/null)
    fi
done

if [ "$REPO_FOUND" = false ]; then
    echo "Kraken sleeps. No Git repositories detected."
fi
