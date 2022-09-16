import re
import codecs
import encodings
import functools


def transform(string, decode_mode):
    string = bytes(string).decode("utf-8")

    postfix_pluses  = r"\w+\+\+"
    prefix_pluses   = r"\+\+\w+"
    postfix_minuses = r"\w+\-\-"
    prefix_minuses  = r"\-\-\w+"
    base_regexp = lambda doesnt_capture, captures: '["\'].*{}.*["\']|{}'.format(doesnt_capture, captures)

    patterns = [
        re.compile(base_regexp(doesnt_capture, captures))
        for captures, doesnt_capture in (
                (f"({postfix_pluses})",  postfix_pluses ), # a++
                (f"({prefix_pluses})",   prefix_pluses  ), # ++a
                (f"({postfix_minuses})", postfix_minuses), # a--
                (f"({prefix_minuses})",  prefix_minuses ), # --a
        )
    ]

    replacements = [
        lambda symbol: "(({0}, {0} := {0}+1)[0])".format(symbol), # a++
        lambda symbol: "(({0}, {0} := {0}+1)[1])".format(symbol), # ++a
        lambda symbol: "(({0}, {0} := {0}-1)[0])".format(symbol), # a--
        lambda symbol: "(({0}, {0} := {0}-1)[1])".format(symbol), # --a
    ]

    lines = []

    for line in string.splitlines(keepends=True):
        for pattern, replacement in zip(patterns, replacements):

            for match_obj in re.finditer(pattern, line):
                captured ,= match_obj.groups()
                if captured:
                    exact_pattern = captured.replace("+", "\+").replace("-", "\-")
                    symbol = captured.strip("-+")
                    line = re.sub(exact_pattern, replacement(symbol), line)

        lines.append(line.encode() if not decode_mode else line)

    if decode_mode:
        text = "".join(lines)
        return text, len(text)
    else:
        text = b"".join(lines)
        return text


decoder = functools.partial(transform, decode_mode=True)
encoder = functools.partial(transform, decode_mode=False)


class IncrementalDecoder(encodings.utf_8.IncrementalDecoder):
    def decode(self, string, final=False):
        self.buffer += string
        if final:
            buffer = self.buffer
            self.buffer = b""
            return super().decode(encoder(buffer))
        return ""


def incdec_codec(encoding):
    if encoding == "incdec":
        return codecs.CodecInfo(
            name="incdec",
            encode=encodings.utf_8.encode,
            decode=decoder,
            incrementaldecoder=IncrementalDecoder,
        )


codecs.register(incdec_codec)
