### Mahiro Hirakawa

I build [Tracefold](https://github.com/TraceFold/tracefold): an agent's change is held with a
checked inverse **before** it lands, and every verdict becomes a receipt that verifies offline,
without trusting whoever issued it. Rust, with a machine-checked model in Lean beside it.

What holds my attention: inverses that are constructed and checked before a change lands,
rather than reconstructed afterwards and hoped about. Verification that needs no account and
trusts no server, mine included. Formal methods pointed at ordinary tools instead of at
spacecraft. And being exact about what a tool cannot take back, which is the half that usually
goes unwritten.

It is not released, and there are platforms it has never run on: Windows, OneDrive and network
shares have zero measured runs. One part of it does work with nothing installed, if you want to
check a receipt rather than take my word for any of this:
[in a browser tab](https://tracefold.github.io/tracefold/verify.html).

An issue on [the repository](https://github.com/TraceFold/tracefold/issues) reaches me and
leaves a public record.
