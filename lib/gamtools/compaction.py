"""
======================
The compaction module
======================

The compaction module contains functions for calculating chromatin
compaction from GAM :ref:`segregation tables <segregation_table>`.

"""

import numpy as np

from .segregation import open_segregation

def get_compaction(segregation_data, no_blanks=False):
    """Get the compaction of each genomic window from a segregation table

    :param segregation_data: Segregation table generated by gamtools
    :returns: :class:`pandas.DataFrame` giving the compaction of each window
    """

    compaction = segregation_data.sum(axis=1)

    if no_blanks:
        compaction = compaction[
            np.logical_and(
                np.logical_not(compaction.isnull()),
                compaction > 0)]

    return compaction


def compaction_from_args(args):
    """Helper function to call compaction from doit"""

    segregation_data = open_segregation(args.segregation_file)

    compaction = get_compaction(segregation_data, args.no_blanks)

    compaction.to_csv(args.output_file, sep='\t')