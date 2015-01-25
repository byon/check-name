Feature: Analysing variable names

Scenario: Forward declarations are skipped
    Given source with class declaration "some_class"
    When analysis is made
    Then analysis should report no rule violations

Scenario: Forward declarations namespaces are skipped
    Given source with namespace "boost"
    And nested class declaration "thread"
    When analysis is made
    Then analysis should report no rule violations
