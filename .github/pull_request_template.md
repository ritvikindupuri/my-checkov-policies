## Summary

## Type of change

- [ ] New custom policy
- [ ] Change to an existing policy
- [ ] Tests or test fixtures only
- [ ] CI / tooling
- [ ] Documentation

## New or changed policy

| | |
|---|---|
| Check ID | `CKV_XM_AWS_{SERVICE}_{NUMBER}` |
| Resource types | |
| What it enforces | |

- [ ] The ID follows `CKV_XM_AWS_{SERVICE}_{NUMBER}` and is not already in use
- [ ] The ID does **not** use the `CKV2_` prefix — checkov reserves that for its own graph checks
- [ ] This is not already covered by a built-in checkov check <!-- a custom policy that duplicates a built-in one just double-reports -->
- [ ] Added a row to `checks/CHECKS.md` with a one-line summary and a link to the tests

### Fixtures and tests

- [ ] `test/resources/terraform/{service}/{check_name}/pass/` — both `main.tf` and `tfplan.json`
- [ ] `test/resources/terraform/{service}/{check_name}/fail/` — both `main.tf` and `tfplan.json`
- [ ] The fixture directory name matches the policy's YAML filename — CI fails the PR otherwise
- [ ] Test class at `test/terraform/{service}/test_{check_name}.py` covering pass and fail against
      both the Terraform runner and the Terraform plan runner

## Verification

- [ ] `pytest` passes locally
- [ ] Ran the new or changed check against a real target: `mcp -d <dir> --check <CHECK_ID>`

## Notes for the reviewer
