Feature: Analysing class names

  Scenario: Classes not in CamelCase are reported
    Given source with class "aBc"
    When analysis is made
    Then analysis reports "class" "aBc" as "CamelCase" rule violation

  Scenario: Structs not in CamelCase are reported
    Given source with struct "aBc"
    When analysis is made
    Then analysis reports "struct" "aBc" as "CamelCase" rule violation

  Scenario: Interface classes require If-postfix
    Given source with class "Class"
    And nested pure virtual method "method"
    When analysis is made
    Then analysis reports "interface class" "Class" as "postfix \"If\"" rule violation

  Scenario: Normal classes require do not require a postfix
    Given source with class "Class"
    And nested method "method"
    When analysis is made
    Then analysis should succeed
