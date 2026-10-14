# Changelog

All notable changes to cotton-icons are listed here. Icon set versions refer to the upstream release the templates were generated from.

## 0.3.0 - 2026-10-14

### Breaking

- **Lucide 1.0 removed 18 brand logos** and they are gone from `c-lucideicon`: `chromium`, `codepen`, `codesandbox`, `dribbble`, `facebook`, `figma`, `framer`, `github`, `gitlab`, `instagram`, `linkedin`, `pocket`, `rail-symbol`, `slack`, `trello`, `twitch`, `twitter`, `youtube`. Lucide's brand logos policy rules out adding them back. 16 of them exist in Tabler under the `brand-` prefix, for example `<c-lucideicon.github />` becomes `<c-tablericon.brand-github />`. `chromium` and `rail-symbol` have no equivalent in any bundled set. ([#6](https://github.com/wrabit/cotton-icons/issues/6), [#11](https://github.com/wrabit/cotton-icons/pull/11))

### Changed

- **All icons now render `aria-hidden="true"` by default**, across Heroicons, Tabler and Lucide. Icons are decorative unless you say otherwise. Override with `aria-hidden="false"` and give the icon a label. Heroicons already carried the attribute but hardcoded it before `{{ attrs }}`, so it could not be overridden; that is fixed too. Screen reader output changes for any icon that was relied on without a label. ([#7](https://github.com/wrabit/cotton-icons/issues/7), [#9](https://github.com/wrabit/cotton-icons/pull/9))
- **Lucide updated from 0.575.0 to 1.57.0.** 1701 icons become 1890: 224 added, 132 with updated artwork, 17 renamed, 18 removed (see Breaking). ([#11](https://github.com/wrabit/cotton-icons/pull/11))
- Heroicons `gift` restored to the artwork released in v2.2.0. The previous copy came from a later unreleased commit. ([#10](https://github.com/wrabit/cotton-icons/pull/10))

### Added

- **Lucide Lab** as a new namespace, `<c-lucidelab.icon-name />`, 354 experimental icons from the `lab/` directory of the Lucide 1.57.0 release. Lab icons may be renamed, removed or promoted to the main set between Lucide releases. There is no name overlap with the main set. ([#6](https://github.com/wrabit/cotton-icons/issues/6), [#11](https://github.com/wrabit/cotton-icons/pull/11))
- **Lucide aliases.** The 264 deprecated aliases Lucide records in its icon metadata are generated as forwarding templates, so a renamed icon still works under its old name and renders identically, for example `<c-lucideicon.trash-2 />` renders `trash` and `<c-lucideicon.smile />` renders `face-slightly-smiling`. Prefer the new names; aliases disappear when Lucide drops them. The mapping is in `lucideicon/icon_map.json` under `aliases`. ([#11](https://github.com/wrabit/cotton-icons/pull/11))
- `CHANGELOG.md`.

### Internal

- Generators clone the latest upstream release tag instead of the default branch, so the icons and the reported version always come from the same commit. Previously a run could include icons merged after a release and miss others from it, which is how 0.2.0 shipped the Lucide 0.576.0 zodiac icons without `fishing-rod`. Tag resolution uses `git ls-remote`, no GitHub API. ([#6](https://github.com/wrabit/cotton-icons/issues/6), [#10](https://github.com/wrabit/cotton-icons/pull/10))
- Generators empty their output directory before writing, so icons removed upstream no longer linger. ([#10](https://github.com/wrabit/cotton-icons/pull/10))
- The Lucide `icon_map.json` gains `source` (`icons` or `lab`) and `aliases`.

### Unchanged

- Heroicons 2.2.0 and Tabler 3.37.1.

## 0.2.0 - 2026-02-23

### Added

- Lucide Icons 0.575.0 as `<c-lucideicon.icon-name />`, 1701 icons. ([#5](https://github.com/wrabit/cotton-icons/pull/5))

### Changed

- Heroicons updated from 2.1.5 to 2.2.0.
- Tabler Icons updated from 3.34.0 to 3.37.1, 4963 icons become 4986.

## 0.1.0 - 2025-06-13

### Added

- Tabler Icons 3.34.0 as `<c-tablericon.icon-name />`, 4963 icons with `outline` and `filled` variants. ([#2](https://github.com/wrabit/cotton-icons/pull/2), [#3](https://github.com/wrabit/cotton-icons/pull/3))

### Changed

- README corrected to the right package and app names. ([#1](https://github.com/wrabit/cotton-icons/pull/1), thanks @danhayden)

## 0.0.2 - 2025-03-08

First release. Heroicons as `<c-heroicon.icon-name />`, 324 icons with `outline`, `solid`, `mini` and `micro` variants.
