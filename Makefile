install:
	uv pip install -r requirements.txt

migrate:
	python manage.py migrate

collectstatic:
	python manage.py collectstatic --noinput

render-start:
	gunicorn task_manager.wsgi