black src
black tests
autoflake --in-place --remove-all-unused-imports --remove-unused-variables -r src
autoflake --in-place --remove-all-unused-imports --remove-unused-variables -r tests