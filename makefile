
build: docker_test

clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete

test_requirements:
	pip install -r requirements_test.txt

FLAKE8 := flake8 . --exclude=migrations,.venv,node_modules
PYTEST := pytest . -v --ignore=node_modules --cov=. --cov-config=.coveragerc --capture=no $(pytest_args)
COLLECT_STATIC := python manage.py collectstatic --noinput
COMPILE_TRANSLATIONS := python manage.py compilemessages
CODECOV := \
	if [ "$$CODECOV_REPO_TOKEN" != "" ]; then \
	   codecov --token=$$CODECOV_REPO_TOKEN ;\
	fi

test:
	$(COLLECT_STATIC) && $(FLAKE8) && $(PYTEST) && $(CODECOV)

DJANGO_WEBSERVER := \
	python manage.py collectstatic --noinput && \
	python manage.py runserver 0.0.0.0:$$PORT

django_webserver:
	$(DJANGO_WEBSERVER)

DOCKER_COMPOSE_REMOVE_AND_PULL := docker-compose -f docker-compose.yml -f docker-compose-test.yml rm -f && docker-compose -f docker-compose.yml -f docker-compose-test.yml pull
DOCKER_COMPOSE_CREATE_ENVS := python ./docker/env_writer.py ./docker/env.json ./docker/env.test.json

docker_run:
	$(DOCKER_COMPOSE_CREATE_ENVS) && \
	$(DOCKER_COMPOSE_REMOVE_AND_PULL) && \
	docker-compose up --build

DOCKER_SET_DEBUG_ENV_VARS := \
	export INVEST_UI_PORT=8012; \
	export INVEST_UI_SECRET_KEY=debug; \
	export INVEST_UI_DEBUG=true; \
	export INVEST_UI_FEATURE_CONTACT_COMPANY_FORM_ENABLED=true; \
	export INVEST_UI_RECAPTCHA_PUBLIC_KEY=debug; \
	export INVEST_UI_RECAPTCHA_PRIVATE_KEY=debug; \
	export INVEST_UI_GOOGLE_TAG_MANAGER_ID=GTM-TC46J8K; \
	export INVEST_UI_GOOGLE_TAG_MANAGER_ENV=&gtm_auth=Ok4kd4Wf_NKgs4c5Z5lUFQ&gtm_preview=env-6&gtm_cookies_win=x; \
	export INVEST_UI_UTM_COOKIE_DOMAIN=.great; \
	export INVEST_UI_NOCAPTCHA=false; \
	export INVEST_UI_SESSION_COOKIE_SECURE=false; \
	export INVEST_UI_SECURE_HSTS_SECONDS=0; \
	export INVEST_UI_SECURE_SSL_REDIRECT=false; \
	export INVEST_UI_CMS_URL=http://cms.trade.great:8010; \
	export INVEST_UI_CMS_SIGNATURE_SECRET=debug; \
	export INVEST_UI_DEFAULT_FROM_EMAIL=debug@foo.com; \
	export INVEST_UI_IIGB_AGENT_EMAIL=debug@foo.com; \
	export INVEST_UI_EMAIL_HOST=foo.com; \
	export INVEST_UI_EMAIL_HOST_USER=debug; \
	export INVEST_UI_EMAIL_HOST_PASSWORD=debug; \
	export INVEST_UI_FEATURE_SEARCH_ENGINE_INDEXING_DISABLED=true; \
	export INVEST_UI_PRIVACY_COOKIE_DOMAIN=.trade.great; \
	export INVEST_UI_DIRECTORY_FORMS_API_BASE_URL=http://forms.trade.great:8011; \
	export INVEST_UI_DIRECTORY_FORMS_API_API_KEY=debug; \
	export INVEST_UI_DIRECTORY_FORMS_API_SENDER_ID=debug; \
	export INVEST_UI_FEATURE_HIGH_POTENTIAL_OPPORTUNITIES_ENABLED=true; \
	export INVEST_UI_FEATURE_FORMS_API_ENABLED=true; \
	export INVEST_UI_HPO_GOV_NOTIFY_AGENT_EMAIL_ADDRESS=test@example.com

docker_test_env_files:
	$(DOCKER_SET_DEBUG_ENV_VARS) && \
	$(DOCKER_COMPOSE_CREATE_ENVS)

DOCKER_REMOVE_ALL := \
	docker ps -a | \
	grep directoryui_ | \
	awk '{print $$1 }' | \
	xargs -I {} docker rm -f {}

docker_remove_all:
	$(DOCKER_REMOVE_ALL)

docker_debug: docker_remove_all
	$(DOCKER_SET_DEBUG_ENV_VARS) && \
	$(DOCKER_COMPOSE_CREATE_ENVS) && \
	docker-compose pull && \
	docker-compose build && \
	docker-compose run --service-ports webserver make django_webserver

docker_webserver_bash:
	docker exec -it directoryui_webserver_1 sh

docker_test: docker_remove_all
	$(DOCKER_SET_DEBUG_ENV_VARS) && \
	$(DOCKER_COMPOSE_CREATE_ENVS) && \
	$(DOCKER_COMPOSE_REMOVE_AND_PULL) && \
	docker-compose -f docker-compose-test.yml build && \
	docker-compose -f docker-compose-test.yml run sut

docker_build:
	docker build -t ukti/directory-ui-supplier:latest .

DEBUG_SET_ENV_VARS := \
	export PORT=8012; \
	export SECRET_KEY=debug; \
	export DEBUG=true ;\
	export FEATURE_CONTACT_COMPANY_FORM_ENABLED=true; \
	export RECAPTCHA_PUBLIC_KEY=debug; \
	export RECAPTCHA_PRIVATE_KEY=debug; \
	export GOOGLE_TAG_MANAGER_ID=GTM-TC46J8K; \
	export GOOGLE_TAG_MANAGER_ENV=&gtm_auth=Ok4kd4Wf_NKgs4c5Z5lUFQ&gtm_preview=env-6&gtm_cookies_win=x; \
	export UTM_COOKIE_DOMAIN=.great; \
	export NOCAPTCHA=false; \
	export SESSION_COOKIE_SECURE=false; \
	export SECURE_HSTS_SECONDS=0 ;\
	export SECURE_SSL_REDIRECT=false; \
	export CMS_URL=http://cms.trade.great:8010; \
	export CMS_SIGNATURE_SECRET=debug; \
	export DEFAULT_FROM_EMAIL=debug@foo.com; \
	export IIGB_AGENT_EMAIL=debug@foo.com; \
	export EMAIL_HOST=foo.com; \
	export EMAIL_HOST_USER=debug; \
	export EMAIL_HOST_PASSWORD=debug; \
	export HEADER_FOOTER_URLS_GREAT_HOME=http://exred.trade.great:8007/; \
	export FEATURE_SEARCH_ENGINE_INDEXING_DISABLED=true; \
	export REDIS_URL=redis://localhost:6379; \
	export PRIVACY_COOKIE_DOMAIN=.trade.great; \
	export DIRECTORY_FORMS_API_BASE_URL=http://forms.trade.great:8011; \
	export FEATURE_HIGH_POTENTIAL_OPPORTUNITIES_ENABLED=true; \
	export FEATURE_FORMS_API_ENABLED=true; \
	export HPO_GOV_NOTIFY_AGENT_EMAIL_ADDRESS=test@example.com

debug_webserver:
	$(DEBUG_SET_ENV_VARS) && $(DJANGO_WEBSERVER)

debug_pytest:
	$(DEBUG_SET_ENV_VARS) && $(COLLECT_STATIC) && $(PYTEST)

debug_test:
	$(DEBUG_SET_ENV_VARS) && $(COLLECT_STATIC) && $(FLAKE8) && $(PYTEST) --cov-report=html

debug_manage:
	$(DEBUG_SET_ENV_VARS) && ./manage.py $(cmd)

debug_shell:
	$(DEBUG_SET_ENV_VARS) && ./manage.py shell

debug: test_requirements debug_test

heroku_deploy_dev:
	./docker/install_heroku_cli.sh
	docker login --username=$$HEROKU_EMAIL --password=$$HEROKU_TOKEN registry.heroku.com
	~/bin/heroku-cli/bin/heroku container:push web --app invest-ui-dev
	~/bin/heroku-cli/bin/heroku container:release web --app invest-ui-dev

integration_tests:
	cd $(mktemp -d) && \
	git clone https://github.com/uktrade/directory-tests && \
	cd directory-tests && \
	make docker_integration_tests

compile_requirements:
	python3 -m piptools compile requirements.in
	python3 -m piptools compile requirements_test.in

translations:
	$(DEBUG_SET_ENV_VARS) && python manage.py makemessages -a

compile_translations:
	$(DEBUG_SET_ENV_VARS) && python manage.py compilemessages

.PHONY: build clean test_requirements docker_run docker_debug docker_webserver_bash docker_test debug_webserver debug_test debug heroku_deploy_dev heroku_deploy_demo
