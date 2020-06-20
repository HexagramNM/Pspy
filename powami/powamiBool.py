
class PowamiBool:
    def __init__ (self, chara):
        self._attr = -1
        self._bool = False
        self._chara = chara
        self._encode()

    def _encode(self):
        if self._chara == u"ぽ":
            self._attr = 0
            self._bool = True
        elif self._chara == u"わ":
            self._attr = 0
            self._bool = False
        elif self._chara == u"！":
            self._attr = 1
            self._bool = True
        elif self._chara == u"？":
            self._attr = 1
            self._bool = False
        elif self._chara == u"～":
            self._attr = 2
            self._bool = True
        elif self._chara == u"ー":
            self._attr = 2
            self._bool = False
        else:
            self._attr = -1
            self._bool = False
            self._chara = u""

    def _decode(self):
        if self._attr == 0 and self._bool:
            self._chara = u"ぽ"
        elif self._attr == 0 and not self._bool:
            self._chara = u"わ"
        elif self._attr == 1 and self._bool:
            self._chara = u"！"
        elif self._attr == 1 and not self._bool:
            self._chara = u"？"
        elif self._attr == 2 and self._bool:
            self._chara = u"～"
        elif self._attr == 2 and not self._bool:
            self._chara = u"ー"
        else:
            self._attr = -1
            self._bool = False
            self._chara = u""

    def chara(self):
        return self._chara

    def __invert__(self):
        result = PowamiBool(self._chara)
        result._bool = not result._bool
        result._decode()
        return result

    def __and__(self, other):
        result = PowamiBool(u"")
        if self._attr == other._attr and self._attr != -1:
            result._attr = self._attr
            result._bool = self._bool and other._bool
            result._decode()
        return result

    def __or__(self, other):
        result = PowamiBool(u"")
        if self._attr == other._attr and self._attr != -1:
            result._attr = self._attr
            result._bool = self._bool or other._bool
            result._decode()
        return result
