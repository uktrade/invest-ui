# Changelog

## Pre-release

### Implemented Enhancements
- [CI-108](https://uktrade.atlassian.net/browse/CI-108) Temporarily Turn off the new custom tags and events for GA 360.
- [CI-123](https://uktrade.atlassian.net/browse/CI-123) Fixed icons to be 60x60 to align with other pages

### Fixed bugs:
- [CMS-1522](https://uktrade.atlassian.net/browse/CMS-1522) Fix language select on contact form
- [CMS-1515](https://uktrade.atlassian.net/browse/CMS-1515) Fixed invest header links going inline rather one on top of the other when on mobile
- [CI-127](https://uktrade.atlassian.net/browse/CI-127) The ISD card changes to a link to the 'tax and incentives' page when the ISD feature flag is turned off


## [2019.05.09](https://github.com/uktrade/invest-ui/releases/tag/2019.05.09)
[Full Changelog](https://github.com/uktrade/invest-ui/compare/2019.04.30...2019.05.09)

### Implemented Enhancements
- [CI-108](https://uktrade.atlassian.net/browse/CI-108) Add GA tags to invest pages.
- Upgrade Directory Components to 11.0.2 to add:
    - [CI-114](https://uktrade.atlassian.net/browse/CI-114) Add 'UK Setup Guide' link to header
    - [CI-108](https://uktrade.atlassian.net/browse/CI-108) Add GA tags to the international header
    - [Full Changelog](https://github.com/uktrade/directory-components/blob/master/CHANGELOG.md)
- [CI-116](https://uktrade.atlassian.net/browse/CI-116) Moved set up guide, ISD section and capital invest section to one row of 3 cards on Invest Home Page

### Fixed bugs:


- [CMS-1395](https://uktrade.atlassian.net/browse/CMS-1395) Fix language cookie name and domain to be the same across all our services.
- [XOT-819](https://uktrade.atlassian.net/browse/XOT-819) Changed HPO contact form data serialization format.


## [2019.04.30](https://github.com/uktrade/invest-ui/releases/tag/2019.04.30)
[Full Changelog](https://github.com/uktrade/invest-ui/compare/2019.04.24...2019.04.30)

- [CI-103](https://uktrade.atlassian.net/browse/CI-103) Whole HPO section disappears if not available in active language
- [CI-101](https://uktrade.atlassian.net/browse/CI-101) Added Investor Support Directory section to Invest landing page behind feature flag


## [2019.04.24](https://github.com/uktrade/invest-ui/releases/tag/2019.04.24)
[Full Changelog](https://github.com/uktrade/invest-ui/compare/2019.04.16...2019.04.24)

### Implemented enhancements:

- Upgraded [CMS client][directory-cms-client] to allow `lookup_by_path`, to facilitate CMS tree based routing.
- Upgraded [CMS client][directory-cms-client] reduces noisy fallback cache logging.
- Upgraded [Forms client][directory-forms-api-client]  because [CMS client][directory-cms-client] upgrade results in [Client core][directory-client-core] being upgraded.
- Added `DIRECTORY_CLIENT_CORE_CACHE_EXPIRE_SECONDS` env var.
- Added `DIRECTORY_CONSTANTS_URL_GREAT_INTERNATIONAL` to 'settings.py'
- Captured UTM codes for HPO & PFP enquiries, sending by email to admins.

### Fixed bugs:
- Upgraded urllib3 to fix [vulnerability](https://nvd.nist.gov/vuln/detail/CVE-2019-11324)


[directory-client-core]: https://github.com/uktrade/directory-client-core
[directory-cms-client]: https://github.com/uktrade/directory-cms-client
[directory-forms-api-client]: https://github.com/uktrade/directory-forms-api-client
