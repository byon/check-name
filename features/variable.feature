Feature: Analysing variable names

Scenario Outline: Succeeding analysis
    Given source with <type> variable "<name>"
    When analysis is made
    Then analysis should report no rule violations

  Examples: Names that follow the rules
  | type          | name              |
  |               | variable          |
  |               | headlessCamelCase |
  | reference     | rVariable         |
  |               | roundAbout        |
  |               | peterPiper        |
  |               | arrhythmia        |
  | pointer       | pVariable         |
  | array         | aVariable         |
  | pointer array | apVariable        |
  | smart pointer | pVariable         |
  | constant      | CONSTANT_VARIABLE |

# Note: Also boost smart arrays are recognized. They are not tested
# here, because that would bring dependency for boost. Also typedefs
# to smart pointers/arrays are recognized, but not tested on feature
# level. For both of these, it is deemed sufficient to test on unit
# level and avoid dependencies and/or complicating the feature tests
# further.

  Scenario Outline: Failing analysis
    Given source with <type> variable "<name>"
    When analysis is made
    Then analysis reports "<type> variable" "<name>" as "<rule>" rule violation

  Examples: Names that break the rules
  | name | type          | rule                 |
  | Foo  |               | headlessCamelCase    |
  | foo  | reference     | prefix "r"           |
  | rFoo |               | redundant prefix "r" |
  | foo  | pointer       | prefix "p"           |
  | pFoo |               | redundant prefix "p" |
  | foo  | array         | prefix "a"           |
  | aFoo |               | redundant prefix "a" |
  | aFoo | pointer array | prefix "p"           |
  | pFoo | pointer array | prefix "a"           |
  | foo  | smart pointer | prefix "p"           |
  | foo  | constant      | SCREAMING_SNAKE_CASE |

  Scenario Outline: Succeeding member variable analysis
    Given source with class "Class"
    And nested <type> variable "<name>"
    When analysis is made
    Then analysis should report no rule violations

  Examples: Names that follow the rules
  | type      | name       |
  |           | variableM  |
  | reference | rVariableM |
  | pointer   | pVariableM |
  | array     | aVariableM |

  Scenario Outline: Failing member variable analysis
    Given source with class "Class"
    And nested <type> variable "<name>"
    When analysis is made
    Then analysis reports "variable" "<name>" as "<rule>" rule violation

  Examples: Names that break the rules
  | name       | type      | rule                 |
  | AbcM       |           | headlessCamelCase    |
  | abc        |           | postfix "M"          |
  | variableM  | reference | prefix "r"           |
  | rvariable  | reference | postfix "M"          |
  | rvariableM | reference | prefix "r"           |
  | variableM  | pointer   | prefix "p"           |
  | pVariableM |           | redundant prefix "p" |
  | variableM  | array     | prefix "a"           |
  | aVariableM |           | redundant prefix "a" |

  Scenario Outline: Succeeding parameter analysis
    Given source with class "Class"
    And nested method "method"
    And nested <type> parameter "<name>"
    When analysis is made
    Then analysis should report no rule violations

  Examples: Names that follow the rules
  | type      | name       |
  |           | variableP  |
  | reference | rVariableP |
  | pointer   | pVariableP |

  Scenario Outline: Failing parameter analysis
    Given source with class "Class"
    And nested method "method"
    And nested <type> parameter "<name>"
    When analysis is made
    Then analysis reports "parameter" "<name>" as "<rule>" rule violation

  Examples: Names that break the rules
  | name       | type      | rule                 |
  | VariableP  |           | headlessCamelCase    |
  | variable   |           | postfix "P"          |
  | variableP  | reference | prefix "r"           |
  | variableP  | pointer   | prefix "p"           |
  | pVariableP |           | redundant prefix "p" |
  | pVariable  | pointer   | postfix "P"          |
