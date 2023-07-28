import uuid
from pathlib import Path
from typing import Optional
from arthur_bench.models.models import CreateRunRequest


class TestRun(CreateRunRequest):
    test_suite_id: Optional[uuid.UUID] = None
    run_dir: Optional[Path] = None

    def save(self):
        """Save a test run to local file system."""
        if self.run_dir is not None:
            run_file = self.run_dir / 'run.json'
            run_file.write_text(self.json(exclude={'test_suite_id', 'run_dir'}))

        # TODO: in client MR, update for if run dir is None
