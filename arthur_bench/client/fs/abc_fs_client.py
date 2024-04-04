import os
import uuid
from abc import ABC, abstractmethod, abstractstaticmethod
from datetime import datetime
from pathlib import Path
from typing import Optional, Union, List

from arthur_bench.models.models import PaginatedTestSuite, PaginatedRun


class ABCFSClient(ABC):

    @abstractmethod
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def get_test_suite_dir(self, test_suite_name: str) -> Path:
        raise NotImplementedError(
            "Calling an abstract method. Please use a concrete base class"
        )

    @abstractmethod
    def create_test_suite_dur(self, test_suite_name: str) -> Path:
        raise NotImplementedError(
            "Calling an abstract method. Please use a concrete base class"
        )

    @abstractmethod
    def create_run_dir(self, test_suite_name: str, run_name: str) -> Path:
        raise NotImplementedError(
            "Calling an abstract method. Please use a concrete base class"
        )

    @abstractmethod
    def get_suite_name_from_id(self, id: str) -> Optional[str]:
        raise NotImplementedError(
            "Calling an abstract method. Please use a concrete base class"
        )

    @abstractmethod
    def get_run_name_from_id(self, test_suite_name: str, id: str) -> Optional[str]:
        raise NotImplementedError(
            "Calling an abstract method. Please use a concrete base class"
        )

    @abstractmethod
    def update_suite_run_time(self, test_suite_name: str, runtime: datetime) -> None:
        raise NotImplementedError(
            "Calling an abstract method. Please use a concrete base class"
        )

    @abstractmethod
    def write_suite_index(self) -> None:
        raise NotImplementedError(
            "Calling an abstract method. Please use a concrete base class"
        )

    @abstractmethod
    def write_run_index(self, test_suite: str) -> None:
        raise NotImplementedError(
            "Calling an abstract method. Please use a concrete base class"
        )

    @staticmethod
    @abstractmethod
    def update_index(filepath: Path, id: uuid.UUID, name: str) -> None:
        raise NotImplementedError(
            "Calling an abstract method. Please use a concrete base class"
        )

    @abstractmethod
    def update_suite_index(self, id: uuid.UUID, name: str) -> None:
        raise NotImplementedError(
            "Calling an abstract method. Please use a concrete base class"
        )

    @abstractmethod
    def update_run_index(self, test_suite_name: str, id: uuid.UUID, name: str) -> None:
        raise NotImplementedError(
            "Calling an abstract method. Please use a concrete base class"
        )

    @abstractmethod
    def get_test_suite_by_name(self, test_suite_name: str) -> PaginatedTestSuite:
        raise NotImplementedError(
            "Calling an abstract method. Please use a concrete base class"
        )

    @staticmethod
    @abstractmethod
    def load_suite_with_optional_id(filepath: Union[str, os.PathLike]) -> Optional[PaginatedTestSuite]:
        raise NotImplementedError(
            "Calling an abstract method. Please use a concrete base class"
        )

    @abstractmethod
    def get_suite_files(self) -> List[str]:
        raise NotImplementedError(
            "Calling an abstract method. Please use a concrete base class"
        )

    @abstractmethod
    def get_run_files(self, test_suite_name: str) -> List[str]:
        raise NotImplementedError(
            "Calling an abstract method. Please use a concrete base class"
        )

    @abstractmethod
    def parse_paginated_test_suite(self, id: str) -> PaginatedTestSuite:
        raise NotImplementedError(
            "Calling an abstract method. Please use a concrete base class"
        )

    @abstractmethod
    def parse_paginated_test_run(self, test_suite_id: str, test_run_id: str) -> PaginatedRun:
        raise NotImplementedError(
            "Calling an abstract method. Please use a concrete base class"
        )

    @abstractmethod
    def write_suite_file(self, suite_dir: Path, test_suite: PaginatedTestSuite) -> None:
        raise NotImplementedError(
            "Calling an abstract method. Please use a concrete base class"
        )

    @abstractmethod
    def write_run_file(self, run_dir: Path, test_run: PaginatedRun) -> None:
        raise NotImplementedError(
            "Calling an abstract method. Please use a concrete base class"
        )
