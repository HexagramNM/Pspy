# -*- coding: utf-8 -*-
import re
import copy
from .powamiBool import PowamiBool 

class Pspy:

    def __init__ (self, input):
        sanitizedInput = u""
        self._powamiChara = [u"ぽ", u"わ", u"！", u"？", u"～", u"ー"]
        for char in input:
            if char in self._powamiChara:
                sanitizedInput = sanitizedInput + char

        self._paramDict = dict()
        self._paramDict["input"] = [sanitizedInput, u"ぽ～わ"]
        self._paramDict["output"] = [u"", u"わ～ぽ"]
        self._paramDict["paramP"] = [u"ぽ", u"ぽぽぽ"]
        self._paramDict["paramW"] = [u"わ", u"わわわ"]
        self._paramDict["param0"] = [u"", u"ぽぽわ"]
        self._paramDict["param1"] = [u"", u"ぽわぽ"]
        self._paramDict["param2"] = [u"", u"わぽぽ"]
        self._paramDict["param3"] = [u"", u"ぽわわ"]
        self._paramDict["param4"] = [u"", u"わぽわ"]
        self._paramDict["param5"] = [u"", u"わわぽ"]
        self._paramDictKey = ["input", "output", "paramP", "paramW", \
            "param0", "param1", "param2", "param3", "param4", "param5"]
        self._translatedPs = u""
        #0...内部処理・翻訳、1...内部処理のみ, 2...翻訳のみ
        self._mode = 0

    def _processCode(self, code, depth = 0):
        if len(code) == 0:
            raise(u"エラー")
        if code[0] == "assignment":
            if len(code) < 3:
                raise(u"エラー")
            self._assignment(code[1], code[2])

        elif code[0] == "addParamToRight":
            if len(code) < 3:
                raise(u"エラー")
            self._addParamToRight(code[1], code[2])

        elif code[0] == "addParamToLeft":
            if len(code) < 3:
                raise(u"エラー")
            self._addParamToLeft(code[1], code[2])

        elif code[0] == "splitRightCharacter":
            if len(code) < 3:
                raise(u"エラー")
            self._splitRightCharacter(code[1], code[2])

        elif code[0] == "splitLeftCharacter":
            if len(code) < 3:
                raise(u"エラー")
            self._splitLeftCharacter(code[1], code[2])

        elif code[0] == "deleteRightCharacter":
            if len(code) < 2:
                raise(u"エラー")
            self._deleteRightCharacter(code[1])

        elif code[0] == "deleteLeftCharacter":
            if len(code) < 2:
                raise(u"エラー")
            self._deleteLeftCharacter(code[1])

        elif code[0] == "powamiFlip":
            if len(code) < 2:
                raise(u"エラー")
            self._powamiFlip(code[1])

        elif code[0] == "powamiAnd":
            if len(code) < 3:
                raise(u"エラー")
            self._powamiAnd(code[1], code[2])

        elif code[0] == "powamiOr":
            if len(code) < 3:
                raise(u"エラー")
            self._powamiOr(code[1], code[2])

        elif code[0] == "if":
            if len(code) < 4:
                raise(u"エラー")
            block = []
            for i in range(3, len(code)):
                block.append(code[i])
            self._psIf(code[1], code[2], block, depth)

        elif code[0] == "ifNot":
            if len(code) < 4:
                raise(u"エラー")
            block = []
            for i in range(3, len(code)):
                block.append(code[i])
            self._psIfNot(code[1], code[2], block, depth)

        elif code[0] == "while":
            if len(code) < 4:
                raise(u"エラー")
            block = []
            for i in range(3, len(code)):
                block.append(code[i])
            self._psWhile(code[1], code[2], block, depth)

        elif code[0] == "whileNot":
            if len(code) < 4:
                raise(u"エラー")
            block = []
            for i in range(3, len(code)):
                block.append(code[i])
            self._psWhileNot(code[1], code[2], block, depth)

        else:
            raise(u"不正な単語")

    def exec(self, codeList):
        for code in codeList:
            self._processCode(code)    

        print(self._paramDict["output"][0])
        return self._translatedPs

    def _validateTwoKeys(self, dest, src, raiseException=True):
        if self._validateKey(dest, raiseException):
            return False
        if self._validateKey(src, raiseException):
            return False

        return True

    def _validateKey(self, paramKey, raiseException=True):
        if not paramKey in self._paramDictKey:
            if raiseException:
                raise(paramKey + u"の名前が不正です。正しい名前：" + ",",join(self._paramDictKey))
            return False
        return True

    def _validatePowaValue(self, value, raiseException=True):
        validCharaList = [u"ぽ", u"わ", u"！", u"？", u"ー", u"～"]
        for char in value:
            if not char in validCharaList:
                if raiseException:
                    raise(value + u"：ぽわみ文字列に対し、不正な文字が使われております。")
                return False
        return True

    def psIf(self, dest, pattern, block):
        self._validateKey(dest)

    #制御構文
    def _validatePattern(self, pattern, raiseException=True):
        validCharaList = [u"ぽ", u"わ", u"＊", u"．", u"？", u"￥"]
        for char in pattern:
            if not char in validCharaList:
                if raiseException:
                    raise(u"制御構文内のパターンに不正な文字が使われております。")
                return False

        return True

    def _ps_pattern_match(self, param, pattern):
        #＊（～）と？は自身も含むので注意。．はもともと自身も含むので問題なし
        reStr = ""
        if pattern == u"＊":
            #"＊"のみは空文字列のみとマッチ（例外）
            reStr = "^$"
        else:
            patternParts = []
            tmpPart = ""
            escape = False
            for char in pattern:
                if not escape:
                    if char == u"￥":
                        escape = True
                        return
                    elif char == u"．":
                        tmpPart += "."
                    elif char == u"＊":
                        patternParts.append(tmpPart)
                        patternParts.append("*")
                        tmpPart = ""
                    elif char == u"？":
                        patternParts.append(tmpPart)
                        patternParts.append("?")
                        tmpPart = ""
                    else:
                        tmpPart += char
                else:
                    if char == u"＊":
                        tmpPart += u"～"
                    elif char == u"．":
                        tmpPart += u"ー"
                    elif char == u"￥":
                        tmpPart += u"！"
                    else:
                        tmpPart += char

                escape = False

            patternParts.append(tmpPart)
            specialWordNum = len(patternParts) // 2

            reStr = "^("
            for i in range(2 ** specialWordNum):
                if i > 0:
                    reStr += "|" 
                currentParts = copy.deepcopy(patternParts)
                for place in range(specialWordNum):
                    if ((i // (2 ** place)) % 2 == 1):
                        if currentParts[2 * place + 1] == "*":
                            currentParts[2 * place + 1] = u"＊"
                        elif currentParts[2 * place + 1] == "?":
                            currentParts[2 * place + 1] = u"？"
                reStr += "".join(currentParts)
        
            reStr += ")$"

        reObj = re.compile(reStr)
        return (reObj.fullmatch(self._paramDict[param][0]) != None)

    def _translatePattern(self, pattern):
        result = pattern
        result = result.replace(u"＊", u"～")
        result = result.replace(u"．", u"ー")
        result = result.replace(u"￥", u"！")
        return result

    def _psIf(self, param, pattern, block, depth = 0):
        self._validateKey(param)
        self._validatePattern(pattern)

        #コード実行
        if depth == 0:
            self._mode = 1
        if self._mode == 0 or self._mode == 1:
            if self._ps_pattern_match(param, pattern):
                for code in block:
                    self._processCode(code, depth+1)
        #PS翻訳
        if depth == 0:
            self._mode = 2
        if self._mode == 0 or self._mode == 2:
            self._translatedPs += u"ぽ？" + self._paramDict[param][1] \
                + self._translatePattern(pattern) + "っ"
            for code in block:
                self._processCode(code, depth+1)
            self._translatedPs += "っ"
        if depth == 0:
            self._mode = 0

    def _psIfNot(self, param, pattern, block, depth = 0):
        self._validateKey(param)
        self._validatePattern(pattern)

        #コード実行
        if depth == 0:
            self._mode = 1
        if self._mode == 0 or self._mode == 1:
            if not self._ps_pattern_match(param, pattern):
                for code in block:
                    self._processCode(code, depth+1)
        #PS翻訳
        if depth == 0:
            self._mode = 2
        if self._mode == 0 or self._mode == 2:
            self._translatedPs += u"ぽ！？" + self._paramDict[param][1] \
                + self._translatePattern(pattern) + "っ"
            for code in block:
                self._processCode(code, depth+1)
            self._translatedPs += "っ"
        if depth == 0:
            self._mode = 0

    def _psWhile(self, param, pattern, block, depth = 0):
        self._validateKey(param)
        self._validatePattern(pattern)

        #コード実行
        if depth == 0:
            self._mode = 1
        if self._mode == 0 or self._mode == 1:
            count = 0
            while self._ps_pattern_match(param, pattern):
                for code in block:
                    self._processCode(code, depth+1)
                count += 1
                if count > 1000:
                    raise("ループ回数が1000回を超えました")
        #PS翻訳
        if depth == 0:
            self._mode = 2
        if self._mode == 0 or self._mode == 2:
            self._translatedPs += u"わ？" + self._paramDict[param][1] \
                + self._translatePattern(pattern) + "っ"
            for code in block:
                self._processCode(code, depth+1)
            self._translatedPs += "っ"
        if depth == 0:
            self._mode = 0

    def _psWhileNot(self, param, pattern, block, depth = 0):
        self._validateKey(param)
        self._validatePattern(pattern)

        #コード実行
        if depth == 0:
            self._mode = 1
        if self._mode == 0 or self._mode == 1:
            count = 0
            while not self._ps_pattern_match(param, pattern):
                for code in block:
                    self._processCode(code, depth+1)
                count += 1
                if count > 1000:
                    raise("ループ回数が1000回を超えました")
        #PS翻訳
        if depth == 0:
            self._mode = 2
        if self._mode == 0 or self._mode == 2:
            self._translatedPs += u"わ！？" + self._paramDict[param][1] \
                + self._translatePattern(pattern) + "っ"
            for code in block:
                self._processCode(code, depth+1)
            self._translatedPs += "っ"
        if depth == 0:
            self._mode = 0

    #命令語
    def _assignment(self, dest, value):
        self._validateKey(dest)
        valueMode = -1
        if self._validatePowaValue(value, False):
            valueMode = 0
        elif self._validateKey(value, False):
            valueMode = 1
        else:
            raise("代入元の指定が不正です："+value)
        
        if self._mode == 0 or self._mode == 1:
            if valueMode == 0:
                self._paramDict[dest][0] = value
            elif valueMode == 1:
                self._paramDict[dest][0] = self._paramDict[value][0]
        if self._mode == 0 or self._mode == 2:
            if valueMode == 0:
                self._translatedPs += u"ぽわ～" + self._paramDict[dest][1] + value + u"っ"
            elif valueMode == 1:
                self._translatedPs += u"わぽ～" + self._paramDict[dest][1] + self._paramDict[value][1]

    def _addParamToRight(self, dest, src):
        self._validateTwoKeys(dest, src)
        if self._mode == 0 or self._mode == 1:
            self._paramDict[dest][0] = self._paramDict[dest][0] + self._paramDict[src][0]
        if self._mode == 0 or self._mode == 2:
            self._translatedPs += u"ぽ～～" + self._paramDict[dest][1] + self._paramDict[src][1]

    def _addParamToLeft(self, dest, src):
        self._validateTwoKeys(dest, src)
        if self._mode == 0 or self._mode == 1:
            self._paramDict[dest][0] = self._paramDict[src][0] + self._paramDict[dest][0]
        if self._mode == 0 or self._mode == 2:
            self._translatedPs += u"わ～～" + self._paramDict[dest][1] + self._paramDict[src][1]

    def _splitRightCharacter(self, target, charParam):
        self._validateTwoKeys(target, charParam)
        if self._mode == 0 or self._mode == 1:
            if len(self._paramDict[target][0]) <= 0:
                self._paramDict[charParam][0] = u""
                self._paramDict[target][0] = u""
            else:
                self._paramDict[charParam][0] = self._paramDict[target][0][-1]
                self._paramDict[target][0] = self._paramDict[target][0][0:-1]
        if self._mode == 0 or self._mode == 2:
            self._translatedPs += u"ぽーー" + self._paramDict[target][1] + self._paramDict[charParam][1]

    def _splitLeftCharacter(self, target, charParam):
        self._validateTwoKeys(target, charParam)
        if self._mode == 0 or self._mode == 1:
            if len(self._paramDict[target][0]) <= 0:
                self._paramDict[charParam][0] = u""
                self._paramDict[target][0] = u""
            else:
                self._paramDict[charParam][0] = self._paramDict[target][0][0]
                self._paramDict[target][0] = self._paramDict[target][0][1:]
        if self._mode == 0 or self._mode == 2:
            self._translatedPs += u"わーー" + self._paramDict[target][1] + self._paramDict[charParam][1]
        
    def _deleteRightCharacter(self, target):
        self._validateKey(target)
        if self._mode == 0 or self._mode == 1:
            if len(self._paramDict[target][0]) <= 0:
                self._paramDict[target][0] = u""
            else:
                self._paramDict[target][0] = self._paramDict[target][0][0:-1]
        if self._mode == 0 or self._mode == 2:
            self._translatedPs += u"ぽー！" + self._paramDict[target][1]

    def _deleteLeftCharacter(self, target):
        self._validateKey(target)
        if self._mode == 0 or self._mode == 1:
            if len(self._paramDict[target][0]) <= 0:
                self._paramDict[target][0] = u""
            else:
                self._paramDict[target][0] = self._paramDict[target][0][1:]
        if self._mode == 0 or self._mode == 2:
            self._translatedPs += u"わー！" + self._paramDict[target][1]

    def _powamiFlip(self, target):
        self._validateKey(target)
        if self._mode == 0 or self._mode == 1:
            result = u""
            for chara in self._paramDict[target][0]:
                powami = PowamiBool(chara)
                result += (~powami).chara()
            self._paramDict[target][0] = result
        if self._mode == 0 or self._mode == 2:
            self._translatedPs += u"ぽーわわ" + self._paramDict[target][1]

    def _powamiAnd(self, dest, src):
        self._validateTwoKeys(dest, src)
        if self._mode == 0 or self._mode == 1:
            result = u""
            minLen = min(len(self._paramDict[dest][0]), len(self._paramDict[src][0]))
            for i in range(minLen):
                powami1 = PowamiBool(self._paramDict[dest][0][i])
                powami2 = PowamiBool(self._paramDict[src][0][i])
                result += (powami1 & powami2).chara()
            self._paramDict[dest][0] = result
        if self._mode == 0 or self._mode == 2:
            self._translatedPs += u"ぽぽ" + self._paramDict[dest][1] + self._paramDict[src][1]

    def _powamiOr(self, dest, src):
        self._validateTwoKeys(dest, src)
        if self._mode == 0 or self._mode == 1:
            result = u""
            minLen = min(len(self._paramDict[dest][0]), len(self._paramDict[src][0]))
            for i in range(minLen):
                powami1 = PowamiBool(self._paramDict[dest][0][i])
                powami2 = PowamiBool(self._paramDict[src][0][i])
                result += (powami1 | powami2).chara()
            self._paramDict[dest][0] = result
        if self._mode == 0 or self._mode == 2:
            self._translatedPs += u"わわ" + self._paramDict[dest][1] + self._paramDict[src][1]
            


