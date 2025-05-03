# animal_bird_kb_ui
An UI to create an knowledge base of animals and birds

1) Start animal knowledge base application: 
$python ./app.py
2) Start celery worker: 
$celery -A celery_worker worker --loglevel=info
3) Start celery flower monitor task service: 
$celery -A celery_worker flower --port=5555
4) Start celery beat scheduler: 
$celery -A celery_worker beat --loglevel=info