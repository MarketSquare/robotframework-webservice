*** Tasks ***
This won't work
    Fail    Doh!

Task with variable
    ${puffer}    Set Variable    ${input}
    Log    ${input}
    Should Be Equal    ${input}    qwerty

Task with more variables
    Should Be Equal    ${firstname}    Max
    Should Be Equal    ${lastname}    Mustermann
