"""
aiida_diff

AiiDA demo plugin that computes the difference between two files.
"""

from __future__ import absolute_import

__version__ = "1.0.0a1"

# disable psycopg2 warning
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='psycopg2')
