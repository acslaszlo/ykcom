from unittest.mock import call

import pytest

from src.ykcom import ykcom
from tests.packages_for_testing import p1


class TestYkcom:
    @pytest.mark.parametrize("target", ["os", ["os"], ("os",), {"os"}])
    def test_one_target(self, target: str | list[str] | tuple[str] | set[str]) -> None:
        with ykcom("tests.packages_for_testing.p1", target) as mocked:
            p1.mock_me("none")

            assert mocked.mocks["os"].mock_calls == [call.environ.__getitem__("none")]
            assert mocked.M.mock_calls == [call.os.environ.__getitem__("none")]

        with pytest.raises(KeyError):
            p1.mock_me("none")

    def test_target_in_args(self) -> None:
        with ykcom("tests.packages_for_testing.p1", "os", "sys") as mocked:
            p1.mock_me("none")

            assert mocked.mocks["sys"].mock_calls == [call.stdout.write("Some text\n")]
            assert mocked.mocks["os"].mock_calls == [call.environ.__getitem__("none")]
            assert mocked.M.mock_calls == [
                call.sys.stdout.write("Some text\n"),
                call.os.environ.__getitem__("none"),
            ]
