import pyvisa

def check_instruments():
    try:
        rm = pyvisa.ResourceManager()
        resources = rm.list_resources()
        if not resources:
            return ["\nNo instruments found.\n"]
        return [f"Found: {r}" for r in resources]
    except Exception as e:
        return [f"Error: {str(e)}"]
