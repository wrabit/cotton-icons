A package to provide popular icon packs for use with [Django Cotton](https://github.com/wrabit/django-cotton). For now, Heroicons is supported [heroicons](https://heroicons.com/).

## Install

**1. Install from pypi**

```
pip install django-icons
```

**2. Install into your django project**

```python
# settings.py
INSTALLED_APPS = [
  'django-icons'
]
```

**3. Use in template**

`<c-heroicon.[kebab-case heroicon name] variant="outline|solid|mini" [any other attribute will pass to the <svg> tag] />`

* `variant` defaults to `outline`
* for outline variant, you can also pass `stroke-width="" stroke_linecap="" stroke_linejoin=""` 

Examples:
   
```html
<c-heroicon.chevron-down class="size-5" /> <!-- default variant "outline" -->
<c-heroicon.chevron-down variant="solid" class="size-5" />
<c-heroicon.chevron-down variant="mini" class="size-5" />
```





### Roadmap

- Add Tabler.io icons


