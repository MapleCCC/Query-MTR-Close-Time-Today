import functools
import typing
from typing import *
from typing import TypingMeta
import inspect

__all__ = ["type_check"]


def is_typing_object(arg) -> bool:
    # TODO: currently only a sanity check, more advanced checking is to add.
    return hasattr(typing, arg.__name__) and getattr(typing, arg.__name__) is arg


def type_check_value(value, annot_type) -> bool:
    """
    Some private API is used here. Be ware of potential broken changes.
    Type system in Python is currently still in heavy development progress.
    It's hard to do a lot of things.
    """
    if isinstance(annot_type, TypingMeta):
        # annot_type is type defined in typing module
        if isinstance(annot_type, GenericMeta):
            if annot_type is typing.List[int]:
                if not isinstance(value, list):
                    return False
                for element in value:
                    if not isinstance(element, int):
                        return False
                return True
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError
    else:
        # annot_type is primitive type
        return isinstance(value, annot_type)


def print_report(report: List[BaseException]) -> None:
    for err in report:
        if isinstance(err, TypeError):
            print(err)


def type_check(func):
    """
    Design philosophy:
    Performance
    Heuristic tricks
    """
    # functools.wraps ensures that wrapper also get original function's __annotations__
    # but some static type checking tools/linters/IDEs don't seem to be able to tackle with this complex case
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        report = []

        try:
            sig = inspect.signature(func)
        except ValueError:
            # no signature can be found
            # some builtin functions in CPython don't provide signature information
            # assign an empty Signature object for fallback
            sig = inspect.Signature()
        param = sig.parameters
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()
        # import pdb; pdb.set_trace()
        for name, value in bound_args.arguments.items():
            annot_type = param[name].annotation
            if annot_type is inspect.Parameter.empty:
                # not type hint info is found for specific argument
                annot_type = typing.Any
            if not type_check_value(value, annot_type):
                report.append(
                    TypeError(
                        f"Argument {name} has type {type(value)} but {annot_type} is expected"
                    )
                )

        # if not hasattr(func, "__annotations__"):
        #     raise NotImplementedError
        # annotations = func.__annotations__

        # # Deal with args list
        # assert len(annotations) >= len(args)
        # # based on the assumption that `__annotations__` is ordered
        # for arg, annot in zip(args, annotations.items()):
        #     name, type_ = annot
        #     if not type_check_value(arg, type_):
        #         raise TypeError(
        #             f"argument {name} has type {type(arg)} but {type_} is expected."
        #         )

        # # Deal with kwargs namespace
        # for name, value in kwargs.items():
        #     if name not in annotations:
        #         # No type hint information is found for the specific variable name
        #         continue
        #     annot_typ = annotations[name]
        #     if not type_check_value(value, annot_typ):
        #         report.append(
        #             TypeError(
        #                 f"Argument {name} has type {type(value)} but {annot_typ} is expected"
        #             )
        #         )

        # raise TypeError(
        #     "\n".join(err for err in report if isinstance(err, TypeError))
        # )

        # if name not in kwargs:
        #     # we only focus on type checking, leave other exceptions to original function
        #     continue

        ret = func(*args, **kwargs)
        if sig.return_annotation is sig.empty:
            # no type hint information is found.
            # assigned to typing.Any for fallback
            sig.return_annotation = typing.Any
        if not type_check_value(ret, sig.return_annotation):
            report.append(
                TypeError(
                    f"Expected return value is of type {sig.return_annotation} but {type(ret)} is given"
                )
            )

        print_report(report)

        return ret

    return wrapper


class Some:
    """
    """

def test():
    @type_check
    def f1(a: int, b: int = 1) -> int:
        return a + b

    print(f1(2, 3))
    print(f1(2, "str"))
    print(f1(2))


if __name__ == "__main__":
    test()
