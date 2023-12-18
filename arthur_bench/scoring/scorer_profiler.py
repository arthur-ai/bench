import asyncio
from arthur_bench.scoring import Scorer
from openai import OpenAI, AsyncOpenAI

PROMPT = "Write me a 5 paragraph story"


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
        _ = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": PROMPT}],
            max_tokens=4000,
        )
        return None

    async def arun_batch(
        self,
        candidate_outputs=None,
        ref_batch=None,
        input_batch=None,
        context_batch=None,
    ):
        _ = await self.async_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": PROMPT,
                }
            ],
            model="gpt-3.5-turbo",
            max_tokes=4000,
        )
        return None


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

    return arun_time, mem_usage


if __name__ == "__main__":
    run_time, mem_usage = profile_run()
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(profile_arun())
