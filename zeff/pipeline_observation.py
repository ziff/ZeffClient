"""Reporter is a protocol that allows tracking of records in the pipeline."""
__copyright__ = """Copyright (C) 2019 Ziff, Inc."""
__docformat__ = "reStructuredText en"
__all__ = [
    "pipeline_add_observer",
    "pipeline_remove_observer",
    "PipelinePhase",
    "PipelineLevel",
]

import enum
import datetime
import logging
from typing import Any, List


class PipelinePhase(enum.Enum):
    """Phase of record processing pipeline to observe."""

    Generate = logging.getLogger("zeffclient.record.generator")
    Build = logging.getLogger("zeffclient.record.builder")
    Validate = logging.getLogger("zeffclient.record.validator")
    Upload = logging.getLogger("zeffclient.record.uploader")


class PipelineLevel(enum.Enum):
    """Level of record processing events to observe."""

    Critical = logging.CRITICAL
    Error = logging.ERROR
    Warning = logging.WARNING
    Info = logging.INFO
    Debug = logging.DEBUG


def pipeline_add_observer(observer, phase: PipelinePhase, level: PipelineLevel):
    """Add an observer to watch pipeline events.

    This allows an event driven observation of the record generation,
    build, validate, and upload phases.

    :param observer: A observer object that will accept a single parameter
        of type PipelineEvent.

    :param phase: The PipelinePhase for events that should be delivered to
        the ``observer``.

    :param level: The minimum level for events that should be delivered to
        the ``observer``.
    """
    logger = phase.value
    handlers = [h for h in logger.handlers if isinstance(h, PipelineHandler)]
    if not handlers:
        handler = PipelineHandler(phase)
        logger.addHandler(handler)
        handlers = [handler]
    handlers[0].add_observer(observer, level)


def pipeline_remove_observer(observer, phase: PipelinePhase, level: PipelineLevel):
    """Remove an observer that is watching pipeline events.

    This will remove all instances of ``observer`` that is watching a
    given ``phase`` and minimum ``level``.

    :param observer: A observer object that will accept a single parameter
        of type PipelineEvent.

    :param phase: The PipelinePhase for events that should be delivered to
        the ``observer``.

    :param level: The minimum level for events that should be delivered to
        the ``observer``.
    """
    logger = phase.value
    handlers = [h for h in logger.handlers if isinstance(h, PipelineHandler)]
    if not handlers:
        return
    handlers[0].remove_observer(observer, level)


class PipelineEvent:
    """Represents an event in the ZeffClient pipeline.

    The pipeline will generate record configuration, build a record
    from the configuration, validate the record, and then upload the
    record to Zeff Cloud.
    """

    def __init__(self, phase: PipelinePhase, record: logging.LogRecord):
        self.__phase = phase
        self.__record = record

    def __str__(self):
        return f"{self.timestamp.isoformat()} [{self.phase.name}] {self.level.name}: {self.message}"

    @property
    def timestamp(self) -> datetime.datetime:
        """When the event was emitted."""
        return datetime.datetime.fromtimestamp(self.__record.created)

    @property
    def phase(self) -> PipelinePhase:
        """Pipeline phase that generated this event."""
        return self.__phase

    @property
    def level(self) -> PipelineLevel:
        """Pipeline level for this event."""
        for level in PipelineLevel:
            if level.value <= self.__record.levelno:
                return level
        return PipelineLevel.Debug

    @property
    def message(self) -> str:
        """Message that is part of the event."""
        return self.__record.getMessage()


class PipelineHandler(logging.Handler):
    """Logging handler for pipeline observation.

    When an observer is added to a phase then an object of this type
    will be added to the assocaited logger in order to receive
    log records from which events will be created.

    This allows the normall logging system to be used in an observable
    manner.
    """

    def __init__(self, phase: PipelinePhase):
        super().__init__(level=logging.DEBUG)
        self.phase = phase
        self.observers: List[Any] = []

    def add_observer(self, observer, level: PipelineLevel):
        """Add observer to this handler."""
        self.observers.append((observer, level))

    def remove_observer(self, observer, level: PipelineLevel):
        """Remove observer from this handler."""
        elems = [t for t in self.observers if t[0] == observer and t[1] == level]
        for elem in elems:
            self.observers.remove(elem)

    def emit(self, record):
        event = PipelineEvent(self.phase, record)
        for observer in (
            observer
            for observer, level in self.observers
            if level.value <= record.levelno
        ):
            observer(event)
