CMSYS = find("System336157.png")
ALT=find("6461HSN.png")

#
switchApp("WinJUPOS")
#CMSYS
dragDrop(Pattern("System336157.png").targetOffset(-277,-27),Pattern("System336157.png").targetOffset(50,13))
type("c", KEY_CTRL)
CMSYStext = Env.getClipboard()
#ALT
dragDrop(Pattern("6461HSN.png").targetOffset(-283,-25),Pattern("6461HSN.png").targetOffset(-17,-27))
type("c", KEY_CTRL)
ALTtext = Env.getClipboard()

#
popup(CMSYStext+\n+ALTtext)
