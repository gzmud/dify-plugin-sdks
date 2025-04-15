import httpx
from pydantic import BaseModel

from dify_plugin.file.constants import DIFY_FILE_IDENTITY
from dify_plugin.file.entities import FileType
from urllib.parse import urljoin

class File(BaseModel):
    dify_model_identity: str = DIFY_FILE_IDENTITY
    url: str
    mime_type: str | None = None
    filename: str | None = None
    extension: str | None = None
    size: int | None = None
    type: FileType

    _blob: bytes | None = None
    base_url: str | None = None

    @property
    def blob(self) -> bytes:
        """
        Get the file content as a bytes object.

        If the file content is not loaded yet, it will be loaded from the URL and stored in the `_blob` attribute.
        """
        effective_url = urljoin(self.base_url, self.url) if self.base_url is not None else self.url
        if self._blob is None:
            response = httpx.get(effective_url)
            response.raise_for_status()
            self._blob = response.content

        assert self._blob is not None
        return self._blob
