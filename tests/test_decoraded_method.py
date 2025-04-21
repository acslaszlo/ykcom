from unittest.mock import MagicMock, call

from src.ykcom import ykcom
from tests.packages_for_testing import p1


class TestDecoratedMethod:
    @ykcom("tests.packages_for_testing.p1", "os")
    def test_one_target_pos(self, mocked: MagicMock) -> None:
        p1.mock_me("none")

        assert mocked.os.mock_calls == [call.environ.__getitem__("none")]
        assert mocked.mock_calls == [call.os.environ.__getitem__("none")]

    @ykcom("tests.packages_for_testing.p1", "os", "sys")
    def test_multiple_targets_pos(self, mocked: MagicMock) -> None:
        p1.mock_me("none")

        assert mocked.os.mock_calls == [call.environ.__getitem__("none")]
        assert mocked.sys.mock_calls == [call.stdout.write("Some text\n")]
        assert mocked.mock_calls == [
            call.sys.stdout.write("Some text\n"),
            call.os.environ.__getitem__("none"),
        ]

    @ykcom("tests.packages_for_testing.p1", "os", name="custom_name")
    def test_one_target_named(self, custom_name: MagicMock) -> None:
        p1.mock_me("none")

        assert custom_name.os.mock_calls == [call.environ.__getitem__("none")]
        assert custom_name.mock_calls == [call.os.environ.__getitem__("none")]

    @ykcom("tests.packages_for_testing.p1", "os", "sys", name="custom_name")
    def test_multiple_targets_named(self, custom_name: MagicMock) -> None:
        p1.mock_me("none")

        assert custom_name.os.mock_calls == [call.environ.__getitem__("none")]
        assert custom_name.sys.mock_calls == [call.stdout.write("Some text\n")]
        assert custom_name.mock_calls == [
            call.sys.stdout.write("Some text\n"),
            call.os.environ.__getitem__("none"),
        ]

    @ykcom("tests.packages_for_testing.p1", "os")
    def test_positional_with_fixture(self, mocked: MagicMock, some_key: str) -> None:
        p1.mock_me(some_key)

        assert mocked.os.mock_calls == [call.environ.__getitem__(some_key)]
        assert mocked.mock_calls == [call.os.environ.__getitem__(some_key)]

    @ykcom("tests.packages_for_testing.p1", "os", name="custom_name")
    def test_named_with_fixture(self, some_key: str, custom_name: MagicMock) -> None:
        p1.mock_me(some_key)

        assert custom_name.os.mock_calls == [call.environ.__getitem__(some_key)]
        assert custom_name.mock_calls == [call.os.environ.__getitem__(some_key)]

    # TODO two pos mocks

    @ykcom("tests.packages_for_testing.p1", "os", name="custom_name")  # TODO multiple targets?
    @ykcom("tests.packages_for_testing.p1", "sys", name="custom_name_2")  # TODO multiple targets?
    def test_multiple_decorated_named(self, custom_name: MagicMock, custom_name_2: MagicMock) -> None:
        p1.mock_me("none")

        assert custom_name.os.mock_calls == [call.environ.__getitem__("none")]
        assert custom_name.mock_calls == [call.os.environ.__getitem__("none")]
        assert custom_name_2.sys.mock_calls == [call.stdout.write("Some text\n")]
        assert custom_name_2.mock_calls == [call.sys.stdout.write("Some text\n")]

    @ykcom("tests.packages_for_testing.p1", "os", name="custom_name")  # TODO multiple targets?
    @ykcom("tests.packages_for_testing.p1", "sys", name="custom_name")  # TODO multiple targets?
    def test_multiple_decorated_same_names_merged(self, custom_name: MagicMock) -> None:
        p1.mock_me("none")

        assert custom_name.os.mock_calls == [call.environ.__getitem__("none")]
        assert custom_name.sys.mock_calls == [call.stdout.write("Some text\n")]
        assert custom_name.mock_calls == [
            call.sys.stdout.write("Some text\n"),
            call.os.environ.__getitem__("none"),
        ]

    # TODO same name, different base path
    # TODO mixed mocks on same method
    # TODO
