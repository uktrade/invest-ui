# Changelog

## Pre-release

## [2019.04.30](https://github.com/uktrade/invest-ui/releases/tag/2019.04.30)
[Full Changelog](https://github.com/uktrade/invest-ui/compare/2019.04.24...2019.04.30)
- [CI-103](https://uktrade.atlassian.net/browse/CI-103) Whole HPO section disappears if not available in active language
- [CI-101](https://uktrade.atlassian.net/browse/CI-101) Added Investor Support Directory section to Invest landing page behind feature flag
- [CI-116](https://uktrade.atlassian.net/browse/CI-116) Moved set up guide, ISD section and capital invest section to one row of 3 cards on Invest Home Page

## [2019.04.24](https://github.com/uktrade/invest-ui/releases/tag/2019.04.24)
[Full Changelog](https://github.com/uktrade/invest-ui/compare/2019.04.16...2019.04.24)
**Implemented enhancements:**

- Upgraded [CMS client][directory-cms-client] to allow `lookup_by_path`, to facilitate CMS tree based routing.
- Upgraded [CMS client][directory-cms-client] reduces noisy fallback cache logging.
- Upgraded [Forms client][directory-forms-api-client]  because [CMS client][directory-cms-client] upgrade results in [Client core][directory-client-core] being upgraded.
- Added `DIRECTORY_CLIENT_CORE_CACHE_EXPIRE_SECONDS` env var.
- Added `DIRECTORY_CONSTANTS_URL_GREAT_INTERNATIONAL` to 'settings.py'

**Fixed bugs:**
- Upgraded urllib3 to fix [vulnerability](https://nvd.nist.gov/vuln/detail/CVE-2019-11324)


[directory-client-core]: https://github.com/uktrade/directory-client-core
[directory-cms-client]: https://github.com/uktrade/directory-cms-client
[directory-forms-api-client]: https://github.com/uktrade/directory-forms-api-client
