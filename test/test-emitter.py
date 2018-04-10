import pytest
from emitter import Emitter


# Emitter()


# emitter.on()


def test_on__1():
    """
    User cannot register a None event.
    """
    emitter = Emitter()

    with pytest.raises(ValueError):
        emitter.on(None, callable)


def test_on__2():
    """
    True is a valid event.
    """
    emitter = Emitter()
    emitter.on(True, callable)

    assert True in emitter.events()


def test_on__3():
    """
    False is a valid event.
    """
    emitter = Emitter()
    emitter.on(False, callable)

    assert False in emitter.events()


def test_on__4():
    """
    A string is a valid event.
    """
    emitter = Emitter()
    emitter.on("event", callable)

    assert "event" in emitter.events()


def test_on__5():
    """
    A listener must be callable.
    """
    emitter = Emitter()

    with pytest.raises(TypeError):
        emitter.on("event", "")


def test_on__6():
    """
    Multiple events can be registered.
    """
    emitter = Emitter()

    emitter.on("event1", callable)
    emitter.on("event2", callable)

    assert "event1" in emitter.events()
    assert "event2" in emitter.events()


def test_on__7():
    """
    Multiple listeners can be registered for an event.
    """
    emitter = Emitter()

    emitter.on("event", callable)
    emitter.on("event", bool)

    assert callable in emitter.listeners("event")
    assert bool in emitter.listeners("event")


def test_on__8():
    """
    Listeners are not shared between events.
    """
    emitter = Emitter()

    emitter.on("event1", str)
    emitter.on("event2", callable)

    assert str in emitter.listeners("event1")
    assert str not in emitter.listeners("event2")

    assert callable in emitter.listeners("event2")
    assert callable not in emitter.listeners("event1")


def test_on__9():
    """
    Returns True when event has been successfully registered.
    """
    emitter = Emitter()
    assert emitter.on("event", callable) is True
    assert callable in emitter.listeners("event")


def test_on__10():
    """
    Allow updating an event from on() to once().
    """
    emitter = Emitter()
    emitter.once("event", callable)
    emitter.on("event", callable)

    emitter.emit("event")
    emitter.emit("event")
    emitter.emit("event")

    assert callable in emitter.listeners("event")


def test_on__11():
    """
    One-shot listeners can be called only once.
    """
    emitter = Emitter()
    l = []
    emitter.on("event", lambda: l.append(1), True)
    emitter.emit("event")
    emitter.emit("event")
    emitter.emit("event")

    assert len(l) == 1


# emitter.once()


def test_once__1():
    """
    Listener can be called only once.
    """
    emitter = Emitter()
    l = []
    emitter.once("event", lambda: l.append(1))
    emitter.emit("event")
    emitter.emit("event")
    emitter.emit("event")

    assert len(l) == 1


def test_once__2():
    """
    Listener should be removed after call.
    """
    emitter = Emitter()
    emitter.once("event", callable)
    emitter.on("event", bool)
    emitter.emit("event")

    assert callable not in emitter.listeners("event")
    assert bool in emitter.listeners("event")


def test_once__3():
    """
    Event should be cleaned if no more listeners.
    """
    emitter = Emitter()
    emitter.once("event", callable)
    emitter.emit("event")

    assert emitter.events() == set()


def test_once__4():
    """
    Allow updating an event from once() to on().
    """
    emitter = Emitter()
    emitter.on("event", callable)
    emitter.once("event", callable)

    emitter.emit("event")

    assert callable not in emitter.listeners("event")


def test_once__5():
    """
    One time listeners should be removed even if an error happens.
    """
    emitter = Emitter()

    def listener(*args, **kwargs):
        raise Exception()

    emitter.once("event", listener)

    emitter.emit("event")

    assert listener not in emitter.listeners("event")


# emitter.emit()


def test_emit__1():
    """
    All the listeners of an event must be triggered.
    """
    emitter = Emitter()
    l = []
    emitter.on("event", lambda: l.append(1))
    emitter.on("event", lambda: l.append(1))
    emitter.on("event", lambda: l.append(1))
    emitter.emit("event")
    assert len(l) == 3


def test_emit__2():
    """
    Listeners are triggered in order of insertion.
    """
    emitter = Emitter()
    l = []
    emitter.on("event", lambda: l.append(1))
    emitter.on("event", lambda: l.append(2))
    emitter.on("event", lambda: l.append(3))
    emitter.emit("event")
    assert l == [1, 2, 3]


def test_emit__3():
    """
    Only the listeners of the specified event should be triggered.
    """
    emitter = Emitter()
    l = []
    emitter.on("event1", lambda: l.append(1))
    emitter.on("event2", lambda: l.append(2))
    emitter.emit("event1")
    assert l == [1]


def test_emit__4():
    """
    Returns False when emitting a non-existent event.
    """
    emitter = Emitter()
    result = emitter.emit("event")
    assert result is False


def test_emit__5():
    """
    Returns True when emitting an event.
    """
    emitter = Emitter()
    emitter.on("event", callable)
    result = emitter.emit("event")
    assert result is True


def test_emit__6():
    """
    Should pass *args and **kwargs to the listeners.
    """
    emitter = Emitter()
    params = []

    def listener(param1, param2, unused=None, param3=None):
        params.append(param1)
        params.append(param2)
        params.append(unused)
        params.append(param3)

    emitter.on("event", listener)
    emitter.emit("event", 10, 20, param3="hello")
    assert params == [10, 20, None, "hello"]


def test_emit__7():
    """
    False event can be emitted.
    """
    emitter = Emitter()
    l = []
    emitter.on(False, lambda: l.append(1))
    emitter.emit(False)
    assert 1 in l


def test_emit__8():
    """
    True event can be emitted.
    """
    emitter = Emitter()
    l = []
    emitter.on(True, lambda: l.append(1))
    emitter.emit(True)
    assert 1 in l


def test_emit__9():
    """
    Emitting None event returns False.
    """
    emitter = Emitter()

    assert emitter.emit(None) is False


# emitter.events()


def test_events__1():
    """
    Returns a empty set if no events registered.
    """
    emitter = Emitter()
    assert emitter.events() == set()


def test_events__2():
    """
    Returns a set containing all the registered events.
    """
    emitter = Emitter()
    emitter.on("event1", callable)
    emitter.on("event2", callable)
    emitter.on("event3", callable)
    events = emitter.events()
    assert events == {"event1", "event2", "event3"}


def test_events__3():
    """
    False event can be retrieved.
    """
    emitter = Emitter()
    emitter.on(False, callable)
    assert False in emitter.events()


def test_events__4():
    """
    True event can be retrieved.
    """
    emitter = Emitter()
    emitter.on(True, callable)
    assert True in emitter.events()


def test_events__5():
    """
    Should not return the original object, but a copy.
    """
    emitter = Emitter()
    emitter.on("event", callable)
    assert emitter.events() is not emitter.events()


# emitter.listeners()


def test_listeners__1():
    """
    Returns an empty list when asking for an unknown event.
    """
    emitter = Emitter()

    assert isinstance(emitter.listeners(""), list)
    assert emitter.listeners("") == []


def test_listeners__2():
    """
    Returns a list containing all the listeners of the given event.
    """
    emitter = Emitter()
    emitter.on("event", callable)
    emitter.on("event", list)

    listeners = emitter.listeners("event")

    assert isinstance(listeners, list)
    assert listeners == [callable, list]


def test_listeners__3():
    """
    The insertion order of the listeners should be conserved.
    """
    emitter = Emitter()
    emitter.on("raccoon", bool)
    emitter.on("raccoon", callable)
    emitter.on("raccoon", dict)

    listeners = emitter.listeners("raccoon")

    assert listeners == [bool, callable, dict]


def test_listeners__4():
    """
    Get the listeners for the False event.
    """
    emitter = Emitter()
    emitter.on(False, callable)
    assert callable in emitter.listeners(False)


def test_listeners__5():
    """
    Get the listeners for the True event.
    """
    emitter = Emitter()
    emitter.on(True, callable)
    assert callable in emitter.listeners(True)


def test_listeners__6():
    """
    Should not return the original object, but a copy.
    """
    emitter = Emitter()
    emitter.on("event", callable)
    assert emitter.listeners("event") is not emitter.listeners("event")


# emitter.off()


def test_off__1():
    """
    Called with no arguments, it removes all the events.
    """
    emitter = Emitter()
    emitter.on("raccoon", callable)
    emitter.on("fox", callable)
    emitter.off()
    assert emitter.events() == set()


def test_off__2():
    """
    When called with 1 argument, it removes only the listeners of the
    specified event.
    """
    emitter = Emitter()
    emitter.on("event", callable)
    emitter.on("event", str)
    emitter.on("raccoon", callable)
    emitter.on("raccoon", str)
    emitter.off("event")

    assert emitter.listeners("event") == []
    assert callable in emitter.listeners("raccoon")
    assert str in emitter.listeners("raccoon")


def test_off__3():
    """
    Called with 2 arguments, it removes the specified listener of the specified
    event.
    """
    emitter = Emitter()
    emitter.on("event", callable)
    emitter.on("event", str)
    emitter.off("event", callable)
    listeners = emitter.listeners("event")
    assert callable not in listeners
    assert str in listeners


def test_off__4():
    """
    False event can be removed.
    """
    emitter = Emitter()
    emitter.on(False, callable)
    assert False in emitter.events()

    emitter.off(False)
    assert False not in emitter.events()


def test_off__5():
    """
    True event can be removed.
    """
    emitter = Emitter()
    emitter.on(True, callable)
    assert True in emitter.events()

    emitter.off(True)
    assert True not in emitter.events()


def test_off__6():
    """
    A listener of the False event can be removed.
    """
    emitter = Emitter()
    emitter.on(False, callable)
    assert callable in emitter.listeners(False)

    emitter.off(False, callable)
    assert callable not in emitter.listeners(False)


def test_off__7():
    """
    A listener of the True event can be removed.
    """
    emitter = Emitter()
    emitter.on(True, callable)
    assert callable in emitter.listeners(True)

    emitter.off(True, callable)
    assert callable not in emitter.listeners(True)


def test_off__8():
    """
    Returns True if all events are deleted.
    """
    emitter = Emitter()
    emitter.on("event1", callable)
    emitter.on("event2", callable)
    assert emitter.off() is True


def test_off__9():
    """
    Returns True if trying to remove a non-existent event.
    """
    emitter = Emitter()
    assert emitter.off("unknown") is True


def test_off__10():
    """
    Returns True if the specified event has been deleted.
    """
    emitter = Emitter()
    emitter.on("event", callable)
    assert emitter.off("event") is True


def test_off__11():
    """
    Returns True if trying to detach a non-existent listener.
    """
    emitter = Emitter()
    emitter.on("event", callable)
    assert emitter.off("event", bool) is True


def test_off__12():
    """
    Returns True if the specified listener has been detached.
    """
    emitter = Emitter()
    emitter.on("event", callable)
    assert emitter.off("event", callable) is True


def test_off__13():
    """
    Delete the event if no more listeners.
    """
    emitter = Emitter()
    emitter.on("event", callable)
    assert "event" in emitter.events()

    emitter.off("event", callable)
    assert emitter.events() == set()

