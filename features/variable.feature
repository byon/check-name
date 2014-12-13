Feature: Analysing variable names

  Scenario: Variables in headlessCamelCase are not reported
    Given source with variable "aBc"
    When analysis is made
    Then analysis should report no rule violations

  Scenario: Variables not in headlessCamelCase are reported
    Given source with variable "Abc"
    When analysis is made
    Then analysis reports "variable" "Abc" as "headlessCamelCase" rule violation

  Scenario: Member variables not in HeadlessCamelCase are reported
    Given source with class "Class"
    And nested variable "Abc"
    When analysis is made
    Then analysis reports "member variable" "Abc" as "headlessCamelCase" rule violation

  Scenario: Member variables without M-postfix are reported
    Given source with class "Class"
    And nested variable "abc"
    When analysis is made
    Then analysis reports "member variable" "abc" as "postfix \"M\"" rule violation

  Scenario: Member variables with M-postfix are not reported
    Given source with class "Class"
    And nested variable "abcM"
    When analysis is made
    Then analysis should succeed

  Scenario: References without r-prefix are reported
    Given source with variable "a"
    And reference variable "b" that is assigned "a"
    When analysis is made
    Then analysis reports "reference variable" "b" as "prefix \"r\"" rule violation
