from pathlib import Path


def get_system_prompt(prompt_name: str) -> str:
    current_dir = Path(__file__).parent
    filepath = current_dir / "data" / f"{prompt_name}.txt"
    
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")
    except Exception as e:
        raise IOError(f"Error reading file {filepath}: {str(e)}")


def attach_system_prompt(text: str, prompt_name: str) -> str:
    system_prompt = get_system_prompt(prompt_name)
    return f"{system_prompt}\n\n{text}"
