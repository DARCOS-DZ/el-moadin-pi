source env/bin/activate ;
celery -A el_moadin_pi worker -c 1 --loglevel=DEBUG -B ;
