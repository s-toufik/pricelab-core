from typing import Union

from pricelab_core.infrastructure.authentication.model.basic_auth import BasicAuth
from pricelab_core.infrastructure.authentication.model.no_auth import NoAuth
from pricelab_core.infrastructure.authentication.model.token_auth import TokenAuth

AuthTyping = Union[NoAuth, TokenAuth, BasicAuth]
