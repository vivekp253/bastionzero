from certificate_service import issue_certificate


certificate = issue_certificate(
    "keys/developer.pub",
    "developer-test",
    "developer",
    30,
)

print(f"SUCCESS: Certificate created at {certificate}")