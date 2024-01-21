*** Variables ***
${hello}    Hello
${who}    John Doe

*** Test Cases ***
Demonstration Test
    Log    ${hello} ${who}

Demonstration Tag Test
    [Tags]   tag  tag1
    Log    Hello Tag1!

Demonstration Tag 2 Test
    [Tags]   tag  tag2
    Log    Hello Tag2!

Log With Levels
    Log    TRACE    level=TRACE
    Log    DEBUG    level=DEBUG
    Log    INFO
    Log    WARN    level=WARN
