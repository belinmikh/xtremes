import io
from csv import DictReader

from aiofile import LineReader


class AsyncDictReader:
    """Source: https://pypi.org/project/aiofile/"""

    def __init__(self, afp, **kwargs):
        self.buffer = io.BytesIO()
        self.file_reader = LineReader(
            afp,
            line_sep=kwargs.pop("line_sep", "\n"),
            chunk_size=kwargs.pop("chunk_size", 4096),
            offset=kwargs.pop("offset", 0),
        )
        self.reader = DictReader(
            io.TextIOWrapper(
                self.buffer,
                encoding=kwargs.pop("encoding", "utf-8"),
                errors=kwargs.pop("errors", "replace"),
            ),
            **kwargs,
        )
        self.line_num = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.line_num == 0:
            header = await self.file_reader.readline()
            self.buffer.write(header)

        line = await self.file_reader.readline()

        if not line:
            raise StopAsyncIteration

        self.buffer.write(line)
        self.buffer.seek(0)

        try:
            result = next(self.reader)
        except StopIteration as e:
            raise StopAsyncIteration from e

        self.buffer.seek(0)
        self.buffer.truncate(0)
        self.line_num = self.reader.line_num

        return result
