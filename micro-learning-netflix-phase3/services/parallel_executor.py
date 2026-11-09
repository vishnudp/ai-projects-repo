# services/parallel_executor.py

from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed
)

from datetime import datetime

from config import MAX_WORKERS


def execute_task(func):

    start = datetime.now()

    try:

        output = func()

        status = "SUCCESS"

    except Exception as e:

        output = str(e)

        status = "FAILED"

    end = datetime.now()

    return {

        "output": output,

        "status": status,

        "start": start,

        "end": end,

        "duration": (
            end - start
        ).total_seconds()
    }


def run_parallel(tasks):

    overall_start = datetime.now()

    results = {}

    with ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    ) as executor:

        future_map = {

            executor.submit(
                execute_task,
                func
            ): name

            for name, func
            in tasks.items()
        }

        for future in as_completed(
            future_map
        ):

            task_name = future_map[
                future
            ]

            results[
                task_name
            ] = future.result()

    overall_end = datetime.now()

    total_time = (
        overall_end -
        overall_start
    ).total_seconds()

    return results, total_time