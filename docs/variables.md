# Variables

## Introduction

Variables are fundamental building blocks in Based. They allow you to store and manipulate data throughout your program. This page covers the syntax, types, and scope of variables in Based.

## Declaring Variables

Variables are declared using the `let` keyword followed by the variable name and type declaration.

```
let x:i32 = 0
```

```
let age:i32 = 25;             // Integer type variable
let name:str = "Alice";       // String type variable
let isStudent:bool = true;    // Boolean type variable
let height:f32 = 5.9;         // Float type variable
```

```
let clothing:str[] = ["pants", "t-shirt", "beanie"]
```

## Variable Scope

Variables in Based can have different scopes depending on where they are declared.

### Global Scope

Variables declared outside of any function or block have global scope and can be accessed from anywhere in the program.

```
let globalVar:i32 = 0;

changeGlobalVar():i32 {
    globalVar = 5;  // Accessible here
}
```

### Local Scope

Variables declared within a function or block have local scope and can only be accessed within that function or block.

```
exampleFunction(): abyss {
    let localVar:i32 = 0;
    localVar = 5;  // Accessible here
}

// localVar = 20;  // Error: localVar is not accessible here
```

### Block Scope

Variables declared within a loop or conditional block are accessible only within that block.
