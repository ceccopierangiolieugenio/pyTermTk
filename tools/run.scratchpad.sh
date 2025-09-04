REPO="ceccopierangiolieugenio/pyTermTk"
WORKFLOW="_scratchpad.yml"
REF=$(git branch --show-current)
WORKFLOW_URL="https://github.com/$REPO/actions/workflows/$WORKFLOW"

curl -s -X POST \
-H "Accept: application/vnd.github+json" \
-H "Authorization: Bearer $GITHUB_TOKEN" \
"https://api.github.com/repos/$REPO/actions/workflows/$WORKFLOW/dispatches" \
-d "{\"ref\":\"$REF\"}"

echo "Scratchpad workflow triggered from branch $REF. You can monitor the progress here: $WORKFLOW_URL"