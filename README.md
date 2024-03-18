# Introduction
As i explore large language models, i realize that programming languages of today are not necessarily how we may program in the future and that a different approach may be required for programming with LLM's.

For this reason, i think it's important to go back to early in computer programming history to look at how programming languages evolved and how we can simplify for the future.

Although I could have chosen many languages for this experiment such as FORTRAN, COBOL, ASSEMBLY, PASCAL, ALGOL or C, i felt picking the simplest possible language that is close as possible to assembly language as possible made the most sense.  I also wanted to pick a language that was essentially interpreted rather than compiled in nature.   For this reason I settled on BASIC.

## The Initial Goal
The initial goal of this project is to build as WebAssembly + WASI interpreter for BASiC.  This interpreter should be ultimately compatible with various flavors of BASIC including

- Dartmouth BASIC
- Vintage BASIC
- Microsoft (ALTAIR) BASIC

It should be possible to be able to old vintage games within the environment such aceyducey, basketball or maze.
Since the BASIC interpreter can run using WASI then it will be possible to run on a webbrowser or server-side using something like a WASM rubtime with the WASI extensions.

# The Approach
In order to achieve the initial goal, we need to perform 4 tasks.

- Build a Tokenizer
- Build a AST Parser
- Build a Web Assembly Emitter
- Build an execution environent

## Implementation Status
The following describes where we are in the process

| Stage     | Status    |
| --------- | --------- |
| Tokenizer | Complete  |

The next stage in the process is to build 

### The Tokenizer
The tokenizer should now correctly tokenize, if you wish to test the tokenizer, you can run

```bash
python main.py
```

or within the lexer folder, you can run

```bash
pytest
```

This has been tested against basic programs like aceyducey and some old dartmouth basic programs and it seems to tokenize well
