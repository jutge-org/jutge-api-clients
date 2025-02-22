# PREAMBLE_HERE


# In order to use this module, you should install its dependencies using pip:
# python3 -m pip install requests requests-toolbelt pyyaml rich pydantic
# A recent version of Python (3.11 or newer) is required.


# pyright: reportUnusedVariable=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownMemberType=false
# pyright: reportUnknownArgumentType=false

# pylint: disable=line-too-long, too-many-lines, unused-variable, fixme, redefined-builtin, too-many-instance-attributes, too-few-public-methods, too-many-locals

from __future__ import annotations

import json
import os
import re
from typing import Any, Type, Optional, BinaryIO
from pydantic import BaseModel, TypeAdapter, Field
from pydantic_core import to_jsonable_python
from requests_toolbelt.multipart import decoder  # type: ignore
from rich import print
import yaml
import requests


# Models

# MODELS_HERE


# exceptions
class UnauthorizedException(Exception):
    """Class UnauthorizedException"""


class InfoException(Exception):
    """Class InfoException"""


class NotFoundException(Exception):
    """Class NotFoundException"""


class InputException(Exception):
    """Class InputException"""


class ProtocolException(Exception):
    """Class ProtocolException"""


class Download(BaseModel):
    """Class for downloaded files (ofiles)"""

    data: bytes
    name: str
    type: str

    def write(self, path: str) -> None:
        """Write the content of the download to the file at the given path."""

        with open(path, "wb") as file:
            file.write(self.data)


def _build(x: Any, t: Any) -> Any:
    try:
        return t.model_validate(x)
    except Exception:
        try:
            return TypeAdapter(t).validate_python(x)
        except Exception:
            return x


def _debuild(x: Any) -> Any:
    if isinstance(x, BaseModel):
        return x.model_dump()
    if isinstance(x, list):
        return [_debuild(v) for v in x]
    if isinstance(x, dict):
        return {k: _debuild(v) for k, v in x.items()}
    return x


def _raise_exception(error: dict[str, Any], operation_id: str | None) -> None:
    # TODO: do something with operation_id
    message = error.get("message", "Unknown error")
    if error["name"] == "UnauthorizedError":
        raise UnauthorizedException(message)
    if error["name"] == "InfoError":
        raise InfoException(message)
    if error["name"] == "NotFoundError":
        raise NotFoundException(message)
    if error["name"] == "InputError":
        raise InputException(message)
    raise Exception("Unknown error")


class Util:
    """
    Utility class with static methods to convert between JSON and YAML formats.
    """

    @staticmethod
    def from_json[T](s: str, t: Type[T]) -> T:
        """Parse a JSON string into a Python object"""

        return TypeAdapter(t).validate_json(s)

    @staticmethod
    def to_json(obj: Any) -> str:
        """Convert a Python object into a JSON string"""

        return json.dumps(obj, default=to_jsonable_python, ensure_ascii=False)

    @staticmethod
    def json_to_yaml(s: str) -> str:
        """Convert a JSON string into a YAML string"""

        return yaml.dump(json.loads(s), allow_unicode=True, indent=4)

    @staticmethod
    def yaml_to_json(s: str) -> str:
        """Convert a YAML string into a JSON string"""

        return json.dumps(yaml.safe_load(s), ensure_ascii=False)

    @staticmethod
    def to_yaml(obj: Any) -> str:
        """Convert a Python object into a YAML string"""
        return Util.json_to_yaml(Util.to_json(obj))

    @staticmethod
    def from_yaml[T](s: str, t: Type[T]) -> T:
        """Convert a YAML string into a Python object"""
        return Util.from_json(Util.yaml_to_json(s), t)


class JutgeApiClient:
    """
    Client to interact with the Jutge API.
    """

    JUTGE_API_URL: str = os.environ.get("JUTGE_API_URL", "https://api.jutge.org/api")

    _meta: Any | None = None

    # MAIN_MODULE_HERE

    def execute(self, func: str, input: Any, ifiles: list[BinaryIO] | None = None) -> tuple[Any, list[Download]]:
        """Function that sends a request to the API and returns the response"""

        data = {"func": func, "input": input, "meta": self._meta}
        files = {}
        if ifiles is not None:
            for i, ifile in enumerate(ifiles):
                files["file_" + str(i)] = ifile
        response = requests.post(self.JUTGE_API_URL, data={"data": json.dumps(data)}, files=files)
        content_type = response.headers.get("content-type", "").split(";")[0].lower()
        if content_type != "multipart/form-data":
            raise ProtocolException("The content type is not multipart/form-data")

        ofiles = []
        answer = None
        multipart_data = decoder.MultipartDecoder.from_response(response)

        for part in multipart_data.parts:

            def get(x: bytes) -> str:
                """Helper function to get a header from a part and decode it without warnings"""
                return part.headers.get(x, "").decode("utf-8")  # type: ignore

            if b"Content-Type" in part.headers:
                filenames = re.findall('filename="(.+)"', get(b"Content-Disposition"))
                if len(filenames) != 1:
                    raise ProtocolException("The part does not have a filename")
                filename = filenames[0]
                type = get(b"Content-Type")
                ofiles.append(Download(data=part.content, name=filename, type=type))
            else:
                if answer is not None:
                    raise ProtocolException("There are multiple parts with JSON content")
                answer = json.loads(part.content)

        if not isinstance(answer, dict):
            raise ProtocolException("The answer is not an object")

        output = answer.get("output", None)
        operation_id = answer.get("operation_id", None)

        if "error" in answer:
            _raise_exception(answer["error"], operation_id)

        return output, ofiles

    def login(self, email: str, password: str) -> CredentialsOut:
        """
        Simple login to the API.

        Attempts to login with the provided email and password.
            - If successful, it returns the credentials and sets the _meta attribute so that the following requests are authenticated.
            - If not, it raises an UnauthorizedException exception.
        """

        input = {"email": email, "password": password}
        credentials_out, _ = self.execute("auth.login", input)
        if credentials_out["error"] != "":
            raise UnauthorizedException(credentials_out["error"])
        self._meta = {
            "token": credentials_out["token"],
            "exam": None,
        }
        return CredentialsOut(**credentials_out)

    def logout(self, silent: bool = False) -> None:
        """
        Simple logout from the API.
        """

        try:
            self.execute("auth.logout", None)
        except UnauthorizedException:
            pass
        except Exception as e:
            if not silent:
                print("[red]Error at log out[/red]")
            else:
                raise e
        finally:
            self._meta = None
            if not silent:
                print("[green]Logged out[/green]")


# MODULES_HERE
