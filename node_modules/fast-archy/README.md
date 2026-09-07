# fast-archy

![npm bundle size](https://img.shields.io/bundlephobia/min/fast-archy) ![npm](https://img.shields.io/npm/v/fast-archy) ![NPM](https://img.shields.io/npm/l/fast-archy)

Render nested hierarchies `npm ls` style with unicode pipes.

Rewrite of [archy](https://www.npmjs.com/package/archy) in TypeScript, making it faster.

## Install

```sh
npm install fast-archy
```

## Usage

```js
import archy from "fast-archy";

const s = archy({
  label: "beep\none\ntwo",
  nodes: [
    "ity",
    {
      label: "boop",
      nodes: [
        {
          label: "o_O\nwheee",
          nodes: [
            {
              label: "oh",
              nodes: ["hello", "puny\nmeat"],
            },
            "creature",
          ],
        },
        "party\ntime!",
      ],
    },
  ],
});

console.log(s);
```

Output:

```
beep
│ one
│ two
├── ity
└─┬ boop
  ├─┬ o_O
  │ │ wheee
  │ ├─┬ oh
  │ │ ├── hello
  │ │ └── puny
  │ │     meat
  │ └── creature
  └── party
      time!
```

## API

### archy(obj, prefix?, opts?)

- `obj` `object|string` - Tree object or string label.
  - `obj.label` `string` - Node label.
  - `obj.nodes` `array` - Array of child nodes (same structure as `obj`).
- `prefix` `string` - Custom prefix for tree branches (default: `""`).
- `opts` `object` - Options object.
  - `opts.unicode` `boolean` - Use Unicode characters (default: `true`). If `false`, uses ASCII characters.

## Benchmarks

```
clk: ~3.91 GHz
cpu: 13th Gen Intel(R) Core(TM) i5-13400F
runtime: node 26.5.0 (x64-win32)

benchmark                   avg (min … max) p75 / p99    (min … top 1%)
------------------------------------------- -------------------------------
• archy - simple tree
------------------------------------------- -------------------------------
fast-archy                   113.96 ns/iter 116.77 ns 147.29 ns ▄██▅▃▃▂▁▁▁▁
archy                        458.72 ns/iter 452.59 ns 733.96 ns █▇▂▂▁▁▁▁▁▁▁

summary
  fast-archy
   4.03x faster than archy

• archy - medium tree
------------------------------------------- -------------------------------
fast-archy                   465.74 ns/iter 468.70 ns 619.04 ns ▃█▅▂▁▂▁▁▁▁▁
archy                          2.73 µs/iter   2.76 µs   3.17 µs ▂▆██▄▁▂▁▁▁▁

summary
  fast-archy
   5.87x faster than archy

• archy - complex tree
------------------------------------------- -------------------------------
fast-archy                   472.15 µs/iter 476.20 µs 717.20 µs ▆█▇▂▁▁▁▁▁▁▁
archy                          1.29 ms/iter   1.29 ms   1.68 ms ▁▃█▃▂▁▁▁▁▁▁

summary
  fast-archy
   2.73x faster than archy

• archy - ascii mode
------------------------------------------- -------------------------------
fast-archy (ascii)           440.13 ns/iter 440.60 ns 693.73 ns ▄█▂▂▁▁▁▁▁▁▁
archy (ascii)                  3.02 µs/iter   3.06 µs   3.16 µs ▁▁▃▄▃▄█▄▃▂▂

summary
  fast-archy (ascii)
   6.87x faster than archy (ascii)

• archy - beepHexo
------------------------------------------- -------------------------------
fast-archy                     1.32 ms/iter   1.32 ms   2.20 ms ▇█▂▁▁▁▁▁▁▁▁
archy                         10.07 ms/iter  10.15 ms  13.73 ms ▃█▆▂▂▁▁▁▁▁▁

summary
  fast-archy
   7.64x faster than archy
```

## License

MIT
