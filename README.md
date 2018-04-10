# emitter.py

A neat event emitter for Python 3.

```sh
$ pip install emitter.py
```


## Quick Use

```python
from emitter import Emitter


emitter = Emitter()

emitter.on("event", print)

emitter.emit("event", "data1", "data2")
```


## API Overview

* `emitter.on(event, listener[, once]): bool`
* `emitter.once(event, listener): bool` 
* `emitter.emit(event[, *args][, **kwargs]): bool`
* `emitter.off([event][, listener]): bool`
* `emitter.events(): set`
* `emitter.listeners(event): list`


### `emitter.on(event, listener[, once])`

```python
emitter.on("click", listener1)
emitter.on("click", listener2, True)  # triggered only once
```


### `emitter.once(event, listener)`

```python
emitter.once("click", listener)

# equivalent
emitter.on("click", listener, True)
```


### `emitter.emit(event[, *args][, **kwargs])`

```python
# emit event with no data
emitter.emit("click")

# emit event with data
emitter.emit("click", 28, y=72)
```


### `emitter.off([event][, listener])`

```python
# remove all the events
emitter.off()

# remove all "click" listeners
emitter.off("click")

# remove a specific listener
emitter.off("click", listener1)
```


### `emitter.events()`


```python
emitter.events()
# => {event1, event2}
```


### `emitter.listeners(event)`


```python
emitter.listeners(event1)
# => [listener1, listener2]
```


## Special Events

### `Emitter.ERROR`

If a listener throws an error, the `Emitter.ERROR` event is emitted.
You can register error handlers for this event to be notified.
The first argument passed to the handler is the `sys.exc_info()` error.

```python
def error_handler(error, *args, **kwargs):
    ...

emitter.on(Emitter.ERROR, error_handler)
```


## Tests

[PyTest][pytest] is used for tests. Python 2 is not supported.

**Install PyTest**

```sh
$ pip install pytest
```

**Test**

```sh
$ py.test test/*

# or to be sure to use python3
$ py.test-3 test/*
```

[pytest]: http://pytest.org/
