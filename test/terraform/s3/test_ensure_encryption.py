from pathlib import Path

from checkov.common.models.enums import CheckResult
from checkov.runner_filter import RunnerFilter
from checkov.terraform.runner import Runner
from checkov.terraform.plan_runner import Runner as TFPlanRunner

CHECKS_DIR = Path(__file__).parents[3] / "checks"
RESOURCES_DIR = Path(__file__).parents[2] / "resources" / "terraform" / "s3" / "ensure_encryption"


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
    """Same as _scan, keyed by resource address — for fixtures with mixed results."""
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


class TestS3EnsureEncryption:
    """CKV_XM_AWS_S3_1 — aws_s3_bucket must have server-side encryption configured."""

    CHECK_ID = "CKV_XM_AWS_S3_1"

    def test_bucket_with_encryption_passes(self):
        results = _scan(RESOURCES_DIR / "pass", self.CHECK_ID)
        assert results == [CheckResult.PASSED]

    def test_bucket_without_encryption_fails(self):
        results = _scan(RESOURCES_DIR / "fail", self.CHECK_ID)
        assert results == [CheckResult.FAILED]

    def test_bucket_with_encryption_passes_plan(self):
        results = _scan_plan(RESOURCES_DIR / "pass" / "tfplan.json", self.CHECK_ID)
        assert results == [CheckResult.PASSED]

    def test_bucket_without_encryption_fails_plan(self):
        results = _scan_plan(RESOURCES_DIR / "fail" / "tfplan.json", self.CHECK_ID)
        assert results == [CheckResult.FAILED]

    # AWS provider v4+ moved encryption out of the bucket and into a separate
    # aws_s3_bucket_server_side_encryption_configuration resource. Both the bucket
    # and that resource are in the check's scope, hence two results.

    def test_bucket_with_separate_encryption_resource_passes(self):
        results = _scan(RESOURCES_DIR / "pass_separate_resource", self.CHECK_ID)
        assert results == [CheckResult.PASSED, CheckResult.PASSED]

    def test_bucket_with_separate_encryption_resource_passes_plan(self):
        results = _scan_plan(RESOURCES_DIR / "pass_separate_resource" / "tfplan.json", self.CHECK_ID)
        assert results == [CheckResult.PASSED, CheckResult.PASSED]

    def test_bucket_without_its_own_encryption_resource_fails(self):
        results = _scan_by_resource(RESOURCES_DIR / "fail_other_bucket_encrypted", self.CHECK_ID)
        assert results["aws_s3_bucket.unencrypted"] == CheckResult.FAILED
        assert results["aws_s3_bucket.encrypted"] == CheckResult.PASSED

    def test_bucket_without_its_own_encryption_resource_fails_plan(self):
        results = _scan_plan_by_resource(
            RESOURCES_DIR / "fail_other_bucket_encrypted" / "tfplan.json", self.CHECK_ID
        )
        assert results["aws_s3_bucket.unencrypted"] == CheckResult.FAILED
        assert results["aws_s3_bucket.encrypted"] == CheckResult.PASSED
