import pytest
from emitter import Emitter


class Spy:
    def __init__(self):
        self.calls = 0
        self.args = None
        self.kwargs = None

    def called(self, n):
        return self.calls == n

    def throw(self, *args, **kwargs):
        self.__call__(*args, **kwargs)
        raise Exception()

    def __call__(self, *args, **kwargs):
        self.calls += 1
        self.args = args
        self.kwargs = kwargs


@pytest.fixture
def spy():
    # called before each test, creating a new Spy instance for the test
    return Spy()


def raise_error(*args, **kwargs):
    raise Exception()


def test_error__1(spy):
    """
    ERROR event is emitted when some listener raises exception.
    """
    emitter = Emitter()
    emitter.on("event", raise_error)
    emitter.on(Emitter.ERROR, spy)

    emitter.emit("event")

    assert spy.called(1)


def test_error__2(spy):
    """
    ERROR event handlers get error data (sys.exc_info), *args and **kwargs.
    """
    emitter = Emitter()

    emitter.on("event", raise_error)
    emitter.on(Emitter.ERROR, spy)

    emitter.emit("event", 10, b=20)

    assert spy.called(1)

    # first arg passed to the error handler is a tuple with 3 elements
    # see sys.exc_info()
    assert isinstance(spy.args[0][1], Exception)

    assert spy.args[1] == 10
    assert spy.kwargs["b"] == 20


def test_error__3(spy):
    """
    If error handler raises exception, it is re-raised, but not catched
    by the emitter this time (no ERROR event this time).
    """
    emitter = Emitter()

    emitter.on("event", spy.throw)
    emitter.on(Emitter.ERROR, spy.throw)

    with pytest.raises(Exception):
        emitter.emit("event")

    assert spy.called(2)


def test_error__4(spy):
    """
    One time listener is removed even if it raises exception.
    """
    emitter = Emitter()

    emitter.once("event", raise_error)

    assert len(emitter.listeners("event")) == 1

    emitter.emit("event")

    assert len(emitter.listeners("event")) == 0


def test_error__5(spy):
    """
    One time ERROR listener is removed even if it raises exception.
    """
    emitter = Emitter()

    emitter.once(Emitter.ERROR, spy.throw)
    emitter.on("event", raise_error)

    assert len(emitter.listeners(Emitter.ERROR)) == 1

    with pytest.raises(Exception):
        emitter.emit("event")

    assert len(emitter.listeners(Emitter.ERROR)) == 0


