import sys
import logging
sys.path.insert(0, "/var/www/ai-captcha")

from app import app as application

logging.basicConfig(stream=sys.stderr)
