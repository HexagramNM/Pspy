from powami.pspy import Pspy

pst = Pspy(u"ぽ")

code = [
    ["assignment", "param0", u"？"],
    ["addParamToRight", "output", "input"],
    ["ifNot", "input", u"＊",
        ["addParamToRight", "output", "input"],
        ["whileNot", "output", u"ぽぽぽぽぽぽぽぽぽぽぽぽぽぽぽぽぽぽぽぽぽぽぽぽぽぽ",
            ["addParamToRight", "output", "input"]
        ],
        ["whileNot", "output", u"＊",
            ["splitLeftCharacter", "output", "param1"],
            ["deleteRightCharacter", "output"],
        ]
    ],
    ["addParamToRight", "output", "input"],
    ["addParamToRight", "output", "param0"],
    ["addParamToLeft", "output", "param0"],
    ["assignment", "param2", "output"],
    ["powamiFlip", "param2"],
    ["powamiOr", "output", "param2"]
]

psResult = pst.exec(code)
print("")
print(psResult)

