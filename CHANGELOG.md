# Changelog

## 1.0.0 (2026-03-17)


### Features

* add sync functionality ([716ffb8](https://github.com/chronicle-cal/chronicle/commit/716ffb80c28659f909b396f93c5f73db2b037cd9))
* **auth:** add token sessions, profile edit, and account delete ([cd84bc7](https://github.com/chronicle-cal/chronicle/commit/cd84bc77ef0a8a5394fa4c1c778684950b4a948d))
* **auth:** persist users in db and switch to argon2 ([0ed845e](https://github.com/chronicle-cal/chronicle/commit/0ed845e4e2bf8b1273e32e77a4ba59c0dba2106d))
* backend and worker overhaul with auth, DB schema updates, and calendar sync ([8f6cc49](https://github.com/chronicle-cal/chronicle/commit/8f6cc49f17a44e0a57f664e747aa71edf13f9894))
* custom UIDs, performance improvements ([edf58ce](https://github.com/chronicle-cal/chronicle/commit/edf58ce939c566c40b294c6c436cd998a75ab307))
* task scheduler ([fe6d32f](https://github.com/chronicle-cal/chronicle/commit/fe6d32f73206e1f1af949cb2bf9f0d6af2825bdb))
* worker rabbit mq connection, restructure ([6273fd0](https://github.com/chronicle-cal/chronicle/commit/6273fd0b4d237b3b7cebdf3c52daa34d0292c772))


### Bug Fixes

* add requirements.txt and uv-lock optional ([3302278](https://github.com/chronicle-cal/chronicle/commit/33022784bd99546dc910635d072d4e81a549f4da))
* add trufflehog version ([c9c3243](https://github.com/chronicle-cal/chronicle/commit/c9c3243ec8abbe7ddb55a4d75afcba7d3554a3ed))
* **backend:** auto-create missing DB tables at startup ([0ead386](https://github.com/chronicle-cal/chronicle/commit/0ead3863d2c886a15121585259f0a45f7e1dac86))
* fix import issues in ruff ([cdbbfd8](https://github.com/chronicle-cal/chronicle/commit/cdbbfd8c101954793781f83d98a3984c73c51f82))
* fix ruff issue with fastAPI ([b191e10](https://github.com/chronicle-cal/chronicle/commit/b191e103039e9730840c5ff3f8ef977e710f0a56))
* fix smoketest ([d0f6256](https://github.com/chronicle-cal/chronicle/commit/d0f62560df9d1f012cdb5bd65419f868177aa4c8))
* fix whitespaces, extra lines etc. ([56bc307](https://github.com/chronicle-cal/chronicle/commit/56bc307f90cde9f7be6a0e252f701264fd4a2672))
* ruff auto fix ([6204acd](https://github.com/chronicle-cal/chronicle/commit/6204acd06ac6c894ed5a55d332565b3d3518e344))
* trufflehog failure fix ([2295625](https://github.com/chronicle-cal/chronicle/commit/22956259883391049e1d2110a513683a314d2f94))
* update token and permissions for release workflow ([0bd80b2](https://github.com/chronicle-cal/chronicle/commit/0bd80b2a86471f17875dedce73cdf7e2c317043b))
