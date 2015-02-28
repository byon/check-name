Feature: Analysing enumeration names

  Scenario Outline: Succeeding analysis for enumeration names
    Given source with enumeration "<name>"
    When analysis is made
    Then analysis should report no rule violations

  Examples: Names that follow the rules
  | name      |
  | Hump      |
  | CamelCase |

  Scenario Outline: Failing analysis for enumeration names
    Given source with enumeration "<name>"
    When analysis is made
    Then analysis reports "enumeration" "<name>" as "CamelCase" rule violation

  Examples: Names that break the rules
  | name                 |
  | humpHump             |
  | caseless             |
  | snaky_snake          |
  | SCREAM_BLOODY_MURDER |

  Scenario Outline: Succeeding analysis for enumeration constants
    Given source with enumeration "ValidName"
    And nested enumeration constant "<name>"
    When analysis is made
    Then analysis should report no rule violations

  Examples: Names that follow the rules
  | name           |
  | AAAAAAARGHHH   |
  | MORE_MORE_MORE |

  Scenario Outline: Failing analysis for enumeration constants
    Given source with enumeration "ValidName"
    And nested enumeration constant "<name>"
    When analysis is made
    Then analysis reports "enumeration constant" "<name>" as "SCREAMING_SNAKE_CASE" rule violation

  Examples: Names that break the rules
  | name           |
  | whisper        |
  | snaky_whisper  |
  | camelyWhisper  |
  | NamedLikeAType |
