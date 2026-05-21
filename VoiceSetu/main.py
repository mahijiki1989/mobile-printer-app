"""
VoiceSetu - Offline Voice to Text Desktop Application
Main entry point.

This application performs all speech recognition locally.
No audio data is ever sent to any cloud service or external server.
"""

import logging
import os
import sys
from pathlib import Path


def setup_logging():
    """Configure application logging."""
    from src.core.config import get_app_data_dir

    log_dir = get_app_data_dir() / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "voicesetu.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def setup_path():
    """Ensure the application can find its modules."""
    if getattr(sys, "frozen", False):
        app_dir = Path(sys._MEIPASS)
    else:
        app_dir = Path(__file__).resolve().parent

    if str(app_dir) not in sys.path:
        sys.path.insert(0, str(app_dir))

    os.chdir(app_dir)


def main():
    """Application main entry point."""
    setup_path()
    setup_logging()

    logger = logging.getLogger(__name__)
    logger.info("VoiceSetu starting...")

    try:
        from src.ui.main_window import MainWindow

        app = MainWindow()
        app.mainloop()

    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)
        try:
            import tkinter.messagebox as mb
            mb.showerror(
                "VoiceSetu - Error",
                f"A fatal error occurred:\n\n{str(e)}\n\nPlease check the log file for details.",
            )
        except Exception:
            pass
        sys.exit(1)


if __name__ == "__main__":
    main()
