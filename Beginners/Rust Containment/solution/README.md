An obvious first step is to see what we have available: googling "rust default import" we see the [prelude](https://doc.rust-lang.org/std/prelude/index.html) first.

The prelude doesn't contain much, but you might notice that there are no macros there! If you look into it, you can find that macros from std namespace are available by default, too.

You can find a list of those macros in the docs [here](https://doc.rust-lang.org/std/index.html), after which it's not hard to notice that we can include the code (with the flag in it) with:
```Rust
panic!(include_str!(file!()))
```