Feature: Analysing method and function names

  Scenario: Methods not in headlessCamelCase are reported
    Given source with class "Class"
    And nested method "Foo"
    When analysis is made
    Then analysis reports "method" "Foo" as "headlessCamelCase" rule violation

  Scenario: Functions not in headlessCamelCase are reported
    Given source with function "Foo"
    When analysis is made
    Then analysis reports "function" "Foo" as "headlessCamelCase" rule violation

  Scenario: Function templates not in headlessCamelCase are reported
    Given source with template function "Foo"
    When analysis is made
    Then analysis reports "function" "Foo" as "headlessCamelCase" rule violation
