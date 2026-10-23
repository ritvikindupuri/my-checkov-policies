from pathlib import Path

from checkov.common.models.enums import CheckResult
from checkov.runner_filter import RunnerFilter
from checkov.terraform.runner import Runner
from checkov.terraform.plan_runner import Runner as TFPlanRunner

CHECKS_DIR = Path(__file__).parents[3] / "checks"
RESOURCES_DIR = Path(__file__).parents[2] / "resources" / "terraform" / "ecr" / "ensure_kms_encryption"


def _scan(tf_dir: Path, check_id: str) -> list[CheckResult]:
    runner = Runner()
    report = runner.run(
        root_folder=str(tf_dir),
        external_checks_dir=[str(CHECKS_DIR)],
        runner_filter=RunnerFilter(checks=[check_id]),
    )
    return [r.check_result["result"] for r in report.passed_checks + report.failed_checks]


def _scan_plan(plan_file: Path, check_id: str) -> list[CheckResult]:
    runner = TFPlanRunner()
    report = runner.run(
        files=[str(plan_file)],
        external_checks_dir=[str(CHECKS_DIR)],
        runner_filter=RunnerFilter(checks=[check_id]),
    )
    return [r.check_result["result"] for r in report.passed_checks + report.failed_checks]


def _scan_by_resource(tf_dir: Path, check_id: str) -> dict[str, CheckResult]:
    runner = Runner()
    report = runner.run(
        root_folder=str(tf_dir),
        external_checks_dir=[str(CHECKS_DIR)],
        runner_filter=RunnerFilter(checks=[check_id]),
    )
    return {r.resource: r.check_result["result"] for r in report.passed_checks + report.failed_checks}


def _scan_plan_by_resource(plan_file: Path, check_id: str) -> dict[str, CheckResult]:
    runner = TFPlanRunner()
    report = runner.run(
        files=[str(plan_file)],
        external_checks_dir=[str(CHECKS_DIR)],
        runner_filter=RunnerFilter(checks=[check_id]),
    )
    return {r.resource: r.check_result["result"] for r in report.passed_checks + report.failed_checks}


class TestEnsureKmsEncryption:
    """CKV_XM_AWS_ECR_42 — aws_ecr_repository must have encryption_configuration.encryption_type set to KMS."""

    CHECK_ID = "CKV_XM_AWS_ECR_42"

    def test_repository_with_kms_encryption_passes(self):
        results = _scan_by_resource(RESOURCES_DIR / "pass", self.CHECK_ID)
        assert results == {"aws_ecr_repository.pass": CheckResult.PASSED}

    def test_repository_non_compliant_cases_fail(self):
        results = _scan_by_resource(RESOURCES_DIR / "fail", self.CHECK_ID)
        assert len(results) == 3
        assert CheckResult.PASSED not in results.values()
        assert results["aws_ecr_repository.fail_aes256"] == CheckResult.FAILED
        assert results["aws_ecr_repository.fail_missing_encryption_config"] == CheckResult.FAILED
        assert results["aws_ecr_repository.fail_empty_encryption_config"] == CheckResult.FAILED

    def test_repository_with_kms_encryption_passes_plan(self):
        results = _scan_plan_by_resource(RESOURCES_DIR / "pass" / "tfplan.json", self.CHECK_ID)
        assert results == {"aws_ecr_repository.pass": CheckResult.PASSED}

    def test_repository_non_compliant_cases_fail_plan(self):
        results = _scan_plan_by_resource(RESOURCES_DIR / "fail" / "tfplan.json", self.CHECK_ID)
        assert len(results) == 3
        assert CheckResult.PASSED not in results.values()
        assert results["aws_ecr_repository.fail_aes256"] == CheckResult.FAILED
        assert results["aws_ecr_repository.fail_missing_encryption_config"] == CheckResult.FAILED
        assert results["aws_ecr_repository.fail_empty_encryption_config"] == CheckResult.FAILED

    def test_repository_inside_module_passes(self):
        results = _scan_by_resource(RESOURCES_DIR / "module", self.CHECK_ID)
        assert len(results) == 1
        assert list(results.values()) == [CheckResult.PASSED]
        assert any("aws_ecr_repository.module_repo" in k for k in results)

    def test_non_ecr_resources_ignored(self):
        # Confirms check does not inadvertently evaluate non-ECR resources if resource_types is modified
        results = _scan_by_resource(RESOURCES_DIR / "non_ecr", self.CHECK_ID)
        assert results == {}

    def test_unresolved_variable_drops_from_directory_scan(self):
        # Pins Checkov limitation: unresolved variables with no default drop out of directory scans
        results = _scan_by_resource(RESOURCES_DIR / "unresolved_var", self.CHECK_ID)
        assert results == {}
