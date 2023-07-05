Date: 2019-07-06
Title: Andaluh-rs, a lib to transcript Spanish to Andaluh
Tags: gnome, software, andaluh, language
Slug: andaluh
Gravatar: 8da96af78e0089d6d970bf3760b0e724
Category: blog

Spain is a big region with a lot of languages, we've the official one for
the whole region, Spanish or Castilian (es-ES), and other officials languages
spoken in other regions, like the Galician (gl-ES) spoken in Galicia,
the Basque (eu-ES), spoken in the Basque Country, the Catalan (ca-ES)
spoken in Catalonia.

But we've more languages that doesn't have the same official support, the
Valencian, the Aragonese, the Asturian, [and more][4]. And also we've some
**dialects** like the *Andalusian*.

All of this languages was discredit during the dictatorship period when the
only official language was the Spanish and the others was treated like
vulgar languages or non educated one, and in some cases the language was
*prohibited*.

Whe the *democracy* arrives, some regions spend a lot of resources trying to
recover the language and are supporting it until now with official institutions
and lessons in the official education system. But in other regions the stigma
continued until today.

That's the case of the *Andalusian*, that right now is not considered a language
but a dialect. In any case, this *dialect* is treated as a non cultivated
language, spoken by illiterates. We've a lot of Spanish movies and Series where
the character that spoke *Andalusian* was the illiterate, from the countryside
or the servant of the family.

## Be proud of it

In Andalusia we've a lot of culture, literature and music done in *Andalusian*,
but we don't have a way to write that and many people try to avoid the *acent*
and the local words to look more cultured and because there's no a writing
system, we write in Spanish, it's hard to write lyrics, poetry and other
kind of literature. The Andalusian is not only a way to talk, some words are
short and we've contractions and other vowel sounds so if you write in Spanish,
it's not the same as spoken, some information is missed and for example in music
or poetry the metric doesn't match.

There's a [movement][1] trying to define a writing **Andalusian** and promoting the
language, trying to make people proud of it and talk and write without complexes.

## Translator, here comes the code

And there's a [group of developers][2] that are working in some tools to provide
direct translation from Spanish and other tools to ease the **Andalusian** writing.

I like to write code and I'm always happy to find new problems to solve, to learn
new languages, tools and to spend some time trying to code something that I've not
done before. So I decided to write a translator from Spanish to Andaluh using rust,
and I've created the [andaluh-rs][3] lib.

The translator is more or less easy, there're some rules that should be applied
from top to bottom that basically replaces some group of letters. There's a
implementation in [python][5] that uses regular expressions for that. There're
a lot of regular expressions, so I thougth that it could be easy to use a parser,
so I used the [pest parser][6].

```
// supress muted /h/

H = { ("h" | "H") }
initial_h = { H ~ letter }
CH = { C ~ H }
inner_ch = { CH ~ letter }
inner_h = { !inner_ch ~ H ~ letter }
hua = { H ~ ("ua" | "UA" | "Ua" | "uA") }
hue = { H ~ ("ue" | "UE" | "Ue" | "uE") }
noh = { !CH ~ !H ~ letter }
h = _{ ((sp|SOI)? ~ initial_h* ~ ((hua | hue | inner_ch | inner_h) | noh+)+)+ }
```

I've defined each rule in the pest format, so I've a parser for each rule
and then I can replace the word with the correct replacement.

```rust
pub fn h_rule(input: &str) -> Result<String, Error> {
    rule!(Rule::h, &input, Some(&defs::H_RULES_EXCEPT),
        Rule::initial_h | Rule::inner_h => |pair: Pair<Rule>| {
            let s = pair.as_str();
            let h = slice!(s, 0, 1);
            let next = slice!(s, 1);
            keep_case(&next, &h)
        },
        Rule::hue => |pair: Pair<Rule>| {
            keep_case("güe", &pair.as_str())
        },
        Rule::hua => |pair: Pair<Rule>| {
            keep_case("gua", &pair.as_str())
        })
}
```

To simplify the code, I've defined the `rule` macro, with the code used in
all rules:

```rust
macro_rules! rule {
    ($rule: expr, $input: expr, $( $($t: pat)|* => $r: expr ),* ) => {{
        let map: Option<HashMap<&str, &str>> = None;
        rule!($rule, $input, map, $( $($t)|* => $r ),*)
    }};
    ($rule: expr, $input: expr, $map: expr, $( $($t: pat)|* => $r: expr ),* ) => {{
        let (repl, input) = match $map {
            Some(ref m) => replace_exceptions($input, m),
            None => (vec![], $input.to_string())
        };

        let pairs = AndaluhParser::parse($rule, &input)?;
        let mut output: Vec<String> = vec![];

        for pair in pairs {
            let chunk = match pair.as_rule() {
                $( $($t)|* => {
                    $r(pair)
                } ),*
                _ => {
                    String::from(pair.as_str())
                },
            };
            output.push(chunk);
        }

        let mut outstr = output.join("");

        if $map.is_some() {
            outstr = replace_exceptions_back(&outstr, repl);
        }

        Ok(outstr)
    }}
}
```

And because the Spanish and the Andaluh languages uses unicode and rust Strings
can not be iterated by *unicode*, I've used `unicode_segmentation` crate, and
defined some utility macros to get the real String len and to get slices of that
String.

```rust
macro_rules! chars {
    ($input: expr) => {
        UnicodeSegmentation::graphemes($input, true)
    }
}

macro_rules! slice {
    ($input: expr, $start: expr, $end: expr) => {
        chars!($input)
            .skip($start)
            .take($end - $start)
            .collect::<String>()
    };
    ($input: expr, $start: expr) => {
        chars!($input)
            .skip($start)
            .collect::<String>()
    }
}

macro_rules! len {
    ($input: expr) => {
        chars!($input).count()
    }
}
```

With all this done, we only have to apply all rules, in the correct order,
to the input string so we can get the translated String as output.

```rust
pub fn epa(input: &str) -> Result<String, Error> {
    // TODO: escape links
    let rules = [
        h_rule,
        x_rule,
        ch_rule,
        gj_rule,
        v_rule,
        ll_rule,
        l_rule,
        psico_rule,
        vaf_rule,
        word_ending_rule,
        digraph_rule,
        exception_rule,
        word_interaction_rule,
    ];

    let mut output = input.to_string();
    for r in rules.iter() {
        let out = r(&output)?;
        output = out.to_string();
    }

    Ok(output)
}
```

## Performance

This code is not the best one, I'm doing a lot of string operations with copies
and clones, I'm sure that anyone with more experience with rust can view a lot
of points where we can optimize this code. At first I thought that the translation
could be done during the parsing, keeping a length to be able to view backward
and forward.

Maybe it's possible to read char by char, keeping a buffer, and detecting if
we can apply any of the rules with the content in the buffer, but I've based
this lib in the python one, so for me it was easier to translate each regex to
pest regex and then do the same translations in the lib.

But I still think that there's a better solution for this problem, but some times
it's better to have something that just works instead of a never done best
solution.

During this process I've learned to use pest and I've been playing a lot with
regular expressions, so it was a fun project.

[1]: https://andaluh.es/
[2]: https://github.com/andalugeeks/
[3]: https://github.com/andalugeeks/andaluh-rs
[4]: https://en.wikipedia.org/wiki/Languages_of_Spain
[5]: https://github.com/andalugeeks/andaluh-py
[6]: https://github.com/pest-parser/pest
