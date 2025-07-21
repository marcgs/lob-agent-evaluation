## Python Coding Guidelines

### Use `|` instead of `Union`

Use the newer syntax of `a | b` instead of `Union[a, b]`.

### Prefer union with `None` over `Optional`

Use the newer syntax of `a | None` instead of `Optional[a]`.

### Don't use deprecated aliases

For type hints, use newer aliases like `list`, `dict` and `tuple` instead of
deprecated ones like `List`, `Dict` and `Tuple`. The full list is below:

<!--
This comment contains the instructions for generating the list below.

Run, assuming `uv` is installed:

    curl https://docs.python.org/3/library/typing.html |
        uvx markitdown@0.1.1 > typing.md

Give the remaining text of this comment as the prompt to Copilot:

Read `typing.md` and write a very brief bullet list of deprecated aliases, e.g.:

- Use `list[T]` instead of `List[T]`
-->

- Use `list[T]` instead of `List[T]`
- Use `dict[KT, VT]` instead of `Dict[KT, VT]`
- Use `list[T]` instead of `List[T]`
- Use `set[T]` instead of `Set[T]`
- Use `frozenset[T]` instead of `FrozenSet[T]`
- Use `tuple[T, ...]` instead of `Tuple[T, ...]`
- Use `type[C]` instead of `Type[C]`
- Use `collections.defaultdict[KT, VT]` instead of `DefaultDict[KT, VT]`
- Use `collections.OrderedDict[KT, VT]` instead of `OrderedDict[KT, VT]`
- Use `collections.ChainMap[KT, VT]` instead of `ChainMap[KT, VT]`
- Use `collections.Counter[T]` instead of `Counter[T]`
- Use `collections.deque[T]` instead of `Deque[T]`
- Use `re.Pattern[AnyStr]` instead of `Pattern[AnyStr]`
- Use `re.Match[AnyStr]` instead of `Match[AnyStr]`
- Use `str` instead of `Text`
- Use `collections.abc.Set[T]` instead of `AbstractSet[T]`
- Use `collections.abc.Collection[T]` instead of `Collection[T]`
- Use `collections.abc.Container[T]` instead of `Container[T]`
- Use `collections.abc.ItemsView[KT, VT]` instead of `ItemsView[KT, VT]`
- Use `collections.abc.KeysView[KT]` instead of `KeysView[KT]`
- Use `collections.abc.Mapping[KT, VT]` instead of `Mapping[KT, VT]`
- Use `collections.abc.MappingView` instead of `MappingView`
- Use `collections.abc.MutableMapping[KT, VT]` instead of `MutableMapping[KT, VT]`
- Use `collections.abc.MutableSequence[T]` instead of `MutableSequence[T]`
- Use `collections.abc.MutableSet[T]` instead of `MutableSet[T]`
- Use `collections.abc.Sequence[T]` instead of `Sequence[T]`
- Use `collections.abc.ValuesView[VT]` instead of `ValuesView[VT]`
- Use `collections.abc.Coroutine[YieldType, SendType, ReturnType]` instead of `Coroutine[YieldType, SendType, ReturnType]`
- Use `collections.abc.AsyncGenerator[YieldType, SendType]` instead of `AsyncGenerator[YieldType, SendType]`
- Use `collections.abc.AsyncIterable[T]` instead of `AsyncIterable[T]`
- Use `collections.abc.AsyncIterator[T]` instead of `AsyncIterator[T]`
- Use `collections.abc.Awaitable[T]` instead of `Awaitable[T]`
- Use `collections.abc.Iterable[T]` instead of `Iterable[T]`
- Use `collections.abc.Iterator[T]` instead of `Iterator[T]`
- Use `collections.abc.Callable[Params, ReturnType]` instead of `Callable[Params, ReturnType]`
- Use `collections.abc.Generator[YieldType, SendType, ReturnType]` instead of `Generator[YieldType, SendType, ReturnType]`
- Use `collections.abc.Hashable` instead of `Hashable`
- Use `collections.abc.Reversible[T]` instead of `Reversible[T]`
- Use `collections.abc.Sized` instead of `Sized`
- Use `contextlib.AbstractContextManager[T_co, ExitT_co]` instead of `ContextManager[T_co, ExitT_co]`
- Use `contextlib.AbstractAsyncContextManager[T_co, AExitT_co]` instead of `AsyncContextManager[T_co, AExitT_co]`

### Prefer `object` over `Any`

Prefer to use `object` instead of `Any`, and `cast` or `assert` as necessary.

For example, suppose the following dictionary:

```python
data: dict[str, object] = {
    "foo": 1,
    "bar": [2, 3, 4],
    "baz": True,
}
```

When the actual type can be assumed, use `cast`:

```python
from typing import cast

foo = cast(int, data["foo"])
bar = cast(list[int], data["bar"])
baz = cast(bool, data["baz"])
```

When checking the type at run-time via `isinstance`, the type checker like
Pyright may issue a `reportUnknownArgumentType` error for generic types on
usage since the type arguments may still be unknown, e.g.:

```python
bar = data["bar"] # here "bar" is "object"
if isinstance(bar, list): # "bar" is now narrowed to "list", but...
    print(bar) # ...argument type is "list[Unknown]" (reportUnknownArgumentType)
```

Use `cast` if the type argument can be assumed, like so:

```python
if isinstance(bar, list): # "bar" is now narrowed to "list[Unknown]"
    bar = cast(list[int], bar) # "bar" is narrowed to "list[int]"
    for item in bar:
        print(item * 2)
```

An alternative would be to assume `object` for the type argument and then
`assert` before using the contained values, as in:

```python
if isinstance(bar, list):
    bar = cast(list[object], bar)
    for item in bar:
        assert isinstance(item, int)
        print(item * 2)
```

## React Coding Guidelines

- Create fully functional React components.
- Mark with `export default function Component() { ... }` to match the expected usage.
- Use Tailwind classes for additional styling.
- Use `import { Button } from '@/components/ui/button'` or other shadcn/ui imports as needed.
- Use `import { IconName } from 'lucide-react'` if you want to embed an icon.
- Include `"use client";` at the top of the file for any component that:
  - Uses React hooks (useState, useEffect, etc.)
  - Has interactivity (event handlers, form submissions)
  - Uses browser-only APIs
  - Imports other client components
  - Do not include it for purely static components that only render UI without interaction
  - Break into multiple files when explicitly prompted or when the task complexity requires separation for clarity.
  - Favor medium-density layouts and generous spacing to encourage a modern, clean aesthetic by default. Use responsive design patterns consistently.
- For images, you may use `/placeholder.svg?height=HEIGHT&width=WIDTH` as placeholders.
- Create folders for new components or pages depending on what the user is asking to prototype. We already have a components folder, so you can create a new folder inside it for the component. If the user is asking for a page, create a new folder inside the `app` directory.

Here's how you can import shadcn components:

```tsx
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
```
