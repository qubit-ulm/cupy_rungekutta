from warnings import warn
import cupy

EPS = cupy.finfo(float).eps


def validate_first_step(first_step, t0, t_bound):
    """Assert that first_step is valid and return it."""
    if first_step <= 0:
        raise ValueError("`first_step` must be positive.")
    if first_step > cupy.abs(t_bound - t0):
        raise ValueError("`first_step` exceeds bounds.")
    return first_step


def validate_max_step(max_step):
    """Assert that max_Step is valid and return it."""
    if max_step <= 0:
        raise ValueError("`max_step` must be positive.")
    return max_step


def warn_extraneous(extraneous):
    """Display a warning for extraneous keyword arguments.

    The initializer of each solver class is expected to collect keyword
    arguments that it doesn't understand and warn about them. This function
    prints a warning for each key in the supplied dictionary.

    Parameters
    ----------
    extraneous : dict
        Extraneous keyword arguments
    """
    if extraneous:
        warn("The following arguments have no effect for a chosen solver: {}."
             .format(", ".join("`{}`".format(x) for x in extraneous)))


def validate_tol(rtol, atol, n):
    """Validate tolerance values."""

    if cupy.any(cupy.asarray(rtol < 100 * EPS)):
        warn("At least one element of `rtol` is too small. "
             f"Setting `rtol = cupy.maximum(rtol, {100 * EPS})`.")
        rtol = cupy.maximum(rtol, 100 * EPS)

    atol = cupy.asarray(atol)
    if atol.ndim > 0 and atol.shape != (n,):
        raise ValueError("`atol` has wrong shape.")

    if cupy.any(atol < 0):
        raise ValueError("`atol` must be positive.")

    return rtol, atol


def norm(x):
    """Compute RMS norm."""
    return cupy.linalg.norm(x) / x.size ** 0.5


def select_initial_step(fun, t0, y0, f0, direction, order, rtol, atol):
    """Empirically select a good initial step.

    The algorithm is described in [1]_.

    Parameters
    ----------
    fun : callable
        Right-hand side of the system.
    t0 : float
        Initial value of the independent variable.
    y0 : ndarray, shape (n,)
        Initial value of the dependent variable.
    f0 : ndarray, shape (n,)
        Initial value of the derivative, i.e., ``fun(t0, y0)``.
    direction : float
        Integration direction.
    order : float
        Error estimator order. It means that the error controlled by the
        algorithm is proportional to ``step_size ** (order + 1)`.
    rtol : float
        Desired relative tolerance.
    atol : float
        Desired absolute tolerance.

    Returns
    -------
    h_abs : float
        Absolute value of the suggested initial step.

    References
    ----------
    .. [1] E. Hairer, S. P. Norsett G. Wanner, "Solving Ordinary Differential
           Equations I: Nonstiff Problems", Sec. II.4.
    """
    if y0.size == 0:
        return cupy.inf

    scale = atol + cupy.abs(y0) * rtol
    d0 = norm(y0 / scale)
    d1 = norm(f0 / scale)
    if d0 < 1e-5 or d1 < 1e-5:
        h0 = 1e-6
    else:
        h0 = 0.01 * d0 / d1

    y1 = y0 + h0 * direction * f0
    f1 = fun(t0 + h0 * direction, y1)
    d2 = norm((f1 - f0) / scale) / h0

    if d1 <= 1e-15 and d2 <= 1e-15:
        h1 = max(1e-6, h0 * 1e-3)
    else:
        h1 = (0.01 / max(d1, d2)) ** (1 / (order + 1))

    return min(100 * h0, h1)

