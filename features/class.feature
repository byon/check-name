Feature: Analysing class names

  Scenario Outline: Succeeding analysis
    Given source with <type> "<name>"
    When analysis is made
    Then analysis should succeed

  Examples: Names that follow the rules
  | type            | name                   |
  | class           | NameInCamelCase        |
  | struct          | AnotherOne             |
  | interface class | AndSomethingAtEndIf    |
  | abstract class  | LikeTotallyAbstractAbs |

  Scenario Outline: Failing analysis
    Given source with <type> "<name>"
    When analysis is made
    Then analysis reports "<type>" "<name>" as "<cause>" rule violation

  Examples: Names that fail the rules
  | type            | name                | cause                   |
  | class           | notInCamelCase      | CamelCase               |
  | struct          | NeitherISThis       | CamelCase               |
  | interface class | ThePostFixIsMissing | postfix "If"            |
  | class           | ThereShouldNotBeIf  | redundant postfix "If"  |
  | abstract class  | WhereIsThePostFix   | postfix "Abs"           |
  | class           | ThereShouldNotBeAbs | redundant postfix "Abs" |
  | interface class | WrongPostfixAbs     | postfix "If"            |
  | abstract class  | TotallyIncorrectIf  | postfix "Abs"           |
