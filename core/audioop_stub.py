# Stub for audioop module (removed in Python 3.13+)
# This stub is used by discord.py for voice support

class audioop_stub:
    """Stub for audioop - not used by Syncord"""
    def __getattr__(self, name):
        return lambda *args, **kwargs: None

# Make it appear as if the module exists
import sys
sys.modules['audioop'] = audioop_stub()
