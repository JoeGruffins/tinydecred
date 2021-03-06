# decred

The `decred` package contains everything needed to create
[Decred](https://decred.org/) applications in Python.

## Features

1. Pure-Python secp256k1 elliptic curve.

1. Serializable and de-serializable python versions of important types
from the `dcrd/wire` package: `MsgTx`, `BlockHeader`, `OutPoint`, etc.

1. BIP-0044 keys. Account creation and management. PGP mnemonic seeds.

1. Network parameters for mainnet, testnet3, and simnet.

1. Clients for the dcrdata block explorer API (websockets, pubsub, HTTP).

## DcrdataClient

DcrdataClient is a dcrdata API client written in Python 3.

The constructor takes a single argument, which is the path to a dcrdata server,
including protocol, e.g. `https://explorer.dcrdata.org/`. The available
endpoints are gathered from the server when the client is created.

```
from decred.dcr.dcrdata import DcrdataClient
import json

client = DcrdataClient("https://explorer.dcrdata.org")
bestBlock = client.block.best()
print(json.dumps(bestBlock, indent=4, sort_keys=True))
```

Because the available dcrdata endpoints can change with new versions, the
interface is generated by pulling a list of endpoints from the API itself.
The acquired list does not include some endpoints, particularly the Insight API
endpoints.

You can print an endpoint guide to the console with  `client.endpointGuide()`,
or a Python list of URLs is returned from `client.endpointList()`.

Depending on the version of dcrdata they are running, different servers might
have different sets of endpoints.

## Examples

In the [`examples`](./examples) directory there are scripts for creating and
using wallets, and for using dcrdata and matplotlib to plot Decred network data.

Here are some more examples:

```
def dumpResponse(obj):
    print(json.dumps(obj, indent=4, sort_keys=True))

blockhash = "00000000000000000fe92d4a057bd4425c5f58fa9b4d5b34b6f2b596ff01b3c9"
txid = "355a6752539486503031d1a0bb62a3c53f83a4cad0765979510742b72b064f75"

# /block/hash/{blockhash} - Get data for a block with it's hash.
dumpResponse( client.block.hash(blockhash) )

# /block/hash/{blockhash}/verbose - Same thing, but more info.
dumpResponse( client.block.hash.verbose(blockhash) )

# /block/range/{idx0}/{idx}/{step}/size - Get the size of every 10th block from
# 299900 to 300000.
idx0 = 299900
idx = 300000
step = 10
dumpResponse( client.block.range.size(idx0, idx, step) )

# /tx/{txid}/in/{txinoutindex} - Get a single input to a transaction
txinoutindex = 0
dumpResponse( tx.__getattr__("in")(txid, txinoutindex) )

# arguments can also be passed as keyword argument, in which case the
# order doesn't matter, but don't mix positional and keyword.
thatOneBlock = "00000000000000000fe92d4a057bd4425c5f58fa9b4d5b34b6f2b596ff01b3c9"
dumpResponse( client.block.hash(blockhash=thatOneBlock) )
```

The dcrdata module includes websocket functionality as well. Subscribe to a
block feed or updates for addresses.

```
client.emitter = dumpResponse
client.subscribeAddresses(["Dcur2mcGjmENx4DhNqDctW5wJCVyT3Qeqkx"])
input("press return to close")
```

### Example endpoint guide
```
address.amountflow(address, chartgrouping)      ->  /address/{address}/amountflow/{chartgrouping}
address.count(address, N)                       ->  /address/{address}/count/{N}
address.count.raw(address, N)                   ->  /address/{address}/count/{N}/raw
address.count.skip(address, N, M)               ->  /address/{address}/count/{N}/skip/{M}
address.count.skip.raw(address, N, M)           ->  /address/{address}/count/{N}/skip/{M}/raw
address.raw(address)                            ->  /address/{address}/raw
address.totals(address)                         ->  /address/{address}/totals
address.types(address, chartgrouping)           ->  /address/{address}/types/{chartgrouping}
block.best()                                    ->  /block/best
block.best.hash()                               ->  /block/best/hash
block.best.header()                             ->  /block/best/header
block.best.header.raw()                         ->  /block/best/header/raw
block.best.height()                             ->  /block/best/height
block.best.pos()                                ->  /block/best/pos
block.best.raw()                                ->  /block/best/raw
block.best.size()                               ->  /block/best/size
block.best.subsidy()                            ->  /block/best/subsidy
block.best.tx()                                 ->  /block/best/tx
block.best.tx.count()                           ->  /block/best/tx/count
block.best.verbose()                            ->  /block/best/verbose
block.hash(blockhash)                           ->  /block/hash/{blockhash}
block.hash.header(blockhash)                    ->  /block/hash/{blockhash}/header
block.hash.header.raw(blockhash                 ->  /block/hash/{blockhash}/header/raw
block.hash.height(blockhash)                    ->  /block/hash/{blockhash}/height
block.hash.pos(blockhash)                       ->  /block/hash/{blockhash}/pos
block.hash.raw(blockhash)                       ->  /block/hash/{blockhash}/raw
block.hash.size(blockhash)                      ->  /block/hash/{blockhash}/size
block.hash.subsidy(blockhash)                   ->  /block/hash/{blockhash}/subsidy
block.hash.tx(blockhash)                        ->  /block/hash/{blockhash}/tx
block.hash.tx.count(blockhash)                  ->  /block/hash/{blockhash}/tx/count
block.hash.verbose(blockhash)                   ->  /block/hash/{blockhash}/verbose
block.range(idx0, idx)                          ->  /block/range/{idx0}/{idx}
block.range.size(idx0, idx)                     ->  /block/range/{idx0}/{idx}/size
block.range(idx0, idx, step)                    ->  /block/range/{idx0}/{idx}/{step}
block.range.size(idx0, idx, step)               ->  /block/range/{idx0}/{idx}/{step}/size
block.hash(idx)                                 ->  /block/{idx}/hash
block.header(idx)                               ->  /block/{idx}/header
block.header.raw(idx)                           ->  /block/{idx}/header/raw
block.pos(idx)                                  ->  /block/{idx}/pos
block.raw(idx)                                  ->  /block/{idx}/raw
block.size(idx)                                 ->  /block/{idx}/size
block.subsidy(idx)                              ->  /block/{idx}/subsidy
block.tx(idx)                                   ->  /block/{idx}/tx
block.tx.count(idx)                             ->  /block/{idx}/tx/count
block.verbose(idx)                              ->  /block/{idx}/verbose
chart.market(token)                             ->  /chart/market/{token}
chart.market.candlestick(token, bin)            ->  /chart/market/{token}/candlestick/{bin}
chart.market.depth(token)                       ->  /chart/market/{token}/depth
exchanges.codes()                               ->  /exchanges/codes
mempool.sstx()                                  ->  /mempool/sstx
mempool.sstx.details()                          ->  /mempool/sstx/details
mempool.sstx.details(N)                         ->  /mempool/sstx/details/{N}
mempool.sstx.fees()                             ->  /mempool/sstx/fees
mempool.sstx.fees(N)                            ->  /mempool/sstx/fees/{N}
stake.diff()                                    ->  /stake/diff
stake.diff.b(idx)                               ->  /stake/diff/b/{idx}
stake.diff.current()                            ->  /stake/diff/current
stake.diff.estimates()                          ->  /stake/diff/estimates
stake.diff.r(idx0, idx)                         ->  /stake/diff/r/{idx0}/{idx}
stake.pool()                                    ->  /stake/pool
stake.pool.b(idx)                               ->  /stake/pool/b/{idx}
stake.pool.b.full(idxorhash)                    ->  /stake/pool/b/{idxorhash}/full
stake.pool.full()                               ->  /stake/pool/full
stake.pool.r(idx0, idx)                         ->  /stake/pool/r/{idx0}/{idx}
stake.powerless()                               ->  /stake/powerless
stake.vote()                                    ->  /stake/vote
stake.vote.info()                               ->  /stake/vote/info
status.happy()                                  ->  /status/happy
ticketpool.bydate(tp)                           ->  /ticketpool/bydate/{tp}
ticketpool.charts()                             ->  /ticketpool/charts
tx.decoded(txid)                                ->  /tx/decoded/{txid}
tx.hex(txid)                                    ->  /tx/hex/{txid}
tx.__getattr__("in")(txid)                      ->  /tx/{txid}/in
tx.__getattr__("in")(txid, txinoutindex)        ->  /tx/{txid}/in/{txinoutindex}
tx.out(txid)                                    ->  /tx/{txid}/out
tx.out(txid, txinoutindex)                      ->  /tx/{txid}/out/{txinoutindex}
tx.tinfo(txid)                                  ->  /tx/{txid}/tinfo
tx.trimmed(txid)                                ->  /tx/{txid}/trimmed
tx.vinfo(txid)                                  ->  /tx/{txid}/vinfo
txs.trimmed()                                   ->  /txs/trimmed
```
