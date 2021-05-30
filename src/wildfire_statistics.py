from collections import defaultdict, namedtuple
import warnings

import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import uniform, expon


def sum_different_length_arrays(a, b):
    if len(a) < len(b):
        c = b.copy()
        c[:len(a)] += a
    else:
        c = a.copy()
        c[:len(b)] += b
    return c


def make_weighted_disturbance_pdf(annual_area_affected_by_wildfire):
    """Create a uniform

    Parameters
    ------
    annual_area_affected_by_wildfire: arraylike
        Elements represent the annual fraction of total
        land area affected by wildfire in a region.

    Returns
    ------
    weighted_uniform_rvs : ndarray
        random variates generated from each value of `annual_area_affected_by_wildfire`.

    """
    x_max = None
    x_min = None
    steps = None

    weighted_uniform_pdf = np.array([])
    area_fractions = np.array([])

    for area_fraction in annual_area_affected_by_wildfire:
        expected_end_date = 1/area_fraction
        area_fractions = np.append(area_fractions, area_fraction)
        x = np.arange(expected_end_date)
        x_min, x_max, steps = _update_linspace_params(x, x_min, x_max, steps)
        new_pdf = uniform.pdf(x=x, loc=0, scale=expected_end_date)
        weighted_uniform_pdf = sum_different_length_arrays(weighted_uniform_pdf, new_pdf)
    print(f'minimum annual fraction of area disturbed: {min(area_fractions)}')

    # renormalize pdf (each step is one year)
    weighted_uniform_pdf = weighted_uniform_pdf/sum(weighted_uniform_pdf)
    return weighted_uniform_pdf, np.linspace(x_min, x_max, num=steps)


def _update_linspace_params(x, x_min, x_max, steps):
    min_ = np.min(x)
    max_ = np.max(x)
    steps_ = len(x)

    if x_min is None:
        x_min = min_
        x_max = max_
        steps = steps_
    else:
        if min_ < x_min:
            x_min = min_
        if max_ > x_max:
            x_max = max_
        if steps_ > steps:
            steps = steps_
    return x_min, x_max, steps


def exp_sum_stats(x, w, scale1, scale2):
    return w*expon.pdf(x, scale=scale1) + (1-w)*expon.pdf(x, scale=scale2)


def fit_wildfire_statistics(annual_stats, eco_unit_column):
    """Fitting wildfire pdfs for spatial units in annual_stats."""

    PDF_Params = namedtuple('PDF_Params', ['w', 'scale1', 'scale2'])
    eco_unit_wildfire_stats = defaultdict()

    for eco_unit in annual_stats[eco_unit_column].unique():
        print(f'eco-unit: {eco_unit}')
        eco_unit_stats = annual_stats[annual_stats[eco_unit_column] == eco_unit]
        annual_area_affected_by_wildfire = eco_unit_stats.LAND_AREA_FRACTION
        samples = annual_area_affected_by_wildfire.shape[0]
        try:
            uniform_pdf, x_range = make_weighted_disturbance_pdf(annual_area_affected_by_wildfire)
        except MemoryError:
            warnings.warn(f'make_weighted_disturbance_pdf() causing MemoryError for {eco_unit}.')
            continue
        try:
            params, cov = curve_fit(
                exp_sum_stats,
                xdata=x_range,
                ydata=uniform_pdf,
                bounds=((0., 1., 1.), (1., np.inf, np.inf)))
        except MemoryError:
            warnings.warn(f'curve_fit() causing MemoryError for uniform_pdf of length {len(uniform_pdf)}.')
            continue
        print(f'params: {params}, samples: {samples}')
        eco_unit_wildfire_stats[eco_unit] = {
            'params': PDF_Params(*params)._asdict(),
            'samples': samples}
    return eco_unit_wildfire_stats
