# -*- coding: utf-8 -*-

from .dice import dice
from .jaccard import jaccard
from .kulsinski import kulsinski
from .sokolsneath import sokolsneath
from .russelrao import russelrao
from .cosine import cosine
from .cosine_binary import cosine_binary

default_similarity = kulsinski
