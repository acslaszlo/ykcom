from unittest.mock import MagicMock, call

import pytest

from src.ykcom import ykcom
from src.ykcom.errors import TargetAlreadyBoundError
from tests.packages_for_testing import p1, p2


@ykcom("tests.packages_for_testing.p1", "os")
def test_standalone_function_one_target_pos(mocked: MagicMock) -> None:
    p1.mock_me("none")

    assert mocked.os.mock_calls == [call.environ.__getitem__("none")]
    assert mocked.mock_calls == [call.os.environ.__getitem__("none")]


@ykcom("tests.packages_for_testing.p1", ["os"])
def test_standalone_function_target_list_pos(mocked: MagicMock) -> None:
    p1.mock_me("none")

    assert mocked.os.mock_calls == [call.environ.__getitem__("none")]
    assert mocked.mock_calls == [call.os.environ.__getitem__("none")]


@ykcom("tests.packages_for_testing.p1", "os", name="custom_name")
def test_standalone_function_one_target_named(custom_name: MagicMock) -> None:
    p1.mock_me("none")

    assert custom_name.os.mock_calls == [call.environ.__getitem__("none")]
    assert custom_name.mock_calls == [call.os.environ.__getitem__("none")]


@ykcom("tests.packages_for_testing.p1", {"os"}, name="custom_name")
def test_standalone_function_target_set_named(custom_name: MagicMock) -> None:
    p1.mock_me("none")

    assert custom_name.os.mock_calls == [call.environ.__getitem__("none")]
    assert custom_name.mock_calls == [call.os.environ.__getitem__("none")]


@ykcom("tests.packages_for_testing.p1", "os")
def test_standalone_function_pos_with_fixture(mocked: MagicMock, some_key: str) -> None:
    p1.mock_me(some_key)

    assert mocked.os.mock_calls == [call.environ.__getitem__(some_key)]
    assert mocked.mock_calls == [call.os.environ.__getitem__(some_key)]


@ykcom("tests.packages_for_testing.p1", "os", name="custom_name")
def test_standalone_function_named_with_fixture(some_key: str, custom_name: MagicMock) -> None:
    p1.mock_me(some_key)

    assert custom_name.os.mock_calls == [call.environ.__getitem__(some_key)]
    assert custom_name.mock_calls == [call.os.environ.__getitem__(some_key)]


@pytest.mark.parametrize("param", [1, 2])
@ykcom("tests.packages_for_testing.p1", "os")
def test_standalone_function_pos_parametrized_before_decorator(mocked: MagicMock, param: int) -> None:
    key = f"none-{param}"

    p1.mock_me(key)

    assert mocked.os.mock_calls == [call.environ.__getitem__(key)]
    assert mocked.mock_calls == [call.os.environ.__getitem__(key)]


@ykcom("tests.packages_for_testing.p1", "os")
@pytest.mark.parametrize("param", [1, 2])
def test_standalone_function_pos_parametrized_after_decorator(mocked: MagicMock, param: int) -> None:
    key = f"none-{param}"

    p1.mock_me(key)

    assert mocked.os.mock_calls == [call.environ.__getitem__(key)]
    assert mocked.mock_calls == [call.os.environ.__getitem__(key)]


@pytest.mark.parametrize("param", [1, 2])
@ykcom("tests.packages_for_testing.p1", "os", name="custom_name")
def test_standalone_function_named_parametrized_before_decorator(custom_name: MagicMock, param: int) -> None:
    key = f"none-{param}"

    p1.mock_me(key)

    assert custom_name.os.mock_calls == [call.environ.__getitem__(key)]
    assert custom_name.mock_calls == [call.os.environ.__getitem__(key)]


@ykcom("tests.packages_for_testing.p1", "os", name="custom_name")
@pytest.mark.parametrize("param", [1, 2])
def test_standalone_function_named_parametrized_after_decorator(custom_name: MagicMock, param: int) -> None:
    key = f"none-{param}"

    p1.mock_me(key)

    assert custom_name.os.mock_calls == [call.environ.__getitem__(key)]
    assert custom_name.mock_calls == [call.os.environ.__getitem__(key)]


@ykcom("tests.packages_for_testing.p1", "os", name="custom_name")
@ykcom("tests.packages_for_testing.p1", "sys", name="custom_name")
def test_multiple_targets_for_the_same_name(custom_name: MagicMock) -> None:
    p1.mock_me("none")

    assert custom_name.os.mock_calls == [call.environ.__getitem__("none")]
    assert custom_name.sys.mock_calls == [call.stdout.write("Some text\n")]
    assert custom_name.mock_calls == [
        call.sys.stdout.write("Some text\n"),
        call.os.environ.__getitem__("none"),
    ]


@ykcom("tests.packages_for_testing.p1", "os", "sys", name="custom_name")
@ykcom("tests.packages_for_testing.p1", "sys", name="custom_name")
def test_target_assigned_twice_for_the_same_name(custom_name: MagicMock) -> None:
    p1.mock_me("none")

    assert custom_name.os.mock_calls == [call.environ.__getitem__("none")]
    assert custom_name.sys.mock_calls == [call.stdout.write("Some text\n")]
    assert custom_name.mock_calls == [
        call.sys.stdout.write("Some text\n"),
        call.os.environ.__getitem__("none"),
    ]


def test_same_target_must_not_belong_to_different_names() -> None:
    with pytest.raises(TargetAlreadyBoundError) as err:

        @ykcom("tests.packages_for_testing.p1", "os", name="custom_name")
        @ykcom("tests.packages_for_testing.p1", "os", name="custom_name_2")
        def test_same_referred_via_multiple_names(custom_name: MagicMock, custom_name_2: MagicMock) -> None: ...

    assert str(err.value) == "Target 'tests.packages_for_testing.p1.os' is already bound"


@ykcom("tests.packages_for_testing.p1", "os", "sys")
@ykcom("tests.packages_for_testing.p1", "sys")
def test_target_assigned_twice_positional(pos: MagicMock) -> None:
    p1.mock_me("none")

    assert pos.os.mock_calls == [call.environ.__getitem__("none")]
    assert pos.sys.mock_calls == [call.stdout.write("Some text\n")]
    assert pos.mock_calls == [
        call.sys.stdout.write("Some text\n"),
        call.os.environ.__getitem__("none"),
    ]


@ykcom("tests.packages_for_testing.p1", "os", name="custom_name")
@ykcom("tests.packages_for_testing.p2", "sys", name="custom_name")  # different base path
def test_multiple_targets_from_different_packages_for_the_same_name(custom_name: MagicMock) -> None:
    p1.mock_me("none")
    p2.mockery()

    assert custom_name.os.mock_calls == [call.environ.__getitem__("none")]
    assert custom_name.sys.mock_calls == [
        call.stdout.write("Something else\n"),
        call.stdout.flush(),
    ]
    assert custom_name.mock_calls == [
        call.os.environ.__getitem__("none"),
        call.sys.stdout.write("Something else\n"),
        call.sys.stdout.flush(),
    ]


# TODO
# @ykcom("tests.packages_for_testing.p1", "os")
# @ykcom("tests.packages_for_testing.p1", "os", name="custom_name")  <- should be an error


# TODO
# @ykcom("tests.packages_for_testing.p1", "os", "sys", name="custom_name")
# @ykcom("tests.packages_for_testing.p2", "sys", name="custom_name")  <- should be error


# TODO
# @ykcom("tests.packages_for_testing.p1", "os", "sys", name="custom_name")
# @ykcom("tests.packages_for_testing.p2", {"target": "sys", "name": "sys2"}, name="custom_name")
