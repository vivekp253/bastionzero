import subprocess
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
CA_KEY = BASE_DIR / "keys" / "user_ca"


def issue_certificate(
    public_key_path: str,
    identity: str,
    username: str,
    minutes: int = 30,
):
    public_key = Path(public_key_path)

    if not public_key.is_file():
        raise FileNotFoundError("Developer public key not found")

    if not 1 <= minutes <= 60:
        raise ValueError("Certificate duration must be between 1 and 60 minutes")

    if not CA_KEY.is_file():
        raise FileNotFoundError("SSH CA private key not found")

    subprocess.run(
        [
            "ssh-keygen",
            "-s",
            str(CA_KEY),
            "-I",
            identity,
            "-n",
            username,
            "-V",
            f"+{minutes}m",
            str(public_key),
        ],
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    )

    certificate = public_key.with_name(
        public_key.name.removesuffix(".pub") + "-cert.pub"
    )

    return certificate


if __name__ == "__main__":
    certificate = issue_certificate(
        "keys/developer.pub",
        "developer-demo",
        "developer",
        30,
    )

    print(f"Certificate created: {certificate}")