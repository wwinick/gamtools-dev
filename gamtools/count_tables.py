import numpy as np

########################################################
#
# Non-cythonized (i.e. slow) functions for counts tables
# (otherwise known as contingency tables).
#
########################################################

def get_transpositions(array):
    """
    Generator that iterates through all possible transpositions of
    an n-dimensional array.
    """

    axes = range(len(array.shape))
    for i in axes:
        yield tuple(axes[i:] + axes[:i])


def frequency_to_probability(counts_table):
    """
    Convert a contingency table expressed in frequencies to one
    expressed in probabilities.
    """

    total = counts_table.sum()
    probs_table = counts_table / float(total)

    return probs_table


def get_marginal_probabilities(probs_table):
    """
    Get the marginal probability of each event given a
    contingency table.
    """

    ind = []
    for t in get_transpositions(probs_table):
        marginal_probs = [probs_table.transpose(t)[1,...].sum(),
                 probs_table.transpose(t)[0,...].sum()]
        ind.append(marginal_probs)
    return np.array(ind)


def either_locus_not_detected(probs):
    """
    Returns True if the probability of any event in a contingency
    table is 0.
    """

    if probs.min() == 0.0:
        return True
    else:
        return False


def cosegregation(counts_table):
    """
    Return the co-segregation frequency of n loci given their
    contingency table.
    """

    probs_table = frequency_to_probability(counts_table)

    if either_locus_not_detected(probs_table):
        return np.NAN

    return probs_table.flat[-1]

def expected(counts_table):
    """
    Return the expected co-segregation probability of an arbitrary number
    of loci given their contingency table.
    """

    probs_table = frequency_to_probability(counts_table)
    marginal_probs = get_marginal_probabilities(probs_table)

    if either_locus_not_detected(marginal_probs):
        return np.NAN

    expected = marginal_probs.prod(axis=0)[0]
    return expected


def D(counts_table):
    """
    Return the linkage disequilibrium (D) for an arbitrary number of
    loci given their contingency table.
    """

    probs_table = frequency_to_probability(counts_table)
    marginal_probs = get_marginal_probabilities(probs_table)

    if either_locus_not_detected(marginal_probs):
        return np.NAN

    expected = marginal_probs.prod(axis=0)[0]
    observed = probs_table.flat[-1]
    if observed == 0:
        return np.NAN
    return observed - expected
