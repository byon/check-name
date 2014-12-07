Feature: Analysing class names

  Scenario: Classes not in CamelCase are reported
    Given source with class "aBc"
    When analysis is made
    Then analysis reports "class" "aBc" as "CamelCase" rule violation

  Scenario: Structs not in CamelCase are reported
    Given source with struct "aBc"
    When analysis is made
    Then analysis reports "struct" "aBc" as "CamelCase" rule violation
