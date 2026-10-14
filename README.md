A package to provide popular icon packs for use with [Django Cotton](https://github.com/wrabit/django-cotton).
Currently, [Heroicons](https://heroicons.com/), [Tabler Icons](https://tabler.io/icons), [Lucide Icons](https://lucide.dev/) and [Lucide Lab](https://github.com/lucide-icons/lucide/tree/main/lab) are supported.

## Supported Icon Libraries

*   **Heroicons:** `v2.2.0`
*   **Tabler Icons:** `v3.37.1`
*   **Lucide Icons:** `v1.57.0`
*   **Lucide Lab:** `v1.57.0`

## Install

**1. Install from pypi**

```
pip install cotton-icons
```

**2. Install into your django project**

```python
# settings.py
INSTALLED_APPS = [
  'cotton_icons'
]
```

**3. Use in template**

| Library | Syntax | Variants | Default |
|---------|--------|----------|---------|
| Heroicons | `<c-heroicon.icon-name />` | `outline`, `solid`, `mini`, `micro` | `outline` |
| Tabler | `<c-tablericon.icon-name />` | `outline`, `filled` | `outline` |
| Lucide | `<c-lucideicon.icon-name />` | - | - |
| Lucide Lab | `<c-lucidelab.icon-name />` | - | - |

All attributes pass through to the `<svg>` tag. For stroke-based icons you can also pass `stroke-width`, `stroke-linecap`, and `stroke-linejoin`.

Icons are treated as decorative and render with `aria-hidden="true"` by default. If an icon carries meaning on its own, override it and give it a label:

```html
<c-heroicon.magnifying-glass aria-hidden="false" aria-label="Search" />
```

**Examples:**

```html
<c-heroicon.chevron-down class="size-5" />
<c-heroicon.chevron-down variant="solid" class="size-5" />
<c-heroicon.chevron-down variant="mini" class="size-5" />

<c-tablericon.graph class="size-5" />
<c-tablericon.graph variant="filled" class="size-5" />

<c-lucideicon.arrow-down class="size-5" />
<c-lucideicon.search class="size-5" stroke-width="3" />

<c-lucidelab.coconut class="size-5" />
```

Lucide Lab holds experimental icons that may be renamed, removed or promoted into the main set between releases. They live in their own namespace so that is visible where you use them and so a lab icon can never shadow a main one.


