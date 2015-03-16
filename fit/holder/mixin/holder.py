#===============================================================================
# Copyright (C) 2011 Diego Duclos
# Copyright (C) 2011-2015 Anton Vorobyov
#
# This file is part of Eos.
#
# Eos is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Eos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Eos. If not, see <http://www.gnu.org/licenses/>.
#===============================================================================


from eos.fit.attribute_calculator import MutableAttributeMap
from eos.fit.exception import NoSourceError
from eos.fit.null_source import NullSource


class HolderBase:
    """
    Base holder class inherited by all classes that
    need to keep track of modified attributes.

    Required arguments:
    type_id -- type ID of item which should serve as base
    for this holder.

    Cooperative methods:
    __init__
    """

    def __init__(self, type_id, **kwargs):
        # TypeID of item this holder is supposed to wrap
        self._type_id = type_id
        # Special dictionary subclass that holds modified attributes
        # and data related to their calculation
        self.attributes = MutableAttributeMap(self)
        # Which fit this holder is bound to
        self.__fit = None
        # Which type this holder wraps
        self.item = None
        super().__init__(**kwargs)

    @property
    def _fit(self):
        return self.__fit

    @_fit.setter
    def _fit(self, new_fit):
        self.__fit = new_fit
        self._refresh_source()

    def _refresh_source(self):
        """
        Each time holder's context is changed (the source it relies on,
        which may change when holder switches fit or its fit switches
        source), this method should be called; it will refresh data
        which is source-dependent.
        """
        self.attributes.clear()
        try:
            self.item = self._cache_handler.get_type(self._type_id)
        # When we're asked to refresh source, but we have no fit or
        # fit has no valid source assigned, we assign NullSource object
        # to an item as it's source-dependent
        except NoSourceError:
            self.item = NullSource

    @property
    def _cache_handler(self):
        """
        Return cache handler attached to the source of fit.
        If source cannot be found, return NullSource object.
        """
        try:
            return self._fit.source.cache_handler
        except AttributeError:
            return NullSource

    def _request_volatile_cleanup(self):
        """
        Request fit to clear all fit volatile data.
        """
        fit = self._fit
        if fit is not None:
            fit._request_volatile_cleanup()
