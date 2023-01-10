from .ex_functions import *
from .config import petpet_config

ex_memes:List[Meme] = [
    
]

ex_memes = [meme for meme in ex_memes if meme.name not in petpet_config.petpet_disabled_list]