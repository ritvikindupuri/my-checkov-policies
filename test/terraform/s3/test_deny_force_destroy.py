from pathlib import Path

from checkov.common.models.enums import CheckResult
from checkov.runner_filter import RunnerFilter
from checkov.terraform.runner import Runner
from checkov.terraform.plan_runner import Runner as TFPlanRunner

CHECKS_DIR = Path(__file__).parents[3] / "checks"
RESOURCES_DIR = Path(__file__).parents[2] / "resources" / "terraform" / "s3" / "deny_force_destroy"


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


class TestS3DenyForceDestroy:
    """CKV_XM_AWS_S3_11 — aws_s3_bucket must not set force_destroy = true."""

    CHECK_ID = "CKV_XM_AWS_S3_11"

    def test_buckets_not_forcing_destroy_pass(self):
        results = _scan(RESOURCES_DIR / "pass", self.CHECK_ID)
        assert results == [CheckResult.PASSED, CheckResult.PASSED]

    def test_bucket_forcing_destroy_fails(self):
        results = _scan(RESOURCES_DIR / "fail", self.CHECK_ID)
        assert results == [CheckResult.FAILED]

    def test_buckets_not_forcing_destroy_pass_plan(self):
        results = _scan_plan(RESOURCES_DIR / "pass" / "tfplan.json", self.CHECK_ID)
        assert results == [CheckResult.PASSED, CheckResult.PASSED]

    def test_bucket_forcing_destroy_fails_plan(self):
        results = _scan_plan(RESOURCES_DIR / "fail" / "tfplan.json", self.CHECK_ID)
        assert results == [CheckResult.FAILED]
