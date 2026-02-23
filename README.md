A package to provide popular icon packs for use with [Django Cotton](https://github.com/wrabit/django-cotton).
Currently, [Heroicons](https://heroicons.com/), [Tabler Icons](https://tabler.io/icons), and [Lucide Icons](https://lucide.dev/) are supported.

## Supported Icon Libraries

*   **Heroicons:** `v2.2.0`
*   **Tabler Icons:** `v3.37.1`
*   **Lucide Icons:** `v0.575.0` 

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

All attributes pass through to the `<svg>` tag. For stroke-based icons you can also pass `stroke-width`, `stroke-linecap`, and `stroke-linejoin`.

**Examples:**

```html
<c-heroicon.chevron-down class="size-5" />
<c-heroicon.chevron-down variant="solid" class="size-5" />
<c-heroicon.chevron-down variant="mini" class="size-5" />

<c-tablericon.graph class="size-5" />
<c-tablericon.graph variant="filled" class="size-5" />

<c-lucideicon.arrow-down class="size-5" />
<c-lucideicon.search class="size-5" stroke-width="3" />
```

### Roadmap

- [x] Add [Tabler Icons](https://tabler-icons.io/)
- [x] Add [Lucide Icons](https://lucide.dev/)


