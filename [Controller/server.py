from desktop import LandingWindow
import signal
from signal_handler import signal_handler

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)
LandingWindow()
