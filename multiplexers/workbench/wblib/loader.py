# MIT License
#
# Copyright (c) 2021 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from TermTk import TTkUtil, TTkWidget, TTkLabel, TTkCanvas

from .colors import *

__all__ = ['WBLoader']

class WBLoader(TTkWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ANSII dumb.image.tool.py
        data = TTkUtil.base64_deflate_2_obj(
            "eJzlXE2OJbcNziKrXMEbnyAoVZX+UOvscoAAPsPcwYsB4oUBexHP2HHsQQIkQID4BgFyF5/ARwg/UlKpSPZ73e4ex0ZmRk/T3exXVRL58eOP3se//uL3H/2K//zhd/Sf" +
            "Dz5aXtE4tnKsxxq3MXb1jVcfmj/qd8/Rfjf08er7N19fhfd9DBHeUh9WWN/Vgr8k9vFP9u9yP3x5uz7fv3n9w7t//UeW5Tc/cl0fu0rRWdKtCff133YI0lhJ+C/3NmuM" +
            "V3pfb967kh1b3mT33Afdw6dX4W0bQ4SXMYzwtOay+9cLh7DRoGdd2kpN33jlL+69dyyZxs7zrr7x6sEdM7/lquoTLvSyi/DQu10Ef3j33d9ofPGwzp+qQnKfkdL/+xkq" +
            "r3SijCG/tW59GI0PKdCgOdb2GEuix0hHWYz+hFiOkPGUocvGI6yk/ZVkv1E7Uo9Q6a1yM46wLUeg/2VY3XX31oVeaeXwOyKbaOcy7eCarNXtaYxmopW+WDA7JmpsKfZh" +
            "bWktY+zjGWT8Um3pmbf5cjf4wov3KCOEFf79QQtkqOcBC/z05RyO+TW8yrA6F0hxyZzWZag+6VsmU0kA+6+Ugi5jsHApR92ODEt9c11Beg0xH7ktYNmOSlYCNf5cXR+m" +
            "V9n85Prk/UJajpqNSbOhtdFwpbZRrOVZYyp9/L8Yk/JbP1tjetxz/jjjuAfHtQ+Hiw3a0z0IuSqy2LAu1oXEZYymxytbALkdEv5SKT2ROnJxmEU4wlHR2BytX2MbQ5is" +
            "M9OtsDmpd17oflf6WW1ej7wlWSgTt9fXbcmVeRouLZLrUXE1K5mi3FyXDMRJA9mg3MA79baF3xrzdLepuVLFmhZ+ZHLJTRYbbq5PwBEWeqTSVpbAqcSj2j0IAYOWdmkq" +
            "UTP/cs6OqFLKuuDpye8/QnQ/hFc4z1OZm4TaNQYPSOQi1GAA6q5dPMtcnxNd/UKsW/3C42MhE7LQLbdxP2wNhAaBCFzYrVZN8W9TlXIkMsDiM8425G3JjcXYTEppVd7H" +
            "aFqVD3jpJRv7L2RCCa9tDQ5AljV+ehiyz7XpCnlIumd7k6TogVh7atZJy0WYtW1GDrpHmt/lyDgSGZ5j7vSMZGeYWDAVfLknizhE61PmSSw+4MtYDc2I+wEYa2sIWKIf" +
            "OCZMKwsaHWOPUQ+wfXthgHLAboe2gdjsJOGFklyxGpnnjgoUA9Tdec/MpAbz3mEKChQcqK2RsaW2G0W8Q3pRrCBdi+4TU79P2uy0mRWqAfgfUofu9MAehmVpKNt0hzYV" +
            "ZCnamOZxJu//eR9AoJx2GENxROvhsc59NCtc4VvCarEdRDkgERO6g4fKA94d5UA0GGRu5An7DYiO94VBiRGo0uyo3c6+f5ABUAi5Lat5gSwWPKHjXAQDFzNS60A4CUDp" +
            "2Ck2lSH4Z0eXy6zLhS3Vu1U4wlR4PhcBeMSL8M5uG1RobBvRgnVBUJ0dYbKmdZ0yavzbyJoFG7Mg7CdlxtwUInB8T7MRDgU6sPPcqE4COwmc0FSyhOycf0hteUkZ6BoJ" +
            "kt8qAF84pMHcsaIkwQqdW9h5a6dcIXwEPIoTuq2SPcE8/Bg22/Nj4GTA8zLoKfkQTMURDYBmTP1uiS4HVrCrtxHQWM/lYgpnNCEzDR1quPG/ZJXg5w0sg4Z3rACWwo2w" +
            "H1GJqn1hbOgmTZq/49WqMtvDxvNk/KkZv4oETjXvqpw5v0Wzw0Vq05wRLO9ij6vjIEEv4N87xSA5CnSSVbqAx48yNcE1iKB6MtBe3rvOcMixwaMwMVBJAL61bUY1LB6e" +
            "NjlZAL1k7IpDyy7qVQCMBJ6bcOFwZHX4jghvszBHD813aOG14co6r29013ddU1v7njMktw4TpNmJ4Srj6pmSIduVsMpuBwEQSEJnSvR0Rajctx9YrIgnVnBqFC7N42lE" +
            "qxBLnBlZZFgR2VisAAAiyOmZU4p8gB2b441wNfi5ZTjQMt3Cy0HBewGDO+KXNILaopLGGJyyHE4tBRuURIkGG6H/CBtRFrOA6+7T+mRxxNlRazhiZN+HIybWDafmhNCc" +
            "EUCGbxl6Eo6ytADWUkY8S99PZEbobjbnuRK4x0lCia9An7j+pZ8rcBZiGZyhMIUpDhpqgDl/11mCxK588Hr5ZZ4dYdhm5Xk/FxAM3nlnjiXCmRIFlQsrLuVxyNxgrQPM" +
            "aer3t032PLAJ2H3beCNG6uOyx8prgwklmXjfcJ2DqZMutxCyy+ONwAVpH+fJCE3Ao3uthb6MkLcbbHI05zfWF0aB988J8Lx99Ofmf4YsclL72FVe9uub+0KOJR+bk2Ui" +
            "3YwyCblYOOZ38mEImhNPDU923j/HQdHmkevoYRC9Hbkmh9aszGOG86fIcsOr3WVYfJosniiD5E3sTVLACdDrcSfqDxGr5QSetQqDqCc2gWU52OTYQ2If6rg7sat10jJy" +
            "YoWzeC4+0jtN8BhR46DJPhj4Dnu3DmXCuIuTjUyrPPOIOgprzGbJeS1I6dRymm7wTLdCZznzi68QzwWJ57T77i44DkkEK1swW3onD/hge8fr9/TvKTf3AlXG52YlVCkB" +
            "/R1t2MCSuV45U+hks/zP7DKpyKEg5e1VAFaA18ZQj3g4ZAIAshw9MkQ9nniI1QAoRj56DAscoP/a20+IO/A6NHQRDVX1ebrIFnkSzYMh06ubvAN2xCnuQggQHFF6E9hR" +
            "HrCT+QacVC0IK4jzWfGPDL7JM2RZlF5SaWjvFgAInlDzKaP4UXkPopPVJZqM0kjqohR+cV3Fyc0RQ9hkEsAHFaFXi89QE6nNyFYiOyGR9lsluHE6t4fkhCfkG6oN97pf" +
            "b+BMYTySnNat3zFAMP8qcYSxFq45vKbpE4w20XjDM/2RL7/p5YnXXewn7zR4bomCW7lkjCi3DSe7lMeQ5B1rlpMKxncDXgcJX4SEXxPBpJIrv+7NSAOKCNZzt5rByHIg" +
            "hYAsp43aEfvxj6LRtuuzMIE/ug4xo6RXy/bo/vjS3c4QiuP9HX5BfGJLQitEn3dR/N2hIhtjQM/SIcm5IbHtZN+zrN/oGIL1Ls16dU20MAIO6yV02rjCYEXjIhfsYe8m" +
            "pZTN9seBTy2n1y4AUg7otG4IAJ10IRxbbl5bl2OFe45HopvmhbMXBw9APqnnt1FKQg3AaBJITDrGxTO/GKmp6aS7vLPfRTO7haOzMAKuKz68Jdpi4EGG/PT1+KlAxCe/" +
            "DIhQsrcKmHe7OecuXd2ZoN/43BlHWLUxXPvVPr63xTOrsYEyN/r0QBksm7NQ1TYace8dGEFusEbgQcaYg4W1yrBmHZ5CgWF0fWcDAh5JaSlRANV2+jzUA9l+HRjahMNs" +
            "DYYKlxaLQ+lQXS48iWDiu3YwldBxl2rBPjw6ruAgtWD5yTXAerhTw7p7ghRUCzuyoFMAZKc4WTosZZ14EWghOiNtXwaKKLvUUu4BG1pHkI2IZ10cteDi53/ilP+p8ovV" +
            "CUYp+osyteffZN+cBNTA/B4IVyZUq5dQhfKfSa3JUeq03iJtO2U3kgbcsPi9J+DabU605ssr9xGi0+jOh+f0Yf//zwbcDGDdOCpgceVG45UVvoFYJ0B5IKRbukzvbu7D" +
            "eWddSt6WPpxygGr94AKlDEc4jNGYYOzDAc48RhNe+nCShudoDn/jlGNw8rI95GrMsXIa0AEajZ3IO4OXOWQLnVy7TJ0WMYNyEBmZk7n0Xhcx58WKkh4gRdTVoVbOgVQL" +
            "s4DqylOz88TEaLVVJIbEMkEiPE1svWL6Tgv6V0MdhaydY2Gn18OKrmgAosk4Lg4412uyH6Xq1UFPenj0zQygJR8XewSsq26R24PWZSxr5f6c6iBYjXJzXZTunL2Cl8FX" +
            "UE9axTTSEVWujpNuwmL15Xdefsw9wqFtjY5TuN21eV0BKbOHh4KygZ3XPz8XSH0KSp4/68ID3EzO38Gy0od9Z9Mgd/ZSW2HdZ43+ijbc0kof97FsqWOIMCd0eTjCYYyB" +
            "J204GZ19jKH6bTjC2xiOsKqtAMJgm90pogyTpVlV2T8xRbb3s0UASR0HKE1U2uNJH1MvFl05x1ScvnvO/Ka5eiZVgMXmB6VWnKZUNu01Nys6Vk10NIU5A/bg3aJXWWpw" +
            "oxrWyZ9hsE6OfpPEu19u3OeeN1SXcmtgUS00KF3Dty7phEt4DcFLja3c7XUV5lNGD2Dr7N2KJDGLPfXD97nOtZKHQ/SFG7NCNwjsdTkcwiunKmQMn414y/HZ0h41epNW" +
            "2tg2XnVctP8MdOqfP4R989uT3HvGUxugjm/o+oWlkQMx7fKe4NnRdKT2rPDZgNgBcu/D2TgDkHNvstbecm0i5uYVGY5GljGGBbXhWHEeo+lv6MMK63oFO2AZTor+HCLM" +
            "5/94ODnyZYymEGurWTnJsyI57BGN0Xp7Cc4UhMp0P4HU4eanDml1cPUT+IMQJJs0EHzaVA1xb8kNfeSJad7USZoD9+Zlb22zVDRGCTfz3a7e224c2K6ded1AdOka3c4D" +
            "KNAaHNDyFCdLFfm8Bam/ePXhGph9TjF5QAeyPJlqdeQKbZgrtBkJFFkxSxWZrA93PSUlNJoGSaCM7U2SGXbuduSXm8pkDuC9M84j7jt1ho+TOkrzANY9t1Hhf0Y6VTft" +
            "7Whbt97q83qXzwfQwjomPuNeK3wG1x0mcx9WWDvDiVjatPXJMR8Dk6q1S04+Vb9VzyLfKPG4AVcfu4JCSyU16ZTzKXvrt7iuBvq5+FUYxFl11R2su7CQScskrHMSkZ3b" +
            "9FvthMZB1G7jZyjNIai1I5DBMBN67Ai3dy0GSxiiqkLJ5KMkGiEJS07NYRYK5PaEA+f4MO8nbu6t2/4rozkMt11xUD1KrXqkHbfuTomSJ4ge+e6OZFqy2JbMem3O3XbR" +
            "JNVnL3tJ6sK0PEwrtrYVMyXglU+8CUiuXL1zuClXoCLP7erH5p2xmc7hzsj0/jpFnH4R5GX6uN6D2v/xuQWO2N106BimV+ZmflMjrgnz54qMPkui4fmEYEfY5ARmFquE" +
            "t3M4+U199MMgbu7DCqOM3MauNsdJsI2oviPuIJ+Opi1jNJUsfVhhJCPbaMJjWGGt7KgDL36/vArzW73K4aU6xdZL3A7g7pwqLaP3t2ddLTIa9FilZc7rXZEu81H5oe/y" +
            "YzoJOVDQGuYTlBywtk6Gz62aXY/2yD7KR9pYzZHe2xGloHGt9fhpVrhIHnYcadnZ7+wek++g2QmkNN9wdVtlcEz5T5omo9duk4VbjsNQCUGHdyAEBwX4VTKdWC16dRzD" +
            "sJMzdyGN846HPKmXx5juIcMlp/dTAa9zG/PxPC08OgY8/vjOA+GXKrgr0ZsJ6K/uvO8F3fUjmg+HKlNeVruCmwUpDdgqaJlA2TG70YnUAXvvwwFsk2p9CmDzKfX9geLz" +
            "IvR5APbCEb2krWyH6zZ6ZW4U/nsBvRtUYTwOFtWYLrVJLH/q6dE9ib0zqGPlVPpW+XHQwjTTwoWv4iVE+fzRPp8/EuK/eidA0E6KEP5sKR3nSG12fBUveSbpuU5UMDvc" +
            "sDc8TAnJ2BKSqn8YGZE4N29HcWLR4iqZC9zJPpZsyrvoElIRHG03i8REPJwsKxLAZXzGDGKQ1T1XU9MYTa2CqJWTyLEV4tiHFbZwM5jdq96Z9PpWhD/XzH94990bGv+k" +
            "8Vd8ctAf0QOJRkiebcbgmUeYnoB+TwK08bNJLWU4wuNnrlMyOnwtNF1SoxrQxs86Ro30pwM7eyvojGB7a9RvMyCMIzlgc6HHBCnwsV/bmoRgcB9nKhD5k67aT/HDIVE2" +
            "rw4QgzFa2FFB+YNtu3gS8NzxQKNRyUkF6tNOHJzuLRdoexHANqdehJWrQf5pp9LOOA4ul7mOXe3nVnDqYpk7dDZJMjoltl14aVewsAZZLyd/rDpKa+b1sq0eqouMPyQh" +
            "2f5yWm80RPfDFwjYpdVWtVuh4TUvE4fESoR+TF6fADZJstmpK+HbPTda+GmHFC6wdEoSEv3j+zef0PQ10OjT799+RtO3LwRKz4Glp0TRlsGN8Zgo+hbP0o0/l1SkRppN" +
            "PmOgdFgCweAoy+lmOZOJg+RsjeToTwMpLefXTwgEbkQMjmQLXnvMwFHcUR3JKB+YMjhO3VnSYW248rZP3dhRemmiswCI/VDAGc1EOLe6+OE7H4FaudmkEZHEIOF9YoxO" +
            "6BRGSodjmgRv5h6h7HwYjO4/SNzM5Ky/+WyAwofNiveesfHqkWXInDCVJLD+nAsd4F24iLb2m+bwZGi4U674UR/G9hOZuqErc+P56zvvfDNhplNxl3j0rvAlu/aIO5k3" +
            "+5lvbuVvvLm9kxuPaYD11gLac/Mj/H3EO9/o+nqeQotm/um3/wW9x45d")

        w,h = self.size()
        l = TTkLabel(parent=self, text=data)
        lw,lh = l.size()
        l.move((w-lw)//2,(h-lh)//2)

            #
            #      ▀▄ █ ██  █ ▖ █    █ ▝▀▀▄ ██
            #       ▗▛█ ██  █ █ █  ▗▄█ █▀▀█ ██
            #      ▝▘ █ ██  ▝▀▝▀▀ ▀▀ ▀  ▀▀  ██
            #           ██                  ██
            #        ████████            ████████
            #
            #
            #        ████████╗            ████████╗
            #        ╚══██╔══╝            ╚══██╔══╝
            #           ██║  ▄▄  ▄ ▄▄ ▄▄▖▄▖  ██║ █ ▗▖
            #   ▞▀▚ ▖▗  ██║ █▄▄█ █▀▘  █ █ █  ██║ █▟▘
            #   ▙▄▞▐▄▟  ██║ ▀▄▄▖ █    █ ▝ █  ██║ █ ▀▄
            #   ▌    ▐  ╚═╝                  ╚═╝
            #     ▚▄▄▘

    def mouseReleaseEvent(self, evt) -> bool:
        self.close()
        return True

    def paintEvent(self, canvas: TTkCanvas):
        canvas.fill(color=bgWHITE)