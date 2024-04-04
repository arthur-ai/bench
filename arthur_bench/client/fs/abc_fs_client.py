import uuid
from abc import ABC, abstractmethod, abstractstaticmethod
from datetime import datetime
from pathlib import Path
from typing import Optional


class ABCFSClient(ABC):

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
