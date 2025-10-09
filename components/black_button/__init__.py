from pathlib import Path
from streamlit.components.v1 import declare_component

_component_path = Path(__file__).parent / "frontend"

black_button = declare_component(
    name="black_button",
    path=str(_component_path),
)
