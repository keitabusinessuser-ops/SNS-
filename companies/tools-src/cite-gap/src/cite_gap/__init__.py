"""cite-gap: 文章中の数字・断定に、出典か「未確認」の印があるかを点検する。

真偽は判定しない。外部通信はしない。
"""

from .core import Finding, Reason, Report, check_text, __version__

__all__ = ["Finding", "Reason", "Report", "check_text", "__version__"]
