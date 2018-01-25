from .fileinfo import FileInfo


class Diff:
    def __init__(self, diff_file):
        source_detail = diff_file.get("source", None)
        if source_detail is not None:
            self.source = FileInfo(diff_file["source"])
        else:
            self.source = None

        dest_detail = diff_file.get("destination", None)
        if dest_detail is not None:
            self.destination = FileInfo(diff_file["destination"])
        else:
            self.destination = None

        self.hunks = diff_file.get("hunks", [])
        self.truncated = diff_file.get("truncated", [])
        self.line_comments = diff_file.get("lineComments", [])

    def _get_source(self):
        return self._source

    def _set_source(self, value):
        self._source = value

    def _get_destination(self):
        return self._destination

    def _set_destination(self, value):
        self._destination = value

    def _get_hunks(self):
        return self._hunks

    def _set_hunks(self, value):
        self._hunks = value

    def _get_truncated(self):
        return self._truncated

    def _set_truncated(self, value):
        self._truncated = value

    def _get_line_comments(self):
        return self._line_comments

    def _set_line_comments(self, value):
        self._line_comments = value

    source = property(_get_source, _set_source, doc="The source of a file in the diff.")

    destination = property(_get_destination, _set_destination, doc="The destination of a file in the diff.")

    hunks = property(_get_hunks, _set_hunks, doc="A dictionary showing the hunks changed in the file difference.")

    truncated = property(_get_truncated, _set_truncated,
                         doc="Whether it has been truncated? I'm not actually sure what this value represents from the JSON response.")

    line_comments = property(_get_line_comments, _set_line_comments,
                             doc="The comments that have been made against a file in the pull request.")
