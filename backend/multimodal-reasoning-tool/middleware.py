# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import TypeVar

import firebase_admin
from firebase_admin import auth  # noqa: F401
from firebase_admin import credentials

from flask import request, Response
import structlog


# Constants
SERVICE_ACCOUNT_FILE = "cecl-genai-demos.json" # TODO: replace with your service account file

a = TypeVar("a")

# Initialize firebase admin
cred = credentials.Certificate(SERVICE_ACCOUNT_FILE)
default_app = firebase_admin.initialize_app(cred)


# [START cloudrun_user_auth_jwt]
def jwt_authenticated(func: Callable[..., int]) -> Callable[..., int]:
    """Use the Firebase Admin SDK to parse Authorization header to verify the
    user ID token.

    The server extracts the Identity Platform uid for that user.
    """

    @wraps(func)
    def decorated_function(*args: a, **kwargs: a) -> a:
        header = request.headers.get("Authorization", None)
        if header:
            token = header.split(" ")[1]
            try:
                decoded_token = firebase_admin.auth.verify_id_token(token)
            except Exception as e:
                logger.exception(e)
                return Response(status=403, response=f"Error with authentication: {e}")
        else:
            return Response(status=401)

        request.uid = decoded_token["uid"]
        return func(*args, **kwargs)

    return decorated_function


# [END cloudrun_user_auth_jwt]

# adapted from https://github.com/ymotongpoo/cloud-logging-configurations/blob/master/python/structlog/main.py


def field_name_modifier(
    logger: structlog._loggers.PrintLogger, log_method: str, event_dict: dict
) -> dict:
    """A structlog processor for mapping fields to Cloud Logging.
    Learn more at https://www.structlog.org/en/stable/processors.html

    Args:
        logger: A logger object.
        log_method: The name of the wrapped method.
        event_dict:Current context together with the current event.

    Returns:
        A structlog processor.
    """
    # Changes the keys for some of the fields, to match Cloud Logging's expectations
    event_dict["severity"] = event_dict["level"]
    del event_dict["level"]
    event_dict["message"] = event_dict["event"]
    del event_dict["event"]
    return event_dict


def getJSONLogger() -> structlog._config.BoundLoggerLazyProxy:
    """Initialize a logger configured for JSON structured logs.

    Returns:
        A configured logger object.
    """
    # extend using https://www.structlog.org/en/stable/processors.html
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            field_name_modifier,
            structlog.processors.TimeStamper("iso"),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
    )
    return structlog.get_logger()


logger = getJSONLogger()


def logging_flush() -> None:
    # Setting PYTHONUNBUFFERED in Dockerfile ensured no buffering
    pass
