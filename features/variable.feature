Feature: Analysing variable names

Scenario Outline: Succeeding analysis
    Given source with <type> variable "<name>"
    When analysis is made
    Then analysis should report no rule violations

  Examples: Names that follow the rules
  | type      | name              |
  |           | variable          |
  |           | aVariable         |
  |           | headlessCamelCase |
  | reference | rVariable         |

  @wip
  Scenario Outline: Failing analysis
    Given source with <type> variable "<name>"
    When analysis is made
    Then analysis reports "<type> variable" "<name>" as "<rule>" rule violation

  Examples: Names that break the rules
  | name | type      | rule                 |
  | Foo  |           | headlessCamelCase    |
  | foo  | reference | prefix "r"           |
  | rFoo |           | redundant prefix "r" |

  Scenario Outline: Succeeding member variable analysis
    Given source with class "Class"
    And nested <type> variable "<name>"
    When analysis is made
    Then analysis should report no rule violations

  Examples: Names that follow the rules
  | type      | name       |
  |           | variableM  |
  | reference | rVariableM |

  Scenario Outline: Failing member variable analysis
    Given source with class "Class"
    And nested <type> variable "<name>"
    When analysis is made
    Then analysis reports "variable" "<name>" as "<rule>" rule violation

  Examples: Names that break the rules
  | name       | type      | rule              |
  | AbcM       |           | headlessCamelCase |
  | abc        |           | postfix "M"       |
  | variableM  | reference | prefix "r"        |
  | rvariable  | reference | postfix "M"       |
  | rvariableM | reference | CamelCase         |
