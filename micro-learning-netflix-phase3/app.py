import json
from pathlib import Path
from datetime import datetime

import pandas as pd
import streamlit as st

from services.vtt_parser import VTTParser
from services.chunker import create_chunks

from services.mini_summary_generator import (
    generate_mini_summary
)

from services.master_summary_generator import (
    generate_master_summary
)
from services.metadata_extractor import extract_metadata
from services.emotion_detector import detect_emotion
from services.knowledge_extractor import extract_knowledge
from services.learning_moment_extractor import (
    extract_learning_moments
)
from services.reel_candidate_generator import (
    generate_reel_candidate
)
from services.parallel_executor import run_parallel

from services.reel_cache import (
    load_reel,
    save_reel
)


from services.netflix_pipeline import (
    run_netflix_pipeline
)

from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed
)

from services.scene_builder import (
    build_scenes
)

from services.subtitle_generator import (
    build_word_subtitles
)

from services.image_generator import (
    generate_scene_images
)

from services.reel_renderer import (
    render_reel
)


from services.music_selector import (
    load_background_music
)

from services.broll_downloader import (
    download_brolls
)

from services.cover_generator import (
    create_cover_clip
)

# ----------------------------------
# CONFIG
# ----------------------------------

GENERATED_REELS_DIR = Path(
    "generated/reels"
)

GENERATED_REELS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# ----------------------------------
# PAGE
# ----------------------------------

st.set_page_config(
    page_title="Micro Content Generation",
    layout="wide"
)

st.title("🎬 Micro Content Generation")

st.markdown("---")

# ----------------------------------
# SESSION STATE
# ----------------------------------

if "pipeline_logs" not in st.session_state:
    st.session_state.pipeline_logs = []

# ----------------------------------
# HELPERS
# ----------------------------------

def run_stage(
    stage_name,
    func,
    *args
):
    """
    Generic stage runner
    """

    stage_start = datetime.now()

    output = func(*args)

    stage_end = datetime.now()

    duration = (
        stage_end -
        stage_start
    ).total_seconds()

    return {
        "output": output,
        "start": stage_start,
        "end": stage_end,
        "duration": duration
    }


# ----------------------------------
# UPLOAD
# ----------------------------------

uploaded_file = st.file_uploader(
    "Upload VTT File",
    type=["vtt"]
)

if uploaded_file:

    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)

    vtt_path = upload_dir / uploaded_file.name

    with open(vtt_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"Uploaded: {uploaded_file.name}")

    parser = VTTParser()

    transcript = parser.parse(str(vtt_path))

    chunks = create_chunks(
        transcript,
        chunk_size=600
    )

    st.info(
        f"Total Chunks Created: {len(chunks)}"
    )

    st.subheader("📚 Chunk Preview")

    for idx, chunk in enumerate(chunks):

        chunk_start = chunk[0]["start"]

        chunk_end = chunk[-1]["end"]

        chunk_text = " ".join(
            [
                item["text"]
                for item in chunk[:5]
            ]
        )

        with st.expander(
            f"Chunk {idx+1} | {chunk_start} → {chunk_end}"
        ):

            st.write(
                f"Entries: {len(chunk)}"
            )

            st.write(
                chunk_text[:1000]
            )

    st.markdown("---")

    if st.button("🚀 Generate Reel Candidates"):

        pipeline_start = datetime.now()

        total_chunks = len(chunks)

        overall_progress = st.progress(0)

        status_box = st.empty()

        pipeline_logs = []

        for idx, chunk in enumerate(chunks):

            chunk_no = idx + 1

            chunk_start = datetime.now()

            cached_reel = load_reel(chunk_no)

            if cached_reel:

                st.success(
                    f"✅ Reel {chunk_no} loaded from cache"
                )

                with st.expander(
                    f"Cached Reel {chunk_no}",
                    expanded=False
                ):
                    st.json(cached_reel)

                continue

            st.markdown(
                f"""
                ## 🎞 Chunk {chunk_no}/{total_chunks}
                """
            )

            chunk_container = st.container()

            with chunk_container:

                text = " ".join(
                    [
                        x["text"]
                        for x in chunk
                    ]
                )

                stage_progress = st.progress(0)

                print(f"Chunk text length: {len(text)}")

                status_box.info(
                    f"""
                    Chunk {chunk_no}/{total_chunks}

                    Running Parallel Analysis...
                    """
                )

                # summary_result = run_stage(
                #     "Summary",
                #     generate_summary,
                #     text
                # )

                # pipeline_logs.append({

                #     "Chunk":
                #         chunk_no,

                #     "Stage":
                #         "summary",

                #     "Started":
                #         summary_result["start"].strftime(
                #             "%H:%M:%S"
                #         ),

                #     "Ended":
                #         summary_result["end"].strftime(
                #             "%H:%M:%S"
                #         ),

                #     "Duration(s)":
                #         round(
                #             summary_result["duration"],
                #             2
                #         ),

                #     "Status":
                #         "SUCCESS"
                # })

                # summary_output = summary_result[
                #     "output"
                # ]

                # with st.expander(
                #     "📄 Summary",
                #     expanded=True
                # ):
                #     st.write(summary_output)

                # ----------------------------------
                # MINI SUMMARIES
                # ----------------------------------

                MAX_SUMMARY_CHARS = 700

                sub_chunks = [

                    text[i:i + MAX_SUMMARY_CHARS]

                    for i in range(
                        0,
                        len(text),
                        MAX_SUMMARY_CHARS
                    )
                ]

                st.info(
                    f"Creating {len(sub_chunks)} mini summaries..."
                )

                summary_tasks = {}

                for i, sub_chunk in enumerate(
                    sub_chunks
                ):

                    summary_tasks[
                        f"mini_summary_{i+1}"
                    ] = lambda c=sub_chunk: (
                        generate_mini_summary(c)
                    )

                mini_results, mini_time = run_parallel(
                    summary_tasks
                )
                

                mini_summary_objects = []

                for stage_name, result in (
                    mini_results.items()
                ):

                    pipeline_logs.append({

                        "Chunk": chunk_no,
                        "Stage": stage_name,
                        "Started": result["start"].strftime("%H:%M:%S"),
                        "Ended": result["end"].strftime("%H:%M:%S"),
                        "Duration(s)": round(result["duration"], 2),
                        "Status": "SUCCESS"
                    })

                    mini_summary_objects.append(
                        result["output"]
                    )

                    with st.expander(
                        stage_name,
                        expanded=False
                    ):
                        st.write(
                            result["output"]
                        )

                

                master_result = run_stage(

                    "master_summary",

                    generate_master_summary,

                    json.dumps(
                        mini_summary_objects,
                        indent=2,
                        ensure_ascii=False
                    )
                )

                summary_output = (
                    master_result["output"]
                )

                pipeline_logs.append({

                    "Chunk":
                        chunk_no,

                    "Stage":
                        "master_summary",

                    "Started":
                        master_result["start"].strftime(
                            "%H:%M:%S"
                        ),

                    "Ended":
                        master_result["end"].strftime(
                            "%H:%M:%S"
                        ),

                    "Duration(s)":
                        round(
                            master_result["duration"],
                            2
                        ),

                    "Status":
                        "SUCCESS"
                })

                with st.expander(
                    "📘 Master Summary",
                    expanded=True
                ):
                    st.write(
                        summary_output
                    )

                tasks = {

                    "metadata":
                        lambda:
                            extract_metadata(
                                summary_output
                            ),

                    "emotion":
                        lambda:
                            detect_emotion(
                                summary_output
                            ),

                    "knowledge":
                        lambda:
                            extract_knowledge(
                                summary_output
                            ),

                    "learning":
                        lambda:
                            extract_learning_moments(
                                summary_output
                            )
                }

                parallel_results, parallel_time = run_parallel(
                    tasks
                )

                stage_progress.progress(20)   # mini summaries done

                stage_progress.progress(40)   # master summary done

                stage_progress.progress(70)   # metadata/emotion/etc done

                stage_progress.progress(100)  # reel candidate done

                st.success(
                    f"""
                    Parallel Analysis Complete

                    Time:
                    {parallel_time:.2f} sec
                    """
                )

                chunk_results = {}

                chunk_results["summary"] = (
                    summary_output
                )


                for stage_name, result in parallel_results.items():

                    status_box.info(
                        f"""
                        Chunk {chunk_no}/{total_chunks}

                        Generating Reel Candidate...
                        """
                    )
               
                    chunk_results[
                        stage_name
                    ] = result["output"]

                    pipeline_logs.append({

                        "Chunk":
                            chunk_no,

                        "Stage":
                            stage_name,

                        "Started":
                            result["start"].strftime(
                                "%H:%M:%S"
                            ),

                        "Ended":
                            result["end"].strftime(
                                "%H:%M:%S"
                            ),

                        "Duration(s)":
                            round(
                                result["duration"],
                                2
                            ),

                        "Status":
                              "SUCCESS"
                    })

                    with st.expander(
                        f"📄 {stage_name.title()} Output",
                        expanded=False
                    ):

                        st.write(
                            result["output"]
                        )

                status_box.info(
                    f"""
                    Chunk {chunk_no}/{total_chunks}

                    Generating Reel Candidate...
                    """
                )

                reel_context = json.dumps({

                    "summary":
                        summary_output,

                    "metadata":
                        parallel_results[
                            "metadata"
                        ]["output"],

                    "emotion":
                        parallel_results[
                            "emotion"
                        ]["output"],

                    "knowledge":
                        parallel_results[
                            "knowledge"
                        ]["output"],

                    "learning":
                        parallel_results[
                            "learning"
                        ]["output"]

                }, indent=2)

                reel_result = run_stage(

                    "Reel Candidate",

                    generate_reel_candidate,

                    reel_context
                )

                pipeline_logs.append({

                    "Chunk":
                        chunk_no,

                    "Stage":
                        "reel_candidate",

                    "Started":
                        reel_result["start"].strftime(
                            "%H:%M:%S"
                        ),

                    "Ended":
                        reel_result["end"].strftime(
                            "%H:%M:%S"
                        ),

                    "Duration(s)":
                        round(
                            reel_result["duration"],
                            2
                        ),

                    "Status":
                        "SUCCESS"
                })

                with st.expander(
                    "🎥 Reel Candidate",
                    expanded=True
                ):
                    st.write(
                        reel_result["output"]
                    )

                chunk_results["reel"] = (
                    reel_result["output"]
                )


                # ----------------------------------
                # SAVE REEL JSON
                # ----------------------------------

                reel_path = (
                    GENERATED_REELS_DIR
                    /
                    f"reel_{chunk_no}.json"
                )

                with open(
                    reel_path,
                    "w"
                ) as f:

                    output_data = {
                        "chunk_number":
                            chunk_no,

                        "mini_summaries": mini_summary_objects,

                        "start_time":
                            chunk[0][
                                "start_seconds"
                            ],

                        "end_time":
                            chunk[-1][
                                "end_seconds"
                            ],

                        "duration":
                            (
                                chunk[-1]["end_seconds"]
                                -
                                chunk[0]["start_seconds"]
                            ),
                        "summary":
                            chunk_results["summary"],

                        "metadata":
                            chunk_results["metadata"],

                        "emotion":
                            chunk_results["emotion"],

                        "knowledge":
                            chunk_results["knowledge"],

                        "learning":
                            chunk_results["learning"],

                        "reel":
                            chunk_results["reel"],
                    }

                    json.dump(
                        output_data,
                        f,
                        indent=2,
                        ensure_ascii=False
                    )

                    save_reel(
                        chunk_no,
                        output_data
                    )

                chunk_duration = (
                    datetime.now()
                    -
                    chunk_start
                ).total_seconds()

                st.success(
                    f"""
                    ✅ Chunk {chunk_no}
                    Completed

                    Duration:
                    {chunk_duration:.2f} sec

                    Saved:
                    {reel_path}
                    """
                )

            overall_progress.progress(
                chunk_no
                /
                total_chunks
            )

            st.markdown("---")

        pipeline_time = (
            datetime.now()
            -
            pipeline_start
        ).total_seconds()

        status_box.success(
            "🎉 All Chunks Processed"
        )

        st.markdown("## 📊 Pipeline Summary")

        df = pd.DataFrame(
            pipeline_logs
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        st.metric(
            "Total Processing Time",
            f"{pipeline_time:.2f} sec"
        )

        st.success(
            f"""
            Finished Processing

            Total Chunks:
            {total_chunks}

            Reel JSON Saved To:
            generated/reels/
            """
        )

st.markdown("---")

st.subheader(
    "🎬 Phase 2 - Content Director Layer"
)

if st.button(
    "Generate Content Storyboards"
):

    reel_files = sorted(
        Path(
            "generated/reels"
        ).glob(
            "reel_*.json"
        )
    )

    if not reel_files:

        st.error(
            "No reel JSON files found."
        )

    else:

        progress = st.progress(0)

        status_box = st.empty()

        table_box = st.empty()

        results = []

        total = len(reel_files)

        status_data = []

        for reel_file in reel_files:

            status_data.append({
                "file": reel_file.name,
                "status": "Queued"
            })

        table_box.dataframe(
            pd.DataFrame(status_data),
            use_container_width=True
        )

        with ThreadPoolExecutor(
            max_workers=4
        ) as executor:

            futures = {}

            for reel_file in reel_files:

                future = executor.submit(
                    run_netflix_pipeline,
                    reel_file
                )

                futures[future] = reel_file

                for row in status_data:

                    if row["file"] == reel_file.name:

                        row["status"] = "Running"

                table_box.dataframe(
                    pd.DataFrame(status_data),
                    use_container_width=True
                )

            completed = 0

            for future in as_completed(futures):

                reel_file = futures[future]

                try:

                    result = future.result()

                    results.append(result)

                    completed += 1

                    progress.progress(
                        completed / total
                    )

                    for row in status_data:

                        if row["file"] == reel_file.name:

                            row["status"] = "Completed"

                    table_box.dataframe(
                        pd.DataFrame(status_data),
                        use_container_width=True
                    )

                    status_box.success(
                        f"""
        Completed:
        {completed}/{total}

        Latest:
        {reel_file.name}
        """
                    )

                except Exception as e:

                    for row in status_data:

                        if row["file"] == reel_file.name:

                            row["status"] = f"Failed: {str(e)}"

                    table_box.dataframe(
                        pd.DataFrame(status_data),
                        use_container_width=True
                    )

                    st.error(
                        f"""
        Failed:
        {reel_file.name}

        Error:
        {e}
        """
                    )

st.markdown("---")

st.subheader(
    "🎥 Phase 3 - Video Engine"
)

if st.button(
    "Generate  Videos"
):
    download_brolls()

    netflix_files = sorted(
        Path(
            "generated/netflix"
        ).glob(
            "reel_*_netflix.json"
        )
    )

    if not netflix_files:

        st.error(
            "No  JSON files found."
        )

    else:

        total = len(
            netflix_files
        )

        progress = st.progress(0)

        status_box = st.empty()

        table_box = st.empty()

        rows = []

        for file in netflix_files:

            rows.append({
                "file": file.name,
                "status": "Queued"
            })

        table_box.dataframe(
            pd.DataFrame(rows),
            use_container_width=True
        )

        completed = 0

        for idx, netflix_file in enumerate(
            netflix_files
        ):

            status_box.info(
                f"""
            Generating Assets

            Images
            +
            Narration
            +
            Video

            {idx+1}/{total}

            {netflix_file.name}
            """
            )

            try:

                for row in rows:

                    if row["file"] == netflix_file.name:

                        row["status"] = "Loading"

                table_box.dataframe(
                    pd.DataFrame(rows),
                    use_container_width=True
                )

                with open(
                    netflix_file,
                    "r"
                ) as f:

                    netflix_json = json.load(f)

                status_box.info(
                    f"""
Building scenes

{netflix_file.name}
"""
                )
                with open(netflix_file, "r") as f:
                    netflix_json = json.load(f)

                scenes = build_scenes(
                    netflix_json
                )

                if not scenes:

                    raise Exception(
                        f"No scenes generated from "
                        f"{netflix_file.name}"
                    )

                st.write(
                    f"Scenes Generated: {len(scenes)}"
                )
              
                # -----------------------
                # SUBTITLES
                # -----------------------

                # subtitles = build_subtitles(
                #     scenes
                # )

                # -----------------------
                # RENDER
                # -----------------------

                output_path = (
                    Path(
                        "generated/videos"
                    )
                    /
                    f"reel_{netflix_json['chunk_number']}.mp4"
                )

                output_path.parent.mkdir(
                    parents=True,
                    exist_ok=True
                )

                status_box.info(
                    f"""
Rendering Video

{netflix_file.name}
"""
                )
                
                result = render_reel(
                    scenes=scenes,
                    output_path=str(output_path)
                )

                st.image(
                    result["thumbnail"],
                    caption="Generated Thumbnail"
                )

                st.video(
                    str(output_path)
                )

                completed += 1

                progress.progress(
                    completed / total
                )

                for row in rows:

                    if row["file"] == netflix_file.name:

                        row["status"] = "Completed"

                table_box.dataframe(
                    pd.DataFrame(rows),
                    use_container_width=True
                )

            except Exception as e:

                for row in rows:

                    if row["file"] == netflix_file.name:

                        row["status"] = (
                            f"Failed: {e}"
                        )

                table_box.dataframe(
                    pd.DataFrame(rows),
                    use_container_width=True
                )

                st.error(
                    f"""
Failed:

{netflix_file.name}

{e}
"""
                )

        status_box.success(
            "All Videos Generated"
        )

        st.success(
            f"""
Generated {completed} videos

Saved in:

generated/videos
"""
        )