# cupy_rungekutta
CuPy port of SciPy's Runge-Kutta code.

This copies substantial portions of SciPy source code and as such (presumably) needs to be distributed under the same license, BSD 3-clause.

## "Installation"

Put these files somewhere on your `$PYTHONPATH`, e.g., in whatever the output of
```
$ python -m site --user-site
```
is (should be `~/.local/lib/python3.X/site-packages` for some `X`).

Naturally, this depends on CuPy and its dependencies.
