# pudzu

## Summary

Various Python 3 utility functions, mostly geared towards dataviz and used to create visualisations such as this [bar chart](https://raw.githubusercontent.com/Udzu/pudzu/master/dataviz/ukelections.png), [time chart](https://raw.githubusercontent.com/Udzu/pudzu/master/dataviz/g7.png), [periodic table](https://raw.githubusercontent.com/Udzu/pudzu/master/dataviz/periodic.png)  and [image grid](https://raw.githubusercontent.com/Udzu/pudzu/master/dataviz/40under40.png).

The modules aren't properly packaged up or pip-able (yet) but are reasonably simple, generic and docstringed. They are not optimised for speed or tested for resilience. They are targeted at for-fun, interactive work.

## Modules

- [utils.py](utils.md) - various utility functions and data structures.
- [dates.py](dates.md) - date classes supporting flexible calendars, deltas and ranges.
- [records.py](records.md) - utilities for functional handling of records (lists of dicts).
- [pillar.py](pillar.md) - various monkey-patched Pillow utilities.
- [charts.py](charts.md) - Pillow-based charting tools.
- *tureen.py* - various BeautifulSoup utilities.
- *wikipage.py* - wikipedia and wikidata parsing utilities.

## Copyright

Copyright © 2017 by Udzu. Licensed under the [MIT License](LICENSE).
