from pathlib import Path

BASE_DIR = Path(__file__).parent

OLLAMA_URL = "http://localhost:11434/api/generate"

CACHE_DIR = BASE_DIR / "cache"

GENERATED_DIR = BASE_DIR / "generated"

UPLOAD_DIR = BASE_DIR / "uploads"

PROMPT_DIR = BASE_DIR / "prompts"

MODELS = {

    "summary": "qwen3:4b",

    "master_summary": "qwen3:4b",

    "metadata": "qwen3:4b",

    "knowledge": "qwen3:4b",

    "emotion": "qwen3:4b",

    "reel_candidate": "qwen3:4b",

    "storyboard": "qwen3:8b",

    "visual_planner": "qwen3:8b",

    "thumbnail": "qwen3:4b"
}

CHUNK_DURATION_SECONDS = 600

MAX_WORKERS = 2