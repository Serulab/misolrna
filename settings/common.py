

# Define in local
STATIC_ROOT = ''


EXPRESSION_S = set(['SGN-U577351.png', 'SGN-U317177.png', 'SGN-U577190.png', 
                    'SGN-U581590.png', 'SGN-U564920.png', 'SGN-U314861.png', 
                    'SGN-U564413.png', 'U217520.png', 'SGN-U580201.png', 
                    'SGN-U219318.png', 'SGN-U575153.png', 'SGN-U225755.png', 
                    'SGN-U573423.png', 'SGN-U315828.png', 'SGN-U573225.png', 
                    'SGN-U579174.png', 'SGN-U580203.png', 'SGN-U576708.png', 
                    'SGN-U579797.png', 'SGN-U313725.png', 'SGN-U313497.png', 
                    'SGN-U574086.png', 'SGN-U312490.png', 'SGN-U567211.png', 
                    'SGN-U315756.png', 'SGN-U319311.png'])



BASE_URL = 'misolrna.org'
dbname = '/var/www/%s/htdocs/mirna20.db'%BASE_URL
rootdir = '/var/www/%s/htdocs/'%BASE_URL
imgdir = 'http://img.%s/'%BASE_URL
imgdirFS = '/var/www/%s/htdocs/img/'%BASE_URL
staticFS = '/var/www/%s/htdocs/img/static/'%BASE_URL
