
# Coding Standards

## 1. Naming Conventions
* **Variables and Functions**: Use  camelCase  for variable and function names.
    - Example:  `userName`,  `fetchUserData()`
    - **EXCEPTION**: React component functions must start with a capital letter
* **Classes**: Each word in a class should start with an uppercase letter.
    - Example:  `UserController`,  `DatabaseService`
* **Constants**: Use  UPPER_CASE  with underscores for constants.
    - Example:  `MAX_USERS`,  `DEFAULT_TIMEOUT`
* **File Names**: Use  lowercase letters and underscores to represent spaces.
	- Example:  `file_name`,  `backend`
* **Avoid ambiguous names**: Choose names that clearly describe the variable or function purpose.

## 2. Formatting
* **Indentation**: Should be 4 spaces.
* **Curly Braces**:
    * Place opening braces on the same line as the control statement.
        * Example: 
        ``` 
        if(condition) {
		    // code
        } 
        ```         
* **Semicolons**: Use semicolons to end statements in languages that allow them (e.g., JavaScript).

## 3. Commenting
* **Single-Line Comments**: Use  `//` or `#`  for single-line comments to describe specific lines of code.
    * Place comments on the line above the code where clarity is needed.
* **Multi-Line Comments**: Use  `/* ... */` or `''' ... '''`  for multi-line comments or explanations of larger blocks.