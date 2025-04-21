from unittest.mock import MagicMock, call

import pytest

from src.ykcom import ykcom
from src.ykcom.errors import TargetAlreadyBoundError
from tests.packages_for_testing import p1


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


def test_same_target_must_not_belong_to_different_names() -> None:
    with pytest.raises(TargetAlreadyBoundError) as err:
        # TODO binding for the same name with the same target should be OK
        @ykcom("tests.packages_for_testing.p1", "os", name="custom_name")
        @ykcom("tests.packages_for_testing.p1", "os", name="custom_name_2")
        def test_same_refferred_via_multiple_names(custom_name: MagicMock, custom_name_2: MagicMock) -> None: ...

    assert str(err.value) == "Target 'tests.packages_for_testing.p1.os' is already bound"


# TODO stacked decorators
