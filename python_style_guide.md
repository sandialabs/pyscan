# Pyscan Python Style Guide

## 1. Summary

Python is the main launguage for pyscan's code. This style guide is a list of rules for 
writing python code for pyscan and pyscan documentation.

## 2. Python's PEP rules

### 2.1 Linting and Flake8

Linting is the analysis of source code and flagging potential problems.  The linter used 
in pyscan is flake8.  We have default flake8 rules in our .flake8 file.  Your code should be
linted before upload via 

`flake8 .`

but is also auto run on the main and development branches upon commit. 

### 2.2 Autopep8

Autopep8 can be used to correct pep8 errors. Though be caeful that this may not correct all 
pep8 issues.  Implement autopep8 via 

`autopep8 --in-place --aggressive -r --max-line-length 120 -v .`

--in-place makes changes in the file<br>
--aggressive changes errors other than just spacing<br>
-r is recursive over all files in the directories<br>
--max-line-length 120 self explanitory<br>
-v verbose prints out changes <br>

in the home directory of pyscan. This significantly helps with small, repeated issues such
blank spaces in empty lines and extra spaces at the end of lines, which no one really wants
to correct on their own. 

## 3 Naming Conventions

The styles are for different types of python entities are listed below and is largely taken from the style guide at https://realpython.com/python-pep8/ 


### 3.1 Functions
|Type | Style | Example|
|----|-----|------|
|Functions| Use a lowercase word or words. Separate words by underscores.| first_string, same_length,|
|Variables | Use a lowercase single letters, word, or words. Separate words by underscores.| x, variable, other_variable|
|Class| Start each word with a capital letter. Do not separate words with underscores. | ItemAttribute, Sweep|
|Method| Same as functions| | 
|Constants| Use an uppercase single letter, word, or words. Separate words with underscores. | X, CONTSANT, OTHER_CONSTANT |
|Files| Use a short, lowercase word or words. Separate words with underscores. | |
|Package| Use a short, lowercase word or words. Do not separate words with underscores.| pyscan, qick-dawg|

## 4 Documentaiton Formatting

Much of the content in our docstrings are taken from the fromatting prescribed by 
numpy docs and is outlined in this document. 


### 4.1 Docstring Structure

The docstring for a function or class definition should be located directly under the 
definition line enclosed with three triple quotes """ """ 

If the enclosed docstring can be a single line keep the doc string on a single line. Such as 

`"""Short docuement string"""`

If the docstring must be on mulitple lines, leave the three double quotes on their own lines. Such as:

```
"""
Long document
string example
"""
```

### 4.2 Referencing functions, classes, etc. in Docstring

### 4.3 What is included in Docstrings for functions

1. The first line should contain a brief describtion of what the function does. 

2. (optional) The second section will have a more detailed description of the the function, if required. 

3. All input parameters the the function are listed as `<parameter_name>: <type>(s)` with a brief description of the parameter

4. A "return" section is included at the end with a type and description of what is being returned. 

Example template:

```
"""
Short description

Long description

Parameters
----------
<parameter_name>: <type>(s)
    <parameter description>

Returns
-------
<return_type>
    <return description>
"""
```


### 4.4 What is included in Docstrings for classes

Example template:

```
"""
Short description

Long description

Parameters
----------
<parameter_name>: <type>(s)
    <parameter description>

Attributes
----------
<attribute_name>: <type>(s)
    <attribute description>

Properties
----------
<property_name>: <type>(s)
    <property description>

Methods
-------
<method_name>(<parameters>) 
    <method description>

Class Functions
---------------
<method_name>(<parameters>) 
    <method description>


"""
```
