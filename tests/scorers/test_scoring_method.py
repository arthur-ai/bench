import pytest
from typing import List, Optional
import sys
from unittest.mock import Mock, patch, MagicMock
from arthur_bench.scoring.scorer import Scorer
from arthur_bench.models.models import ScoringMethodType


class MockScorer(Scorer):
    def __init__(self, param_1="default_1", param_2: Optional[str] = None):
        self.param_1 = param_1
        self.param_2 = param_2
        self.param_3 = "param_3"
        self.non_json_param = Mock()
        if param_2 is not None:
            self.modify("test_4")

    def name():
        return "mock"

    def run_batch(
        self,
        candidate_batch: List[str],
        reference_batch: List[str] = None,
        input_text_batch: List[str] = None,
        context_batch: List[str] = None,
    ) -> List[float]:
        pass

    def modify(self, param_4):
        self.param_4 = param_4


@pytest.mark.parametrize(
    "args, expected_dict",
    [
        (
            ["test_1", "test_2"],
            {
                "param_1": "test_1",
                "param_2": "test_2",
                "param_3": "param_3",
                "param_4": "test_4",
            },
        ),
        ([], {"param_1": "default_1", "param_2": None, "param_3": "param_3"}),
    ],
)
def test_scorer_to_dict(args, expected_dict):
    scorer = MockScorer(*args)
    assert scorer.to_dict() == expected_dict


def test_scorer_from_dict():
    params = {
        "param_1": "test_1",
        "param_2": "test_2",
        "param_3": "param_3",
        "param_4": "test_4",
    }
    scorer = MockScorer.from_dict(params)
    assert scorer.param_1 == "test_1"
    assert scorer.param_2 == "test_2"

    scorer = MockScorer.from_dict({})
    assert scorer.param_1 == "default_1"
    assert scorer.param_2 == None


@pytest.mark.parametrize(
    "module_path,platform,expected_type",
    [
        (
            "/Users/bench_user/arthur_bench/scoring/exact_match.py",
            "darwin",
            ScoringMethodType.BuiltIn,
        ),
        (
            "/Users/bench_user/custom_dir/custom_scorer.py",
            "darwin",
            ScoringMethodType.Custom,
        ),
        (
            "C:\\Program Files\\Python311\\Lib\\site-packages\\arthur_bench\\scoring\\exact_match.py",
            "win32",
            ScoringMethodType.BuiltIn,
        ),
        (
            "C:\\Users\\bench_user\\custom_bench\\scoring\\exact_match.py",
            "win32",
            ScoringMethodType.Custom,
        ),
    ],
)
def test_scorer_type(module_path, platform, expected_type):
    if platform != sys.platform:
        return
    with patch(
        "arthur_bench.scoring.scorer.sys.modules", MagicMock()
    ) as module_mock:
        module_mock[MockScorer.__module__].__file__ = module_path
        scorer = MockScorer()
        assert scorer.type() == expected_type
