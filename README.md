A package to provide popular icon packs for use with [Django Cotton](https://github.com/wrabit/django-cotton).
Currently, [Heroicons](https://heroicons.com/) and [Tabler Icons](https://tabler-icons.io/) are supported.

## Supported Icon Libraries

*   **Heroicons:** `v2.1.5` 
*   **Tabler Icons:** `v3.34.0` 

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

`<c-heroicon.[kebab-case heroicon name] variant="outline|solid|mini" [any other attribute will pass to the <svg> tag] />`
`<c-tablericon.[kebab-case tabler icon name] variant="outline|filled" [any other attribute will pass to the <svg> tag] />`

* `variant` defaults to `outline`
* for outline variant, you can also pass `stroke-width="" stroke_linecap="" stroke_linejoin=""` 

Examples:
   
```html
<c-heroicon.chevron-down class="size-5" /> <!-- default variant "outline" -->
<c-heroicon.chevron-down variant="solid" class="size-5" />
<c-heroicon.chevron-down variant="mini" class="size-5" />
```
   
```html
<c-tablericon.graph class="size-5" /> <!-- default variant "outline" -->
<c-tablericon.graph variant="filled" class="size-5" />
```

### Roadmap

- [x] Add [Tabler Icons](https://tabler-icons.io/)


