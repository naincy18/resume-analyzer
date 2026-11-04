# The ONLY place the backend decides which analyze_resume to use.
#
# Right now: the temporary stub.
# Later: when the AI developer's function is ready, comment out the stub
# line and use the real import instead (the exact path comes from them).

from ml_engine.stub import analyze_resume

# from app.ml.<their_file> import analyze_resume   # <- real one, later

__all__ = ["analyze_resume"]