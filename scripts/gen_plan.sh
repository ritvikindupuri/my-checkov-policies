#!/usr/bin/env bash
#
# gen_plan.sh — generate a Terraform plan JSON for scanning with mcp or checkov
#
# Usage:
#   ./scripts/gen_plan.sh <terraform-dir> [output.json]
#
#   <terraform-dir>   path to a directory containing .tf files
#   [output.json]     where to write the JSON (default: <terraform-dir>/tfplan.json)
#
# Terraform init/plan artifacts (.terraform/, .terraform.lock.hcl) are kept in a
# temp directory and cleaned up automatically — nothing is written back to
# <terraform-dir> except the final JSON file.
#
# Scan the output:
#   mcp -f tfplan.json --file-type terraform_plan
#   checkov -f tfplan.json --file-type terraform_plan

set -euo pipefail

# ── helpers ──────────────────────────────────────────────────────────────────

usage() {
    echo "Usage: $(basename "$0") <terraform-dir> [output.json]"
    echo ""
    echo "  <terraform-dir>   directory containing .tf files"
    echo "  [output.json]     output path (default: <terraform-dir>/tfplan.json)"
    exit 1
}

step() { echo ""; echo "==> $*"; }

# ── validate inputs ───────────────────────────────────────────────────────────

[[ $# -lt 1 ]] && usage

if ! command -v terraform &>/dev/null; then
    echo "Error: terraform not found in PATH" >&2
    exit 1
fi

TERRAFORM_DIR="$(cd "$1" && pwd)"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Resolve output path relative to CWD so a relative second arg works as expected
if [[ -n "${2:-}" ]]; then
    OUTPUT_DIR="$(mkdir -p "$(dirname "$2")" && cd "$(dirname "$2")" && pwd)"
    OUTPUT_FILE="${OUTPUT_DIR}/$(basename "$2")"
else
    OUTPUT_FILE="${TERRAFORM_DIR}/tfplan.json"
fi

# ── temp workspace ────────────────────────────────────────────────────────────

WORK_DIR="$(mktemp -d)"
trap 'rm -rf "$WORK_DIR"' EXIT

# Copy .tf files from the source dir into the temp workspace
cp "${TERRAFORM_DIR}"/*.tf "${WORK_DIR}/" 2>/dev/null || true

# Inject a providers.tf (overrides any providers.tf in the source dir).
# A local scripts/providers.tf wins if you have one; otherwise fall back to the
# default below. Credentials are mock values passed via the environment so that
# `terraform plan` can run fully offline — nothing is ever authenticated or applied.
if [[ -f "${SCRIPT_DIR}/providers.tf" ]]; then
    cp "${SCRIPT_DIR}/providers.tf" "${WORK_DIR}/providers.tf"
else
    cat > "${WORK_DIR}/providers.tf" <<'EOF'
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region                      = "us-east-1"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
}
EOF
fi

# Satisfy the AWS provider without real credentials. Required even with the
# skip_* flags above, which only disable the pre-flight validation calls.
export AWS_ACCESS_KEY_ID="mock"
export AWS_SECRET_ACCESS_KEY="mock"
export AWS_DEFAULT_REGION="us-east-1"

# ── run ───────────────────────────────────────────────────────────────────────

echo "Source    : $TERRAFORM_DIR"
echo "Workspace : $WORK_DIR"
echo "Output    : $OUTPUT_FILE"

step "[1/3] terraform init"
terraform -chdir="$WORK_DIR" init \
    -backend=false \
    -input=false \
    -no-color

step "[2/3] terraform plan"
terraform -chdir="$WORK_DIR" plan \
    -out=".tfplan.bin" \
    -input=false \
    -no-color

step "[3/3] convert to JSON"
terraform -chdir="$WORK_DIR" show -json ".tfplan.bin" > "$OUTPUT_FILE"

# ── done ──────────────────────────────────────────────────────────────────────

echo ""
echo "Plan written to: $OUTPUT_FILE"
echo ""
echo "Scan with:"
echo "  mcp -f \"$OUTPUT_FILE\" --file-type terraform_plan"
echo "  checkov -f \"$OUTPUT_FILE\" --file-type terraform_plan"
