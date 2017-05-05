# -*- coding: utf-8 -*-

from .dice import dice
from .jaccard import jaccard
from .kulsinski import kulsinski
from .sokalsneath import sokalsneath
from .russellrao import russellrao
from .cosine import cosine
from .cosine_binary import cosine_binary

default_similarity = kulsinski
