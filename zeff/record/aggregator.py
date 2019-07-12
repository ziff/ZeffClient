"""Zeff aggregator."""
__docformat__ = "reStructuredText en"

import re


def aggregation(cls_container, container_prop_name=None, contained_prop_name=None):
    """Add an aggregation relationship to a data type.

    The purpose of this is to allow the target of the aggregation to
    handle adding and removing of itself from a Record without the
    requirement of duplicate code in multiple targets.

    :param cls_container: The class of the object that will contain the
        aggregated objects.

    :param container_prop_name: The name of the property in the contained
        object to the container. This property is used to get, set, and
        delete the container of the contained object. If this is ``None``
        then the name of the property will be the name of the class of
        the container converted to snake case.

    :param contained_prop_name: The name of the property in the
        ``cls_container`` object that may be used to get an iterator
        of all the contained objects. If this is ``None`` then the
        name of the class of contained objects will be converted to
        snake case.
    """

    def container_property(cls_contained, attr_name):
        """Get an iterator for all {0.__name__} elements."""

        def getter(self):
            prop = getattr(self, attr_name, set())
            return iter(prop)

        doc = container_property.__doc__.format(cls_contained)
        return property(fget=getter, doc=str(doc))

    def contained_property(
        cls_container, container_prop_name, container_attr_name, contained_attr_name
    ):
        """TBW."""

        def getter(self):
            """Get, set, or delete this object in {0.__name__}.

            :exception ValueError: This will be raised when an attempt
                to set the container to ``None`` or the container is
                already set. In either case use ``del x.{1}()``.
            """
            return getattr(self, container_attr_name)

        getter.__doc__ = getter.__doc__.format(cls_container, container_prop_name)

        def setter(self, value: cls_container):
            if value is None:
                raise ValueError(
                    f"Reference to {cls_container.__name__} cannot be None"
                )
            if (
                getattr(self, container_attr_name) is not None
                and getattr(self, container_attr_name) != value
            ):
                raise ValueError(f"Item is associated with a {cls_container.__name__}")
            if not isinstance(value, cls_container):
                raise TypeError(f"Container must be of type {cls_container.__name__}")
            setattr(self, container_attr_name, value)
            if not hasattr(value, contained_attr_name):
                setattr(value, contained_attr_name, set())
            getattr(value, contained_attr_name).add(self)

        def deleter(self):
            getattr(getattr(self, container_attr_name), contained_attr_name).remove(
                self
            )
            setattr(self, container_attr_name, None)

        return property(fget=getter, fset=setter, fdel=deleter, doc=getter.__doc__)

    def decorator(
        cls_contained,
        cls_container=cls_container,
        container_prop_name=container_prop_name,
        contained_prop_name=contained_prop_name,
    ):
        def snake_case(cls):
            name = cls.__name__
            name = re.sub(r"([A-Z])", r"_\1", name).lstrip("_")
            name = name.lower()
            return name

        def contained_setattr(cls, prop_name, attr_name):
            def wrap_setattr(cls, prop_name, attr_name):
                orig_setattr = getattr(cls, "__setattr__")

                def aggregator_setattr(self, name, value):
                    if name in (prop_name, attr_name):
                        object.__setattr__(self, name, value)
                    else:
                        orig_setattr(self, name, value)

                return aggregator_setattr

            if hasattr(cls, "__setattr__"):
                setattr(cls, "__setattr__", wrap_setattr(cls, prop_name, attr_name))

        if not contained_prop_name:
            contained_prop_name = snake_case(cls_contained)
        contained_attr_name = f"_{cls_container.__name__}__{contained_prop_name}"

        if not container_prop_name:
            container_prop_name = snake_case(cls_container)
        container_attr_name = f"__{container_prop_name}"

        setattr(
            cls_container,
            contained_prop_name,
            container_property(cls_contained, contained_attr_name),
        )

        contained_setattr(cls_contained, container_prop_name, container_attr_name)
        setattr(cls_contained, container_attr_name, None)
        setattr(
            cls_contained,
            container_prop_name,
            contained_property(
                cls_container,
                container_prop_name,
                container_attr_name,
                contained_attr_name,
            ),
        )
        return cls_contained

    return decorator
