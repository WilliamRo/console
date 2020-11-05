Console
-------

This package provides necessary tools for printing text (with fancy styles
if specified) in terminal.
To use, import an instance of `Console` class by 
```python
from console import console
```

### Text With Fancy Styles
Fancy texts are produced based on `termcolor` package.
The usage of this package is similar to `termcolor`:
```python
console.write_line('Hello World!', color='yellow')
```
However, `console` provides another way to print text base on a simple **syntax**,
which is more flexible and powerful:
```python
console.write_line('#{Hello}{red} #{World}{blue}{bold}!')
```
Here, the syntax is `#{<text>}[{<text_color>}][<text_highlight>}][{<attributes_1>}]...[{<attributes_N>}]`.

Example of other fancy usages:
```python
console.split('#{-}{red}#{-}{yellow}#{-}{blue}')
```
