#===============================================================================
# Copyright (C) 2011 Diego Duclos
# Copyright (C) 2011-2013 Anton Vorobyov
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


from eos.tests.cacheGenerator.generatorTestCase import GeneratorTestCase
from eos.tests.environment import Logger


class TestConversionModifier(GeneratorTestCase):
    """
    As modifiers generated by modifier builder have custom
    processing in converter, we have to test it too.
    """

    def testFields(self):
        self.dh.data['invtypes'].append({'typeID': 1, 'groupID': 1})
        self.dh.data['dgmtypeeffects'].append({'typeID': 1, 'effectID': 111})
        self.dh.data['dgmeffects'].append({'effectID': 111, 'preExpression': 1, 'postExpression': 11, 'effectCategory': 111})
        data = self.runGenerator()
        self.assertEqual(len(self.log), 1)
        cleanStats = self.log[0]
        self.assertEqual(cleanStats.name, 'eos_test.cacheGenerator')
        self.assertEqual(cleanStats.levelno, Logger.INFO)
        self.assertEqual(len(data['modifiers']), 1)
        self.assertIn(1, data['modifiers'])
        expected = {'modifierId': 1, 'state': 2, 'context': 3, 'sourceAttributeId': 4, 'operator': 5,
                    'targetAttributeId': 6, 'location': 7, 'filterType': 8, 'filterValue': 9}
        self.assertEqual(data['modifiers'][1], expected)
        self.assertIn(111, data['effects'])
        modifiers = data['effects'][111]['modifiers']
        self.assertEqual(modifiers, [1])

    def testNumberingSingleEffect(self):
        # Check how multiple modifiers generated out of single effect are numbered
        self.dh.data['invtypes'].append({'typeID': 1, 'groupID': 1})
        self.dh.data['dgmtypeeffects'].append({'typeID': 1, 'effectID': 111})
        self.dh.data['dgmeffects'].append({'effectID': 111, 'preExpression': 21, 'postExpression': 21, 'effectCategory': 21})
        data = self.runGenerator()
        self.assertEqual(len(self.log), 1)
        cleanStats = self.log[0]
        self.assertEqual(cleanStats.name, 'eos_test.cacheGenerator')
        self.assertEqual(cleanStats.levelno, Logger.INFO)
        self.assertEqual(len(data['modifiers']), 2)
        self.assertIn(1, data['modifiers'])
        expected = {'modifierId': 1, 'state': 20, 'context': 30, 'sourceAttributeId': 40, 'operator': 50,
                    'targetAttributeId': 60, 'location': 70, 'filterType': 80, 'filterValue': 90}
        self.assertEqual(data['modifiers'][1], expected)
        self.assertIn(2, data['modifiers'])
        expected = {'modifierId': 2, 'state': 200, 'context': 300, 'sourceAttributeId': 400, 'operator': 500,
                    'targetAttributeId': 600, 'location': 700, 'filterType': 800, 'filterValue': 900}
        self.assertEqual(data['modifiers'][2], expected)
        self.assertIn(111, data['effects'])
        modifiers = data['effects'][111]['modifiers']
        self.assertEqual(sorted(modifiers), [1, 2])

    def testNumberingMultipleEffects(self):
        # Check how multiple modifiers generated out of two effects are numbered
        self.dh.data['invtypes'].append({'typeID': 1, 'groupID': 1})
        self.dh.data['dgmtypeeffects'].append({'typeID': 1, 'effectID': 111})
        self.dh.data['dgmtypeeffects'].append({'typeID': 1, 'effectID': 222})
        self.dh.data['dgmeffects'].append({'effectID': 111, 'preExpression': 1, 'postExpression': 11, 'effectCategory': 111})
        self.dh.data['dgmeffects'].append({'effectID': 222, 'preExpression': 111, 'postExpression': 1, 'effectCategory': 111})
        data = self.runGenerator()
        self.assertEqual(len(self.log), 1)
        cleanStats = self.log[0]
        self.assertEqual(cleanStats.name, 'eos_test.cacheGenerator')
        self.assertEqual(cleanStats.levelno, Logger.INFO)
        self.assertEqual(len(data['modifiers']), 2)
        self.assertIn(1, data['modifiers'])
        expected = {'modifierId': 1, 'state': 2, 'context': 3, 'sourceAttributeId': 4, 'operator': 5,
                    'targetAttributeId': 6, 'location': 7, 'filterType': 8, 'filterValue': 9}
        self.assertEqual(data['modifiers'][1], expected)
        self.assertIn(2, data['modifiers'])
        expected = {'modifierId': 2, 'state': 22, 'context': 33, 'sourceAttributeId': 44, 'operator': 55,
                    'targetAttributeId': 66, 'location': 77, 'filterType': 88, 'filterValue': 99}
        self.assertEqual(data['modifiers'][2], expected)
        self.assertIn(111, data['effects'])
        modifiers = data['effects'][111]['modifiers']
        self.assertEqual(modifiers, [1])
        self.assertIn(222, data['effects'])
        modifiers = data['effects'][222]['modifiers']
        self.assertEqual(modifiers, [2])

    def testMergeMultipleEffects(self):
        # Check that if modifiers with the same values are generated on multiple effects,
        # they're assigned to single identifier
        self.dh.data['invtypes'].append({'typeID': 1, 'groupID': 1})
        self.dh.data['dgmtypeeffects'].append({'typeID': 1, 'effectID': 111})
        self.dh.data['dgmtypeeffects'].append({'typeID': 1, 'effectID': 222})
        self.dh.data['dgmeffects'].append({'effectID': 111, 'preExpression': 1, 'postExpression': 11, 'effectCategory': 111})
        self.dh.data['dgmeffects'].append({'effectID': 222, 'preExpression': 111, 'postExpression': 11, 'effectCategory': 1})
        data = self.runGenerator()
        self.assertEqual(len(self.log), 1)
        cleanStats = self.log[0]
        self.assertEqual(cleanStats.name, 'eos_test.cacheGenerator')
        self.assertEqual(cleanStats.levelno, Logger.INFO)
        self.assertEqual(len(data['modifiers']), 1)
        self.assertIn(1, data['modifiers'])
        expected = {'modifierId': 1, 'state': 2, 'context': 3, 'sourceAttributeId': 4, 'operator': 5,
                    'targetAttributeId': 6, 'location': 7, 'filterType': 8, 'filterValue': 9}
        self.assertEqual(data['modifiers'][1], expected)
        self.assertIn(111, data['effects'])
        modifiers = data['effects'][111]['modifiers']
        self.assertEqual(modifiers, [1])
        self.assertIn(111, data['effects'])
        modifiers = data['effects'][111]['modifiers']
        self.assertEqual(modifiers, [1])
        self.assertIn(222, data['effects'])
        modifiers = data['effects'][222]['modifiers']
        self.assertEqual(modifiers, [1])

    def testMergeSignleEffect(self):
        # Check that if modifiers with the same values are generated on single effect,
        # they're assigned to single identifier and it is listed twice in list of
        # modifiers
        self.dh.data['invtypes'].append({'typeID': 1, 'groupID': 1})
        self.dh.data['dgmtypeeffects'].append({'typeID': 1, 'effectID': 111})
        self.dh.data['dgmeffects'].append({'effectID': 111, 'preExpression': 22, 'postExpression': 22, 'effectCategory': 22})
        data = self.runGenerator()
        self.assertEqual(len(self.log), 1)
        cleanStats = self.log[0]
        self.assertEqual(cleanStats.name, 'eos_test.cacheGenerator')
        self.assertEqual(cleanStats.levelno, Logger.INFO)
        self.assertEqual(len(data['modifiers']), 1)
        self.assertIn(1, data['modifiers'])
        expected = {'modifierId': 1, 'state': 32, 'context': 43, 'sourceAttributeId': 54, 'operator': 65,
                    'targetAttributeId': 76, 'location': 87, 'filterType': 98, 'filterValue': 90}
        self.assertEqual(data['modifiers'][1], expected)
        self.assertIn(111, data['effects'])
        modifiers = data['effects'][111]['modifiers']
        self.assertEqual(modifiers, [1, 1])

    def testLogger(self):
        # Check that proper logger is passed to modifier builder
        self.dh.data['invtypes'].append({'typeID': 1, 'groupID': 1})
        self.dh.data['dgmtypeeffects'].append({'typeID': 1, 'effectID': 111})
        self.dh.data['dgmeffects'].append({'effectID': 111, 'preExpression': 108, 'postExpression': 108, 'effectCategory': 108})
        self.runGenerator()
        self.assertEqual(len(self.log), 2)
        cleanStats = self.log[0]
        self.assertEqual(cleanStats.name, 'eos_test.cacheGenerator')
        self.assertEqual(cleanStats.levelno, Logger.INFO)
        builderWarning = self.log[1]
        self.assertEqual(builderWarning.name, 'eos_test.modifierBuilder')
        self.assertEqual(builderWarning.levelno, Logger.WARNING)
        self.assertEqual(builderWarning.msg, 'modbuilder warning')