# CHANGELOG



## v1.1.0 (2024-04-16)

### Build

* build: update dev dependencies

Dependencies:
python-semantic-release (9.4.1 -&gt; 9.4.2) ([`5c4f7b6`](https://github.com/trumully/artipy/commit/5c4f7b66fe8f9d0f59c92f58a2c71205b0e140af))

### Ci

* ci: remove push condition on semver, docs jobs ([`b594fb8`](https://github.com/trumully/artipy/commit/b594fb8b62ab43398aadebb65c908b3a329f8e31))

* ci: release and doc job only on push to main ([`e456599`](https://github.com/trumully/artipy/commit/e4565995004237236c164059be3f15e4d9ab4fff))

* ci: modify concurrency ([`52dc4c7`](https://github.com/trumully/artipy/commit/52dc4c705c536c0bf6cab004f9a63361b3981252))

* ci: run doc job only on release ([`8edaa65`](https://github.com/trumully/artipy/commit/8edaa65469600bfe8896d24746d16a69c516112f))

* ci: fix pylint on pre-commit. ([`73583c9`](https://github.com/trumully/artipy/commit/73583c91900bf7b802124dc10718ed89acbd4764))

* ci: phase out isort in favor of ruff ([`70f6e10`](https://github.com/trumully/artipy/commit/70f6e10c0da968d5c742ee62b7b8db3b43b7a468))

### Feature

* feat(Artifact): type for artifact&#39;s slot ArtifactSlot ([`71d764a`](https://github.com/trumully/artipy/commit/71d764a809a6c43ff7b41329598e9cd0a3945e4f))

### Fix

* fix(artipy.analysis.plots): TypeError when indexing ArtifactSlot as str instead of ArtifactSlot ([`1c3a0ad`](https://github.com/trumully/artipy/commit/1c3a0ad3ca36000906b898eb98dc5fd73ed37f2b))

### Refactor

* refactor: StatData -&gt; DataGen at base module level ([`d887371`](https://github.com/trumully/artipy/commit/d887371a3c92a6dd9aaf33d1cfff20ef1a383467))

### Test

* test: re-add artifact fixture ([`b05a26f`](https://github.com/trumully/artipy/commit/b05a26f30e3387ce357587a1cde800bfd708e8da))

* test: add property based testing for artifact module ([`a5adbf3`](https://github.com/trumully/artipy/commit/a5adbf366c1bb15d8808cdbf732c54bee018efa7))

* test: refactor testing for artipy.stats module to use property testing

shadow removal of rounded_value property ([`2124f05`](https://github.com/trumully/artipy/commit/2124f050be29561b6c4eec0678e9318e7ae2741d))

### Unknown

* initial commit ([`5a11ed1`](https://github.com/trumully/artipy/commit/5a11ed1074a13421d0b50954f4fb530773691d01))

* improvement(Artifact): enhance getter and setter syntax

You can now do `artifact.level = level` instead of `artifact.set_level(level)` ([`27bebbc`](https://github.com/trumully/artipy/commit/27bebbc7ce82493aac6b4262fa86f7c6c8916311))

* improvement(Artifact): max_level property ([`efd100d`](https://github.com/trumully/artipy/commit/efd100d8d634f9b7493e334eb90792f681ae0161))


## v1.0.1 (2024-04-15)

### Build

* build: add black config to pyproject.toml ([`bc81ec7`](https://github.com/trumully/artipy/commit/bc81ec71fea87891d142229c13f5fce71657debe))

### Chore

* chore(release): v1.0.1 [skip ci] ([`05c8b7f`](https://github.com/trumully/artipy/commit/05c8b7f5d72a9c1c0bd383306c449b95be4dffa2))

* chore: add ruff to dev dependencies ([`63ef475`](https://github.com/trumully/artipy/commit/63ef4755c88d370b9305093ceb94066e09c6e6e9))

* chore(README): add https to doc badge ([`880ef71`](https://github.com/trumully/artipy/commit/880ef719b84ab94b3216b0c9776b7d3d4e890c50))

* chore(README): update doc status badge hyperlink ([`bf4f141`](https://github.com/trumully/artipy/commit/bf4f141c67bcc79795aaf64492e3a21471b7c850))

* chore(pyproject.toml): change black version to 24.4.0 ([`f479656`](https://github.com/trumully/artipy/commit/f47965608eccbeec3e4e60a1ee1ef2e8f3b36b28))

* chore: update badges in README ([`8bdfe31`](https://github.com/trumully/artipy/commit/8bdfe31740808c56fb114f3995145124ce859092))

* chore: add ruff badge to README ([`9726026`](https://github.com/trumully/artipy/commit/97260264660bb9c97a59c68fb2582d6df83ebee4))

* chore: add docs ref to README ([`8e240be`](https://github.com/trumully/artipy/commit/8e240be415952e01ac8d87cb4a7c8918943c2e2e))

* chore: add ghp-import to dev dependencies ([`dd19826`](https://github.com/trumully/artipy/commit/dd19826d98500185644fe04e0422ac12ada2235f))

* chore: add sphinx for doc building ([`727753c`](https://github.com/trumully/artipy/commit/727753c21ca4e166cf978574a1456d26a86b4f41))

* chore: fix docs gitignore ([`7359e92`](https://github.com/trumully/artipy/commit/7359e926f2635459d2efc11a903349bf59a37e9e))

* chore: remove docs (for now) ([`62a620e`](https://github.com/trumully/artipy/commit/62a620ef596886d056971ce6decb0afac974b897))

### Ci

* ci: change release job condition ([`18c54ef`](https://github.com/trumully/artipy/commit/18c54ef0bc92736dd2af0a177785fbb512f8edb8))

* ci: consistent naming of lint.yml job across workflows ([`4075bba`](https://github.com/trumully/artipy/commit/4075bba1086355440248bd5add0c1747bda42af3))

* ci: add ruff to lint &amp; format job ([`a7f637a`](https://github.com/trumully/artipy/commit/a7f637a5276f0e908f2de2d84db1bef261268629))

* ci: add pylint linting; adherence to Google styling ([`5094ace`](https://github.com/trumully/artipy/commit/5094acec7ed0ba3c0ca99b641c4c32767fc03054))

* ci: use latest black version ([`033ec16`](https://github.com/trumully/artipy/commit/033ec16c55f63d489fd4a5a9418723fe438e629c))

* ci: separate lint and test jobs ([`35e2931`](https://github.com/trumully/artipy/commit/35e29310af3566de28bc07d5c4c16f2b3ab4e86e))

* ci: use python 3.12.1 for black format job ([`3bab8c9`](https://github.com/trumully/artipy/commit/3bab8c930b7dc75511e15a91c17854ef2d60987c))

* ci: specify python &amp; poetry version for release job ([`5b8edea`](https://github.com/trumully/artipy/commit/5b8edea01e6f08c684e4c38c9b9b7336a834139d))

* ci: add format and lint job ([`9d12ea0`](https://github.com/trumully/artipy/commit/9d12ea0a5975981b408d1a0d6b25d9e5d2d1a3fd))

* ci: grant permission to docs job ([`3a298a1`](https://github.com/trumully/artipy/commit/3a298a12b9a2a9ac6bbf824692cff39aeb4d0cbb))

* ci: im no good at ci :( ([`40234de`](https://github.com/trumully/artipy/commit/40234dee7ec44d5049e08de569cd4e0d6b6783d8))

* ci: fix missing sphinx ([`f6f76d9`](https://github.com/trumully/artipy/commit/f6f76d9efa186c4250a3785401ed72a4de3e2b32))

* ci: remove if statement from documentation job ([`df64d2b`](https://github.com/trumully/artipy/commit/df64d2b9fe2ff050eaa874fa16871fca1b817fd6))

* ci: prepare ci for building documentation ([`25c5f30`](https://github.com/trumully/artipy/commit/25c5f30e19f3c25d0d4477417cf16c3b61ef4940))

### Documentation

* docs: thoroughly explain package usage in README with accompanying examples ([`f936c13`](https://github.com/trumully/artipy/commit/f936c13d84d933d0055b1bcb40094d6dbd684ab9))

* docs: add docs (pray) ([`1937d1e`](https://github.com/trumully/artipy/commit/1937d1e934444fa3066881fc121af88b907f5c31))

* docs: fix deployed docs ([`cdb5dab`](https://github.com/trumully/artipy/commit/cdb5dab04a933c28723e5970231a1bb2a2457f81))

* docs: auto generate w/ Sphinx ([`5f1a095`](https://github.com/trumully/artipy/commit/5f1a0955a063c7cb2e91c790f0cd63a378161c57))

* docs: add docstrings to any public methods missing one ([`e3337b3`](https://github.com/trumully/artipy/commit/e3337b3ec74d7ea30021a16f3cffa44478b80d4a))

### Fix

* fix(SubStat): use Stat.__str__() method driectly to avoid TypeError using super() ([`48d9354`](https://github.com/trumully/artipy/commit/48d9354db6a786cb94b5447c08d915fae951c86e))

### Performance

* perf: add slots to Stat superclass and inheriters ([`3d94bea`](https://github.com/trumully/artipy/commit/3d94bea0fcc7f7d3f18a773734a763f1b322f565))

### Style

* style: adhere to Google styling ([`68c890e`](https://github.com/trumully/artipy/commit/68c890e503aae3ef38662cfbfe1a8a1c3f359a9c))

### Unknown

* improvement(plot_artifact_substat_rolls): use matching color sequence for pie and bar chart ([`ccb1733`](https://github.com/trumully/artipy/commit/ccb1733ca4676adc838dc72809b9301ff7204b52))

* Delete CNAME ([`c35660e`](https://github.com/trumully/artipy/commit/c35660e3f03f192aa3df2eba3901a37354ceaf53))

* Create CNAME ([`4d77db5`](https://github.com/trumully/artipy/commit/4d77db5ffb618f725f4a882d7841ee32d4949928))


## v1.0.0 (2024-04-13)

### Chore

* chore(release): v1.0.0 [skip ci] ([`84a7e30`](https://github.com/trumully/artipy/commit/84a7e30bc0fc847d1df4a2f27f6c26c251d47cae))

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
