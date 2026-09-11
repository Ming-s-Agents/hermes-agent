"""State-store helpers must survive installed imports outside the checkout."""
from pathlib import Path
import tomllib


def test_state_modules_are_in_installation_manifest():
    """Checkout imports hide omissions in setuptools' editable module map.

    Keep the state-store module family declared so external CLI/adaptor
    processes can import the same runtime as processes started in the repo.
    """
    root = Path(__file__).resolve().parents[1]
    metadata = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    declared = set(metadata["tool"]["setuptools"]["py-modules"])
    state_modules = {path.stem for path in root.glob("hermes_state*.py")}
    assert state_modules <= declared, (
        "State modules missing from installation manifest: "
        f"{sorted(state_modules - declared)}"
    )
