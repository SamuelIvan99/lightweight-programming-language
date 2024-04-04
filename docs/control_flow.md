# Control Flow

The ability to run code depending on whether a condition is true and to run code repeatedly while a condition is true are basic building blocks in most programming languages. The most common constructs that handle control flow of execution of code are if expressions and loops.

## if Expressions

An if expression allows to branch code depending on conditions.

All if expressions start with the keyword if, followed by a condition. We place the block of code to execute if the condition is true immediately after the condition inside curly brackets.

Optionally, an else expression can be included, to give the program an alternative block of code to execute should the condition evaluate to false. If no else expression is provided and the condition is false, the program will just skip the if block and move on to the next bit of code.

```
i32 temperature = 25;

if (temperature > 30) {
    # if block code
} else {
    # else block code
}
```

In this example, the program checks the value of the temperature variable. If it's greater than 30, it will run code in the if block. Otherwise, it will run code in else block.

## Loops

It’s often useful to execute a block of code more than once. For this task, Based provides several loops, which will run through the code inside the loop body to the end and then start immediately back at the beginning.

Based has two kinds of loops: while and for.

### while

A while loop repeatedly executes a block of code as long as a specified condition is true. The syntax for a while loop is:

```
while (condition) {
    # code block to be executed
}
```

Here, condition is a Boolean expression that is evaluated before each iteration of the loop. If the condition evaluates to true, the code block inside the loop is executed. Afterward, the condition is evaluated again, and if it's still true, the code block is executed again. This process continues until the condition becomes false, at which point the loop terminates, and the program moves on to the next section of code.

```
var count = 0;
while (count < 5) {
    # code in while block
    count = count + 1;
}
```

This while loop will run the code inside the while block as long as it is less than 5. The loop terminates when count becomes 5 or greater.

### for
