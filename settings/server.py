import os
from common import *

#STATIC_ROOT = '/Users/sbassi/projects/serulab/misolrna/static/'
STATIC_ROOT = '/var/www/misolrna.org.v2/misolrna/static/'

BASE_URL = 'misolrna.org'

ROOT_DIR = '/var/www/misolrna.org.v2/misolrna/'
DB_NAME = os.path.join(ROOT_DIR,'mirna20.db')

#STATIC_FS = '/var/www/%s/htdocs/img/static/'%BASE_URL

STATIC_URL = 'static'

# BLAST path
BLASTN_EXE = '/var/www/misolrna.org.v2/blast/ncbi-blast-2.2.23+/bin/blastn'

# BLAST DBs path
BLASTDB_PATH = '/var/www/misolrna.org.v2/misolrna/blastdbs/'

# VENV
VENVS = '/var/www/misolrna.org.v2/venvs/misolrnav2/lib/python2.7/site-packages/'
