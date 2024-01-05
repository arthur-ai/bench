import asyncio
from typing import List, Optional, TypeVar, get_origin, get_args, Union
import concurrent.futures
import itertools
from arthur_bench.scoring import Scorer
from openai import OpenAI, AsyncOpenAI

PROMPT = "Write me a 5 paragraph story"
NUM_OUTPUTS = 100


class LLMCall(Scorer):
    def __init__(self):
        self.client = OpenAI(
            # Defaults to os.environ.get("OPENAI_API_KEY")
            # Otherwise use: api_key="Your_API_Key",
        )
        self.async_client = AsyncOpenAI()

    @staticmethod
    def name() -> str:
        return "llm_call_profile"

    def run_batch(
        self, candidate_outputs, ref_batch=None, input_batch=None, context_batch=None
    ):
        for _ in candidate_outputs:
            _ = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": PROMPT}],
                max_tokens=4000,
            )
        return ["" for _ in range(len(candidate_outputs))]

    async def arun_batch(
        self,
        candidate_outputs=None,
        ref_batch=None,
        input_batch=None,
        context_batch=None,
    ):
        for _ in candidate_outputs:
            _ = await self.async_client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": PROMPT,
                    }
                ],
                model="gpt-3.5-turbo",
                max_tokens=4000,
            )
        return ["" for _ in range(len(candidate_outputs))]

    def run_multiprocess(
        self,
        candidate_outputs: List[str],
        reference_outputs: Optional[List[str]] = None,
        inputs: Optional[List[str]] = None,
        contexts: Optional[List[str]] = None,
        batch_size: int = 5,
    ):
        all_scores = []
        input_batches = []
        ref_batches = []
        context_batches = []
        candidate_batches = []

        for i in range(0, len(candidate_outputs), batch_size):
            input_batch = (
                list(inputs[i : i + batch_size]) if inputs is not None else None
            )
            ref_batch = (
                list(reference_outputs[i : i + batch_size])
                if reference_outputs is not None
                else None
            )

            context_batch = None if contexts is None else contexts[i : i + batch_size]
            cand_batch = candidate_outputs[i : i + batch_size]
            input_batches.append(input_batch)
            ref_batches.append(ref_batch)
            context_batches.append(context_batch)
            candidate_batches.append(cand_batch)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            all_scores = executor.map(
                self.run_batch,
                candidate_batches,
                ref_batches,
                input_batches,
                context_batches,
            )
            # all_scores.extend(scores)  # type: ignore
            all_scores = list(itertools.chain.from_iterable(list(all_scores)))
        print(len(all_scores))
        return all_scores


def profile_run(candidate_outputs):
    import time
    import os
    import psutil

    process = psutil.Process(os.getpid())
    mem_info_before = process.memory_info()
    start_time = time.time()

    LLMCall().run(candidate_outputs)

    end_time = time.time()
    mem_info_after = process.memory_info()

    run_time = end_time - start_time
    mem_usage = mem_info_after.rss - mem_info_before.rss

    return run_time, mem_usage


async def profile_arun(candidate_outputs):
    import time
    import os
    import psutil

    process = psutil.Process(os.getpid())
    mem_info_before = process.memory_info()
    start_time = time.time()

    await LLMCall().arun(candidate_outputs)

    end_time = time.time()
    mem_info_after = process.memory_info()

    arun_time = end_time - start_time
    mem_usage = mem_info_after.rss - mem_info_before.rss
    print("num threads", len(process.threads()))

    return arun_time, mem_usage


def profile_threaded(candidate_outputs):
    import time
    import os
    import psutil

    process = psutil.Process(os.getpid())
    mem_info_before = process.memory_info()
    start_time = time.time()

    LLMCall().run_multiprocess(candidate_outputs)

    end_time = time.time()
    mem_info_after = process.memory_info()

    run_time = end_time - start_time
    mem_usage = mem_info_after.rss - mem_info_before.rss
    print("num threads", len(process.threads()))

    return run_time, mem_usage


if __name__ == "__main__":
    candidate_outputs = ["" for _ in range(NUM_OUTPUTS)]
    # run_time, mem_usage = profile_threaded(candidate_outputs)
    # print("run time 5 workers", run_time)
    # print("mem usage 5 workers", mem_usage)
    # run_time, mem_usage = profile_run(candidate_outputs)
    # print("run time", run_time)
    # print("mem usage", mem_usage)
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(profile_arun(candidate_outputs))
    print("async run time", result[0])
    print("async mem usage", result[1])
