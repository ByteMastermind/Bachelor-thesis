#Counting lines
line_count=$(find ./src -name "*.py" -exec grep -v '^ *#' {} + | grep -v '^ *$' | wc -l)
echo "Have $line_count lines of code in total"

#Removing unneseccary imports:
python -m autoflake --in-place --remove-all-unused-imports --expand-star-imports -r ./src --exclude __init__.py,toast_lib

#Sorting imports
python -m isort ./src --skip toast_lib 

#Formatting file:
python -m autopep8 --max-line-length 150 --in-place --aggressive --recursive ./src --exclude toast_lib

#Linting: 
python -m pylint ./src --ignore=toast_lib
