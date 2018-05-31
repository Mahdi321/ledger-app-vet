#!/usr/bin/env python
"""
*******************************************************************************
*   Ledger Blue
*   (c) 2016 Ledger
*
*  Licensed under the Apache License, Version 2.0 (the "License");
*  you may not use this file except in compliance with the License.
*  You may obtain a copy of the License at
*
*      http://www.apache.org/licenses/LICENSE-2.0
*
*  Unless required by applicable law or agreed to in writing, software
*  distributed under the License is distributed on an "AS IS" BASIS,
*  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
*  See the License for the specific language governing permissions and
*  limitations under the License.
********************************************************************************
"""
from ledgerblue.comm import getDongle
from decimal import Decimal
from vetBase import Transaction, UnsignedTransaction, Clause
from rlp import encode
from rlp.utils import decode_hex, encode_hex, str_to_bytes
from bip32 import bip32_path_message


chaintag = 207
blockref = "0x01bd39a05de362"
expiration = 720
gaspricecoef = 128
gas = 21000
dependson = 0
nonce = "0xc1dc42b4e7"

amount = Decimal(5) * 10**18
to = "0x655fe90ea5ced47e14b01b9eabbf9827366d77c7"
data = ""

tx = Transaction(
    chaintag=int(chaintag),
    blockref=decode_hex(blockref[2:]),
    expiration=int(expiration),
    gaspricecoef=int(gaspricecoef),
    gas=int(gas),
    dependson="",
    nonce=decode_hex(nonce[2:]),
    clauses=[Clause(to=decode_hex(to[2:]), value=int(amount), data=data)],
    reserved=""
)

encodedTx = encode(tx, UnsignedTransaction)

donglePath = bip32_path_message()
apdu = "e0040000".decode('hex') + chr(len(donglePath) + len(encodedTx)) + donglePath + encodedTx

dongle = getDongle(True)
result = dongle.exchange(bytes(apdu))

v = result[0]
r = int(str(result[1:1 + 32]).encode('hex'), 16)
s = int(str(result[1 + 32: 1 + 32 + 32]).encode('hex'), 16)

tx = Transaction(tx.nonce, tx.gasprice, tx.startgas, tx.to, tx.value, tx.data, v, r, s)

print "Signed transaction " + encode_hex(encode(tx))
