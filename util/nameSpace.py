#===============================================================================
# Copyright (C) 2011 Diego Duclos
# Copyright (C) 2011-2012 Anton Vorobyov
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


class NameSpace(type):
    """
    We use classes as namespaces throughout eos,
    this class can be used as metaclass for such
    namespace classes, providing some additional
    functionality.
    """

    def __iter__(self):
        # Get all attribute values, which do not start with
        # at least one underscore, into cached _all attribute
        if getattr(self, "_all", None) is None:
            self._all = tuple(getattr(self, attr) for attr in filter(lambda attr: attr.startswith("_") is False, dir(self)))
        return (attr for attr in self._all)