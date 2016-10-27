"""      Please refer to the license file for complete details. 
  *      Project: OpenPy
  *      Developer: Yash Lamba
  *      Institute: Indraprastha Institute of Information Technology, Delhi
  *      Advisor: Pandarasamy Arjunan, Dr. Pushpendra Singh
"""

#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OpenPy.settings")

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
