Feature: Analysing variable names

Scenario Outline: Succeeding analysis
    Given source with typedef "<name>"
    When analysis is made
    Then analysis should report no rule violations

  Examples: Names that follow the rules
  | name              |
  | Camel             |
  | AndOneWithCaseToo |


  Scenario Outline: Failing analysis
    Given source with typedef "<name>"
    When analysis is made
    Then analysis reports "typedef" "<name>" as "CamelCase" rule violation

  Examples: Names that break the rules
  | name                       |
  | lowercaseisjustsobadforyou |
  | no_snake_can_do            |
  | norShouldItStartAsLower    |
