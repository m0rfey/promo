work dir: promo

```bash
python3.7 -m pip install pipenv
cd promo/
pipenv install
pipenv shell
```

run celery
```bash
 (promo)$ celery -A configs worker --loglevel=info
```

run dev server
```bash
 (promo)$ ./manage.py runserver
```
