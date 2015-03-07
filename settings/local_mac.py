import os
from common import *

STATIC_ROOT = '/Users/sbassi/projects/serulab/misolrna/static/'

BASE_URL = 'misolrna.org'

ROOT_DIR = '/Users/sbassi/projects/serulab/misolrna/'
DB_NAME = os.path.join(ROOT_DIR,'mirna20.db')

STATIC_FS = '/var/www/%s/htdocs/img/static/'%BASE_URL

STATIC_URL = 'static'