#---[ Global Imports ]----------------------------------------------------------
from textnode import TextNode, TextType
from htmlnode import HTMLNode

#---[ Global Imports ]----------------------------------------------------------


#---[ Main Function ]-----------------------------------------------------------
def main():
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)

    return

#---[ Main Function ]-----------------------------------------------------------



#---[ Entry ]-------------------------------------------------------------------
if __name__ == "__main__":
    main()

#---[ Entry ]-------------------------------------------------------------------
