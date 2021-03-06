"""
Copyright (c) 2019-2020, the Decred developers
See LICENSE for details
"""

from decred.crypto.secp256k1 import field


class Test_FieldVal:
    def test_set_int(self):
        """
        test_set_int ensures that setting a field value to various native
        integers works as expected.
        """
        tests = [
            (1, [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),  # 1
            (5, [5, 0, 0, 0, 0, 0, 0, 0, 0, 0]),  # 5
            (65535, [65535, 0, 0, 0, 0, 0, 0, 0, 0, 0]),  # 2^16 - 1
            (67108864, [67108864, 0, 0, 0, 0, 0, 0, 0, 0, 0]),  # 2^26
            (67108865, [67108865, 0, 0, 0, 0, 0, 0, 0, 0, 0]),  # 2^26 + 1
            (4294967295, [4294967295, 0, 0, 0, 0, 0, 0, 0, 0, 0]),  # 2^32 - 1
        ]

        for i, v in tests:
            f = field.FieldVal()
            f.setInt(i)
            assert v == f.n

    def test_zero(self):
        """
        test_zero ensures that zeroing a field value works as expected.
        """
        f = field.FieldVal.fromHex(
            "a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5"
        )
        f.zero()
        assert all((x == 0 for x in f.n))

    def test_is_zero(self):
        """
        test_is_zero ensures that checking if a field is zero works as expected.
        """
        f = field.FieldVal()
        assert f.isZero()

        f.setInt(1)
        assert not f.isZero()

        f.zero()
        assert f.isZero()

    def test_normalize(self):
        """
        test_normalize ensures that normalizing the internal field words works
        as expected.
        """
        tests = [
            # 5
            [  # 0
                [0x00000005, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0x00000005, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            # 2^26
            [  # 1
                [0x04000000, 0x0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0x00000000, 0x1, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            # 2^26 + 1
            [  # 2
                [0x04000001, 0x0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0x00000001, 0x1, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            # 2^32 - 1
            [  # 3
                [0xFFFFFFFF, 0x00, 0, 0, 0, 0, 0, 0, 0, 0],
                [0x03FFFFFF, 0x3F, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            # 2^32
            [  # 4
                [0x04000000, 0x3F, 0, 0, 0, 0, 0, 0, 0, 0],
                [0x00000000, 0x40, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            # 2^32 + 1
            [  # 5
                [0x04000001, 0x3F, 0, 0, 0, 0, 0, 0, 0, 0],
                [0x00000001, 0x40, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            # 2^64 - 1
            [  # 6
                [0xFFFFFFFF, 0xFFFFFFC0, 0xFC0, 0, 0, 0, 0, 0, 0, 0],
                [0x03FFFFFF, 0x03FFFFFF, 0xFFF, 0, 0, 0, 0, 0, 0, 0],
            ],
            # 2^64
            [  # 7
                [0x04000000, 0x03FFFFFF, 0x0FFF, 0, 0, 0, 0, 0, 0, 0],
                [0x00000000, 0x00000000, 0x1000, 0, 0, 0, 0, 0, 0, 0],
            ],
            # 2^64 + 1
            [  # 8
                [0x04000001, 0x03FFFFFF, 0x0FFF, 0, 0, 0, 0, 0, 0, 0],
                [0x00000001, 0x00000000, 0x1000, 0, 0, 0, 0, 0, 0, 0],
            ],
            # 2^96 - 1
            [  # 9
                [0xFFFFFFFF, 0xFFFFFFC0, 0xFFFFFFC0, 0x3FFC0, 0, 0, 0, 0, 0, 0],
                [0x03FFFFFF, 0x03FFFFFF, 0x03FFFFFF, 0x3FFFF, 0, 0, 0, 0, 0, 0],
            ],
            # 2^96
            [  # 10
                [0x04000000, 0x03FFFFFF, 0x03FFFFFF, 0x3FFFF, 0, 0, 0, 0, 0, 0],
                [0x00000000, 0x00000000, 0x00000000, 0x40000, 0, 0, 0, 0, 0, 0],
            ],
            # 2^128 - 1
            [  # 11
                [
                    0xFFFFFFFF,
                    0xFFFFFFC0,
                    0xFFFFFFC0,
                    0xFFFFFFC0,
                    0xFFFFC0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
                [
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0xFFFFFF,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
            ],
            # 2^128
            [  # 12
                [
                    0x04000000,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x0FFFFFF,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
                [
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x1000000,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
            ],
            # 2^256 - 4294968273 (secp256k1 prime)
            [  # 13
                [
                    0xFFFFFC2F,
                    0xFFFFFF80,
                    0xFFFFFFC0,
                    0xFFFFFFC0,
                    0xFFFFFFC0,
                    0xFFFFFFC0,
                    0xFFFFFFC0,
                    0xFFFFFFC0,
                    0xFFFFFFC0,
                    0x3FFFC0,
                ],
                [
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x000000,
                ],
            ],
            # Prime larger than P where both first and second words are larger
            # than P's first and second words.
            [  # 14
                [
                    0xFFFFFC30,
                    0xFFFFFF86,
                    0xFFFFFFC0,
                    0xFFFFFFC0,
                    0xFFFFFFC0,
                    0xFFFFFFC0,
                    0xFFFFFFC0,
                    0xFFFFFFC0,
                    0xFFFFFFC0,
                    0x3FFFC0,
                ],
                [
                    0x00000001,
                    0x00000006,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x000000,
                ],
            ],
            # Prime larger than P where only the second word is larger
            # than P's second words.
            [  # 15
                [
                    0xFFFFFC2A,
                    0xFFFFFF87,
                    0xFFFFFFC0,
                    0xFFFFFFC0,
                    0xFFFFFFC0,
                    0xFFFFFFC0,
                    0xFFFFFFC0,
                    0xFFFFFFC0,
                    0xFFFFFFC0,
                    0x3FFFC0,
                ],
                [
                    0x03FFFFFB,
                    0x00000006,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x000000,
                ],
            ],
            # 2^256 - 1
            [  # 16
                [
                    0xFFFFFFFF,
                    0xFFFFFFC0,
                    0xFFFFFFC0,
                    0xFFFFFFC0,
                    0xFFFFFFC0,
                    0xFFFFFFC0,
                    0xFFFFFFC0,
                    0xFFFFFFC0,
                    0xFFFFFFC0,
                    0x3FFFC0,
                ],
                [
                    0x000003D0,
                    0x00000040,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x000000,
                ],
            ],
            # Prime with field representation such that the initial
            # reduction does not result in a carry to bit 256.
            #
            # 2^256 - 4294968273 (secp256k1 prime)
            [  # 17
                [
                    0x03FFFC2F,
                    0x03FFFFBF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x003FFFFF,
                ],
                [
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                ],
            ],
            # Prime larger than P that reduces to a value which is still
            # larger than P when it has a magnitude of 1 due to its first
            # word and does not result in a carry to bit 256.
            #
            # 2^256 - 4294968272 (secp256k1 prime + 1)
            [  # 18
                [
                    0x03FFFC30,
                    0x03FFFFBF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x003FFFFF,
                ],
                [
                    0x00000001,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                ],
            ],
            # Prime larger than P that reduces to a value which is still
            # larger than P when it has a magnitude of 1 due to its second
            # word and does not result in a carry to bit 256.
            #
            # 2^256 - 4227859409 (secp256k1 prime + 0x4000000)
            [  # 19
                [
                    0x03FFFC2F,
                    0x03FFFFC0,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x003FFFFF,
                ],
                [
                    0x00000000,
                    0x00000001,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                ],
            ],
            # Prime larger than P that reduces to a value which is still
            # larger than P when it has a magnitude of 1 due to a carry to
            # bit 256, but would not be without the carry.  These values
            # come from the fact that P is 2^256 - 4294968273 and 977 is
            # the low order word in the internal field representation.
            #
            # 2^256 * 5 - ((4294968273 - (977+1)) * 4)
            [  # 20
                [
                    0x03FFFFFF,
                    0x03FFFEFF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x0013FFFFF,
                ],
                [
                    0x00001314,
                    0x00000040,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x000000000,
                ],
            ],
            # Prime larger than P that reduces to a value which is still
            # larger than P when it has a magnitude of 1 due to both a
            # carry to bit 256 and the first word.
            [  # 21
                [
                    0x03FFFC30,
                    0x03FFFFBF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x07FFFFFF,
                    0x003FFFFF,
                ],
                [
                    0x00000001,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000001,
                ],
            ],
            # Prime larger than P that reduces to a value which is still
            # larger than P when it has a magnitude of 1 due to both a
            # carry to bit 256 and the second word.
            #
            [  # 22
                [
                    0x03FFFC2F,
                    0x03FFFFC0,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x3FFFFFF,
                    0x07FFFFFF,
                    0x003FFFFF,
                ],
                [
                    0x00000000,
                    0x00000001,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x0000000,
                    0x00000000,
                    0x00000001,
                ],
            ],
            # Prime larger than P that reduces to a value which is still
            # larger than P when it has a magnitude of 1 due to a carry to
            # bit 256 and the first and second words.
            #
            [  # 23
                [
                    0x03FFFC30,
                    0x03FFFFC0,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x03FFFFFF,
                    0x07FFFFFF,
                    0x003FFFFF,
                ],
                [
                    0x00000001,
                    0x00000001,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000000,
                    0x00000001,
                ],
            ],
        ]

        for i, (raw, normalized) in enumerate(tests):
            f = field.FieldVal()
            f.n = raw
            f.normalize()
            assert normalized == f.n, f"test {i}"

    def test_equals(self):
        """
        test_equals ensures that checking two field values for equality
        works as expected.
        """
        tests = [
            ("0", "0", True),
            ("0", "1", False),
            ("1", "0", False),
            # 2^32 - 1 == 2^32 - 1?
            ("ffffffff", "ffffffff", True),
            # 2^64 - 1 == 2^64 - 2?
            ("ffffffffffffffff", "fffffffffffffffe", False),
            # 0 == prime (mod prime)?
            (
                "0",
                "fffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f",
                True,
            ),
            # 1 == prime+1 (mod prime)?
            (
                "1",
                "fffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc30",
                True,
            ),
        ]
        for i, (a, b, eq) in enumerate(tests):
            fa = field.FieldVal.fromHex(a).normalize()
            fb = field.FieldVal.fromHex(b).normalize()
            assert fa.equals(fb) == eq, f"test {i}"

    def test_negate(self):
        """
        test_negate ensures that negating field values works as expected.
        """
        tests = [
            # zero
            ("0", "0"),
            # secp256k1 prime (direct val in with 0 out)
            ("fffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f", "0"),
            # "secp256k1 prime (0 in with direct val out)"
            ("0", "fffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f"),
            # 1 -> secp256k1 prime - 1
            ("fffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2e", "1"),
            # secp256k1 prime-1 -> 1
            ("1", "fffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2e"),
            # 2 -> secp256k1 prime-2
            ("2", "fffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2d"),
            # secp256k1 prime-2 -> 2
            ("fffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2d", "2"),
            # Random sampling
            (
                "b3d9aac9c5e43910b4385b53c7e78c21d4cd5f8e683c633aed04c233efc2e120",
                "4c2655363a1bc6ef4bc7a4ac381873de2b32a07197c39cc512fb3dcb103d1b0f",
            ),
            (
                "f8a85984fee5a12a7c8dd08830d83423c937d77c379e4a958e447a25f407733f",
                "757a67b011a5ed583722f77cf27cbdc36c82883c861b56a71bb85d90bf888f0",
            ),
            (
                "45ee6142a7fda884211e93352ed6cb2807800e419533be723a9548823ece8312",
                "ba119ebd5802577bdee16ccad12934d7f87ff1be6acc418dc56ab77cc131791d",
            ),
            (
                "53c2a668f07e411a2e473e1c3b6dcb495dec1227af27673761d44afe5b43d22b",
                "ac3d59970f81bee5d1b8c1e3c49234b6a213edd850d898c89e2bb500a4bc2a04",
            ),
        ]

        for i, (a, b) in enumerate(tests):
            fa = field.FieldVal.fromHex(a).normalize().negate(1).normalize()
            fb = field.FieldVal.fromHex(b).normalize()
            assert fa.equals(fb), f"test {i}"

    def test_add_add2(self):
        """
        test_add ensures that adding two field values together works as
        expected.
        """
        tests = [
            # zero + zero
            ("0", "0", "0"),
            # zero + one
            ("0", "1", "1"),
            # one + zero
            ("1", "0", "1"),
            # one + one
            ("1", "1", "2"),
            # secp256k1 prime-1 + 1
            (
                "fffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2e",
                "1",
                "0",
            ),
            # secp256k1 prime + 1
            (
                "fffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f",
                "1",
                "1",
            ),
            # close but over the secp256k1 prime
            (
                "fffffffffffffffffffffffffffffffffffffffffffffffffffffff000000000",
                "f1ffff000",
                "1ffff3d1",
            ),
            # Random samples.
            (
                "2b2012f975404e5065b4292fb8bed0a5d315eacf24c74d8b27e73bcc5430edcc",
                "2c3cefa4e4753e8aeec6ac4c12d99da4d78accefda3b7885d4c6bab46c86db92",
                "575d029e59b58cdb547ad57bcb986e4aaaa0b7beff02c610fcadf680c0b7c95e",
            ),
            (
                "8131e8722fe59bb189692b96c9f38de92885730f1dd39ab025daffb94c97f79c",
                "ff5454b765f0aab5f0977dcc629becc84cabeb9def48e79c6aadb2622c490fa9",
                "80863d2995d646677a00a9632c8f7ab175315ead0d1c824c9088b21c78e10b16",
            ),
            (
                "c7c95e93d0892b2b2cdd77e80eb646ea61be7a30ac7e097e9f843af73fad5c22",
                "3afe6f91a74dfc1c7f15c34907ee981656c37236d946767dd53ccad9190e437c",
                "02c7ce2577d72747abf33b3116a4df00b881ec6785c47ffc74c105d158bba36f",
            ),
            (
                "fd1c26f6a23381e5d785ba889494ec059369b888ad8431cd67d8c934b580dbe1",
                "a475aa5a31dcca90ef5b53c097d9133d6b7117474b41e7877bb199590fc0489c",
                "a191d150d4104c76c6e10e492c6dff42fedacfcff8c61954e38a628ec541284e",
            ),
            (
                "ad82b8d1cc136e23e9fd77fe2c7db1fe5a2ecbfcbde59ab3529758334f862d28",
                "4d6a4e95d6d61f4f46b528bebe152d408fd741157a28f415639347a84f6f574b",
                "faed0767a2e98d7330b2a0bcea92df3eea060d12380e8ec8b62a9fdb9ef58473",
            ),
            (
                "f3f43a2540054a86e1df98547ec1c0e157b193e5350fb4a3c3ea214b228ac5e7",
                "25706572592690ea3ddc951a1b48b504a4c83dc253756e1b96d56fdfb3199522",
                "19649f97992bdb711fbc2d6e9a0a75e5fc79d1a7888522bf5abf912bd5a45eda",
            ),
            (
                "6915bb94eef13ff1bb9b2633d997e13b9b1157c713363cc0e891416d6734f5b8",
                "11f90d6ac6fe1c4e8900b1c85fb575c251ec31b9bc34b35ada0aea1c21eded22",
                "7b0ec8ffb5ef5c40449bd7fc394d56fdecfd8980cf6af01bc29c2b898922e2da",
            ),
            (
                "48b0c9eae622eed9335b747968544eb3e75cb2dc8128388f948aa30f88cabde4",
                "0989882b52f85f9d524a3a3061a0e01f46d597839d2ba637320f4b9510c8d2d5",
                "523a5216391b4e7685a5aea9c9f52ed32e324a601e53dec6c699eea4999390b9",
            ),
        ]

        for i, (a, b, res) in enumerate(tests):
            fa = field.FieldVal.fromHex(a).normalize()
            fb = field.FieldVal.fromHex(b).normalize()
            fres = field.FieldVal.fromHex(res).normalize()
            # add
            result = fa.add(fb).normalize()
            assert fres.equals(result), f"test add {i}"
            # add2
            fa = field.FieldVal.fromHex(a).normalize()
            result = fa.add2(fa, fb).normalize()
            assert fres.equals(result), f"test add2 {i}"

    def test_mul(self):
        """
        test_mul ensures that multiplying two field values works as expected.
        """
        tests = [
            # zero * zero
            ("0", "0", "0"),
            # one * zero
            ("1", "0", "0"),
            # zero * one
            ("0", "1", "0"),
            # one * one
            ("1", "1", "1"),
            # slightly over prime
            (
                "ffffffffffffffffffffffffffffffffffffffffffffffffffffffff1ffff",
                "1000",
                "1ffff3d1",
            ),
            # secp256k1 prime-1 * 2
            (
                "fffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2e",
                "2",
                "fffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2d",
            ),
            # secp256k1 prime * 3
            (
                "fffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f",
                "3",
                "0",
            ),
            # secp256k1 prime-1 * 8
            (
                "fffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2e",
                "8",
                "fffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc27",
            ),
            # Random samples.
            (
                "cfb81753d5ef499a98ecc04c62cb7768c2e4f1740032946db1c12e405248137e",
                "58f355ad27b4d75fb7db0442452e732c436c1f7c5a7c4e214fa9cc031426a7d3",
                "1018cd2d7c2535235b71e18db9cd98027386328d2fa6a14b36ec663c4c87282b",
            ),
            (
                "26e9d61d1cdf3920e9928e85fa3df3e7556ef9ab1d14ec56d8b4fc8ed37235bf",
                "2dfc4bbe537afee979c644f8c97b31e58be5296d6dbc460091eae630c98511cf",
                "da85f48da2dc371e223a1ae63bd30b7e7ee45ae9b189ac43ff357e9ef8cf107a",
            ),
            (
                "5db64ed5afb71646c8b231585d5b2bf7e628590154e0854c4c29920b999ff351",
                "279cfae5eea5d09ade8e6a7409182f9de40981bc31c84c3d3dfe1d933f152e9a",
                "2c78fbae91792dd0b157abe3054920049b1879a7cc9d98cfda927d83be411b37",
            ),
            (
                "b66dfc1f96820b07d2bdbd559c19319a3a73c97ceb7b3d662f4fe75ecb6819e6",
                "bf774aba43e3e49eb63a6e18037d1118152568f1a3ac4ec8b89aeb6ff8008ae1",
                "c4f016558ca8e950c21c3f7fc15f640293a979c7b01754ee7f8b3340d4902ebb",
            ),
        ]

        for i, (a, b, res) in enumerate(tests):
            fa = field.FieldVal.fromHex(a).normalize()
            fb = field.FieldVal.fromHex(b).normalize()
            fres = field.FieldVal.fromHex(res).normalize()
            result = fa.mul(fb).normalize()
            assert fres.equals(result), f"test {i}"

    def test_square(self):
        """
        test_square ensures that squaring field values works as expected.
        """
        tests = [
            # zero
            ("0", "0"),
            # secp256k1 prime (direct val in with 0 out) -> 0
            ("fffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f", "0"),
            # 0 -> secp256k1 prime (direct val in with 0 out)
            ("0", "fffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f"),
            # secp256k1 prime-1
            ("fffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2e", "1"),
            # secp256k1 prime-2
            ("fffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2d", "4"),
            # Random sampling
            (
                "b0ba920360ea8436a216128047aab9766d8faf468895eb5090fc8241ec758896",
                "133896b0b69fda8ce9f648b9a3af38f345290c9eea3cbd35bafcadf7c34653d3",
            ),
            (
                "c55d0d730b1d0285a1599995938b042a756e6e8857d390165ffab480af61cbd5",
                "cd81758b3f5877cbe7e5b0a10cebfa73bcbf0957ca6453e63ee8954ab7780bee",
            ),
            (
                "e89c1f9a70d93651a1ba4bca5b78658f00de65a66014a25544d3365b0ab82324",
                "39ffc7a43e5dbef78fd5d0354fb82c6d34f5a08735e34df29da14665b43aa1f",
            ),
            (
                "7dc26186079d22bcbe1614aa20ae627e62d72f9be7ad1e99cac0feb438956f05",
                "bf86bcfc4edb3d81f916853adfda80c07c57745b008b60f560b1912f95bce8ae",
            ),
        ]

        for i, (a, res) in enumerate(tests):
            f = field.FieldVal.fromHex(a).normalize().square().normalize()
            expected = field.FieldVal.fromHex(res).normalize()
            assert f.equals(expected), f"test {i}"

    def test_string(self):
        """
        test_string ensures the stringer returns the appropriate hex string.
        """
        tests = [
            # zero
            ("0", "0000000000000000000000000000000000000000000000000000000000000000"),
            # one
            ("1", "0000000000000000000000000000000000000000000000000000000000000001"),
            # ten
            ("a", "000000000000000000000000000000000000000000000000000000000000000a"),
            # eleven
            ("b", "000000000000000000000000000000000000000000000000000000000000000b"),
            # twelve
            ("c", "000000000000000000000000000000000000000000000000000000000000000c"),
            # thirteen
            ("d", "000000000000000000000000000000000000000000000000000000000000000d"),
            # fourteen
            ("e", "000000000000000000000000000000000000000000000000000000000000000e"),
            # fifteen
            ("f", "000000000000000000000000000000000000000000000000000000000000000f"),
            # 240
            ("f0", "00000000000000000000000000000000000000000000000000000000000000f0"),
            # 2^26-1
            (
                "3ffffff",
                "0000000000000000000000000000000000000000000000000000000003ffffff",
            ),
            # 2^32-1
            (
                "ffffffff",
                "00000000000000000000000000000000000000000000000000000000ffffffff",
            ),
            # 2^64-1
            (
                "ffffffffffffffff",
                "000000000000000000000000000000000000000000000000ffffffffffffffff",
            ),
            # 2^96-1
            (
                "ffffffffffffffffffffffff",
                "0000000000000000000000000000000000000000ffffffffffffffffffffffff",
            ),
            # 2^128-1
            (
                "ffffffffffffffffffffffffffffffff",
                "00000000000000000000000000000000ffffffffffffffffffffffffffffffff",
            ),
            # 2^160-1
            (
                "ffffffffffffffffffffffffffffffffffffffff",
                "000000000000000000000000ffffffffffffffffffffffffffffffffffffffff",
            ),
            # 2^192-1
            (
                "ffffffffffffffffffffffffffffffffffffffffffffffff",
                "0000000000000000ffffffffffffffffffffffffffffffffffffffffffffffff",
            ),
            # 2^224-1
            (
                "ffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                "00000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
            ),
            # 2^256-4294968273 (the secp256k1 prime, so should result in 0)
            (
                "fffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f",
                "0000000000000000000000000000000000000000000000000000000000000000",
            ),
            # 2^256-4294968274 (the secp256k1 prime+1, so should result in 1)
            (
                "fffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc30",
                "0000000000000000000000000000000000000000000000000000000000000001",
            ),
            # # Invalid hex
            # These are silently converted in go, but allowed to raise an exception
            # in Python:
            # ("g", "0000000000000000000000000000000000000000000000000000000000000000"),
            # ("1h", "0000000000000000000000000000000000000000000000000000000000000000"),
            # ("i1", "0000000000000000000000000000000000000000000000000000000000000000"),
        ]

        for i, (a, res) in enumerate(tests):
            f = field.FieldVal.fromHex(a)
            assert res == f.string(), f"test {i}"

    def test_inverse(self):
        """
        test_inverse ensures that finding the multiplicative inverse works as
        expected.
        """
        tests = [
            # zero
            ("0", "0"),
            # secp256k1 prime (direct val in with 0 out) -> 0
            ("fffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f", "0"),
            # 0 -> secp256k1 prime (direct val in with 0 out)
            ("0", "fffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f"),
            # secp256k1 prime-1
            (
                "fffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2e",
                "fffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2e",
            ),
            # secp256k1 prime-2
            (
                "fffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2d",
                "7fffffffffffffffffffffffffffffffffffffffffffffffffffffff7ffffe17",
            ),
            # Random sampling
            (
                "16fb970147a9acc73654d4be233cc48b875ce20a2122d24f073d29bd28805aca",
                "987aeb257b063df0c6d1334051c47092b6d8766c4bf10c463786d93f5bc54354",
            ),
            (
                "69d1323ce9f1f7b3bd3c7320b0d6311408e30281e273e39a0d8c7ee1c8257919",
                "49340981fa9b8d3dad72de470b34f547ed9179c3953797d0943af67806f4bb6",
            ),
            (
                "e0debf988ae098ecda07d0b57713e97c6d213db19753e8c95aa12a2fc1cc5272",
                "64f58077b68af5b656b413ea366863f7b2819f8d27375d9c4d9804135ca220c2",
            ),
            (
                "dcd394f91f74c2ba16aad74a22bb0ed47fe857774b8f2d6c09e28bfb14642878",
                "fb848ec64d0be572a63c38fe83df5e7f3d032f60bf8c969ef67d36bf4ada22a9",
            ),
        ]

        for i, (a, e) in enumerate(tests):
            f = field.FieldVal.fromHex(a).normalize()
            expected = field.FieldVal.fromHex(e).normalize()
            result = f.inverse().normalize()
            assert result.equals(expected)
