source env/bin/activate ;
celery -A el_moadin_pi worker --loglevel=DEBUG -B ;
