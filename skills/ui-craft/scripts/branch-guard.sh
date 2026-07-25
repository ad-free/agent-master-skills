BRANCH="$(jq -r '.activeBranch / empty' .ui-craft/state.json)"
if [ -z "$BRANCH" ]; then
  BRANCH="<type>/<scope>-<short-description>"
  jq --arg b "$BRANCH" '.activeBranch = $b' .ui-craft/state.json > .ui-craft/state.tmp \
    && mv .ui-craft/state.tmp .ui-craft/state.json
fi

if git show-ref --verify --quiet "refs/$BRANCH"; then
  git checkout "$BRANCH"
elif [ "$(git branch --show-current)" = "$BRANCH" ]; then
  :
else
  git checkout -b "$BRANCH"
fi

CURRENT="$(git branch --show-current)"
case "$CURRENT" in
  main|master|develop) echo "ERROR: still on base branch $CURRENT"; exit 1 ;;
  "")                  echo "ERROR: detached HEAD"; exit 1 ;;
  "$BRANCH")           echo "OK: on $BRANCH" ;;
  *)                   echo "ERROR: on $CURRENT, expected $BRANCH"; exit 1 ;;
esac
