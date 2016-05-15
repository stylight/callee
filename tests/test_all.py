"""
Tests that touch more than a single module.
"""
import inspect

import callee
from tests import TestCase


class Init(TestCase):
    """Tests for the __init__ module."""

    def test_exports__only_available(self):
        """Test that __all__ has only names that are available
        (i.e. have been imported from submodules into the __init__ module).
        """
        missing = set(n for n in callee.__all__
                      if getattr(callee, n, None) is None)
        self.assertEmpty(
            missing, msg="callee.__all__ contains unresolved names: %s" % (
                ", ".join(missing),))

    def test_exports__only_exported_by_submodules(self):
        """Test that __all__ contains only names that are actually exported
        by the submodules.
        """
        exported_by_submodules = set()
        for mod in self.get_submodules():
            exported_by_submodules.update(mod.__all__)
        exported_by_root = set(callee.__all__)

        private_exports = exported_by_root - exported_by_submodules
        self.assertEmpty(
            private_exports,
            msg="callee.__all__ contains private symbols: %s" % (
                ", ".join(private_exports),))

    def test_exports__all_of_submodule_exports(self):
        """Test that __all__ contains all the publically exported names
        from the (public) submodules.
        """
        exported_by_submodules = set()
        for mod in self.get_submodules():
            exported_by_submodules.update(mod.__all__)
        exported_by_root = set(callee.__all__)

        missing_exports = exported_by_submodules - exported_by_root
        self.assertEmpty(
            missing_exports,
            msg="missing public symbols from callee.__all__: %s" % (
                ", ".join(missing_exports),))

    # Utility functions

    def get_submodules(self):
        """Get an iterable of submodules in the library, w/o private ones."""
        for name, obj in vars(callee).items():
            if not name.startswith('_') and inspect.ismodule(obj):
                yield obj
