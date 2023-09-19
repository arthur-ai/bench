import os

from arthur_bench.exceptions import UserValueError, MissingParameterError
from arthur_bench.client.bench_client import BenchClient
from arthur_bench.client.local import LocalBenchClient
from arthur_bench.client.rest import ArthurClient


def _get_bench_client() -> BenchClient:
    client: BenchClient
    use_remote = os.getenv("ARTHUR_BENCH_AUTOLOG", "false").lower() == "true"
    if use_remote:  # if remote url is specified use remote client
        try:
            client = ArthurClient().bench
        except (UserValueError, MissingParameterError) as e:
            raise UserValueError(
                f"You must provide authentication when using remote url: {e}"
            )
    else:
        client = LocalBenchClient()
    return client
