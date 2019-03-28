"""
aiida_diff

AiiDA demo plugin that computes the difference between two files.
"""

from __future__ import absolute_import

__version__ = "0.1.0a0"

# disable psycopg2 warning
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='psycopg2')
