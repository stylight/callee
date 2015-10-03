"""
Matchers based on Python operators.
"""
import operator

from callee.base import BaseMatcher, Eq, Is


__all__ = [
    'Eq', 'Is',  # they are defined elsewhere but they fit in this module, too

    'Less', 'LessThan', 'Lt',
    'LessOrEqual', 'LessOrEqualTo', 'Le',
    'Greater', 'GreaterThan', 'Gt',
    'GreaterOrEqual', 'GreaterOrEqualTo', 'Ge',
]


class OperatorMatcher(BaseMatcher):
    """Matches based on comparison operator and a reference object.
    This class shouldn't be used directly.
    """
    #: Operator function to use for comparing a value with a reference object.
    #: Must be overridden in subclasses.
    OP = None

    #: Transformation function to apply to given value before comparison.
    TRANSFORM = None

    def __init__(self, *args, **kwargs):
        """Constructor.

        Accepts a single argument: the reference object to compare against.
        It can be passed either as a single positional parameter,
        or as a single keyword argument -- preferably with a readable name,
        for example::

            some_mock.assert_called_with(Number() & LessOrEqual(to=42))
        """
        assert self.OP, "must specify comparison operator to use"

        # check that we've received exactly one argument,
        # either positional or keyword
        argcount = len(args) + len(kwargs)
        if argcount != 1:
            raise TypeError("a single argument expected, got %s" % argcount)
        if len(args) > 1:
            raise TypeError(
                "at most one positional argument expected, got %s" % len(args))
        if len(kwargs) > 1:
            raise TypeError(
                "at most one keyword argument expected, got %s" % len(kwargs))

        # extract the reference object from arguments
        ref = None
        if args:
            ref = args[0]
        elif kwargs:
            _, ref = kwargs.popitem()

        #: Reference object to compare given values to.
        self.ref = ref

    def match(self, value):
        if self.TRANSFORM is not None:
            value = self.TRANSFORM(value)
        return self.OP(value, self.ref)


# Simple comparisons

class Less(OperatorMatcher):
    """Matches values that are smaller (as per ``<`` operator)
    than given object.
    """
    OP = operator.lt

#: Alias for :class:`Less`.
LessThan = Less

#: Alias for :class:`Less`.
Lt = Less


class LessOrEqual(OperatorMatcher):
    """Matches values that are smaller than (as per ``<`` operator),
    or equal to (as per ``==`` operator), given object.
    """
    OP = operator.le

#: Alias for :class:`LessOrEqual`.
LessOrEqualTo = LessOrEqual

#: Alias for :class:`LessOrEqual`.
Le = LessOrEqual


class Greater(OperatorMatcher):
    """Matches values that are greater (as per ``>`` operator)
    than given object.
    """
    OP = operator.gt

#: Alias for :class:`Greater`.
GreaterThan = Greater

#: Alias for :class:`Greater`.
Gt = Greater


class GreaterOrEqual(OperatorMatcher):
    """Matches values that are greater than (as per ``>`` operator),
    or equal to (as per ``==`` operator), given object.
    """
    OP = operator.ge

#: Alias for :class:`GreaterOrEqual`.
GreaterOrEqualTo = GreaterOrEqual

#: Alias for :class:`GreaterOrEqual`.
Ge = GreaterOrEqual
