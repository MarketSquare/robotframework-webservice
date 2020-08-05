*** Tasks ***
Das wird nichts
    Fail    Schrott!

Task mit Variable
    ${puffer}    Set Variable    ${eingabe}
    Log    ${eingabe}
    Should Be Equal    ${eingabe}    qwerty

Task mit mehreren Variablen
    Should Be Equal    ${vorname}    Max
    Should Be Equal    ${nachname}    Mustermann
