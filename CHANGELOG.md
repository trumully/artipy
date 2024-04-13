# CHANGELOG



## v1.0.0 (2024-04-13)

### Chore

* chore: merge pull request #2 from trumully/feature/analysis-module

feature/analysis-module ([`678cfbe`](https://github.com/trumully/artipy/commit/678cfbe2f3eeeaff0c0021de9bd9c641c5982749))

* chore: bump version to 0.3.0-beta.2 ([`975b67f`](https://github.com/trumully/artipy/commit/975b67fcff0bd45dbc6f48c01960ebb1a43624f8))

### Feature

* feat: add plot_expected_against_actual_mainstats method ([`1446bcb`](https://github.com/trumully/artipy/commit/1446bcbccf4540f0b91e6d7d1217769c80f9b26d))


## v0.3.0-beta.2 (2024-04-13)

### Feature

* feat(analysis.plots): add plot_multi_value_distribution ([`5e6db3a`](https://github.com/trumully/artipy/commit/5e6db3a52c86ed9e783e41d813d57d21f634fb90))

### Unknown

* improvement: add colors to bin on plot_crit_value_distribution ([`5614309`](https://github.com/trumully/artipy/commit/5614309d0c9b372375e354a3037ff3cdb1b734c6))


## v0.3.0-beta.1 (2024-04-13)

### Breaking

* feat!: add plots to analysis module

BREAKING CHANGES: pandas, plotly new dependencies ([`9bf0acf`](https://github.com/trumully/artipy/commit/9bf0acf5d67ec874b1c8f0472f69cc9c4174677b))

### Chore

* chore: fix versioning in pyproject.toml ([`89d8d2a`](https://github.com/trumully/artipy/commit/89d8d2aed093c89864f25532b77e9057c2533937))

* chore: bump version to 0.3.0.alpha ([`d731668`](https://github.com/trumully/artipy/commit/d7316687bed70f2cb83dc5b321c10bddcea50871))

### Ci

* ci: add support for test runs on feature branches ([`88f1815`](https://github.com/trumully/artipy/commit/88f181575f2ec72bb41ca500e57291197d6845fe))

### Documentation

* docs: update banner ([`8394353`](https://github.com/trumully/artipy/commit/8394353c9ab7b8d0b3bc22047c14d23111a188c2))

### Feature

* feat: calculate_substat_rolls method ([`586a763`](https://github.com/trumully/artipy/commit/586a763a4c2809917ba2f3dc5eae38ec2847a85f))

### Unknown

* Merge pull request #1 from trumully/main

ci: add support for test runs on feature branches ([`988c04d`](https://github.com/trumully/artipy/commit/988c04d0665008adfc2effc11b52c19504ad2cbb))

* initial commit ([`f770960`](https://github.com/trumully/artipy/commit/f770960557efd9c8a520ff1b966e02655ac93c74))


## v0.2.3 (2024-04-12)

### Chore

* chore(release): v0.2.3 [skip ci] ([`82229d4`](https://github.com/trumully/artipy/commit/82229d47461b4bb3aee01c473c8a2f17c57d290d))

* chore(merge): merge upstream changes ([`228cee0`](https://github.com/trumully/artipy/commit/228cee02376b3001b1a75ad72a4ca66f819843e1))

### Ci

* ci: edit concurrency of test job to cancel-in-progress ([`8fdfac6`](https://github.com/trumully/artipy/commit/8fdfac6099ac0218738eacc62c368233fc9e58ba))

### Fix

* fix(ArtifactBuilder): refine constraints for with_substat, with_substats, with_level parameters ([`1c56475`](https://github.com/trumully/artipy/commit/1c56475466656697796ea9532c986843231f5016))

* fix(ArtifactBuilder): add constraints for mainstat, substat, level, rarity setters ([`6786fa6`](https://github.com/trumully/artipy/commit/6786fa65321020a40d4f131bdb70d3d6c2adf37a))

### Style

* style: run isort ([`85414a6`](https://github.com/trumully/artipy/commit/85414a6028e04538d3e96c57e11ab14b32093496))

### Test

* test: add tests for ArtifactBuilder constraints. ([`0e4aab7`](https://github.com/trumully/artipy/commit/0e4aab79f320b189022adb7ef2655650a341cf01))


## v0.2.2 (2024-04-12)

### Chore

* chore(release): v0.2.2 [skip ci] ([`1440e40`](https://github.com/trumully/artipy/commit/1440e40e09502e53e308ba4dd83370c1e529331f))

### Documentation

* docs: correct example.py with up-to-date build syntax ([`2044744`](https://github.com/trumully/artipy/commit/2044744846f149c20a7309312eb722a34d8f16e5))

* docs: correct anchor headers in README ([`0f932da`](https://github.com/trumully/artipy/commit/0f932daeb58ecd60717ddbe8f4d36c82c66ebc98))

* docs: fix table of contents for README ([`b49a525`](https://github.com/trumully/artipy/commit/b49a525cb9ed1a43398a27c30ccae925c1b2e145))

* docs: beautify README ([`015cfa7`](https://github.com/trumully/artipy/commit/015cfa762737a35b69ef0b62f643cc8ac78e1f25))

### Performance

* perf(Artifact): add __slots__ ([`8cb20f1`](https://github.com/trumully/artipy/commit/8cb20f180b8ef34f8876aa818bfe1f14c383db81))

### Refactor

* refactor(ArtifactBuilder): simplify with_substat, with_substats parameters

Add substats like with_substat(&lt;stat_name&gt;, &lt;stat_value&gt;) instead of with_substat(SubStat(&lt;stat_name&gt;, &lt;stat_value&gt;)) ([`a3199d4`](https://github.com/trumully/artipy/commit/a3199d435e2e889bc3bc3791e7ca061d05bef900))


## v0.2.1 (2024-04-12)

### Chore

* chore(release): v0.2.1 [skip ci] ([`c34dfea`](https://github.com/trumully/artipy/commit/c34dfea5f060d0746d9c998c527d631309dcb434))

### Fix

* fix: change &#39;DECIMAL_PLACES&#39; constant type from float to str ([`11cdecc`](https://github.com/trumully/artipy/commit/11cdecccb2a12b57595243ea6fa2a723464a8257))

* fix(Stat.value): convert value to Decimal by default ([`0cf4418`](https://github.com/trumully/artipy/commit/0cf44184c351c0160fb282fcab675ebc5a51dc52))

* fix: move DECIMAL_PLACES constant from stats module to parent module ([`1759c80`](https://github.com/trumully/artipy/commit/1759c806f69a078762c160de6d4816949555c673))

### Refactor

* refactor(Stat): rename &#39;truncated_value&#39; to &#39;rounded_value&#39; ([`7857289`](https://github.com/trumully/artipy/commit/78572897f3fa162416940058179dac22a4c44b12))

### Unknown

* tests: new verbose stat fixtures for rounded_values property testing ([`725d5ec`](https://github.com/trumully/artipy/commit/725d5ec4301973b11c804d85d2e3187f624ec6dc))


## v0.2.0 (2024-04-11)

### Chore

* chore(release): v0.2.0 [skip ci] ([`290440b`](https://github.com/trumully/artipy/commit/290440b1b00a41520d87a00bf5b1bdadeb354d51))

### Ci

* ci: remove upload binaries step from workflow ([`cee8c57`](https://github.com/trumully/artipy/commit/cee8c57a16a869378aa122aaf8fad048dc61fab9))

### Feature

* feat: add truncated_value property to SubStat using helper function ([`1beaec6`](https://github.com/trumully/artipy/commit/1beaec69bc5c8396c71ec0266bf6b0173537e283))

### Refactor

* refactor(Stat): change truncated_value property to directly quantize ([`272b2d8`](https://github.com/trumully/artipy/commit/272b2d8e7562134e5c5e6d5d54a5f1b450b1f525))

### Unknown

* Merge branch &#39;main&#39; of https://github.com/trumully/artipy ([`42faf2d`](https://github.com/trumully/artipy/commit/42faf2d543e81eae00d04448babf92db679e4e4f))


## v0.1.1 (2024-04-11)

### Build

* build: add ruff, pytest, and isort to pyproject.toml ([`d8280ef`](https://github.com/trumully/artipy/commit/d8280efe05e77edc037764420f5e7908e32578e6))

### Chore

* chore(release): v0.1.1 [skip ci] ([`43c2ea6`](https://github.com/trumully/artipy/commit/43c2ea69bbcafea5294c9e5291ffe99e50a04cc3))

* chore: Updated workflow to upload binaries to GitHub Releases ([`d8a9d29`](https://github.com/trumully/artipy/commit/d8a9d2909a71c2032317bdfcc4585390a29d8cbe))

### Ci

* ci: remove &#39;poetry.lock&#39; from workflow trigger. ([`5745012`](https://github.com/trumully/artipy/commit/5745012909af89b2139151062f5dbeef52f4639b))

* ci: add isort to pre-commit hooks ([`888ed53`](https://github.com/trumully/artipy/commit/888ed53c59fb9884d3092f85d7cce00a3b375701))

### Documentation

* docs: add acknowledgements to README ([`d240a2f`](https://github.com/trumully/artipy/commit/d240a2f98f29fd9591e2f24a4fa5a05913f99518))

* docs: update README.md with quick start instructions and badges ([`c5fe1a9`](https://github.com/trumully/artipy/commit/c5fe1a9d659b7b6c7c97ffcd2e8899a17881a60c))

### Fix

* fix: prevent create_substat from picking incorrect StatType ([`d2aefd3`](https://github.com/trumully/artipy/commit/d2aefd31f75ee444cd3175b438251936d95dc522))


## v0.1.0 (2024-04-11)

### Chore

* chore(release): v0.1.0 [skip ci] ([`c527364`](https://github.com/trumully/artipy/commit/c5273649e7bcb17184a8594fb09b5ef1319f1453))

* chore: Fix workflow to install package before running pytest ([`70b2fc5`](https://github.com/trumully/artipy/commit/70b2fc5b7ab5df1bbbf0de1a6d7ff82e20db24c8))

* chore: Added test job to workflow. ([`670fc99`](https://github.com/trumully/artipy/commit/670fc991bd08da3d7f3906f3389a2621f15fad5a))

* chore: Added types-toml as an additional depndency for the pre-commit hook. ([`d4d4287`](https://github.com/trumully/artipy/commit/d4d4287ed01e2f70e45a89386edff3f7a517f014))

* chore: Added ruff linting &amp; formatting with mypy type checking to pre-commit hooks ([`5061aeb`](https://github.com/trumully/artipy/commit/5061aeb11882787ae076ea848a8414c11bdf64b5))

### Feature

* feat(ArtifactBuilder.with_substats): Add substats to an artifact w/ the builder.

Can either provide the substats or have them generated for you.

chore: Added ruff linting &amp; formatting with mypy type checking to pre-commit hooks ([`c071d93`](https://github.com/trumully/artipy/commit/c071d93e2e84bf1aa456a43076d037abbaff20ac))

* feat(ArtifactBuilder.with_substats): Add substats to an artifact w/ the builder.

Can either provide the substats or have them generated for you. ([`3eb33d5`](https://github.com/trumully/artipy/commit/3eb33d59f8e2bb51f98d0f0145be60ce70bb59b8))

### Unknown

* tests: Added tests for artifact and stats module. ([`94e313b`](https://github.com/trumully/artipy/commit/94e313b886d6dddc8abdbab2c826009af46cd10e))

* Merge branch &#39;main&#39; of https://github.com/trumully/artipy ([`4765d5c`](https://github.com/trumully/artipy/commit/4765d5cfefec8e5c74ed80c8010b06db1e09e224))

* Initial commit ([`ad9c953`](https://github.com/trumully/artipy/commit/ad9c9531e4db9076bc506f3f5a45c850bd2e3850))
