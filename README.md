# invest-ui
[Invest UI](https://www.directory.exportingisgreat.gov.uk/)

[![code-climate-image]][code-climate]
[![circle-ci-image]][circle-ci]
[![codecov-image]][codecov]
[![gemnasium-image]][gemnasium]

---

## Requirements

[Python 3.5](https://www.python.org/downloads/release/python-350/)

[Docker >= 1.10](https://docs.docker.com/engine/installation/)

[Docker Compose >= 1.8](https://docs.docker.com/compose/install/)


## Local installation

    $ git clone https://github.com/uktrade/invest-ui
    $ cd invest-ui
    $ make

## Running with Docker
Requires all host environment variables to be set.

    $ make docker_run

### Run debug webserver in Docker

    $ brew link gettext --force (OS X only)
    $ make docker_debug

### Run tests in Docker

    $ make docker_test

### Host environment variables for docker-compose
``.env`` files will be automatically created (with ``env_writer.py`` based on ``env.json``) by ``make docker_test``, based on host environment variables with ``INVEST_UI_`` prefix.

#### Web server
| Host environment variable | Docker environment variable  |
| ------------- | ------------- |
| INVEST_UI_SECRET_KEY | SECRET_KEY |
| INVEST_UI_PORT | PORT |
| INVEST_UI_UI_SESSION_COOKIE_SECURE | UI_SESSION_COOKIE_SECURE |

## Debugging

### Setup debug environment

    $ make debug

### Run debug webserver

    $ make debug_webserver

### Run debug tests

    $ make debug_test

## CSS development

### Requirements
[node](https://nodejs.org/en/download/)
[SASS](http://sass-lang.com/)
[gulp](https://gulpjs.com/)

	$ npm install

### Update CSS under version control

	$ gulp sass

### Rebuild the CSS files when the scss file changes

	$ gulp sass:watch

## Session

Signed cookies are used as the session backend to avoid using a database. We therefore must avoid storing non-trivial data in the session, because the browser will be exposed to the data.


[code-climate-image]: https://codeclimate.com/github/uktrade/invest-ui/badges/issue_count.svg
[code-climate]: https://codeclimate.com/github/uktrade/invest-ui

[circle-ci-image]: https://circleci.com/gh/uktrade/invest-ui/tree/master.svg?style=svg
[circle-ci]: https://circleci.com/gh/uktrade/invest-ui/tree/master

[codecov-image]: https://codecov.io/gh/uktrade/invest-ui/branch/master/graph/badge.svg
[codecov]: https://codecov.io/gh/uktrade/invest-ui

[gemnasium-image]: https://gemnasium.com/badges/github.com/uktrade/invest-ui.svg
[gemnasium]: https://gemnasium.com/github.com/uktrade/invest-ui
