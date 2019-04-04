# invest-ui
[Invest UI](https://invest.great.gov.uk/)

[![circle-ci-image]][circle-ci]
[![codecov-image]][codecov]

---

## Requirements

[Python 3.6](https://www.python.org/downloads/release/python-360/)
[Redis](https://redis.io/)

## Local installation

    $ git clone https://github.com/uktrade/invest-ui
    $ cd invest-ui
    $ make

## Directory Forms

Form submissions are powered by [directory-forms-api](https://github.com/uktrade/directory-forms-api). Set that up locally then generate a API client [here](http://forms.trade.great:8011/admin/client/client/) and add the following entries to your `conf/.env` file.

| Environment variable                                  | Notes                             |
| ----------------------------------------------------- | --------------------------------- |
| DIRECTORY_FORMS_API_API_KEY                           | Populate from client `access_key` |
| DIRECTORY_FORMS_API_SENDER_ID                         | Populate from client `identifier` |

## Debugging

### Setup debug environment

    $ make debug

### Run debug webserver

    $ make debug_webserver

### Run debug tests

    $ make debug_test

## CSS development

If you're doing front-end development work you will need to be able to compile the SASS to CSS. For this you need:

    $ npm install yarn
    $ yarn install --production=false

We add compiled CSS files to version control. This will sometimes result in conflicts if multiple developers are working on the same SASS files. However, by adding the compiled CSS to version control we avoid having to install node, npm, node-sass, etc to non-development machines.

You should not edit CSS files directly, instead edit their SCSS counterparts.

### Update CSS under version control

    $ make compile_css


## Session

Signed cookies are used as the session backend to avoid using a database. We therefore must avoid storing non-trivial data in the session, because the browser will be exposed to the data.


[circle-ci-image]: https://circleci.com/gh/uktrade/invest-ui/tree/master.svg?style=svg
[circle-ci]: https://circleci.com/gh/uktrade/invest-ui/tree/master

[codecov-image]: https://codecov.io/gh/uktrade/invest-ui/branch/master/graph/badge.svg
[codecov]: https://codecov.io/gh/uktrade/invest-ui

