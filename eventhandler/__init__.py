import sys
import types

__version__ = '1.0.1'


class EventHandler:
    """Event manager, bind, unbind and fire events."""

    class Exceptions:
        class EventNotAllowedError(Exception):
            pass

        class InitializationError(Exception):
            pass

    class Callbacks:
        """Empty class to hold callbacks callables."""
        pass

    events: dict = None
    allowed_callbacks = []

    def __init__(self, *args, verbose=False):
        """EventHandler initiazition recibe a list of allowed event names."""
        self.verbose = verbose
        if not args:
            raise EventHandler.Exceptions.InitializationError(
                'EventHandler must be initialized with a list of callbacks')

        self.set_allowed_callbacks(args) if args else None

    def set_allowed_callbacks(self, allowed_callbacks: [str]):
        """Set the allowed events names"""
        # remove previous
        for callback in self.allowed_callbacks:
            delattr(self.Callbacks, callback.upper())

        self.allowed_callbacks = allowed_callbacks

        for callback in self.allowed_callbacks:
            setattr(self.Callbacks, callback.upper(), [])

    def is_callable(self, func: callable) -> bool:
        """Return true if func is a callable variable."""
        return isinstance(func,
                          (types.FunctionType, types.BuiltinFunctionType, types.MethodType, types.BuiltinMethodType))

    def bind(self, event: str, callback: callable) -> bool:
        """Bind a callback to an event."""
        if not self.is_callable(callback):
            print(f'Callback not registered. Type {type(callback)} '
                  f'is not a callable function.', file=sys.stdout) if self.verbose else None
            return False

        if not event in self.allowed_callbacks:
            raise EventHandler.Exceptions.EventNotAllowedError(
                f'Event {event} is not allowed. Allowed events are: {self.allowed_callbacks}. '
                f'Please register event {event} on object initialization.')

        active_list = getattr(self.Callbacks, event.upper())
        if callback not in active_list:
            active_list.append(callback)
            setattr(self.Callbacks, event.upper(), active_list)
            return True

        print(f'Event {str(callback.__name__)} is already registered in '
              f'{event.upper()} event.', file=sys.stdout) if self.verbose else None
        return False

    def fire(self, event: str, *args, **kwargs):
        """Fire a callback to an event."""
        active_list = getattr(self.Callbacks, event.upper(), None)
        for callback in active_list:
            callable(callback(*args, **kwargs))

    def unbind(self, event: str, callback: callable) -> bool:
        """Unbind a callback from an event."""
        active_list = getattr(self.Callbacks, event.upper())
        if callback in active_list:
            active_list.remove(callback)
            return True
        return False
