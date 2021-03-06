# -*- coding: utf-8 -*-

from .collaborativefiltering import CollaborativeFiltering
from .truncatedsvd import TruncatedSVD
from .mostpopular import MostPopular
from .baselines import Baseline, default_baseline

DefaultAlgorithm = CollaborativeFiltering
