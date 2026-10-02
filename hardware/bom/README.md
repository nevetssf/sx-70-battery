# Bills of Materials

```
bom-option-a-aaa.csv    Option A — 4x regulated 1.5 V AAA
bom-option-b-lipo.csv   Option B — 2S LiPo + USB-C charger + adjustable buck
digikey-order.csv       Consolidated Digi-Key line items across pack, flex and bench
<ref>-<part>/           Reference material per part
```

## Per-part directories

One directory per BOM reference, holding whatever was gathered while sourcing it: vendor photos, datasheets, dimension drawings, screenshots of listings, and a `notes.md` recording what was actually verified versus assumed.

Listings vanish and vendors swap revisions without changing the listing, so anything that settled a decision gets saved here rather than linked.

| Directory | Ref | Part |
|---|---|---|
| `U1-2s-protection/` | U1 | 2S protection board (DW01/8205-class) |
| `U2-ip2326-charger/` | U2 | IP2326 USB-C 2S charger module |
| `U3-pololu-d30v33/` | U3-alt | Pololu D30V33MALCMA fine-adjust buck (fallback; U3 is the TPS630702 on PCB1) |
| `B1-lipo-2s/` | B1 | 2S LiPo pack |
| `P1-pogo-millmax-7982/` | P1 | Mill-Max 7982-1 spring-loaded pins |
| `PCB1-carrier/` | PCB1 | Carrier PCB — see [docs/pcb.md](../../docs/pcb.md) |
| `enclosure-hardware/` | — | Inserts, screws, magnets, steel shim |
