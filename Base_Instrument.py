# instrument_automation/base/base_instrument.py (Modified for Lazy Connection)
import logging
import pyvisa

class BaseInstrument:
    def __init__(self, visa_address: str, visa_manager: pyvisa.ResourceManager):
        self.visa_address = visa_address
        self.rm = visa_manager
        self.instrument = None # Start with no connection
        self._command_history = []
        logging.info(f"Initialized lazy instrument handle for: {self.visa_address}")

    def _ensure_connection(self):
        """Internal method to connect if not already connected."""
        if self.instrument is None:
            self.connect()

    def connect(self) -> None:
        """Establishes connection to the instrument."""
        if self.instrument:
            logging.warning(f"Already connected to {self.visa_address}. Ignoring connect call.")
            return
        try:
            # ... (the rest of the connect method is the same) ...
            self.instrument = self.rm.open_resource(self.visa_address)
            self.instrument.timeout = 5000
            idn = self.query("*IDN?") # The query here will trigger the real connection
            logging.info(f"Connected to: {idn.strip()}")
        except pyvisa.errors.VisaIOError as e:
            logging.error(f"Failed to connect to {self.visa_address}: {e}")
            self.instrument = None # Ensure instrument is None on failure
            raise ConnectionError(f"Could not connect to instrument at {self.visa_address}") from e

    def disconnect(self) -> None:
        # ... (disconnect method is the same) ...
        if self.instrument:
            self.instrument.close()
            logging.info(f"Disconnected from {self.visa_address}")
            self.instrument = None

    def write(self, command: str) -> None:
        """Sends a command, connecting if necessary."""
        self._ensure_connection() # Check and connect if needed
        # ... (the rest of the method is the same) ...
        self._command_history.append(command)
        self.instrument.write(command)
        logging.debug(f"Wrote to {self.visa_address}: {command}")


    def query(self, command: str) -> str:
        """Sends a command and reads, connecting if necessary."""
        self._ensure_connection() # Check and connect if needed
        # ... (the rest of the method is the same) ...
        self._command_history.append(f"{command}?")
        response = self.instrument.query(command)
        logging.debug(f"Queried {self.visa_address} with '{command}': Received '{response.strip()}'")
        return response.strip()

    # The __enter__ and __exit__ methods still work perfectly with this pattern!
    def __enter__(self):
        self._ensure_connection()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()