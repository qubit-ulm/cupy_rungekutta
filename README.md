# cupy_rungekutta
CuPy port of SciPy's Runge-Kutta code.

This copies substantial portions of SciPy source code and as such (presumably) needs to be distributed under the same license, BSD 3-clause.

Naturally, this depends on CuPy and its dependencies.

## How to use
This module (`cupy_rungekutta`) provides CuPy functionality for a subset of `scipy.integrate` routines, in particular `scipy.integrate.RK45`.
This means that `cupy_rungekutta.RK45` can be called on `cupy` arrays to the same effect as `scipy.integrate.RK45` acting on NumPy arrays.
To achieve this, either place the directory `cupy_rungekutta` directly inside the working directory, or see the next section "Installation".

### "Installation"
Put these files somewhere on your `$PYTHONPATH`, e.g., in whatever the output of
```
$ python -m site --user-site
```
is (should be `~/.local/lib/python3.X/site-packages` for some `X`).
