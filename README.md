# Ykcom

Your friendly mocker.

![Ykcom](ykcom.jpg)

## Why
TODO explain

## What
Ykcom provides a user-friendly way to interact with multiple mock
targets.

TODO explain the returned magic mock setup

### Context manager
Ykcom can be used as a context manager:
```python
with ykcom("base_path", "os") as mocked:
    # Do some calls

    assert mocked.os.mock_calls == []
    assert mocked.mock_calls == []
```

### Positional decorator
Ykcom can be used as a decorator:
```python
@ykcom("base_path", "os")
def test_bad(mocked: MagicMock) -> None:
    # Do some calls

    assert mocked.os.mock_calls == []
    assert mocked.mock_calls == []
```

**Important:** if Ykcom is used as a decorator without a given name
then the first parameter will be replaced with the `MagicMock` instance.

Multiple nameless Ykcom decorators are merged into the same `MagicMock`
instance. The caller must expect only one `MagicMock` instance.

```python
@ykcom("base_path", "os")
@ykcom("base_path", "sys")
def test_bad(mocked: MagicMock) -> None:
    # Do some calls

    # Both `os` and `sys` are accessible via the same MagicMock instance.s
    assert mocked.os.mock_calls == []
    assert mocked.sys.mock_calls == []
    assert mocked.mock_calls == []
```

The first parameter is the base path for mocking (like `"package"` or `"package.sub_package"`).

The next parameter is either a name to mock on the base path or a list/tuple of names.

```python
# The following calls result in the same MagicMock setup
@ykcom("base_path", ["os", "sys"])
def test_as_list(mocked: MagicMock) -> None:
    ...


@ykcom("base_path", ("os", "sys"))
def test_as_tuple(mocked: MagicMock) -> None:
    ...


@ykcom("base_path", "os", "sys")
def test_as_args(mocked: MagicMock) -> None:
    ...
```

### Named decorator
A Ykcom decorator also can be given a name - the parameter with the
given name will be replaced with the `MagicMock` instance.

```python
@ykcom("base_path", "os", name="custom_name")
def test_bad(custom_name: MagicMock) -> None:
    # Do some calls

    assert custom_name.os.mock_calls == []
    assert custom_name.mock_calls == []
```

TODO Add use cases and examples

The following use cases are not supported:
* Registering the same target under multiple Ykcom name. The same `MagicMock`
  instance cannot have multiple parents. The behavior here would be that only
  one of the `MagicMock` instanced would receive the mock calls - which might
  be unexpected.
  ```python
  @ykcom("base_path", "os", name="name_1")
  @ykcom("base_path", "os", name="name_2")
  def test_bad(name_1: MagicMock, name_2: MagicMock) -> None: ...
  ```
  This will raise a `TargetAlreadyBoundError` exception.

## TODOs/Ideas

* [ ] Decorator support on functions
* [ ] Decorator support on classes
* [ ] pypi upload
