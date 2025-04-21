# Ykcom

Your friendly mocker.

![Ykcom](ykcom.jpg)

## Why
TODO explain

## What
Ykcom provides a user-friendly way to interact with multiple mock
targets.

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
