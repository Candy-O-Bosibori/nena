#!/usr/bin/env python
"""
One-off script to clean up old upload directories after media-deletion refactor.
Run once manually post-deploy to remove leftover files from static/uploads/ and static/audio/.
Not part of the Alembic migration chain.
"""
import os
import shutil

DIRS_TO_CLEAN = [
    'static/uploads',
    'static/audio',
]

for directory in DIRS_TO_CLEAN:
    if os.path.exists(directory):
        print(f"Removing {directory}...")
        shutil.rmtree(directory)
        print(f"  ✅ Removed {directory}")
    else:
        print(f"  (Directory {directory} does not exist, skipping)")

print("\nCleanup complete!")
