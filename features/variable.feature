Feature: Analysing variable names

  Scenario: Variables in headlessCamelCase are not reported
    Given source with variable "aBc"
    When analysis is made
    Then analysis should report no rule violations

  Scenario: Variables not in headlessCamelCase are reported
    Given source with variable "Abc"
    When analysis is made
    Then analysis reports "variable" "Abc" as "headlessCamelCase" rule violation
