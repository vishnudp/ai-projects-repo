from app.collectors.factory import create_collector


source_config = {
    "source_id": "test-oecd",
    "name": "Test OECD",
    "collection": {
        "method": "web",
        "base_url": "https://example.org",
    },
}


collector = create_collector(
    source_id="test-oecd",
    config=source_config,
)

print("COLLECTOR TYPE:")
print(type(collector).__name__)

print("SOURCE ID:")
print(collector.source_id)

print("COLLECTOR FACTORY TEST: OK")