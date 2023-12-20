from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field, validator, root_validator


# COMMON


class ScoringMethodType(str, Enum):
    """
    Indicates whether the scoring method was provided by the package or a custom
    implementation
    """

    BuiltIn = "built_in"
    Custom = "custom"


class ScorerOutputType(str, Enum):
    """
    Indicates the output type of the scorer
    """

    Continuous = "continuous"
    Categorical = "categorical"


class Category(BaseModel):
    name: str
    description: Optional[str] = None


class ScoringMethod(BaseModel):
    """
    Scoring method configuration
    """

    name: str
    """
    Name of the scorer
    """
    type: ScoringMethodType
    """
    Whether the scoring method was bench default or custom implementation
    """
    config: dict = {}
    """
    Configuration as used by the scorer to_dict and from_dict methods
    """
    output_type: ScorerOutputType = ScorerOutputType.Continuous
    """
    Whether the scoring method returns categorical scores
    """
    categories: Optional[List[Category]] = None
    """
    Valid categories returned by the scorer. Only valid if categories is True.
    """

    @root_validator
    def scoring_method_categorical_defined(cls, values):
        output_type = values.get("output_type")
        categories = values.get("categories")
        if output_type == ScorerOutputType.Continuous:
            if categories is not None:
                raise ValueError(
                    "continuous scoring methods may not have categories defined"
                )

        else:
            if categories is None or len(categories) == 0:
                raise ValueError("categorical scorers must have categories defined")
        return values


# REQUESTS


class CommonSortEnum(str, Enum):
    NAME_ASC = "name"
    NAME_DESC = "-name"
    CREATED_AT_ASC = "created_at"
    CREATED_AT_DESC = "-created_at"


class TestSuiteSortEnum(str, Enum):
    LAST_RUNTIME_ASC = "last_run_time"
    LAST_RUNTIME_DESC = "-last_run_time"


class TestRunSortEnum(str, Enum):
    AVG_SCORE_ASC = "avg_score"
    AVG_SCORE_DESC = "-avg_score"


class TestCaseSortEnum(str, Enum):
    SCORE_ASC = "score"
    SCORE_DESC = "-score"


PaginationSuiteSortEnum = Union[CommonSortEnum, TestSuiteSortEnum]

PaginationRunSortEnum = Union[CommonSortEnum, TestRunSortEnum]

PaginationSortEnum = Union[
    TestCaseSortEnum, PaginationSuiteSortEnum, PaginationRunSortEnum
]


class TestCaseRequest(BaseModel):
    """
    An input, reference output pair.
    """

    input: str
    """
    Input to the test case. Does not include the prompt template.
    """
    reference_output: Optional[str]
    """
    Reference or "Golden" output for the given input.
    """


class TestSuiteRequest(BaseModel):
    """
    Test case data and metadata for the test suite.
    """

    name: str
    """
    Name of the test suite
    """
    description: Optional[str] = None
    """
    Optional description of the test suite
    """
    scoring_method: ScoringMethod
    """
    Scoring configuration to use as criteria for the test suite
    """
    test_cases: List[TestCaseRequest] = Field(..., min_items=1)
    """
    List of input texts and optional reference outputs to consistently score
    model generations against
    """

    @validator("test_cases")
    def null_reference_outputs_all_or_none(cls, v):
        """
        Validate that all or none of test case reference outputs are null
        """
        last_ref_output_null = None
        for tc in v:
            # get ref output value
            if isinstance(tc, TestCaseRequest):
                ref_val = tc.reference_output
            elif isinstance(tc, dict):
                ref_val = tc.get("reference_output", None)
            else:
                raise TypeError(
                    f"Unable to extract reference output value for type '{type(v)}'"
                )

            # check it matches what we've been seeing
            if ref_val is None and last_ref_output_null is False:
                raise ValueError(
                    "Test Suite has both null and non-null reference outputs. Reference"
                    " outputs for test cases within a suite should be all null or all"
                    " non-null."
                )
            if ref_val is not None and last_ref_output_null is True:
                raise ValueError(
                    "Test Suite has both null and non-null reference outputs. Reference"
                    " outputs for test cases within a suite should be all null or all"
                    " non-null."
                )
            if ref_val is None:
                last_ref_output_null = True
            else:
                last_ref_output_null = False

        return v

    @validator("scoring_method", pre=True)
    def scoring_method_backwards_compatible(cls, v):
        if isinstance(v, str):
            return ScoringMethod(name=v, type=ScoringMethodType.BuiltIn)
        return v


class ScoreResult(BaseModel):
    score: Optional[float] = None
    category: Optional[Category] = None

    @root_validator
    def contains_score(cls, values):
        if values.get("score") is None and values.get("category") is None:
            raise ValueError("at least one of score or category must be defined")
        return values


class TestCaseOutput(BaseModel):
    """
    A generated output, score pair
    """

    id: UUID
    """
    Optional unique identifier for this test case of the suite and run
    """
    output: str
    """
    Generated output for test case
    """
    score: Optional[float] = None
    """
    Score assigned to output. This field is decprecated, used score_result instead
    """
    score_result: ScoreResult
    """
    Score information about output. Contains float score and / or category description
    """

    @root_validator(pre=True)
    def score_result_backwards_compatible(cls, values):
        if values.get("score_result") is None:
            values["score_result"] = ScoreResult(score=values.get("score"))
        return values


class CreateRunRequest(BaseModel):
    name: str
    """
    Name identifier of the run
    """
    test_cases: List[TestCaseOutput] = Field(alias="test_case_outputs")
    """
    List of outputs and scores for all cases in the test suite
    """
    description: Optional[str] = None
    """
    Optional description of the run
    """
    model_name: Optional[str] = None
    """
    Optional model name identifying the model used to generate outputs
    """
    foundation_model: Optional[str] = None
    """
    Optional foundation model name identifiying the pretrained model used to generate
    outputs
    """
    prompt_template: Optional[str] = None
    """
    Optional prompt template name identifying the global prompt used to generate outputs
    """
    model_version: Optional[str] = None
    """
    Optional model version identifying the version of the model used to generate outputs
    """

    class Config:
        allow_population_by_field_name = True

    @validator("test_cases")
    def consistent_categories(cls, v):
        last_score_result_categorical = None
        for tc in v:
            if (
                tc.score_result.category is not None
                and last_score_result_categorical is False
            ) or (tc.score_result.category is None and last_score_result_categorical):
                raise ValueError(
                    "all score results must provide categories if any one does"
                )
            elif tc.score_result.category is None:
                last_score_result_categorical = False
            elif tc.score_result.category is not None:
                last_score_result_categorical = True
        return v


# RESPONSES


class TestSuiteMetadata(BaseModel):
    id: UUID
    name: str
    scoring_method: ScoringMethod
    last_run_time: Optional[datetime] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class PaginatedTestSuites(BaseModel):
    """
    Paginated list of test suites.
    """

    test_suites: List[TestSuiteMetadata]
    page: int
    page_size: int
    total_pages: int
    total_count: int


class TestCaseResponse(BaseModel):
    id: UUID
    input: str
    """
    Input to the test case. Does not include the prompt template.
    """
    reference_output: Optional[str] = None
    """
    Reference or "Golden" output for the given input.
    """


class PaginatedTestSuite(BaseModel):
    """
    Test suite and optional page information
    """

    id: UUID
    name: str
    scoring_method: ScoringMethod
    test_cases: List[TestCaseResponse]
    created_at: datetime
    updated_at: datetime
    description: Optional[str] = None
    last_run_time: Optional[datetime] = None
    num_runs: int = 0
    page: Optional[int] = None
    page_size: Optional[int] = None
    total_pages: Optional[int] = None
    total_count: Optional[int] = None


class TestRunMetadata(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime
    avg_score: Optional[float] = None
    model_version: Optional[str] = None
    prompt_template: Optional[str] = None


class PaginatedRuns(BaseModel):
    """
    Paginated list of runs for a test suite.
    """

    test_runs: List[TestRunMetadata]
    page: int
    page_size: int
    total_pages: int
    total_count: int


class HistogramItem(BaseModel):
    """
    Boundaries and count for a single bucket of a run histogram
    """

    count: int
    low: float
    high: float


class CategoricalHistogramItem(BaseModel):
    count: int
    category: Category


class SummaryItem(BaseModel):
    """
    Aggregate statistics for a single run: average score and score distribution
    """

    id: UUID
    name: str
    avg_score: float
    histogram: List[Union[HistogramItem, CategoricalHistogramItem]]

    @validator("histogram")
    def either_continuous_or_categorical(cls, v):
        """
        Validate that the items in the histogram list are all
        containing low/high floats or are all containing a category
        """
        both_error = (
            "Histogram has both low/high floats and category "
            "values, which is invalid."
        )
        is_categorical = isinstance(v[0], CategoricalHistogramItem)
        for h in v:
            if isinstance(h, CategoricalHistogramItem) and not is_categorical:
                raise ValueError(both_error)

            elif isinstance(h, HistogramItem) and is_categorical:
                raise ValueError(both_error)
        return v


class TestSuiteSummary(BaseModel):
    """
    Aggregate descriptions of runs of a test suite.
    Provides averages and score distributions
    """

    summary: List[SummaryItem]
    page: int
    page_size: int
    total_pages: int
    total_count: int
    num_test_cases: int
    categorical: bool = False


class CreateRunResponse(BaseModel):
    id: UUID


class RunResult(BaseModel):
    id: UUID
    output: str
    score: float  # deprecated
    input: Optional[str] = None
    reference_output: Optional[str] = None
    score_result: ScoreResult

    @root_validator(pre=True)
    def score_result_backwards_compatible(cls, values):
        if values.get("score_result") is None:
            values["score_result"] = ScoreResult(score=values.get("score"))
        return values


class PaginatedRun(BaseModel):
    """
    Paginated list of prompts, reference outputs, model outputs, and scores for a
    particular run.
    """

    id: UUID
    name: str
    test_suite_id: UUID
    test_cases: List[RunResult] = Field(alias="test_case_runs")
    updated_at: datetime
    created_at: datetime
    page: Optional[int] = None
    page_size: Optional[int] = None
    total_pages: Optional[int] = None
    total_count: Optional[int] = None

    class Config:
        allow_population_by_field_name = True
